from text.symbols import symbols
from text.cleaner import clean_text
from text import cleaned_text_to_sequence, get_bert
from models import SynthesizerTrn
from tqdm import tqdm
from utils import _L, MODEL_DIR
import gradio as gr
import numpy as np
import commons
import random
import utils
import torch
import sys
import re
import os

if sys.platform == "darwin":
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

import logging

logging.getLogger("numba").setLevel(logging.WARNING)
logging.getLogger("markdown_it").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.INFO,
    format="| %(name)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)
net_g = None
debug = False


def get_text(text, language_str, hps):
    norm_text, phone, tone, word2ph = clean_text(text, language_str)
    phone, tone, language = cleaned_text_to_sequence(phone, tone, language_str)
    if hps.data.add_blank:
        phone = commons.intersperse(phone, 0)
        tone = commons.intersperse(tone, 0)
        language = commons.intersperse(language, 0)
        for i in range(len(word2ph)):
            word2ph[i] = word2ph[i] * 2

        word2ph[0] += 1

    bert = get_bert(norm_text, word2ph, language_str)
    del word2ph
    assert bert.shape[-1] == len(phone)
    phone = torch.LongTensor(phone)
    tone = torch.LongTensor(tone)
    language = torch.LongTensor(language)
    return bert, phone, tone, language


def TTS_infer(text, sdp_ratio, noise_scale, noise_scale_w, length_scale, sid):
    global net_g
    bert, phones, tones, lang_ids = get_text(text, "ZH", hps)
    with torch.no_grad():
        x_tst = phones.to(device).unsqueeze(0)
        tones = tones.to(device).unsqueeze(0)
        lang_ids = lang_ids.to(device).unsqueeze(0)
        bert = bert.to(device).unsqueeze(0)
        x_tst_lengths = torch.LongTensor([phones.size(0)]).to(device)
        del phones
        speakers = torch.LongTensor([hps.data.spk2id[sid]]).to(device)
        audio = (
            net_g.infer(
                x_tst,
                x_tst_lengths,
                speakers,
                tones,
                lang_ids,
                bert,
                sdp_ratio=sdp_ratio,
                noise_scale=noise_scale,
                noise_scale_w=noise_scale_w,
                length_scale=length_scale,
            )[0][0, 0]
            .data.cpu()
            .float()
            .numpy()
        )
        del x_tst, tones, lang_ids, bert, x_tst_lengths, speakers
        return audio


def tts_fn(text, speaker, sdp_ratio, noise_scale, noise_scale_w, length_scale):
    with torch.no_grad():
        audio = TTS_infer(
            text,
            sdp_ratio=sdp_ratio,
            noise_scale=noise_scale,
            noise_scale_w=noise_scale_w,
            length_scale=length_scale,
            sid=speaker,
        )

    return (hps.data.sampling_rate, audio)


def text_splitter(text: str):
    punctuation = r"[。,；,！,？,〜,\n,\r,\t,.,!,;,?,~, ]"
    # 使用正则表达式根据标点符号分割文本, 并忽略重叠的分隔符
    sentences = re.split(punctuation, text.strip())
    # 过滤掉空字符串
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def concatenate_audios(audio_samples, sample_rate=44100):
    half_second_silence = np.zeros(int(sample_rate / 2))
    # 初始化最终的音频数组
    final_audio = audio_samples[0]
    # 遍历音频样本列表, 并将它们连接起来, 每个样本之间插入半秒钟的静音
    for sample in audio_samples[1:]:
        final_audio = np.concatenate((final_audio, half_second_silence, sample))

    print("音频片段连接完成！")
    return (sample_rate, final_audio)


def read_text(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        return content


def infer_upl(text, speaker, sdp_ratio, noise_scale, noise_scale_w, length_scale):
    status = "Success"
    audio = content = None
    try:
        content = read_text(text)
        sentences = text_splitter(content)
        audios = []
        for sentence in tqdm(sentences, desc="TTS 推理中..."):
            with torch.no_grad():
                audios.append(
                    TTS_infer(
                        sentence,
                        sdp_ratio=sdp_ratio,
                        noise_scale=noise_scale,
                        noise_scale_w=noise_scale_w,
                        length_scale=length_scale,
                        sid=speaker,
                    )
                )

        audio = concatenate_audios(audios, hps.data.sampling_rate)

    except Exception as e:
        status = f"{e}"

    return status, audio, content


def infer_txt(content, speaker, sdp_ratio, noise_scale, noise_scale_w, length_scale):
    status = "Success"
    audio = None
    try:
        sentences = text_splitter(content)
        audios = []
        for sentence in tqdm(sentences, desc="TTS 推理中..."):
            with torch.no_grad():
                audios.append(
                    TTS_infer(
                        sentence,
                        sdp_ratio=sdp_ratio,
                        noise_scale=noise_scale,
                        noise_scale_w=noise_scale_w,
                        length_scale=length_scale,
                        sid=speaker,
                    )
                )

        audio = concatenate_audios(audios, hps.data.sampling_rate)

    except Exception as e:
        status = f"{e}"

    return status, audio


if __name__ == "__main__":
    if debug:
        logger.info("Enable DEBUG-LEVEL log")
        logging.basicConfig(level=logging.DEBUG)

    hps = utils.get_hparams_from_dir(MODEL_DIR)
    device = (
        "cuda:0"
        if torch.cuda.is_available()
        else (
            "mps"
            if sys.platform == "darwin" and torch.backends.mps.is_available()
            else "cpu"
        )
    )
    net_g = SynthesizerTrn(
        len(symbols),
        hps.data.filter_length // 2 + 1,
        hps.train.segment_size // hps.data.hop_length,
        n_speakers=hps.data.n_speakers,
        **hps.model,
    ).to(device)
    net_g.eval()
    utils.load_checkpoint(f"{MODEL_DIR}/G_78000.pth", net_g, None, skip_optimizer=True)
    speaker_ids = hps.data.spk2id
    speakers = list(speaker_ids.keys())
    random.shuffle(speakers)
    with gr.Blocks() as app:
        gr.Markdown(
            _L(
                """欢迎使用此创空间，此创空间基于 <a href="https://github.com/fishaudio/Bert-VITS2">Bert-vits2</a> 开源项目制作。使用此创空间必须遵守当地相关法律法规，禁止用其从事任何违法犯罪活动。"""
            )
        )
        with gr.Accordion(label=_L("原理浅讲"), open=False):
            gr.HTML(
                """<iframe src="//player.bilibili.com/player.html?bvid=BV1hergYRENX&p=2&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" width="100%" style="aspect-ratio: 16 / 9;"></iframe>"""
            )

        with gr.Tab(_L("输入模式")):
            gr.Interface(
                fn=infer_txt,  # 使用 text_to_speech 函数
                inputs=[
                    gr.TextArea(
                        label=_L("请输入简体中文文案"),
                        placeholder=_L("首次推理需耗时下载模型，还请耐心等待。"),
                        buttons=["copy"],
                    ),
                    gr.Dropdown(choices=speakers, value="莱依拉", label=_L("角色")),
                    gr.Slider(
                        minimum=0, maximum=1, value=0.2, step=0.1, label=_L("语调调节")
                    ),  # SDP/DP混合比
                    gr.Slider(
                        minimum=0.1,
                        maximum=2,
                        value=0.6,
                        step=0.1,
                        label=_L("感情调节"),
                    ),
                    gr.Slider(
                        minimum=0.1,
                        maximum=2,
                        value=0.8,
                        step=0.1,
                        label=_L("音素长度"),
                    ),
                    gr.Slider(
                        minimum=0.1, maximum=2, value=1, step=0.1, label=_L("生成时长")
                    ),
                ],
                outputs=[
                    gr.Textbox(label=_L("状态栏"), buttons=["copy"]),
                    gr.Audio(label=_L("输出音频")),
                ],
                flagging_mode="never",
                concurrency_limit=4,
                examples=[
                    [
                        "就算我们不抬头仰望，星空，也永远注视着我们。",
                        "莱依拉",
                        0.2,
                        0.6,
                        0.8,
                        1,
                    ]
                ],
                cache_examples=True,
            )

        with gr.Tab(_L("上传模式")):
            gr.Interface(
                fn=infer_upl,  # 使用 text_to_speech 函数
                inputs=[
                    gr.components.File(
                        label=_L("请上传简体中文 TXT 文案"),
                        type="filepath",
                        file_types=[".txt"],
                    ),
                    gr.Dropdown(choices=speakers, value="莱依拉", label=_L("角色")),
                    gr.Slider(
                        minimum=0,
                        maximum=1,
                        value=0.2,
                        step=0.1,
                        label=_L("语调调节"),
                    ),  # SDP/DP混合比
                    gr.Slider(
                        minimum=0.1,
                        maximum=2,
                        value=0.6,
                        step=0.1,
                        label=_L("感情调节"),
                    ),
                    gr.Slider(
                        minimum=0.1,
                        maximum=2,
                        value=0.8,
                        step=0.1,
                        label=_L("音素长度"),
                    ),
                    gr.Slider(
                        minimum=0.1,
                        maximum=2,
                        value=1,
                        step=0.1,
                        label=_L("生成时长"),
                    ),
                ],
                outputs=[
                    gr.Textbox(label=_L("状态栏"), buttons=["copy"]),
                    gr.Audio(label=_L("输出音频")),
                    gr.TextArea(label=_L("文案提取结果"), buttons=["copy"]),
                ],
                flagging_mode="never",
                concurrency_limit=4,
            )

    app.launch(css="#gradio-share-link-button-0 { display: none; }", ssr_mode=False)
