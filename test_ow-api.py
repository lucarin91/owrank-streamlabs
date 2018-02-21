"""
examples:
    https://owapi.net/api/v3/u/serranda-2860/stats
    https://ow-api.herokuapp.com/profile/pc/eu/serranda-2860
"""
import httplib
import json

BASE_URL = 'ow-api.herokuapp.com'
NICK = 'serranda-2860'
PATH_URL = '/profile/pc/eu/{}'.format(NICK)

c = httplib.HTTPSConnection(BASE_URL)
c.request("GET", PATH_URL)#, headers={"User-Agent":"Linux/generic"})
response = c.getresponse()

if response.status != 200:
    print response.status, response.reason

data_raw = response.read()
data = json.loads(data_raw)
if data is None or ('competitive' not in data
                    and 'rank' not in data['competitive']):
    print 'json error'

rank = data['competitive']['rank']
print 'rank:', data['competitive']['rank']