# subtitles_match_relocated
an python cli tool for subtitles_match_relocated in movies&amp;episode path  
需求来源于emby的视频字幕不支持手动选择字幕地址,默认需要和视频在同一路径下并且同名,一般下载的电影或剧集所带字幕在视频文件目录的Subs目录下且不同名,通常情况下载后需要人工改名和移动到视频文件目录下,所以特地写了这个python小程序指定电影或者剧集目录后自动识别和复制字幕到视频文件目录下.只在mac下测试成功,理论上支持windows或者其他环境,但是未经验证,
程序逻辑如下:
![Alt text](https://github.com/zhouyunjian/subtitles_match_relocated/blob/main/flow-process-diagram.jpeg)
