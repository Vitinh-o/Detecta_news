from typing import Union
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from process_notice import Notice, NoticeSitesFact, ImageNotice, VerificationSpam
from fastapi.middleware.cors import CORSMiddleware
image_notice = ImageNotice()


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"] 
)


#Rota para ativação da IA, verifica o que foi recebido e instancia a classe notice conforme o recebido
@app.get("/notice")
async def read_notice(recived_link:str = None, text_notice:str = None, recived_image:str = None):

    if recived_link:

        notice = Notice(link=recived_link)

    elif text_notice:

        notice = Notice(notice=text_notice)
    
    else:

        text = image_notice.notice_in_text

        notice = Notice(notice=text)

    
    result = notice.get_notice()

    return result  


#Rota para verificar se existe notícas similares em sites de checagem
@app.get("/notice_text_form")
async def read_notice(recived_link:str = None, text_notice:str = None, recived_image:str = None):

    if recived_link:

        notice = NoticeSitesFact(link=recived_link)
        notice_collected = notice.check_notice_site()

        if notice_collected == 1:
        
            return "Não conseguimos extrair o texto da notícia ou encontrar a página, por favor faça uma cópia da mesma e cole."  
        
        elif notice_collected == 0:
            
            return "Este site está listado em nossos sistemas como um site de notícias confiáveis!"
        

        return notice.check_notice_verification()
        

    else:

        spam = VerificationSpam()

        validate = spam.validate_detailed_text(text_notice)

        if not isinstance(validate, str):

            text = NoticeSitesFact(notice=text_notice)
        
            result = text.check_notice_verification()

            return result  

        result = validate

        return result  



#Rota específica para o processamento da imagem
@app.post("/notice_image")
async def read_image(image:UploadFile = File(...)):

        try:

            file_content = await image.read()

        except:

            return "O formato inserido não é aceito em nossos sistemas."    

        text = image_notice.convert_image_to_text(file_content)


        #Verifica  o formato da imagem, caso 0 significa que o tipo da  imagem não é aceita 
        if text == 0:
            
            return  "O formato inserido não é aceito em nossos sistemas." 

        links = NoticeSitesFact(notice=text)

        result = links.check_notice_verification()

        return result

