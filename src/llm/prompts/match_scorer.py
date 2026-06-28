# src/llm/prompts/match_scorer.py

from langchain_core.messages import HumanMessage, SystemMessage

def match_score_prompt(resume_context: str, job_description: str) -> str:
    return f"""
You are an expert recruiter and resume analyst.

Below is a candidate's resume and a job description.
Analyse how well the candidate matches the role.

RESUME:
{resume_context}

JOB DESCRIPTION:
{job_description}

Respond in this exact format:
Match Score: [number]/100

Strong Matches:
- [point]

Weak Matches:
- [point]

Overall Verdict: [one sentence]
"""

def get_match_score(llm, resume_context: str, job_description: str) -> str:
    prompt = match_score_prompt(resume_context, job_description)
    messages = [
        SystemMessage(content="You are a professional recruiter who gives honest, structured feedback."),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)
    return response.content