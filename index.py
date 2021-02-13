#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib3, sys, toml, json, development, datetime
from time import sleep
from datetime import datetime
http = urllib3.PoolManager()
dev = development.devVariables()

paths = {
  'config': 'config/bilirank.toml',
  'output': 'config/result.bilirank.json',
  'api': {
    'card': 'https://api.bilibili.com/x/web-interface/card'
    # 'stat': 'https://api.bilibili.com/x/relation/stat',
    # 'upstat': 'https://api.bilibili.com/x/space/upstat'
  }
}

listId = []
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
  config = toml.load(f_bilirank_toml)['bilirank']
  
  # 若配置文件要求使用上一次的结果，则载入
  if ('readOutput' in config and config['readOutput'] == True):
    # 若配置文件要求使用特定路径的结果，则载入
    if ('output' in config and type(config['output']) == str):
      paths['output'] = config['output']
    config['listUploader'] = []
    print('使用上一次的结果 ({0}) 作为配置文件'.format(paths['output']))
    print('请注意，原配置文件 (bilirank.toml) 中 listUploader 字段将会被忽略')
    
    print('正在载入配置文件')
    try:
      f_result_bilirank_json_input = open(paths['output'], 'r')
      result_input = json.load(f_result_bilirank_json_input)
      config['result_input'] = result_input
      print('配置文件载入成功')
    except OSError as err: 
      print('配置文件读取错误', err)
    finally:
      f_result_bilirank_json_input.close()
      
    for uploader in config['result_input']['listUploader']:
      config['listUploader'].append(uploader[0])
      
    printDebug(result_input, dev['printConfig'])
    
  uploaderCount = len(config['listUploader'])
  print('配置文件载入成功')
  print('待查询的 up 主数量:', uploaderCount)
  
  if dev['ignoreAntiFlood']:
    print('Anti-Flood 机制被忽略，若人数 >= 200 建议重新开启')
  else:
    print('人数多，每次访问将会增加一定延迟') if uploaderCount > 200 else True;
  
  printDebug(config, dev['printConfig'])
  
  # 逐个进行请求
  for id in config['listUploader']:
    request = http.request('GET', paths['api']['card'],
                  fields={
                    'mid': str(id),
                    'photo': False
                  })
    response = json.loads(request.data.decode('utf-8'))
    
    name = response['data']['card']['name']
    follower = response['data']['card']['fans']
    
    listId.append(id)
    listName.append(name)
    listFollower.append(follower)
    
    print('用户数据已载入: {name} ({id})，粉丝数量 {fans}'.format(name=name, id=id, fans=follower))
    printDebug(response, dev['printResponse'])
    
    # anti flood
    if uploaderCount >= 180:
      sleep(75)
    
# 错误处理
except OSError as err: 
  print('配置文件读取错误', err)
except KeyboardInterrupt as err:
  print('程序退出')
except:
  print('未知错误', sys.exc_info()[0])
finally:
  f_bilirank_toml.close() # 关闭文件
  for index in range(len(listName)): # 换成 listFollower 理论上也行得通
    dataMap.append([listId[index], listName[index], listFollower[index]])
  
  print('查询完毕')
  dataMap.sort(key=lambda el: el[0])
  printDebug(dataMap, dev['printDataMap'])
  
  print('生成输出信息')
  result = json.dumps({
    'timestamp': datetime.now().timestamp(),
    'lastTimestamp': config['result_input']['timestamp'] 
      if ('readOutput' in config and config['readOutput'] == True)
      else 0,
    'listUploader': dataMap
  })
  printDebug(result, dev['printResult'])
  
  print('导出文件')
  try:
    f_result_bilirank_json = open(paths['output'], 'w+')
    f_result_bilirank_json.write(result)
  except OSError as err:
    print('导出失败', err)
  finally:
    f_result_bilirank_json.close()
  
  print('完成')

# req_stat = http.request('GET', api['stat'], 
#                   fields={
#                     'vmid': ''
#                   })
# print(json.loads(req_stat.data.decode('utf-8')))
