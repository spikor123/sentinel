# 🛡️ Sentinel AI: Autonomous Remediation Agent

> **"Beyond Chat: The Future of Autonomous DevSecOps on GitLab."**

Sentinel AI is the first "Zero-Touch" security remediation agent built specifically for the GitLab AI Hackathon. It eliminates developer "toil" by automatically identifying, patching, and verifying security vulnerabilities in Merge Requests—before a human even has to look at the code.

## 🚀 The Vision: Beyond Chat
While most AI tools just "talk" about problems, Sentinel **acts**. 
- **The Problem:** Developers spend 75% of their time on manual tasks like security compliance and fixing minor vulnerabilities.
- **The Solution:** An autonomous teammate that monitors GitLab webhooks, uses Claude 3.5 Sonnet to "reason" through fixes, and creates verified shadow branches for one-click merging.

## ✨ Key Features
- **🧠 Contextual Remediation:** Leverages Anthropic Claude 3.5 to understand project logic and apply patches that match the existing coding style.
- **🔐 Secret Vault Migrator:** Automatically detects hardcoded secrets and migrates them to the GitLab Secrets Manager (masked CI/CD variables).
- **🌿 Pipeline Verification:** Only presents fixes that have successfully passed the existing GitLab CI/CD tests via shadow branches.
- **📊 Toil Tracker Dashboard:** A minimalist React dashboard that visualizes manual work hours saved and identifies high-risk areas in real-time.

## 🛠️ Technical Stack
- **AI Engine:** Anthropic Claude 3.5 Sonnet
- **Orchestration:** GitLab Duo Agent Platform (Tools & Triggers)
- **Backend:** Node.js / Express (Webhook Listener)
- **Frontend:** React + Vite + Lucide (Minimalist Monitoring Station)
- **API:** GitLab REST API (@gitbeaker)

## 🏗️ How it Works
1. **Trigger:** A Merge Request is opened or updated on GitLab.
2. **Analysis:** Sentinel intercepts the diff and runs a "Deep-Diff" analysis using Claude 3.5.
3. **Drafting:** If a vulnerability is found, Sentinel drafts a secure code replacement.
4. **Validation:** Sentinel creates a shadow branch, applies the fix, and triggers a CI pipeline.
5. **Remediation:** Upon success, Sentinel posts a summarized patch on the MR, ready for a one-click merge.

---
Built for the **2026 GitLab AI Hackathon**.
*"You Orchestrate. AI Accelerates."*
