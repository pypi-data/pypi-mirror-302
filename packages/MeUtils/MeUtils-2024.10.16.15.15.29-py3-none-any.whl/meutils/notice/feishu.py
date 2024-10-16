#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : feishu
# @Time         : 2021/1/20 6:04 下午
# @Author       : yuanjie
# @Email        : meutils@qq.com
# @Software     : PyCharm
# @Description  : todo: 输出json优化

from meutils.pipe import *


@background_task
def send_message(
        content: Any = '',
        title: Optional[str] = '',
        message: Optional[Dict] = None,
        url: Optional[str] = None,
        n: int = 1,
):
    if any(i in str(content).lower() for i in {'重定向', 'pass'}):
        return

    if any((content, title)):

        if isinstance(content, str):  # todo: post_process
            content = content.replace("<", "【").replace(">", "】")
            contents = [content]
            # contents = [{"a": 1}]*3

        elif isinstance(content, (list,)):
            contents = list(map(bjson, content))

        elif isinstance(content, (dict,)):
            contents = [bjson(content)]

        elif isinstance(content, BaseModel):
            contents = [content.model_dump_json(indent=4)]

        else:
            contents = [str(content)]

        message = message or {
            "msg_type": "interactive",
            "card": {
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "content": str(content),
                            "tag": "lark_md"
                        }
                    } for content in contents
                ],
                "header": {
                    "title": {
                        "content": str(title).title(),
                        "tag": "plain_text"
                    }
                }
            }
        }
        url = url or "https://open.feishu.cn/open-apis/bot/v2/hook/f7cf6f2a-30da-4e7a-ae6f-b48c8bb1ecf8"  # 测试群
        r = None
        for i in range(n):
            time.sleep(i ** 2)
            r = httpx.post(url, json=message)
        return r and r.text


@decorator
def catch(
        fn: Callable,
        task_name: Optional[str] = None,
        trace: bool = True,
        url: Optional[str] = None,
        *args,
        **kwargs
):
    task_name = task_name or fn.__name__
    r = None
    try:
        # s = time.perf_counter()
        r = fn(*args, **kwargs)
        # content = f"Task done in {time.perf_counter() - s:.2f} s"

    except Exception as e:
        content = str(e)
        if trace:
            content = traceback.format_exc()
        send_message(title=task_name, content=content, url=url, n=3)

    return r


if __name__ == '__main__':
    send_message("xxx", title=None)

    # @catch(task_name='这是一个任务名')
    # def f():
    #     time.sleep(3)
    #     1 / 0
    #
    #
    # f()
    # with timer():
    #     send_message(BaseModel, title='GitHub Copilot Chat Error')

    # print(bjson(['a']))
