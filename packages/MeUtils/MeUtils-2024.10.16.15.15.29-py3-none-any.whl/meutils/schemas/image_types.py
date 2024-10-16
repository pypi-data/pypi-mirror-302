#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : image_types
# @Time         : 2024/8/21 14:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import time

from meutils.pipe import *

ASPECT_RATIOS = {
    "1:1": "1024x1024",

    "1:2": "512x1024",
    "2:1": "1024x512",

    '2:3': "768x512",
    '3:2': "512x768",

    "4:3": "1280x960",  # "1024x768"
    "3:4": "960x1280",

    "5:4": "1280x960",
    "4:5": "960x1280",

    "16:9": "1366x768",  # "1024x576"
    "9:16": "768x1366",

    "21:9": "1344x576",
}


# prompt: str,
#         model: Union[str, ImageModel, None] | NotGiven = NOT_GIVEN,
#         n: Optional[int] | NotGiven = NOT_GIVEN,


class ImageRequest(BaseModel):  # openai
    prompt: str = ""
    negative_prompt: Optional[str] = None

    model: Optional[str] = None

    n: Optional[int] = 1

    quality: Optional[Literal["standard", "hd"]] = None
    style: Union[str, Literal["vivid", "natural"]] = None
    size: Optional[Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]] = '1024x1024'  # 测试默认值

    response_format: Optional[Literal["url", "b64_json"]] = "url"
    user: Optional[str] = None

    seed: Optional[int] = None

    # 拓展：垫图
    # image: Optional[str] = None

    class Config:
        # frozen = True
        # populate_by_name = True

        json_schema_extra = {
            "examples": [
                {
                    "model": "stable-diffusion-3-medium",  # sd3
                    "prompt": "画条狗",
                },
            ]
        }


class FluxImageRequest(ImageRequest):
    image_size: str

    num_inference_steps: int = 50
    prompt_enhancement: bool = True


class FluxProImageRequest(ImageRequest):  # together
    steps: int = 20

    height: int = 1024
    width: int = 1024


class SDImageRequest(ImageRequest):
    image_size: str
    batch_size: int
    guidance_scale: float
    num_inference_steps: int


class HunyuanImageRequest(ImageRequest):
    image_size: str
    batch_size: int
    guidance_scale: float
    num_inference_steps: int


class KlingImageRequest(ImageRequest):
    image_size: str
    batch_size: int
    guidance_scale: float
    num_inference_steps: int


class CogImageRequest(ImageRequest):
    image_size: str
    batch_size: int
    guidance_scale: float
    num_inference_steps: int


class StepImageRequest(ImageRequest):
    image_size: str
    batch_size: int
    guidance_scale: float
    num_inference_steps: int


if __name__ == '__main__':
    # print(ASPECT_RATIOS.items())

    # ImageRequest(quality=1)
    @lru_cache()
    def f(r):
        return r

    # f(FluxImageRequest(prompt="xx"))

    from openai import OpenAI
    from meutils.llm.openai_utils import to_openai_images_params

    data = to_openai_images_params(ImageRequest(prompt="a dog"))

    print(data)

    # OpenAI().images.generate(**ImageRequest(prompt="a dog").model_dump())
