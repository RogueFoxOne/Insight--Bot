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
