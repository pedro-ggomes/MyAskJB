import os
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama

from get_embedding_function import get_embedding_function

CHROMA_PATH = os.environ.get("CHROMADB_PATH")

PROMPT_TEMPLATE = """
                  You are an expert in Jitterbit and Jitterbit documentation. 
                  Your task is to assist me by providing accurate and detailed information 
                  based exclusively on the official Jitterbit documentation. Please avoid 
                  speculation, and if something is unclear or not covered in the documentation,
                  indicate that explicitly. Always cite the relevant section or provide reference
                  links to the specific parts of the documentation when answering. context:
                  
                  {context}
                  
                  ---
                  
                  Answer the question based on the above context: {question}
                  """

def query_rag(query_text: str):
	# Prepare the DB.
	embedding_function = get_embedding_function()
	db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

	# Search the DB.
	results = db.similarity_search_with_score(query_text, k=2)

	context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
	prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
	prompt = prompt_template.format(context=context_text, question=query_text)
	print(prompt)

	model = Ollama(model="mistral")
	response_text = model.invoke(prompt)

	sources = [doc.metadata.get("id", None) for doc, _score in results]
	formatted_response = f"Response: {response_text}\nSources: {sources}"
	print(formatted_response)
	return response_text
