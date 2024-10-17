#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : image_types
# @Time         : 2024/8/21 14:18
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

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

    model: str = ""

    n: Optional[int] = 1

    quality: Optional[Literal["standard", "hd"]] = None
    style: Union[str, Literal["vivid", "natural"]] = None
    size: str = '1024x1024'  # 测试默认值 Optional[Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]]

    response_format: Optional[Literal["url", "b64_json"]] = "url"
    user: Optional[str] = None

    seed: Optional[int] = None

    prompt_enhancement: bool = True  # 翻译or润色

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.size = self.size if 'x' in self.size else '512x512'

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
    image_size: Optional[str] = None

    num_inference_steps: Optional[int] = None
    prompt_enhancement: bool = True

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.image_size = self.size


class TogetherImageRequest(ImageRequest):  # together
    steps: Optional[int] = None

    height: int = 1024
    width: int = 1024

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        try:
            self.width, self.height = map(int, self.size.split('x'))
        except Exception as e:
            logger.error(e)


class SDImageRequest(ImageRequest):
    image_size: str
    batch_size: int
    guidance_scale: float
    num_inference_steps: int

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.image_size = self.size


class HunyuanImageRequest(ImageRequest):
    size: Literal["1:1", "3:4", "4:3", "9:16", "16:9"] = "1:1"
    style: Optional[Literal[
        '摄影',
        '童话世界',
        '奇趣卡通',
        '二次元',
        '纯真动漫',

        '清新日漫',
        '3D'
        '赛博朋克',
        '像素',
        '极简',

        '复古',
        '暗黑系',
        '波普风',
        '中国风',
        '国潮',

        '糖果色',
        '胶片电影',
        '素描',
        '水墨画',
        '油画',

        '水彩',
        '粉笔',
        '粘土',
        '毛毡',
        '贴纸',

        '剪纸',
        '刺绣',
        '彩铅',
        '梵高',
        '莫奈',

        '穆夏',
        '毕加索',
    ]] = None

    def __init__(self, /, **data: Any):
        super().__init__(**data)


class KlingImageRequest(ImageRequest):
    image_size: str
    batch_size: int
    guidance_scale: float
    num_inference_steps: int


class CogviewImageRequest(ImageRequest):
    size: Optional[Literal["1024x1024", "768x1344", "864x1152", "1344x768", "1152x864", "1440x720", "720x1440"]] = None


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

    # from openai import OpenAI
    # from meutils.llm.openai_utils import to_openai_images_params
    #
    # data = to_openai_images_params(ImageRequest(prompt="a dog"))
    #
    # print(data)
    #
    # OpenAI().images.generate(**ImageRequest(prompt="a dog").model_dump())

    print(CogviewImageRequest(size="1024x10241"))
