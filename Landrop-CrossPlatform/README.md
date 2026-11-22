# Landrop 跨平台包 · 局域网快传

核心就是 `server.py` 一个文件（纯 Python 标准库，零依赖、零编译），任何装了 **Python 3.7+** 的机器都能当服务端。其余文件都是各平台的"启动壳"，让双击就能用。

## 30 秒上手

| 系统 | 做法 |
|---|---|
| **macOS** | 双击 `macOS/install-app.command` → 桌面生成 Landrop.app，以后双击它 |
| **Windows** | 双击 `Windows/start.bat`（没装 Python 会给安装指引） |
| **Linux / WSL / Termux** | 终端执行 `bash start.sh` |

启动后：本机访问 http://127.0.0.1:8989 ；同一 Wi-Fi 下的手机/其他电脑访问页面顶部列出的 `http://局域网IP:8989`。

## 文件一览

| 文件 | 平台 | 用途 |
|---|---|---|
| `server.py` | 全平台 | 核心服务，单文件，无需安装任何库 |
| `start.sh` / `stop.sh` | macOS / Linux / WSL / Termux | 启动 / 停止后台服务 |
| `macOS/install-app.command` | macOS | 生成桌面双击客户端（Chrome 独立窗口） |
| `macOS/setup-autostart.command` | macOS | 开机自启（launchd）；卸载：终端执行 `...command remove` |
| `Windows/start.bat` | Windows | 双击启动服务并打开页面 |
| `Windows/stop.bat` | Windows | 停止服务 |
| `Windows/create-window-shortcut.bat` | Windows | 桌面生成 Landrop 独立窗口快捷方式（Chrome/Edge 应用模式） |
| `Windows/setup-autostart.bat` | Windows | 开机自启；`remove-autostart.bat` 卸载 |
| `Linux/create-window-launcher.sh` | Linux | 应用菜单生成 Landrop 入口（Chrome 应用模式） |
| `Linux/setup-autostart.sh` | Linux | 开机自启（systemd --user）；卸载：`...sh remove` |

## 传的文件存在哪

默认 `~/Downloads/LanDrop`（Windows：`C:\Users\你\Downloads\LanDrop`）。就是普通文件，原样落盘；重名自动加 `(1)` 不覆盖；网页里的 ✕ 删除是直接删、不进回收站。想换存储目录：`python3 server.py /你的目录`。

## 注意事项

- 首次启动防火墙弹窗 → 点"允许访问"，否则手机连不上
- 可选访问验证：启动前设置环境变量 `LANDROP_KEY=你的密钥`，或把密钥写进 `~/.landrop_key` 文件（对双击客户端、开机自启同样生效）；设置后所有设备需输密钥登录一次，30 天免重输
- Windows 未装 Python：安装时务必勾选 **Add Python to PATH**，装完重新双击
- 页面二维码靠 CDN 加载，纯内网断网环境不显示（不影响传文件）
- 端口 8989 被占用会自动换 8990 往后找
- 文件名里的 Windows 非法字符（`: * ? " < > |`）会自动清洗，三平台通用
- 双击 `.command` 被拦：终端执行 `xattr -dr com.apple.quarantine macOS/`
- Windows 拦截 bat：右键文件 → 属性 → 勾"解除锁定"
- 开机自启只在登录时拉起一次服务；平时手动 `start.sh` / `start.bat` 启停照常可用，两者不冲突
- Linux 无桌面/纯 SSH 长期挂机需执行一次：`loginctl enable-linger $USER`

## 迁移到新电脑

把整个文件夹拷过去（U盘 / 微信 / 用 Landrop 自己传都行），按上表对应系统双击或执行即可。已传的文件存在各机器本地，不随包迁移。
