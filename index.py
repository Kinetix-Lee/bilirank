#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import urllib3, toml, json, development, datetime
from time import sleep
from datetime import datetime
http = urllib3.PoolManager()
dev = development.devVariables()

PATH_CONFIG = 'config/bilirank.toml'
API_CARD = 'https://api.bilibili.com/x/web-interface/card'

listUploader = []
listName = []
listFollower = []
dataMap = {}
differenceFollower = {}

# 调试打印程序
def printDebug(content, condition=True):
  print('[DEBUG]', content) if condition else True;

print('\nBiliRank - 哔哩哔哩数据自动化程序')
print('https://github.com/Kinetix-Lee/bilirank\n')

# 读取配置文件
print('正在载入配置文件')
# 打开并解析
f_bilirank_toml = open(PATH_CONFIG, 'r')
config = toml.load(f_bilirank_toml)['bilirank']
f_bilirank_toml.close() # 关闭文件

READ_LAST_OUTPUT = ('readOutput' in config and config['readOutput']) # 若配置文件要求使用上一次的结果，则载入
PATH_OUTPUT = config['output'] \
  if ('output' in config and type(config['output']) == str) \
  else 'config/result.bilirank.json' # 若配置文件要求使用特定路径的结果，则载入

if READ_LAST_OUTPUT:
  print('使用上一次的结果 ({0}) 作为配置文件'.format(PATH_OUTPUT))
  print('请注意，原配置文件 (bilirank.toml) 中 listUploader 字段将会被忽略')
  
  print('正在载入配置文件')
  try:
    f_result_bilirank_json_input = open(PATH_OUTPUT, 'r')
    result_input = json.load(f_result_bilirank_json_input)
    f_result_bilirank_json_input.close()
    listUploader = list(result_input['listUploader'].keys())
    printDebug(result_input, dev['printConfig'])
  except: 
    print('配置文件非法，正在使用普通模式')
    READ_LAST_OUTPUT = False # Editing a 'constant' is kinda violation. Awaiting correction.
    listUploader = config['listUploader']
else:
  listUploader = config['listUploader']

uploaderCount = len(config['listUploader'])
print('待查询的 up 主数量:', uploaderCount)

if dev['ignoreAntiFlood']:
  print('Anti-Flood 机制被忽略，若人数 >= 200 建议重新开启')
else:
  print('人数多，每次访问将会增加一定延迟') if uploaderCount > 200 else True;

printDebug(config, dev['printConfig'])

# 逐个进行请求
for id in listUploader:
  request = http.request('GET', API_CARD,
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

# 生成 dataMap 和 differenceFollower
for index in range(len(listUploader)):
  dataMap[listUploader[index]] = [listName[index], listFollower[index]]
  differenceFollower[listUploader[index]] =\
    listFollower[index] - result_input['listUploader'][listUploader[index]][1]\
    if READ_LAST_OUTPUT\
    else {}

print('查询完毕')
printDebug(dataMap, dev['printDataMap'])

print('生成输出信息')
now = datetime.now().timestamp()
result = {
  'timestamp': now,
  'listUploader': dataMap,
  'lastData': {}, # available if READ_LAST_OUTPUT
  'differences': {} # available if READ_LAST_OUTPUT
}
if READ_LAST_OUTPUT:
  # 禁止套娃
  del result_input['lastData']
  # del result_input['differences']
  
  result['lastData'] = result_input
  result['differences'] = {
    'timestamp': int(now - result_input['timestamp']),
    'follower': differenceFollower
  }
  
printDebug(json.dumps(result, indent = 2 if dev['jsonPrettify'] else None), dev['printResult'])

print('导出文件')
f_result_bilirank_json = open(PATH_OUTPUT, 'w+')
json.dump(result, f_result_bilirank_json)
f_result_bilirank_json.close()

print('完成')
