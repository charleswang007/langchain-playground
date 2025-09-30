from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureChatOpenAI,AzureOpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore

import os
from dotenv import dotenv_values
config = dotenv_values(".env")


# 初始化語言模型
generator_llm = AzureChatOpenAI(
    azure_endpoint=config.get("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=config.get("AZURE_OPENAI_DEPLOYMENT_NAME"),
    openai_api_version=config.get("AZURE_OPENAI_API_VERSION"),
    api_key=config.get("AZURE_OPENAI_KEY"),
)

embedding_llm = AzureOpenAIEmbeddings(
    azure_endpoint=config.get("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=config.get("AZURE_OPENAI_Embedding_DEPLOYMENT_NAME"),
    api_key=config.get("AZURE_OPENAI_KEY"),
    openai_api_version=config.get("AZURE_OPENAI_API_VERSION"),
)

# ----- 第一次要把知識文件加入Qdrant 向量資料庫時，執行以下程式碼 -----

# Load PDF文件
loader = PyPDFLoader("../docs/raccoon_ai_1.pdf")
pages = loader.load_and_split()

# 分割文本
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(pages)

# Qdrant向量資料庫
qdrant = QdrantVectorStore.from_documents(
    splits,
    embedding=embedding_llm,
    url="http://localhost:6333",  # 假設Qdrant運行在本地的6333端口
    collection_name="km_docs_1",
)

#---------------------------------------------------------