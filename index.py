#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib3, sys, toml, json
from development import devVariables
http = urllib3.PoolManager()

paths = {
  'config': 'config/bilirank.toml',
  'api': {
    'card': 'https://api.bilibili.com/x/web-interface/card'
    # 'stat': 'https://api.bilibili.com/x/relation/stat',
    # 'upstat': 'https://api.bilibili.com/x/space/upstat'
  }
}
dev = devVariables()

# 调试打印程序
def debugPrint(content):
  print('[DEBUG]', content) if dev['printResponse'] else True;

print('\nBiliRank - 哔哩哔哩数据自动化程序')
print('https://github.com/Kinetix-Lee/bilirank\n')

# 读取配置文件
print('正在载入配置文件')
try:
  # 打开并解析
  f_bilirank_toml = open(paths['config'], 'r')
  config = toml.load(f_bilirank_toml)
  
  print('配置文件载入成功')
  print('待查询的 up 主数量:', len(config['bilirank']['listUploader']))
  debugPrint(config)
  
  # 逐个进行请求
  for id in config['bilirank']['listUploader']:
    request = http.request('GET', paths['api']['card'],
                  fields={
                    'mid': str(id),
                    'photo': False
                  })
    response = json.loads(request.data.decode('utf-8'))
    name = response['data']['card']['name']
    follower = response['data']['card']['fans']
    print('用户数据已载入: {name} ({id})，粉丝数量 {fans}'.format(name=name, id=id, fans=follower))
    debugPrint(response)
# 错误处理
except OSError as err: 
  print('配置文件读取错误\n{0}'.format(err))
except KeyboardInterrupt as err:
  print('程序退出')
except:
  print('未知错误', sys.exc_info()[0])
finally:
  f_bilirank_toml.close() # 关闭文件

# req_stat = http.request('GET', api['stat'], 
#                   fields={
#                     'vmid': ''
#                   })
# print(json.loads(req_stat.data.decode('utf-8')))
