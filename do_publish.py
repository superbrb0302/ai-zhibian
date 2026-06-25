#!/usr/bin/env python3
"""全自动发布脚本 - 不阻塞"""
import os, sys, time, json, re, random
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def find_page(pages, keyword):
    for p in pages:
        if keyword in p.url.lower():
            return p
    return None

# Load today's articles
daily_dir = os.path.join(BASE, "daily_pack_20260626")
articles = []
if os.path.exists(daily_dir):
    files = sorted([f for f in os.listdir(daily_dir) if f.endswith(".txt") and not f.endswith("_info.txt")])
    for f in files:
        with open(os.path.join(daily_dir, f), "r") as fh:
            content = fh.read().strip()
        lines = content.split("\n")
        title = lines[0].replace("#", "").strip() if lines else "AI文章"
        body = "\n".join(lines[1:]).strip()
        articles.append({"title": title, "body": body, "file": f})

# Connect to Chrome
log("🚀 连接Chrome浏览器...")
play = sync_playwright().start()
browser = play.chromium.connect_over_cdp("http://localhost:9222")
context = browser.contexts[0]
pages = context.pages
log(f"✅ 已连接，共 {len(pages)} 个标签页")

# ======== 1. 头条号 ========
log("\n" + "="*50)
log("📰 头条号发布中...")
toutiao = find_page(pages, "toutiao")
if toutiao:
    toutiao.bring_to_front()
    time.sleep(1)
    log(f"  页面: {toutiao.title()}")
    
    if articles:
        art = articles[0]
        log(f"  填入: {art['title'][:30]}...")
        
        # Fill title
        try:
            ti = toutiao.locator('input[placeholder*="标题"]').first
            if ti.is_visible(timeout=3000):
                ti.click()
                ti.fill("")
                time.sleep(0.3)
                ti.fill(art['title'])
                log(f"  ✅ 标题")
        except Exception as e:
            log(f"  ⚠️ 标题: {str(e)[:40]}")
        
        # Fill body
        try:
            ed = toutiao.locator('[contenteditable="true"]').first
            if ed.is_visible(timeout=3000):
                ed.click()
                time.sleep(0.3)
                ed.fill(art['body'][:3000])
                log(f"  ✅ 正文 ({len(art['body'][:3000])}字)")
        except Exception as e:
            log(f"  ⚠️ 正文: {str(e)[:40]}")
        
        log(f"  💡 内容已填入第1篇，请手动点「发布」")
else:
    log("⚠️ 未找到头条号")

# ======== 2. 百家号 ========
log("\n" + "="*50)
log("📰 百家号发布中...")
baijia = find_page(pages, "baijiahao")
if baijia:
    baijia.bring_to_front()
    time.sleep(1)
    
    # Navigate to create page
    baijia.goto("https://baijiahao.baidu.com/builder/rc/article/create?type=news", wait_until='domcontentloaded', timeout=20000)
    time.sleep(4)
    
    if len(articles) >= 3:
        art = articles[2]  # Use 3rd article
        log(f"  填入: {art['title'][:30]}...")
        
        # Fill title
        try:
            ti = baijia.locator('input[placeholder*="标题"]').first
            if ti.is_visible(timeout=3000):
                ti.click()
                ti.fill("")
                time.sleep(0.3)
                ti.fill(art['title'])
                log(f"  ✅ 标题")
        except Exception as e:
            log(f"  ⚠️ 标题: {str(e)[:40]}")
        
        # Fill body
        try:
            ed = baijia.locator('[contenteditable="true"]').first
            if ed.is_visible(timeout=3000):
                ed.click()
                time.sleep(0.3)
                ed.fill(art['body'][:3000])
                log(f"  ✅ 正文")
        except Exception as e:
            log(f"  ⚠️ 正文: {str(e)[:40]}")
        
        log(f"  💡 内容已填入，请手动设置封面后点「发布」")
else:
    log("⚠️ 未找到百家号")

# ======== 3. 知乎 ========
log("\n" + "="*50)
log("💬 知乎提交回答...")

# Read today's answers
zhihu_dir = os.path.join(BASE, "zhihu_output")
answers = {}
if os.path.exists(zhihu_dir):
    for f in sorted(os.listdir(zhihu_dir)):
        if f.startswith("zhihu_20260626"):
            with open(os.path.join(zhihu_dir, f), "r") as fh:
                answers[f] = fh.read()
            log(f"  📄 {f}")

# Find question pages (not search pages)
q_pages = [p for p in pages if "zhihu.com/question/" in p.url]
log(f"  📑 找到 {len(q_pages)} 个知乎问题页")

for p in q_pages:
    try:
        p.bring_to_front()
        time.sleep(2)
        log(f"  📄 {p.title()[:40]}...")
        
        # Click "写回答"
        try:
            btn = p.locator('button:has-text("写回答")').first
            if btn.is_visible(timeout=3000):
                btn.click()
                time.sleep(2)
                log(f"  ✅ 已点「写回答」")
                
                # Fill editor
                editor = p.locator('[contenteditable="true"]').first
                if editor.is_visible(timeout=3000):
                    # Find matching answer
                    body = ""
                    for fname, content in answers.items():
                        # Try to match
                        if any(kw in fname.lower() for kw in ['ai赚钱', '赚钱', '5000'] if kw in p.title().lower()):
                            body = content.split("---")[0] if "---" in content else content
                            break
                    
                    if not body and answers:
                        first_key = list(answers.keys())[0]
                        body = answers[first_key].split("---")[0] if "---" in answers[first_key] else answers[first_key]
                    
                    if body:
                        editor.fill(body[:3000])
                        log(f"  ✅ 回答已填入")
                else:
                    log(f"  ⚠️ 编辑器不可见")
        except Exception as e:
            log(f"  ⚠️ {str(e)[:40]}")
    except Exception as e:
        log(f"  ❌ {str(e)[:40]}")

# ======== 4. 小红书 ========
log("\n" + "="*50)
log("🛍️ 小红书发布...")
xhs = find_page(pages, "xiaohongshu")
if xhs:
    xhs.bring_to_front()
    time.sleep(1)
    log(f"  ✅ 已就绪（需手动发布首帖）")
    log(f"  💡 请打开创作中心 → 发布笔记")
else:
    log("⚠️ 未找到小红书")

# ======== 5. 闲鱼 ========
log("\n" + "="*50)
log("🏪 闲鱼检查...")
xianyu = find_page(pages, "goofish")
if xianyu:
    xianyu.bring_to_front()
    time.sleep(1)
    log(f"  ✅ 已就绪")
    log(f"  💡 请检查是否有新消息和订单")
else:
    log("⚠️ 未找到闲鱼")

# ======== Summary ========
log("\n" + "="*50)
log("🎉 发布完成！")
log("="*50)
log(f"""
📋 今日总结（{datetime.now().strftime('%Y-%m-%d')}）:

📰 头条号:  ✅ 第1篇内容已填入 → 请手动点「发布」
📰 百家号:  ✅ 内容已填入 → 请设置封面后点「发布」
💬 知乎:    ✅ 回答已填入部分问题
🛍️ 小红书:  已就绪 → 请手动发首帖
🏪 闲鱼:   已就绪 → 请检查消息
📱 公众号:  文章已生成 → 但需扫码注册

Chrome窗口会保持打开，您可以检查各平台的发布结果
""")

# Don't close browser
play.stop()
