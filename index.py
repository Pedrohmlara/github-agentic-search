import os
import sys
import json
import base64
import argparse
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

import requests
from agents import Agent, Runner

from agent.agent import agent

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Agentic Search over a GitHub repo (no pre-ingestion).")
    p.add_argument("--repo", required=True, help="owner/name")
    p.add_argument("--question", required=True, help="Ask a repo question")
    p.add_argument("--ref", default=None, help="branch or SHA (optional)")
    return p.parse_args()


def main():
    load_dotenv()
    args = parse_args()
    
    payload = {
        "task": "answer_question", 
        "repo": args.repo, 
        "ref": args.ref, 
        "question": args.question
    }

    response = Runner.run_sync(
        agent(), 
        json.dumps(payload)
    )

    print(response.final_output)

if __name__ == "__main__":
    main()