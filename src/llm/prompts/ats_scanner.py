# src/llm/prompts/ats_scanner.py

import json
import re
from langchain_core.messages import HumanMessage, SystemMessage

def ats_scanner_prompt(resume_context: str, job_description: str) -> str:
    return f"""
You are an ATS (Applicant Tracking System) expert.

Analyse the job description and resume below.

Extract the most important keywords from the job description — technical skills, tools, qualifications, and role-specific terms.

Then check each keyword against the resume and classify it as FOUND or MISSING.

RESUME:
{resume_context}

JOB DESCRIPTION:
{job_description}

Respond ONLY with a JSON object in this exact format, no other text:
{{
  "ats_score": <number 0-100 based on keyword match percentage>,
  "found": ["keyword1", "keyword2", ...],
  "missing": ["keyword1", "keyword2", ...],
  "verdict": "<one sentence ATS likelihood assessment>"
}}
"""

def get_ats_scan(llm, resume_context: str, job_description: str) -> dict:
    messages = [
        SystemMessage(content="You are an ATS expert. Respond only with valid JSON, no markdown, no explanation."),
        HumanMessage(content=ats_scanner_prompt(resume_context, job_description))
    ]
    response = llm.invoke(messages)
    text = response.content.strip()

    # Strip markdown fences if LLM adds them anyway
    text = re.sub(r'^```json|^```|```$', '', text, flags=re.MULTILINE).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "ats_score": 0,
            "found": [],
            "missing": [],
            "verdict": "Could not parse ATS results. Try again."
        }