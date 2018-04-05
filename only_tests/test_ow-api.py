"""
examples:
    https://owapi.net/api/v3/u/sedia-21534/stats
    https://ow-api.herokuapp.com/profile/pc/eu/serranda-2863
"""
import urllib2
import json

NICK = 'sedia-23434'
REGION = 'eu'
URL = 'https://owapi.net/api/v3/u/{}/stats'.format(NICK)

# c = httplib.HTTPSConnection(BASE_URL)
# c.request("GET", PATH_URL)#, headers={"User-Agent":"Linux/generic"})
# response = c.getresponse()

# if response.status != 200:
#     print response.status, response.reason

# data_raw = response.read()
# data = json.loads(data_raw)
# if data is None or ('competitive' not in data
#                     and 'rank' not in data['competitive']):
#     print 'json error'

# rank = data['competitive']['rank']
# print 'rank:', data['competitive']['rank']

res = urllib2.Request(URL, headers={"User-Agent":"Linux/generic"})

opener = urllib2.build_opener()
res = opener.open(res)
data_raw = res.read()
# print 'DEBUG:', data_raw
data = json.loads(data_raw)
if not data\
   or not REGION in data\
   or not 'stats' in data[REGION]\
   or not 'competitive' in data[REGION]['stats']\
   or not 'overall_stats' in data[REGION]['stats']['competitive']\
   or not 'comprank' in data[REGION]['stats']['competitive']['overall_stats']:
    print 'json error'
    exit()

rank = data[REGION]['stats']['competitive']['overall_stats']['comprank']
print 'rank:', rank