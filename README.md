# PDF Q&A Chatbot 🤖

## 📖 Introduction

**PDF Q&A Chatbot** is an AI-powered web application that allows you to upload any text-based PDF and ask natural-language questions about its content.  
It combines [Streamlit](https://streamlit.io/) for the user interface, [LangChain](https://www.langchain.com/) for workflow orchestration, [ChromaDB](https://www.trychroma.com/) for semantic retrieval, [HuggingFace Embeddings](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) for semantic understanding, and [Groq Llama3-70B](https://groq.com/) as the large language model that generates answers.  
This tool is perfect for extracting insights from research papers, reports, books, or any other PDF.

---

## 🚀 How to Run (Setup Process)

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/yourrepo.git
    cd yourrepo
    ```

2. **Create and activate a Python virtual environment** (recommended)
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On Mac/Linux:
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    <details>
    <summary>Sample <code>requirements.txt</code></summary>

    ```
    streamlit
    langchain
    langchain-community
    langchain-groq
    chromadb
    huggingface-hub
    ```
    </details>

4. **Set your Groq API key**
    - [Sign up for Groq](https://console.groq.com/keys) and copy your API key.
    - For demos, you may hardcode it, but for best practice, create a `.env` file:
        ```
        GROQ_API_KEY=your_actual_groq_api_key
        ```
      And update your code to use `os.getenv("GROQ_API_KEY")`.

5. **Run the app**
    ```bash
    streamlit run app.py
    ```
    - Open [http://localhost:8501](http://localhost:8501) in your browser.
    - Upload a PDF and start chatting!

---

## 🔄 Workflow

### Visual Diagram

```mermaid
graph TD
    A[User uploads PDF] --> B[PDF parsed into text chunks]
    B --> C[Chunks embedded with HuggingFace model]
    C --> D[Stored in Chroma VectorDB]
    D --> E[User asks a question]
    E --> F[Relevant chunks retrieved by semantic search]
    F --> G[Prompt built for Groq Llama3-70B]
    G --> H[LLM generates answer]
    H --> I[Answer displayed in Streamlit]
