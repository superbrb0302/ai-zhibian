#!/usr/bin/env python3
"""AI智变 - 静态站点生成器"""
import json
import os
import re
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
ARTICLES_DIR = os.path.join(BASE_DIR, "articles")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
SITE_DIR = os.path.join(BASE_DIR, "site")

def load_template():
    with open(os.path.join(TEMPLATE_DIR, "base.html"), "r", encoding="utf-8") as f:
        return f.read()

def load_articles():
    articles = []
    if not os.path.exists(ARTICLES_DIR):
        return articles
    for fname in os.listdir(ARTICLES_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(ARTICLES_DIR, fname), "r", encoding="utf-8") as f:
                articles.append(json.load(f))
    return sorted(articles, key=lambda x: x["date"], reverse=True)

def render_home(template, articles):
    items = []
    for a in articles[:20]:
        items.append(f'''
        <div class="article-card">
            <div class="meta">
                <span>📅 {a["date"]}</span>
                <span>📂 {a["category"]}</span>
            </div>
            <h2><a href="/{a["slug"]}">{a["title"]}</a></h2>
            <div class="excerpt">{a["excerpt"]}...</div>
            <a href="/{a["slug"]}" class="read-more">阅读全文 →</a>
        </div>''')

    content = f'''
    <div class="article-list">
        <div style="text-align:center;padding:20px 0;">
            <h2 style="font-size:1.4em;color:#333;">最新AI内容</h2>
            <p style="color:#999;font-size:0.9em;">每日更新，帮你掌握AI前沿资讯与实用技巧</p>
        </div>
        {"".join(items)}
    </div>'''

    return template.replace("{{ title }}", "AI智变 - AI工具评测/AI教程/AI赚钱指南").replace(
        "{{ description }}", "AI智变为你提供最新的AI工具评测、实用AI教程、AI赚钱方法，帮助你在AI时代抓住机遇、提升效率、实现变现。").replace(
        "{{ keywords }}", "AI,人工智能,AI工具,AI教程,AI赚钱,AIGC,副业").replace(
        "{{ url }}", "/").replace(
        "{{ content }}", content)

def render_article(template, article):
    content = f'''
    <article class="article-content">
        <h1>{article["title"]}</h1>
        <div class="meta">
            <span>📅 {article["date"]}</span>
            <span>📂 {article["category"]}</span>
            <span>🏷️ {article["keywords"]}</span>
        </div>
        {article["content"]}
    </article>'''

    return template.replace("{{ title }}", article["title"]).replace(
        "{{ description }}", article["description"]).replace(
        "{{ keywords }}", article["keywords"]).replace(
        "{{ url }}", f"/{article['slug']}").replace(
        "{{ content }}", content)

def render_category(template, articles, cat_slug, cat_name):
    filtered = [a for a in articles if a["category"] == cat_slug]
    items = []
    for a in filtered[:30]:
        items.append(f'''
        <div class="article-card">
            <div class="meta"><span>📅 {a["date"]}</span></div>
            <h2><a href="/{a["slug"]}">{a["title"]}</a></h2>
            <div class="excerpt">{a["excerpt"]}...</div>
            <a href="/{a["slug"]}" class="read-more">阅读全文 →</a>
        </div>''')

    content = f'''
    <div class="article-list">
        <h2 style="margin-bottom:20px;">{cat_name}</h2>
        <p style="color:#999;margin-bottom:20px;">共 {len(filtered)} 篇文章</p>
        {"".join(items)}
    </div>'''

    return template.replace("{{ title }}", f"{cat_name} - AI智变").replace(
        "{{ description }}", f"AI智变{cat_name}分类，精选{cat_name}相关文章").replace(
        "{{ keywords }}", f"AI,{cat_name}").replace(
        "{{ url }}", f"/category/{cat_slug}.html").replace(
        "{{ content }}", content)

def render_about(template):
    content = '''
    <div class="article-content" style="max-width:700px;margin:0 auto;">
        <h1>关于AI智变</h1>
        <p>AI智变是一个专注人工智能领域的知识分享平台。</p>
        <p>我们的使命是：<strong>让每个人都能用AI武装自己，在AI时代抓住机遇。</strong></p>
        <h2>我们的内容</h2>
        <ul>
            <li><strong>AI工具评测</strong> - 实测市面上最热门的AI工具，给你最真实的使用体验和对比分析</li>
            <li><strong>AI教程</strong> - 从入门到精通，手把手教你使用各类AI工具和应用</li>
            <li><strong>AI赚钱</strong> - 分享普通人利用AI实现副业变现的真实方法和案例</li>
            <li><strong>AI资讯</strong> - 追踪AI行业最新动态，不错过任何重要变化</li>
        </ul>
        <h2>联系我们</h2>
        <p>有任何问题或合作意向，欢迎通过以下方式与我们联系。</p>
    </div>'''
    return template.replace("{{ title }}", "关于我们 - AI智变").replace(
        "{{ description }}", "关于AI智变平台").replace(
        "{{ keywords }}", "关于AI智变,联系我们").replace(
        "{{ url }}", "/about.html").replace(
        "{{ content }}", content)

def render_privacy(template):
    content = '''
    <div class="article-content" style="max-width:700px;margin:0 auto;">
        <h1>隐私政策</h1>
        <p>我们尊重并保护您的隐私。本隐私政策说明了我们如何收集、使用和保护您的个人信息。</p>
        <h2>信息收集</h2>
        <p>本网站使用Google Analytics等第三方服务收集匿名访问数据，包括页面浏览量、访问来源、设备信息等。这些数据仅用于优化网站内容和提升用户体验。</p>
        <h2>广告服务</h2>
        <p>本网站使用Google AdSense投放广告。Google可能会使用Cookie向您展示基于兴趣的广告。您可以在Google广告设置页面管理您的广告偏好。</p>
        <h2>外部链接</h2>
        <p>本网站包含指向第三方网站的外部链接。我们对这些网站的隐私保护措施不承担责任。</p>
        <h2>联系我们</h2>
        <p>如您对本隐私政策有任何疑问，请通过网站提供的联系方式与我们沟通。</p>
    </div>'''
    return template.replace("{{ title }}", "隐私政策 - AI智变").replace(
        "{{ description }}", "AI智变隐私政策").replace(
        "{{ keywords }}", "隐私政策,AI智变").replace(
        "{{ url }}", "/privacy.html").replace(
        "{{ content }}", content)

def build():
    print("🧹 清理输出目录...")
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    os.makedirs(os.path.join(OUTPUT_DIR, "category"))

    print("📖 加载文章...")
    articles = load_articles()
    print(f"   共 {len(articles)} 篇文章")

    print("🎨 加载模板...")
    template = load_template()

    print("🏠 生成首页...")
    homepage = render_home(template, articles)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(homepage)

    print("📄 生成文章页面...")
    for a in articles:
        page = render_article(template, a)
        with open(os.path.join(OUTPUT_DIR, a["slug"]), "w", encoding="utf-8") as f:
            f.write(page)

    print("📂 生成分类页面...")
    cats = {
        "ai-tools": "AI工具评测",
        "ai-tutorial": "AI教程",
        "ai-money": "AI赚钱",
        "ai-news": "AI资讯",
    }
    for slug, name in cats.items():
        page = render_category(template, articles, slug, name)
        with open(os.path.join(OUTPUT_DIR, "category", f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(page)

    print("ℹ️ 生成关于/隐私页面...")
    about = render_about(template)
    with open(os.path.join(OUTPUT_DIR, "about.html"), "w", encoding="utf-8") as f:
        f.write(about)
    privacy = render_privacy(template)
    with open(os.path.join(OUTPUT_DIR, "privacy.html"), "w", encoding="utf-8") as f:
        f.write(privacy)

    print(f"\n✅ 站点构建完成！输出目录: {OUTPUT_DIR}")
    print(f"   共生成 {len(articles) + 4} 个页面")
    
    # 统计摘要
    cat_counts = {}
    for a in articles:
        cat_counts[a["category"]] = cat_counts.get(a["category"], 0) + 1
    print(f"   分类分布: {cat_counts}")

if __name__ == "__main__":
    build()
