def is_summary_request(question):

    phrases = [
        "conversation summary",
        "show my summary",
        "what have we discussed",
        "What are my strengths?",
        "What are my weaknesses?",
        "What are my learning gaps?"
    ]

    question = question.lower()

    return any(
        phrase in question
        for phrase in phrases
    )