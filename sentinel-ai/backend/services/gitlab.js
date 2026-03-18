const { Gitlab } = require('@gitbeaker/rest');
require('dotenv').config();

// We need the GitLab Personal Access Token or Project Token
const api = new Gitlab({
  host: 'https://gitlab.com', // or self-hosted URL
  token: process.env.GITLAB_TOKEN || 'PLACEHOLDER_TOKEN',
});

/**
 * Creates a remediation branch, commits the fix, and opens a Merge Request.
 * @param {number} projectId 
 * @param {string} sourceBranch The MR source branch
 * @param {string} fixedCode The securely patched code to overwrite the vulnerable file.
 * @param {string} filePath Path to the vulnerable file in the repo.
 */
async function applySentinelPatch(projectId, sourceBranch, fixedCode, filePath) {
  try {
    const sentinelBranch = `sentinel/fix-${Date.now()}`;

    // 1. Create a shadow branch off the developer's source branch
    await api.Branches.create(projectId, sentinelBranch, sourceBranch);
    console.log(`Shadow branch created: ${sentinelBranch}`);

    // 2. Commit the fixed code to the new shadow branch
    await api.Commits.create(
      projectId,
      sentinelBranch,
      `[Sentinel] Security Patch: Remediation applied on ${filePath}`,
      [
        {
          action: 'update',
          filePath: filePath,
          content: fixedCode,
        }
      ]
    );
    console.log(`Security patch committed to ${sentinelBranch}`);

    // 3. (Optional / Advanced) We could open a new MR here or update the existing one.
    // For this hackathon scope, we can post a comment back to the original MR indicating the branch is ready.
    return { success: true, branch: sentinelBranch, fallback: false };
    
  } catch (error) {
    console.error('GitLab Integration Error:', error);
    return { success: false, error: 'Failed to apply patch' };
  }
}

/**
 * Posts a comment summarizing the findings to the MR thread.
 */
async function notifyMergeRequest(projectId, mrIid, analysisResult, sentinelBranch) {
  try {
    let message = `### 🛡️ Sentinel AI Security Scan\n`;
    
    if (analysisResult.hasVulnerability) {
      message += `🚨 **Vulnerability Detected:** ${analysisResult.type}\n`;
      message += `**Details:** ${analysisResult.description}\n\n`;
      message += `✅ **Remediation Ready:** I have automatically verified a fix and committed it to a shadow branch: \`${sentinelBranch}\`.\n`;
      message += `Please review and merge the shadow branch to resolve this issue.`;
    } else {
      message += `✅ Zero vulnerabilities found in this diff. You are good to go!`;
    }

    await api.MergeRequestNotes.create(projectId, mrIid, message);
    console.log(`Posted notification to MR #${mrIid}`);
  } catch (err) {
    console.error('Failed to notify MR:', err);
  }
}

module.exports = {
  applySentinelPatch,
  notifyMergeRequest
};
