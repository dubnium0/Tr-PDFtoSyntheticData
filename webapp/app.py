import os
import tempfile
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_ollama import ChatOllama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate
import json

output_parser = StrOutputParser()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatOllama(model="gemma3n:e4b", temperature=0.2, base_url="http://host.docker.internal:11434")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

@app.post("/process_pdf/")
async def process_pdf(
    file: UploadFile = File(...),
    input_que: str = Form("bana 50 tane mantıklı soru üret"),
    q_prompt_input: str = Form(None),
    system_message_input: str = Form(None)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        pdf_path = tmp.name
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(split_docs, embeddings, persist_directory="retriever")
    retriever = vectorstore.as_retriever()
    q_prompt_final = q_prompt_input if q_prompt_input else """
Sen finansal okur yazarlık alanında insanlara bir şeyler öğretmek isteyen bir profesörsün. 
Elindeki kaynaklardan finans alanında genel olarak sorulması gereken mantıklı soruları çıkartırsın.
her bir sorunun arasına "~" koy.
Asla elindeki mentinden farklı bir konu bağlamaına çıkmaz ve gerekli soruları sorarsın. 
Bağlam:{context}
Soru: {input}
Cevap:
"""
    q_prompt_obj = PromptTemplate(
        template=q_prompt_final,
        input_variables=["context", "input"]
    )
    document_chain = create_stuff_documents_chain(llm=llm, prompt=q_prompt_obj, output_parser=output_parser)
    rag_chain = create_retrieval_chain(retriever=retriever, combine_docs_chain=document_chain)
    response = rag_chain.invoke({'input': input_que})
    sorular = response['answer'].split("~")[:-1]
    system_message_final = system_message_input if system_message_input else """
Sen, finansal okuryazarlık seviyesi sıfır olan bireylere yardımcı olmak için tasarlanmış bir yapay zeka asistanısın.
Görevin, sadece verilen *bağlam* içindeki bilgilere dayanarak öğretici ve sade açıklamalar üretmektir.

Aşağıdaki JSON yapısını her zaman kullan:
{{
  "instruction": "Kullanıcının öğrenmek istediği finansal konu başlığı",
  "input": "Kullanıcının sorduğu basit soru",
  "output": "Konuyu hiç bilmeyen biri için kısa, açık, sade bir açıklama. Gerekirse günlük hayattan örnek vererek anlat."
}}

Kurallar:
1. Yalnızca verilen bağlamdaki bilgileri kullan. Bağlam dışında bilgi varsa, kesinlikle yanıt verme.
2. Asla uydurma bilgi üretme. Emin değilsen ya da bağlamda bilgi yoksa şu sabit yanıtı ver:
   "Bu konuda bilgim yok. Lütfen bir finansal danışmana başvurun."
3. Yanıtlar sade, kısa ve öğretici olsun. Teknik terimler gerekiyorsa açıklayıp günlük örnekle açıkla.
   Hedef kitlen, ilk kez finansla tanışan bireylerdir.
4. Format dışına çıkma. Her zaman belirtilen JSON yapısında cevap ver.
5. Bağlam dışı soruları pass geç ve o soruyu üretme. çıktı olarak sadece "Dökümantasyonla alakalı bir soru değil" de 

Bağlam: {context}
Soru:{input}
Cevap:
"""
    system_prompt_obj = PromptTemplate(
        template=system_message_final,
        input_variables=["context", "input"]
    )
    document_chain2 = create_stuff_documents_chain(llm=llm, prompt=system_prompt_obj, output_parser=output_parser)
    rag_chain2 = create_retrieval_chain(retriever=retriever, combine_docs_chain=document_chain2)
    json_format = []
    for soru in sorular:
        resp = rag_chain2.invoke({'input': soru})
        json_format.append(resp["answer"])
    os.remove(pdf_path)
    return JSONResponse(content={"results": json_format}) 