import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader
import json


class RAG:
    """
    Implements Retrieval Augmented Generation with a given configuration
    

    use get_relavant_context with your large file path, query string and collection name after RAG class instantiation
    """
    def __init__(self, config_file) -> None:
        """
        Initialize the RAG instance

        :config_file: Initialize with mllm config file. Please provide following info in the config file \n

        chunk_size: int, number of characters in each chunk \n
        chunk_overlap: int, overlap characters \n
        max_chunk_size: int, maximum number of characters in a chunk. depends on embedding model \n
        db_path: str, path where to save the vector database file \n
        k_matches: int, top k mataches to retrieve \n
        credentials_openai: str, path to openai credential file (make sure key value format {"api_key" : "your key"})
        """
        try:
            self.config_content: dict[str, str | int] = read_file(config_file)["Config"]["VectorStore"]
        except FileNotFoundError:
            FileNotFoundError("Please check the path of config file and make sure you have provided VectorStore key with all the required key-value pairs")
        self.chunk_size = self.config_content["chunk_size"]
        self.chunk_overlap = self.config_content["chunk_overlap"]
        self.max_chunk_size = self.config_content["max_chunk_size"]
        self.db_path = self.config_content["db_path"]
        self.credentials_openai = self.config_content["credentials_openai"]
        self.k = self.config_content["k_matches"]

    def chunk_large_file(self, file_path: str) -> list[str]:
        """
        Chunks large string into chunks of smaller strings. 
        Takes chunk size, overlap size in number of characters from config file

        :file_path: path of large file 
        """
        file_content = read_file(file_path)
        splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        chunks = splitter.split_text(text=file_content)
        return chunks

    def get_embedding_model(self, embedding_source: str):
        if embedding_source == "openai":
            credentials = read_file(self.credentials_openai)
            OPENAI_API_KEY = credentials["api_key"]
            embedding_model = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
        else:
            print("This is a placeholder for other embedding models")
        return embedding_model

    def get_vector_store(self, file_path: str, collection="VerifaiDB"):
        """
        Fetches if collection exists in vector BD
        or Creates a vector database for given collection name from a file
        
        :file_path: path to the user file
        :collection: name of collection, default="VerifaiDB"
        """
        client = chromadb.PersistentClient(path=self.db_path)
        collections_list = [c.name for c in client.list_collections()]
        embedding_model = self.get_embedding_model(embedding_source="openai")
        
        vector_store = Chroma(collection_name=collection, embedding_function=embedding_model,
                            persist_directory=self.db_path, collection_metadata={"source": "dev uploaded data"})

        if collection not in collections_list:
            text_chunks = self.chunk_large_file(file_path=file_path)
            vector_store.add_texts(texts=text_chunks)

        return vector_store

    def get_relevant_context(self, user_file: str, query: str, collection: str = "VerifaiDB") -> dict[str, str]:
        """
        
        """
        vectorstore = self.get_vector_store(file_path=user_file, collection=collection)

        # Perform Queries
        results = vectorstore.similarity_search_with_score(query=query, k=self.k)
        context = '. '.join(result.page_content for result, score in results)
        return context



##------------------------Utility Functions------------------------------

# Read files
def read_file(file_path: str) -> str:
    try:
        if file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
            output_text = []
            for page in reader.pages:
                page_text = page.extract_text()
                processed_text = process_text(page_text)
                output_text.append(processed_text)
            return " ".join(output_text)
            # return output_text
        elif file_path.endswith(".json"):
            with open(file_path, "r") as file:
                return json.load(file)
        else:
            with open(file_path, "r") as file:
                return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"'{file_path}' not found.")

def process_text(text: str) -> str:
    cleaned_text  = []
    lines: list[str] = text.split("\n")
    for line in lines:
        cleaned_text.append(line.strip())
    return "\n".join(cleaned_text)

##-------------------Unit tests------------------------------------
if __name__ == "__main__":
    config_path = "/data/mihir/mllm/config.json"
    file_path = "/data/mihir/mllm_temp/Activation-Functions.pdf"
    my_collection = "VerifaiDB"

    query = "what is sigmoid activation?"
    msg = RAG(config_path).get_relevant_context(file_path, query, my_collection)
    print(msg)