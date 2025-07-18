import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
import tempfile

st.title("PDF Q&A :)")

GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-70b-8192"  

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

@st.cache_resource
def get_llm():
    return ChatGroq(
        model_name=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0.0,
    )

def ingest_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    # Increase chunk size and overlap for better coverage
    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    docs = splitter.split_documents(pages)
    return docs

def get_bot_Response(question: str, db, llm, token_limit=4800):
    results = db.similarity_search(question, k=8)
    context = ""
    used_tokens = 0
    selected = []
    for r in results:
        chunk = r.page_content.strip()
        # Simple approximation: 1 word ≈ 1.3 tokens
        tokens = int(len(chunk.split()) * 1.3)
        if used_tokens + tokens > token_limit:
            break
        context += chunk + "\n\n"
        used_tokens += tokens
        selected.append(r)
    if not selected:
        return "Sorry, couldn't find relevant information within token limit.", []
    prompt = (
        "You are a helpful assistant. Using the provided context, answer the question as accurately as possible. "
        "If you can't find the answer in the context, use your best judgment.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
        "Answer:"
    )
    answer = llm.invoke(prompt)
    return (str(answer.content).strip() if hasattr(answer, "content") else str(answer)), selected


db = None
llm = get_llm()
embeddings = get_embeddings()

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    st.info("Ingesting PDF, please wait...")
    docs = ingest_pdf(tmp_path)
    db = Chroma.from_documents(docs, embeddings)
    st.success("PDF ingested! Ask your question below:")

    user_question = st.text_input("Ask a question about your PDF:")
    if user_question:
        with st.spinner("Getting answer from Groq LLM..."):
            response, results = get_bot_Response(user_question, db, llm)
        st.markdown("**Bot Response:**")
        st.info(response)
else:
    st.info("Please upload a PDF file to begin.")
