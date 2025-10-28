# 🚀 Quick Deployment Guide

## Step 1: Install Dependencies

```
npm install
npm install -g devvit
```

## Step 2: Configure Environment

```
cp .env.example .env
# Edit .env with your Reddit credentials from screenshot
```

## Step 3: Build & Deploy

```
npm run build
devvit login
devvit upload
```

## Step 4: Install in Subreddit

1. Go to https://developers.reddit.com/apps
2. Find "insight-bot"
3. Click "Install to Community"
4. Select r/gestaltview_bot_dev

## Monitoring

```
devvit logs insight-bot
```

For help: keith@gestaltview.com
