代码流程

1.获取贴吧某个帖子的链接：
a,通过贴吧主页地址获取总页码（正则）；
b,指定页码，分析内容，获取帖子链接（帖子列表是以<!-- -->注释形式展示，HTMLparser需要先将注释内容提取-正则）；
c,指定标题，获取帖子链接。

2.获取帖子内用户信息：
a,获取帖子页数；
b,指定页码，分析页面，用户名和img地址（src:http://tb2.bdstatic.com/tb/static-pb/img/head_80.jpg非真实地址，需要排除和寻找真实地址）；
c,去除重复的用户名及地址（分析时可直接剔除）。

3.下载图片，存储。
