import pandas as pd
import numpy as np
from spacy.training import Example
from sklearn.model_selection import train_test_split
import spacy
from spacy.tokens import DocBin


#Este csv já comtém as informações com técnicas de pré-procesamento aplicadas.
df_fake_news = pd.read_csv("pre-processed.csv")

pln = spacy.load("pt_core_news_lg")

modelo = spacy.blank("pt")


#Separando dados de treinamento em dados e target
X = df_fake_news["preprocessed_news"]
y = df_fake_news["label"]

X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.15, random_state=42)

X_treino, X_validacao, y_treino, y_validacao = train_test_split(X_treino, y_treino,  test_size=0.15, random_state=42)

data = []
validacao = []

for texto, target in zip(X_treino, y_treino):
  data.append((texto, target))

for texto, target in zip(X_validacao, y_validacao):
  validacao.append((texto, target))


base_no_formato_correto = []
db = DocBin()

def make_docs(data):
  docs = []

  for doc, label in pln.pipe(data, as_tuples=True):

      if label == "fake":
          doc.cats["verdade"] = 0
          doc.cats["fake"] = 1

      else:
          doc.cats["verdade"] = 1
          doc.cats["fake"] = 0

      docs.append(doc)

  return docs

numero_de_textos = 200

train_docs = make_docs(data)

doc_bin = DocBin(docs=train_docs)
doc_bin.to_disk("train.spacy")

valida_docs = make_docs(validacao)

doc_bin = DocBin(docs=valida_docs)
doc_bin.to_disk("valid.spacy")


