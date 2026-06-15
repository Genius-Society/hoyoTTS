---
license: cc-by-nc-nd-4.0
viewer: false
---

# Genshin Impact & Honkai Star Rail Game Character Voice Dataset
This repository is the integration code for the TTS datasets of miHoYo games provided by [AI Hobbyist](https://www.modelscope.cn/organization/aihobbyist), with the final right of interpretation belonging to [miHoYo](https://www.mihoyo.com). The integration code aims to provide a more convenient usage solution for the community: for `Python` developers, only a few lines of code are needed to automatically search, download, split by language, and normalize on demand, instead of manually searching for and downloading the cumbersome complete package to accommodate users with different backgrounds and thresholds. The integration code is provided by [Genius-Society](https://www.modelscope.cn/organization/Genius-Society). If you need to use the compressed package version of the data source and write your own data processing scripts, you can support the original author.

## Environment
```bash
pip install datasets==3.6
```

## Supported characters
<https://res.acgnai.top>

## Splits
| Language | Genshin Impact | Honkai Star Rail |
| :------: | :------------: | :--------------: |
| Chinese  |  `Genshin_zh`  |  `StarRail_zh`   |
| Japanese |  `Genshin_jp`  |  `StarRail_jp`   |
| English  |  `Genshin_en`  |  `StarRail_en`   |
|  Korean  |  `Genshin_kr`  |  `StarRail_kr`   |

## Usage
```python
from datasets import load_dataset

ds = load_dataset(
    "Genius-Society/hoyoTTS",
    name="黑塔",  # The Chinese name of the character
    split="StarRail_en",  # The language options should match the character's game
    cache_dir="./__pycache__",  # The cache location of the dataset
    trust_remote_code=True,
)
for item in ds:
    print(item)
```

## Maintenance
```bash
git clone git@hf.co:datasets/Genius-Society/hoyoTTS
cd hoyoTTS
```

## Mirror
<https://www.modelscope.cn/datasets/Genius-Society/hoyoTTS>

## Thanks
 - <https://pan.ai-hobbyist.com>
 - <https://ys.mihoyo.com/main>
 - <https://sr.mihoyo.com>