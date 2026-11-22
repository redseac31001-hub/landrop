#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Landrop — 局域网快传（纯 Python 标准库，零依赖）

用法:
    python3 server.py [存储目录]
环境变量:
    LANDROP_PORT  监听端口，默认 8989（被占用时自动 +1 往后找）
"""
import json
import mimetypes
import os
import re
import socket
import sys
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("LANDROP_PORT", "8989"))
STORE = os.path.abspath(os.path.expanduser(
    sys.argv[1] if len(sys.argv) > 1
    else os.path.join(os.path.expanduser("~"), "Downloads", "LanDrop")))
os.makedirs(STORE, exist_ok=True)

IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg", ".ico"}
INLINE_EXT = IMG_EXT | {".pdf", ".txt", ".md", ".mp4", ".mp3", ".mov", ".json", ".csv", ".log"}


def lan_ips():
    """返回本机所有候选局域网 IPv4，第一个是默认路由出口 IP。"""
    ips = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        s.connect(("8.8.8.8", 80))
        ips.append(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = info[4][0]
            if not ip.startswith("127.") and ip not in ips:
                ips.append(ip)
    except Exception:
        pass
    return ips


_WIN_RESERVED = {"con", "prn", "aux", "nul",
                 *(f"com{i}" for i in range(1, 10)),
                 *(f"lpt{i}" for i in range(1, 10))}


def safe_name(name):
    name = os.path.basename(str(name).replace("\\", "/")).strip().lstrip(".")
    name = re.sub(r'[<>:"|?*\x00-\x1f/]', "", name).rstrip(". ")
    if name.split(".")[0].lower() in _WIN_RESERVED:  # Windows 保留名（CON.txt 等）
        name = "landrop_" + name
    return (name or "unnamed")[:150]


def unique_path(name):
    base, ext = os.path.splitext(name)
    p = os.path.join(STORE, name)
    i = 1
    while os.path.exists(p):
        p = os.path.join(STORE, "%s (%d)%s" % (base, i, ext))
        i += 1
    return p


def human(n):
    n = float(n)
    for u in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or u == "TB":
            return ("%d %s" % (n, u)) if u == "B" else ("%.1f %s" % (n, u))
        n /= 1024


PAGE = r"""<!doctype html>
<html lang="zh"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Landrop · 局域网快传</title>
<style>
:root{--bg:#10141c;--card:#1a212e;--line:#2a3446;--tx:#e8edf5;--dim:#8a97ab;--ac:#4f8cff;--ok:#3ecf8e}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--tx);font:15px/1.5 -apple-system,"PingFang SC","Segoe UI",sans-serif;padding:24px 16px 60px}
.wrap{max-width:760px;margin:0 auto}
h1{font-size:26px;margin-bottom:4px}
.sub{color:var(--dim);margin-bottom:18px}
.urls{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;margin-bottom:18px}
.urow{display:flex;align-items:center;gap:8px;margin:4px 0}
.urow code{flex:1;font-size:15px;color:var(--ac);word-break:break-all}
.chip{font-size:12px;color:var(--dim);border:1px solid var(--line);border-radius:99px;padding:1px 8px}
button{background:var(--ac);color:#fff;border:0;border-radius:8px;padding:6px 14px;font-size:14px;cursor:pointer}
button.ghost{background:transparent;border:1px solid var(--line);color:var(--dim)}
#qr{margin-top:10px;background:#fff;padding:8px;border-radius:8px;width:max-content}
#drop{border:2px dashed var(--line);border-radius:14px;padding:42px 20px;text-align:center;color:var(--dim);cursor:pointer;transition:.15s;margin-bottom:16px}
#drop.on{border-color:var(--ac);color:var(--ac);background:rgba(79,140,255,.08)}
.row{display:flex;gap:8px;margin-bottom:16px}
textarea{flex:1;background:var(--card);border:1px solid var(--line);border-radius:10px;color:var(--tx);padding:10px;min-height:64px;resize:vertical;font:inherit}
#prog .pbar{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 10px;margin-bottom:6px;font-size:13px}
#prog .bar{height:5px;background:var(--line);border-radius:3px;margin-top:5px;overflow:hidden}
#prog .bar i{display:block;height:100%;width:0;background:var(--ok);transition:.15s}
h2{font-size:16px;margin:22px 0 10px;display:flex;align-items:center;justify-content:space-between}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}
th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);font-size:14px}
th{color:var(--dim);font-weight:500;font-size:12px}
tr:last-child td{border-bottom:0}
td a{color:var(--tx);text-decoration:none;word-break:break-all}
td a:hover{color:var(--ac)}
td .m{color:var(--dim);font-size:12px;white-space:nowrap}
td .del{background:none;border:none;color:#ff6b6b;padding:2px 6px;font-size:16px}
.empty{color:var(--dim);text-align:center;padding:24px}
</style></head><body>
<div class="wrap">
  <h1>📮 Landrop</h1>
  <div class="sub">同一 Wi-Fi / 局域网内，任何设备打开这个网址即可互传文件</div>
  <div class="urls">
    <div id="urlrows"></div>
    <div id="qr"></div>
  </div>
  <div id="drop">📤 拖拽文件到这里 &nbsp;·&nbsp; 点击选择 &nbsp;·&nbsp; 或直接 ⌘V / 长按粘贴截图</div>
  <input type="file" id="file" multiple hidden>
  <div class="row">
    <textarea id="txt" placeholder="也可以发一段文字 / 链接给局域网里的其他设备…"></textarea>
    <button id="sendtxt">发送文本</button>
  </div>
  <div id="prog"></div>
  <h2>📂 共享文件 <button class="ghost" id="rf">刷新</button></h2>
  <table><thead><tr><th>文件</th><th>大小</th><th>时间</th><th></th></tr></thead><tbody id="rows"></tbody></table>
</div>
<script src="https://cdn.jsdelivr.net/gh/davidshimjs/qrcodejs/qrcode.min.js"></script>
<script>
var IPS=__IPS_JSON__, PORT=__PORT__;
function esc(s){return String(s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function human(n){n=+n;var u=['B','KB','MB','GB','TB'],i=0;while(n>=1024&&i<4){n/=1024;i++}return (i?n.toFixed(1):n)+' '+u[i]}
var rows=document.getElementById('urlrows'), primary=IPS[0]?('http://'+IPS[0]+':'+PORT):location.origin;
IPS.forEach(function(ip,i){
  var d=document.createElement('div');d.className='urow';
  d.innerHTML='<code>http://'+esc(ip)+':'+PORT+'</code>'+(i?'<span class="chip">备用</span>':'<span class="chip">本机</span>');
  var b=document.createElement('button');b.className='ghost';b.textContent='复制';
  b.onclick=function(){navigator.clipboard.writeText('http://'+ip+':'+PORT);b.textContent='✓';setTimeout(function(){b.textContent='复制'},1200)};
  d.appendChild(b);rows.appendChild(d);
});
if(typeof QRCode!=='undefined'&&IPS[0]){try{new QRCode(document.getElementById('qr'),{text:primary,width:120,height:120})}catch(e){}}
var drop=document.getElementById('drop'),fileI=document.getElementById('file');
drop.onclick=function(){fileI.click()};
fileI.onchange=function(){upAll(fileI.files);fileI.value=''};
document.addEventListener('dragover',function(e){e.preventDefault();drop.classList.add('on')});
document.addEventListener('dragleave',function(e){if(e.target===document)drop.classList.remove('on')});
document.addEventListener('drop',function(e){e.preventDefault();drop.classList.remove('on');upAll(e.dataTransfer.files)});
document.addEventListener('paste',function(e){if(e.clipboardData&&e.clipboardData.files.length){e.preventDefault();upAll(e.clipboardData.files)}});
function upAll(fs){for(var i=0;i<fs.length;i++)up(fs[i])}
function up(f){
  var box=document.createElement('div');box.className='pbar';
  box.innerHTML='<span>'+esc(f.name)+' 0%</span><div class="bar"><i></i></div>';
  document.getElementById('prog').appendChild(box);
  var lab=box.querySelector('span'),bar=box.querySelector('i');
  var t0=Date.now();
  function fmtS(s){return s>=60?Math.floor(s/60)+'分'+Math.round(s%60)+'秒':Math.max(1,Math.round(s))+'秒'}
  var xhr=new XMLHttpRequest();
  xhr.open('POST','/upload?name='+encodeURIComponent(f.name));
  xhr.setRequestHeader('X-Filename',encodeURIComponent(f.name));
  xhr.upload.onprogress=function(e){
    if(!e.lengthComputable)return;
    var p=Math.round(e.loaded/e.total*100);
    bar.style.width=p+'%';
    var el=(Date.now()-t0)/1000, sp=e.loaded/Math.max(el,0.2);
    lab.textContent=esc(f.name)+' '+p+'% · '+(sp/1048576).toFixed(1)+' MB/s'+
      (p<100?' · 剩余 '+fmtS((e.total-e.loaded)/Math.max(sp,1)):' · 用时 '+fmtS(el));
  };
  xhr.onload=function(){setTimeout(function(){box.remove();refresh()},400)};
  xhr.onerror=function(){lab.textContent=esc(f.name)+' ❌ 上传失败'};
  xhr.send(f);
}
document.getElementById('sendtxt').onclick=function(){
  var v=document.getElementById('txt').value.trim();if(!v)return;
  fetch('/api/text',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:v})})
    .then(function(){document.getElementById('txt').value='';refresh()});
};
document.getElementById('rf').onclick=refresh;
function refresh(){
  fetch('/api/list').then(function(r){return r.json()}).then(function(list){
    var tb=document.getElementById('rows');tb.innerHTML='';
    if(!list.length){tb.innerHTML='<tr><td colspan="4" class="empty">还没有文件，传一个试试</td></tr>';return}
    list.forEach(function(f){
      var tr=document.createElement('tr');
      var a=document.createElement('a');a.href='/files/'+encodeURIComponent(f.name);a.textContent=f.name;
      if(new RegExp('\\.(png|jpe?g|gif|webp|bmp|svg|ico|pdf|mp4|mp3|mov)$','i').test(f.name))a.target='_blank';
      var td1=document.createElement('td');td1.appendChild(a);
      var td2=document.createElement('td');td2.className='m';td2.textContent=human(f.size);
      var td3=document.createElement('td');td3.className='m';td3.textContent=new Date(f.mtime*1000).toLocaleString();
      var td4=document.createElement('td');td4.className='m';
      var del=document.createElement('button');del.className='del';del.textContent='✕';del.title='删除';
      del.onclick=function(){if(confirm('删除 '+f.name+' ?')){fetch('/api/delete?name='+encodeURIComponent(f.name),{method:'POST'}).then(refresh)}};
      td4.appendChild(del);
      tr.appendChild(td1);tr.appendChild(td2);tr.appendChild(td3);tr.appendChild(td4);tb.appendChild(tr);
    });
  });
}
refresh();setInterval(refresh,4000);
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    server_version = "Landrop/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (time.strftime("%H:%M:%S"), fmt % args))

    def send_json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def redirect(self, loc):
        self.send_response(302)
        self.send_header("Location", loc)
        self.send_header("Content-Length", "0")
        self.end_headers()

    # ---------- GET ----------
    def do_GET(self):
        path = urllib.parse.urlsplit(self.path)
        route = path.path
        if route == "/" or route == "/index.html":
            b = PAGE.replace("__IPS_JSON__", json.dumps(lan_ips())) \
                    .replace("__PORT__", str(PORT)).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)
        elif route == "/api/info":
            self.send_json({"ips": lan_ips(), "port": PORT, "store": STORE})
        elif route == "/api/list":
            items = []
            try:
                for n in os.listdir(STORE):
                    p = os.path.join(STORE, n)
                    if os.path.isfile(p):
                        st = os.stat(p)
                        items.append({"name": n, "size": st.st_size, "mtime": st.st_mtime})
            except OSError:
                pass
            items.sort(key=lambda x: -x["mtime"])
            self.send_json(items)
        elif route.startswith("/files/"):
            name = safe_name(urllib.parse.unquote(route[len("/files/"):]))
            p = os.path.join(STORE, name)
            if not os.path.isfile(p):
                self.send_json({"error": "not found: %s" % name}, 404)
                return
            size = os.path.getsize(p)
            ext = os.path.splitext(name)[1].lower()
            ctype = mimetypes.guess_type(name)[0] or "application/octet-stream"
            disp = "inline" if ext in INLINE_EXT else "attachment"
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(size))
            self.send_header("Content-Disposition",
                             "%s; filename*=UTF-8''%s" % (disp, urllib.parse.quote(name)))
            self.end_headers()
            with open(p, "rb") as f:
                while True:
                    c = f.read(1 << 20)
                    if not c:
                        break
                    self.wfile.write(c)
        elif route == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
        else:
            self.redirect("/")

    # ---------- POST ----------
    def do_POST(self):
        path = urllib.parse.urlsplit(self.path)
        route = path.path
        q = urllib.parse.parse_qs(path.query)
        if route == "/upload":
            name = self.headers.get("X-Filename") or (q.get("name") or [""])[0]
            name = safe_name(urllib.parse.unquote(name))
            n = int(self.headers.get("Content-Length") or 0)
            p = unique_path(name)
            got = 0
            try:
                with open(p, "wb") as f:
                    while got < n:
                        c = self.rfile.read(min(1 << 20, n - got))
                        if not c:
                            break
                        f.write(c)
                        got += len(c)
            except OSError as e:
                self.send_json({"error": str(e)}, 500)
                return
            self.send_json({"ok": True, "name": os.path.basename(p), "size": got})
        elif route == "/api/text":
            body = self.read_body()
            try:
                text = json.loads(body.decode("utf-8")).get("text", "").rstrip()
            except Exception:
                text = body.decode("utf-8", "replace").rstrip()
            if text:
                fn = time.strftime("文本_%Y%m%d_%H%M%S") + ".txt"
                with open(unique_path(fn), "w", encoding="utf-8") as f:
                    f.write(text + "\n")
            self.send_json({"ok": True})
        elif route == "/api/delete":
            name = safe_name(urllib.parse.unquote((q.get("name") or [""])[0]))
            p = os.path.join(STORE, name)
            try:
                os.remove(p)
                self.send_json({"ok": True})
            except OSError as e:
                self.send_json({"error": str(e)}, 404)
        else:
            self.send_json({"error": "unknown route"}, 404)

    def read_body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return self.rfile.read(n) if n else b""

    do_DELETE = do_POST  # 兼容 DELETE 方法走同一逻辑


def main():
    global PORT
    srv = None
    for p in range(PORT, PORT + 25):
        try:
            srv = ThreadingHTTPServer(("0.0.0.0", p), Handler)
            PORT = p
            break
        except OSError:
            continue
    if srv is None:
        raise SystemExit("8989~9013 全被占用")
    print("Landrop 已启动，共享目录: %s" % STORE, flush=True)
    for ip in lan_ips():
        print("  ➜  http://%s:%d" % (ip, PORT), flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
