#!/bin/bash
cd /home/user/one_bite_news_project
git config user.email 'auto@hanipnews.kr'
git config user.name '한입뉴스'
git add web/posts.json web/posts/ _posts/
git commit -m 'feat: 2026-05-07 한입뉴스 4건 자동 발행'
git remote set-url origin 'https://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@github.com/jiseungchan/one_bite_news_project.git'
git push origin main
