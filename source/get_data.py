import os
import subprocess
from source.keys import API_KEY


DOWNLOAD_REPO = "repos/ldoshi/rome-wasnt-built-in-a-day/commits"

def main():
    os.makedirs(f"data/{DOWNLOAD_REPO}", exist_ok=True)
    for i in range(3):
        with open(f"data/{DOWNLOAD_REPO}/pull_requests_{i}.json", "w") as pull_request_json:
            subprocess.run(["gh", "api" , "-H", "Accept: application/vnd.github+json", "-H", f"Authorization: Bearer {API_KEY}", DOWNLOAD_REPO+f"&page={i+1}"], stdout=pull_request_json)


if __name__ == "__main__":
    main()