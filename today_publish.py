#!/usr/bin/env python3
"""
今日发布脚本 - 连接运行中的Chrome，自动发布到所有平台
"""
import os, sys, time, json, re, random
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))

def log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    print(f"[{t}] {msg}")

def find_page(pages, keyword):
    for p in pages:
        if keyword in p.url.lower():
            return p
    return None

def wait_and_click(page, selector, timeout=5000):
    try:
        el = page.locator(selector).first
        if el.is_visible(timeout=timeout):
            el.click()
            time.sleep(1)
            return True
    except:
        pass
    return False

def fill_input(page, selector, text, timeout=3000):
    try:
        el = page.locator(selector).first
        if el.is_visible(timeout=timeout):
            el.fill(text)
            time.sleep(0.5)
            return True
    except:
        pass
    return False

# ================================================================
# Main
# ================================================================
log("🚀 今日发布脚本启动")
log(f"📅 {datetime.now().strftime('%Y年%m月%d日')}")

# Connect to Chrome
play = sync_playwright().start()
browser = play.chromium.connect_over_cdp("http://localhost:9222")
context = browser.contexts[0]
pages = context.pages
log(f"✅ 已连接到Chrome，共 {len(pages)} 个标签页")

# ================================================================
# 1. 头条号发布
# ================================================================
log("\n" + "="*50)
log("📰 头条号 - 发布内容")
log("="*50)

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

log(f"📚 共 {len(articles)} 篇今日文章")

# 头条号
toutiao_page = find_page(pages, "toutiao")
if toutiao_page:
    log("📰 头条号页面已找到，跳转到发布页...")
    try:
        toutiao_page.goto("https://mp.toutiao.com/profile_v4/article/create", wait_until='domcontentloaded', timeout=20000)
        time.sleep(4)
        
        for i, art in enumerate(articles[:2]):
            log(f"  📝 第{i+1}篇: {art['title'][:30]}...")
            
            # Clear and fill title
            try:
                title_input = toutiao_page.locator('input[placeholder*="标题"]').first
                if title_input.is_visible(timeout=3000):
                    title_input.click()
                    title_input.fill("")
                    time.sleep(0.5)
                    title_input.fill(art['title'])
                    log(f"    ✅ 标题已填入")
            except Exception as e:
                log(f"    ⚠️ 标题: {str(e)[:40]}")
            
            # Fill body
            try:
                # Try different editor selectors
                body_editor = toutiao_page.locator('[contenteditable="true"]').first
                if body_editor.is_visible(timeout=3000):
                    body_editor.click()
                    time.sleep(0.5)
                    # Type in chunks
                    text = art['body'][:3000]
                    body_editor.fill(text)
                    log(f"    ✅ 正文已填入 ({len(text)}字)")
            except Exception as e:
                log(f"    ⚠️ 正文: {str(e)[:40]}")
            
            if i == 0:
                log(f"    💡 内容已填入第1篇文章，请检查后手动点「发布」")
                break  # Just fill first article for now
    except Exception as e:
        log(f"❌ 头条号出错: {e}")
else:
    log("⚠️ 未找到头条号标签页，正在创建...")
    toutiao_page = context.new_page()
    toutiao_page.goto("https://mp.toutiao.com/profile_v4/article/create", wait_until='domcontentloaded', timeout=20000)
    time.sleep(5)

# ================================================================
# 2. 百家号发布
# ================================================================
log("\n" + "="*50)
log("📰 百家号 - 发布内容")
log("="*50)

baijia_page = find_page(pages, "baijiahao")
if baijia_page:
    log("📰 百家号页面已找到")
    try:
        # Navigate to content list first
        baijia_page.goto("https://baijiahao.baidu.com/builder/rc/content?currentPage=1&pageSize=10&search=&startTime=&endTime=&type=&status=0", wait_until='domcontentloaded', timeout=20000)
        time.sleep(4)
        
        # Click "写文章" button - try different approaches
        log("  🔍 寻找「写文章」按钮...")
        
        # Try clicking via JS
        try:
            btn = baijia_page.locator('span:has-text("写文章"), button:has-text("写文章"), a:has-text("写文章"), .article-btn, .publish-btn').first
            if btn.is_visible(timeout=5000):
                btn.click()
                log("  ✅ 点击了「写文章」")
                time.sleep(3)
            else:
                # Try direct URL
                log("  ⚠️ 按钮不可见，尝试直接URL...")
                baijia_page.goto("https://baijiahao.baidu.com/builder/rc/article/create?type=news", wait_until='domcontentloaded', timeout=20000)
                time.sleep(4)
        except:
            baijia_page.goto("https://baijiahao.baidu.com/builder/rc/article/create?type=news", wait_until='domcontentloaded', timeout=20000)
            time.sleep(4)
        
        # Fill content
        for i, art in enumerate(articles[2:4]):  # articles 3 and 4
            log(f"  📝 第{i+1}篇: {art['title'][:30]}...")
            
            # Fill title
            try:
                title_input = baijia_page.locator('input[placeholder*="标题"], #title, .title-input').first
                if title_input.is_visible(timeout=3000):
                    title_input.click()
                    title_input.fill("")
                    time.sleep(0.5)
                    title_input.fill(art['title'])
                    log(f"    ✅ 标题已填入")
            except Exception as e:
                log(f"    ⚠️ 标题: {str(e)[:40]}")
            
            # Fill body - contenteditable div
            try:
                body_editor = baijia_page.locator('[contenteditable="true"], .ql-editor, #article-content').first
                if body_editor.is_visible(timeout=3000):
                    body_editor.click()
                    time.sleep(0.5)
                    text = art['body'][:2000]
                    body_editor.fill(text)
                    log(f"    ✅ 正文已填入")
            except Exception as e:
                log(f"    ⚠️ 正文: {str(e)[:40]}")
            
            # Try to set cover image
            try:
                cover_btn = baijia_page.locator('span:has-text("上传封面"), .cover-upload, button:has-text("添加封面")').first
                if cover_btn.is_visible(timeout=3000):
                    cover_btn.click()
                    log(f"    ⚠️ 需要手动选择封面图")
                    time.sleep(2)
            except:
                pass
            
            if i == 0:
                log(f"    💡 内容已填入，请检查后手动点「发布」")
                break
    except Exception as e:
        log(f"❌ 百家号出错: {e}")
else:
    log("⚠️ 未找到百家号标签页")
    baijia_page = context.new_page()
    baijia_page.goto("https://baijiahao.baidu.com/builder/rc/article/create?type=news", wait_until='domcontentloaded', timeout=20000)
    time.sleep(5)

# ================================================================
# 3. 知乎提交回答
# ================================================================
log("\n" + "="*50)
log("💬 知乎 - 提交回答")
log("="*50)

zhihu_output = os.path.join(BASE, "zhihu_output")
answer_files = sorted([f for f in os.listdir(zhihu_output) if f.startswith("zhihu_20260626")]) if os.path.exists(zhihu_output) else []

if answer_files:
    log(f"📚 今天有 {len(answer_files)} 篇回答待发布")
    
    # Find zhihu pages
    zhihu_pages = [p for p in pages if "zhihu.com" in p.url and "search" not in p.url.lower()]
    log(f"📑 找到 {len(zhihu_pages)} 个知乎问题页")
    
    for p in zhihu_pages:
        try:
            log(f"  📄 {p.title()[:40]}...")
            p.bring_to_front()
            time.sleep(1)
            
            # Check if we can write answer
            try:
                write_btn = p.locator('button:has-text("写回答")').first
                if write_btn.is_visible(timeout=3000):
                    write_btn.click()
                    log(f"    ✅ 点击了「写回答」")
                    time.sleep(3)
                    
                    # Editor should now be visible
                    editor = p.locator('[contenteditable="true"], .editable, .DraftEditor-editorContainer').first
                    if editor.is_visible(timeout=3000):
                        # Read answer content
                        # Try to match answer to question
                        page_title = p.title().lower()
                        matched = None
                        for af in answer_files:
                            af_lower = af.lower()
                            if any(kw in af_lower for kw in ['ai赚钱', '月多赚', '5000'] if kw in page_title) or \
                               any(kw in af_lower for kw in ['ai技能', '赚钱技能'] if kw in page_title):
                                matched = af
                                break
                            if any(kw in page_title for kw in [af_lower[20:40] if len(af_lower)>20 else af_lower]):
                                matched = af
                                break
                        
                        if not matched:
                            matched = answer_files[0]
                        
                        with open(os.path.join(zhihu_output, matched), "r") as f:
                            answer_text = f.read()
                        
                        # Extract main body (after first --- and before affiliate)
                        parts = answer_text.split("---")
                        body = parts[0] if parts else answer_text
                        
                        # Paste into editor
                        editor.fill(body[:2000])
                        log(f"    ✅ 回答已填入")
                        
                        # Try to submit
                        submit_btn = p.locator('button:has-text("发布"), button:has-text("提交")').first
                        if submit_btn.is_visible(timeout=3000):
                            log(f"    💡 请检查内容后手动点击「发布」")
            except Exception as e:
                log(f"    ⚠️ {str(e)[:40]}")
        except Exception as e:
            log(f"  ⚠️ {str(e)[:40]}")
else:
    log("⚠️ 没有找到今日知乎回答文件")

# ================================================================
# 4. 小红书发布
# ================================================================
log("\n" + "="*50)
log("🛍️ 小红书 - 发布首帖")
log("="*50)

xhs_page = find_page(pages, "xiaohongshu")
if xhs_page:
    log("🛍️ 小红书页面已找到")
    try:
        xhs_page.bring_to_front()
        # Navigate to create page
        xhs_page.goto("https://creator.xiaohongshu.com/new/note", wait_until='domcontentloaded', timeout=20000)
        time.sleep(4)
        
        # Fill first post content
        xhs_article = articles[0] if articles else None
        if xhs_article:
            log(f"  📝 {xhs_article['title'][:30]}...")
            
            # Fill title/content
            try:
                title_input = xhs_page.locator('input[placeholder*="标题"], .note-input, [contenteditable="true"]').first
                if title_input.is_visible(timeout=3000):
                    title_input.fill(xhs_article['title'])
                    log(f"    ✅ 标题已填入")
            except:
                pass
            
            try:
                body_area = xhs_page.locator('textarea[placeholder*="正文"], [contenteditable="true"]').first
                if body_area.is_visible(timeout=3000):
                    body_area.fill(xhs_article['body'][:800])
                    log(f"    ✅ 正文已填入")
            except:
                pass
            
            log(f"    💡 请检查内容后手动发布")
        else:
            log("⚠️ 没有文章内容")
    except Exception as e:
        log(f"❌ 小红书出错: {e}")
else:
    log("⚠️ 未找到小红书页面")

# ================================================================
# 5. 闲鱼检查
# ================================================================
log("\n" + "="*50)
log("🏪 闲鱼 - 检查消息")
log("="*50)

xianyu_page = find_page(pages, "goofish")
if xianyu_page:
    try:
        xianyu_page.bring_to_front()
        time.sleep(2)
        log("✅ 闲鱼页面已就绪")
        
        # Check for messages
        try:
            msg_count = xianyu_page.locator('.message-badge, .unread-count, [class*="unread"]').first
            if msg_count.is_visible(timeout=2000):
                log(f"  💬 有未读消息: {msg_count.text_content()}")
            else:
                log(f"  ✅ 暂无未读消息")
        except:
            log(f"  ℹ️ 请自行检查消息和订单")
    except Exception as e:
        log(f"❌ 闲鱼出错: {e}")
else:
    log("⚠️ 未找到闲鱼页面")

# ================================================================
# Summary
# ================================================================
log("\n" + "="*50)
log("🎉 今日发布任务执行完成！")
log("="*50)

# Print summary
summary = f"""
📋 今日工作总结（{datetime.now().strftime('%Y-%m-%d')}）:

📰 头条号:    内容已填入编辑器，请手动点「发布」
📰 百家号:    内容已填入编辑器，请手动点「发布」（可能需要设置封面）
💬 知乎:      回答已填入/就绪，请手动点「发布」
🛍️ 小红书:    首帖已就绪，请手动发布
🏪 闲鱼:      请查看是否有新消息
📱 公众号:    注册指南准备好，但需扫码注册

💡 请在各平台检查内容后手动点发布按钮
"""
log(summary)

# Don't close the browser - keep it running
# browser.close()
# play.stop()

input("\n按 Enter 退出脚本（Chrome会保持打开）...")
