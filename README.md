
## Usage

```sh
git clone https://github.com/XiaomingX/pornhub-spider
cd pornhub-spider && pip install -r requirements.txt
# Edit the settings.toml file to configure `proxy_url` and specify your preferred list pages.
python3 crawler.py webm
# After the script finishes running, webm thumbnails from two pages will be downloaded into the `webm` folder.
# The filenames will match the URL suffix of the corresponding detail pages. Select the videos you wish to keep.
python3 crawler.py mp4
# You can find the downloaded MP4 files in the `mp4` folder.
```

## 用法

```sh
git clone https://github.com/XiaomingX/pornhub-spider
cd pornhub-spider && pip install -r requirements.txt
# 编辑 settings.toml, 配置proxy_url 和 喜欢的列表页面
python3 crawler.py webm
# 待程序运行完毕， 会在webm文件夹下download两页的webm缩略图，对应名称为详细页面的URL后缀，筛选出自己想要保留的视频.
python3 crawler.py mp4
# 在MP4文件夹可看到下载好的MP4文件.
```
