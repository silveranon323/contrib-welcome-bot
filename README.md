# 🤖 GitHub Contribution Bot

A GitHub Action bot that automatically comments on issues or pull requests when triggered.  
Built using **Python** and **GitHub Actions**, this bot can be reused across repositories without much modification.

---

## 🚀 Features
- Automatically posts a predefined or generated comment on issues/PRs.
- Runs on various GitHub events (`issues`, `pull_request`, etc.).
- Written in Python — easy to customize.
- Can be used in **any repository** with minimal setup.
- Supports **personal access tokens** for cross-repo usage.

---

## 📦 Installation & Setup

### 1. Create a Personal Access Token
1. Go to **[GitHub Developer Settings → Personal Access Tokens](https://github.com/settings/tokens)**
2. Generate a token with `repo` and `workflow` permissions.
3. Store it as a secret in your repo:  
   - Navigate to **Settings → Secrets and variables → Actions**
   - Add a new repository secret:
     - **Name:** `GH_TOKEN`
     - **Value:** your token

---

### 2. Add Workflow File
Create a file in your repo:  
`.github/workflows/contribution-bot.yml`

```yaml
name: GitHub Contribution Bot

on:
  issues:
    types: [opened]
  pull_request:
    types: [opened]

jobs:
  comment:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: pip install requests
      - name: Run Bot
        env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
          REPO: ${{ github.repository }}
          ISSUE_NUMBER: ${{ github.event.issue.number || github.event.pull_request.number }}
        run: python bot.py
```