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
