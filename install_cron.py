#!/usr/bin/env python3
"""安装每日自动任务"""
import os
import plistlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLIST_PATH = os.path.expanduser("~/Library/LaunchAgents/com.aizhibian.daily.plist")
RUN_SCRIPT = os.path.join(BASE_DIR, "run.py")
LOG_DIR = os.path.expanduser("~/Library/Logs/aizhibian")

AUTO_SCRIPT = os.path.join(BASE_DIR, "auto_daily.sh")

def install():
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Create auto script that generates + pushes to GitHub
    with open(AUTO_SCRIPT, "w") as f:
        f.write(f"""#!/bin/bash
cd {BASE_DIR}
/usr/bin/python3 {RUN_SCRIPT} full 2>>{LOG_DIR}/build.err
cd {BASE_DIR}
git add -A 2>>{LOG_DIR}/git.err
git commit -m "auto: daily content update $(date +%Y-%m-%d)" 2>>{LOG_DIR}/git.err
git push origin main 2>>{LOG_DIR}/git.err
""")
    os.chmod(AUTO_SCRIPT, 0o755)

    plist = {
        "Label": "com.aizhibian.daily",
        "ProgramArguments": ["/bin/bash", AUTO_SCRIPT],
        "WorkingDirectory": BASE_DIR,
        "StandardOutPath": os.path.join(LOG_DIR, "daily.log"),
        "StandardErrorPath": os.path.join(LOG_DIR, "daily.err"),
        "StartCalendarInterval": {"Hour": 6, "Minute": 0},
        "RunAtLoad": False,
        "KeepAlive": False,
        "EnvironmentVariables": {"PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"},
    }

    with open(PLIST_PATH, "wb") as f:
        plistlib.dump(plist, f)

    os.system(f"launchctl unload {PLIST_PATH} 2>/dev/null")
    os.system(f"launchctl load {PLIST_PATH}")

    log_path = os.path.join(LOG_DIR, "daily.log")
    print(f"✅ 每日自动任务已安装！")
    print(f"   时间：每天早上6:00")
    print(f"   内容：自动生成文章 + 构建网站 + 推送到GitHub")
    print(f"   日志：{log_path}")
    print(f"\n📌 查看日志: cat {log_path}")
    print(f"📌 手动触发: bash {AUTO_SCRIPT}")
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
