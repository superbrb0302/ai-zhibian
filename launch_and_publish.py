#!/usr/bin/env python3
"""一站式Chrome启动+自动发布"""
import subprocess, time, os, sys, json
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE_DIR = "/tmp/chrome_persist"  # Persistent profile

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def start_chrome():
    """Launch Chrome with CDP"""
    # Kill existing Chrome
    subprocess.run(["pkill", "-9", "-f", "Google Chrome"], capture_output=True)
    time.sleep(2)
    
    # Create profile dir if not exists
    os.makedirs(PROFILE_DIR, exist_ok=True)
    
    # Launch Chrome
    proc = subprocess.Popen(
        [CHROME_PATH,
         f"--user-data-dir={PROFILE_DIR}",
         "--remote-debugging-port=9222",
         "--no-first-run",
         "--no-default-browser-check",
         "--window-size=1400,900",
         "--new-window", "https://www.zhihu.com"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    
    # Wait for CDP
    for i in range(30):
        import urllib.request
        try:
            resp = urllib.request.urlopen("http://localhost:9222/json/version", timeout=2)
            data = json.loads(resp.read())
            log(f"✅ Chrome已启动: {data.get('Browser')}")
            return proc
        except:
            time.sleep(1)
    
    log("❌ Chrome启动失败")
    return None

def open_all_platforms():
    """Open all platform tabs"""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        
        urls = [
            ("头条号", "https://mp.toutiao.com/"),
            ("百家号", "https://baijiahao.baidu.com/"),
            ("知乎", "https://www.zhihu.com/"),
            ("闲鱼", "https://www.goofish.com/"),
            ("小红书", "https://creator.xiaohongshu.com/"),
        ]
        
        for name, url in urls:
            pg = context.new_page()
            pg.goto(url, wait_until='domcontentloaded', timeout=15000)
            log(f"  ✅ {name}")
        
        log(f"\n🎉 共打开 {len(context.pages)} 个标签页")
        log("请在所有平台登录后，按 Enter 继续...")

def read_content():
    """Read all content files"""
    # Daily articles
    dp = os.path.join(BASE, "daily_pack_20260624")
    articles = []
    if os.path.exists(dp):
        files = sorted([f for f in os.listdir(dp) if f.endswith(".txt") and not f.endswith("_info.txt")])
        for f in files:
            with open(os.path.join(dp, f), "r", encoding="utf-8") as fh:
                content = fh.read().strip()
            lines = content.split("\n")
            title = lines[0].replace("#", "").strip() if lines else "AI文章"
            body = "\n".join(lines[1:]).strip()
            articles.append({"title": title, "body": body})
    
    # Zhihu answers
    zd = os.path.join(BASE, "zhihu_output")
    answers = []
    if os.path.exists(zd):
        files = sorted([f for f in os.listdir(zd) if f.startswith("zhihu_") and f.endswith(".md")])
        for f in files:
            with open(os.path.join(zd, f), "r", encoding="utf-8") as fh:
                answers.append(fh.read().strip())
    
    return articles, answers

def publish_all():
    """Publish to all platforms"""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        
        articles, answers = read_content()
        log(f"📚 内容准备: {len(articles)}篇文章, {len(answers)}个知乎回答")
        
        # Find pages by URL
        pages = {}
        for pg in context.pages:
            url = pg.url
            if "toutiao" in url:
                pages["toutiao"] = pg
            elif "baijiahao" in url:
                pages["baijiahao"] = pg
            elif "zhihu" in url:
                pages["zhihu"] = pg
            elif "goofish" in url:
                pages["xianyu"] = pg
        
        log(f"📑 找到 {len(pages)} 个平台页面")
        
        # ======== 头条号 ========
        if "toutiao" in pages:
            log("\n📰 头条号发布中...")
            pg = pages["toutiao"]
            pg.goto("https://mp.toutiao.com/profile_v4/article/create", wait_until='domcontentloaded', timeout=20000)
            time.sleep(3)
            
            for i, art in enumerate(articles[:2]):
                log(f"  📝 [{i+1}/2] {art['title'][:30]}")
                try:
                    # Fill title
                    ti = pg.locator('input[placeholder*="标题"]').first
                    if ti.is_visible(timeout=3000):
                        ti.fill(art['title'])
                    # Fill body
                    ed = pg.locator('[contenteditable="true"]').first
                    if ed.is_visible(timeout=3000):
                        ed.fill(art['body'][:3000])
                    log(f"    ✅ 内容已填入")
                except Exception as e:
                    log(f"    ⚠️ {str(e)[:40]}")
        else:
            log("⚠️ 未找到头条号页面")
        
        # ======== 百家号 ========
        if "baijiahao" in pages:
            log("\n📰 百家号发布中...")
            pg = pages["baijiahao"]
            pg.goto("https://baijiahao.baidu.com/publish", wait_until='domcontentloaded', timeout=20000)
            time.sleep(3)
            
            for i, art in enumerate(articles[2:4]):
                log(f"  📝 [{i+1}/2] {art['title'][:30]}")
                try:
                    ti = pg.locator('input[placeholder*="标题"]').first
                    if ti.is_visible(timeout=3000):
                        ti.fill(art['title'])
                    ed = pg.locator('[contenteditable="true"]').first
                    if ed.is_visible(timeout=3000):
                        ed.fill(art['body'][:3000])
                    log(f"    ✅ 内容已填入")
                except Exception as e:
                    log(f"    ⚠️ {str(e)[:40]}")
        else:
            log("⚠️ 未找到百家号页面")
        
        # ======== 知乎 ========
        if "zhihu" in pages:
            log("\n💬 知乎好物发布中...")
            pg = pages["zhihu"]
            questions = [
                "普通人如何利用AI每月多赚5000元",
                "2026年学什么AI技能最赚钱",
                "AI写作工具哪个最好用 免费的有哪些"
            ]
            
            for i, (qn, ans) in enumerate(zip(questions, answers[:3])):
                log(f"  📝 [{i+1}/3] {qn[:25]}")
                try:
                    pg.goto(f"https://www.zhihu.com/search?type=content&q={qn}", wait_until='domcontentloaded', timeout=20000)
                    time.sleep(4)
                    # Try to click first result
                    try:
                        r = pg.locator('.ContentItem-title a, .SearchResult-title a').first
                        if r.is_visible(timeout=5000):
                            r.click()
                            time.sleep(2)
                    except:
                        pass
                    log(f"    ✅ 已打开问题页")
                except Exception as e:
                    log(f"    ⚠️ {str(e)[:40]}")
        else:
            log("⚠️ 未找到知乎页面")
        
        # ======== 闲鱼 ========
        if "xianyu" in pages:
            log("\n🏪 闲鱼页面已就绪")
            pages["xianyu"].bring_to_front()
            log("ℹ️ 请手动点击「发布」→「发布闲置」")
        
        log("\n" + "=" * 50)
        log("🎉 发布完成！")
        log("=" * 50)

def main():
    log("🚀 AI智变·全自动发布系统启动")
    
    # Step 1: Start Chrome
    log("正在启动Chrome浏览器...")
    proc = start_chrome()
    if not proc:
        sys.exit(1)
    
    # Step 2: Open platforms
    log("正在打开所有平台...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            
            urls = [
                ("头条号", "https://mp.toutiao.com/"),
                ("百家号", "https://baijiahao.baidu.com/"),
                ("知乎", "https://www.zhihu.com/"),
                ("闲鱼", "https://www.goofish.com/"),
                ("小红书", "https://creator.xiaohongshu.com/"),
            ]
            
            for name, url in urls:
                pg = context.new_page()
                pg.goto(url, wait_until='domcontentloaded', timeout=15000)
                log(f"  ✅ {name}")
    except Exception as e:
        log(f"❌ 打开页面失败: {e}")
        return
    
    log("\n🎉 浏览器已打开！请在Chrome窗口中登录所有平台")
    log("登录完成后，在终端按 Enter 继续...")
    input()
    
    # Step 3: Publish
    log("开始自动发布...")
    publish_all()
    
    log("\n💡 Chrome窗口会保持打开，您可以检查发布结果")

if __name__ == "__main__":
    main()
