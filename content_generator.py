#!/usr/bin/env python3
"""AI内容自动生成器 - 生产SEO优化的AI领域文章"""

import json
import os
import random
from datetime import datetime, timedelta

class AIContentGenerator:
    def __init__(self):
        self.articles_dir = os.path.join(os.path.dirname(__file__), "articles")
        os.makedirs(self.articles_dir, exist_ok=True)

    def get_all_articles(self):
        """读取所有已生成的文章"""
        articles = []
        if not os.path.exists(self.articles_dir):
            return articles
        for fname in sorted(os.listdir(self.articles_dir)):
            if fname.endswith(".json"):
                with open(os.path.join(self.articles_dir, fname), "r", encoding="utf-8") as f:
                    articles.append(json.load(f))
        return sorted(articles, key=lambda x: x["date"], reverse=True)

    def _make_slug(self, title):
        """生成URL友好的slug"""
        import re
        slug = title.lower()
        # Replace all Chinese/special chars and slashes with dash
        slug = re.sub(r'[，。！？：；""''（）【】《》、·…—/\ ]+', '-', slug)
        # Remove non-alphanumeric except dash
        slug = re.sub(r'[^a-z0-9\-]', '', slug)
        while "--" in slug: slug = slug.replace("--", "-")
        return slug.strip("-")[:60].strip("-") + ".html"

    def generate_batch(self, count=5):
        """批量生成文章"""
        articles = self.get_all_articles()
        existing_titles = {a["title"] for a in articles}
        latest_date = datetime.strptime(articles[0]["date"], "%Y-%m-%d") if articles else datetime.now()

        new_articles = []
        topics = self._get_topic_pool()
        random.shuffle(topics)

        for topic in topics:
            if len(new_articles) >= count:
                break
            if topic["title"] in existing_titles:
                continue
            latest_date += timedelta(hours=random.randint(4, 12))
            article = self._generate_one(topic, latest_date)
            new_articles.append(article)
            self._save_article(article)

        return new_articles

    def _save_article(self, article):
        fname = article["slug"].replace(".html", ".json")
        path = os.path.join(self.articles_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(article, f, ensure_ascii=False, indent=2)

    def _get_topic_pool(self):
        """AI领域选题池（可无限扩展）"""
        return [
            # AI工具评测系列
            {"title": "2026年最值得使用的10款免费AI写作工具评测", "category": "ai-tools", "keywords": "AI写作工具,免费AI写作,AI写作评测,AIGC工具推荐"},
            {"title": "Claude vs ChatGPT vs Gemini 2026最新对比：哪个更适合你？", "category": "ai-tools", "keywords": "Claude,ChatGPT,Gemini,AI对比,AI助手选择"},
            {"title": "2026年AI绘画工具推荐：Midjourney、DALL-E 3、Stable Diffusion全面对比", "category": "ai-tools", "keywords": "AI绘画,Midjourney,DALL-E,Stable Diffusion,AI绘图工具"},
            {"title": "Notion AI vs Microsoft Copilot vs 钉钉AI：办公AI助手哪家强？", "category": "ai-tools", "keywords": "AI办公,Notion AI,Microsoft Copilot,钉钉AI,办公效率"},
            {"title": "5款免费AI视频生成工具推荐：新手也能做出专业级视频", "category": "ai-tools", "keywords": "AI视频生成,免费AI工具,视频制作,AI视频教程"},
            # AI教程系列
            {"title": "零基础学AI：如何用ChatGPT在30分钟内完成一份商业计划书", "category": "ai-tutorial", "keywords": "ChatGPT教程,商业计划书,AI写作,效率提升"},
            {"title": "Prompt工程入门：5个万能公式让你成为AI提示词高手", "category": "ai-tutorial", "keywords": "Prompt工程,AI提示词,ChatGPT提示词,Prompt技巧"},
            {"title": "AI自动化工作流入门：用n8n和GPT搭建你的第一个智能助手", "category": "ai-tutorial", "keywords": "AI自动化,n8n,工作流自动化,GPT应用"},
            {"title": "如何用AI辅助学习任何技能：一个系统化方法", "category": "ai-tutorial", "keywords": "AI学习,AI辅助学习,技能学习,效率方法"},
            {"title": "2026年最实用的10个AI提示词模板（直接复制使用）", "category": "ai-tutorial", "keywords": "AI提示词模板,Prompt模板,ChatGPT模板,AI提示词"},
            # AI赚钱系列
            {"title": "普通人如何用AI副业月入5000+：5个经过验证的方法", "category": "ai-money", "keywords": "AI副业,AI赚钱,副业收入,AIGC变现"},
            {"title": "AI生成内容如何在头条号/百家号赚取流量收益：完整实操指南", "category": "ai-money", "keywords": "AI内容变现,头条号赚钱,百家号收益,流量分成"},
            {"title": "2026年最赚钱的AI技能排名：学完就能接单", "category": "ai-money", "keywords": "AI技能,赚钱技能,AI接单,自由职业"},
            {"title": "如何用AI制作数字产品在电商平台销售（模板/提示词包/教程）", "category": "ai-money", "keywords": "数字产品,AI变现,电商销售,被动收入"},
            {"title": "AI自媒体矩阵搭建指南：一次性运营5个平台的核心策略", "category": "ai-money", "keywords": "AI自媒体,矩阵运营,多平台运营,内容分发"},
            # AI资讯系列
            {"title": "OpenAI最新发布GPT-5：你需要知道的5个关键变化", "category": "ai-news", "keywords": "OpenAI,GPT-5,AI新闻,AI最新进展"},
            {"title": "2026年AI行业趋势报告：10个将改变世界的AI发展方向", "category": "ai-news", "keywords": "AI趋势,AI行业,AI发展方向,科技趋势"},
            {"title": "Google、Meta、微软2026年AI战略布局全面解读", "category": "ai-news", "keywords": "AI战略,Google AI,Meta AI,微软AI,科技巨头"},
            {"title": "中国AI大模型2026年最新进展：文心一言、通义千问、豆包等全面对比", "category": "ai-news", "keywords": "中国AI,大模型,文心一言,通义千问,豆包"},
            {"title": "AI安全与伦理2026：我们需要担心AI取代人类吗？", "category": "ai-news", "keywords": "AI安全,AI伦理,AI取代,人工智能未来"},
        ]

    def _generate_one(self, topic, date):
        """生成一篇文章的所有内容"""
        title = topic["title"]
        slug = self._make_slug(title)
        date_str = date.strftime("%Y-%m-%d")

        content_html = self._generate_content(title, topic["category"])
        excerpt = self._extract_excerpt(content_html)

        return {
            "title": title,
            "slug": slug,
            "date": date_str,
            "category": topic["category"],
            "keywords": topic["keywords"],
            "description": excerpt[:120],
            "excerpt": excerpt[:200],
            "content": content_html,
        }

    def _generate_content(self, title, category):
        """根据标题和分类自动生成文章内容"""
        paragraphs = []
        paragraphs.append(self._generate_intro(title))
        paragraphs.append(self._generate_section(title))
        paragraphs.append(self._generate_detail())
        paragraphs.append(self._generate_affiliate_section(title))
        paragraphs.append(self._generate_conclusion())
        paragraphs.append(self._generate_interaction())
        return "\n".join(paragraphs)

    def _generate_intro(self, title):
        intros = [
            f"<p>随着人工智能技术的飞速发展，{title}成为越来越多人关注的话题。无论你是AI新手还是有一定经验的从业者，这篇文章都将为你提供最实用、最前沿的信息。</p>",
            f"<p>在这个AI改变一切的时代，{title}是每一个想抓住机遇的人都需要了解的内容。本文将从多个角度深入分析，帮助你快速掌握核心要点。</p>",
            f"<p>最近很多朋友在问关于{title}的问题。为了让大家少走弯路，我花了大量时间研究整理了这份完整的指南，建议点赞收藏，方便以后查阅。</p>",
            f"<p>2026年，AI已经渗透到我们生活的方方面面。今天我们来聊聊{title}这个话题，内容很干货，相信对你一定有帮助。</p>",
        ]
        return random.choice(intros)

    def _generate_section(self, title):
        h2_texts = [
            f"<h2>为什么{title}如此重要？</h2>",
            f"<h2>{title}的核心要点</h2>",
            f"<h2>深度解析：{title}</h2>",
        ]
        body_texts = [
            "<p>根据最新的行业数据显示，AI领域的用户规模正在以惊人的速度增长。掌握这些知识和工具，不仅能提升个人效率，更能为职业发展和副业收入创造新的可能性。</p><p>在深入研究后，我发现普通人往往低估了这些工具的潜力。实际上，只要掌握了正确的使用方法，效果会超出你的想象。</p>",
            "<p>经过大量的测试和对比分析，我得出了以下几个关键结论。这些结论基于真实的用户体验和数据反馈，具有很高的参考价值。</p><p>首先，工具的选取非常重要。市面上的AI工具层出不穷，每一款都有自己的特点和适用场景。了解它们的差异，是高效使用的第一步。</p>",
            "<p>很多人在使用AI工具时，往往会遇到效果不佳的问题。其实问题的关键不在于工具本身，而在于使用的方法和技巧。下面我分享几个经过验证的有效策略。</p><p>这些策略来自多个领域的实践总结，覆盖了从入门到精通的各个阶段。</p>",
        ]
        return f"{random.choice(h2_texts)}{random.choice(body_texts)}"

    def _generate_detail(self):
        h2 = random.choice([
            "<h2>具体操作指南</h2>",
            "<h2>实用技巧分享</h2>",
            "<h2>上手实操步骤</h2>",
        ])
        
        steps = []
        for i in range(1, random.randint(4, 7)):
            step_title = random.choice([
                f"明确你的目标和需求",
                f"选择合适的工具和平台",
                f"掌握基础操作方法",
                f"建立自己的工作流程",
                f"持续优化和迭代",
                f"扩展应用到更多场景",
                f"与他人交流分享经验",
                f"关注行业最新动态",
            ])
            step_detail = random.choice([
                f"在开始之前，先想清楚你想要达成的具体目标。目标越明确，执行起来效率越高。建议把目标写下来，量化成可衡量的指标。",
                f"这一步很关键。市面上的选择很多，根据上一步确定的需求来筛选，不要盲目追求功能最全的，适合的才是最好的。",
                f"不要急于求成，先从最基础的功能开始熟悉。建议每天花15-30分钟，持续练习一周，基本就能上手了。",
                f"把常用的操作流程化、模板化，可以大幅提升效率。好的工作流程应该是可复制、可优化的。",
                f"没有一劳永逸的方案。定期回顾你的使用效果，找出可以改进的地方，持续优化你的方法。",
                f"当你熟练掌握基础用法后，尝试将这个方法应用到其他类似的场景中，举一反三，效果会更好。",
            ])
            steps.append(f"<h3>第{i}步：{step_title}</h3><p>{step_detail}</p>")

        return f"{h2}{''.join(steps)}"

    def _generate_affiliate_section(self, title):
        """联盟推广区域"""
        ads = [
            '<div class="affiliate-box">'
            '<div><strong>💡 推荐工具：AI效率工具箱</strong><br>'
            '<span style="font-size:0.9em;color:#666;">收录了50+精选AI工具的使用指南和提示词模板，助你快速上手</span></div>'
            '<a href="#" class="btn" onclick="alert(\'请替换为你的推广链接\')">立即获取 →</a>'
            '</div>',
            '<div class="affiliate-box">'
            '<div><strong>📚 推荐资源：AI赚钱实操指南</strong><br>'
            '<span style="font-size:0.9em;color:#666;">从零开始教你用AI变现，包含20+实操案例和详细步骤</span></div>'
            '<a href="#" class="btn" onclick="alert(\'请替换为你的推广链接\')">了解详情 →</a>'
            '</div>',
        ]
        content = [
            f"<p在阅读完整篇文章后，相信你对{title}有了更深入的了解。如果你还想进一步提升效率，下面这个工具/资源推荐给你——</p>",
            f"<p>如果你觉得这篇文章有帮助，想更进一步系统地学习，不妨看看我为你准备的这份资源——</p>",
        ]
        return f"{random.choice(content)}{random.choice(ads)}"

    def _generate_conclusion(self):
        h2 = random.choice([
            "<h2>总结</h2>",
            "<h2>写在最后</h2>",
        ])
        texts = [
            "<p>AI技术每天都在进步，今天的分享只是冰山一角。核心思路是：不要把AI想得太复杂，把它当成一个强大的助手，关键是学会如何正确地给它下达指令。</p><p>如果你在实操过程中遇到任何问题，欢迎在评论区留言交流。我会定期整理大家的问题，出后续的解答文章。</p>",
            "<p>掌握了这些方法，你就已经领先了大多数人。剩下的就是坚持实践、不断优化。记住，AI只是工具，真正创造价值的是使用工具的人。</p><p>如果你觉得这篇文章对你有帮助，请点赞收藏并分享给需要的朋友。你的支持是我持续创作的动力！</p>",
            "<p>2026年是AI全面普及的一年，现在开始行动一点都不晚。希望这篇文章能为你提供一些有价值的参考和启发。</p><p>关注我，每天分享AI实用技巧和前沿资讯，让我们一起在AI时代抓住机会！</p>",
        ]
        return f"{h2}{random.choice(texts)}"

    def _generate_interaction(self):
        return random.choice([
            '<div style="background:#f0f4ff;border-radius:8px;padding:20px;margin-top:24px;">'
            '<p style="margin:0;text-indent:0;"><strong>💬 互动话题：</strong>你对AI领域最感兴趣的是什么？欢迎在评论区告诉我，我会根据大家的反馈出更多相关内容！</p></div>',
            '<div style="background:#f0f4ff;border-radius:8px;padding:20px;margin-top:24px;">'
            '<p style="margin:0;text-indent:0;"><strong>📢 觉得有用？</strong> 点个赞支持一下，让更多人看到！关注我获取每日AI实用内容推送 🚀</p></div>',
        ])

    def _extract_excerpt(self, html):
        """从HTML中提取纯文本摘要"""
        import re
        text = re.sub(r'<[^>]+>', '', html)
        text = text.replace('\n', ' ').strip()
        return text[:200]


if __name__ == "__main__":
    gen = AIContentGenerator()
    new = gen.generate_batch(5)
    print(f"✅ 成功生成 {len(new)} 篇文章：")
    for a in new:
        print(f"  📄 [{a['category']}] {a['title']} ({a['date']})")
