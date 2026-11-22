# Landrop · 局域网快传

单文件、零依赖的局域网互传工具：同一 Wi-Fi 下，手机/电脑打开一个网址即可互传文件与文字。截图、文档、视频，拖进来就到对面设备。

## 快速开始

```bash
python3 server.py        # 纯 Python 标准库，无需 pip install
# 终端会打印访问地址，例如：
#   ➜  http://192.168.1.4:8989
```

手机浏览器打开该地址（或扫页面上的二维码）→ 拖文件上传 → 文件出现在电脑 `~/Downloads/LanDrop/`。反向传：电脑在页面里上传，手机点列表下载。

## 特性

- **单文件零依赖**：`server.py` 一个文件跑通一切，Python 3.7+ 全平台通用
- **全端可用**：手机 / 电脑 / 平板，浏览器即客户端
- **文件 + 文字**：支持传文件，也支持互发文本/链接（自动存为 txt）
- **重名不覆盖**：自动加 `(1)`、`(2)` 后缀
- **端口自适应**：8989 被占自动换 8990+ 往后找
- **文件名清洗**：自动去除 Windows 非法字符（`: * ? " < > |`）与保留名（CON 等），三平台落盘无忧
- **网页即管理台**：文件列表 4 秒自动刷新，支持预览（图片/PDF/音视频）与在线删除

## 各平台启动壳

`Landrop-CrossPlatform/` 目录提供三平台"双击即用"的启动器与开机自启配置：

| 平台 | 双击客户端 | 开机自启 |
|---|---|---|
| macOS | `macOS/install-app.command` | `macOS/setup-autostart.command` |
| Windows | `Windows/start.bat` + `create-window-shortcut.bat` | `Windows/setup-autostart.bat` |
| Linux | `Linux/create-window-launcher.sh` | `Linux/setup-autostart.sh` |

详见 [Landrop-CrossPlatform/README.md](Landrop-CrossPlatform/README.md)。

## 文件存储

默认 `~/Downloads/LanDrop`（Windows：`C:\Users\你\Downloads\LanDrop`），普通文件原样落盘。指定其他目录：`python3 server.py /你的目录`。

> 注意：网页中的删除按钮直接删除文件、不进回收站。

## macOS 桌面客户端

`Landrop.applescript` 为生成源码：`osacompile -o Landrop.app Landrop.applescript` 编译后，双击 Landrop.app = 自动拉起后台服务 + 弹出 Chrome 应用模式独立窗口（无地址栏、无标签页）。

## 安全边界

本工具面向**可信局域网**（家庭/个人 Wi-Fi）设计，无鉴权机制——不要在公共 Wi-Fi 或不可信网络中长期运行。
