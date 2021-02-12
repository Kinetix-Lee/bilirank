#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib3, sys, toml
http = urllib3.PoolManager()

paths = {
  'config': 'config/bilirank.toml',
  'stat': 'https://api.bilibili.com/x/relation/stat',
  'upstat': 'https://api.bilibili.com/x/space/upstat'
}

print('BiliRank - 哔哩哔哩数据自动化程序\nhttps://github.com/Kinetix-Lee/bilirank\n')

# 读取配置文件
print('正在读取配置文件')
try:
  bilirank_toml = open(paths['config'])
  config = toml.load(bilirank_toml)
  print(config)
except OSError as err: 
  print('配置文件读取错误：\n{0}'.format(err))
except KeyboardInterrupt as err:
  print('程序退出\n')
except:
  print('未知错误：\n', sys.exc_info()[0])

# req_stat = http.request('GET', api['stat'], 
#                   fields={
#                     'vmid': ''
#                   })
# print(json.loads(req_stat.data.decode('utf-8')))
