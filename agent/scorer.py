import os
import json
from groq import Groq
from agent.prompt_builder import RUBRIC

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def score_policy(policy_text: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": RUBRIC},
            {"role": "user", "content": (
                "Score the following privacy policy using the rubric. "
                "Respond ONLY with a JSON object, no other text:\n\n"
                + policy_text[:8000]
            )}
        ],
        temperature=0,
        max_tokens=512
    )
    raw = response.choices[0].message.content.strip()
    print("RAW RESPONSE:", repr(raw[:300]))

    # Extract JSON from anywhere in the response
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError(f"No JSON found in response: {raw[:200]}")
    
    return json.loads(raw[start:end])