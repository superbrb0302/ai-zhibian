#!/usr/bin/env python3
"""安装每日自动任务 - 用 launchd 定时生成内容"""
import os
import plistlib
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLIST_PATH = os.path.expanduser("~/Library/LaunchAgents/com.aizhibian.daily.plist")
SCRIPT_PATH = os.path.join(BASE_DIR, "run.py")
LOG_DIR = os.path.expanduser("~/Library/Logs/aizhibian")

def install():
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(LOG_DIR, "daily.log")
    err_file = os.path.join(LOG_DIR, "daily.err")

    plist = {
        "Label": "com.aizhibian.daily",
        "ProgramArguments": ["/usr/bin/python3", SCRIPT_PATH, "full"],
        "WorkingDirectory": BASE_DIR,
        "StandardOutPath": log_file,
        "StandardErrorPath": err_file,
        "StartCalendarInterval": {
            "Hour": 6,
            "Minute": 0,
        },
        "RunAtLoad": False,
        "KeepAlive": False,
    }

    with open(PLIST_PATH, "wb") as f:
        plistlib.dump(plist, f)

    os.system(f"launchctl load {PLIST_PATH}")
    print(f"✅ 每日自动任务已安装！")
    print(f"   时间：每天早上6:00")
    print(f"   内容：自动生成文章 + 构建网站")
    print(f"   日志：{log_dir}/daily.log")
    print(f"\n📌 查看日志: cat {log_dir}/daily.log")
    print(f"📌 卸载: launchctl unload {PLIST_PATH}")

def uninstall():
    if os.path.exists(PLIST_PATH):
        os.system(f"launchctl unload {PLIST_PATH}")
        os.remove(PLIST_PATH)
        print("✅ 已卸载每日自动任务")
    else:
        print("未安装任务")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        uninstall()
    else:
        install()
