from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def extract_text_from_pdf(pdf_documents):
    """
    Extracts text from a list of PDF documents.
    """
    text = ""
    for pdf_doc in pdf_documents:
        reader = PdfReader(pdf_doc)
        for page in reader.pages:
            text += page.extract_text()
    return text


def split_text_into_chunks(text_content):
    """
    Splits text content into smaller chunks with specified size and overlap.
    """
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = splitter.split_text(text_content)
    return chunks


def create_vector_store(text_segments):
    """
    Creates a vector store using embeddings for the provided text segments.
    """
    embedding_model = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_segments, embedding=embedding_model)
    return vectorstore


def build_conversational_chain(text_store):
    """
    Builds a conversational retrieval chain using the provided vector store.
    """
    chatbot = ChatOpenAI(openai_api_key=openai_api_key)
    conversation_memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    chain = ConversationalRetrievalChain.from_llm(
        llm=chatbot,
        retriever=text_store.as_retriever(),
        memory=conversation_memory
    )
    return chain


def get_chatbot_answer(conversation_history, user_query):
    """
    Retrieves relevant conversation history and uses it to get a chatbot response for the user query.
    """
    chain = build_conversational_chain(conversation_history)
    response = chain({'question': user_query})
    chat_history = response['chat_history']
    chatbot_answers = []

    for index, message in enumerate(chat_history):
        if index % 2 != 0:  # Considering only chatbot responses (odd indices)
            chatbot_answers.append(message.content)

    return chatbot_answers[0]  # Returning the first answer


def answer_user_question(pdf_filepath, user_question):
    """
    Processes a PDF file, extracts text, interacts with the chatbot based on the extracted text 
    and the user query, and returns the chatbot's first response.
    """
    pdf_documents = [pdf_filepath]
    extracted_text = extract_text_from_pdf(pdf_documents)
    text_chunks = split_text_into_chunks(extracted_text)
    conversation_store = create_vector_store(text_chunks)
    answer = get_chatbot_answer(conversation_store, user_question)
    return answer

