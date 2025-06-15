# Classificador de Fake News

Este projeto web combina **HTML com Bootstrap 5, CSS e JavaScript no frontend** com um **backend Python utilizando FastAPI** para criar um classificador de fake news. Ele emprega a inteligência artificial **spaCy TextCatBow v3** para determinar se uma notícia é verdadeira ou falsa e oferece a funcionalidade de **buscar em sites de checagem através da API Google Search antes da classificação**.

---

## 🧩 Recursos

- **Interface Amigável**: Frontend construído com HTML, Bootstrap 5, CSS e JavaScript para uma experiência de usuário intuitiva.
- **Classificação de Notícias**: Utiliza o modelo **spaCy TextCatBow v3** para classificar notícias como verdadeiras ou falsas.
- **Verificação Prévia**: Integração com a **API Google Search** para permitir que o usuário verifique a notícia em sites de checagem antes de submetê-la à classificação da IA.
- **Backend Robusto**: Desenvolvido com **FastAPI** para um desempenho rápido e eficiente.

---

## 📚 Dataset Utilizado

O modelo foi treinado com base em um corpus de notícias em português, utilizando os seguintes trabalhos acadêmicos:

- **Monteiro et al. (2018)**  
  *Contributions to the Study of Fake News in Portuguese: New Corpus and Automatic Detection Results*  
  In: *Computational Processing of the Portuguese Language*, Springer International Publishing, pp. 324–334.  
  ISBN: 978-3-319-99722-3  
  [Link da Publicação](https://doi.org/10.1007/978-3-319-99722-3_33)

- **Silva et al. (2020)**  
  *Towards automatically filtering fake news in Portuguese*  
  In: *Expert Systems with Applications*, Volume 146, 2020, 113199.  
  ISSN: 0957-4174  
  [Link do Artigo](http://www.sciencedirect.com/science/article/pii/S0957417420300257)  
  DOI: [10.1016/j.eswa.2020.113199](https://doi.org/10.1016/j.eswa.2020.113199)

---

## 🧠 Como a IA Funciona e Suas Limitações

O coração deste classificador reside no modelo **spaCy TextCatBow v3**.  
**"TextCat"** refere-se à categorização de texto, e **"Bow"** (Bag-of-Words, ou Saco de Palavras) é uma técnica de representação de texto.

### 🔍 Como Funciona

1. **Pré-processamento**:  
   Quando uma notícia é submetida, o spaCy:
   - Tokeniza o texto (divide em palavras),
   - Remove pontuações,
   - Converte para minúsculas,
   - Pode lematizar (reduzir as palavras à sua forma base, como "correndo" para "correr").

2. **Vetorização (Bag-of-Words)**:  
   O modelo cria uma representação numérica do texto.  
   Na abordagem Bag-of-Words, a ordem das palavras não importa — apenas a **frequência** de cada palavra no texto.

3. **Classificação**:  
   A representação numérica é alimentada a um algoritmo de classificação.  
   Ele foi previamente treinado com um grande conjunto de dados do Fake.br-Corpus, que possuí notícias **rotuladas como verdadeiras ou falsas**.

---

### ⚠️ Limitações

- **Contexto e Semântica**:  
  Bag-of-Words ignora a ordem das palavras, dificultando a compreensão de **contexto e nuances**.  
  Exemplo: "o cachorro morde o homem" ≈ "o homem morde o cachorro".

- **Sarcasmo e Ironia**:  
  Linguagem figurada ou sarcástica pode enganar o modelo que é baseado em frequência de palavras.

- **Evolução da Linguagem**:  
  A linguagem e táticas de fake news **evoluem constantemente**.  
  O modelo precisa de **re-treinamento periódico** para se manter eficaz.

---

## ▶️ Como Usar

1. Acesse a página web em seu navegador.
2. Insira o **texto da notícia** no campo fornecido.
3. Clique em **"Verificar em Sites de Checagem"** para buscar na API Google Search.
4. Clique em **"Classificar Notícia"** para que a IA determine se a notícia é verdadeira ou falsa.
5. O resultado será exibido na página.

---

## 🗂 Estrutura do Projeto

### 📁 backend/
- `backend.py` – Define as rotas principais da API com FastAPI.
- `process_notice.py` – Processa a notícia, interage com o modelo spaCy e realiza buscas no Google.
- `output/` – Diretório para armazenar os modelos do spaCy.
- `requirements.txt` – Lista de dependências Python do projeto.
- `.env` – Contém variáveis de ambiente, como chaves de API.

### 📁 frontend/
- `index.html` – Página principal da aplicação.
- `outraspaginas/listaDeSitesDeChecagemSugeridos.html` – Página extra com uma lista de sites de notícias
- `outraspaginas/SobreNos` – Página extra com informações gerais do projeto.
- `style.css` – Estilos personalizados da interface.
- `script.js` – Código JavaScript para comunicação com o backend.

### 📁 TreinamentoDaIa/
- `train_IA_fake_news.py` – Processo de treinamento do modelo de inteligência artificial responsável pela classificação das notícias.


### Arquivos na raiz
- `README.md` – Documento com descrição e instruções do projeto.
- `.gitignore` – Arquivos e pastas que devem ser ignorados pelo Git.
