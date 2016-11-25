from urllib2 import Request, urlopen
from urllib import urlencode, quote_plus
import sys
import re
from bs4 import BeautifulSoup

key = 'mcGA6xDEsvdIH3sbow%2B7gIBwxcGJC4dTkHt%2Bd7DXJ2pg2Gqq3g6IvU%2BLwFKCiqOQncYX2uI2Kav1yzRw7WO1RA%3D%3D'
#url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade'
#url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?_wadl&type=xml'
url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?LAWD_CD=11110&DEAL_YMD=201512&ServiceKey='+key

#queryParams = '?' + urlencode({ quote_plus('ServiceKey') : key, quote_plus('numOfRows') : '999', quote_plus('pageNo') : '1' })

#print url+queryParams

request = Request(url)
request.get_method = lambda: 'GET'
res = urlopen(request).read()
#print res

soup = BeautifulSoup(res, 'html.parser')
items = soup.findAll('item')
for i,item in enumerate(items):
    print i, item.text

    item = item.text.encode('utf-8')
    item = re.sub('<.*?>', '|', item)
    parsed = item.split('|')
    print parsed
    row = parsed[3]+'/'+parsed[6]+'/'+parsed[7]+', '+parsed[4]+' '+parsed[5]+', '+parsed[8]+'m, '+parsed[11]+'F, '+parsed[1].strip()+'\n'
    print row
    print