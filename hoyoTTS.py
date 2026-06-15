import os
import time
import random
import datasets
import requests

_GAMES = {"Genshin": "原神", "StarRail": "星穹铁道"}

_LANGS = {"zh": "中文", "jp": "日语", "en": "英语", "kr": "韩语"}

_URL = "https://res.ai-lab.top/api/acgnailib/models"

_HOME = f"https://www.modelscope.cn/datasets/Genius-Society/{os.path.basename(__file__)[:-3]}"


class hoyoTTS(datasets.GeneratorBasedBuilder):
    def _info(self):
        if self.config.name == "default":
            self.config.name = "众人"

        return datasets.DatasetInfo(
            features=datasets.Features(
                {
                    "audio": datasets.Audio(sampling_rate=44_100),
                    "text": datasets.Value("string"),
                }
            ),
            supervised_keys=("audio", "text"),
            license="CC-BY-NC-ND",
            version="0.0.1",
            homepage=_HOME,
        )

    def _get_txt(self, audio_path: str):
        txt_path = audio_path.replace(".wav", ".lab")
        with open(txt_path, "r", encoding="utf-8") as file:
            content = file.read()

        return content.strip()

    def _parse_url(self, game: str, lang: str):
        try:
            response = requests.post(
                _URL,
                json={
                    "category": _GAMES[game],
                    "repo": f"datasets/aihobbyist/{game}_Dataset",
                    "root_path": "/datasets",
                    "subcategory": _LANGS[lang],
                },
                headers={
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"
                },
            )
            response.raise_for_status()
            data = response.json()
            for item in data:
                if item["dataname"] == self.config.name:
                    return item["dl_link"]

            return None

        except Exception as e:
            print(f"{e}, retrying...")
            time.sleep(random.randint(3, 5))
            return self._parse_url(game, lang)

    def _download_and_extract(self, dl_manager: datasets.DownloadManager, lnk: str):
        try:
            return dl_manager.download_and_extract(
                requests.head(lnk, allow_redirects=True).url
            )
        except Exception as e:
            print(f"{e}, retrying...")
            return self._download_and_extract(dl_manager, lnk)

    def _split_generators(self, dl_manager):
        data_splits = []
        for game in _GAMES:
            for lang in _LANGS:
                url = self._parse_url(game, lang)
                if not url:
                    continue

                files = []
                split_name = f"{game}_{lang}"
                data_files = self._download_and_extract(dl_manager, url)
                for fpath in dl_manager.iter_files([data_files]):
                    if os.path.basename(fpath).endswith(".wav"):
                        files.append({"audio": fpath, "text": self._get_txt(fpath)})

                random.shuffle(files)
                data_splits.append(
                    datasets.SplitGenerator(
                        name=split_name,
                        gen_kwargs={"files": files},
                    )
                )

        return data_splits

    def _generate_examples(self, files):
        for i, fpath in enumerate(files):
            yield i, fpath
