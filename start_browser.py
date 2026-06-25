"""Start Chrome and open all platform tabs"""
import subprocess, time, os, json, urllib.request

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE_DIR = "/tmp/chrome_persist_v2"

# Kill existing Chrome
subprocess.run(["pkill", "-9", "-f", "Google Chrome"], capture_output=True)
time.sleep(2)

# Launch Chrome
os.makedirs(PROFILE_DIR, exist_ok=True)
subprocess.Popen(
    [CHROME_PATH,
     f"--user-data-dir={PROFILE_DIR}",
     "--remote-debugging-port=9222",
     "--no-first-run", "--no-default-browser-check",
     "--window-size=1400,900",
     "--new-window", "https://www.zhihu.com"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

# Wait for CDP
for i in range(30):
    try:
        resp = urllib.request.urlopen("http://localhost:9222/json/version", timeout=2)
        data = json.loads(resp.read())
        print(f"✅ Chrome已启动: {data.get('Browser')}")
        break
    except:
        time.sleep(1)
else:
    print("❌ Chrome启动失败")
    exit(1)

# Open platform tabs via CDP HTTP API
import urllib.parse
platforms = [
    ("头条号", "https://mp.toutiao.com/"),
    ("百家号", "https://baijiahao.baidu.com/"),
    ("知乎", "https://www.zhihu.com/"),
    ("闲鱼", "https://www.goofish.com/"),
    ("小红书", "https://creator.xiaohongshu.com/"),
]

for name, url in platforms:
    try:
        req = urllib.request.Request(f"http://localhost:9222/json/new?{url}")
        urllib.request.urlopen(req, timeout=5)
        print(f"  ✅ {name}")
    except Exception as e:
        print(f"  ❌ {name}: {e}")

print("\n🎉 浏览器已打开！请登录所有平台后，运行:")
print("   python3 do_publish.py")
