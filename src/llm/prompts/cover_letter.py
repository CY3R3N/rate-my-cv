# src/llm/prompts/cover_letter.py

from langchain_core.messages import HumanMessage, SystemMessage

def cover_letter_prompt(resume_context: str, job_description: str) -> str:
    return f"""
You are an expert career coach who writes compelling, authentic cover letters.

Using ONLY the experience and skills mentioned in the resume below, write a tailored cover letter for the job description provided.
Do NOT invent or assume any experience not present in the resume.

RESUME:
{resume_context}

JOB DESCRIPTION:
{job_description}

Write a professional cover letter with:
- An engaging opening paragraph
- 2 middle paragraphs linking the candidate's real experience to the role
- A confident closing paragraph

Keep it under 350 words.
"""

def get_cover_letter(llm, resume_context: str, job_description: str) -> str:
    prompt = cover_letter_prompt(resume_context, job_description)
    messages = [
        SystemMessage(content="You are a professional cover letter writer. Only use information explicitly present in the resume."),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)
    return response.content