# 说明
百度网盘会屏蔽某些敏感的视频, 加密上传可以避免被屏蔽, 但是无法在线播放;   
m3u8(hls协议)可以播放加密的视频;  
两者结合一下或许有点意思...

本程序是一个测试的演示程序.  

# 启动程序
程序地址:   
github: [qiaoxingxing/baidupan-video](https://github.com/qiaoxingxing/baidupan-video)  
gitee: [qiaoxingxing/baidupan-video](https://gitee.com/qiaoxingxing/baidupan-video)  

python版本: 3.7  
使用的包: 
- Flask: web框架
- bypy: 百度网盘Python客户端

1. 安装依赖:
```
pip install -r requirements.txt 
```

2. 给bypy授权: 
```
bypy info
```
然后跟着提示操作; 

3. 启动web: 
```
flask run --host=0.0.0.0 --port=5000
```
打开[http://127.0.0.1:5000/static/index.html](http://127.0.0.1:5000/static/index.html)  
点击页面底部按钮播放(视频上传完成之后才会有)

# 生成`.m3u8`文件和加密ts分片
新建一个文件夹, 包含以下文件: 
- 一个mp4文件, `source.mp4`
- 秘钥文件`key.txt`, 文件内容: 
```
0123456789ABCDEF
```
- 密钥信息文件`keyinfo.txt`, 文件内容: 
```
/key
key.txt
0123456789ABCDEF0123456789ABCDEF
```
- 空文件夹: `video01`

执行命令: 
```shell
ffmpeg.exe -y -i source.mp4 -c:v libx264 -c:a copy -f hls -hls_time 5 -hls_list_size 0 -hls_key_info_file keyinfo.txt -hls_playlist_type vod -hls_segment_filename video01/video-%%03d.ts video01/index.m3u8
```
以上命令的部分参数说明: 
|参数|说明|
| - | - |
| -y | 直接覆盖已经存在的输出文件 |
| -c | 指定输入输出的解码编码器 |
| -f | 强制设置输入输出的文件格式，默认情况下ffmpeg会根据文件后缀名判断文件格式 |
| -hls_time | 指定生成 ts 视频切片的时间长度s |
| -hls_list_size 0 | 索引播放列表的最大列数 默认5，0 为不限制 |
| -hls_playlist_type vod | 表示当前的视频流并不是一个直播流，而是点播流 |
| -hls_segment_filename | 输出 ts m3u8 文件路径 |

注意: 为了配合程序使用, `.m3u8`文件必须取名为"index.m3u8"  

考虑到百度网盘的网速, 视频可能需要一些压缩:   
```shell
ffmpeg.exe -y -i source.mp4 -s 600x480 -r 20 -b 700K -b:a 32K -c:v libx264 -c:a aac -f hls -hls_time 5 -force_key_frames "expr:gte(t,n_forced*1)" -hls_list_size 0 -hls_key_info_file keyinfo.txt -hls_playlist_type vod -hls_segment_filename video01/video-%%03d.ts video01/index.m3u8
```
- -s 600x480 画面尺寸
- -r 20 帧率
- -b 700K 比特率
- `-force_key_frames "expr:gte(t,n_forced*1)"` 每秒前增加关键帧, 使得每个ts文件都是准确的5秒钟;

如果百度网盘的速度是100kb/s, 5秒一个视频, 视频文件大于500kb, 播放就会卡.

参考: [使用 FFmpeg 生成 ts 切片并使用 AES-128 加密 · Qu](https://rockycoder.cn/ffmpeg/2018/10/26/Generate-encrypted-video.html)  

# 上传视频到百度网盘

打开百度云, 上传后目录结构如下: 
```
我的应用数据
└─bypy
    └─视频
        ├─视频01
        │      index.m3u8
        │      video-000.ts
        │      video-001.ts
        │      .......
        │
        └─视频02
                index.m3u8
                video-000.ts
                video-001.ts
                ........
```
说明:
- 文件夹"我的应用数据"也可能叫apps
- 文件夹"bypy"不需要手动创建, 应该已经存在, 如果不存在应该是刚才授权失败.
- 新建文件夹"视频", 名称不能改动;
- 重命名刚才的video01文件夹, 上传到"视频"文件夹下; 这里重命名为"视频01"
- `.m3u8`文件必须取名为"index.m3u8"

视频上传完成之后, 刷新刚才的页面, 底部会有"视频01"、"视频02"的按钮, 点击即可播放; 


