from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(temperature=0.2)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

INTENT_PROMPT = PromptTemplate(
    input_variables=["input", "chat_history"],
    template="""
You are a sales assistant AI.

Conversation history:
{chat_history}

User input:
{input}

Classify the intent into one of:
- GET_DAILY_TASK
- SUBMIT_SALES_REPORT
- GET_PERFORMANCE
- OTHER

Return ONLY the intent.
"""
)

def detect_intent(user_input: str):
    response = llm.predict(
        INTENT_PROMPT.format(
            input=user_input,
            chat_history=memory.buffer
        )
    )

    memory.save_context(
        {"input": user_input},
        {"output": response}
    )

    return response.strip()
