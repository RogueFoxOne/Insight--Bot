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
