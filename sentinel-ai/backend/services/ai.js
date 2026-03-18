const { Anthropic } = require('@anthropic-ai/sdk');
require('dotenv').config();

// We initialize the Anthropic client using the API key from the environment
const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY || 'PLACEHOLDER_KEY', // Default to placeholder if not set yet
});

/**
 * Analyzes a given code snippet or git diff for security vulnerabilities.
 * @param {string} codeDiff The git diff or source code to analyze.
 * @returns {Promise<Object>} An object containing the analysis and a suggested fix.
 */
async function analyzeCode(codeDiff) {
  try {
    const prompt = `
You are Sentinel AI, an autonomous enterprise security engineer.
Your task is to review the following Git diff or code snippet and identify ANY HIGH OR CRITICAL security vulnerabilities (e.g., hardcoded secrets, SQL injection, XSS).

If you find a vulnerability:
1. Identify the exact issue.
2. Provide a fully functional, secure code replacement (only the patched code).
3. Specify if it is a 'Secret Leak' or 'Code Vulnerability'.

Respond strictly in valid JSON format matching this schema:
{
  "hasVulnerability": boolean,
  "type": "Secret Leak" | "Code Vulnerability" | null,
  "description": string | null,
  "suggestedFix": string | null
}

CODE TO ANALYZE:
\`\`\`
${codeDiff}
\`\`\`
    `;

    // Make the API call to Claude 3.5 Sonnet
    const msg = await anthropic.messages.create({
      model: "claude-3-sonnet-20240229", // Claude 3 Sonnet is excellent for this
      max_tokens: 1500,
      temperature: 0,
      system: "You are an expert DevSecOps agent. Always respond in valid JSON without any markdown formatting wrappers or additional text.",
      messages: [
        { role: "user", content: prompt }
      ]
    });

    const responseText = msg.content[0].text.trim();
    // Parse the JSON response
    return JSON.parse(responseText);

  } catch (error) {
    console.error('Error during AI analysis:', error);
    return { hasVulnerability: false, error: 'Analysis Failed' };
  }
}

module.exports = {
  analyzeCode
};
