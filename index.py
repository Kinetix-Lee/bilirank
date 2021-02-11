import urllib3, json
http = urllib3.PoolManager()

api = {
  'stat': 'https://api.bilibili.com/x/relation/stat',
  'upstat': 'https://api.bilibili.com/x/space/upstat'
}
req_stat = http.request('GET', api['stat'], 
                  fields={
                    'vmid': ''
                  })
print(json.loads(req_stat.data.decode('utf-8')))
