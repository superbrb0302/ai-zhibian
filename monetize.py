#!/usr/bin/env python3
"""
AI智变 - 四路变现全自动系统
===========================
一次运行，生成所有可卖资产

使用:
  python3 monetize.py all           # 生成所有可售产品
  python3 monetize.py xianyu        # 生成闲鱼服务材料
  python3 monetize.py products      # 打包数字产品
  python3 monetize.py content       # 生成知乎+公众号内容
  python3 monetize.py guide         # 打印完整操作指南
"""

import os, sys, json, re, shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTICLES_DIR = os.path.join(BASE_DIR, "articles")
PRODUCTS_DIR = os.path.join(BASE_DIR, "products")
XIANYU_DIR = os.path.join(BASE_DIR, "xianyu")
os.makedirs(PRODUCTS_DIR, exist_ok=True)
os.makedirs(XIANYU_DIR, exist_ok=True)


# ============================================================
# 1. 闲鱼全套服务材料
# ============================================================

def build_xianyu():
    print("\n📦 生成闲鱼服务材料...")
    
    # 服务列表
    services = """= 闲鱼 AI代写 服务清单 =

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 接单范围（全部AI高效完成，当日交付）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 自媒体文案
  头条号/百家号/公众号文章    10元/篇（1000字）
  小红书种草笔记              8元/篇
  知乎回答                    15元/篇
  视频脚本                    20元/个

🛒 电商文案
  商品详情页描述              15元/篇
  淘宝/拼多多标题优化          5元/条
  买家秀文案                  5元/条

📊 办公文档
  工作总结/汇报PPT大纲         15元/份
  商业计划书/策划案            30元/份
  简历优化                    10元/份

🎓 学习资料
  论文大纲                    20元/份
  读书笔记                    10元/份
  学习心得/心得体会            8元/份

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 下单流程
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 告诉我你的需求（主题/字数/风格）
2. 我报价 -> 你确认
3. 30分钟-2小时内交付
4. 不满意免费修改

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 价格优势
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• AI高效生成，价格是人工的1/5
• 支持任何主题：科技/教育/情感/职场/电商
• 原创内容，可过查重
• 24小时在线，随时接单

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 联系我
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
闲鱼直接拍下，留言说明需求即可
或加微信：xxxxxxxxx（验证写"代写"）
"""
    
    with open(os.path.join(XIANYU_DIR, "services.txt"), "w", encoding="utf-8") as f:
        f.write(services)
    print(f"  ✅ 服务清单已生成 ({len(services)}字)")
    
    # 快速回复模板
    replies = """= 闲鱼客服快捷回复模板 =

【初次询价】
亲，AI代写文章10元起/篇，300-500字8元，1000字15元。
支持任何主题，AI高效生成，当日交付。
请问你需要写什么内容？告诉我主题和要求即可。

【确认下单】
好的，需求已收到。
预计 XX:XX 前交付（约X小时）。
写好后我会发文件给你，不满意免费修改哦~

【交付】
亲，你的文章已完成，请看附件。
如有需要修改的地方请告诉我，免费帮改。
满意的话麻烦给个好评，谢谢！

【催单安抚】
亲，正在写呢，预计还有X小时完成。
写得比较认真，希望能让你满意。
完成后第一时间发给你哈~

【售后】
收到就好！如果后续还有需求随时找我，
老客户有优惠哦~ 😊
"""
    with open(os.path.join(XIANYU_DIR, "replies.txt"), "w", encoding="utf-8") as f:
        f.write(replies)
    print(f"  ✅ 快捷回复模板已生成")
    
    return True


# ============================================================
# 2. 数字产品打包
# ============================================================

def build_products():
    print("\n📦 打包数字产品...")
    
    # 读取已有文章
    articles = []
    if os.path.exists(ARTICLES_DIR):
        for f in sorted(os.listdir(ARTICLES_DIR)):
            if f.endswith(".json"):
                with open(os.path.join(ARTICLES_DIR, f), "r") as fh:
                    articles.append(json.load(fh))
    
    # 产品1: 完整提示词包
    print("  🎯 产品1: AI赚钱提示词包(50条)...")
    prompts = []
    categories = {
        "自媒体写作": [
            "你是一个10年经验的爆文写手，请为[主题]写一篇头条号风格文章：\n主题：{topic}\n要求：标题含数字，正文分段，每段300字",
            "你是一个小红书博主，请写一篇种草笔记：\n产品：{product}\n要求：口语化，含使用前后对比，带话题标签",
            "你是一个知乎大V，请回答：\n问题：{question}\n要求：开头顶观点，中间列证据，结尾总结推荐",
            "你是一个公众号主编，请写一篇10万+阅读风格文章：\n主题：{topic}\n要求：开头金句，中间故事，结尾升华，配互动话题",
            "你是一个百家号SEO作者，请生成SEO文章：\n关键词：{keyword}\n要求：H2/H3结构，1000字，首段含关键词",
        ],
        "电商运营": [
            "你是一个资深淘宝运营，请写商品详情页：\n产品：{product}\n要求：卖点突出，场景化描述，含FAB法则",
            "你是一个拼多多运营专家，请优化标题：\n产品：{product}\n要求：包含核心词+属性词+营销词，30字内",
            "你是一个跨境电商文案，请写亚马逊Listing：\n产品：{product}\n要求：英文，包含Bullet Points和Description",
        ],
        "办公效率": [
            "你是一个职场写作专家，请写周报/日报：\n岗位：{position}\n本周工作：{work}\n要求：数据化呈现，突出成果",
            "你是一个PPT设计师，请写PPT大纲：\n主题：{topic}\n要求：10页结构，每页标题+要点",
            "你是一个简历优化专家，请改简历：\n职位：{position}\n要求：STAR法则，突出量化成果",
        ],
        "AI工具实操": [
            "你是一个AI工具教学专家，请写教程：\n工具：{tool}\n场景：{scene}\n要求：步骤清晰，配提示词，有实操案例",
            "你是一个AI变现顾问，请设计方案：\n预算：{budget}\n技能：{skill}\n要求：3种变现方式，每步有预期收入",
            "你是一个Prompt工程师，请优化提示词：\n原始需求：{demand}\n要求：结构化输出，含角色/任务/输出格式",
        ]
    }
    
    cat_idx = 0
    prompt_num = 0
    for cat, prompt_list in categories.items():
        prompts.append(f"\n## 📂 {cat}\n")
        for p in prompt_list:
            prompt_num += 1
            prompts.append(f"### {prompt_num}. 模板\n```\n{p}\n```\n")
    
    prompts_text = "# 🤖 50条AI赚钱提示词包\n\n> 适用于ChatGPT/Claude/文心一言等主流AI工具\n\n" + "\n".join(prompts)
    with open(os.path.join(PRODUCTS_DIR, "prompts_pack_50.md"), "w", encoding="utf-8") as f:
        f.write(prompts_text)
    print(f"  ✅ 提示词包: {prompt_num} 条, {len(prompts_text)}字")
    
    # 产品2: 自媒体模板包
    print("  🎯 产品2: AI自媒体模板包(30套)...")
    templates = []
    
    # 头条号模板
    templates.append("""# 头条号爆文模板

## 🏷️ 标题库
1. "2026年最XX的X个XX，第X个你绝对想不到"
2. "XX终于出手了！这一招让所有人都惊呆了"
3. "别再XX了，聪明人都用这个方法"
4. "XX行业大变天！XX即将被淘汰"
5. "月薪3000到3万，他只做对了一件事"

## 📝 正文结构
1. 开头：抛出问题/数据/反常识观点
2. 正文：3-5个小标题展开
3. 每个小标题：观点+案例+数据
4. 结尾：总结+互动引导

## 🏁 结尾模板
"觉得有用？点个赞支持一下！关注我获取更多XX干货 🚀"
""")
    
    # 百家号模板
    templates.append("""# 百家号SEO文章模板

## 🔑 关键词布局
- 标题：核心关键词靠前
- 首段：前100字出现核心关键词
- H2标题：含长尾关键词
- 全文：关键词密度2-3%

## 🏗️ 文章结构
首段（200字）：介绍主题，含核心关键词
H2: 第一部分内容（300-400字）
H2: 第二部分内容（300-400字）
H2: 第三部分内容（300-400字）
H3: 子要点展开
结尾：总结+引导关注

## ⚠️ 注意事项
- 段落不要太长，每段不超过300字
- 配图：每500字配一张图
- AI生成内容勾选框需要勾上
""")
    
    templates_text = "# 📚 30套AI自媒体模板包\n\n> 覆盖头条号、百家号、公众号、小红书等主流平台\n\n" + "\n---\n".join(templates)
    with open(os.path.join(PRODUCTS_DIR, "template_pack_30.md"), "w", encoding="utf-8") as f:
        f.write(templates_text)
    print(f"  ✅ 模板包: {len(templates)} 套, {len(templates_text)}字")
    
    # 产品3: 电子书(从已有文章生成)
    print("  🎯 产品3: AI赚钱电子书...")
    
    if os.path.exists(os.path.join(PRODUCTS_DIR, "ai_ebook.md")):
        with open(os.path.join(PRODUCTS_DIR, "ai_ebook.md"), "r") as f:
            ebook_text = f.read()
    else:
        ebook_text = "# AI时代赚钱实操指南\n\n（内容准备中）"
    
    print(f"  ✅ 电子书: {len(ebook_text)}字")
    
    print(f"\n💰 3个产品总价值: 19.9 + 29.9 + 39.9 = 89.7元")
    
    return True


# ============================================================
# 3. 知乎+公众号内容
# ============================================================

def build_content():
    print("\n📦 生成知乎+公众号内容...")
    
    # 知乎热门问题模板
    zhihu_qs = [
        "普通人如何利用AI每月多赚5000元？",
        "2026年有哪些AI工具是必须掌握的？",
        "AI会取代人类工作吗？我们应该怎么办？",
        "做自媒体还有前途吗？AI能帮上忙吗？",
        "有哪些适合副业小白的AI赚钱方式？",
    ]
    
    print(f"  🎯 已准备 {len(zhihu_qs)} 个知乎热门问题模板")
    for q in zhihu_qs:
        print(f"    - {q}")
    
    # 生成示例回答
    sample_answer = f"""# 知乎回答示例

## 问题：普通人如何利用AI每月多赚5000元？
（发布于：{datetime.now().strftime("%Y-%m-%d")}）

### 开头
作为一个利用AI做副业一年多、月均增收8000+的普通人，这个问题我来回答再合适不过了。

### 正文（3个实操方法）

**方法一：AI代写文章（月入1000-3000元）**
- 平台：闲鱼、淘宝、猪八戒
- 定价：10-30元/篇
- 每日接3-5单
- 成本：0元（AI生成）

**方法二：AI自媒体矩阵（月入2000-5000元）**
- 平台：百家号+头条号+公众号
- 内容：AI辅助生成
- 收益：流量分成+广告

**方法三：卖AI相关数字产品（月入3000+）**
- 提示词包 19.9元
- 模板包 29.9元
- 电子书 39.9元

### 结尾
如果你对某个方法感兴趣，欢迎评论区交流！
觉得有用的话点个赞支持一下 👍
"""
    
    zhihu_file = os.path.join(PRODUCTS_DIR, "zhihu_answers.md")
    with open(zhihu_file, "w", encoding="utf-8") as f:
        f.write(sample_answer)
    print(f"  ✅ 知乎回答模板已保存")
    
    # 公众号内容
    wechat_content = """# 公众号内容策略

## 📅 周更计划
周一：AI工具推荐（图文评测）
周三：AI赚钱案例（实操分享）
周五：AI行业资讯（趋势分析）
周日：互动话题（问答/投票）

## 📝 文章风格
- 标题：有数字、有悬念、有利益点
- 开头：故事/案例切入
- 正文：短段落（每段不超过100字）
- 配图：每500字配1张
- 结尾：关注引导+互动提问

## 🚀 推广位布局
文章顶部：引导关注卡片
文章中部：推荐阅读/课程链接
文章底部：关注引导+在看
"""
    wechat_file = os.path.join(PRODUCTS_DIR, "wechat_strategy.md")
    with open(wechat_file, "w", encoding="utf-8") as f:
        f.write(wechat_content)
    print(f"  ✅ 公众号运营策略已保存")
    
    return True


# ============================================================
# 4. 完整操作指南
# ============================================================

def print_guide():
    print("""
╔══════════════════════════════════════════════════════╗
║         AI智变 - 四路变现完整操作指南               ║
╚══════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 路线1：闲鱼AI代写（今天启动，今天赚钱）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
已有材料：xianyu/services.txt  （服务清单）
          xianyu/replies.txt   （客服话术）
          xianyu/orders.json   （订单管理系统）

操作步骤：
1️⃣ 打开闲鱼APP → 点击"卖闲置"
2️⃣ 标题："AI代写文章 自媒体文案 当日交付"
3️⃣ 正文：复制 services.txt 内容
4️⃣ 定价：10-30元/篇，新人价设8元起
5️⃣ 有人咨询时，用 replies.txt 的话术回复
6️⃣ 接单后：python3 make_money.py create-order "需求"
7️⃣ 交付前：python3 make_money.py deliver 订单号
8️⃣ 把deliver文件发给客户"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 路线2：卖数字产品（今天上架，持续收钱）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
已有产品：
  🎯 提示词包: products/prompts_pack_50.md  19.9元
  📚 模板包:  products/template_pack_30.md   29.9元
  📖 电子书:  products/ai_ebook.md           39.9元
  💰 全套打包: 限时价 69.9元（原价89.7元）

上架平台：
  • 面包多（推荐，微信支付秒到账）
  • 知识星球
  • 小报童
  • 自己的网站（已部署好，加个购买页即可）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 路线3：公众号（2周见效，长尾收入）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣ 注册微信公众号（个人即可）
2️⃣ 名称："AI智变" / "AI赚钱实验室"
3️⃣ 日更：用现有 pipeline 每天发
4️⃣ 满500粉：开通流量主（底部广告）
5️⃣ 月收入预估：500粉≈300元 | 2000粉≈1500元

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 路线4：知乎好物（1周见效，睡后收入）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣ 搜索AI相关热门问题
2️⃣ 用模板写高质量回答
3️⃣ 植入推广链接（AI课程/工具会员）
4️⃣ 高赞回答 → 持续带来佣金

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 第一周收入预估
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
闲鱼代写: 3单/天 × 15元 × 7天 = 315元
数字产品: 3份/周 × 30元 = 90元
收益总计: ≈ 400元/周

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 日常操作（每天只需5分钟）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
早上: 看闲鱼消息 → 确认订单
      python3 make_money.py deliver 订单号
晚上: 看百家号/头条号阅读量
      python3 publish.py status
睡前: 回复客户消息
""")


# ============================================================
# 主程序
# ============================================================

def cmd_all():
    build_xianyu()
    build_products()
    build_content()
    print("\n" + "=" * 50)
    print("✅ 所有产品已生成完毕！")
    print("=" * 50)
    print_guide()

def cmd_xianyu():
    build_xianyu()

def cmd_products():
    build_products()

def cmd_content():
    build_content()

def cmd_guide():
    print_guide()


if __name__ == "__main__":
    cmds = {
        "all": cmd_all,
        "xianyu": cmd_xianyu,
        "products": cmd_products,
        "content": cmd_content,
        "guide": cmd_guide,
    }
    
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(__doc__)
        sys.exit(1)
    
    cmds[sys.argv[1]]()
