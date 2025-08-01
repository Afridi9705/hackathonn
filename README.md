# AI-Powered PDF Q&A App

This is a Flask web app where users can upload a PDF, and ask questions about its content using OpenAI + LangChain.

## Features
- Upload PDF and extract its content
- Ask questions and get answers from the PDF using GPT
- Works with your own OpenAI API Key

## How to Deploy on Render

### 1. Create a GitHub Repo
Push this project folder to a GitHub repository.

### 2. Add Your OpenAI API Key
Edit `render.yaml` or set the `OPENAI_API_KEY` during Render setup.

### 3. Deploy on Render
- Visit https://render.com
- Click "New Web Service"
- Connect to your GitHub repo
- Choose this project
- Render will build and serve it!

## Local Run
```bash
pip install -r requirements.txt
python app.py
```
Visit: http://localhost:5000