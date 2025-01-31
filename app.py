
import streamlit as st
from dotenv import load_dotenv #To use .env packages and tokens stored
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
#from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import conversational_retrieval
#from langchain.chains import ConversationRetrievalChain
from langchain.llms import huggingface_hub
from langchain_huggingface import ChatHuggingFace
#from langchain.llms import HuggingFaceHub
from htmlTemplates import css, bot_template, user_template

def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks=text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    # Initialize without any unexpected keyword arguments
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore



def get_conversation_chain(vectorstore):
    llm = huggingface_hub(repo_id="meta-llama/Llama-3.3-70B-Instruct", model_kwargs={"temperature":0.5, "max_length":512})
    
    memory=ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = conversational_retrieval.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory)
    return conversation_chain



def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    #st.write(response)
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("$MSG", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("$MSG", message.content), unsafe_allow_html=True)




def main():
    load_dotenv()
    st.set_page_config(page_title="TicketMind", page_icon=":books:")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("TicketMind :books:")
    st.subheader("chat with Multiple Ticket data or any data through Pdf")
    user_question=st.text_input("Ask any question related to the doc's given:")
    if user_question:
        handle_userinput(user_question)

    st.write(user_template.replace("$MSG", "Hello Rob"), unsafe_allow_html=True)
    st.write(bot_template.replace("$MSG","hello AJ"), unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader("Upload you PDF's here and click on 'Upload'", accept_multiple_files=True)
        if st.button("Upload"):
            with st.spinner("Processing"):
                #get the pdf text
                raw_text = get_pdf_text(pdf_docs)
                #st.write(raw_text)

                #get text chunks
                text_chunks= get_text_chunks(raw_text)
                #st.write(text_chunks)

                #Create vector store
                vectorstore=get_vectorstore(text_chunks)

                #create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)
    
  




if __name__== '__main__':
    main()












