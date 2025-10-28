import { Devvit } from '@devvit/public-api';
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
