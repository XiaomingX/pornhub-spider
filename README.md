
## 用法

```sh
git clone https://github.com/XiaomingX/pornhub-spider
cd pornhub-spider && pip install -r requirements.txt
# 编辑 settings.toml, 配置proxy_url 和 喜欢的列表页面
python3 crawler.py webm
# 待程序运行完毕， 会在webm文件夹下download两页的webm缩略图，对应名称为详细页面的URL后缀
python3 crawler.py mp4
# 在MP4文件夹可看到下载好的MP4文件
```