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
