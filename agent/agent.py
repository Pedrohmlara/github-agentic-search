import os
from agents import Agent
from dotenv import load_dotenv
from agent.tools import list_repo_tree, get_readme, search_code, get_file_content, get_prs, get_issues

load_dotenv()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

def agent():
    sp = """
        You are a senior engineer doing on-demand Agentic Search over a GitHub repo.
        Plan briefly, then call tools to:
        - list tree, get README, search code, fetch file contents, list PRs/issues.
        Be concise and factual. Cite file paths and include short relevant snippets from files you read.
        Prefer targeted search before opening large files. If uncertain, say what else you would check.
        Do not invent paths; only cite files you actually fetched via tools.
        Do not call more than 5 tools.
        Stop as soon as you have enough evidence to answer.
    """

    return Agent(
        name="GitHubResearcher",
        instructions=sp,
        model=OPENAI_MODEL,
        tools=[list_repo_tree, get_readme, search_code, get_file_content, get_prs, get_issues],
    )