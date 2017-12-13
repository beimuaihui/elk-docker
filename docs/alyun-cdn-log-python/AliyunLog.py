# coding=utf-8

import fileinput
import re
import os
import time

try:
    import simplejson as json
except ImportError:
    import json


# 读取输入文件并返回Dict对象
def readfile(file):
    filecontent = {}
    index = 0
    statinfo = os.stat(file)

    # just a guestimate. I believe a single entry contains atleast 150 chars
    if statinfo.st_size < 150:
        print "Not a valid log file. It does not have enough data"
    else:
        for line in fileinput.input(file):
            index = index + 1
            if line != "\n":  # don't read newlines
                filecontent[index] = line2dict(line)

        fileinput.close()
    return filecontent


# 将单条记录转换为Dict对象
def line2dict(line):
    # Snippet, thanks to http://www.seehuhn.de/blog/52
    parts = [
        r'\[(?P<time>.+)\]',        # 时间 %t
        r'(?P<res_ip>\S+)',         # 访问IP %h
        r'(?P<origin_ip>\S+)',      # 回源IP %h
        r'(?P<res_time>[0-9]+)',    # 响应时间 %>s
        r'"(?P<referer>.*)"',       # Referer "%{Referer}i"
        r'"(?P<req_url>.+)"',       # 请求地址 "%r"
        r'(?P<http_code>[0-9]+)',   # Httpcode %>s
        r'(?P<req_size>\S+)',       # 请求大小 %b (careful, can be '-')
        r'(?P<res_size>[0-9]+)',    # 响应大小 size %>s
        r'(?P<cache_status>\S+)',   # 缓存状态 %s
        r'"(?P<ua>.*)"',            # user agent "%{User-agent}i"
        r'"(?P<content_type>.*)"',  # content type "%{Content-type}i"
    ]
    pattern = re.compile(r'\s+'.join(parts) + r'\s*\Z')
    m = pattern.match(line)
    res = m.groupdict()
    print json.dumps(res)
    time.sleep( 3 )
    return res


# 转换整个记录为Json对象
def toJson(file):
    entries = readfile(file)    
    return json.JSONEncoder(indent=4).encode(entries)