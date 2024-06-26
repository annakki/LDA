# pakettien lataus
Z:\>pip install gensim
Z:\>pip install nltk
import gensim
from gensim import corpora
from pprint import pprint
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import pyLDAvis.gensim_models
import string
import re
nltk.download('punkt')

# aineiston lataus (VARMISTA SIJAINTI)
file_path = "Z:\\dataUTF.csv"
data = pd.read_csv(file_path, sep=';', dtype={'puhe': str})
data = data.iloc[:, :3]
data = data.dropna(subset=['puhe'])

# välimerkkien ja numeroiden poisto
def remove_punctuation_and_numbers(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\d+', '', text)
    return text

data['puhe'] = data['puhe'].apply(remove_punctuation_and_numbers).str.lower()
print(data.head())
# VARMISTA TULOSTE

# dokumenttien tokenisointi
documents = data['puhe'].tolist()
tokenized_documents = [doc.lower().split() if isinstance(doc, str) else [] for doc in documents]

# stoplistan lataus (VARMISTA SIJAINTI)
stopword_file_path = "Z:\\finnish.txt"
with open(stopword_file_path, "r", encoding="utf-8") as file:
    finnish_stopwords = set(file.read().splitlines())

# stop-sanojen poisto
filtered_documents = [[word for word in doc if word.lower() not in finnish_stopwords] for doc in tokenized_documents]
filtered_documents_strings = [' '.join(doc) for doc in filtered_documents]
data['puhe'] = filtered_documents_strings

# sanakirjan ja korpuksen luonti
dictionary = corpora.Dictionary(filtered_documents)
corpus = [dictionary.doc2bow(doc) for doc in filtered_documents]

# LDA-mallin koulutus (VALITSE AIHEIDEN JA ITERAATIOIDEN MÄÄRÄ)
lda_model = gensim.models.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=15)

# tulosten visualisointi
lda_display = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary, sort_topics=False)
pyLDAvis.display(lda_display)

#vaihtoehtoinen visualisointi
for topic_id, topic_words in lda_model.print_topics():
    print(f"Topic ID: {topic_id}")
    print(f"Words: {topic_words}")
    print()  # Print an empty line for readability
