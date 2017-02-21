# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 12:14:02 2017

@author: HW
"""
## use dictionary to optimize.


def get_page(url):
    try:
        if url == "http://www.udacity.com/cs101x/index.html":
            return '''<html> <body> This is a test page for learning to crawl!
<p> It is a good idea to
<a href="http://www.udacity.com/cs101x/crawling.html">
learn to crawl</a> before you try to
<a href="http://www.udacity.com/cs101x/walking.html">walk</a> or
<a href="http://www.udacity.com/cs101x/flying.html">fly</a>.</p></body></html>'''

        elif url == "http://www.udacity.com/cs101x/crawling.html":
            return '''<html> <body> I have not learned to crawl yet, but I am
quite good at  <a href="http://www.udacity.com/cs101x/kicking.html">kicking</a>.
</body> </html>'''

        elif url == "http://www.udacity.com/cs101x/walking.html":
            return '''<html> <body> I cant get enough
<a href="http://www.udacity.com/cs101x/index.html">crawling</a>!</body></html>'''

        elif url == "http://www.udacity.com/cs101x/flying.html":
            return '<html><body>The magic words are Squeamish Ossifrage!</body></html>'
        elif url == "http://www.udacity.com/cs101x/kicking.html":        ##These three lines are added by myself
            return '''<html>\n<body>\n<b>Kick! Kick! Kick!</b>\n</body>\n</html>'''
    except:
        return ""
    return ""

def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)


def add_to_index(index, keyword, url):
    # format of index: {keyword:[[url, count], [url, count],..],...}
    if keyword in index:
        exi = False
        for s in index[keyword]:
            if s[0] == url:
                exi == True
                break
        if not exi:
            index[keyword].append([url, 0])
    else:
        # not found, add new keyword to index
        index[keyword] = [[url, 0]]

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)                ##此url下的content，建索引时content里的word会关联到此url
            add_page_to_index(index, page, content)
            union(tocrawl, get_all_links(content))
            crawled.append(page)
    return index

def record_user_click(index, keyword, url):         ##standard answer
    urls = lookup(index, keyword)                   ##如果index中没有此keyword-url对，则不操作。
    if urls:
        for entry in urls:
            if entry[0] == url:
                entry[1] = entry[1] + 1

#Here is an example showing a sequence of interactions:
index = crawl_web('http://www.udacity.com/cs101x/index.html')
print(lookup(index, 'href="http://www.udacity.com/cs101x/kicking.html">kicking</a>.'))  ##体会一下split()函数
print (lookup(index, 'good'))
print(lookup(index, 'Kick!'))
#>>> [['http://www.udacity.com/cs101x/index.html', 0],
#>>> ['http://www.udacity.com/cs101x/crawling.html', 0]]
record_user_click(index, 'good', 'http://www.udacity.com/cs101x/crawling.html')
record_user_click(index, 'Kick!', 'http://www.udacity.com/cs101x/kicking.html')
print (lookup(index, 'good'))
print (lookup(index, 'Kick!'))
#>>> [['http://www.udacity.com/cs101x/index.html', 0],
#>>> ['http://www.udacity.com/cs101x/crawling.html', 1]]




