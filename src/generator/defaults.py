VALIDATE_CONTEXT_PROMPT = [
            {"role": "system", "content": "You are a chatbot designed to evaluate whether the given contexts are sufficient to answer a user's question accurately. Respond with '1' (yes) or '0' (no)."},
            {"role": "system", "content": """
Here are the selected story excerpts for evaluation:\n{source_knowledge}\n
User's description: {query}
User's question: Please tell me which chapter this detail is from."""},
            {"role": "user", "content": """
Based on the provided contexts, can you accurately answer the user's question? 
If yes, respond with '1'. If no, respond with '0'."""},
        ]

ANSWER_PROMPT = [
        {"role": "system", "content": "You are a chatbot that helps users identify the specific chapter of a story based on their descriptions. Respond to the user in Vietnamese."},
        {"role": "system", "content": "Details about the story excerpts:\n{source_knowledge}\nUser's description:"},
        {"role": "user", "content": "{query}\nHãy cho tôi biết tình tiết này ở chương nào."},
    ]

SUMMARIZE_PROMPT = [
    ("system", "You are a helpful assistant, answer with retrieved context {retrieved_context}"),
    ("user", "Tell me a joke about {query}")
]