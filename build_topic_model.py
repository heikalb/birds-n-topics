"""
Build a topic model based on the corpus of Wikipedia articles of bird species.
Heikal Badrulhisham, 2019 <heikal93@gmail.com>
"""
from get_data import get_data
import spacy
from nltk.stem import WordNetLemmatizer
from gensim.models import LdaModel
from gensim.corpora import Dictionary

# Recurrently used NLP-related objects
spacy_model = spacy.load("en_core_web_sm")
lemmatizer = WordNetLemmatizer()


def preprocess_documents(documents):
    """
    Normalize texts in a list of documents.
    :param documents: list of documents (string)
    :return: list of processed documents
    """
    processed_docs = []

    for doc in documents:
        processed_doc = []

        # Tokenize document
        tokens = spacy_model(doc)

        for token in tokens:
            # Only include nominal words
            if 'NN' in token.tag_:
                # Normalize text
                token_text = token.text.lower()
                token_text = lemmatizer.lemmatize(token_text)
                processed_doc.append(token_text)

        processed_docs.append(processed_doc)

    return processed_docs


def build_model(documents, iterations=10, num_topics=10):
    """
    Build and train an LDA topic model for a list of documents.
    :param documents: list of documents
    :param iterations: number of iterations for the LDA model
    :param num_topics: number of topics for the LDA model
    :return: LDA topic model of the list of documents
    """
    # Get bag of words and word ID dictionary
    dictionary = Dictionary(documents)
    bows = [dictionary.doc2bow(doc) for doc in documents]
    temp = dictionary[0]
    id2word = dictionary.id2token

    # Train model
    model = LdaModel(corpus=bows, id2word=id2word, iterations=iterations,
                     num_topics=num_topics)

    return model


def get_topic_model(corpus, iterations, num_topics):
    """
    Get corpus of Wikipedia articles on bird species and a topic model based on
    the corpus.
    :param iterations: number of iterations for training the topic model
    :param num_topics: number of topics specified for the topic model
    :return: topic model, dictionary of bird family name to list of documents
    """
    # Gather all texts, regardless of taxonomic family
    documents = [doc for fam in corpus for doc in corpus[fam]]

    # Preprocess texts in corpus
    documents = preprocess_documents(documents)

    # Build and train topic model
    topic_model = build_model(documents, iterations, num_topics)

    return topic_model
