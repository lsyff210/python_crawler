# coding:utf-8

"""运行环境： python2.7.11   requests2.10.0 """
from HTMLParser import HTMLParser
import requests
import re
import time
import os
import urllib2


def _attr(attrs, attr_name):
    for attr in attrs:
        if attr[0] == attr_name:
            return attr[1]
    return None


agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER'
host = 'tieba.baidu.com'
headers1 = {
    'Host': host,
    'User-Agent': agent,
}

# 贴吧帖子量一直在变化，需要知道当前的页面总数
def tieba_content_page():
    url_python = 'http://tieba.baidu.com/f?kw=python&ie=utf-8'
    tieba_html = requests.get(url_python, headers=headers1)
    tieba_con = tieba_html.content
    sumpage_pattern = re.compile(r'<a href="http://tieba\.baidu\.com/f\?kw=python&ie=utf-8&pn=(\d*)"'
                                 r' class="last pagination-item " >尾页')
    sumpage_str = re.search(sumpage_pattern, tieba_con)
    sumpage = int(sumpage_str.group(1))
    return sumpage

# 获取贴吧指定页面的内容，用来获取帖子链接
def tieba_page_content():
    sum_page = tieba_content_page()
    url_page = 'http://tieba.baidu.com/f'
    pn = int(input('总页码为[%s]请输入要查询的页数编码【以50的倍数为准】' % (sum_page,)))
    params = {
        'kw': 'python',
        'ie': 'utf-8',
        'pn': pn,
    }
    if pn <= sum_page and pn % 50 == 0:
        page_html = requests.get(url_page, params=params, headers=headers1)
        page_content = page_html.content
        return page_content
    elif pn%50 != 0:
        print '您输入的页码编码不是50的倍数'
    elif pn > sum_page:
        print '您输入的页码编码大于总页码编码'

# 由于帖子列表是以<!-- -->注释形式展示，需要从得到的页面内容中找出真正需要的内容（正则）
def page_real_content(content):
    patterns = re.compile(r'<!--\s*?(<ul.*?div>)\s*?-->', re.DOTALL)
    real_content_search = re.search(patterns, content)
    print real_content_search
    real_content = real_content_search.group(1)
    return real_content

# 用来分析贴吧指定页面，提取帖子标题及链接
class tieba_page_paser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_div = False
        self.tiezi = []
        self.url_fist = 'http://tieba.baidu.com'

    def handle_starttag(self, tag, attrs):
        # print '[%s]%s' % (tag, attrs)
        if tag == 'div' and _attr(attrs, 'class') == 'threadlist_title pull_left j_th_tit ':
            self.in_div = True

        if tag == 'a' and self.in_div:
            every_tie = dict()
            every_tie['url'] = self.url_fist + _attr(attrs, 'href')
            every_tie['title'] = _attr(attrs, 'title')
            self.tiezi.append(every_tie)

    def handle_endtag(self, tag):
        if tag == 'div':
            self.in_div = False

# 提取贴吧指定页面贴子链接
def page_url_list():
    python_page_content = tieba_page_content()
    time.sleep(5)
    # print python_page_content
    print '=' * 99
    # page_real_content(python_page_content)
    python_real_content = page_real_content(python_page_content)
    parser_content = python_real_content.decode('utf8')
    page_url_parser = tieba_page_paser()
    page_url_parser.feed(parser_content)
    return page_url_parser.tiezi


def page_url():
    page_url_l = page_url_list()
    # print page_url_l
    print '[帖子列表]'
    for i in page_url_l:
        print i['title']
    title_input = raw_input('请输入您要查询的帖子名称【必须包含在帖子名称列表】')
    for j in page_url_l:
        title = j['title'].encode('utf8')
        if title == title_input:
            page_url = j['url']
            return page_url

# 分析指定帖子页面主页内容，提取页码
# 回复贴，共<span class="red">1</span>页
def tiezi_page(url_page):
    print url_page
    url_python = url_page
    tieba_html = requests.get(url_python, headers=headers1)
    tieba_con = tieba_html.content
    sumpage_pattern = re.compile(r'回复贴，共<span class="red">(\d*?)</span>页')
    sumpage_str = re.search(sumpage_pattern, tieba_con)
    sumpage = int(sumpage_str.group(1))
    return sumpage

# 提取指定帖子指定页面内容
def tiezi_page_content(url_page):
    sum_page = tiezi_page(url_page)
    url_page = url_page
    pn = int(input('总页码为[%s]请输入要查询的页数编码' % (sum_page,)))
    params = {
        'pn': pn,
    }
    if pn <= sum_page:
        page_html = requests.get(url_page, params=params, headers=headers1)
        page_content = page_html.content
        return page_content
    elif pn > sum_page:
        print '您输入的页码编码大于总页码编码'

# 分析指定页面指定帖子，提取用户名及用户头像链接
class user_paser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.user = []
        self.user_name = []
        self.user_check = []
        self.in_li = False

    def handle_starttag(self, tag, attrs):
        # print '[%s]%s' % (tag, attrs)
        if tag == 'li' and _attr(attrs, 'class') == 'icon':
            self.in_li = True
        # <li class="icon"> <img username="黄哥python培训" class="" src="http://tb.himg.baidu.com/sys/portrait/item/892fe9bb84e593a5707974686f6ee59fb9e8aeaded6a"/>
        if tag == 'img' and self.in_li and _attr(attrs, 'username'):
            every_user = dict()
            username2 = _attr(attrs, 'username')
            if username2 in self.user_check:
                self.user_name.append(username2)
            else:
                self.user_check.append(username2)
                self.user_name.append(username2)
                every_user['username'] = username2
                # http://tb2.bdstatic.com/tb/static-pb/img/head_80.jpg非真实地址，需要排除
                if _attr(attrs, 'src') == 'http://tb2.bdstatic.com/tb/static-pb/img/head_80.jpg':
                    every_user['img_src'] = _attr(attrs, 'data-tb-lazyload')
                else:
                    every_user['img_src'] = _attr(attrs, 'src')
                self.user.append(every_user)

    def handle_endtag(self, tag):
        if tag == 'li':
            self.in_li = False

# 分析指定页面，提取用户名及头像链接
def user_img_url(url_page):
    python_tiezi_content = tiezi_page_content(url_page)
    # print python_tiezi_content
    tiezi_parser = user_paser()
    tiezi_parser.feed(python_tiezi_content)
    username_tiezi = tiezi_parser.user_name
    print '[username all length]' + str(username_tiezi.__len__())
    return tiezi_parser.user

# 下载和保存用户头像
def _download_img(user_list, url_page):
    folder = url_page.split('/')[-1]
    host1 = 'tb.himg.baidu.com'
    headers2 = {
        'Host': host1,
        'User-Agent': agent,
    }
    if not os.path.exists(folder):
        os.mkdir(folder)
    for i in user_list:
        username_parser = i['username'].decode('utf8')
        userimg_parser = i['img_src']
        print username_parser
        print userimg_parser
        try:
            request = urllib2.Request(userimg_parser, headers=headers2)
            user_img = urllib2.urlopen(request)
            user_img_name = '%s/%s.jpg' % (folder, username_parser)
            f = open(user_img_name, 'wb')
            f.write(user_img.read())
            f.close()
        except Exception as e:
            print e


def download():
    url_page1 = page_url()
    user_list1 = user_img_url(url_page1)
    _download_img(user_list1, url_page1)


if __name__ == '__main__':
    download()


