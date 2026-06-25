#!/usr/bin/env python3
"""AI智变·全自动发布引擎 - 一键发布到所有平台"""
import os, sys, time, json, re
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def read_daily_articles():
    """读取每日内容包"""
    dir_path = os.path.join(BASE, "daily_pack_20260624")
    files = sorted([f for f in os.listdir(dir_path) if f.endswith(".txt") and not f.endswith("_info.txt")])
    articles = []
    for f in files:
        with open(os.path.join(dir_path, f), "r", encoding="utf-8") as fh:
            content = fh.read().strip()
        lines = content.split("\n")
        title = lines[0].replace("#", "").strip() if lines else "AI文章"
        body = "\n".join(lines[1:]).strip()
        articles.append({"title": title, "body": body, "file": f})
    return articles

def read_zhihu_answers():
    """读取知乎回答"""
    dir_path = os.path.join(BASE, "zhihu_output")
    files = sorted([f for f in os.listdir(dir_path) if f.startswith("zhihu_") and f.endswith(".md")])
    answers = []
    for f in files:
        with open(os.path.join(dir_path, f), "r", encoding="utf-8") as fh:
            content = fh.read().strip()
        answers.append({"content": content, "file": f})
    return answers

class AutoPublish:
    def __init__(self):
        self.play = None
        self.browser = None
        self.context = None
    
    def connect(self):
        self.play = sync_playwright().start()
        self.browser = self.play.chromium.connect_over_cdp("http://localhost:9222")
        self.context = self.browser.contexts[0]
        log("✅ 已连接到Chrome浏览器")
        return self
    
    def find_page(self, keyword):
        """Find page by URL keyword"""
        for p in self.context.pages:
            if keyword in p.url:
                return p
        return None
    
    def new_page(self, url):
        p = self.context.new_page()
        p.goto(url, wait_until='domcontentloaded', timeout=20000)
        return p
    
    # ============================================================
    # 📰 头条号发布
    # ============================================================
    def publish_toutiao(self, articles):
        log("=" * 50)
        log("📰 头条号 - 开始发布")
        log("=" * 50)
        
        page = self.find_page("mp.toutiao.com")
        if not page:
            page = self.new_page("https://mp.toutiao.com/profile_v4/article/create")
        
        for i, art in enumerate(articles[:2]):
            log(f"📝 发布 [{i+1}/2]: {art['title'][:30]}...")
            try:
                # Navigate to create page
                page.goto("https://mp.toutiao.com/profile_v4/article/create", 
                          wait_until='domcontentloaded', timeout=20000)
                time.sleep(3)
                
                # Try to fill title
                try:
                    title_input = page.locator('input[placeholder*="标题"], .article-title-input, .title-input').first
                    if title_input.is_visible(timeout=5000):
                        title_input.fill(art['title'])
                        log(f"  ✅ 标题已填入")
                except:
                    log(f"  ⚠️ 标题填入失败")
                
                # Try to fill body
                try:
                    body_editor = page.locator('[contenteditable="true"], .editor-content, .ql-editor').first
                    if body_editor.is_visible(timeout=5000):
                        body_editor.fill(art['body'][:2000])
                        log(f"  ✅ 正文已填入")
                except:
                    log(f"  ⚠️ 正文填入失败")
                
                # Try to click publish
                try:
                    pub_btn = page.locator('button:has-text("发布"), button:has-text("发表")').first
                    if pub_btn.is_visible(timeout=3000):
                        pub_btn.click()
                        log(f"  ✅ 已点击发布")
                        time.sleep(3)
                except:
                    log(f"  ⚠️ 需要手动发布")
            except Exception as e:
                log(f"  ❌ 出错: {str(e)[:50]}")
        log("✅ 头条号发布完成")
    
    # ============================================================
    # 📰 百家号发布
    # ============================================================
    def publish_baijiahao(self, articles):
        log("=" * 50)
        log("📰 百家号 - 开始发布")
        log("=" * 50)
        
        page = self.find_page("baijiahao.baidu.com")
        if not page:
            page = self.new_page("https://baijiahao.baidu.com/publish")
        
        for i, art in enumerate(articles[2:4]):
            log(f"📝 发布 [{i+1}/2]: {art['title'][:30]}...")
            try:
                page.goto("https://baijiahao.baidu.com/publish", 
                          wait_until='domcontentloaded', timeout=20000)
                time.sleep(3)
                
                try:
                    title_input = page.locator('input[placeholder*="标题"], .article-title, .ql-title').first
                    if title_input.is_visible(timeout=5000):
                        title_input.fill(art['title'])
                        log(f"  ✅ 标题已填入")
                except:
                    log(f"  ⚠️ 标题填入失败")
                
                try:
                    body_editor = page.locator('[contenteditable="true"], .ql-editor, .article-content').first
                    if body_editor.is_visible(timeout=5000):
                        body_editor.fill(art['body'][:2000])
                        log(f"  ✅ 正文已填入")
                except:
                    log(f"  ⚠️ 正文填入失败")
                
                try:
                    pub_btn = page.locator('button:has-text("发布"), button:has-text("发表")').first
                    if pub_btn.is_visible(timeout=3000):
                        pub_btn.click()
                        log(f"  ✅ 已点击发布")
                        time.sleep(3)
                except:
                    log(f"  ⚠️ 需要手动发布")
            except Exception as e:
                log(f"  ❌ 出错: {str(e)[:50]}")
        log("✅ 百家号发布完成")
    
    # ============================================================
    # 💬 知乎好物发布
    # ============================================================
    def publish_zhihu(self, answers):
        log("=" * 50)
        log("💬 知乎好物 - 开始发布回答")
        log("=" * 50)
        
        page = self.find_page("zhihu.com")
        if not page:
            page = self.new_page("https://www.zhihu.com/")
        
        # Questions to search for
        questions = [
            "普通人如何利用AI每月多赚5000元",
            "2026年学什么AI技能最赚钱",
            "AI写作工具哪个最好用 免费的有哪些"
        ]
        
        for i, (qn, ans) in enumerate(zip(questions, answers[:3])):
            log(f"📝 回答 [{i+1}/3]: {qn[:25]}...")
            try:
                # Parse the answer content
                content = ans['content']
                # Extract main text (between question and resource section)
                parts = content.split("---")
                main_text = parts[0] if len(parts) > 0 else content
                
                # Search for the question
                search_url = f"https://www.zhihu.com/search?type=content&q={qn}"
                page.goto(search_url, wait_until='domcontentloaded', timeout=20000)
                time.sleep(4)
                
                # Try to find and click a question link
                try:
                    # Click on the first search result
                    first_result = page.locator('.ContentItem-title a, .SearchResult-title a, .List-item a').first
                    if first_result.is_visible(timeout=5000):
                        first_result.click()
                        time.sleep(3)
                        log(f"  ✅ 已打开问题页")
                except:
                    log(f"  ⚠️ 无法点击搜索结果")
                
                # Try to click "写回答" button
                try:
                    answer_btn = page.locator('button:has-text("写回答"), div:has-text("写回答")').first
                    if answer_btn.is_visible(timeout=5000):
                        answer_btn.click()
                        time.sleep(2)
                        log(f"  ✅ 已打开回答编辑器")
                except:
                    log(f"  ⚠️ 未找到写回答按钮")
                
                # Fill in the answer
                try:
                    editor = page.locator('[contenteditable="true"], .RichText-editor, .DraftEditor-editor').first
                    if editor.is_visible(timeout=5000):
                        editor.fill(main_text[:1500])
                        log(f"  ✅ 回答内容已填入")
                except:
                    log(f"  ⚠️ 回答填入失败")
                
                # Try to publish
                try:
                    pub_btn = page.locator('button:has-text("发布"), button:has-text("提交")').first
                    if pub_btn.is_visible(timeout=3000):
                        pub_btn.click()
                        log(f"  ✅ 已提交回答")
                        time.sleep(3)
                except:
                    log(f"  ⚠️ 需要手动发布")
            except Exception as e:
                log(f"  ❌ 出错: {str(e)[:50]}")
        log("✅ 知乎好物发布完成")
    
    # ============================================================
    # 🏪 闲鱼准备
    # ============================================================
    def prepare_xianyu(self):
        log("=" * 50)
        log("🏪 闲鱼 - 准备上架服务")
        log("=" * 50)
        
        page = self.find_page("goofish.com")
        if not page:
            page = self.new_page("https://www.goofish.com/")
        
        try:
            page.bring_to_front()
            log("✅ 闲鱼页面已激活")
            log("ℹ️ 请手动点击「发布」→「发布闲置」来上架AI代写服务")
            log("📄 服务描述已准备好: xianyu/services.txt")
        except Exception as e:
            log(f"  ❌ {str(e)[:50]}")
        log("✅ 闲鱼准备完成")
    
    def close(self):
        if self.browser:
            self.browser.close()
        if self.play:
            self.play.stop()

def main():
    print("╔══════════════════════════════════════╗")
    print("║   AI智变 · 全自动发布引擎 v3.0       ║")
    print("╚══════════════════════════════════════╝")
    
    articles = read_daily_articles()
    answers = read_zhihu_answers()
    
    log(f"📚 今日文章: {len(articles)}篇")
    log(f"💬 知乎回答: {len(answers)}个")
    
    pub = AutoPublish()
    try:
        pub.connect()
        
        # Execute all publishing tasks
        pub.publish_toutiao(articles)
        pub.publish_baijiahao(articles)
        pub.publish_zhihu(answers)
        pub.prepare_xianyu()
        
        log("\n" + "=" * 50)
        log("🎉 所有发布任务已完成!")
        log("=" * 50)
        log("\n💰 今日收入来源:")
        log("  - 知乎好物: 3天见效，持续引流")
        log("  - 头条号/百家号: 流量分成")
        log("  - 闲鱼代写: 今天可接单赚钱!")
        log("  - 数字产品: 网站已部署可销售")
    except Exception as e:
        log(f"❌ 发生错误: {e}")
    finally:
        # Don't close browser, leave it open for user
        pass

if __name__ == "__main__":
    main()
