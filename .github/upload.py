import argparse
from modelscope import HubApi
from huggingface_hub import HfApi


def upl2ds(mstk: str, hftk: str):
    ms_api = HubApi(token=mstk)
    for file in ["hoyoTTS.py", "quickstart.md", "README.md", ".gitattributes"]:
        ms_api.upload_file(
            path_or_fileobj=f"./{file}",
            path_in_repo=file,
            repo_id="Genius-Society/hoyoTTS",
            repo_type="dataset",
        )

    hf_api = HfApi(token=hftk)
    hf_api.upload_file(
        path_or_fileobj="./hoyoTTS.py",
        path_in_repo="hoyoTTS.py",
        repo_id="Genius-Society/hoyoTTS",
        repo_type="dataset",
    )
    hf_api.upload_file(
        path_or_fileobj="./README.en.md",
        path_in_repo="README.md",
        repo_id="Genius-Society/hoyoTTS",
        repo_type="dataset",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upl to MS & HF dataset")
    parser.add_argument("--mstk", required=True, help="Your ModelScope Access Token")
    parser.add_argument("--hftk", required=True, help="Your HuggingFace Access Token")
    args = parser.parse_args()
    upl2ds(args.mstk, args.hftk)
