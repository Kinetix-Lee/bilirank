#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib3, sys, toml, json
from time import sleep
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

listName = []
listFollower = []
dataMap = []

# 调试打印程序
def printDebug(content, condition=True):
  print('[DEBUG]', content) if condition else True;

print('\nBiliRank - 哔哩哔哩数据自动化程序')
print('https://github.com/Kinetix-Lee/bilirank\n')

# 读取配置文件
print('正在载入配置文件')
try:
  # 打开并解析
  f_bilirank_toml = open(paths['config'], 'r')
  config = toml.load(f_bilirank_toml)
  
  uploaderCount = len(config['bilirank']['listUploader'])
  print('配置文件载入成功')
  print('待查询的 up 主数量:', uploaderCount)
  
  if dev['ignoreAntiFlood']:
    print('Anti-Flood 机制被忽略，若人数 >= 200 建议重新开启')
  else:
    print('人数多，每次访问将会增加一定延迟') if uploaderCount > 200 else True;
  
  printDebug(config, dev['printConfig'])
  
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
    
    listName.append(name)
    listFollower.append(follower)
    
    print('用户数据已载入: {name} ({id})，粉丝数量 {fans}'.format(name=name, id=id, fans=follower))
    printDebug(response, dev['printResponse'])
    
    # anti flood
    if uploaderCount >= 180:
      sleep(75)
    
# 错误处理
except OSError as err: 
  print('配置文件读取错误\n{0}'.format(err))
except KeyboardInterrupt as err:
  print('程序退出')
except:
  print('未知错误', sys.exc_info()[0])
finally:
  f_bilirank_toml.close() # 关闭文件
  for index in range(len(listName)): # 换成 listFollower 理论上也行得通
    dataMap.append([listName[index], listFollower[index]])
  print('查询完毕')
  printDebug(dataMap, dev['printDataMap'])

# req_stat = http.request('GET', api['stat'], 
#                   fields={
#                     'vmid': ''
#                   })
# print(json.loads(req_stat.data.decode('utf-8')))
