import json
import logging
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from src.config import settings

logger = logging.getLogger("AI_Engine")
client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a Lead Qualification Agent. Your job is to read Reddit posts and decide if the user is a potential customer for our product: "RedditHelper - A tool that automates lead generation on Reddit."

Output strictly in JSON format with these keys:
- "score" (int): 0-100 relevance score.
- "reason" (str): Brief explanation of why this is/isn't a lead.
- "draft_reply" (str): A helpful, casual, non-salesy comment. (Only if score > 75).
"""


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def analyze_lead(post_title: str, post_body: str) -> dict:
    """
    Analyzes a post and returns a structured dictionary.
    Retries automatically on API failure.
    """
    user_content = f"Title: {post_title}\n\nBody: {post_body}"

    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"},  # Critical: Forces valid JSON
            temperature=0.7
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        # Fallback for missing keys (Defensive Coding)
        if "score" not in data: data["score"] = 0
        if "reason" not in data: data["reason"] = "AI Error: Missing reason"

        return data

    except json.JSONDecodeError:
        logger.error("AI returned invalid JSON.")
        return {"score": 0, "reason": "JSON Parse Error"}
    except Exception as e:
        logger.error(f"OpenAI API Error: {e}")
        raise  # Let Tenacity handle the retry