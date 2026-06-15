---
license: CC-BY-NC-ND
text:
  text-to-speech:
    language:
      - zh
      - jp
      - en
      - kr
tags:
  - TTS
  - mihoyo
  - Genshin Impact
  - star rail
  - Honkai
---

# 简介
本仓库为由 [AI Hobbyist](https://www.modelscope.cn/organization/aihobbyist) 提供的米家游戏TTS数据集的集成代码，最终解释权均归 [米哈游](https://www.mihoyo.com) 所有。集成代码旨在为社区提供更加便捷的使用方案：对于 `Python` 开发者仅需几行代码即可实现自动按需查找、下载、按语言拆分以及正规化，而非手动搜索和下载笨重的完整包以照顾不同背景和门槛的使用者。集成代码由 [Genius-Society](https://www.modelscope.cn/organization/Genius-Society) 提供，若您需要使用压缩包版数据源并自行编写数据处理脚本，可去支持原作者。

## 环境
```bash
pip install py7zr modelscope[framework]
```

## 支持角色
<https://res.acgnai.top>

## 语言选项
| 语言  |     原神     |     崩铁      |
| :---: | :----------: | :-----------: |
|  中   | `Genshin_zh` | `StarRail_zh` |
|  日   | `Genshin_jp` | `StarRail_jp` |
|  英   | `Genshin_en` | `StarRail_en` |
|  韩   | `Genshin_kr` | `StarRail_kr` |

## 使用
:modelscope-code[]{type="sdk"}

## 维护
:modelscope-code[]{type="git"}

## 镜像
<https://huggingface.co/datasets/Genius-Society/hoyoTTS>

## 致谢
 - <https://pan.ai-hobbyist.com>
 - <https://ys.mihoyo.com/main>
 - <https://sr.mihoyo.com>

<div style="display:none">