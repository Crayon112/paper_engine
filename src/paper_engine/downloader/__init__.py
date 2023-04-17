import os
import requests


def download(url, save_dir):
    response = requests.get(url)
    content = response.content
    path = os.path.join(save_dir, url[-10:])
    with open(path, "wb") as f:
        f.write(content)
