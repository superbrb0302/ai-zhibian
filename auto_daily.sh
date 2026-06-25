#!/bin/bash
# AI智变 每日自动任务
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH
cd /Users/mattlam/Documents/副业养家/ai-content-site || exit 1
/usr/bin/python3 run.py full >> /Users/mattlam/Library/Logs/aizhibian/daily.log 2>> /Users/mattlam/Library/Logs/aizhibian/daily.err
cd /Users/mattlam/Documents/副业养家/ai-content-site
/usr/bin/git add -A 2>> /Users/mattlam/Library/Logs/aizhibian/git.err
/usr/bin/git commit -m "auto: daily content update $(/bin/date +%Y-%m-%d)" 2>> /Users/mattlam/Library/Logs/aizhibian/git.err
/usr/bin/git push origin main 2>> /Users/mattlam/Library/Logs/aizhibian/git.err
