from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

llm = ChatOpenAI()
memory = ConversationBufferMemory()

def understand_query(text):
    memory.save_context({"input": text}, {"output": ""})
    return llm.predict(text)
