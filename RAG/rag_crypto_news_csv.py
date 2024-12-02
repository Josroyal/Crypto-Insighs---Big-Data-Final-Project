
# Import necessary libraries
import os
import csv  # Added import for handling CSV operations
from pymongo import MongoClient
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain_core.vectorstores import InMemoryVectorStore
from langchain import hub
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

# Replace with your database and collection names
database_name = 'cryptonews'
collection_name = 'bitcoin news'

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client[database_name]
collection = db[collection_name]
documents = list(collection.find())

# Close the MongoDB connection
client.close()

# Create LangChain Document objects
docs = []
for doc in documents:
    title = doc.get('title', '')
    description = doc.get('description', '')
    content = doc.get('content', '')

    # Combine title, description, and content
    full_content = f"{title}\n\n{description}\n\n{content}"

    # Create a Document with content and metadata
    langchain_doc = Document(
        page_content=full_content,
        metadata={
            'url': doc.get('url', ''),
            'source': doc.get('source', ''),
            'published': doc.get('published', '')
        }
    )
    docs.append(langchain_doc)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

split_docs = text_splitter.split_documents(docs)
embedding_model = OpenAIEmbeddings()
vector_store = InMemoryVectorStore(embedding_model)

_ = vector_store.add_documents(documents=split_docs)

llm = ChatOpenAI(model="gpt-4o-mini")

# Define prompt for question-answering
prompt = hub.pull("rlm/rag-prompt")


# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}
    

# Compile application and test
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

# Define the list of questions
questions = [
    "Cuales son las ultimas noticias de bitcoin",
    "Es un buen momento para comprar criptomonedas?",
    "Estamos en un bear or bullish market segun las noticias?"
]

# Prepare a list to hold query-response pairs
qa_pairs = []

# Iterate over each question, get the answer, and store the pair
for question in questions:
    response = graph.invoke({"question": question})
    answer = response["answer"]
    print(f"Q: {question}\nA: {answer}\n")
    qa_pairs.append({"query": question, "response": answer})

# Define the CSV file name
csv_file_name = "ai_rag_insights.csv"

# Write the query-response pairs to the CSV file
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['query', 'response']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for pair in qa_pairs:
        writer.writerow(pair)

print(f"Query and responses have been saved to {csv_file_name}")
