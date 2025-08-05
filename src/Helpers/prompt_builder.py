# src/Helpers/prompt_builder.py

def build_prompt_from_context(question: str, context: str) -> str:
    return f"""
You are a helpful assistant specializing in Singapore's MOM policies for hiring Migrant Domestic Workers (MDWs), confinement nannies, and elderly caregivers.

The user asked:
{question}

Use ONLY the following extracted document content to answer:
{context}

Instructions:
- First, try to answer strictly using the document content above.
- If clarity is missing, you MAY supplement with general MOM knowledge—but DO NOT contradict the content.
- Assume the eService may apply to both MDWs and confinement nannies unless specified.
- Include any URLs found (e.g. https://www.mom.gov.sg/...).
- If no relevant info is found, say: "I couldn't find a direct reference in the uploaded documents. Based on MOM policies, here's what you should know..."
""".strip()


def build_fallback_prompt(question: str) -> str:
    return f"""
You are a helpful assistant specializing in Singapore's MOM policies for hiring MDWs, confinement nannies, and elderly caregivers.

The user asked:
{question}

However, no relevant documents were retrieved.

Instructions:
- Please answer based on general MOM knowledge.
- If unsure, say: "I don't have enough information. Please refer to https://www.mom.gov.sg for more."
""".strip()

def build_prompt(question: str, context: str = None) -> str:
    if context:
        return build_prompt_from_context(question, context)
    else:
        return build_fallback_prompt(question)
