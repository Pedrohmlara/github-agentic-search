# GitHub Agentic Search

A CLI tool that answers questions about a GitHub repository on demand, without pre-ingestion. It fetches the repo tree, README, searches code, and inspects files, PRs, and issues via the GitHub API.

## Prerequisites
- Python 3.10+ installed and available as `python3`
- A GitHub Personal Access Token (classic or fine-grained) with `repo` read permissions
- An OpenAI API key to run the agent model
- macOS/Linux shell (examples use zsh/bash)

## Quick Start

### 1) Clone the repository
```bash
git clone https://github.com/<your-username>/github-agentic-search.git
cd github-agentic-search
```

### 2) Create and activate a virtual environment (Python 3)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4) Configure environment variables
Create a `.env` file in the project root with the following variables:

```bash
GITHUB_TOKEN=ghp_your_personal_access_token
OPENAI_API_KEY=sk-your_openai_api_key
```

Notes:
- Check how to get a GitHub Acess Token [Here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- `OPENAI_MODEL` defaults to `gpt-5-mini` if omitted.

### 5) Run the CLI
The CLI entrypoint is `index.py`. Use: 
- `--repo` as `owner/name`
- `--question` as your query
- `--ref` for a branch or commit SHA (Optional).

```bash
python index.py --repo owner/name --question "What is the deployment process?" --ref main
```

Examples:
```bash
# Ask about project structure
python index.py --repo pytorch/pytorch --question "Where is the build configuration defined?"

# Ask about recent PRs/issues (agent may check PRs/issues if relevant)
python index.py --repo owner/private-repo --question "What PR added feature X?" --ref 123abc4
```

## Output
- The tool prints a concise, sourced answer to stdout.
- Responses may cite paths like `path/to/file.py` and include short snippets from fetched files.
- If information is uncertain, it may state additional places it would check.