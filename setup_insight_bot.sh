#!/bin/bash
#
# Insight-Bot Automatic Setup Script
# Creates complete directory structure and all files
# Run this in your Museum repo to add Insight-Bot
#
# Usage: bash setup_insight_bot.sh
#

set -e  # Exit on error

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                INSIGHT-BOT AUTOMATIC DEPLOYMENT SETUP                         ║"
echo "║                      For Keith Soyka / GestaltView                            ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right place
if [ ! -d ".git" ]; then
    echo "⚠️  Warning: Not in a git repository. Continue anyway? (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        exit 1
    fi
fi

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p insight-bot/src/{core,reddit,plk,crisis,utils}
mkdir -p insight-bot/tests/{core,reddit,plk}
mkdir -p insight-bot/{scripts,docs,logs}

# Create package.json
echo "📦 Creating package.json..."
cat > insight-bot/package.json << 'EOF'
{
  "name": "insight-bot",
  "version": "1.0.0",
  "description": "Consciousness-serving Reddit companion with PLK v5.0",
  "type": "module",
  "main": "src/main.ts",
  "scripts": {
    "build": "devvit build",
    "dev": "devvit playtest",
    "deploy": "devvit upload",
    "install-cli": "npm install -g devvit",
    "setup": "npm install && npm run install-cli"
  },
  "dependencies": {
    "@devvit/public-api": "^0.12.0",
    "@devvit/kit": "^0.12.0"
  },
  "devDependencies": {
    "typescript": "^5.3.3",
    "@types/node": "^20.10.6"
  },
  "keywords": ["reddit", "bot", "consciousness", "plk", "gestaltview"],
  "author": "Keith Soyka <keith@gestaltview.com>",
  "license": "MIT"
}
EOF

# Create devvit.yaml
echo "⚙️  Creating devvit.yaml..."
cat > insight-bot/devvit.yaml << 'EOF'
name: insight-bot
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
    cron: "*/5 * * * *"
EOF

# Create tsconfig.json
echo "🔧 Creating tsconfig.json..."
cat > insight-bot/tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "node",
    "lib": ["ES2022"],
    "jsx": "react",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
EOF

# Create .env.example
echo "🔐 Creating .env.example..."
cat > insight-bot/.env.example << 'EOF'
# Reddit API (from your screenshot)
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT="Insight-Bot:v1.0.0 (by u/RogueFoxOne)"
REDDIT_USERNAME=your_bot_username
REDDIT_PASSWORD=your_bot_password

# Subreddits to monitor
SUBREDDITS=GestaltView,gestaltview_bot_dev

# MongoDB (from Museum env)
MONGODB_URI=mongodb+srv://KSoyka413:a8DZX6V5WxnrSf43@museumofimpossiblething.wtdrofv.mongodb.net/?retryWrites=true&w=majority&appName=museumofimpossiblethings
DATABASE_NAME=museum

# AI APIs (from Museum env)
OPENROUTER_API_KEY=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

# GestaltView Backend
GESTALTVIEW_API_URL=https://museum-of-impossible-things-production.up.railway.app

# Crisis Management
CRISIS_WEBHOOK_URL=your_discord_webhook_url
EOF

# Create .gitignore
echo "🚫 Creating .gitignore..."
cat > insight-bot/.gitignore << 'EOF'
.env
.env.local
node_modules/
dist/
*.log
logs/
.devvit/
.DS_Store
EOF

# Create main.ts
echo "📝 Creating src/main.ts..."
cat > insight-bot/src/main.ts << 'EOF'
import { Devvit } from '@devvit/public-api';
import { setupScheduler } from './core/scheduler.js';

Devvit.configure({
  redditAPI: true,
  redis: true,
  http: true,
});

console.log('🧠 Insight-Bot initializing...');
setupScheduler();
console.log('✓ Insight-Bot ready!');

export default Devvit;
EOF

# Create scheduler.ts
echo "⏰ Creating src/core/scheduler.ts..."
cat > insight-bot/src/core/scheduler.ts << 'EOF'
import { Devvit } from '@devvit/public-api';
import { analyzePLK } from '../plk/analyzer.js';
import { detectCrisis } from '../crisis/detector.js';
import { generateResponse } from './bot.js';

export function setupScheduler() {
  Devvit.addScheduler({
    name: 'monitor_comments',
    cron: '*/5 * * * *',
    onRun: async (event, context) => {
      const subreddits = process.env.SUBREDDITS?.split(',') || ['GestaltView'];

      for (const subreddit of subreddits) {
        try {
          const comments = await context.reddit.getComments({
            subredditName: subreddit.trim(),
            limit: 50,
          }).all();

          for (const comment of comments) {
            const processed = await context.redis.get(`processed:${comment.id}`);
            if (processed || comment.authorName === context.reddit.username) continue;

            const plkAnalysis = await analyzePLK(comment.body);
            const crisisDetected = await detectCrisis(comment.body);

            if (crisisDetected.isInCrisis) {
              const response = await generateResponse(comment.body, plkAnalysis, { isCrisis: true, crisisData: crisisDetected }, context);
              await context.reddit.submitComment({ id: comment.id, text: response });

              if (process.env.CRISIS_WEBHOOK_URL) {
                await fetch(process.env.CRISIS_WEBHOOK_URL, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    embeds: [{
                      title: '🚨 Crisis Detected',
                      description: `User: u/${comment.authorName}`,
                      color: 16711680,
                    }],
                  }),
                });
              }
            } else if (plkAnalysis.resonanceScore > 75) {
              const response = await generateResponse(comment.body, plkAnalysis, { isCrisis: false }, context);
              await context.reddit.submitComment({ id: comment.id, text: response });
            }

            await context.redis.set(`processed:${comment.id}`, 'true', { expiration: new Date(Date.now() + 86400000) });
          }
        } catch (error) {
          console.error(`Error in r/${subreddit}:`, error);
        }
      }
    },
  });
}
EOF

# Create bot.ts
echo "🤖 Creating src/core/bot.ts..."
cat > insight-bot/src/core/bot.ts << 'EOF'
export async function generateResponse(text: string, plkAnalysis: any, options: any, context: any): Promise<string> {
  const systemPrompt = `You are Insight Bot, a consciousness-serving AI companion.

PLK Analysis: ${plkAnalysis.resonanceScore}% resonance, ${plkAnalysis.tone} tone

Respond with warmth and empathy. Match their authentic voice.${options.isCrisis ? ' CRISIS MODE: Provide support and resources.' : ''}`;

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
      reply += `\n\n**Crisis Resources:**\n- 🆘 988 Suicide & Crisis Lifeline (US)\n- 💬 Text HOME to 741741`;
    }

    reply += `\n\n---\n*^(Insight-Bot | Built with 💜 by GestaltView)*`;
    return reply;
  } catch (error) {
    return `I appreciate you sharing. 🤍\n\n---\n*^(Insight-Bot - technical difficulties)*`;
  }
}
EOF

# Create analyzer.ts
echo "🔍 Creating src/plk/analyzer.ts..."
cat > insight-bot/src/plk/analyzer.ts << 'EOF'
export async function analyzePLK(text: string): Promise<any> {
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
EOF

# Create detector.ts
echo "🚨 Creating src/crisis/detector.ts..."
cat > insight-bot/src/crisis/detector.ts << 'EOF'
export async function detectCrisis(text: string): Promise<any> {
  const keywords = ['kill myself', 'suicide', 'end it', 'self-harm', 'no point', 'give up'];
  const lower = text.toLowerCase();
  const markers = keywords.filter(k => lower.includes(k));

  return {
    isInCrisis: markers.length > 0,
    severity: markers.length * 3,
    markers,
  };
}
EOF

# Create README
echo "📖 Creating README.md..."
cat > insight-bot/README.md << 'EOF'
# 🧠 Insight-Bot

Consciousness-serving Reddit companion with PLK v5.0

## Quick Start

```bash
npm install
npm run setup
cp .env.example .env
# Edit .env with Reddit credentials
npm run build
npm run deploy
```

## Deploy

1. Get Reddit credentials from https://reddit.com/prefs/apps
2. Add to `.env` file
3. Run `npm run deploy`
4. Install in subreddit at https://developers.reddit.com/apps

Built with 💜 by GestaltView
EOF

# Create deployment guide
echo "📚 Creating DEPLOYMENT.md..."
cat > insight-bot/DEPLOYMENT.md << 'EOF'
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
EOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "📂 Project structure created in: $(pwd)/insight-bot"
echo ""
echo "🚀 Next steps:"
echo "   1. cd insight-bot"
echo "   2. npm install"
echo "   3. cp .env.example .env"
echo "   4. Edit .env with your Reddit credentials (from screenshot)"
echo "   5. npm run build"
echo "   6. npm run deploy"
echo ""
echo "📖 See DEPLOYMENT.md for detailed instructions"
echo ""
echo "💜 Built for consciousness growth, not engagement extraction"
echo "   - Keith Soyka / GestaltView"
echo ""
