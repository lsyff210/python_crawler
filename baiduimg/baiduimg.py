# coding:utf-8
# python2.7.11
import requests
import time
import re
import urllib2
import os

agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2774.3 Safari/537.36'

def get_pic(x):
    pattern = re.compile(r'''
flip\.setData\('imgData'.*?"data":\[(.*?)\]}\)
 ''', re.VERBOSE)
#     pattern1 = re.compile(r'''
# flip
#  ''', re.VERBOSE)
    txt = re.search(pattern, x)
    return txt


def get_imgurl(x):
    pattern = re.compile(r'"objURL":"(.*?)",')
    imgurl = re.findall(pattern, x)
    return imgurl


def baidu_img2(word='铅笔', pn=0 ):
    global agent
    url = 'http://image.baidu.com/search/flip?'
    header = {
        'User-Agent':agent,
    }
    params = {
        'tn': 'baiduimage',
        'ie': 'utf-8',
        'word': word,
        'pn': pn,
        'gsm': '0',
    }
    img_html = requests.get(url, headers=header, params=params)
    # y = img_html.url
    s2 = img_html.content
    r = get_pic(s2).group(1)
    # print r
    baidu_img_down(r)


def baidu_img_down(r):
    global agent
    imgurl = get_imgurl(r)
    print len(imgurl)
    print '=' * 99
    z = int(input('请需要下载的图片数量：'))
    folder = 'baidu_img'
    if not os.path.exists(folder):
        os.mkdir(folder)
    for x in range(z):
        i = imgurl[x]
        # host = i.replace('http://', ''),
        headers1 = {
            # 'Host':host,
            # 'Referer':y,
            # 'Upgrade-Insecure-Requests':'1',
            'User-Agent': agent,
        }
        imgname = i.split('/')[-1]
        filename = folder + "/" + imgname
        req = urllib2.Request(i, headers=headers1)
        picture = urllib2.urlopen(req)
        img = picture.read()
        # print img
        print('[%s]download from:[%s]' % (filename, i))
        local_img = open(filename, 'wb')
        local_img.write(img)
        local_img.close()
    print '下载完成'








if __name__ == '__main__':
    # baidu_img_down()
    baidu_img2(2)



