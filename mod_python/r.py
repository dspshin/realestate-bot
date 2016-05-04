#-*- coding: utf-8 -*-

from mod_python import apache
from mod_python import util

from urllib2 import Request, urlopen
from bs4 import BeautifulSoup
import re
import traceback

key = 'mcGA6xDEsvdIH3sbow%2B7gIBwxcGJC4dTkHt%2Bd7DXJ2pg2Gqq3g6IvU%2BLwFKCiqOQncYX2uI2Kav1yzRw7WO1RA%3D%3D'
url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?ServiceKey='+key


def howmuch(loc_param, date_param, apt, pyung):
    res=''
    data=[]
    request = Request(url+'&LAWD_CD='+loc_param+'&DEAL_YMD='+date_param)
    request.get_method = lambda: 'GET'
    try:
      res_body = urlopen(request).read()
    except:
      return '',[], traceback.format_exc().splitlines()[-1]

    soup = BeautifulSoup(res_body, 'html.parser')
    items = soup.findAll('item')
    for item in items:
        item = item.text.encode('utf-8')
        item = re.sub('<.*?>', '|', item)
        parsed = item.split('|')
        try:
            #res = parsed[3]+' '+parsed[4]+', '+parsed[7]+'m², '+parsed[9]+'F, '+parsed[1].strip()+'만원\n'
            if parsed[7]==pyung and parsed[4].find(apt)>-1:
              res+='<tr><td>'+parsed[2]+'/'+parsed[5]+'/'+parsed[6]+'</td><td>'+parsed[3]+' '+parsed[4]+'</td><td>'+parsed[7]+'</td><td>'+parsed[9]+'</td><td>'+parsed[1]+'</td></tr>'
              data.append( (parsed[2],parsed[5],parsed[6], parsed[1]) )
        except IndexError:
            continue
    return res, data, None

def howmuch2(loc_param, date_param, apt, pyung, to_param):
    res=''
    data=[]

    if to_param:
      for m in range(int(date_param), int(to_param)+1):
        d = m%100
        if d<1 or d>12:
          continue
        r,d,e = howmuch(loc_param, str(m), apt, pyung)
        if e:
          return '',[],e
        res+=r
        data.extend(d)
      return res, data, None

    return howmuch(loc_param, date_param, apt, pyung)


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

      <script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
      <!-- 아파트매매 배너 -->
      <center><ins class="adsbygoogle"
           style="display:inline-block;width:320px;height:100px"
           data-ad-client="ca-pub-2054582141950401"
           data-ad-slot="6593224489"></ins></center>
      <script>
      (adsbygoogle = window.adsbygoogle || []).push({});
      </script>

        <div id="chart" style="min-width: 310px; height: 400px; margin: 0 auto"></div>

        <div class="form-group">
          시작월 : <input id="sDate" class="form-control" type="text"/>
          <br/>
          종료월 : <input id="eDate" class="form-control" type="text"/>
          <br/>
          <button type="button" class="btn btn-default" id="search">위 날자로 다시 월단위 검색!</button>
        </div>
        <div class="col-md-6">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>거래일</th>
                <th>아파트명</th>
                <th>평수(m²)</th>
                <th>층수(F)</th>
                <th>거래액(만원)</th>
              </tr>
            </thead>
            <tbody>
"""

def handler(req):
  req.content_type="Text/html"
  req.send_http_header()
  fs = util.FieldStorage(req)

  loc_param = fs.getfirst('l', None)
  date_param = fs.getfirst('d', None)
  apt = fs.getfirst('a',None)
  pyung = fs.getfirst('p',None)
  date_to = fs.getfirst('t', None)
  trs, data, error = howmuch2(loc_param, date_param, apt, pyung, date_to)

  prices = []
  for d in data:
    day = "21"
    if d[2].find("10")>-1:
      day="1"
    elif d[2].find("20")>-1:
      day="11"
    price = d[3].replace(",","").strip()
    prices.append("[Date.UTC("+d[0]+","+d[1]+","+day+"),"+price+"]")

  prices = str(prices).replace("'","")
  html2="""
            </tbody>
          </table>
        </div>
    </div>

    <div class="container theme-showcase">
      <div class="well">
        <p>개인서버라 속도가 굉장히 느리고, 거래정보를 얻고 있는 data.go.kr이 502 proxy를 에러를 내는 경우가 굉장히 많습니다. 양해 부탁드립니다.</p>
      </div>
    </div>

    <script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
    <!-- 아파트매매 footer -->
    <center><ins class="adsbygoogle"
         style="display:inline-block;width:336px;height:280px"
         data-ad-client="ca-pub-2054582141950401"
         data-ad-slot="2023424088"></ins></center>
    <script>
    (adsbygoogle = window.adsbygoogle || []).push({});
    </script>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>

    <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">

    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>

    <script>
    $(function() {
      $("#sDate,#eDate").datepicker();

      $("#search").click(function() {
        var s = $("#sDate").val(),
            e = $("#eDate").val(),
            date_param, date_to, url, params, i, params2=[], key;

        if (s && e) {
          date_param = s.split("/")[2]+s.split("/")[0];
          date_to = e.split("/")[2]+e.split("/")[0];

          url = location.origin + location.pathname + "?";
          params = location.search.slice(1).split("&");
          for(i in params) {
            key = params[i].split("=")[0];
            if (key==="l" || key==="a" || key==="p") {
              params2.push( params[i] );
            }
          }
          params2.push("d="+date_param);
          params2.push("t="+date_to);
          location.replace( url + params2.join("&") );
        } else {
          alert("시작월, 종료월을 선택해야 합니다.");
        }
      });

      $('#chart').highcharts({
        chart: {
            zoomType: 'x'
        },
        title: {
            text: '%s 매매가 추이 그래프'
        },
        subtitle: {
            text: document.ontouchstart === undefined ?
                    'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: '거래액 (만원)'
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        },

        series: [{
            type: 'area',
            name: '거래액',
            data: %s
        }]
      });

      var error='%s';
      if (error !== "None") {
        alert(error);
      }
    });
    </script>

  </body>
</html>
"""%(apt, prices, error)

  req.write(html1 + trs + html2)
  return apache.OK

