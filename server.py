from flask import Flask
from flask import request
from flask import jsonify
import os

app = Flask(__name__)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route('/manifest.webmanifest')
def manifest():
    return jsonify({
  "name": "Onstar Dialer",
  "short_name": "Onstar",
  "scope": "./",
  "start_url": "./home",
  "display": "standalone",
  "icons": [{
      "src": "static/icon.png",
      "sizes": "180x180"}]
})

@app.route('/start')
def start():
    html = '<!doctype html><html><head profile="http://www.w3.org/2005/10/profile"><link rel="apple-touch-icon" sizes="180x180" href="static/icon.png"><link rel="manifest" href="./manifest.webmanifest"><meta name="apple-mobile-web-app-capable" content="yes" /><meta name="viewport" id="viewport" content="width=device-width,minimum-scale=1.0,maximum-scale=1.0,initial-scale=1.0" /><meta http-equiv="ScreenOrientation" content="autoRotate:disabled"><meta charset="UTF-8"><title>Onstar Dialer</title></head><body><br><br><br><br><a href="/home"><img src="/static/logo.png" width="100%" border="0"></a></body></html>'
    return html

@app.route('/home')
def home():
    autodial = request.args.get('autodial')
    delay = request.args.get('delay')
    if (not delay):
        delay = ''
    if (not autodial):
        autodial=''
    html = '<!doctype html><html><head profile="http://www.w3.org/2005/10/profile"><link rel="apple-touch-icon" sizes="180x180" href="static/icon.png"><link rel="manifest" href="./manifest.webmanifest"><meta name="apple-mobile-web-app-capable" content="yes" /><meta name="viewport" id="viewport" content="width=device-width,minimum-scale=1.0,maximum-scale=1.0,initial-scale=1.0" /><meta http-equiv="ScreenOrientation" content="autoRotate:disabled"><meta charset="UTF-8"><title>Onstar Dialer</title><script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script><style type="text/css">body {	background-color: #000000;} table td { border-collapse:collapse; border-spacing:0px; border:0px; padding:0; } td,img { padding:0px; border-width:0px; margin:0px; display: block; } form {display:inline; margin:0; padding:0;} label {whitespace:nowrap;} .wrappable{white-space:normal; padding:0px;} input, textarea { border-radius: 0;} </style><script>(function(a,b,c){if(c in b&&b[c]){var d,e=a.location,f=/^(a|html)$/i;a.addEventListener("click",function(a){d=a.target;while(!f.test(d.nodeName))d=d.parentNode;"href"in d&&(d.href.indexOf("http")||~d.href.indexOf(e.host))&&(a.preventDefault(),e.href=d.href)},!1)}})(document,window.navigator,"standalone");</script></head><body><table width="100%" border="0" cellspacing="0" cellpadding="0" margin="0"><tbody><tr><td align="center"><form method="POST"><input type="image" class="wrappable" src="/static/dialerinfo/custname.png" formaction="/picture" style="display:inline; vertical-align:bottom" width="100%" height="auto" alt="" border="0" /></td></tr><tr><td align="center"><input type="image" class="wrappable" src="/static/dialerinfo/vehicle.png" formaction="/picture" style="display:inline; vertical-align:bottom" width="100%" height="auto" alt="" border="0" /></td></tr><tr><td align="left" width="100%" bgcolor="#f0f0f0"><input type="image" class="wrappable" src="/static/dialerinfo/r5type.png" formaction="/picture" style="display:inline; vertical-align:bottom" width="40%" height="auto" alt="" border="0" />&nbsp;&nbsp;&nbsp;<label for="autodial"><input type="checkbox" id="autodial" name="autodial" '+autodial+'><span class="wrappable">Autodial</span></label>&nbsp;<label for="delay"></label><input type="tel" size="3" id="delay" name="delay" value="'+str(delay)+'">&nbsp;Delay</td></tr><tr><td align="center"><input type="image" class="wrappable" src="/static/dial.png" formaction="/dial" width="100%" /></tr><tr><td align="center"><input type="image" class="wrappable" src="/static/machine.png" formaction="/machine" width="100%" /></tr><tr><td align="center"><input type="image" class="wrappable" src="/static/callback.png" formaction="/callback" width="100%" /></tr><tr><td align="center"><input type="image" class="wrappable" src="/static/hangup.png" formaction="/hangup" width="100%" /></tr><tr><td align="center"><input type="image" class="wrappable" src="/static/refusal.png" formaction="/refusal" width="100%" /></tr><tr><td align="center"><input type="image" class="wrappable" src="/static/donotcall.png" formaction="/donotcall" width="100%" /></tr><tr><td align="center"><input type="image" class="wrappable" src="/static/noanswer.png" formaction="/noanswer" width="100%" /></td></tr><tr><td align="center"><input type="image" class="wrappable" src="/static/language.png" formaction="/languagebarrier" width="100%" /></td></tr><tr><td align="center"><input type="image" class="wrappable" src="/static/scccomerror.png" formaction="/scccomerror" width="100%" /></form></td></tr></tbody></table></body></html>'
    return html

@app.route('/cert')
def cert():
    html = '<a href="/static/cert.pem">download certificate</a>'
    return html

@app.route('/dial', methods=['POST', 'GET'])
def dial():
    workflow = 'dial'
    autodial = ''
    selected = request.form.get('autodial')
    delay = request.form.get('delay')
    user_delay = str(delay).strip("'[]")
    if delay is None:
        autodial = request.args.get('autodial')
        user_delay = request.args.get('delay')
    if bool(selected):
        autodial = 'checked'
    if autodial == 'checked':
        workflow = 'autodial'
    os.system('open /Users/gabepersaud/Local\ Documents/server/'+workflow+'.app')
    html = '<!doctype html><html><head><meta charset="UTF-8"><title>Dispositioning Call</title><meta name="apple-mobile-web-app-capable" content="yes" /><style type="text/css">body,td,th {	color: #D9D9D9;	font-family: Gotham, "Helvetica Neue", Helvetica, Arial, sans-serif;	font-weight: bolder;}.big {	font-size: 164px;	}	.small {	font-size:48px;	}	body {	background-color: #4B4B4B;}</style></head><body><center>  <p>      <script>var timer = setTimeout(function() {{window.location="/home?autodial='+autodial+'&delay='+user_delay+'"}}, 2000);</script>      <br>      </p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p><span class="small">Dialing...</span><br></p>    <p class="big"><span id="counter">2</span></p><script type="text/javascript">function countdown() {    var i = document.getElementById("counter");    if (parseInt(i.innerHTML)!=0) {    i.innerHTML = parseInt(i.innerHTML)-1;}}setInterval(function(){ countdown(); },1000);	</script></center></body></html>'
    return html

@app.route('/machine', methods=['POST'])
def machine():
    location = 'picture'
    autodial = ''
    selected = request.form.get('autodial')
    user_delay = request.form.get('delay').strip("'[]")
    if (str(user_delay)=='None') or (not user_delay) or (int(user_delay)<6):
        delay = '6'
    else: delay = user_delay
    if bool(selected):
        location = 'dial'
        autodial = 'checked'
    os.system('open /Users/gabepersaud/Local\ Documents/server/machine.app')
    
    html = '<!doctype html><html><head><meta charset="UTF-8"><title>Dispositioning Call</title><meta name="apple-mobile-web-app-capable" content="yes" /><style type="text/css">body,td,th {	color: #D9D9D9;	font-family: Gotham, "Helvetica Neue", Helvetica, Arial, sans-serif;	font-weight: bolder;}.big {	font-size: 164px;	}	.small {	font-size:48px;	}	body {	background-color: #4B4B4B;}</style></head><body><center>  <p>      <script>var timer = setTimeout(function() {{window.location="/'+location+'?autodial='+autodial+'&delay='+user_delay+'"}}, '+delay+'000);</script>      <br>      </p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p><span class="small">Next lead in...</span><br></p>    <p class="big"><span id="counter">'+delay+'</span></p><script type="text/javascript">function countdown() {    var i = document.getElementById("counter");    if (parseInt(i.innerHTML)!=0) {    i.innerHTML = parseInt(i.innerHTML)-1;}}setInterval(function(){ countdown(); },1000);	</script></center></body></html>'
    return html

@app.route('/callback', methods=['POST'])
def callback():
    location = 'picture'
    autodial = ''
    selected = request.form.get('autodial')
    user_delay = request.form.get('delay').strip("'[]")
    if (str(user_delay)=='None') or (not user_delay) or (int(user_delay)<6):
        delay = '6'
    else: delay = user_delay
    if bool(selected):
        location = 'dial'
        autodial = 'checked'
    os.system('open /Users/gabepersaud/Local\ Documents/server/callback.app')
    
    html = '<!doctype html><html><head><meta charset="UTF-8"><title>Dispositioning Call</title><meta name="apple-mobile-web-app-capable" content="yes" /><style type="text/css">body,td,th {	color: #D9D9D9;	font-family: Gotham, "Helvetica Neue", Helvetica, Arial, sans-serif;	font-weight: bolder;}.big {	font-size: 164px;	}	.small {	font-size:48px;	}	body {	background-color: #4B4B4B;}</style></head><body><center>  <p>      <script>var timer = setTimeout(function() {{window.location="/'+location+'?autodial='+autodial+'&delay='+user_delay+'"}}, '+delay+'000);</script>      <br>      </p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p><span class="small">Next lead in...</span><br></p>    <p class="big"><span id="counter">'+delay+'</span></p><script type="text/javascript">function countdown() {    var i = document.getElementById("counter");    if (parseInt(i.innerHTML)!=0) {    i.innerHTML = parseInt(i.innerHTML)-1;}}setInterval(function(){ countdown(); },1000);	</script></center></body></html>'
    return html

@app.route('/hangup', methods=['POST'])
def hangup():
    location = 'picture'
    autodial = ''
    selected = request.form.get('autodial')
    user_delay = request.form.get('delay').strip("'[]")
    if (str(user_delay)=='None') or (not user_delay) or (int(user_delay)<7):
        delay = '7'
    else: delay = user_delay
    if bool(selected):
        location = 'dial'
        autodial = 'checked'
    os.system('open /Users/gabepersaud/Local\ Documents/server/hangup.app')
    
    html = '<!doctype html><html><head><meta charset="UTF-8"><title>Dispositioning Call</title><meta name="apple-mobile-web-app-capable" content="yes" /><style type="text/css">body,td,th {	color: #D9D9D9;	font-family: Gotham, "Helvetica Neue", Helvetica, Arial, sans-serif;	font-weight: bolder;}.big {	font-size: 164px;	}	.small {	font-size:48px;	}	body {	background-color: #4B4B4B;}</style></head><body><center>  <p>      <script>var timer = setTimeout(function() {{window.location="/'+location+'?autodial='+autodial+'&delay='+user_delay+'"}}, '+delay+'000);</script>      <br>      </p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p><span class="small">Next lead in...</span><br></p>    <p class="big"><span id="counter">'+delay+'</span></p><script type="text/javascript">function countdown() {    var i = document.getElementById("counter");    if (parseInt(i.innerHTML)!=0) {    i.innerHTML = parseInt(i.innerHTML)-1;}}setInterval(function(){ countdown(); },1000);	</script></center></body></html>'
    return html

@app.route('/noanswer', methods=['POST'])
def noanswer():
    location = 'picture'
    autodial = ''
    selected = request.form.get('autodial')
    user_delay = request.form.get('delay').strip("'[]")
    if (str(user_delay)=='None') or (not user_delay) or (int(user_delay)<6):
        delay = '6'
    else: delay = user_delay
    if bool(selected):
        location = 'dial'
        autodial = 'checked'
    os.system('open /Users/gabepersaud/Local\ Documents/server/noanswer.app')
    
    html = '<!doctype html><html><head><meta charset="UTF-8"><title>Dispositioning Call</title><meta name="apple-mobile-web-app-capable" content="yes" /><style type="text/css">body,td,th {	color: #D9D9D9;	font-family: Gotham, "Helvetica Neue", Helvetica, Arial, sans-serif;	font-weight: bolder;}.big {	font-size: 164px;	}	.small {	font-size:48px;	}	body {	background-color: #4B4B4B;}</style></head><body><center>  <p>      <script>var timer = setTimeout(function() {{window.location="/'+location+'?autodial='+autodial+'&delay='+user_delay+'"}}, '+delay+'000);</script>      <br>      </p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p><span class="small">Next lead in...</span><br></p>    <p class="big"><span id="counter">'+delay+'</span></p><script type="text/javascript">function countdown() {    var i = document.getElementById("counter");    if (parseInt(i.innerHTML)!=0) {    i.innerHTML = parseInt(i.innerHTML)-1;}}setInterval(function(){ countdown(); },1000);	</script></center></body></html>'
    return html

@app.route('/refusal', methods=['POST'])
def refusal():
    location = 'picture'
    autodial = ''
    selected = request.form.get('autodial')
    user_delay = request.form.get('delay').strip("'[]")
    if (str(user_delay)=='None') or (not user_delay) or (int(user_delay)<12):
        delay = '12'
    else: delay = user_delay
    if bool(selected):
        location = 'dial'
        autodial = 'checked'
    os.system('open /Users/gabepersaud/Local\ Documents/server/rpcrefusal.app')
    html = '<!doctype html><html><head><meta charset="UTF-8"><title>Dispositioning Call</title><meta name="apple-mobile-web-app-capable" content="yes" /><style type="text/css">body,td,th {	color: #D9D9D9;	font-family: Gotham, "Helvetica Neue", Helvetica, Arial, sans-serif;	font-weight: bolder;}.big {	font-size: 164px;	}	.small {	font-size:48px;	}	body {	background-color: #4B4B4B;}</style></head><body><center>  <p>      <script>var timer = setTimeout(function() {{window.location="/'+location+'?autodial='+autodial+'&delay='+user_delay+'"}}, '+delay+'000);</script>      <br>      </p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p><span class="small">Next lead in...</span><br></p>    <p class="big"><span id="counter">'+delay+'</span></p><script type="text/javascript">function countdown() {    var i = document.getElementById("counter");    if (parseInt(i.innerHTML)!=0) {    i.innerHTML = parseInt(i.innerHTML)-1;}}setInterval(function(){ countdown(); },1000);	</script></center></body></html>'
    return html

@app.route('/donotcall', methods=['POST'])
def donotcall():
    location = 'picture'
    autodial = ''
    selected = request.form.get('autodial')
    user_delay = request.form.get('delay').strip("'[]")
    if (str(user_delay)=='None') or (not user_delay) or (int(user_delay)<7):
        delay = '7'
    else: delay = user_delay
    if bool(selected):
        location = 'dial'
        autodial = 'checked'
    os.system('open /Users/gabepersaud/Local\ Documents/server/donotcall.app')
    
    html = '<!doctype html><html><head><meta charset="UTF-8"><title>Dispositioning Call</title><meta name="apple-mobile-web-app-capable" content="yes" /><style type="text/css">body,td,th {	color: #D9D9D9;	font-family: Gotham, "Helvetica Neue", Helvetica, Arial, sans-serif;	font-weight: bolder;}.big {	font-size: 164px;	}	.small {	font-size:48px;	}	body {	background-color: #4B4B4B;}</style></head><body><center>  <p>      <script>var timer = setTimeout(function() {{window.location="/'+location+'?autodial='+autodial+'&delay='+user_delay+'"}}, '+delay+'000);</script>      <br>      </p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p><span class="small">Next lead in...</span><br></p>    <p class="big"><span id="counter">'+delay+'</span></p><script type="text/javascript">function countdown() {    var i = document.getElementById("counter");    if (parseInt(i.innerHTML)!=0) {    i.innerHTML = parseInt(i.innerHTML)-1;}}setInterval(function(){ countdown(); },1000);	</script></center></body></html>'
    return html

@app.route('/languagebarrier', methods=['POST'])
def languagebarrier():
    location = 'picture'
    autodial = ''
    selected = request.form.get('autodial')
    user_delay = request.form.get('delay').strip("'[]")
    if (str(user_delay)=='None') or (not user_delay) or (int(user_delay)<8):
        delay = '8'
    else: delay = user_delay
    if bool(selected):
        location = 'dial'
        autodial = 'checked'
    os.system('open /Users/gabepersaud/Local\ Documents/server/language.app')
    
    html = '<!doctype html><html><head><meta charset="UTF-8"><title>Dispositioning Call</title><meta name="apple-mobile-web-app-capable" content="yes" /><style type="text/css">body,td,th {	color: #D9D9D9;	font-family: Gotham, "Helvetica Neue", Helvetica, Arial, sans-serif;	font-weight: bolder;}.big {	font-size: 164px;	}	.small {	font-size:48px;	}	body {	background-color: #4B4B4B;}</style></head><body><center>  <p>      <script>var timer = setTimeout(function() {{window.location="/'+location+'?autodial='+autodial+'&delay='+user_delay+'"}}, '+delay+'000);</script>      <br>      </p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p><span class="small">Next lead in...</span><br></p>    <p class="big"><span id="counter">'+delay+'</span></p><script type="text/javascript">function countdown() {    var i = document.getElementById("counter");    if (parseInt(i.innerHTML)!=0) {    i.innerHTML = parseInt(i.innerHTML)-1;}}setInterval(function(){ countdown(); },1000);	</script></center></body></html>'
    return html

@app.route('/scccomerror', methods=['POST'])
def scccom():
    autodial = ''
    selected = request.form.get('autodial')
    delay = request.form.get('delay')
    user_delay = str(delay).strip("'[]")
    if bool(selected):
        autodial = 'checked'
    os.system('open /Users/gabepersaud/Local\ Documents/server/scccom.app')
    html = '<!doctype html><html><head><meta charset="UTF-8"><title>Dispositioning Call</title><meta name="apple-mobile-web-app-capable" content="yes" /><style type="text/css">body,td,th {	color: #D9D9D9;	font-family: Gotham, "Helvetica Neue", Helvetica, Arial, sans-serif;	font-weight: bolder;}.big {	font-size: 164px;	}	.small {	font-size:48px;	}	body {	background-color: #4B4B4B;}</style></head><body><center>  <p>      <script>var timer = setTimeout(function() {{window.location="/home?autodial='+autodial+'&delay='+user_delay+'"}}, 2000);</script>      <br>      </p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p><span class="small">Getting info...</span><br></p>    <p class="big"><span id="counter">2</span></p><script type="text/javascript">function countdown() {    var i = document.getElementById("counter");    if (parseInt(i.innerHTML)!=0) {    i.innerHTML = parseInt(i.innerHTML)-1;}}setInterval(function(){ countdown(); },1000);	</script></center></body></html>'
    return html

@app.route('/picture', methods=['POST', 'GET'])
def picture():
    autodial = ''
    selected = request.form.get('autodial')
    delay = request.form.get('delay')
    user_delay = str(delay).strip("'[]")
    if delay is None:
        autodial = request.args.get('autodial')
        user_delay = request.args.get('delay')
    if bool(selected):
        autodial = 'checked'

    os.system('open /Applications/Anydesk.app; sleep .5')
    os.system('open /Users/gabepersaud/Local\ Documents/server/custinfo.app')
    html = '<!doctype html><html><head><meta charset="UTF-8"><title>Dispositioning Call</title><meta name="apple-mobile-web-app-capable" content="yes" /><style type="text/css">body,td,th {	color: #D9D9D9;	font-family: Gotham, "Helvetica Neue", Helvetica, Arial, sans-serif;	font-weight: bolder;}.big {	font-size: 164px;	}	.small {	font-size:48px;	}	body {	background-color: #4B4B4B;}</style></head><body><center>  <p>      <script>var timer = setTimeout(function() {{window.location="/home?autodial='+autodial+'&delay='+user_delay+'"}}, 2000);</script>      <br>      </p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p>&nbsp;</p>  <p><span class="small">Next lead in...</span><br></p>    <p class="big"><span id="counter">2</span></p><script type="text/javascript">function countdown() {    var i = document.getElementById("counter");    if (parseInt(i.innerHTML)!=0) {    i.innerHTML = parseInt(i.innerHTML)-1;}}setInterval(function(){ countdown(); },1000);	</script></center></body></html>'
    return html

if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0', ssl_context=('./static/cert.pem', './static/key.pem'))
