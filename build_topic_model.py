from get_data import get_data
import spacy
from nltk.stem import WordNetLemmatizer
from gensim.models import LdaModel
from gensim.corpora import Dictionary

spacy_model = spacy.load("en_core_web_sm")
lemmatizer = WordNetLemmatizer()


def preprocess_documents(documents):
    processed_docs = []

    for doc in documents:
        processed_doc = []
        tokens = spacy_model(doc)

        for token in tokens:
            if 'NN' in token.tag_:
                token_text = token.text.lower()
                token_text = lemmatizer.lemmatize(token_text)
                processed_doc.append(token_text)

        processed_docs.append(processed_doc)

    return processed_docs


def build_model(documents):
    dictionary = Dictionary(documents)
    bows = [dictionary.doc2bow(doc) for doc in documents]
    temp = dictionary[0]
    id2word = dictionary.id2token

    model = LdaModel(corpus=bows, id2word=id2word, iterations=2,
                     num_topics=40)

    return model


def get_topic_model():
    # Get corpus
    corpus = get_data()

    # Gather all texts, regardless of taxonomic family
    documents = [doc for fam in corpus for doc in corpus[fam]]

    # Preprocess texts in corpus
    documents = preprocess_documents(documents)

    # Build and train topic model
    topic_model = build_model(documents)

    return topic_model, corpus
