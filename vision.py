from fastapi import FastAPI, File, UploadFile
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure a chave da API
key="AIzaSyAxQ6AGJZJ58zkqy3AX4TRWUAwXVW5wgZk"
genai.configure(api_key=os.environ["API_KEY"])  # Substitua 'API_KEY' pela variável de ambiente correta

app = FastAPI()

# Endpoint para upload de imagem e envio para o Google Gemini
@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Salve o arquivo temporariamente
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Passo 1: Faça o upload da imagem
    sample_file = genai.upload_file(path=file_location, display_name="Cavalo")

    # Passo 2: Use o modelo generativo para descrever o conteúdo da imagem
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    response = model.generate_content([sample_file, "Descreva o que está na imagem."])

    # Remova o arquivo temporário após o upload
    os.remove(file_location)

    # Retorna o resultado processado pelo Google Gemini
    return {"description": response.text}

# Para rodar o servidor:
# uvicorn nome_do_arquivo:app --reload
