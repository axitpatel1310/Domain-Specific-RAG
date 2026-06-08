from datetime import datetime
import json

PERSONALITY_INDEX = "personality_profiles"


def generate_personality_profile(llm, messages):

    conversation_text = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in messages
    )

    prompt = f"""
Analyze the user's personality.

Return JSON only.

{{
    "traits": [],
    "communication_style": "",
    "learning_behavior": "",
    "motivation_style": ""
}}

Conversation:

{conversation_text}
"""

    response = llm.invoke(prompt)

    try:
        return json.loads(response.content)

    except Exception:
        return None


def save_personality_profile(es, profile_id, profile):

    doc = {
        "user_id": profile_id,
        "updated_at": datetime.now().isoformat(),
        **profile
    }

    es.index(
        index=PERSONALITY_INDEX,
        document=doc
    )