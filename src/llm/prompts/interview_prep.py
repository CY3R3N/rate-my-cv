# src/llm/prompts/interview_prep.py

from langchain_core.messages import HumanMessage, SystemMessage

def interview_prep_prompt(resume_context: str, job_description: str) -> str:
    return f"""
You are an interview coach preparing a candidate for a job interview.

Based on the resume and job description below, generate likely interview questions and suggested answer frameworks.

RESUME:
{resume_context}

JOB DESCRIPTION:
{job_description}

Provide 5 interview questions with:
- The question
- Why the interviewer is asking it
- A suggested answer framework based on the candidate's actual experience

Focus on questions that expose the gap between the candidate's background and the role requirements.
"""

def get_interview_prep(llm, resume_context: str, job_description: str) -> str:
    prompt = interview_prep_prompt(resume_context, job_description)
    messages = [
        SystemMessage(content="You are an expert interview coach who gives practical, grounded preparation advice."),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)
    return response.content