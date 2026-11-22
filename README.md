<p align="center"><img src="assets/icon.png" width="140" alt="Landrop 图标"></p>

<h1 align="center">Landrop · 局域网快传</h1>

<p align="center">同一 Wi-Fi 下，手机 / 电脑打开一个网址，互传文件与文字</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-3776AB?logo=python&logoColor=white" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/依赖-零安装-3ECF8E" alt="零依赖">
  <img src="https://img.shields.io/badge/核心-单文件-4F8CFF" alt="单文件">
  <img src="https://img.shields.io/badge/平台-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey" alt="平台">
</p>

---

## 这是什么

一个**单文件、零依赖**的局域网互传工具：`server.py` 用纯 Python 标准库跑一个 HTTP 服务，任何设备（手机/平板/电脑）浏览器打开即用。 AirDrop 只属于苹果生态，Landrop 是给**整个局域网**的快传——传截图、文档、视频、安装包，也支持互发文本和链接。

```bash
python3 server.py        # 无需 pip install，Python 3.7+ 直接跑
# ➜  http://192.168.1.4:8989     （终端会打印实际地址）
```

手机打开该地址（或扫页面二维码）→ 拖文件上传 → 文件即刻出现在电脑上。反向同理：电脑上传，手机点列表下载。

## 特性

**传得快**
- 局域网直连，不受网速/云盘限制，大文件流式落盘（1MB 分块，内存占用恒定，传 2GB 视频也不吃内存）
- 粘贴即传：截图 ⌘V 直接发到对面设备
- 传输进度实时显示（百分比 + 速度 + 剩余时间）

**用得省心**
- 重名文件自动加 `(1)` `(2)` 后缀，永不覆盖
- 文件名自动清洗 Windows 非法字符（`:` `*` `?` 等）与保留名（`CON` 等），三平台落盘无忧
- 端口 8989 被占用自动换 8990 往后找
- 文件列表 4 秒自动刷新；图片 / PDF / 音视频可在线预览

**管得清楚**
- 网页即管理台：列表、大小、时间、删除一目了然
- 传的文字自动存为 `文本_日期_时间.txt`，链接和验证码不再丢在聊天记录里
- 可选访问验证：设一个密钥，外人拿到网址也进不来（默认关闭）

## 各平台启动壳

核心 `server.py` 全平台通用；`Landrop-CrossPlatform/` 提供三平台"双击即用"的启动器：

| 平台 | 双击客户端 | 开机自启 | 说明 |
|---|---|---|---|
| macOS | `macOS/install-app.command` | `macOS/setup-autostart.command` | 生成桌面 Landrop.app（带图标），双击 = 拉起服务 + Chrome 独立窗口 |
| Windows | `Windows/start.bat` | `Windows/setup-autostart.bat` | 没装 Python 会给安装指引；可再生成 Chrome/Edge 应用模式快捷方式 |
| Linux / WSL / Termux | `Linux/create-window-launcher.sh` | `Linux/setup-autostart.sh` | 应用菜单入口 + systemd 用户级自启 |

详见 [Landrop-CrossPlatform/README.md](Landrop-CrossPlatform/README.md)。

## 文件存在哪

默认 `~/Downloads/LanDrop`（Windows：`C:\Users\你\Downloads\LanDrop`），普通文件原样落盘，服务重启不丢失。指定其他目录：

```bash
python3 server.py /你的目录
```

> ⚠️ 网页中的 ✕ 删除按钮直接删除文件、**不进回收站**。

## 常见问题

**手机连不上？**
确认设备和电脑在同一 Wi-Fi；首次启动弹出防火墙提示要点"允许"；用页面顶部列出的局域网地址（不是 127.0.0.1）。

**页面上二维码不显示？**
二维码脚本来自 CDN，纯内网断网环境加载不到——不影响传输，直接手输网址即可。

**8989 打不开？**
端口被占会自动换 8990、8991…以启动日志或页面顶部显示的为准。

**传的文件会占内存吗？**
只占磁盘。传输时以 1MB 块流式写盘，服务进程常驻内存约 8MB，与文件大小无关。

**安全吗？**
面向**可信局域网**（家庭 / 个人 Wi-Fi）设计。担心同网其他人顺手围观/误删？一行开启访问验证：

```bash
LANDROP_KEY=你的密钥 python3 server.py    # 或把密钥写进 ~/.landrop_key 文件（对双击客户端同样生效）
```

开启后所有设备首次访问需输入密钥，登录态保持 30 天；网页右上角出现"退出"按钮。默认**不开启**，家人日常使用零摩擦。

**也可以直接在网页里配**：在本机（跑服务的这台电脑）打开 `http://127.0.0.1:8989`，右上角有"⚙ 设置"入口（局域网其他设备看不到），可开启 / 修改 / 关闭验证——忘了密钥也在这里重置。

> 说明：局域网 HTTP 为明文传输，此验证挡的是"拿到网址的顺手访问者"，不防蓄意抓包的攻击者；后者需 HTTPS（暂未引入以保持零依赖）。

## 目录结构

```
landrop/
├── server.py                    # 核心服务（单文件，全平台）
├── start.sh / stop.sh           # macOS/Linux 启停脚本
├── Landrop.applescript          # macOS 双击客户端源码
├── assets/                      # 项目图标（png 全尺寸 + svg 矢量）
├── tools/
│   └── make_icons.py            # 图标生成脚本（Pillow，可复现）
└── Landrop-CrossPlatform/       # 三平台启动包（详见其 README）
    ├── assets/landrop.icns      # macOS .icns（供 install-app.command 打进客户端）
    ├── macOS/  Windows/  Linux/
    └── start.sh / stop.sh
```

## 图标

`assets/` 内含全尺寸 PNG（1024→64）与 SVG 矢量版；macOS `.icns` 在 `Landrop-CrossPlatform/assets/landrop.icns`。修改设计后运行 `python3 tools/make_icons.py` 重新生成 PNG，`Landrop-CrossPlatform/macOS/install-app.command` 会自动把新图标打进桌面客户端。

## License

尚未指定——公开使用前建议补一份（如 MIT）。
