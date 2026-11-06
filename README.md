# 实验一 静态网页爬取

《大数据采集与处理》实验一的两个案例，均使用 `requests` 实现，并按“通用函数 + 调用代码”的方式重构，便于复用。

## 目录结构

```
lab01-static-web-crawler/
├── qq_emoji_downloader.py   # 任务1：QQ 表情包图片批量下载
├── phone_query.py           # 任务2：手机号码归属地查询
├── requirements.txt
├── .gitignore
└── README.md
```

## 环境依赖

- Python 3.8+
- requests

安装依赖：

```bash
pip install -r requirements.txt
```

## 任务1：QQ 表情包图片批量下载

参考教材第 3 章 3.4 案例1，目标列表页：`http://www.bspider.top/yh31/`。

实现思路：

1. `get_image_urls()` 请求列表页，用正则提取所有 `<img>` 的 `src`，再用 `urljoin` 补全为绝对地址并去重；
2. `get_image()` 请求单张图片，返回 `resp.content` 二进制数据；
3. `save_image()` 自动创建目录并以 `wb` 方式写入本地；
4. `download_images()` 是通用调用函数，可传入任意图片列表页地址与保存目录。

运行：

```bash
python qq_emoji_downloader.py
```

默认保存到 `downloads/qq_emoji/`，实测共下载 50 张表情包图片。

## 任务2：手机号码归属地查询

参考教材第 3 章 3.5 案例2，查询接口：`https://www.ip138.com/mobile.asp`。

实现思路：

1. `get_html()` 将手机号和 `action=mobile` 作为 GET 参数拼接到 URL，携带 `User-Agent` 发起请求，并用 `resp.apparent_encoding` 解决中文乱码；
2. `save_html()` 将响应源码以 UTF-8 编码保存为本地 HTML；
3. `parse_result()` 用正则从响应中提取归属地、运营商、区号、邮编；
4. `query_mobile()` 为通用查询函数，更换手机号即可复用。

运行：

```bash
python phone_query.py
```

默认查询 `19552835059`，结果保存为 `output/phone_19552835059.html`，控制台同时输出：

```
归属地：江苏 淮安
运营商：中国移动
区号：0517
邮编：223000
```

## 说明

- 目标网站结构可能随时调整，若字段解析失败，可按实际返回的 HTML 修改 `parse_result()` 中的正则；
- 代码仅用于课程实验与学习，请勿用于高频、大规模采集。
