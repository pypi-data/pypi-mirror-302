#!/usr/bin/env python3
# encoding: utf-8

from __future__ import annotations

__author__ = "ChenyangGao <https://chenyanggao.github.io>"
__all__ = ["relogin_wrap_maker", "crack_captcha"]

from asyncio import Lock as AsyncLock
from collections import defaultdict, ChainMap
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager, AbstractContextManager
from inspect import isawaitable
from sys import _getframe
from threading import Lock
from typing import cast, Any
from weakref import WeakKeyDictionary

from concurrenttools import thread_pool_batch
from p115client.client import default_check_for_relogin
from p115.component.client import P115Client


CAPTCHA_CRACK: Callable[[bytes], str]


# TODO: 支持异步
def relogin_wrap_maker(
    relogin: None | Callable[[], Any] = None, 
    client: None | P115Client = None, 
    check_for_relogin: Callable[[BaseException], bool | int] = default_check_for_relogin, 
    lock: None | AbstractContextManager | AbstractAsyncContextManager = None,   
) -> Callable:
    """包装调用：执行调用，成功则返回，当遇到特定错误则重新登录后循环此流程

    :param relogin: 调用以自定义重新登录，如果为 None，则用默认的重新登录
    :param client: 115 客户端或 cookies，当 relogin 为 None 时被使用
    :param check_for_relogin: 检查以确定是否要重新登录，如果为 False，则抛出异常
        - 如果值为 bool，如果为 True，则重新登录
        - 如果值为 int，则视为返回码，当值为 405 时会重新登录
    :param lock: 如果不为 None，执行调用时加这个锁（或上下文管理器）

    :return: 返回函数，用于执行调用，必要时会重新登录再重试
    """
    from httpx import HTTPStatusError

    if relogin is None:
        d: WeakKeyDictionary[P115Client, tuple[AbstractContextManager, AbstractAsyncContextManager]] = WeakKeyDictionary()
    def wrapper(func, /, *args, **kwargs):
        nonlocal client
        if relogin is None:
            if client is None:
                f = func
                while hasattr(f, "__wrapped__"):
                    f = f.__wrapped__
                if hasattr(f, "__self__"):
                    f = f.__self__
                if isinstance(f, P115Client):
                    client = f
                elif hasattr(f, "client"):
                    client = f.client
                else:
                    frame = _getframe(1)
                    client = ChainMap(frame.f_locals, frame.f_globals, frame.f_builtins)["client"]
            elif not isinstance(client, P115Client):
                client = P115Client(client)
            if not isinstance(client, P115Client):
                raise ValueError("no awailable client")
            try:
                relogin_lock, relogin_alock = d[client]
            except KeyError:
                relogin_lock, relogin_alock = d[client] = (Lock(), AsyncLock())
        is_cm = isinstance(lock, AbstractContextManager)
        while True:
            try:
                if is_cm:
                    with cast(AbstractContextManager, lock):
                        ret = func(*args, **kwargs)
                else:
                    ret = func(*args, **kwargs)
                if isawaitable(ret):
                    is_acm = isinstance(lock, AbstractAsyncContextManager)
                    async def wrap(ret):
                        while True:
                            try:
                                if is_cm:
                                    with cast(AbstractContextManager, lock):
                                        return await ret
                                elif is_acm:
                                    async with cast(AbstractAsyncContextManager, lock):
                                        return await ret
                                else:
                                    return await ret
                            except BaseException as e:
                                res = check_for_relogin(e)
                                if isawaitable(res):
                                    res = await res
                                if not res if isinstance(res, bool) else res != 405:
                                    raise
                                if relogin is None:
                                    client = cast(P115Client, client)
                                    cookies = client.cookies
                                    async with relogin_alock:
                                        if cookies == client.cookies:
                                            await client.login_another_app(replace=True, async_=True)
                                else:
                                    res = relogin()
                                    if isawaitable(res):
                                        await res
                                ret = func(*args, **kwargs)
                    return wrap(ret)
                else:
                    return ret
            except HTTPStatusError as e:
                res = check_for_relogin(e)
                if not res if isinstance(res, bool) else res != 405:
                    raise
                if relogin is None:
                    client = cast(P115Client, client)
                    cookies = client.cookies
                    with relogin_lock:
                        if cookies == client.cookies:
                            client.login_another_app(replace=True)
                else:
                    relogin()
    return wrapper


def crack_captcha(
    client: str | P115Client, 
    sample_count: int = 16, 
    crack: None | Callable[[bytes], str] = None, 
) -> bool:
    """破解 115 的图片验证码。如果返回 True，则说明破解成功，否则失败。如果失败，就不妨多运行这个函数几次。

    :param client: 115 客户端或 cookies
    :param sample_count: 单个文字的采样次数，共会执行 10 * sample_count 次识别
    :param crack: 破解验证码图片，输入图片的二进制数据，输出识别的字符串

    :return: 是否破解成功

    你可以反复尝试，直到破解成功，代码如下

        while not crack_captcha(client):
            pass

    如果你需要检测是否存在验证码，然后进行破解，代码如下

        resp = client.download_url_web("a")
        if not resp["state"] and resp["code"] == 911:
            print("出现验证码，尝试破解")
            while not crack_captcha(client):
                print("破解失败，再次尝试")
    """
    global CAPTCHA_CRACK
    if crack is None:
        try:
            crack = CAPTCHA_CRACK
        except NameError:
            try:
                # https://pypi.org/project/ddddocr/
                from ddddocr import DdddOcr
            except ImportError:
                from subprocess import run
                from sys import executable
                run([executable, "-m", "pip", "install", "-U", "ddddocr==1.4.11"], check=True)
                from ddddocr import DdddOcr # type: ignore
            crack = CAPTCHA_CRACK = cast(Callable[[bytes], str], DdddOcr(show_ad=False).classification)
    if not isinstance(client, P115Client):
        client = P115Client(client)
    while True:
        captcha = crack(client.captcha_code())
        if len(captcha) == 4 and all("\u4E00" <= char <= "\u9FFF" for char in captcha):
            break
    ls: list[defaultdict[str, int]] = [defaultdict(int) for _ in range(10)]
    def crack_single(i, submit):
        try:
            char = crack(client.captcha_single(i))
            if len(char) == 1 and "\u4E00" <= char <= "\u9FFF":
                ls[i][char] += 1
            else:
                submit(i)
        except:
            submit(i)
    thread_pool_batch(crack_single, (i for i in range(10) for _ in range(sample_count)))
    l: list[str] = [max(d, key=lambda k: d[k]) for d in ls]
    try:
        code = "".join(str(l.index(char)) for char in captcha)
    except ValueError:
        return False
    resp = client.captcha_verify(code)
    return resp["state"]

