import os
from typing import TypedDict, Annotated, Literal

import streamlit as st
from dotenv import load_dotenv

from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# =========================================================
# Page config + styling
# =========================================================

st.set_page_config(
    page_title="College Assistant",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    #MainMenu, footer, header {visibility: hidden;}

    .stApp {
        background: linear-gradient(160deg, #0f172a 0%, #1e1b4b 45%, #0f172a 100%);
    }

    .hero {
        text-align: center;
        padding: 1.6rem 1rem 1.2rem 1rem;
        margin-bottom: 0.5rem;
    }
    .hero h1 {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .hero p {
        color: #94a3b8;
        font-size: 0.95rem;
    }

    .programme-badge {
        display: inline-block;
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        background: rgba(167, 139, 250, 0.15);
        border: 1px solid rgba(167, 139, 250, 0.4);
        color: #c4b5fd;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 0.4rem;
    }

    .category-tag {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        padding: 0.15rem 0.55rem;
        border-radius: 999px;
        margin-bottom: 0.4rem;
    }
    .tag-academic { background: rgba(96, 165, 250, 0.18); color: #93c5fd; border: 1px solid rgba(96,165,250,0.4); }
    .tag-fee { background: rgba(52, 211, 153, 0.18); color: #6ee7b7; border: 1px solid rgba(52,211,153,0.4); }
    .tag-general { background: rgba(251, 191, 36, 0.18); color: #fcd34d; border: 1px solid rgba(251,191,36,0.4); }

    section[data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.9);
        border-right: 1px solid rgba(148, 163, 184, 0.15);
    }
    section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: #e2e8f0;
    }

    .stChatMessage {
        border-radius: 16px;
        padding: 0.4rem 0.2rem;
    }

    div[data-testid="stChatInput"] textarea {
        border-radius: 14px !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =========================================================
# Graph state
# =========================================================

class State(TypedDict):
    programme: str
    messages: Annotated[list, add_messages]
    query_type: str
    retrieved_context: str


TAG_CLASS = {
    "academic": "tag-academic",
    "fee": "tag-fee",
    "general": "tag-general",
}

# =========================================================
# Cached resources: embeddings, retrievers, llm, graph
# =========================================================

@st.cache_resource(show_spinner="Loading embedding model...")
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


@st.cache_resource(show_spinner="Indexing college documents...")
def build_retriever(pdf_path: str):
    embeddings = get_embeddings()
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 4})


@st.cache_resource(show_spinner=False)
def get_llm():
    return ChatGroq(model="openai/gpt-oss-20b", temperature=0.4)


@st.cache_resource(show_spinner="Building the assistant graph...")
def build_graph():
    academic_retriever = build_retriever("Files/academics_handbook.pdf")
    fee_retriever = build_retriever("Files/fee_structure.pdf")
    llm = get_llm()

    def classifier_node(state: State) -> dict:
        last_message = state["messages"][-1].content
        prompt = (
            "Classify the following student query into exactly one category: "
            "'academic', 'fee', or 'general'.\n\n"
            "Use 'academic' for questions about attendance, exams, grading, credits, "
            "promotion, course structure, summer training, or degree requirements.\n"
            "Use 'fee' for questions about tuition, payment, refund, late charges, "
            "scholarships, or any money-related topic.\n"
            "Use 'general' for greetings, casual talk, or anything not related to "
            "the college rules or fee.\n\n"
            f"Query: {last_message}\n\n"
            "Return only one word: academic, fee, or general."
        )
        response = llm.invoke(prompt)
        category = response.content.strip().lower()
        if "academic" in category:
            category = "academic"
        elif "fee" in category:
            category = "fee"
        else:
            category = "general"
        return {"query_type": category}

    def academic_rag_node(state: State) -> dict:
        query = state["messages"][-1].content
        docs = academic_retriever.invoke(query)
        context = "\n\n".join(doc.page_content for doc in docs)
        return {"retrieved_context": context}

    def fee_rag_node(state: State) -> dict:
        query = state["messages"][-1].content
        docs = fee_retriever.invoke(query)
        context = "\n\n".join(doc.page_content for doc in docs)
        return {"retrieved_context": context}

    def general_node(state: State) -> dict:
        return {"retrieved_context": "NO_RETRIEVAL_NEEDED"}

    def response_node(state: State) -> dict:
        query = state["messages"][-1].content
        programme = state.get("programme", "Unknown")
        context = state["retrieved_context"]

        if context == "NO_RETRIEVAL_NEEDED":
            prompt = (
                f"You are a friendly college assistant talking to a {programme} student. "
                f"Answer this question using your own general knowledge:\n\n{query}"
            )
        else:
            prompt = (
                f"You are a college assistant helping a {programme} student. "
                f"Use the following context from the official college documents to answer "
                f"the question accurately. If the context mentions specific figures for "
                f"different programmes, highlight the one relevant to {programme} if possible.\n\n"
                f"Context:\n{context}\n\n"
                f"Question: {query}\n\n"
                f"Give a clear, friendly, and precise answer."
            )

        response = llm.invoke(prompt)
        return {"messages": [("ai", response.content.strip())]}

    def route_query(state: State) -> Literal["academic_rag", "fee_rag", "general"]:
        if state["query_type"] == "academic":
            return "academic_rag"
        elif state["query_type"] == "fee":
            return "fee_rag"
        return "general"

    graph = StateGraph(State)
    graph.add_node("classifier", classifier_node)
    graph.add_node("academic_rag", academic_rag_node)
    graph.add_node("fee_rag", fee_rag_node)
    graph.add_node("general", general_node)
    graph.add_node("response", response_node)

    graph.add_edge(START, "classifier")
    graph.add_conditional_edges("classifier", route_query)
    graph.add_edge("academic_rag", "response")
    graph.add_edge("fee_rag", "response")
    graph.add_edge("general", "response")
    graph.add_edge("response", END)

    return graph.compile()


# =========================================================
# Session state
# =========================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of dicts: role, content, tag(optional)

if "programme" not in st.session_state:
    st.session_state.programme = None

# =========================================================
# Sidebar
# =========================================================

with st.sidebar:
    st.markdown("## 🎓 Your Programme")
    st.caption("This personalizes every answer the assistant gives you.")

    programme_choice = st.radio(
        "Select your programme",
        options=["BCA", "BBA", "B.Com (H)"],
        index=0 if st.session_state.programme is None else
        ["BCA", "BBA", "B.Com (H)"].index(st.session_state.programme),
        label_visibility="collapsed",
    )
    st.session_state.programme = programme_choice

    st.divider()
    st.markdown("### ℹ️ About")
    st.caption(
        "Ask about attendance, exams, grading, fees, refunds, scholarships, "
        "or anything else about college life. Questions are automatically "
        "routed to the right knowledge base."
    )

    st.divider()
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    if os.getenv("GROQ_API_KEY") is None:
        st.warning("GROQ_API_KEY not found in environment. Set it in your .env file.", icon="⚠️")

# =========================================================
# Hero header
# =========================================================

st.markdown(
    f"""
    <div class="hero">
        <h1>College Assistant</h1>
        <p>Your AI guide to academics, fees & everything in between</p>
        <div class="programme-badge">📘 {st.session_state.programme} Student</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# Chat history render
# =========================================================

if not st.session_state.chat_history:
    st.info(
        "👋 Hi! Ask me anything about attendance, exams, grading, tuition fees, "
        "refunds, scholarships, or general college life.",
        icon="💬",
    )

for msg in st.session_state.chat_history:
    avatar = "🧑‍🎓" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        if msg["role"] == "assistant" and msg.get("tag"):
            tag = msg["tag"]
            st.markdown(
                f'<span class="category-tag {TAG_CLASS.get(tag, "tag-general")}">{tag}</span>',
                unsafe_allow_html=True,
            )
        st.markdown(msg["content"])

# =========================================================
# Chat input
# =========================================================

user_query = st.chat_input("Type your question here...")

if user_query:
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(user_query)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            try:
                app = build_graph()
                result = app.invoke(
                    {
                        "programme": st.session_state.programme,
                        "messages": [("human", user_query)],
                    }
                )
                answer = result["messages"][-1].content
                tag = result.get("query_type", "general")
            except Exception as e:
                answer = f"⚠️ Something went wrong: `{e}`"
                tag = "general"

        st.markdown(
            f'<span class="category-tag {TAG_CLASS.get(tag, "tag-general")}">{tag}</span>',
            unsafe_allow_html=True,
        )
        st.markdown(answer)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": answer, "tag": tag}
    )