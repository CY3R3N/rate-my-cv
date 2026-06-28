# src/llm/prompts/gap_analyser.py

from langchain_core.messages import HumanMessage, SystemMessage

def gap_analyser_prompt(resume_context: str, job_description: str) -> str:
    return f"""
You are a career advisor helping a candidate identify skill gaps.

Compare the resume below against the job description and identify what's missing.

RESUME:
{resume_context}

JOB DESCRIPTION:
{job_description}

Provide:
1. Missing technical skills
2. Missing experience or domain knowledge
3. Three concrete actions the candidate can take to close these gaps

Be specific and actionable.
"""

def get_gap_analysis(llm, resume_context: str, job_description: str) -> str:
    prompt = gap_analyser_prompt(resume_context, job_description)
    messages = [
        SystemMessage(content="You are a career advisor who gives honest, actionable gap analysis."),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)
    return response.content