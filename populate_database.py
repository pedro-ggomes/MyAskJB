import os
import shutil
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders.json_loader import JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from get_embedding_function import get_embedding_function
from langchain.vectorstores.chroma import Chroma


CHROMA_PATH = os.environ.get("CHROMADB_PATH")
DATA_PATH = os.environ.get("DATA_PATH")

def main():
	# Create (or update) the data store.
	documents = load_documents(DATA_PATH)
	chunks = split_documents(documents)
	add_to_chroma(chunks)
	print("✨ Documents added to Database")


def load_documents(path:str):
	document_loader = DirectoryLoader(path,
                                      glob="**/*.json",
                                      show_progress=True,
                                      loader_cls=JSONLoader,
                                      loader_kwargs={'jq_schema':".[] | {url: .url, text: .text}","text_content":False})
	return document_loader.load()


def split_documents(documents: list[Document]):
	text_splitter = RecursiveCharacterTextSplitter(
		chunk_size=1000,
		chunk_overlap=100,
		length_function=len,
		is_separator_regex=False,
	)
	return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document]):
	# Load the existing database.
	db = Chroma(
		persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
	)
	print(chunks[0].metadata.get("source"), chunks[0].metadata.get("seq_num"))

	# Calculate Page IDs.
	chunks_with_ids = calculate_chunk_ids(chunks)

	# Add or Update the documents.
	existing_items = db.get(include=[])  # IDs are always included by default
	existing_ids = set(existing_items["ids"])
	print(f"Number of existing documents in DB: {len(existing_ids)}")

	# Only add documents that don't exist in the DB.
	new_chunks = []
	for chunk in chunks_with_ids:
		if chunk.metadata["id"] not in existing_ids:
			new_chunks.append(chunk)

	# Batch the insertion of new documents
	if len(new_chunks) > 0:
		print(f"👉 Adding new documents: {len(new_chunks)}")
		batch_size = 1000
		for i in range(0, len(new_chunks), batch_size):
			batch = new_chunks[i:i + batch_size]
			new_chunk_ids = [chunk.metadata["id"] for chunk in batch]
			db.add_documents(batch, ids=new_chunk_ids)
			print(f"Batch {i//batch_size + 1}: Added {len(batch)} documents")
			
	else:
		print("✅ No new documents to add")


def calculate_chunk_ids(chunks):

	# This will create IDs like "scrape_jitterbit_result/1-output2024-09-27T20-05-22.992580+00-00.json:6:2"
	# Document Source : Sequential Number : Chunk Index

	last_document_id = None
	current_chunk_index = 0

	for chunk in chunks:
		source = chunk.metadata.get("source")
		seq_num = chunk.metadata.get("seq_num")
		current_document_id = f"{source}:{seq_num}"

		# If the page ID is the same as the last one, increment the index.
		if current_document_id == last_document_id:
			current_chunk_index += 1
		else:
			current_chunk_index = 0

		# Calculate the chunk ID.
		chunk_id = f"{current_document_id}:{current_chunk_index}"
		last_document_id = current_document_id

		# Add it to the page meta-data.
		chunk.metadata["id"] = chunk_id

	return chunks


def clear_database():
	if os.path.exists(CHROMA_PATH):
		shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
	main()
