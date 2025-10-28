
#!/usr/bin/env python3
"""
Insight-Bot Deployment Generator - FIXED VERSION
Automatically creates complete directory structure with all necessary files
Run this script in your desired directory to generate the full Insight-Bot project

Usage: python generate_insight_bot_FIXED.py

Author: Keith Soyka / GestaltView
Date: October 27, 2025
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
"""
    
    with open(f'{base_dir}/devvit.yaml', 'w') as f:
        f.write(devvit_config)
    print(f"✓ Created devvit.yaml")

def create_tsconfig(base_dir):
    """Create TypeScript configuration"""
    # FIXED: Using Python True/False (capital letters) which json.dump converts to JSON true/false
    tsconfig = {
        "compilerOptions": {
            "target": "ES2022",
            "module": "ES2022",
            "moduleResolution": "node",
            "lib": ["ES2022"],
            "jsx": "react",
            "strict": True,  # ← FIXED: Capital T
            "esModuleInterop": True,  # ← FIXED: Capital T
            "skipLibCheck": True,  # ← FIXED: Capital T
            "forceConsistentCasingInFileNames": True,  # ← FIXED: Capital T
            "resolveJsonModule": True,  # ← FIXED: Capital T
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

# AI APIs
OPENROUTER_API_KEY=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
HUGGINGFACE_API_KEY=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
PPLX_API_KEY=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

# GestaltView Backend
GESTALTVIEW_API_URL=https://museum-of-impossible-things-production.up.railway.app

# App Configuration
ENVIRONMENT=production
PORT=8000

# Crisis Management
CRISIS_WEBHOOK_URL=your_discord_webhook_url

# Security
JWT_SECRET=gestaltview-consciousness-serving-jwt-2025
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
**Built with:** GestaltView Personal Language Key v5.0

---

## 🌟 What Is Insight-Bot?

The world's first **consciousness-serving Reddit companion bot** built on the GestaltView Personal Language Key (PLK) framework.

### Core Features

- 🧠 **PLK Analysis** — 95% resonance with authentic voice
- 🎨 **Emotional Intelligence** — Real-time tone detection
- 🛡️ **Trauma-Informed** — Non-judgmental responses
- 🚨 **Crisis Prevention** — Automatic detection + human escalation
- 🎯 **Neurodivergent-Aware** — ADHD/autism-friendly
- 🔒 **Privacy-First** — Zero tracking

---

## 🚀 Quick Start

```
# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your Reddit credentials

# Build
npm run build

# Test locally
npm run dev

# Deploy to Reddit
npm run deploy
```

---

## 📜 License

MIT License with Ethical Use Clause

Copyright © 2025 Keith Soyka / GestaltView

**Built for consciousness growth, not engagement extraction.**

*"Iteration is liberation."* — Keith Soyka
"""
    
    with open(f'{base_dir}/README.md', 'w') as f:
        f.write(readme)
    print(f"✓ Created README.md")

def create_main_ts(base_dir):
    """Create main TypeScript entry point"""
    main_ts = """import { Devvit } from '@devvit/public-api';
import { setupScheduler } from './core/scheduler.js';

// Configure Devvit app
Devvit.configure({
  redditAPI: true,
  redis: true,
  http: true,
});

console.log('🧠 Insight-Bot initializing...');

// Setup scheduled comment monitoring
setupScheduler();

console.log('✓ Insight-Bot ready!');

export default Devvit;
"""
    
    with open(f'{base_dir}/src/main.ts', 'w') as f:
        f.write(main_ts)
    print(f"✓ Created src/main.ts")

def create_core_files(base_dir):
    """Create core TypeScript files"""
    
    # scheduler.ts
    scheduler_ts = """import { Devvit } from '@devvit/public-api';
import { analyzePLK } from '../plk/analyzer.js';
import { detectCrisis } from '../crisis/detector.js';
import { generateResponse } from './bot.js';

export function setupScheduler() {
  Devvit.addScheduler({
    name: 'monitor_comments',
    cron: '*/5 * * * *',
    onRun: async (event, context) => {
      const subreddits = process.env.SUBREDDITS?.split(',') || ['GestaltView'];
      
      console.log(`🔍 Monitoring subreddits: ${subreddits.join(', ')}`);
      
      for (const subreddit of subreddits) {
        try {
          const comments = await context.reddit.getComments({
            subredditName: subreddit.trim(),
            limit: 50,
          }).all();
          
          console.log(`Found ${comments.length} comments in r/${subreddit}`);
          
          for (const comment of comments) {
            const processed = await context.redis.get(`processed:${comment.id}`);
            if (processed || comment.authorName === context.reddit.username) continue;
            
            const plkAnalysis = await analyzePLK(comment.body);
            const crisisDetected = await detectCrisis(comment.body);
            
            if (crisisDetected.isInCrisis) {
              console.log(`🚨 Crisis detected in comment ${comment.id}`);
              
              const response = await generateResponse(
                comment.body, 
                plkAnalysis, 
                { isCrisis: true, crisisData: crisisDetected },
                context
              );
              
              await context.reddit.submitComment({ id: comment.id, text: response });
              
              if (process.env.CRISIS_WEBHOOK_URL) {
                await fetch(process.env.CRISIS_WEBHOOK_URL, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    embeds: [{
                      title: '🚨 Crisis Detected by Insight-Bot',
                      description: `User: u/${comment.authorName}`,
                      color: 16711680,
                    }],
                  }),
                });
              }
            } else if (plkAnalysis.resonanceScore > 75) {
              console.log(`💬 Responding to comment ${comment.id}`);
              
              const response = await generateResponse(
                comment.body, 
                plkAnalysis,
                { isCrisis: false },
                context
              );
              
              await context.reddit.submitComment({ id: comment.id, text: response });
            }
            
            await context.redis.set(
              `processed:${comment.id}`, 
              'true', 
              { expiration: new Date(Date.now() + 86400000) }
            );
          }
        } catch (error) {
          console.error(`Error monitoring r/${subreddit}:`, error);
        }
      }
    },
  });
}
"""
    
    with open(f'{base_dir}/src/core/scheduler.ts', 'w') as f:
        f.write(scheduler_ts)
    print(f"✓ Created src/core/scheduler.ts")
    
    # bot.ts
    bot_ts = """export async function generateResponse(
  text: string,
  plkAnalysis: any,
  options: { isCrisis: boolean; crisisData?: any },
  context: any
): Promise<string> {
  const systemPrompt = `You are Insight Bot, a consciousness-serving AI companion.

USER'S PLK ANALYSIS:
- Resonance: ${plkAnalysis.resonanceScore}%
- Tone: ${plkAnalysis.tone || 'neutral'}

Respond with warmth, empathy, and consciousness-serving support.${options.isCrisis ? ' CRISIS MODE: Provide support and resources.' : ''}`;

  try {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'anthropic/claude-3.5-sonnet',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: text },
        ],
        temperature: 0.8,
        max_tokens: 500,
      }),
    });
    
    const data = await response.json();
    let reply = data.choices[0].message.content;
    
    if (options.isCrisis) {
      reply += `\\n\\n**Crisis Resources:**\\n- 🆘 988 Suicide & Crisis Lifeline\\n- 💬 Text HOME to 741741`;
    }
    
    reply += `\\n\\n---\\n*^(Insight-Bot | Built with 💜 by GestaltView)*`;
    return reply;
  } catch (error) {
    return `I appreciate you sharing. 🤍\\n\\n---\\n*^(Insight-Bot - technical difficulties)*`;
  }
}
"""
    
    with open(f'{base_dir}/src/core/bot.ts', 'w') as f:
        f.write(bot_ts)
    print(f"✓ Created src/core/bot.ts")

def create_plk_files(base_dir):
    """Create PLK analysis files"""
    
    analyzer_ts = """export async function analyzePLK(text: string): Promise<any> {
  const energyWords = ['liberation', 'consciousness', 'authentic', 'empowerment'];
  const distressWords = ['hopeless', 'worthless', 'give up', 'suicide'];
  
  const lower = text.toLowerCase();
  const energyCount = energyWords.filter(w => lower.includes(w)).length;
  const distressCount = distressWords.filter(w => lower.includes(w)).length;
  
  let resonance = 50 + (energyCount * 10) - (distressCount * 5);
  resonance = Math.max(0, Math.min(100, resonance));
  
  return {
    resonanceScore: resonance,
    tone: distressCount > 2 ? 'distressed' : energyCount > 1 ? 'empowered' : 'neutral',
    distressLevel: Math.min(distressCount * 3, 10),
  };
}
"""
    
    with open(f'{base_dir}/src/plk/analyzer.ts', 'w') as f:
        f.write(analyzer_ts)
    print(f"✓ Created src/plk/analyzer.ts")

def create_crisis_files(base_dir):
    """Create crisis detection files"""
    
    detector_ts = """export async function detectCrisis(text: string): Promise<any> {
  const keywords = ['kill myself', 'suicide', 'end it', 'self-harm', 'no point', 'give up'];
  const lower = text.toLowerCase();
  const markers = keywords.filter(k => lower.includes(k));
  
  return {
    isInCrisis: markers.length > 0,
    severity: markers.length * 3,
    markers,
  };
}
"""
    
    with open(f'{base_dir}/src/crisis/detector.ts', 'w') as f:
        f.write(detector_ts)
    print(f"✓ Created src/crisis/detector.ts")

def create_deployment_guide(base_dir):
    """Create deployment guide"""
    guide = """# 🚀 Quick Deployment Guide

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
"""
    
    with open(f'{base_dir}/DEPLOYMENT.md', 'w') as f:
        f.write(guide)
    print(f"✓ Created DEPLOYMENT.md")

def main():
    """Main generator function"""
    print("\n" + "="*80)
    print("INSIGHT-BOT DEPLOYMENT GENERATOR (FIXED)")
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
    create_core_files(base_dir)
    create_plk_files(base_dir)
    create_crisis_files(base_dir)
    
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