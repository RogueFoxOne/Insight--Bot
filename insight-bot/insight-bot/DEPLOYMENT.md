# Deployment Guide

## Prerequisites

- Reddit API credentials (from your screenshot)
- Node.js 18+
- npm or yarn

## Steps

1. **Install dependencies**
   ```bash
   npm install
   npm install -g devvit
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Reddit credentials
   ```

3. **Build**
   ```bash
   npm run build
   ```

4. **Deploy**
   ```bash
   devvit login
   devvit upload
   ```

5. **Install in subreddit**
   - Go to https://developers.reddit.com/apps
   - Click "Install to Community"
   - Select r/gestaltview_bot_dev

## Monitoring

```bash
devvit logs insight-bot
```

For help: keith@gestaltview.com
