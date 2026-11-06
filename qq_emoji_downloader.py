# -*- coding: utf-8 -*-
"""
实验一 任务1：QQ表情包图片批量下载（代码重构可复用版）
参考教材第3章 3.4 案例1

运行：python qq_emoji_downloader.py
"""
import os
import re
import requests
from urllib.parse import urljoin, urlparse

# ① 定义请求信息：列表页地址、保存目录、请求头
PAGE_URL = "http://www.bspider.top/yh31/"
SAVE_DIR = "downloads/qq_emoji"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/79.0.3945.88 Safari/537.36"
}


def get_image_urls(page_url, headers=HEADERS, timeout=10):
    """解析列表页中所有 <img> 的 src，返回图片的完整 URL 列表"""
    resp = requests.get(page_url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding
    srcs = re.findall(r'<img[^>]+src="([^"]+)"', resp.text, re.IGNORECASE)
    urls = [urljoin(page_url, src) for src in srcs]
    return list(dict.fromkeys(urls))  # 去重，避免同一张图片被重复下载


def get_image(url, headers=HEADERS, timeout=10):
    """② 发送请求并获得响应：返回图片的二进制数据"""
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.content


def save_image(content, save_dir, file_name):
    """③ 将响应图片存储到本地"""
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, file_name)
    with open(path, "wb") as f:
        f.write(content)
    return path


def download_images(page_url=PAGE_URL, save_dir=SAVE_DIR, limit=None):
    """通用下载函数：调用代码与通用函数分离，可复用于其它图片列表页"""
    urls = get_image_urls(page_url)
    if limit is not None:
        urls = urls[:limit]
    saved_paths = []
    for index, url in enumerate(urls, start=1):
        try:
            file_name = urlparse(url).path.split("/")[-1]
            content = get_image(url)
            path = save_image(content, save_dir, file_name)
            saved_paths.append(path)
            print(f"[{index}/{len(urls)}] {path} ({len(content)} 字节)")
        except requests.RequestException as err:
            print(f"[{index}/{len(urls)}] 下载失败：{url} -> {err}")
    return saved_paths


if __name__ == "__main__":
    paths = download_images()
    print(f"共保存 {len(paths)} 张图片到 {SAVE_DIR}")
