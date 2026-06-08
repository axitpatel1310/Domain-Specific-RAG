from datetime import datetime
import json


PROFILE_INDEX = "user_profiles"


def generate_user_profile(llm, messages):

    conversation_text = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in messages
    )

    prompt = f"""
You are a user profiling analyst.

Analyze the conversation.

Return JSON only.

{{
    "interests": [],
    "goals": [],
    "experience_level": "",
    "learning_style": "",
    "strengths": [],
    "struggles": []
}}

Conversation:

{conversation_text}
"""

    response = llm.invoke(prompt)

    try:
        return json.loads(response.content)

    except Exception:
        return None


def save_user_profile(es, profile_id, profile):

    doc = {
        "user_id": profile_id,
        "updated_at": datetime.now().isoformat(),
        **profile
    }

    es.index(
        index=PROFILE_INDEX,
        document=doc
    )


def get_user_profile(es, profile_id):

    query = {
        "query": {
            "term": {
                "user_id": profile_id
            }
        },
        "size": 1,
        "sort": [
            {
                "updated_at": {
                    "order": "desc"
                }
            }
        ]
    }

    result = es.search(
        index=PROFILE_INDEX,
        body=query
    )

    hits = result["hits"]["hits"]

    if not hits:
        return None

    return hits[0]["_source"]