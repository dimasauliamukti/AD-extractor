from langchain_ollama.chat_models import ChatOllama
import asyncio
import json

chat = ChatOllama(model="llama3.1:8b", temperature=0.0,base_url="http://127.0.0.1:11434")

async def output(tags,content):
    if "applicability" in tags:
       instruction = """
        Based on the paragraph below, answer the following questions and return ONLY a JSON object.

        Questions:
        1. What aircraft models are affected by this AD? List all variants explicitly.
        2. Are there any MSN (Manufacturer Serial Number) constraints?
        - If the AD applies to all MSNs, return ["ALL"].
        - If a specific range or list of MSN numbers is given, return ONLY those numbers or ranges.
        - If no MSN constraints are mentioned, return an empty list.
        3. Which Service Bulletins or modifications EXEMPT an aircraft from this AD?
        - Look for phrases such as "except", "unless", or "not applicable if".
        - Return ONLY modification or Service Bulletin identifiers.
        - If none are mentioned, return an empty list.
        4. Which modifications MUST be present for this AD to apply?
        - ONLY fill this if the text explicitly states that applicability depends on a modification already being installed.
        - Otherwise, return an empty list.

        STRICT RULES:
        - msn_constraints MUST contain ONLY serial numbers or the token "ALL".
        - Do NOT include exception clauses, modification names, or sentences in msn_constraints.
        - Do NOT invent JSON sub-structures (no objects, only lists of strings).
        - Compliance actions or paragraphs MUST NOT be treated as required_modifications.
        - Approval authorities (e.g. FAA, EASA, Boeing ODA) are NOT modifications.
        - A modification MUST NOT appear in both "excluded_if_modifications" and "required_modifications".
        - AD numbers, Emergency ADs, or superseded ADs MUST NEVER appear in excluded_if_modifications or required_modifications.
        - If the text refers only to replacing or superseding another AD, return an empty list.

        Return format:
        {
        "aircraft_models": [],
        "msn_constraints": ,
        "excluded_if_modifications": [],
        "required_modifications": []
        }
        """
   
    elif "ad_number" in tags:
        instruction = """
        Based on the paragraph below, answer these questions and return ONLY a JSON object:

        Questions:
        1. What is the current AD number? Include both:
        - The issuing authority (e.g., "FAA", "EASA")
        - The AD number itself (e.g., "2025-0254R1")
        - Format rule: Use "IssuingAuthority AD Number" (e.g., "EASA AD 2025-0254"). 
            If the AD number contains any letters or extra characters, remove the first letter found and all characters that follow it.
        - If no AD number is found, return only the issuing authority in the format above.
        - Do NOT include punctuation other than the dash (-).

        Do NOT extract superseded ADs or references; only the current AD in the header/title.
        2. What is the effective date of this AD?
        - Search for the phrase "Effective Date" first.
        - If no "Effective Date" is found, search for "Issued", "Issue Date", or similar synonyms.  
        - Make sure the year of the date matches the year in the AD number.  

        Return format:
        {
        "ad_id": "",
        "effective_date": ""
        }
        """
    
    else:
        instruction = """
        Based on the paragraph below, answer this question and return ONLY a JSON object:

        Question:
        What is the actual unsafe condition that led to the issuance of this AD? Focus only on the condition or defect that was observed or identified at the time the AD was issued. Do NOT include predicted consequences, hypothetical risks, or administrative/procedural text such as "this AD is revised".
        
        STRICT
        - Do NOT include any sentence containing phrases like "could result in", "may lead to", "might cause".

        Return format:
        {
            "reason": ""
        }
        """

        
    prompt = f"""
    {instruction}

    PARAGRAPH:
    {content}

    OUTPUT REQUIREMENTS:
    - Return ONLY valid JSON
    - No markdown (no ```json wrapper)
    - No explanation outside the JSON
    - If information is not found, use null or []

    OUTPUT:
    """
    answer=await chat.ainvoke(prompt)
    try:
        parsed = json.loads(answer.content)
    except json.JSONDecodeError:
        parsed = None 

    return {tags: parsed}




