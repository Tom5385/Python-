import urllib.request
from urllib.error import HTTPError, URLError,ContentTooShortError
import gzip
import re
from bs4 import BeautifulSoup
import os,subprocess,requests
def get_html(url,user_agent,num_retries=2):
    print('download:',url)
    user_agent = user_agent.encode('ascii','ignore')
    request=urllib.request.Request(url)
    request.add_header('User-Agent',user_agent,)
    #给request请求头增加代理
    try:
        response = urllib.request.urlopen(request)
        cs=response.headers.get_content_charset()
        #这行代码的作用是 从 HTTP 响应头（Content-Type）中提取响应内容的字符编码，通常用来决定以什么编码方式去解码网页内容
        if response.headers.get("Content-Encoding") == "gzip":
            #从HTTP响应头中获取数据是否被gzip压缩
            html= gzip.decompress(response.read())
            # 解压 gzip
            if not cs:
                cs = 'utf-8'
            html = html.decode(cs)
        else:
            if not cs:
                cs='utf-8'
            html=response.read().decode(cs)


    except (HTTPError,URLError,ContentTooShortError) as e:
        print('Error:',e.reason)
        html=None
        if num_retries > 0 and 500<=e.code<600:
            return get_html(url,user_agent,num_retries-1)
    return html






"""下载网页视频"""
def download_video1(m3u8_url):
    m3u8_text=requests.get(m3u8_url).text
    base_url = m3u8_url.rsplit("/", 1)[0] + "/"
    ts_files = [line.strip() for line in m3u8_text.split("\n") if line and not line.startswith("#")]
    # 下载 ts 分片
    for i, ts in enumerate(ts_files, 1):
        ts_url = base_url + ts
        r = requests.get(ts_url, stream=True)
        with open(f"{i}.ts", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"已下载 {i}/{len(ts_files)}")

    # 合并为 mp4
    subprocess.run("copy /b *.ts output.mp4", shell=True)


def download_video2(video_url,i):
# m3u8 地址

    # 输出文件名（可以改成你想要的路径）
    output_file = "output.mp4"

    # 调用 ffmpeg 下载并合并
    cmd = [
        "ffmpeg",
        "-i",video_url,  # 输入 m3u8
        "-c", "copy",    # 不重新编码，直接拷贝流
        f'D:/Users/爬虫实战/straplez-{i}.mp4',
    ]

    # 执行命令
    subprocess.run(cmd, check=True)
    print(f"下载完成：{output_file}")





# def bs4(html):模板
#     #实例化BeautifulSoup对象
#     soup = BeautifulSoup(html, "html5lib")
#     alist=soup.find_all('script',attrs={'crossorigin':'anonymous'})
#     #获取所有的a标签
#     li=[]
#     for a in alist:#这里的a并不是字符串是tag对象，所以不能够直接使用，比如："'/video.' in a","set(a)"
#         if a.get("href"):#a_tag.get("href") 才是调用 Tag 对象的 .get() 方法，去取这个标签的某个属性，如：print(a_tag.get("href"))   # https://example.com。
#            herf=a.get("href")
#         #有些a标签没有'href',更不要说对应的值了，所以用get()更好，没有这个标签就返回NONE
#         if '/video.' in herf:
#             li.append(herf)
#
#     li=list(set(li))#set（li）是去除重复
#     return li

def bs4(html):
    #实例化BeautifulSoup对象,将html内容解析成soup文档
    soup = BeautifulSoup(html, "html5lib")
    alist=soup.find_all('script',attrs={'crossorigin':'anonymous'})#得到的是一个list,list里面是tag对象
    #获取所有的a标签
    url_li=[]
    for a in alist:
        positions=str(a.string).splitlines()#str()将NavigableString(表现得像 str)转换成python中的的STR;
        # 想按“行”分割 → 用 splitlines(),想按“某种符号”或“空白”分割 → 用 split()
        #.string属性属于tag对象，如果标签中只有一个文本节点 → 返回字符串(NavigableString(表现得像 str)),<p>Hello World</p>-->Hello World;
        # 如果标签中有多个子节点（包含文本和其他标签） → 返回 None,a=<p>Hello <b>World</b></p>-->None,正解（获取b标签里的'World'）：tag_b=a.b,print(tag.string)
        # 或者要获取标签里的所有文本，应该用 .get_text()，print(a.p.get_text())-->Hello World(把所有文本拼起来)，返回的是str或者.text 属性可以获取 标签中所有的文本内容（包括子标签里的文本），并且会把它们拼接成一个字符串返回。
        #.get_text() 和 .text 基本等价
        #获取标签的属性值：herf=a['herf']或者a.attrs['href'](此a为beautifulsoup对象)或者a.get(‘herf’)
        for p in positions:
            if 'html5player.setVideoHLS' in p:
                match = re.search(r"'(https?://[^']+)'", p)
                if match:
                    url = match.group(1)
                    url_li.append(url)
    return url_li




# url_li=[]
# base_url="https://www.xvideos.com"
# for url in urllist:
#     final_url=base_url+url
#     Html=get_html(final_url,user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36')
#     soup=BeautifulSoup(Html,"lxml")
#     scriptlist=soup.find_all("script")
#     for script in scriptlist:
#         if script.get('crossorigin')=="anonymous" and not script.get('src'):
#             positions=str(script.string).splitlines()
#             for position in positions:
#                 if 'html5player.setVideoHLS' in position:
#                     match = re.search(r"'(https?://[^']+)'", position)
#                     if match:
#                         url = match.group(1)
#                         url_li.append(url)


# print(url_li)



from urllib.parse import urljoin

def get_highest_quality_m3u8(master_url):
    resp = requests.get(master_url)
    resp.raise_for_status()
    base_url = master_url.rsplit('/', 1)[0] + "/"

    lines = resp.text.splitlines()
    best_url = None
    best_res = 0

    for i, line in enumerate(lines):
        if line.startswith("#EXT-X-STREAM-INF"):
            # 解析分辨率
            if "RESOLUTION=" in line:
                res_text = line.split("RESOLUTION=")[1].split(",")[0]
                width, height = map(int, res_text.split("x"))
                res = height  # 用高度作为清晰度标准
                # 下一行就是对应的分片 m3u8 文件名
                stream_url = urljoin(base_url, lines[i+1].strip())
                if res > best_res:
                    best_res = res
                    best_url = stream_url
    return best_url




html=get_html(
'https://www.xvideos.com/channels/karbo/videos/best/straight/2',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0').split(',')

# import pprint
# pprint.pprint(html)
# print('*'*60)
url_list=[]
i=70
for html_line in html:
    if '/prof-video-click\\/upload\\/karbo' in html_line:
        url=html_line.split('\/')
        video_url='https://www.xvideos.com/video.'+url[-2]+'/'+url[-1]
        video_html=get_html(
            video_url,
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0')
        url_li=bs4(video_html)
        for url in url_li:
            i+=1
            best_url=get_highest_quality_m3u8(url)
            print(best_url)
            download_video2(best_url,i)







https://upos-hz-mirrorakam.akamaized.net/upgcxcode/98/45/43854598/43854598_da2-1-100022.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&oi=1385734734&og=cos&uipk=5&platform=pc&nbs=1&deadline=1755708684&gen=playurlv3&os=akam&trid=be3c535f3e2840abb847ca46d685707u&mid=0&upsig=bbc38a19b28f845bb239b91197a0d0d9&uparams=e,oi,og,uipk,platform,nbs,deadline,gen,os,trid,mid&hdnts=exp=1755708684~hmac=4937ea2d6937d43cb253fe3b5f05515d9c5d7da85cf922e7da480103a519dfa3&bvc=vod&nettype=0&bw=205742&dl=0&f=u_0_0&agrr=0&buvid=FEE8CAA4-13D7-DFD1-CB93-9DB0381C847C36380infoc&build=0&orderid=0,2


https://upos-hz-mirrorakam.akamaized.net/upgcxcode/82/48/43854882/43854882_da2-1-100022.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&deadline=1755708590&mid=0&os=akam&nbs=1&oi=1385734734&uipk=5&platform=pc&trid=190f4ce84d304f5ba7a97fcfd0f4a0bu&gen=playurlv3&og=hw&upsig=b389f5f82468bc0e5a141cbb3ceb1faa&uparams=e,deadline,mid,os,nbs,oi,uipk,platform,trid,gen,og&hdnts=exp=1755708590~hmac=af0e355df36b5b4b31fd3442f0b9088a9544f09f2df89a1961a90d10e4113079&bvc=vod&nettype=0&bw=220307&f=u_0_0&agrr=0&buvid=FEE8CAA4-13D7-DFD1-CB93-9DB0381C847C36380infoc&build=0&dl=0&orderid=0,2

