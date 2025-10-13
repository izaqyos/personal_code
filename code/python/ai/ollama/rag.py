import ollama 
import bs4 #bs4 is a library for parsing HTML and XML documents, that produces a tree of Pythonic Tag, NavigableString and BeautifulSoup objects.

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma 
from langchain_community.embeddings import OllamaEmbeddings 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

#We load web page content, convert it to embeddings and then pass to ollama
#create the web loader
loader = WebBaseLoader(web_paths=['https://www.gutenberg.org/cache/epub/10830/pg10830-images.html',],
                       bs_kwargs=dict(
                           parse_only=bs4.SoupStrainer(
                               class_=("post_content", "post_title", "post_header")
                           )
                       ))

#load the web content into a bs4 soup object document
docs = loader.load()
print(f"loaded docs {docs}")

#create the text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#actually perform the split operation
splits = text_splitter.split_documents(docs)

#now create ollama embeddings and vectore store 
embeddings = OllamaEmbeddings(model='mistral')
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

#now create the retriever
retriever = vectorstore.as_retriever()
 
def format_docs(docs):
    return '\n'.join(doc.page_content for doc in docs)

#now define the question answering function  that will be used to answer questions using OLLAMA LLM
def ollama_llm(question, context):
    formatted_prompt = f"Question: {question}\n\nContext: {context}"
    response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': formatted_prompt}])
    return response['message']['content']
    
#define the RAG chain function that will be used to answer questions using OLLAMA LLM
def rag_chain(question):
    retrieved_docs = retriever.invoke(question)
    formatted_context = format_docs(retrieved_docs)
    return ollama_llm(question, formatted_context)

result=rag_chain('What is on the news today?')
print(f"Result: {result}")

