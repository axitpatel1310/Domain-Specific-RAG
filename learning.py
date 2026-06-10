import json
from datetime import datetime

from elasticsearch import Elasticsearch

from config import (
    ELASTIC_URL,
    llm
)

SUMMARY_INDEX = "learning_summaries"

es = Elasticsearch(ELASTIC_URL)

def generate_learning_summary(messages):

    conversation_text = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in messages
    )

    prompt = f"""
You are an educational learning analyst.

Return JSON only.

Conversation:

{conversation_text}
"""

    response = llm.invoke(prompt)

    try:
        return json.loads(response.content)
    except:
        return None


def save_learning_summary(
    profile_id,
    summary_data
):

    doc = {
        "user_id": profile_id,
        "date": datetime.now().isoformat(),
        **summary_data
    }

    es.index(
        index=SUMMARY_INDEX,
        document=doc
    )


def get_learning_summaries(profile_id):

    query = {
        "query": {
            "term": {
                "user_id": profile_id
            }
        },
        "size": 5,
        "sort": [
            {
                "date": {
                    "order": "desc"
                }
            }
        ]
    }

    result = es.search(
        index=SUMMARY_INDEX,
        body=query
    )

    summaries = []

    for hit in result["hits"]["hits"]:
        summaries.append(
            hit["_source"]["summary"]
        )

    return "\n".join(summaries)