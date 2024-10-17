#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_images
# @Time         : 2024/10/16 08:54
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from openai import AsyncOpenAI

from meutils.pipe import *
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.llm.openai_utils import to_openai_images_params
from meutils.llm.check_utils import check_token_for_siliconflow

from meutils.schemas.image_types import ImageRequest, FluxImageRequest
from meutils.notice.feishu import IMAGES, send_message as _send_message

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=3aA5dH"
FEISHU_URL_FREE = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=xlvlrH"

BASE_URL = os.getenv("SILICONFLOW_BASE_URL")

DEFAULT_MODEL = "black-forest-labs/FLUX.1-schnell"
MODELS = {

    "flux.1-schnell": "black-forest-labs/FLUX.1-schnell",
    "flux.1-dev": "black-forest-labs/FLUX.1-dev",
    "flux.1-pro": "black-forest-labs/FLUX.1-dev",

    "flux-schnell": "black-forest-labs/FLUX.1-schnell",
    "flux-dev": "black-forest-labs/FLUX.1-dev",
    "flux-pro": "black-forest-labs/FLUX.1-dev",

    "stable-diffusion-xl-base-1.0": "stabilityai/stable-diffusion-xl-base-1.0",  # 图生图
    "stable-diffusion-2-1": "stabilityai/stable-diffusion-2-1",  # 图生图

    "stable-diffusion": "stabilityai/stable-diffusion-3-medium",
    "stable-diffusion-3-medium": "stabilityai/stable-diffusion-3-medium",
    "stable-diffusion-3": "stabilityai/stable-diffusion-3-medium",

}

send_message = partial(
    _send_message,
    title=__name__,
    url=IMAGES
)
check_token = partial(check_token_for_siliconflow, threshold=0.1)


async def generate(request: ImageRequest, redirect_model: Optional[str] = None, api_key: Optional[str] = None):
    request.model = MODELS.get(request.model, DEFAULT_MODEL)

    if any(i in request.model.lower() for i in {"dev", "pro"}):
        api_key = api_key or await get_next_token_for_polling(FEISHU_URL, check_token=check_token)
        request.num_inference_steps = 20
    else:
        api_key = api_key or await get_next_token_for_polling(FEISHU_URL_FREE, from_redis=True)

    data = to_openai_images_params(request)
    logger.debug(data)

    for i in range(5):
        try:
            client = AsyncOpenAI(base_url=BASE_URL, api_key=api_key)
            response = await client.images.generate(**data)
            # response.model = redirect_model or request.model
            response.model = ""

            return response
        except Exception as e:
            logger.error(e)
            if i > 2:
                send_message(f"生成失败: {e}\n\n{api_key}\n\n{request.model_dump_json(indent=4, exclude_none=True)}")


if __name__ == '__main__':
    from meutils.pipe import *

    request = FluxImageRequest(model="flux.1-dev", prompt="a dog", size="1024x1024")
    print(any(i in request.model.lower() for i in {"dev", "pro"}))

    arun(generate(request))
