-- Landrop.app — 双击启动：确保后台服务在跑，然后弹出独立客户端窗口
-- 逻辑：服务活着 → 直接开窗口；服务没跑 → 先拉起再开窗口
set serverUp to false
try
	do shell script "curl -s -m 2 http://127.0.0.1:8989/api/info >/dev/null"
	set serverUp to true
end try

if not serverUp then
	do shell script "nohup python3 $HOME/Desktop/PersonalProject/landrop/server.py >> /tmp/landrop.log 2>&1 &"
	delay 1.2
end if

-- Chrome 应用模式 = 无地址栏独立窗口，观感就是原生客户端
try
	do shell script "test -d '/Applications/Google Chrome.app' && open -na 'Google Chrome' --args --app=http://127.0.0.1:8989"
on error
	open location "http://127.0.0.1:8989"
end try
