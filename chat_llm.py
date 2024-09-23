import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_chroma import Chroma
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain

API_KEY = os.environ.get("OPENAI_APIKEY")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, max_tokens=500, api_key=API_KEY)

memory = ConversationBufferMemory(memory_key="chat_history", return_message=True)

embeddings = OpenAIEmbeddings(api_key=API_KEY)

vector_db = Chroma(embedding_function=embeddings,collection_name="myaskjb",persist_directory="./chroma_db")

retriever = ContextualCompressionRetriever(
    base_compressor = LLMChainExtractor.from_llm(llm),
    base_retriever = vector_db.as_retriever()
)

promp_template = ChatPromptTemplate.from_template("""
                                              Context: {context}
                                              Chat History: {chat_history}
                                              Human: {question}
                                              AI: Please provide a relevant answer based on context and chat history.
                                              """)

chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs = {"prompt": promp_template}
)

def chat_response(user_input:str) -> str:
    print(API_KEY)
    return chain({"question":user_input})["answer"]