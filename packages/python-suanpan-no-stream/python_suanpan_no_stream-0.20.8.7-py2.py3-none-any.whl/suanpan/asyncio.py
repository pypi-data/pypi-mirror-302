# coding=utf-8
from __future__ import absolute_import, print_function
import concurrent.futures
import time
import asyncio
from suanpan.utils import pbar as spbar

def imap(func, iterable, timeout=None, max_workers=None, pbar=None, **kwargs):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(func, i): i for i in iterable}
        total = len(futures)
        iterable, _ = spbar.getIterableLen(futures, config=pbar, total=total)
        for future in concurrent.futures.as_completed(futures, timeout=timeout):
            if future.exception() is not None:
                raise future.exception()
            yield future.result()

def map(func, iterable, timeout=None, max_workers=None, pbar=None, **kwargs):
    return list(imap(func, iterable, timeout=timeout, max_workers=max_workers, pbar=pbar, **kwargs))

def istarmap(func, iterable, timeout=None, max_workers=None, pbar=None, **kwargs):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(func, *i): i for i in iterable}
        total = len(futures)
        iterable, _ = spbar.getIterableLen(futures, config=pbar, total=total)
        for future in concurrent.futures.as_completed(futures, timeout=timeout):
            if future.exception() is not None:
                raise future.exception()
            yield future.result()

def starmap(func, iterable, timeout=None, max_workers=None, pbar=None, **kwargs):
    return list(istarmap(func, iterable, timeout=timeout, max_workers=max_workers, pbar=pbar, **kwargs))

def run(funcs, *args, max_workers=None, **kwargs):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        return [executor.submit(func, *args, **kwargs) for func in funcs]

def wait(objects, timeout=None, pbar=None, **kwargs):
    return list(iwait(objects, timeout=timeout, pbar=pbar, **kwargs))

def iwait(objects, timeout=None, pbar=None, **kwargs):
    iterable, total = spbar.getIterableLen(objects, config=pbar, total=len(objects))
    for obj in concurrent.futures.as_completed(objects, timeout=timeout):
        if obj.exception() is not None:
            raise obj.exception()
        yield obj.result()

def sleep(seconds=0):
    if asyncio.iscoroutinefunction(sleep):
        return asyncio.sleep(seconds)
    else:
        return time.sleep(seconds)

def switch():
    return sleep(0)

def kill(futures, exception=None, block=True, timeout=None):
    for future in futures:
        if isinstance(future, concurrent.futures.Future):
            future.cancel()
    if block:
        concurrent.futures.wait(futures, timeout=timeout)

def current():
    try:
        return asyncio.current_task()
    except RuntimeError:
        return None