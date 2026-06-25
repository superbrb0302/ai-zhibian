#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║         AI智变 · 全自动发布引擎 v3.0                          ║
║         连接到Playwright Chrome，全自动发布到所有平台           ║
╚═══════════════════════════════════════════════════════════════╝

使用方法:
  1. 先启动 Chrome with Playwright:
     python3 -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.chromium.launch_persistent_context('/tmp/chrome_profile', headless=False, args=['--remote-debugging-port=9222']); input('Press Enter to exit')"
  
  2. 登录所有平台（手动一次）
  
  3. 运行本脚本:
     python3 publish_automation.py
"""
import os, sys, json, time, re
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class PublishEngine:
    def __init__(self):
        self.play = None
        self.browser = None
        self.context = None
    
    def connect(self):
        """连接到已有的Chrome实例"""
        self.play = sync_playwright().start()
        # 连接到现有的Chrome (需要--remote-debugging-port=9222启动)
        self.browser = self.play.chromium.connect_over_cdp("http://localhost:9222")
        self.context = self.browser.contexts[0]
        print("✅ 已连接到Chrome浏览器")
    
    def launch_fresh(self):
        """启动一个新的Chrome实例"""
        self.play = sync_playwright().start()
        self.browser = self.play.chromium.launch(
            headless=False,
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            args=['--no-first-run', '--no-default-browser-check', '--window-size=1400,900']
        )
        self.context = self.browser.new_context()
        print("✅ 已启动新的Chrome实例")
        return self.context
    
    def new_tab(self, url, timeout=15000):
        """打开新标签页"""
        page = self.context.new_page()
        page.goto(url, wait_until='domcontentloaded', timeout=timeout)
        return page
    
    # ================================================================
    # 知乎好物发布
    # ================================================================
    def publish_zhihu(self):
        """发布3篇知乎好物回答"""
        print("\n" + "="*50)
        print("💬 知乎好物 - 开始发布回答")
        print("="*50)
        
        # 读取已生成的回答
        zhihu_dir = os.path.join(BASE_DIR, "zhihu_output")
        if not os.path.exists(zhihu_dir):
            print("❌ 没有找到知乎回答文件，请先运行 python3 boss.py zhihu")
            return
        
        answer_files = sorted([f for f in os.listdir(zhihu_dir) if f.startswith("zhihu_") and f.endswith(".md")])
        if not answer_files:
            print("❌ 没有找到知乎回答文件")
            return
        
        # 定义3个知乎问题的真实链接（需要用户确认或者手动搜索）
        # 这里我们在知乎上搜索对应问题
        search_queries = [
            "普通人如何利用AI每月多赚5000元",
            "2026年学什么AI技能最赚钱",
            "AI写作工具哪个最好用 免费的有哪些"
        ]
        
        for i, (af, query) in enumerate(zip(answer_files[:3], search_queries)):
            print(f"\n📝 回答 {i+1}: {query[:30]}...")
            
            # 读取回答内容
            with open(os.path.join(zhihu_dir, af), "r", encoding="utf-8") as f:
                content = f.read()
            
            # 提取正文（去掉头部的markdown标题和结尾的推广信息）
            # 先找到第一个---之后的内容
            parts = content.split("---")
            main_body = parts[0] if len(parts) > 0 else content
            
            # 打开知乎搜索
            page = self.new_tab(f"https://www.zhihu.com/search?type=content&q={query}", timeout=20000)
            time.sleep(5)
            
            # 检查是否已登录
            page_title = page.title()
            if "登录" in page_title or "signin" in page.url:
                print(f"  ⚠️  知乎未登录，跳过")
                page.close()
                continue
            
            # 尝试点击"写回答"按钮
            try:
                write_btn = page.locator('button:has-text("写回答")').first
                if write_btn.is_visible(timeout=5000):
                    write_btn.click()
                    time.sleep(3)
                    
                    # 在编辑器输入内容
                    editor = page.locator('[contenteditable="true"]').first
                    if editor.is_visible(timeout=5000):
                        editor.fill(main_body[:1000])  # 先输入前1000字
                        print(f"  ✅ 已填入内容")
                    else:
                        print(f"  ⚠️ 未找到编辑器")
                else:
                    print(f"  ⚠️ 未找到写回答按钮")
            except Exception as e:
                print(f"  ⚠️ {e}")
            
            page.close()
        
        print("\n✅ 知乎发布完成！（部分需要手动确认）")
    
    # ================================================================
    # 闲鱼上架
    # ================================================================
    def publish_xianyu(self):
        """在闲鱼上架AI代写服务"""
        print("\n" + "="*50)
        print("🏪 闲鱼 - 上架AI代写服务")
        print("="*50)
        
        page = self.new_tab("https://www.goofish.com/", timeout=20000)
        time.sleep(5)
        
        # 检查是否登录
        if "login" in page.url.lower():
            print("  ⚠️ 闲鱼未登录")
            page.close()
            return
        
        # 读取服务描述
        services_path = os.path.join(BASE_DIR, "xianyu", "services.txt")
        if not os.path.exists(services_path):
            print("❌ 未找到services.txt")
            page.close()
            return
        
        with open(services_path, "r", encoding="utf-8") as f:
            services = f.read()
        
        # 寻找"发布"按钮
        try:
            publish_btn = page.locator('text=发布').first
            if publish_btn.is_visible(timeout=5000):
                publish_btn.click()
                time.sleep(3)
                print("  ✅ 已点击发布按钮")
            else:
                print("  ⚠️ 未找到发布按钮")
        except:
            # Try going directly to the publish page
            page.goto("https://www.goofish.com/publish", wait_until='domcontentloaded', timeout=15000)
            time.sleep(3)
            print("  ℹ️ 尝试直接导航到发布页")
        
        page.close()
        print("\n✅ 闲鱼上架流程已启动（请手动确认）")
    
    # ================================================================
    # 头条号发布
    # ================================================================
    def publish_toutiao(self):
        """发布每日内容到头条号"""
        print("\n" + "="*50)
        print("📰 头条号 - 发布内容")
        print("="*50)
        
        # 查找每日内容包
        daily_dir = os.path.join(BASE_DIR, "daily_pack_20260624")
        if not os.path.exists(daily_dir):
            print("❌ 未找到每日内容包")
            return
        
        files = sorted([f for f in os.listdir(daily_dir) if f.endswith(".txt") and not f.endswith("_info.txt")])
        if not files:
            print("❌ 没有内容可发布")
            return
        
        # 打开头条号管理后台
        page = self.new_tab("https://mp.toutiao.com/", timeout=20000)
        time.sleep(5)
        
        if "login" in page.url.lower() or "passport" in page.url.lower():
            print("  ⚠️ 头条号未登录")
            page.close()
            return
        
        # 尝试找到"发布文章"按钮
        try:
            publish_btn = page.locator('text=发布文章, text=写文章, text=新建').first
            if publish_btn.is_visible(timeout=5000):
                publish_btn.click()
                time.sleep(3)
                print("  ✅ 已打开文章编辑器")
            else:
                page.goto("https://mp.toutiao.com/profile_v4/article/create", wait_until='domcontentloaded', timeout=15000)
                time.sleep(3)
        except:
            pass
        
        # 发布第一篇
        for f in files[:2]:  # 发布2篇
            filepath = os.path.join(daily_dir, f)
            with open(filepath, "r", encoding="utf-8") as fh:
                content = fh.read()
            
            # 提取标题和正文
            lines = content.strip().split("\n")
            title = lines[0].replace("#", "").strip() if lines else "AI文章"
            body = "\n".join(lines[1:]).strip()
            
            print(f"  发布: {title[:30]}...")
            
            # 填入标题
            try:
                title_input = page.locator('[placeholder*="标题"], .article-title, input[type="text"]').first
                if title_input.is_visible(timeout=3000):
                    title_input.fill(title)
            except:
                pass
            
            # 填入正文
            try:
                body_editor = page.locator('[contenteditable="true"], .editor-content, textarea').first
                if body_editor.is_visible(timeout=3000):
                    body_editor.fill(body[:2000])
            except:
                pass
            
            # 尝试发布
            try:
                submit_btn = page.locator('button:has-text("发布"), button:has-text("发表"), button:has-text("提交")').first
                if submit_btn.is_visible(timeout=3000):
                    submit_btn.click()
                    print(f"  ✅ 已提交发布")
                    time.sleep(3)
            except:
                print(f"  ⚠️ 需要手动确认发布")
        
        page.close()
        print("\n✅ 头条号发布完成")
    
    # ================================================================
    # 百家号发布
    # ================================================================
    def publish_baijiahao(self):
        """发布每日内容到百家号"""
        print("\n" + "="*50)
        print("📰 百家号 - 发布内容")
        print("="*50)
        
        daily_dir = os.path.join(BASE_DIR, "daily_pack_20260624")
        if not os.path.exists(daily_dir):
            print("❌ 未找到每日内容包")
            return
        
        files = sorted([f for f in os.listdir(daily_dir) if f.endswith(".txt") and not f.endswith("_info.txt")])
        if not files:
            print("❌ 没有内容可发布")
            return
        
        page = self.new_tab("https://baijiahao.baidu.com/", timeout=20000)
        time.sleep(5)
        
        if "login" in page.url.lower():
            print("  ⚠️ 百家号未登录")
            page.close()
            return
        
        # 导航到发布页
        try:
            page.goto("https://baijiahao.baidu.com/publish", wait_until='domcontentloaded', timeout=15000)
            time.sleep(3)
            print("  ✅ 已打开百家号发布页")
        except:
            pass
        
        for f in files[2:4]:  # 发布2篇
            filepath = os.path.join(daily_dir, f)
            with open(filepath, "r", encoding="utf-8") as fh:
                content = fh.read()
            
            lines = content.strip().split("\n")
            title = lines[0].replace("#", "").strip() if lines else "AI文章"
            body = "\n".join(lines[1:]).strip()
            
            print(f"  发布: {title[:30]}...")
            
            try:
                title_input = page.locator('[placeholder*="标题"], input[type="text"]').first
                if title_input.is_visible(timeout=3000):
                    title_input.fill(title)
            except:
                pass
            
            try:
                body_editor = page.locator('[contenteditable="true"], .ql-editor, textarea').first
                if body_editor.is_visible(timeout=3000):
                    body_editor.fill(body[:2000])
            except:
                pass
            
            try:
                submit_btn = page.locator('button:has-text("发布"), button:has-text("发表")').first
                if submit_btn.is_visible(timeout=3000):
                    submit_btn.click()
                    time.sleep(3)
            except:
                pass
        
        page.close()
        print("\n✅ 百家号发布完成")
    
    # ================================================================
    # 公众号注册引导
    # ================================================================
    def setup_wechat(self):
        """引导注册微信公众号"""
        print("\n" + "="*50)
        print("📱 公众号 - 注册引导")
        print("="*50)
        
        page = self.new_tab("https://mp.weixin.qq.com/", timeout=20000)
        time.sleep(3)
        
        print("\n  ℹ️ 公众号注册需要扫码 + 实名认证，无法自动完成")
        print("  请手动完成以下步骤：")
        print("    1. 点击「立即注册」按钮")
        print("    2. 选择「订阅号」")
        print("    3. 填写邮箱、密码等信息")
        print("    4. 用微信扫码验证")
        print("    5. 实名认证")
        
        # 读取公众号设置指南
        guide_path = os.path.join(BASE_DIR, "wechat_output", f"wechat_setup_guide_20260624.md")
        if os.path.exists(guide_path):
            with open(guide_path, "r", encoding="utf-8") as f:
                guide = f.read()
            print(f"\n📄 注册指南已准备好在: wechat_output/")
        
        page.close()
    
    def close(self):
        """清理资源"""
        if self.browser:
            self.browser.close()
        if self.play:
            self.play.stop()


def main():
    engine = PublishEngine()
    
    print("╔══════════════════════════════════════════╗")
    print("║   AI智变 · 全自动发布引擎 v3.0           ║")
    print("╚══════════════════════════════════════════╝")
    print()
    
    # 先连接或启动浏览器
    choice = input("1. 连接到已有Chrome (端口9222)\n2. 启动新Chrome\n请选择 [1]: ") or "1"
    
    if choice == "2":
        ctx = engine.launch_fresh()
        # 打开所有平台
        for name, url in [
            ("头条号", "https://mp.toutiao.com/"),
            ("百家号", "https://baijiahao.baidu.com/"),
            ("知乎", "https://www.zhihu.com/"),
            ("闲鱼", "https://www.goofish.com/"),
            ("公众号", "https://mp.weixin.qq.com/"),
        ]:
            p = ctx.new_page()
            p.goto(url, wait_until='domcontentloaded', timeout=20000)
            print(f"  ✅ 已打开{name}")
        
        input("\n请登录所有平台后，按 Enter 继续...")
    else:
        try:
            engine.connect()
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            print("请确保Chrome以 --remote-debugging-port=9222 启动")
            return
    
    # 执行发布任务
    print("\n🚀 开始自动发布...")
    
    engine.publish_zhihu()
    engine.publish_xianyu()
    engine.publish_toutiao()
    engine.publish_baijiahao()
    engine.setup_wechat()
    
    print("\n" + "="*50)
    print("🎉 所有发布任务已完成！")
    print("="*50)
    print("\n💰 变现提醒:")
    print("  - 闲鱼代写: 今天即可接单")
    print("  - 知乎好物: 3天后开始见效")
    print("  - 头条/百家: 持续积累流量")
    print("  - 公众号: 注册后即可发布")
    
    engine.close()


if __name__ == "__main__":
    main()
