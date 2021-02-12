#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib3, sys, toml
from development import devVariables
http = urllib3.PoolManager()

paths = {
  'config': 'config/bilirank.toml',
  'stat': 'https://api.bilibili.com/x/relation/stat',
  'upstat': 'https://api.bilibili.com/x/space/upstat'
}
dev = devVariables()

print('\nBiliRank - 哔哩哔哩数据自动化程序')
print('https://github.com/Kinetix-Lee/bilirank\n')

# 读取配置文件
print('正在载入配置文件')
try:
  f_bilirank_toml = open(paths['config'], 'r')
  config = toml.load(f_bilirank_toml)
  print('配置文件载入成功')
  print(config) if dev['printConfig'] else True;
except OSError as err: 
  print('配置文件读取错误\n{0}'.format(err))
except KeyboardInterrupt as err:
  print('程序退出')
except:
  print('未知错误', sys.exc_info()[0])
finally:
  f_bilirank_toml.close()

# req_stat = http.request('GET', api['stat'], 
#                   fields={
#                     'vmid': ''
#                   })
# print(json.loads(req_stat.data.decode('utf-8')))
