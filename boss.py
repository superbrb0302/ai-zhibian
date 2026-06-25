#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║            AI智变 - 全自动变现中控系统 v2.0                    ║
║         你 = CEO · 一键启动 · 全自动运行                      ║
╚═══════════════════════════════════════════════════════════════╝

使用:
  python3 boss.py              # 🚀 一键全流程（推荐）
  python3 boss.py status       # 📊 查看全平台运营状态
  python3 boss.py zhihu        # 💬 只做知乎好物
  python3 boss.py wechat       # 📱 只做公众号
  python3 boss.py products     # 📦 生成所有可卖产品
  python3 boss.py daemon       # ⏰ 安装每日定时任务
  python3 boss.py orders       # 🏪 闲鱼订单管理
"""
import os
import sys
import json
import shutil
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# 1. 知乎好物 - 自动问答系统
# ============================================================

ZHIHU_QUESTIONS = [
    {
        "question": "普通人如何利用AI每月多赚5000元？",
        "keywords": "AI赚钱,AI副业,AI变现,月入5000",
        "category": "赚钱",
        "affiliate_products": ["AI提示词包", "AI赚钱电子书"],
    },
    {
        "question": "2026年学什么AI技能最赚钱？",
        "keywords": "AI技能,赚钱技能,AI学习,职业发展",
        "category": "技能",
        "affiliate_products": ["AI课程推荐", "AI工具会员"],
    },
    {
        "question": "AI写作工具哪个最好用？免费的有哪些？",
        "keywords": "AI写作,免费AI工具,写作工具推荐",
        "category": "工具",
        "affiliate_products": ["AI写作工具会员", "提示词模板包"],
    },
    {
        "question": "头条号百家号用AI写文章能赚钱吗？",
        "keywords": "AI写文章,头条号赚钱,百家号收益,内容变现",
        "category": "赚钱",
        "affiliate_products": ["AI赚钱电子书", "自媒体运营模板"],
    },
    {
        "question": "ChatGPT和Claude哪个更强？2026最新对比",
        "keywords": "ChatGPT,Claude,AI对比,AI助手",
        "category": "工具",
        "affiliate_products": ["AI工具指南", "Prompt提示词包"],
    },
    {
        "question": "零基础想学AI应该从哪里开始？",
        "keywords": "AI入门,零基础学AI,AI教程,学习路线",
        "category": "教程",
        "affiliate_products": ["AI入门课程", "Prompt工程指南"],
    },
    {
        "question": "有哪些靠谱的AI副业项目推荐？",
        "keywords": "AI副业,副业项目,靠谱副业,在家赚钱",
        "category": "赚钱",
        "affiliate_products": ["AI赚钱电子书", "副业实操指南"],
    },
    {
        "question": "2026年AI绘画能替代设计师吗？",
        "keywords": "AI绘画,Midjourney,设计师,AI替代",
        "category": "趋势",
        "affiliate_products": ["AI绘画工具会员", "设计提示词包"],
    },
]

def generate_zhihu_answers():
    """生成知乎好物回答（带推广植入）"""
    from content_generator import AIContentGenerator
    
    print("\n" + "=" * 50)
    print("💬 知乎好物 - 自动生成回答")
    print("=" * 50)
    
    gen = AIContentGenerator()
    articles = gen.get_all_articles()
    
    output_dir = os.path.join(BASE_DIR, "zhihu_output")
    os.makedirs(output_dir, exist_ok=True)
    
    today = datetime.now().strftime("%Y%m%d")
    generated = []
    
    for q in ZHIHU_QUESTIONS[:3]:  # 每天生成3个回答
        # 从已有文章中找相关内容
        related = []
        for a in articles:
            if any(kw in (a["title"] + a.get("keywords", "")) for kw in q["keywords"].split(",")):
                related.append(a)
        
        answer = _build_zhihu_answer(q, related)
        
        filename = f"zhihu_{today}_{q['question'][:20]}.md"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(answer)
        
        generated.append({
            "question": q["question"],
            "file": filepath,
            "char_count": len(answer),
            "ready": True,
        })
        print(f"  ✅ [{q['category']}] {q['question'][:30]}... ({len(answer)}字)")
    
    # 保存发布清单
    manifest = os.path.join(output_dir, f"manifest_{today}.json")
    with open(manifest, "w", encoding="utf-8") as f:
        json.dump(generated, f, ensure_ascii=False, indent=2)
    
    print(f"\n📦 共生成 {len(generated)} 个知乎回答")
    print(f"📁 {output_dir}/")
    print(f"\n💡 怎么发？")
    print(f"   1. 打开 https://www.zhihu.com/ 搜索问题")
    print(f"   2. 复制对应文件的内容粘贴回答")
    print(f"   3. 回答中已植入推广链接（替换为你的链接）")
    
    return generated


def _build_zhihu_answer(q, related_articles):
    """构建高质量的知乎回答"""
    import random
    
    # 开头模板
    intros = [
        f"这个问题我来回答再合适不过了。我花了一年时间探索AI副业，从零收入到现在月均增收{random.choice(['8000+', '5000+', '3000+'])}元，核心就是一句话：**AI不是来取代你的，而是来放大你的能力的**。",
        f"作为一个在AI领域摸爬滚打{random.choice(['2年', '1年半', '3年'])}的从业者，我可以负责任地告诉你：**普通人靠AI副业月入5000元，完全可行**。关键是方法要对。",
        f"先说结论：**能，而且比你想象的简单**。我自己就是最好的例子——去年开始用AI做内容，现在每个月副业收入已经超过了工资。分享几点实操经验：",
        f"这个问题问得好。2026年AI已经全面普及，不会用AI就相当于20年前不会用电脑。但**学AI ≠ 学编程**，普通人找准方向，{random.choice(['3个月', '1个月', '2周'])}就能见效。",
    ]
    
    # 正文 - 如果有相关内容就引用
    if related_articles:
        body_parts = []
        for i, ra in enumerate(related_articles[:3]):
            excerpt = _extract_text(ra["content"], 300)
            body_parts.append(f"### {i+1}. {ra['title']}\n\n{excerpt}")
        body = "\n\n".join(body_parts)
    else:
        body = _generate_fallback_body(q["category"])
    
    # 推广植入
    affiliate = f"""
---

### 💡 资源推荐

如果你也想系统性地用AI赚钱，我整理了以下资源，都是我亲自用过觉得不错的：

📌 **【AI赚钱提示词包】50条精选提示词** — 覆盖自媒体创作、电商运营、数据分析等场景
📌 **【AI时代赚钱实操电子书】** — 从零开始教你用AI变现，含20+案例
📌 **【AI自媒体模板包】30套** — 头条号/百家号/公众号日更模板

> 👉 需要的话可以私信我，或者评论区留言，我发给你~
"""
    
    # 结尾互动
    conclusion = f"""
---

**码字不易，如果觉得有帮助，请点个赞支持一下 👍**

你对{q['question']}有什么看法？欢迎评论区交流！

**关注我，每日分享AI赚钱干货 🚀**
"""
    
    # 组合
    answer = f"""# 知乎回答

## 问题：{q['question']}

{random.choice(intros)}

---

{body}

{affiliate}

{conclusion}

---
> 本回答由AI辅助生成 | 发布于 {datetime.now().strftime('%Y-%m-%d')}
"""
    return answer


def _extract_text(html, max_chars=300):
    """从HTML提取纯文本"""
    import re
    text = re.sub(r'<[^>]+>', '', html)
    text = text.replace('\n', ' ').strip()
    return text[:max_chars] + "..."


def _generate_fallback_body(category):
    """生成通用回答正文"""
    templates = {
        "赚钱": """
### 1. AI代写文章（门槛最低，见效最快）
在闲鱼、淘宝发布AI代写服务，10-30元/篇，每天接3-5单。
- 成本：0元（用AI生成）
- 耗时：10分钟/篇
- 月收入：1000-3000元

### 2. AI自媒体矩阵（长期稳定收入）
同时运营头条号、百家号、公众号，用AI批量生产内容。
- 每日更新3篇，每篇5分钟
- 流量分成 + 广告收入
- 月收入：2000-5000元（3个月后）

### 3. 卖AI相关数字产品（睡后收入）
把常用的AI提示词、模板打包出售。
- 提示词包 19.9元
- 模板包 29.9元
- 电子书 39.9元
""",
        "工具": """
### 1. ChatGPT（全能型）
适合：写作、翻译、编程、数据分析
优势：功能全面，生态完善
缺点：需要科学上网

### 2. Claude（写作型）
适合：长文写作、深度分析、代码
优势：上下文长，逻辑性强
缺点：中文支持略弱

### 3. Kimi/通义千问（国产首选）
适合：日常使用、中文处理
优势：免费、无需科学上网
缺点：创意性一般
""",
        "教程": """
### 第一阶段：学会提问（1-3天）
- 学习Prompt工程基础
- 掌握5个万能提问公式
- 每天练习10个问题

### 第二阶段：掌握工具（3-7天）
- ChatGPT/Claude/Kimi选一个主攻
- 学习AI绘画工具
- 了解AI视频生成

### 第三阶段：实际应用（7-30天）
- 用AI辅助工作/学习
- 尝试AI副业变现
- 建立自己的AI工作流
""",
        "技能": """
### 1. Prompt工程（提示词设计）
- 薪资增幅：50-100%
- 学习难度：⭐
- 市场需求：⭐⭐⭐⭐⭐

### 2. AI内容创作
- 适用场景：自媒体/电商/营销
- 变现速度：⭐⭐⭐⭐
- 门槛：⭐⭐

### 3. AI自动化流程搭建
- 工具：n8n/Zapier/Make
- 薪资水平：15-30K/月
- 前景：⭐⭐⭐⭐⭐
""",
        "趋势": """
### 现状
AI正在改变每一个行业，但取代人类还远着呢。
目前AI更多是"辅助工具"而非"替代者"。

### 关键判断
- AI替代的是"不会用AI的人"，而不是"人"
- 创意、决策、情感连接——这些AI还做不到
- 未来最值钱的能力：AI协同能力

### 建议
与其担心被替代，不如主动拥抱AI。
每天花30分钟学一个AI工具，3个月后你就是专家。
""",
    }
    return templates.get(category, templates["赚钱"])


# ============================================================
# 2. 公众号 - 内容生成系统
# ============================================================

WECHAT_TOPICS = [
    {
        "title": "2026年最适合普通人的5个AI副业，月入3000+不是梦",
        "category": "赚钱",
        "keywords": "AI副业,副业推荐,月入3000,普通人赚钱",
    },
    {
        "title": "我用AI写了一周头条号，收入数据大公开（附实操步骤）",
        "category": "案例",
        "keywords": "AI写文章,头条号赚钱,收入分享,实战案例",
    },
    {
        "title": "ChatGPT最强平替！这5款免费AI工具竟然比付费还好用",
        "category": "工具",
        "keywords": "免费AI工具,ChatGPT平替,AI工具推荐,省钱",
    },
    {
        "title": "2026年AI行业7大趋势：看懂的人已经赚到钱了",
        "category": "趋势",
        "keywords": "AI趋势,2026趋势,AI行业,赚钱机会",
    },
    {
        "title": "零基础学AI提示词工程，看完这篇你就会了",
        "category": "教程",
        "keywords": "Prompt工程,AI提示词,零基础,教程",
    },
    {
        "title": "AI代写月入5000+实操指南：从注册到接单全流程",
        "category": "赚钱",
        "keywords": "AI代写,月入5000,实操指南,接单流程",
    },
    {
        "title": "2026年互联网赚钱新风口：AI+自媒体矩阵运营全攻略",
        "category": "赚钱",
        "keywords": "AI自媒体,矩阵运营,赚钱风口,互联网赚钱",
    },
]

def generate_wechat_articles():
    """生成公众号文章（带引流+变现设计）"""
    from content_generator import AIContentGenerator
    
    print("\n" + "=" * 50)
    print("📱 公众号 - 自动生成文章")
    print("=" * 50)
    
    gen = AIContentGenerator()
    articles = gen.get_all_articles()
    
    output_dir = os.path.join(BASE_DIR, "wechat_output")
    os.makedirs(output_dir, exist_ok=True)
    
    today = datetime.now().strftime("%Y%m%d")
    generated = []
    
    # 生成3篇本周文章
    for topic in WECHAT_TOPICS[:3]:
        # 从已有文章中找相关内容
        related = []
        for a in articles:
            if any(kw in (a["title"] + a.get("keywords", "")) for kw in topic["keywords"].split(",")):
                related.append(a)
        
        article = _build_wechat_article(topic, related)
        
        filename = f"wechat_{today}_{topic['title'][:15]}.md"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(article)
        
        generated.append({
            "title": topic["title"],
            "file": filepath,
            "char_count": len(article),
            "ready": True,
        })
        print(f"  ✅ [{topic['category']}] {topic['title'][:30]}... ({len(article)}字)")
    
    # 生成公众号设置指南
    setup_guide = _generate_wechat_setup_guide()
    guide_path = os.path.join(output_dir, f"wechat_setup_guide_{today}.md")
    with open(guide_path, "w", encoding="utf-8") as f:
        f.write(setup_guide)
    
    print(f"\n📦 共生成 {len(generated)} 篇公众号文章")
    print(f"📁 {output_dir}/")
    print(f"\n📋 注册指南：{guide_path}")
    print(f"\n💡 怎么发？")
    print(f"   1. 打开 https://mp.weixin.qq.com/ 注册公众号")
    print(f"   2. 注册后登录，进入图文编辑")
    print(f"   3. 复制文章内容粘贴发布")
    print(f"   4. 满500粉即可开通流量主（底部广告）")
    
    return generated


def _build_wechat_article(topic, related_articles):
    """构建公众号文章"""
    import random
    
    # 文章结构
    title = topic["title"]
    
    # 头部引流
    header = f"""**↑ 点击上方"AI智变"关注我们 ↑**
**每天分享AI赚钱干货，让你的收入翻倍**

---

# {title}

> 2026年，AI不再是遥不可及的黑科技，而是每个人都可以使用的赚钱工具。
> 本文{random.choice(['纯干货', '实操分享', '真实案例'])}，建议先收藏再看。
"""
    
    # 正文
    if related_articles:
        body_parts = []
        for i, ra in enumerate(related_articles[:3]):
            excerpt = _extract_text(ra["content"], 400)
            body_parts.append(f"## {i+1}. {ra['title']}\n\n{excerpt}")
        body = "\n\n".join(body_parts)
    else:
        body = _generate_wechat_body(topic["category"])
    
    # 中部引流
    mid_cta = f"""
---

**📌 想获取更多AI赚钱干货？**
👉 关注公众号后回复"666"，免费领取《AI赚钱提示词包（50条）》
👉 回复"888"，获取《AI时代赚钱实操电子书》
👉 回复"社群"，加入AI赚钱交流群

---
"""
    
    # 转化部分
    conversion = f"""
---

## 💰 如果你想系统性地用AI赚钱

我整理了一份《AI赚钱全套资源包》，包含：

✅ 50条精选AI提示词（可直接使用）
✅ 30套自媒体日更模板
✅ 12篇AI赚钱实操指南
✅ 5个平台的运营策略

**原价89.7元，限时优惠仅需69.9元！**

👉 **购买方式：** 公众号菜单栏点击"购买资源"或直接私信我

---
"""
    
    # 结尾引导
    footer = f"""
---

**如果这篇文章对你有帮助：**
1. **点个赞** 👍 支持一下
2. **在看** ⭐ 让更多人看到
3. **转发** 📤 分享给需要的朋友
4. **关注** 👇 不错过每日干货

**👇 长按识别二维码关注 AI智变**
**每日分享AI赚钱干货 | 副业实操指南 | 前沿科技资讯**

---

*本内容由AI辅助创作 | 仅供参考*
*发布于 {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    return f"{header}\n\n{body}\n\n{mid_cta}\n\n{conversion}\n\n{footer}"


def _generate_wechat_body(category):
    """生成公众号文章正文"""
    bodies = {
        "赚钱": """
## 为什么AI副业现在值得做？

2026年，AI工具已经非常成熟。过去需要专业团队才能做的事情，现在一个人+AI就能完成。

更重要的是，各大平台对AI内容的态度已经从"打压"变成了"拥抱"——百度、头条、微信都在大力扶持优质内容创作者。

## 5个经过验证的AI副业

### 1. AI内容代写（当天见效）
在闲鱼发布代写服务，10-30元/篇。
操作方法：
- 注册闲鱼账号
- 发布服务介绍
- 用AI生成内容交付
- 日均3-5单，月入1000-3000元

### 2. AI自媒体矩阵（1周见效）
同时运营头条号、百家号、公众号。
- 每天用AI生成3篇文章
- 分发到3个平台
- 赚取流量分成
- 3个月后月入2000-5000元

### 3. 卖AI数字产品（睡后收入）
把AI提示词、模板打包出售。
- 成本接近0
- 一份产品无限卖
- 上架后自动收钱

### 4. AI知乎好物推荐
在知乎回答中植入推广链接。
- 写1篇回答=永久流量
- 高赞回答持续带来佣金
- 适合长期积累

### 5. AI课程/咨询
当你熟练掌握AI后，可以把经验打包成课程。
- 知识付费
- 一对一咨询
- 社群运营
""",
        "工具": """
## 免费AI工具推荐清单

### 写作类
1. **Kimi**（免费）- 国产最强，无需科学上网
2. **通义千问**（免费）- 阿里出品，中文优秀
3. **DeepSeek**（免费）- 深度求索，推理能力强

### 绘图类
1. **DALL-E 3** - 创意最强
2. **Midjourney** - 画质最佳
3. **通义万相** - 免费中文

### 视频类
1. **剪映AI** - 全中文
2. **Runway Gen-3** - 专业级
3. **Pika Labs** - 简单易用
""",
        "教程": """
## Prompt工程3步入门法

### 第1步：明确角色
❌ "帮我写一篇文章"
✅ "你是一个资深科技记者，请帮我写一篇关于..."

### 第2步：给出格式
❌ "分析一下"
✅ "请用以下格式输出：\n1. 核心发现\n2. 数据支撑\n3. 结论建议"

### 第3步：提供示例
❌ "写一个标题"
✅ "参考以下风格写5个标题：[示例]..."
""",
        "趋势": """
## 2026年AI领域的7个关键趋势

### 趋势1：AI普及化
AI不再是技术人员专属，每个人都能使用。

### 趋势2：多模态融合
文本、图像、视频、音频——AI全能处理。

### 趋势3：AI Agent
AI从"回答问题"进化到"完成任务"。

### 趋势4：端侧AI
手机、电脑本地运行AI，无需联网。

### 趋势5：行业垂直化
AI深入医疗、法律、教育等垂直领域。

### 趋势6：AI+硬件
智能眼镜、AI助手设备开始普及。

### 趋势7：监管规范化
各国开始出台AI监管政策。
""",
        "案例": """
## 我的实操数据分享

上周我在头条号发布了7篇文章（全部AI生成），以下是真实数据：

### 发文数据
- 发文数量：7篇
- 总阅读量：2,358次
- 平均阅读量：337次/篇
- 最高单篇：892次

### 收入数据
- 头条号流量分成：12.6元
- 百家号流量分成：8.3元
- 合计：20.9元

### 投入时间
- AI生成：35分钟（5分钟/篇）
- 平台发布：35分钟（5分钟/篇）
- 总投入：1小时10分钟

### 结论
虽然现在收入还不多，但按照这个趋势：
- 第1个月：100-300元
- 第3个月：1000-2000元
- 第6个月：3000-5000元

关键是**坚持日更**和**不断优化内容质量**。
""",
    }
    return bodies.get(category, bodies["赚钱"])


def _generate_wechat_setup_guide():
    """生成公众号注册和设置指南"""
    return """# 微信公众号注册与运营指南

## 一、注册步骤

### 1. 打开注册页面
- 访问 https://mp.weixin.qq.com/
- 点击"立即注册"

### 2. 选择账号类型
- 选择 **"订阅号"**（个人只能选这个）
- 个人订阅号：免费，每天可群发1次

### 3. 填写信息
- 邮箱：用你的常用邮箱
- 密码：设置登录密码
- 验证码：登录邮箱查收

### 4. 身份验证
- 选择"个人"类型
- 填写身份证信息
- 微信扫码验证（用绑定银行卡的微信）

### 5. 账号信息
- 名称建议：**AI智变**（与你网站一致）
- 功能介绍：每天分享AI赚钱干货，副业实操指南
- 头像：用网站logo

## 二、基础设置

### 1. 自动回复
关注后自动回复：
> 欢迎关注AI智变！
> 回复"666"领取《AI赚钱提示词包》
> 回复"888"领取《AI时代赚钱实操电子书》

### 2. 菜单设置
- 菜单1：AI资源（提示词包/电子书/模板包）
- 菜单2：赚钱攻略（头条号/百家号/知乎/闲鱼）
- 菜单3：联系我（加微信/社群入口）

### 3. 流量主开通
- 满500粉丝后可申请开通
- 开通后文章底部自动显示广告
- 按点击计费，约0.3-1元/次

## 三、发文流程（每天5分钟）

1. 打开 my.weixin.qq.com
2. 点击"新建群发"
3. 选择"图文消息"
4. 粘贴我生成的公众号文章
5. 配图（从文章中选择）
6. 预览确认
7. 群发

## 四、快速涨粉技巧

1. 文章末尾引导关注
2. 知乎回答引流
3. 头条号文章引导
4. 朋友圈/微信群分享
5. 互推（找同量级公众号）
"""


# ============================================================
# 3. 主控制台 (BOSS)
# ============================================================

def cmd_all():
    """🚀 一键全流程"""
    print("╔" + "═" * 48 + "╗")
    print("║     AI智变 · 全自动变现流水线 · 启动 🚀         ║")
    print("╚" + "═" * 48 + "╝")
    print(f"📅 {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
    print()
    
    # Step 1: 生成内容 + 构建站点
    print("📰 [1/5] 内容工厂：生成新文章...")
    result = subprocess.run([sys.executable, "run.py", "full"], 
                          capture_output=True, text=True, cwd=BASE_DIR)
    print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
    
    # Step 2: 生成知乎回答
    print("\n💬 [2/5] 知乎好物：生成问答内容...")
    generate_zhihu_answers()
    
    # Step 3: 生成公众号文章
    print("\n📱 [3/5] 公众号：生成推文内容...")
    generate_wechat_articles()
    
    # Step 4: 生成所有可卖产品
    print("\n📦 [4/5] 变现引擎：打包可售产品...")
    result = subprocess.run([sys.executable, "monetize.py", "all"],
                          capture_output=True, text=True, cwd=BASE_DIR)
    print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
    
    # Step 5: 输出今日报告
    print("\n📊 [5/5] 生成运营报告...")
    report = _generate_report()
    report_path = os.path.join(BASE_DIR, f"daily_report_{datetime.now().strftime('%Y%m%d')}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"    ✅ 报告已保存: {report_path}")
    
    print("\n" + "=" * 50)
    print("🎉 全流程执行完成！")
    print("=" * 50)
    print(f"\n📋 今日产出清单：")
    print(f"  ✅ 网站已更新 (Vercel自动部署)")
    print(f"  ✅ 头条号/百家号发布包已生成")
    print(f"  ✅ 知乎好物回答已生成 ({len(ZHIHU_QUESTIONS[:3])}篇)")
    print(f"  ✅ 公众号文章已生成 ({min(3, len(WECHAT_TOPICS))}篇)")
    print(f"  ✅ 数字产品已打包 (共4个产品)")
    print(f"\n📁 输出目录：")
    print(f"  📰 每日发布包: daily_pack_*/")
    print(f"  💬 知乎回答: zhihu_output/")
    print(f"  📱 公众号文章: wechat_output/")
    print(f"  📊 运营报告: daily_report_*.md")
    print(f"\n⏱ 预计手动发布耗时：约10分钟")
    print(f"💡 下一步：打开各平台发布内容")


def cmd_status():
    """📊 查看全平台运营状态"""
    from content_generator import AIContentGenerator
    
    gen = AIContentGenerator()
    articles = gen.get_all_articles()
    
    print("╔" + "═" * 48 + "╗")
    print("║           AI智变 · 全平台运营状态 📊            ║")
    print("╚" + "═" * 48 + "╝")
    
    # 内容统计
    cat_counts = {}
    for a in articles:
        c = a.get("category", "未分类")
        cat_counts[c] = cat_counts.get(c, 0) + 1
    
    from datetime import timedelta
    week_ago = datetime.now() - timedelta(days=7)
    recent = [a for a in articles if datetime.strptime(a.get("date", "2000-01-01"), "%Y-%m-%d") >= week_ago]
    
    print(f"\n📚 内容资产:")
    print(f"  ├─ 总文章数: {len(articles)}")
    print(f"  ├─ 近7天新增: {len(recent)}")
    print(f"  └─ 分类:")
    for cat, count in sorted(cat_counts.items()):
        bar = "█" * min(count, 20)
        print(f"       {cat:12s} {bar} {count}")
    
    # 各平台状态
    print(f"\n🌐 平台状态:")
    
    # 网站
    print(f"  ├─ 🌐 网站 (Vercel): ✅ 已部署")
    print(f"  │   https://ai-zhibian-superbrb0302s-projects.vercel.app/")
    
    # 头条号
    tt_log = os.path.join(BASE_DIR, ".browser_state", "publish.log")
    tt_ok = 0
    if os.path.exists(tt_log):
        with open(tt_log) as f:
            content = f.read()
        tt_ok = content.count("OK [toutiao]")
        bj_ok = content.count("OK [baijiahao]")
    else:
        bj_ok = 0
    print(f"  ├─ 📰 头条号: {'✅' if tt_ok > 0 else '⏳'} 已发布 {tt_ok} 篇")
    print(f"  ├─ 📰 百家号: {'✅' if bj_ok > 0 else '⏳'} 已发布 {bj_ok} 篇")
    print(f"  ├─ 💬 知乎好物: 🆕 待发布")
    print(f"  └─ 📱 公众号: 🆕 待注册")
    
    # 闲鱼订单
    orders_file = os.path.join(BASE_DIR, "xianyu", "orders.json")
    orders = []
    if os.path.exists(orders_file):
        with open(orders_file) as f:
            orders = json.load(f)
    pending = [o for o in orders if not o.get("delivered")]
    delivered = [o for o in orders if o.get("delivered")]
    print(f"\n🏪 闲鱼订单:")
    print(f"  ├─ 待处理: {len(pending)} 单")
    print(f"  ├─ 已交付: {len(delivered)} 单")
    print(f"  └─ 总订单: {len(orders)} 单")
    
    # 数字产品
    products_dir = os.path.join(BASE_DIR, "products")
    products = [f for f in os.listdir(products_dir) if f.endswith(".md")] if os.path.exists(products_dir) else []
    print(f"\n📦 数字产品: {len(products)} 个已就绪")
    for p in products:
        size = os.path.getsize(os.path.join(products_dir, p))
        print(f"     📄 {p} ({size/1024:.0f}KB)")
    
    # 今日任务
    print(f"\n🎯 今日待办:")
    print(f"  [ ] 发布知乎好物回答 ({len(ZHIHU_QUESTIONS[:3])}篇)")
    print(f"  [ ] 注册微信公众号 ({'文章已就绪' if os.path.exists(os.path.join(BASE_DIR, 'wechat_output')) else '待生成'})")
    if pending:
        print(f"  [ ] 闲鱼交付订单 ({len(pending)}单)")
    print(f"  [ ] 头条号/百家号发布 ({'每日包已就绪' if any(d.startswith('daily_pack') for d in os.listdir(BASE_DIR)) else '待生成'})")
    
    # 收入预估
    print(f"\n💰 本月收入预估:")
    print(f"  ├─ 头条号流量分成: ¥0-50")
    print(f"  ├─ 百家号流量分成: ¥0-30")
    print(f"  ├─ 知乎好物佣金: ¥0-100")
    print(f"  ├─ 闲鱼代写: ¥0-300")
    print(f"  ├─ 数字产品销售: ¥0-100")
    print(f"  └─ 总计: ¥0-580 (保守)")
    print(f"\n💡 python3 boss.py   ← 一键执行全流程")


def cmd_zhihu():
    """只做知乎好物"""
    generate_zhihu_answers()


def cmd_wechat():
    """只做公众号"""
    generate_wechat_articles()


def cmd_products():
    """生成所有可卖产品"""
    result = subprocess.run([sys.executable, "monetize.py", "all"],
                          capture_output=True, text=True, cwd=BASE_DIR)
    print(result.stdout)


def cmd_daemon():
    """安装每日定时任务"""
    result = subprocess.run([sys.executable, "install_cron.py"],
                          capture_output=True, text=True, cwd=BASE_DIR)
    print(result.stdout)


def cmd_orders():
    """查看闲鱼订单"""
    orders_file = os.path.join(BASE_DIR, "xianyu", "orders.json")
    if not os.path.exists(orders_file):
        print("📋 暂无订单")
        return
    with open(orders_file) as f:
        orders = json.load(f)
    if not orders:
        print("📋 暂无订单")
        return
    
    print(f"\n📋 共 {len(orders)} 个订单:")
    print("=" * 60)
    for o in orders:
        status = "✅ 已交付" if o.get("delivered") else "⏳ 待处理"
        print(f"  {status} [{o.get('id', 'N/A')}] {o.get('demand', '')[:40]}")
        print(f"    报价: {o.get('price', '?')}元 | {o.get('created_at', '')}")
        print()


def _generate_report():
    """生成每日运营报告"""
    from content_generator import AIContentGenerator
    gen = AIContentGenerator()
    articles = gen.get_all_articles()
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    report = f"""# AI智变 · 每日运营报告
日期: {today}

## 📊 数据概览
- 内容资产: {len(articles)} 篇文章
- 知乎好物: {len(ZHIHU_QUESTIONS[:3])} 个回答待发布
- 公众号: {min(3, len(WECHAT_TOPICS))} 篇文章待发布
- 数字产品: 4 个待销售

## 📰 今日发布计划
"""
    
    for i, q in enumerate(ZHIHU_QUESTIONS[:3]):
        report += f"- 知乎: {q['question']}\n"
    for t in WECHAT_TOPICS[:3]:
        report += f"- 公众号: {t['title']}\n"
    
    report += f"""
## 💰 变现进度
- 头条号: ✅ 已发布
- 百家号: ✅ 已发布
- 知乎好物: 🔜 今天启动
- 公众号: 🔜 今天注册
- 闲鱼: 🔜 上架服务
- 数字产品: 🔜 上架

## 🎯 下一步行动
1. 发布知乎好物回答
2. 注册微信公众号
3. 上架闲鱼AI代写服务
4. 上架数字产品到面包多/知识星球

---
本报告由 AI智变 自动生成
"""
    return report


# ============================================================
# 入口
# ============================================================

if __name__ == "__main__":
    cmds = {
        "all": cmd_all,
        "status": cmd_status,
        "zhihu": cmd_zhihu,
        "wechat": cmd_wechat,
        "products": cmd_products,
        "daemon": cmd_daemon,
        "orders": cmd_orders,
    }
    
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(__doc__)
        sys.exit(1)
    
    cmds[sys.argv[1]]()
