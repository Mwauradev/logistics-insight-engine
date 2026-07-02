from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)

def generate_insight(system_prompt: str, user_prompt: str, max_tokens: int = 300) -> str:
    
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        max_tokens=max_tokens,
        temperature=0.7
    )
    
    return response.choices[0].message.content

