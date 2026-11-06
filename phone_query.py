# -*- coding: utf-8 -*-
"""
实验一 任务2：手机号码归属地查询（代码重构可复用版）
参考教材第3章 3.5 案例2

运行：python phone_query.py
"""
import os
import re
import requests
from urllib.parse import urlencode

# ① 定义请求信息：查询接口、请求头、超时时间
QUERY_URL = "https://www.ip138.com/mobile.asp"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/79.0.3945.88 Safari/537.36"
}


def get_html(mobile, headers=HEADERS, timeout=10):
    """② 发送请求并获得响应：手机号、action 作为 GET 参数，返回网页文本"""
    params = {"mobile": mobile, "action": "mobile"}
    url = QUERY_URL + "?" + urlencode(params)
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding
    return resp.text


def save_html(html, save_dir, file_name):
    """③ 将响应存储到本地 html"""
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, file_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def parse_result(html):
    """从响应网页中提取归属地、运营商、区号、邮编"""
    patterns = {
        "归属地": r"<td>卡号归属地</td>\s*<td><span>(.*?)</span>",
        "运营商": r"<td>运 营 商</td>\s*<td>\s*<a[^>]*>(.*?)</a>",
        "区号": r"<td>区 号</td>\s*<td>\s*<a[^>]*>(.*?)</a>",
        "邮编": r"<td>邮 编</td>\s*<td>\s*<a[^>]*>(.*?)</a>",
    }
    info = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, html, re.S)
        info[key] = match.group(1).strip() if match else ""
    return info


def query_mobile(mobile, save_dir="output"):
    """通用查询函数：查询手机号并保存网页，返回结果信息"""
    html = get_html(mobile)
    path = save_html(html, save_dir, f"phone_{mobile}.html")
    info = parse_result(html)
    info["保存路径"] = os.path.abspath(path)
    return info


if __name__ == "__main__":
    mobile = "19552835059"
    result = query_mobile(mobile)
    print(f"查询号码：{mobile}")
    for key, value in result.items():
        print(f"{key}：{value}")
