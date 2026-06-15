## 数据集: Genius-Society/hoyoTTS
```python
from modelscope.msdatasets import MsDataset

ds = MsDataset.load(
    "Genius-Society/hoyoTTS",
    subset_name="黑塔",  # 角色中文名
    split="StarRail_zh",  # 语言选项需与角色所在游戏匹配
    cache_dir="./__pycache__",  # 数据集缓存位置
    trust_remote_code=True,
)
for i in ds:
    print(i)
```