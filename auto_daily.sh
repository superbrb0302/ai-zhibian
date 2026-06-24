#!/bin/bash
cd /Users/mattlam/Documents/副业养家/ai-content-site
/usr/bin/python3 /Users/mattlam/Documents/副业养家/ai-content-site/run.py full 2>>/Users/mattlam/Library/Logs/aizhibian/build.err
cd /Users/mattlam/Documents/副业养家/ai-content-site
git add -A 2>>/Users/mattlam/Library/Logs/aizhibian/git.err
git commit -m "auto: daily content update $(date +%Y-%m-%d)" 2>>/Users/mattlam/Library/Logs/aizhibian/git.err
git push origin main 2>>/Users/mattlam/Library/Logs/aizhibian/git.err
