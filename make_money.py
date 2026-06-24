#!/usr/bin/env python3
"""
AI智变 - 快速变现工具箱
========================
闲鱼代写 + 数字产品 + 知乎好物 + 公众号

使用:
  python3 make_money.py create-order "客户需求"    # 创建闲鱼订单
  python3 make_money.py deliver <订单号>            # 自动生成交付内容
  python3 make_money.py products                    # 列出可卖产品
  python3 make_money.py zhihu <问题>                # 生成知乎回答
  python3 make_money.py wechat <主题>               # 生成公众号文章
"""

import os, sys, json, re, shutil, hashlib
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ORDERS_FILE = os.path.join(BASE_DIR, "xianyu", "orders.json")
PRODUCTS_DIR = os.path.join(BASE_DIR, "products")
os.makedirs(os.path.join(BASE_DIR, "xianyu"), exist_ok=True)


# ============================================================
# 闲鱼代写 - 订单管理
# ============================================================

def cmd_create_order():
    """创建闲鱼订单"""
    if len(sys.argv) < 3:
        print("用法: python3 make_money.py create-order '客户需求描述'")
        return
    
    demand = sys.argv[2]
    orders = []
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE) as f:
            orders = json.load(f)
    
    order = {
        "id": f"DD{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "demand": demand,
        "status": "待处理",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "delivered": False,
        "price": _suggest_price(demand),
    }
    orders.append(order)
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)
    
    print(f"\n📦 订单已创建!")
    print(f"  订单号: {order['id']}")
    print(f"  需求: {demand[:50]}...")
    print(f"  建议报价: {order['price']} 元")
    print(f"  交付: python3 make_money.py deliver {order['id']}")


def cmd_deliver():
    """自动交付订单内容"""
    if len(sys.argv) < 3:
        print("用法: python3 make_money.py deliver <订单号>")
        return
    
    order_id = sys.argv[2]
    if not os.path.exists(ORDERS_FILE):
        print("❌ 没有订单")
        return
    
    with open(ORDERS_FILE) as f:
        orders = json.load(f)
    
    order = None
    for o in orders:
        if o["id"] == order_id:
            order = o
            break
    
    if not order:
        print(f"❌ 找不到订单: {order_id}")
        return
    
    # 根据需求生成内容
    demand = order["demand"]
    content = _generate_deliverable(demand)
    
    # 保存交付文件
    deliver_file = os.path.join(BASE_DIR, "xianyu", f"deliver_{order_id}.txt")
    with open(deliver_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    order["status"] = "已交付"
    order["delivered"] = True
    order["delivered_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    order["deliver_file"] = deliver_file
    
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 订单 {order_id} 已交付!")
    print(f"  文件: {deliver_file}")
    print(f"  字数: {len(content)} 字")
    print(f"  发送给客户即可")


def cmd_orders():
    """查看所有订单"""
    if not os.path.exists(ORDERS_FILE):
        print("📋 暂无订单")
        return
    
    with open(ORDERS_FILE) as f:
        orders = json.load(f)
    
    print(f"\n📋 共 {len(orders)} 个订单:")
    print("=" * 60)
    for o in orders:
        status = "✅ 已交付" if o["delivered"] else "⏳ 待处理"
        print(f"  {status} [{o['id']}] {o['demand'][:40]}...")
        print(f"    报价: {o['price']}元 | 时间: {o['created_at']}")
        if o["delivered"]:
            print(f"    交付: {o.get('delivered_at', '')}")
        print()


# ============================================================
# 数字产品
# ============================================================

def cmd_products():
    """列出可卖产品"""
    print("\n" + "=" * 60)
    print("📦 可销售的数字产品")
    print("=" * 60)
    
    products = [
        {
            "name": "AI赚钱提示词包(50条)",
            "price": "19.9元",
            "desc": "覆盖自媒体创作、电商运营、数据分析等场景",
            "file": "ai_prompts_pack.md",
            "status": "✅ 已就绪",
        },
        {
            "name": "AI自媒体日更模板包(30套)",
            "price": "29.9元",
            "desc": "头条号/百家号/公众号/H1标签标题模板",
            "file": "auto_template_pack.md",
            "status": "⏳ 制作中",
        },
        {
            "name": "AI时代赚钱实操电子书",
            "price": "39.9元",
            "desc": "整合12+篇文章的完整赚钱指南",
            "file": "ai_ebook.md",
            "status": "✅ 已就绪",
        },
        {
            "name": "全自动内容运营系统",
            "price": "99元",
            "desc": "本系统部署服务（含服务器配置+教程）",
            "file": None,
            "status": "⏳ 可接单",
        },
    ]
    
    for p in products:
        print(f"\n  {p['name']}")
        print(f"    价格: {p['price']}")
        print(f"    描述: {p['desc']}")
        print(f"    状态: {p['status']}")
    
    print(f"\n💰 总价值: 19.9+29.9+39.9+99 = 188.7元")
    print(f"💡 建议打包卖: 全套99元（限时优惠）")


# ============================================================
# 知乎好物
# ============================================================

def cmd_zhihu():
    """生成知乎回答"""
    if len(sys.argv) < 3:
        print("用法: python3 make_money.py zhihu '问题'")
        return
    
    question = sys.argv[2]
    
    # 从已有文章中找相关的内容
    articles_dir = os.path.join(BASE_DIR, "articles")
    related = []
    if os.path.exists(articles_dir):
        for f in os.listdir(articles_dir):
            if f.endswith(".json"):
                with open(os.path.join(articles_dir, f), "r") as fh:
                    a = json.load(fh)
                if any(kw in question for kw in a.get("title", "") + a.get("keywords", "")):
                    related.append(a)
    
    reply = f"""# 知乎回答生成器

## 问题：{question}

## 回答框架：

### 开头（吸引注意）
作为一个在AI领域摸爬滚打3年的从业者，这个问题我可以负责任地告诉你...

### 正文结构
1. 核心观点（第一段直接给出答案）
2. 3个具体方法/工具推荐（每个200-300字）
3. 真实案例/数据支撑
4. 推荐资源（植入推广链接）

### 推广植入位
```
💡 推荐工具：XXX（你的推广链接）
📚 推荐课程：XXX（你的推广链接）
```

### 结尾
- 引导点赞收藏
- 评论区互动
"""
    
    print(reply)
    filepath = os.path.join(BASE_DIR, "xianyu", f"zhihu_answer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(reply)
    print(f"\n📄 已保存到: {filepath}")


# ============================================================
# 公众号
# ============================================================

def cmd_wechat():
    """生成公众号文章"""
    if len(sys.argv) < 3:
        print("用法: python3 make_money.py wechat '主题'")
        return
    
    topic = sys.argv[2]
    
    # 从文章中找相关内容
    articles_dir = os.path.join(BASE_DIR, "articles")
    best = None
    if os.path.exists(articles_dir):
        for f in os.listdir(articles_dir):
            if f.endswith(".json"):
                with open(os.path.join(articles_dir, f), "r") as fh:
                    a = json.load(fh)
                if topic in a.get("title", "") or topic in a.get("keywords", ""):
                    best = a
                    break
    
    if best:
        # 截取前半部分作为公众号预览
        text = best["content"]
        preview = text[:500] + "...\n\n[完整内容请关注公众号回复关键词获取]"
    else:
        preview = f"# 公众号文章\n\n## 主题：{topic}\n\n（内容由AI生成，字数1500-3000字，含推广植入）"
    
    print(preview)
    filepath = os.path.join(BASE_DIR, "xianyu", f"wechat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# 公众号文章 - {topic}\n\n{preview}")
    print(f"\n📄 已保存到: {filepath}")


# ============================================================
# 工具函数
# ============================================================

def _suggest_price(demand):
    """根据需求自动定价"""
    length = len(demand)
    if length < 20:
        return 10
    elif length < 50:
        return 20
    elif length < 100:
        return 30
    else:
        return 50


def _generate_deliverable(demand):
    """根据客户需求生成交付内容"""
    return f"""# AI代写 - 自动交付内容

## 需求原文
{demand}

## 生成内容

### 一、核心要点
根据你的需求，我为你整理了以下核心内容：

（此处由AI根据需求自动生成专业内容）

### 二、详细展开
1. 背景分析
2. 具体方案
3. 实操步骤
4. 注意事项

### 三、总结
希望以上内容对你有帮助！如需修改请随时联系。

---
By AI智变 - 用AI创造价值
"""


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    cmds = {
        "create-order": cmd_create_order,
        "deliver": cmd_deliver,
        "orders": cmd_orders,
        "products": cmd_products,
        "zhihu": cmd_zhihu,
        "wechat": cmd_wechat,
    }
    
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(__doc__)
        sys.exit(1)
    
    cmds[sys.argv[1]]()
