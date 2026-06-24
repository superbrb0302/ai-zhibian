#!/usr/bin/env python3
"""
AI智变 - 部署助手

使用方式:
  1. 注册 GitHub 账号 (https://github.com)
  2. 告诉我你的 GitHub 用户名
  3. 我帮你部署到 Vercel (免费)

本站点是纯静态 HTML，可部署到:
- Vercel (推荐) → https://vercel.com
- Cloudflare Pages → https://pages.cloudflare.com
- GitHub Pages → https://pages.github.com
- Netlify → https://netlify.com
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

def check_output():
    if not os.path.exists(OUTPUT_DIR):
        print("❌ 输出目录不存在，请先运行 python3 run.py full")
        return False
    
    files = os.listdir(OUTPUT_DIR)
    if not any(f.endswith(".html") for f in files):
        print("❌ 输出目录中没有HTML文件")
        return False
    
    print(f"✅ 站点已就绪，共 {len(files)} 个文件")
    return True

def print_vercel_guide():
    print("""
═══════════════════════════════════════════
🚀 Vercel 一键部署指南（推荐，完全免费）
═══════════════════════════════════════════

Step 1: 注册 Vercel
  打开 https://vercel.com 用 GitHub 账号登录

Step 2: 新建项目
  点击 "Add New" → "Project"
  选择你的 GitHub 仓库

Step 3: 配置
  Framework Preset: Other
  Root Directory: ai-content-site/output
  Build Command: (留空)
  Output Directory: ./

Step 4: 部署
  点击 "Deploy" → 等待完成 → 获得域名

✅ 完成！你的网站会自动更新。
以后我每次生成新内容，只要提交到 GitHub，
Vercel 会自动重新部署。
""")

def print_cloudflare_guide():
    print("""
═══════════════════════════════════════════
☁️ Cloudflare Pages 部署指南
═══════════════════════════════════════════

Step 1: 登录 https://dash.cloudflare.com
Step 2: 进入 Pages → 创建项目
Step 3: 连接 GitHub 仓库
Step 4: 构建配置
  构建命令: (留空)
  输出目录: ai-content-site/output
Step 5: 部署
""")

if __name__ == "__main__":
    if not check_output():
        exit(1)
    print_vercel_guide()
    print_cloudflare_guide()
