from src.ingestion.resume_parser import parse_resume
from src.preprocessing.cleaner import clean_text
from src.preprocessing.chunker import chunk_text

text = parse_resume("src/ingestion/Ahnaf_s_Resume1.pdf")
cleaned = clean_text(text)
chunks = chunk_text(cleaned)

print(f"Total chunks: {len(chunks)}")
print(f"\n--- Chunk 1 ---\n{chunks[0]}")
print(f"\n--- Chunk 2 ---\n{chunks[1]}")

from src.embeddings.embedder import load_embedder

embedder = load_embedder()

# test it on one chunk
test_vector = embedder.embed_query(chunks[0])

print(f"Embedding dimension: {len(test_vector)}")
print(f"First 5 values: {test_vector[:5]}")


# Vector store
from src.embeddings.vector_store import build_vector_store, search_vector_store

# build the index from your resume chunks
vector_store = build_vector_store(chunks, embedder)

# test with a sample query
query = "What are this person's technical skills?"
results = search_vector_store(vector_store, query)

print(f"\n--- Top matching chunks for: '{query}' ---")
for i, result in enumerate(results):
    print(f"\n[{i+1}] {result}")

#llm client

from src.llm.llm_client import load_llm

llm = load_llm()

# quick test
response = llm.invoke("Say hello in one sentence.")
print(f"\nLLM test: {response.content}")


# Match scorer
from src.llm.prompts.match_scorer import get_match_score

# sample job description to test with
job_description = """
We are looking for a Machine Learning Engineer with experience in:
- Python and ML frameworks (PyTorch, scikit-learn)
- NLP and LLM integration
- REST API development
- Cloud platforms (AWS or Azure)
- Strong communication and teamwork skills
"""

# join top retrieved chunks as context
resume_context = "\n\n".join(results)  # results from your vector store search earlier

score = get_match_score(llm, resume_context, job_description)
print(f"\n--- Match Score ---\n{score}")


# Cover letter
from src.llm.prompts.cover_letter import get_cover_letter

cover_letter = get_cover_letter(llm, resume_context, job_description)
print(f"\n--- Cover Letter ---\n{cover_letter}")


# gap analyzer and interview prep

from src.llm.prompts.gap_analyser import get_gap_analysis
from src.llm.prompts.interview_prep import get_interview_prep

gaps = get_gap_analysis(llm, resume_context, job_description)
print(f"\n--- Gap Analysis ---\n{gaps}")

interview = get_interview_prep(llm, resume_context, job_description)
print(f"\n--- Interview Prep ---\n{interview}")

from src.llm.prompts.ats_scanner import get_ats_scan

ats = get_ats_scan(llm, resume_context, job_description)
print(f"\n--- ATS Scan ---")
print(f"ATS Score: {ats['ats_score']}")
print(f"Found: {ats['found']}")
print(f"Missing: {ats['missing']}")
print(f"Verdict: {ats['verdict']}")