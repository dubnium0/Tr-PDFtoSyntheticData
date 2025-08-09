# Turkish Financial PDF to Synthetic Data Generation Web Application

## Purpose of the Application
This application is developed to generate synthetic question-answer (instruction) datasets from Turkish financial PDF documents. The aim is to produce automatic, high-quality, and contextually appropriate data for financial literacy education and artificial intelligence applications.

## Key Features
- Text extraction and chunking from PDF files
- Vector-based document retrieval using LangChain
- LLM-based question and answer generation with Ollama (e.g., gemma3n:e4b)
- Ability to accept custom prompts (question/answer templates) from users
- View results on screen and download as JSON
- Modern and user-friendly interface based on Streamlit

## Main Implementations
- PDF processing and LLM integration with FastAPI
- User-friendly frontend with Streamlit
- Embedding operations with HuggingFace sentence-transformers
- Easy deployment and execution with Docker
- Script preventing frontend from starting before backend is ready
- GPU support (automatic in suitable environments for Ollama and embedding models)
- Accepting custom prompts and question quantity from users
- Progress bar during PDF processing
- Cleaning of unnecessary comments and explanation lines

## Requirements
- Docker (and preferably NVIDIA GPU with CUDA drivers)
- Ollama installed on the host machine with the model (e.g., gemma3n:e4b) downloaded

## Running with Docker
1. **Start Ollama on the host:**
   ```bash
   ollama serve
   # or
   ollama run gemma3n:e4b
   ```
2. **Build the Docker image:**
   ```bash
   docker build -t tr-pdftosyntheticdata-webapp:latest .
   ```
3. **Start the container:**
   ```bash
   docker run --gpus all -p 8501:8501 -p 8000:8000 tr-pdftosyntheticdata-webapp:latest
   ```
   > If you don't have a GPU, you can remove the `--gpus all` part.

4. **Access the application:**
   - [http://localhost:8501](http://localhost:8501) (Streamlit interface)
   - [http://localhost:8000/docs](http://localhost:8000/docs) (FastAPI documentation)

## Usage
- Upload your PDF file.
- Specify how many and what type of questions to generate (e.g., "generate 50 logical questions for me").
- Enter your custom prompts or use the defaults. (the default prompt is designed for generating financial data)
- You can view the results on screen and download them as JSON.

## Notes
- GPU support is automatically used for Ollama and embedding processes if available.
- Dockerfile and scripts prevent the frontend from starting before the backend is ready.
- The application is optimized for education and data generation in the field of financial literacy.