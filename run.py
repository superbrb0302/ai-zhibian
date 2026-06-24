#!/usr/bin/env python3
"""
AI智变 - 全自动内容运营系统
================================
使用方法:
  python3 run.py generate   # 生成新内容
  python3 run.py build      # 构建静态站点
  python3 run.py full       # 生成+构建（日常使用）
  python3 run.py daily      # 生成本日内容包（准备发头条号/百家号）
  python3 run.py status     # 查看当前状态
"""
import json
import os
import sys
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from content_generator import AIContentGenerator
from generate_site import build as build_site

def cmd_generate():
    gen = AIContentGenerator()
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    new = gen.generate_batch(count)
    print(f"✅ 生成了 {len(new)} 篇新文章")
    return new

def cmd_build():
    build_site()

def cmd_full():
    print("=" * 50)
    print("🚀 AI智变 - 全自动运营流水线")
    print("=" * 50)
    cmd_generate()
    cmd_build()
    print("\n🎉 全部完成！")

def cmd_daily():
    """生成每日内容包，用于发布到头条号/百家号"""
    gen = AIContentGenerator()
    new = gen.generate_batch(3)
    build_site()
    
    output_dir = os.path.join(BASE_DIR, "output")
    daily_dir = os.path.join(BASE_DIR, "daily_pack")
    if os.path.exists(daily_dir):
        shutil.rmtree(daily_dir)
    
    date_str = datetime.now().strftime("%Y%m%d")
    daily_dir = os.path.join(BASE_DIR, f"daily_pack_{date_str}")
    os.makedirs(daily_dir, exist_ok=True)

    for i, a in enumerate(new):
        # 纯文本版本 - 可直接复制到头条号
        import re
        text = re.sub(r'<[^>]+>', '', a["content"])
        text = re.sub(r'\n{3,}', '\n\n', text).strip()
        
        txt_path = os.path.join(daily_dir, f"{i+1}_{a['slug'].replace('.html','')}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"标题：{a['title']}\n")
            f.write(f"关键词：{a['keywords']}\n")
            f.write(f"{'='*40}\n\n")
            f.write(text)
        
        # 附带文章信息
        info_path = os.path.join(daily_dir, f"{i+1}_info.txt")
        with open(info_path, "w", encoding="utf-8") as f:
            f.write(f"标题: {a['title']}\n")
            f.write(f"分类: {a['category']}\n")
            f.write(f"日期: {a['date']}\n")
            f.write(f"关键词: {a['keywords']}\n")
            f.write(f"描述: {a['description']}\n")

    print(f"\n📦 每日内容包已生成: {daily_dir}/")
    print(f"   共 {len(new)} 篇文章")
    print("\n📋 今日文章列表：")
    for i, a in enumerate(new):
        print(f"  {i+1}. [{a['category']}] {a['title']}")
    print(f"\n⏱ 预计发布耗时：约3-5分钟")
    print(f"💡 打开 {daily_dir}/ 复制内容到头条号/百家号即可")

def cmd_status():
    gen = AIContentGenerator()
    articles = gen.get_all_articles()
    
    cat_counts = {}
    for a in articles:
        cat = a["category"]
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    
    # 统计最近7天
    from datetime import timedelta
    week_ago = datetime.now() - timedelta(days=7)
    recent = [a for a in articles if datetime.strptime(a["date"], "%Y-%m-%d") >= week_ago]
    
    print("=" * 50)
    print("📊 AI智变 - 运营状态")
    print("=" * 50)
    print(f"📚 总文章数: {len(articles)}")
    print(f"📅 近7天新增: {len(recent)}")
    print(f"\n📂 分类分布:")
    for cat, count in sorted(cat_counts.items()):
        bar = "█" * min(count, 20)
        print(f"  {cat:15s} {bar} {count}")
    print(f"\n🏠 站点目录: {os.path.join(BASE_DIR, 'output')}/")
    print(f"📦 内容目录: {os.path.join(BASE_DIR, 'articles')}/")
    print(f"\n💡 下一步:")
    print(f"  python3 run.py full    # 生成内容+构建站点")
    print(f"  python3 run.py daily   # 生成每日发布包")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    commands = {
        "generate": cmd_generate,
        "build": cmd_build,
        "full": cmd_full,
        "daily": cmd_daily,
        "status": cmd_status,
    }
    
    if cmd not in commands:
        print(f"未知命令: {cmd}")
        print(__doc__)
        sys.exit(1)
    
    commands[cmd]()
