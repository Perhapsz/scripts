from email import charset
import requests
import re
import os


class NovelSpider:
    def __init__(self):
        #下载器
        self.session = requests.Session()

    def get_novel(self, url):
        # 下载小说的首页面html
        index_html = self.download(url, encoding='gbk')

        # 提取小说标题
        title = self.get_title(index_html)
        print(title)
        work_dir = os.getcwd()
        novel_dir = work_dir + '\\' + title
        print(novel_dir)
        if not os.path.exists(novel_dir):
             os.makedirs(novel_dir)
        os.chdir(novel_dir)
        # 提取章节信息， url 网址
        novel_chapter_infos = self.get_chapter_info(index_html)
        for chapter_info in novel_chapter_infos:
            chapter_url = url + chapter_info[0]
            fb = open('%s.txt' % chapter_info[1], 'w', encoding='utf-8')
            content = self.get_chapter_content(chapter_url)
            fb.write(content)
            fb.write('\n')
            print(content)
            fb.close()

        os.chdir(work_dir)

    def get_chapter_content(self, chapter_url):
        chapter_html = self.download(chapter_url, encoding='gbk')
        content = re.findall(r'<div id="content">(.*?)</div>', chapter_html, re.S)[0]
        content = content.replace('&nbsp;', '')
        content = content.replace('<br />', '')
        content = content.replace('\r\n', '')
        return content

    def download(self, url, encoding):
        headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
                'Referer': "https://creator.douyin.com/"
        }
        response = self.session.get(url, headers=headers)
        response.encoding = encoding
        html = response.text
        return html

    def get_chapter_info(self, index_html):
        # 提取章节
        div = re.findall(r'<div class="box_con">.*?<div id="list">.*?</div>', index_html, re.S)[0]
        # print(div)

        # <a href="/32_32803/49431020.html">第997章 大结局！</a>
        info = re.findall(r'<dd><a href="(.*?)">(.*?)</a>', div)
        # print(info)
        return info

    def get_title(self, index_html):
        titile = re.findall(r'<h1>(.*?)</h1>', index_html, re.S)[0]
        return titile


if __name__ == '__main__':
    novel_url = 'https://www.qbiqu.com/32_32803/'
    spider = NovelSpider()
    spider.get_novel(novel_url)