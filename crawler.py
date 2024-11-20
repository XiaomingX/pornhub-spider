#!/usr/bin/env python

import os
import re
import requests
from lxml import etree
from loguru import logger
from dynaconf import Dynaconf
import youtube_dl
import fire

# 加载配置文件
settings = Dynaconf(settings_files=["settings.toml"])

# 配置日志记录
logger.add("logs/stdout.log", format="{time:MM-DD HH:mm:ss} {level} {message}")

# 请求头配置
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
}

# 代理配置
PROXIES = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
    "all": "socks5://127.0.0.1:7890",
}


# 创建文件夹
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"创建目录: {directory}")
    else:
        logger.info(f"目录已存在: {directory}")


# 下载文件
def download_file(url, name, filetype):
    filepath = os.path.join(filetype, f"{name}.{filetype}")
    if os.path.exists(filepath):
        logger.info(f"文件已下载: {filepath}")
        return

    try:
        response = requests.get(url, headers=HEADERS, proxies=PROXIES)
        response.raise_for_status()
        with open(filepath, "wb") as file:
            file.write(response.content)
        logger.info(f"下载成功: {filepath}")
    except Exception as err:
        logger.error(f"下载失败: {err}")


# 获取 webm 格式的文件
def fetch_webm_files(page_url):
    logger.info(f"正在爬取页面: {page_url}")
    try:
        response = requests.get(page_url, headers=HEADERS, proxies=PROXIES, verify=False)
        response.raise_for_status()
        html = etree.HTML(response.text)

        base_xpath = '//*[@class="phimage"]/a/'
        video_urls = html.xpath(f"{base_xpath}img/@data-mediabook")
        video_names = html.xpath(f"{base_xpath}/@href")

        for video_url, name_path in zip(video_urls, video_names):
            try:
                print(name_path)
                print(video_url)
                name = re.search(r"=(\w+)", name_path).group(1)
                print(name)
                download_file(video_url, name, "webm")
            except Exception as err:
                logger.error(f"解析失败: {err}")
    except Exception as err:
        logger.error(f"页面爬取失败: {err}")


# 下载 mp4 文件
def download_mp4_files(video_urls):
    logger.info("开始下载 MP4 文件")
    ydl_opts = {
        "ignoreerrors": True,
        "outtmpl": "mp4/%(extractor)s-%(id)s-%(title)s.%(ext)s",
        "proxy": "http://127.0.0.1:7890",  # 设置 youtube_dl 的代理
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_urls)


# 运行程序
def run(task_type=None):
    create_directory("webm")
    create_directory("mp4")

    if task_type == "webm":
        for url in settings.urls:
            fetch_webm_files(url)
    elif task_type == "mp4":
        downloaded_keys = [filename.split(".")[0] for filename in os.listdir("webm")]
        video_urls = [f"https://www.pornhub.com/view_video.php?viewkey=ph{key}" for key in downloaded_keys]
        download_mp4_files(video_urls)
    else:
        logger.info("""
使用说明:
    python crawler.py webm
        - 下载热门页面的缩略图，存放于 webm 文件夹

    python crawler.py mp4
        - 根据 webm 文件夹中的数据，下载对应的 MP4 文件
        """)
    logger.info("任务完成！")


# 主函数
def main():
    fire.Fire(run)


if __name__ == "__main__":
    main()
