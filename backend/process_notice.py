from pydantic import BaseModel
import spacy
from unicodedata import normalize, combining
import requests
from bs4 import BeautifulSoup 
import json
from PIL import Image
import pytesseract
from io import BytesIO
import base64
from collections import Counter
from math import log2
from langdetect import detect
from dotenv import load_dotenv
import os
import re




class Notice(BaseModel):
    link: str = None
    notice: str = None

    #inicia a classe diretamente    
    def __init__(self, **data):
        super().__init__(**data)

        #Verifica se o método usado é por link ou texto
        if self.link:

            notice = NoticeSitesFact(link=self.link)

            #Extrai novamente o texto do site de notícias
            checked = notice.get_text_from_pages()

            #Quando checked finalizado, 
            if checked:
                self.preprocess_text(checked)
            
        #Caso seja texto
        else:
            self.preprocess_text(self.notice)


    def preprocess_text(self, notice):
        # Etapa 1: limpeza bruta do texto
        text = notice
        text = re.sub(r'\s+', ' ', text)  # remover múltiplos espaços/linhas
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  # remover pontuação e símbolos

        # Carregar modelo spaCy
        nlp = spacy.load("pt_core_news_md")
        doc = nlp(text)

        def remove_accent(text):
            text = normalize("NFD", text)
            return ''.join(char for char in text if not combining(char))

        def palavra_valida(palavra):
            # Regras básicas para remover ruído OCR
            if len(palavra) < 3:  # muito curtas
                return False
            if not re.search(r'[aeiouáéíóúãõ]', palavra):  # sem vogal
                return False
            if re.search(r'\d+[a-zA-Z]+|[a-zA-Z]+\d+', palavra):  # mistura de letras e números
                return False
            return True

        processed_words = []
        for token in doc:
            # remover stopwords e pontuação
            if not token.is_stop and not token.is_punct:
                lemma = token.lemma_
                lemma_no_accent = remove_accent(lemma)
                if palavra_valida(lemma_no_accent):
                    processed_words.append(lemma_no_accent)

        # Resultado final
        return self.IA_classification(' '.join(processed_words))
    
    
    def IA_classification(self, processed_notice):

        print(processed_notice)

        nlp = spacy.load("output/model-best")
        
        pln = spacy.load("pt_core_news_md")

        # Transformando texto em linguagem de máquina para IA
        doc = pln(processed_notice)

        # Mandando texto para IA
        novo_doc = nlp(doc)

        self.notice = doc.cats


    def get_notice(self):

        notice = self.notice

        #Caso de algum problema na notíca
        if isinstance(notice, str):
            return notice

        #Realiza os cálculos de porcentagem e retorna a mensagem
        max_catagory = max(notice, key=notice.get)
        max_value = notice[max_catagory]

        total_sum = sum(notice.values())
        porcent = (max_value / total_sum) * 100
   
        final_text = f"A notícia possui {porcent:.2f}% de probabilidade de ser {max_catagory}."

        return final_text



class NoticeSitesFact(BaseModel):

    notice: str = None
    link: str = None

    def check_notice_site(self):

            #Verifica se a url inserida não possui os valores descritos no JSON 
            with open('sitesconfiaveis.json', 'r', encoding='utf-8') as f:
                notices_sites = json.load(f)

            for url in notices_sites:
                
                if url in self.link:
                    return 0

            return self.get_text_from_pages()


    def get_text_from_pages(self):

        link = self.link
        notice = None
    
        try:

            response = requests.get(link)

            #Verifica se a url é válida e disponível e tenta extrair as informações do mesmo
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")

                title = soup.find("h1").get_text()
                body = soup.find_all("p")

            if body:
                
                new_body = "\n".join([p.get_text(strip=False) for p in body])

                if title:                
                    
                    notice = title + "\n\n" + new_body
            
        except:
            
            print("Página não encontrada")

        return self.notice_collected(notice)
    
    #Verifica se a notícia foi coletada ou não retornando 1 caso a váriável notice esteja vazia
    def notice_collected(self, notice):

        self.notice = notice

        if not self.notice:

            return 1 
    
        return self.notice

    #Verifica com a API do google se existem notícias similares as informações que o usuário inseriu
    def check_notice_verification(self):

        load_dotenv()

        notice_body = self.extract_key_words(num_words=5)
        print(notice_body)

        API_KEY = os.getenv("GOOGLE_API_KEY")
        CSE_ID = os.getenv("GOOGLE_CSE_ID")
        API_URL = f"https://www.googleapis.com/customsearch/v1?q={notice_body}&cx={CSE_ID}&key={API_KEY}&num=3"

        response = requests.get(API_URL)

        data = response.json()

        search_results = []
        
        for item in data.get('items', []):
            link = item.get('link')
            title = item.get('title')  
            snippet = item.get('snippet')  
            image = item.get('pagemap', {}).get('cse_image', [{}])[0].get('src') 

            search_results.append({
            "title": title,
            "link": link,
            "snippet": snippet,
            "image": image
            })

        return(search_results)

    #Extrai palavras chaves das notícias enviadas    
    def extract_key_words(self, num_words=5):

        notice_body = self.notice

        # Carrega o modelo de português
        nlp = spacy.load("pt_core_news_sm")
        
        # Processa o texto
        doc = nlp(notice_body.lower())
        
        # Extrai substantivos e nomes próprios, evitando stopwords e pontuação
        key_words = [token.text for token in doc if not token.is_stop and not token.is_punct and (token.pos_ == "NOUN" or token.pos_ == "PROPN")]
        
        # Retorna as 'num_palavras' primeiras palavras-chave encontradas
        return " ".join(key_words[:num_words])

class ImageNotice(BaseModel):

    notice_in_text: str = None


    @classmethod
    def obter_valor(cls):
        
        return cls.notice_in_text


    def convert_image_to_text(self, image):

        #Tenta processar a imagem 
        try:

            pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

            converted_image = Image.open(BytesIO(image))

            text = pytesseract.image_to_string(converted_image, lang='por')  # Idioma: Português

            self.notice_in_text = text



        #Caso o formato não seja aceito
        except: 
            
            text = 0    

        return text
        


class VerificationSpam(BaseModel):

    def validate_repetitions(self, text, repetition_limit=0.4):
        words = text.split()
        word_count = Counter(words)
        repetitions = sum(1 for word, freq in word_count.items() if freq > 1)
        
        return repetitions / len(words) < repetition_limit

    def calculate_entropy(self, text):
        probabilities = {char: text.count(char) / len(text) for char in set(text)}
        return -sum(p * log2(p) for p in probabilities.values())

    def validate_entropy(self, text, entropy_limit=3.0):
        return self.calculate_entropy(text) > entropy_limit
    
    def validate_language(self, texto, idioma_esperado='pt'):
        try:
            return detect(texto) == idioma_esperado
        except:
            return False
        

    def validate_detailed_text(self, text):

        if not self.validate_repetitions(text):
            return "Texto contém palavras repetidas em excesso."
        elif not self.validate_entropy(text):
            return "Texto parece ser aleatório ou sem sentido."      
        elif not self.validate_language(text):
            return "O texto não está na linguagem esperada"
    
        return True