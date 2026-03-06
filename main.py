# -*- coding:utf-8 -*-
"""
  此网站是个瑞数5代cookie加密网站
  根据瑞数特点，设计验证函数
  验证函数1：
    第一次请求首页，获取服务器返回的cookie，解析返回的数据
    运行瑞数代码，获取真正的cookie
  验证函数2：
    第二次请求首页，返回状态码200，表示成功
    后续获取数据即可
"""

import time
import urllib.parse
from loguru import logger as log  # 日志模块
import requests
from lxml import etree
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs
from requests.utils import dict_from_cookiejar
import csv
import os


class HN:
  # 初始化函数
  def __init__(self, index_url, data_url, file_csv='招标公告.csv'):
    self.csv_file = file_csv
    self._init_csv()
    self.url = index_url
    self.data_url = data_url
    self.header = {
      "Accept-Language": "zh-CN,zh;q=0.9",
      "accept": "application/json, text/plain, */*",
      "origin": "https://www.114yygh.com",
      "request-source": "UNICOM_SERVICE",
      "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Android WebView\";v=\"127\", \"Chromium\";v=\"127\"",
      "sec-ch-ua-mobile": "?1",
      "sec-ch-ua-platform": "Android",
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "navigate",
      "sec-fetch-site": "same-origin",
      "upgrade-insecure-requests": "1",
      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"
    }
    self.cookies = {}
    self.compile = None
    self.session = requests.Session()
  
  # 创建.csv文件
  def _init_csv(self):
    # 如果文件不存在，创建并写入表头
    if not os.path.exists(self.csv_file):
      with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['公告ID','标题','招标编号','创建时间','活跃时间','平台'])
    
  
  # 验证函数1
  def first_request(self):
    # verify=False：忽略证书验证
    response = self.session.get(url=self.url, headers=self.header, verify=False)
    # 将返回的cookies，变为普通的字典
    cookies_dict = dict_from_cookiejar(response.cookies)
    # update：“添加/更新”字典,将一个字典合并到另一个字典中,如果键存在,新值覆盖旧值,键不存在,添加新键值对
    self.cookies.update(cookies_dict)
    # 打印日志
    log.info('rs提交第一次: %d' % response.status_code)
    
    # 解析文本
    tree = etree.HTML(response.content.decode())
    content = tree.xpath('//meta/@content')[-1]
    ts_code = tree.xpath('//script/text()')[0]
    # 拆解首页地址
    path = urllib.parse.urlparse(self.url)
    # 拼接外接js地址
    js_url = path.scheme + "://" + path.netloc + tree.xpath('//script[2]/@src')[0]
    header = {
      "Accept": "*/*",
      "Accept-Language": "zh-CN,zh;q=0.9",
      "Cache-Control": "no-cache",
      "Connection": "keep-alive",
      "Pragma": "no-cache",
      "Referer": "https://www.114yygh.com/newhlwyl/mobile/appointmentRegisterHome?pathchannel=bjwechat",
      "Sec-Fetch-Dest": "script",
      "Sec-Fetch-Mode": "no-cors",
      "Sec-Fetch-Site": "same-origin",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
      "sec-ch-ua": "\"Chromium\";v=\"142\", \"Google Chrome\";v=\"142\", \"Not_A Brand\";v=\"99\"",
      "sec-ch-ua-mobile": "?1",
      "sec-ch-ua-platform": "\"Android\""
    }
    # 获取js代码
    js_code = requests.get(url=js_url, headers=header, verify=False).text
    # 将“browwer”文件中的ts和js代码进行替换，形成新的js文件，产生新的cookie
    new_js_code = open('browwer.js', 'r', encoding='utf-8').read().replace('content1', content).replace('"ts_code"', ts_code).replace('"fun_code"', js_code)
    # 创建一个新的js文件，存储获取到的瑞数代码，方便获取数据时，因cookie时效问题，方便随时调取获取新cookie
    with open('new_browwer.js', 'w', encoding='utf-8') as f:
      f.write(new_js_code)
    self.compile = execjs.compile(new_js_code)
    cookie = self.compile.call('get_cookie')
    # 分割cookie，获取cookie值
    new_cookies = {cookie.split('=')[0]: cookie.split('=')[1].split(';')[0]}
    # 更新cookie字典
    self.cookies.update(new_cookies)
      
  # 验证函数2
  def second_request(self):
    # 间隔请求时间
    time.sleep(1)
    response = requests.get(url=self.url, headers=self.header, cookies=self.cookies, verify=False)
    print(response.status_code)
    log.info('rs提交第二次: %s' % response.status_code)
    return response.status_code
  
  # 数据获取函数
  def get_data(self,page,max_retries=3):
    print('正在获取%s页数据'%page)
    header = {
      "accept": "application/json, text/plain, */*",
      "accept-encoding": "gzip, deflate, br, zstd",
      "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
      "cache-control": "no-cache",
      "connection": "keep-alive",
      "content-length": "59",
      "content-type": "application/json",
      "host": "ec.chng.com.cn",
      "origin": "https://ec.chng.com.cn",
      "pragma": "no-cache",
      "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Microsoft Edge\";v=\"145\", \"Chromium\";v=\"145\"",
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": "\"Windows\"",
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "same-origin",
      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"
    }
    # start 控制获取页数
    data = {
      "start": page,
      "limit": 10,
      "type": "103",
      "search": "",
      "ifend": ""
    }
    # 使用循环，设置最大重试次数，避免防止陷入无限递归
    for number in range(max_retries):
      response = requests.post(url=self.data_url, headers=header, json=data, cookies=self.cookies, verify=False)
      # 判断cookie是否还有用
      if response.status_code == 200:
        return response.json()
      else:
        print('%s页数据没有获取'%page)
        print('正在调用新js文件生成新cookie')
        # 调用新的js文件形成新的cookie
        js = execjs.compile(open('new_browwer.js', 'r', encoding='utf-8').read())
        cookie = js.call('get_cookie')
        # 分割cookie，获取cookie值
        new_cookies = {cookie.split('=')[0]: cookie.split('=')[1].split(';')[0]}
        # 更新cookie字典
        self.cookies.update(new_cookies)
        print('cookie已更新:',self.cookies)
    # 重试耗尽后仍未成功，可记录日志或抛出异常
    raise Exception(f"Failed to get data after {max_retries} attempts")

  
  # 解析数据
  def perse_data(self, data):
    json_data = data['root']
    for info in json_data:
      # id标识
      id = info['announcementId']
      # 标题
      title = info['announcementTitle']
      # 招标编号
      if info['businessInfo']:
        refer_number = info['businessInfo']+ '-01'
      else:
        refer_number = info['businessInfo']
      # 创建时间
      createtime = info['createtime']
      # 活跃时间
      activetime = info['activetime']
      # 平台
      platform = info['creator']
      
      # 调用保存函数
      self.save_data([id,title,refer_number,createtime,activetime,platform])


  # 数据保存函数
  def save_data(self, row_data):
    with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
      # 避免数据中存在特殊字符，仅在必要时加引号
      witer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
      witer.writerow(row_data)
  
  
  # 主函数
  def main(self):
    self.first_request()
    code = self.second_request()
    # 200表示cookie逆向成功，可以后续数据获取
    if code == 200:
      # 循环获取
      for page in range(0,31190,10):
        # 调用数据获取函数
        data = self.get_data(page=page)
        self.perse_data(data=data)
    else:
      print('首页请求失败，反爬没有处理掉哦!!!')


if __name__ == '__main__':
  # 华能电子商务平台地址
  index_url = 'https://ec.chng.com.cn/channel/home/#/purchase?top=0'
  # 招标数据地址
  data_url = 'https://ec.chng.com.cn/scm-uiaoauth-web/s/business/uiaouth/queryAnnouncementByTitle'
  execute = HN(index_url=index_url, data_url=data_url)
  execute.main()
