from langchain_community.document_loaders import JSONLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

embedding_function = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2")

loader = JSONLoader(file_path="../response.json",
                    jq_schema=".data[]", text_content=False)
documents = loader.load()

db = Chroma.from_documents(documents, embedding_function)
query = "Is G2 useful?"
docs = db.similarity_search(query)
print(docs[0].page_content)
