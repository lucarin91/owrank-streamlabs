"""
examples:
    https://owapi.net/api/v3/u/serranda-2863/stats
    https://ow-api.herokuapp.com/profile/pc/eu/serranda-2863
"""
import urllib2
import json

NICK = 'serranda-2863'
URL = 'http://ow-api.herokuapp.com/profile/pc/eu/{}'.format(NICK)

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

res = urllib2.urlopen(URL)

data_raw = res.read()
data = json.loads(data_raw)
if not data or ('competitive' not in data
                and 'rank' not in data['competitive']):
    print 'json error'
    exit()

rank = data['competitive']['rank']
print 'rank:', data['competitive']['rank']