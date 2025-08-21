以bilibili为例，我们点击要爬取的视频，将视频播放，右键点击检查，<img width="1465" height="818" alt="{E030F73A-3772-4E3B-840A-454C969E546C}" src="https://github.com/user-attachments/assets/f4b6c55d-77de-4f1e-b5f2-f326e4cb537f" />
看到网络这个选项，点击它，视频文件的url一般是xhr/fetch<img width="675" height="907" alt="image" src="https://github.com/user-attachments/assets/8580ae90-06f7-4167-947c-6d480beb61f2" />
<img width="12这就是我们寻找的url,我们另开一个浏览器，输入url,发现这只是纯视频，而将其他url输入进去，发现是音频，这就要用到ffmpeg,具体如何将视频和音频结合在一起这里不过多介绍13" height="957" alt="image" src="https://github.com/user-attachments/assets/91344a6d-fe40-4477-98dd-b14fee4e072f" />
然后右键，点击页面源码，再点击ctrl键和f键，打开搜索栏，我们将关键的参数：1-30216.m4s输入进去，![Uploading image.png…]()，搜索栏显示有4个结果，至此，浏览器的任务结束了
我的爬虫文件里有些函数待会要使用，首先我们要调用get_html()函数获取页面源码，接着用bs4()函数生成beautifulsoup对象（bs4()函数要根据实际情况进行修改），这里我们就得到了纪录片所以视频及音频的url
接着我们使用download_video2()下载视频（只有最低画质所以不要用到get_highest_quality_m3u8（））

