# Retrieval-Augmented Generation (RAG)

Enhancing LLMs with external knowledge.

## Overview

RAG combines retrieval of relevant documents with LLM generation.

```
Query → Retrieve relevant docs → Augment prompt → Generate answer

Benefits:
- Up-to-date information
- Reduced hallucinations
- Cite sources
- Domain-specific knowledge
```

## Basic RAG Pipeline

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# 1. Load and split documents
from langchain.document_loaders import TextLoader
loader = TextLoader("document.txt")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)

# 2. Create embeddings and vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(splits, embeddings)

# 3. Create retrieval chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

# 4. Query
answer = qa_chain.run("What is the main topic of the document?")
```

## Document Processing

### Loading Different Sources
```python
from langchain.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    WebBaseLoader,
    DirectoryLoader
)

# PDF
loader = PyPDFLoader("document.pdf")
pages = loader.load()

# Web page
loader = WebBaseLoader("https://example.com/article")
docs = loader.load()

# Directory of files
loader = DirectoryLoader(
    "./documents/",
    glob="**/*.txt",
    loader_cls=TextLoader
)
docs = loader.load()

# CSV
loader = CSVLoader("data.csv")
docs = loader.load()
```

### Text Splitting Strategies

```python
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter
)

# Recursive (recommended for most cases)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)

# By tokens (for LLM context limits)
splitter = TokenTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)
```

## Vector Stores

### FAISS (Local)
```python
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

# Create
vectorstore = FAISS.from_documents(documents, embeddings)

# Save
vectorstore.save_local("faiss_index")

# Load
vectorstore = FAISS.load_local("faiss_index", embeddings)

# Search
docs = vectorstore.similarity_search("query", k=3)
```

### Chroma (Local with persistence)
```python
from langchain.vectorstores import Chroma

vectorstore = Chroma.from_documents(
    documents,
    embeddings,
    persist_directory="./chroma_db"
)

# Automatic persistence
vectorstore.persist()
```

### Pinecone (Cloud)
```python
import pinecone
from langchain.vectorstores import Pinecone

pinecone.init(api_key="key", environment="env")

vectorstore = Pinecone.from_documents(
    documents,
    embeddings,
    index_name="my-index"
)
```

## Retrieval Strategies

### Basic Similarity Search
```python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)
```

### Maximum Marginal Relevance (MMR)
Balances relevance with diversity.

```python
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 20,  # Fetch more, then diversify
        "lambda_mult": 0.5  # 0=diverse, 1=similar
    }
)
```

### Hybrid Search
Combines keyword and semantic search.

```python
from langchain.retrievers import BM25Retriever, EnsembleRetriever

# Keyword retriever
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 5

# Semantic retriever
semantic_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Combine
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, semantic_retriever],
    weights=[0.3, 0.7]
)
```

### Contextual Compression
Re-rank and compress retrieved documents.

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
)
```

## Prompt Templates

```python
from langchain.prompts import PromptTemplate

template = """Use the following pieces of context to answer the question.
If you don't know the answer, just say you don't know. Don't make up an answer.

Context:
{context}

Question: {question}

Answer: """

prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)
```

## Complete RAG Implementation

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

class RAGSystem:
    def __init__(self, documents_path):
        # Load and process documents
        loader = DirectoryLoader(documents_path, glob="**/*.txt")
        documents = loader.load()
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = splitter.split_documents(documents)
        
        # Create vector store
        embeddings = OpenAIEmbeddings()
        self.vectorstore = FAISS.from_documents(splits, embeddings)
        
        # Create chain with memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(model="gpt-3.5-turbo"),
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory=self.memory,
            return_source_documents=True
        )
    
    def query(self, question):
        result = self.chain({"question": question})
        return {
            "answer": result["answer"],
            "sources": [doc.metadata for doc in result["source_documents"]]
        }

# Usage
rag = RAGSystem("./documents/")
response = rag.query("What are the main topics covered?")
print(response["answer"])
print("Sources:", response["sources"])
```

## Advanced Techniques

### Parent Document Retriever
Store full documents but search on chunks.

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore

store = InMemoryStore()
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
)
```

### Self-Query Retriever
LLM generates structured queries for metadata filtering.

```python
from langchain.retrievers.self_query.base import SelfQueryRetriever

metadata_field_info = [
    {"name": "author", "type": "string", "description": "Author name"},
    {"name": "date", "type": "date", "description": "Publication date"},
    {"name": "category", "type": "string", "description": "Document category"}
]

retriever = SelfQueryRetriever.from_llm(
    llm,
    vectorstore,
    document_contents="Scientific papers",
    metadata_field_info=metadata_field_info
)

# Query: "papers by Einstein about relativity"
# Automatically filters by author and searches for relativity
```

### Multi-Query Retriever
Generate multiple query variations.

```python
from langchain.retrievers.multi_query import MultiQueryRetriever

retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)

# Single user query generates multiple variations
# Results are combined and deduplicated
```

## Evaluation

```python
from ragas import evaluate
from ragas.metrics import (
    context_precision,
    context_recall,
    faithfulness,
    answer_relevancy
)

# Evaluate RAG pipeline
result = evaluate(
    dataset,
    metrics=[
        context_precision,
        context_recall,
        faithfulness,
        answer_relevancy
    ]
)
```

## Quick Reference

```python
# Basic RAG flow
1. Load documents → DocumentLoaders
2. Split into chunks → TextSplitters
3. Create embeddings → Embeddings
4. Store in vector DB → VectorStores
5. Retrieve relevant chunks → Retrievers
6. Generate with context → LLM + Chain

# Key components
RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
OpenAIEmbeddings() or HuggingFaceEmbeddings()
FAISS.from_documents(docs, embeddings)
vectorstore.as_retriever(search_kwargs={"k": 5})
RetrievalQA.from_chain_type(llm, retriever=retriever)
```

## Related Topics
- [LLMs](llms.md)
- [LangChain](langchain.md)
- [Embeddings](../02_deep_learning/transformers.md)
