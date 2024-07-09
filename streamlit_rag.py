import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_experimental.llms.ollama_functions import ChatOllama
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings


if "phi3" not in st.session_state:
    st.session_state["phi3"] = ChatOllama(model="phi3", temperature=0)
if "embeddings" not in st.session_state:
    st.session_state["embeddings"] = OllamaEmbeddings(
        model="nomic-embed-text",
        show_progress=True,
        temperature=0.5,
    )
if "db" not in st.session_state:
    st.session_state["db"] = Chroma(
        persist_directory="./chroma_db",
        embedding_function=st.session_state["embeddings"],
    )
if "prompt" not in st.session_state:
    st.session_state["prompt"]  = PromptTemplate.from_template(
        """
        <|user|>
        You are an assistant. You will be provided the context relevant to the user's question and output the answer to the user.
        If the retrieved context was not relevant at all to the question, answer the question with your knowledge, say sorry to the user when you can not find the answer.
        You can also add some information if you know something about it, as long as your knowledge is relevant to the context. 
        context: {context}
        question: {question}
        <|end|>
        <|assistant|>
        """
    )
if "qa_chain" not in st.session_state:
    st.session_state["qa_chain"] = st.session_state["prompt"] | st.session_state["phi3"]


if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = st.session_state["qa_chain"].stream(
        {
                "question": prompt,
                "context": "/n".join(
                    result.page_content 
                    for result in st.session_state["db"].similarity_search(prompt, k=6)
                )
            }
        )
        response = st.write_stream(stream)
