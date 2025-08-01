from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import tempfile
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain

app = Flask(__name__, template_folder='templates')
CORS(app)

os.environ["OPENAI_API_KEY"] = "your-openai-api-key"  # Replace with your real key

llm = OpenAI(temperature=0)
embedding = OpenAIEmbeddings()
db = None

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    global db
    file = request.files['pdf']
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file.save(tmp.name)
        text = extract_text_from_pdf(tmp.name)

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.create_documents([text])
    db = FAISS.from_documents(docs, embedding)

    return jsonify({"message": "PDF uploaded and indexed successfully."})

@app.route('/ask', methods=['POST'])
def ask_question():
    global db
    question = request.json.get('question')
    if not db:
        return jsonify({"error": "No PDF uploaded."}), 400

    retriever = db.as_retriever()
    qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever)
    result = qa_chain.run(question)

    return jsonify({"answer": result})

if __name__ == '__main__':
    app.run(debug=True)
