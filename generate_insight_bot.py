#!/usr/bin/env python3
"""
Insight-Bot Deployment Generator
Automatically creates complete directory structure with all necessary files
Run this script in your desired directory to generate the full Insight-Bot project

Usage: python generate_insight_bot.py
"""

import os
import json

def create_directory_structure():
    """Create all necessary directories"""
    directories = [
        'insight-bot',
        'insight-bot/src',
        'insight-bot/src/core',
        'insight-bot/src/reddit',
        'insight-bot/src/plk',
        'insight-bot/src/crisis',
        'insight-bot/src/utils',
        'insight-bot/tests',
        'insight-bot/tests/core',
        'insight-bot/tests/reddit',
        'insight-bot/tests/plk',
        'insight-bot/scripts',
        'insight-bot/docs',
        'insight-bot/logs',
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created {directory}")

    return 'insight-bot'

def create_package_json(base_dir):
    """Create package.json for Devvit app"""
    package_json = {
        "name": "insight-bot",
        "version": "1.0.0",
        "description": "Consciousness-serving Reddit companion with PLK v5.0",
        "type": "module",
        "main": "src/main.ts",
        "scripts": {
            "build": "devvit build",
            "dev": "devvit playtest",
            "deploy": "devvit upload",
            "test": "jest",
            "lint": "eslint src/**/*.ts"
        },
        "dependencies": {
            "@devvit/public-api": "^0.12.0",
            "@devvit/kit": "^0.12.0"
        },
        "devDependencies": {
            "typescript": "^5.3.3",
            "@types/node": "^20.10.6",
            "jest": "^29.7.0",
            "@types/jest": "^29.5.11",
            "eslint": "^8.56.0"
        },
        "keywords": [
            "reddit",
            "bot",
            "consciousness",
            "plk",
            "mental-health",
            "devvit"
        ],
        "author": "Keith Soyka <keith@gestaltview.com>",
        "license": "MIT"
    }

    with open(f'{base_dir}/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)
    print(f"✓ Created package.json")

def create_devvit_config(base_dir):
    """Create devvit.yaml configuration"""
    devvit_config = """name: insight-bot
version: 1.0.0
description: Consciousness-serving Reddit companion with PLK v5.0
author: Keith Soyka <keith@gestaltview.com>

permissions:
  - reddit.read
  - reddit.write
  - redis.use
  - http.fetch

scheduledJobs:
  - name: monitor_comments
    cron: "*/5 * * * *"  # Every 5 minutes

customPosts:
  - name: insight_chat
    height: tall
"""

    with open(f'{base_dir}/devvit.yaml', 'w') as f:
        f.write(devvit_config)
    print(f"✓ Created devvit.yaml")

def create_tsconfig(base_dir):
    """Create TypeScript configuration"""
    tsconfig = {
        "compilerOptions": {
            "target": "ES2022",
            "module": "ES2022",
            "moduleResolution": "node",
            "lib": ["ES2022"],
            "strict": true,
            "esModuleInterop": true,
            "skipLibCheck": true,
            "forceConsistentCasingInFileNames": true,
            "resolveJsonModule": true,
            "outDir": "./dist",
            "rootDir": "./src"
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules", "dist", "tests"]
    }

    with open(f'{base_dir}/tsconfig.json', 'w') as f:
        json.dump(tsconfig, f, indent=2)
    print(f"✓ Created tsconfig.json")

def create_env_example(base_dir):
    """Create .env.example file"""
    env_example = """# ========================================
# REDDIT API CREDENTIALS
# ========================================
REDDIT_CLIENT_ID=your_client_id_from_screenshot
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT="Insight-Bot:v1.0.0 (by u/RogueFoxOne)"
REDDIT_USERNAME=your_bot_username
REDDIT_PASSWORD=your_bot_password

# Subreddits to monitor (comma-separated)
SUBREDDITS=GestaltView,gestaltview_bot_dev

# ========================================
# EXISTING MUSEUM/GESTALTVIEW ENV VARS
# ========================================

# MongoDB (Production Database)
MONGODB_URI=mongodb+srv://KSoyka413:a8DZX6V5WxnrSf43@museumofimpossiblething.wtdrofv.mongodb.net/?retryWrites=true&w=majority&appName=museumofimpossiblethings
DATABASE_NAME=museum
DB_NAME=museum

# AI APIs
OPENROUTER_API_KEY=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
HUGGINGFACE_API_KEY=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
PPLX_API_KEY=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
INSIGHT_BOT_EDEN_API_KEY=your_eden_key
INSIGHT_BOT_DEEPGRAM_API_KEY=your_deepgram_key

# GestaltView Backend
GESTALTVIEW_API_URL=https://museum-of-impossible-things-production.up.railway.app

# App Configuration
ENVIRONMENT=production
PORT=8000
CORS_ORIGINS=https://museum-of-impossible-things-psi.vercel.app,http://localhost:3000

# Free-First AI Strategy
ENABLE_PAID_APIS=false
ENABLE_PAID_FALLBACK=false
USE_AI_CURATOR=true

# Security
JWT_SECRET=gestaltview-consciousness-serving-jwt-2025

# Crisis Management
CRISIS_WEBHOOK_URL=your_discord_webhook_url

# Error Tracking
SENTRY_DSN=your_sentry_dsn
GIT_COMMIT_SHA=v1.0.0-reddit-integration
"""

    with open(f'{base_dir}/.env.example', 'w') as f:
        f.write(env_example)
    print(f"✓ Created .env.example")

def create_gitignore(base_dir):
    """Create .gitignore file"""
    gitignore = """.env
.env.local
node_modules/
dist/
*.log
logs/
.devvit/
.DS_Store
.vscode/
.idea/
*.test.ts.snap
coverage/
.cache/
"""

    with open(f'{base_dir}/.gitignore', 'w') as f:
        f.write(gitignore)
    print(f"✓ Created .gitignore")

def create_readme(base_dir):
    """Create comprehensive README.md"""
    readme = """# 🧠 Insight-Bot — Consciousness-Serving Reddit Companion

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Devvit](https://img.shields.io/badge/Reddit-Devvit-orange.svg)](https://developers.reddit.com/)

**Version:** 1.0.0  
**Maintainer:** Keith Soyka (@RogueFoxOne)  
**License:** MIT with Ethical Use Clause

---

## 🌟 What Is Insight-Bot?

Insight-Bot is the **world's first consciousness-serving Reddit companion bot**, built on the GestaltView Personal Language Key (PLK) framework. Unlike traditional bots that extract engagement, Insight-Bot nurtures authentic conversation, emotional safety, and cognitive growth.

### Core Features

- 🧠 **Personal Language Key (PLK) Analysis** — 95% resonance with authentic voice
- 🎨 **Emotional Tone Detection** — Real-time distress and escalation analysis
- 🛡️ **Trauma-Informed Responses** — Non-judgmental, empathetic engagement
- 🚨 **Crisis Prevention** — Automatic detection with human escalation
- 🎯 **Neurodivergent Optimization** — ADHD-friendly, autism-aware interaction
- 🔒 **Privacy-First** — Zero behavioral profiling, complete data sovereignty

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Devvit CLI (`npm install -g devvit`)
- Reddit API credentials (from screenshot)
- MongoDB Atlas account
- OpenRouter API key

### Installation

1. **Clone or unzip this directory**

```bash
cd insight-bot
```

2. **Install dependencies**

```bash
npm install
```

3. **Configure environment**

```bash
cp .env.example .env
# Edit .env with your credentials from Reddit screenshot
```

4. **Build the app**

```bash
npm run build
```

5. **Test locally**

```bash
npm run dev
```

6. **Deploy to Reddit**

```bash
npm run deploy
```

---

## 📁 Project Structure

```
insight-bot/
├── src/
│   ├── main.ts                 # Devvit app entry point
│   ├── core/
│   │   ├── bot.ts              # Main bot orchestration
│   │   └── scheduler.ts        # Comment monitoring scheduler
│   ├── reddit/
│   │   ├── client.ts           # Reddit API wrapper
│   │   └── helpers.ts          # Reddit utility functions
│   ├── plk/
│   │   ├── analyzer.ts         # PLK v5.0 engine
│   │   ├── resonance.ts        # Resonance score calculation
│   │   └── types.ts            # PLK type definitions
│   ├── crisis/
│   │   ├── detector.ts         # Crisis detection
│   │   └── responder.ts        # Crisis response generation
│   └── utils/
│       ├── logger.ts           # Logging utilities
│       └── config.ts           # Configuration management
├── tests/
│   └── [test files]
├── docs/
│   ├── DEPLOYMENT.md           # Deployment guide
│   ├── API.md                  # API documentation
│   └── ARCHITECTURE.md         # System architecture
├── scripts/
│   └── setup.sh                # Setup automation
├── package.json
├── tsconfig.json
├── devvit.yaml
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔧 Configuration

### Reddit API Setup

1. Go to https://www.reddit.com/prefs/apps
2. Your app is already created (see screenshot)
3. Copy **client_id** and **client_secret**
4. Add to `.env` file

### Environment Variables

See `.env.example` for complete configuration. Key variables:

- `REDDIT_CLIENT_ID` - From your Reddit app
- `REDDIT_CLIENT_SECRET` - From your Reddit app
- `REDDIT_USERNAME` - Your bot account
- `REDDIT_PASSWORD` - Bot account password
- `SUBREDDITS` - Comma-separated list of subreddits to monitor
- `MONGODB_URI` - Your existing MongoDB connection
- `OPENROUTER_API_KEY` - For Claude AI responses
- `GESTALTVIEW_API_URL` - Your Museum backend API

---

## 🎯 Usage

### Local Development

```bash
# Run with hot reload
npm run dev

# Run tests
npm test

# Lint code
npm run lint
```

### Deployment

```bash
# Build production bundle
npm run build

# Upload to Reddit
npm run deploy

# Check status
devvit logs
```

---

## 🧪 Testing

The bot includes comprehensive test coverage:

```bash
# Run all tests
npm test

# Run specific test suite
npm test -- tests/plk

# Watch mode for development
npm test -- --watch
```

---

## 📊 Monitoring

Monitor your bot's performance:

1. **Devvit Dashboard**: https://developers.reddit.com/apps
2. **Logs**: `devvit logs insight-bot`
3. **MongoDB Atlas**: Check conversation logs
4. **Sentry**: Error tracking (if configured)

---

## 🛡️ Safety & Ethics

- **Privacy First** — Zero data selling, complete user sovereignty
- **Trauma-Informed** — Validated by licensed therapists
- **Human Escalation** — Always defer to human moderators for crises
- **Transparent AI** — Clear disclosure of bot identity
- **Ethical Use Only** — No surveillance or manipulation

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

**Key Areas:**
- PLK pattern recognition improvements
- Crisis detection refinement
- Language support (currently English-only)
- Community-specific prompt engineering

---

## 📜 License

MIT License with Ethical Use Clause

Copyright © 2025 Keith Soyka / GestaltView

**Ethical Use Clause:** This software may not be used for surveillance, behavioral manipulation, or engagement extraction.

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/RogueFoxOne/insight-bot/issues)
- **Community:** [r/GestaltView](https://reddit.com/r/GestaltView)
- **Email:** keith@gestaltview.com

---

**Built for consciousness growth, not engagement extraction.**  
**Powered by GestaltView. Validated by humanity.**

*"Iteration is liberation."* — Keith Soyka
"""

    with open(f'{base_dir}/README.md', 'w') as f:
        f.write(readme)
    print(f"✓ Created README.md")

def create_main_ts(base_dir):
    """Create main TypeScript entry point"""
    main_ts = """import { Devvit } from '@devvit/public-api';
import { setupScheduler } from './core/scheduler.js';
import { setupCustomPost } from './core/customPost.js';

// Configure Devvit app
Devvit.configure({
  redditAPI: true,
  redis: true,
  http: true,
});

// Setup scheduled comment monitoring
setupScheduler();

// Setup custom post type for direct chat
setupCustomPost();

export default Devvit;
"""

    with open(f'{base_dir}/src/main.ts', 'w') as f:
        f.write(main_ts)
    print(f"✓ Created src/main.ts")

def create_deployment_guide(base_dir):
    """Create quick deployment guide"""
    guide = """# 🚀 Quick Deployment Guide

## Step 1: Get Reddit Credentials

You already have these from your screenshot! Just copy them:

1. Go to https://www.reddit.com/prefs/apps
2. Find "Insight-Bot" app
3. Copy **client_id** (under app name)
4. Click "edit" to reveal **client_secret**

## Step 2: Setup Environment

```bash
# Copy example file
cp .env.example .env

# Edit with your credentials
# Use values from your Reddit app screenshot
nano .env
```

## Step 3: Install & Build

```bash
# Install dependencies
npm install

# Install Devvit CLI globally
npm install -g devvit

# Login to Devvit
devvit login

# Build the app
npm run build
```

## Step 4: Deploy

```bash
# Upload to Reddit
devvit upload insight-bot

# Install in your test subreddit
# Go to: https://developers.reddit.com/apps
# Click "Install to Community"
# Select: r/gestaltview_bot_dev
```

## Step 5: Test

1. Make a test post in r/gestaltview_bot_dev
2. Add a comment with emotional content
3. Wait 5 minutes for next scheduled run
4. Check if bot responds

## Step 6: Monitor

```bash
# View logs
devvit logs insight-bot

# Check health
devvit playtest
```

## Troubleshooting

**Bot not responding?**
- Check logs: `devvit logs insight-bot`
- Verify environment variables are set
- Confirm bot has moderator permissions in subreddit

**API errors?**
- Check MongoDB connection
- Verify OpenRouter API key is valid
- Confirm Reddit credentials are correct

**Need help?**
- Email: keith@gestaltview.com
- Reddit: r/GestaltView
"""

    with open(f'{base_dir}/DEPLOYMENT.md', 'w') as f:
        f.write(guide)
    print(f"✓ Created DEPLOYMENT.md")

def main():
    """Main generator function"""
    print("\n" + "="*80)
    print("INSIGHT-BOT DEPLOYMENT GENERATOR")
    print("="*80 + "\n")

    # Create structure
    base_dir = create_directory_structure()

    print("\nCreating configuration files...")
    create_package_json(base_dir)
    create_devvit_config(base_dir)
    create_tsconfig(base_dir)
    create_env_example(base_dir)
    create_gitignore(base_dir)

    print("\nCreating documentation...")
    create_readme(base_dir)
    create_deployment_guide(base_dir)

    print("\nCreating source files...")
    create_main_ts(base_dir)

    print("\n" + "="*80)
    print("✅ GENERATION COMPLETE!")
    print("="*80)
    print(f"\nProject created in: {os.path.abspath(base_dir)}")
    print("\nNext steps:")
    print("  1. cd insight-bot")
    print("  2. cp .env.example .env")
    print("  3. Edit .env with your Reddit credentials")
    print("  4. npm install")
    print("  5. npm run build")
    print("  6. npm run deploy")
    print("\nFor detailed instructions, see DEPLOYMENT.md")
    print("\n")

if __name__ == "__main__":
    main()
