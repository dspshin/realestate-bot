#-*- coding: utf-8 -*-

from mod_python import apache
from mod_python import util

from urllib2 import Request, urlopen
from bs4 import BeautifulSoup
import re
import traceback

key = 'mcGA6xDEsvdIH3sbow%2B7gIBwxcGJC4dTkHt%2Bd7DXJ2pg2Gqq3g6IvU%2BLwFKCiqOQncYX2uI2Kav1yzRw7WO1RA%3D%3D'
url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?ServiceKey='+key


def howmuch(loc_param, date_param, dong, apt, pyung):
    res_list = []
    res=''

    request = Request(url+'&LAWD_CD='+loc_param+'&DEAL_YMD='+date_param)
    request.get_method = lambda: 'GET'
    try:
        res_body = urlopen(request).read()
    except UnicodeEncodeError:
        res = ['오류가 발생했습니다. 명령어를 정확히 사용했는지 확인해 보세요.']
        return res

    soup = BeautifulSoup(res_body, 'html.parser')
    items = soup.findAll('item')
    for item in items:
        item = item.text.encode('utf-8')
        item = re.sub('<.*?>', '|', item)
        parsed = item.split('|')
        try:
            #res = parsed[3]+' '+parsed[4]+', '+parsed[7]+'m², '+parsed[9]+'F, '+parsed[1].strip()+'만원\n'
            res+='<tr><td>'+parsed[3]+' '+parsed[4]+'</td><td>'+parsed[7]+'</td><td>'+parsed[9]+'</td><td>'+parsed[1]+'</td></tr>'
        except IndexError:
            continue

    return res


html1 = """
<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>아파트 매매 추이</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>


    <!-- Fixed navbar -->
    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">아파트 매매 추이</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li><a href="#about">About</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container theme-showcase" role="main" style="margin-top:60px;">
        <div class="col-md-6">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>아파트명</th>
                <th>평수(m²)</th>
                <th>층수(F)</th>
                <th>거래액(만원)</th>
              </tr>
            </thead>
            <tbody>
"""

html2="""
            </tbody>
          </table>
        </div>
    </div>


    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>

    <script>
      var key = 'mcGA6xDEsvdIH3sbow%2B7gIBwxcGJC4dTkHt%2Bd7DXJ2pg2Gqq3g6IvU%2BLwFKCiqOQncYX2uI2Kav1yzRw7WO1RA%3D%3D',
          url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?ServiceKey='+key;
      // request = Request(url+'&LAWD_CD='+loc_param+'&DEAL_YMD='+date_param)
      $.get( url ).done(function(res) {
        console.log('success:', res);
      }).fail(function(res){
        console.log('fail:', res);
      })
    </script>


  </body>
</html>
"""

def handler(req):
  req.content_type="Text/html"
  req.send_http_header()
  fs = util.FieldStorage(req)

  loc_param = fs.getfirst('l', None)
  date_param = fs.getfirst('d', None)
  trs = howmuch(loc_param, date_param, None, None, None)

  req.write(html1 + trs + html2)
  return apache.OK

