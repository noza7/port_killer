# Windows Port Process Killer

A simple GUI tool for finding and killing processes using specific ports on Windows.

一个简单的图形界面工具，用于在Windows系统上查找和结束占用特定端口的进程。

## Features / 功能特点

- Clean GitHub-style interface / 简洁的GitHub风格界面
- Search for processes using specific ports / 查找占用特定端口的进程
- Kill processes with one click / 一键结束进程
- Display process information / 显示进程信息
- Admin privileges status display / 管理员权限状态显示
- English/Chinese language switch / 中英文切换
- Windows system optimized / Windows系统优化支持

## Requirements / 安装要求

- Windows 10/11
- Python 3.8+
- PyQt6
- psutil

## Installation / 安装步骤

1. Clone or download this repository / 克隆或下载此仓库
2. Install dependencies / 安装依赖：
```bash
pip install -r requirements.txt
```

## Usage / 使用方法

### Regular User Mode / 普通用户模式
1. Run the program / 运行程序：
```bash
python port_killer.py
```

### Administrator Mode (Recommended) / 管理员模式（推荐）
1. Right-click Command Prompt or PowerShell and select "Run as administrator" / 右键点击命令提示符或PowerShell，选择"以管理员身份运行"
2. Navigate to the program directory / 导航到程序目录
3. Run the program / 运行程序：
```bash
python port_killer.py
```

### Operation Steps / 使用步骤
1. Enter the port number (1-65535) in the input box / 在输入框中输入要查找的端口号（1-65535）
2. Click "Search" to find processes using the port / 点击"查找进程"查看占用该端口的进程
3. Click "Kill Process" to terminate the process / 点击"结束进程"来终止进程
4. Process information will be displayed in the text area / 进程信息会显示在文本区域

## Notes / 注意事项

- It's recommended to run the program as administrator for full functionality / 建议以管理员权限运行程序，以确保能够结束所有进程
- The program will display current administrator privileges status / 程序会显示当前是否具有管理员权限
- If you see "Access denied" error, try running the program as administrator / 如果看到"访问被拒绝"错误，请尝试以管理员身份重新运行程序
- Port number must be between 1-65535 / 端口号必须在1-65535范围内
- Some system processes may not be terminated due to security mechanisms / 某些系统进程可能无法被终止，这是正常的安全机制 