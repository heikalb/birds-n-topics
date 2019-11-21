"""

Heikal Badrulhisham, 2019 <heikal93@gmail.com>
"""
from build_topic_model import get_topic_model
from build_topic_model import preprocess_documents
from gensim.corpora import Dictionary


def split_corpus(corpus, split_idx):
    """

    :param corpus:
    :param split_idx:
    :return:
    """
    comparison_docs = dict()
    test_docs = dict()

    for fam in corpus:
        comparison_docs[fam] = corpus[fam][:split_idx]
        test_docs[fam] = corpus[fam][split_corpus:]

    return comparison_docs, test_docs


def get_topics(corpus, topic_model):
    """

    :param corpus:
    :param topic_model:
    :return:
    """
    family_topics = dict()

    for fam in corpus:
        family_topics[fam] = []

        for doc in corpus[fam]:
            doc = preprocess_documents([doc])
            dictionary = Dictionary(doc)
            bow = [dictionary.doc2bow(d) for d in doc]
            topic = topic_model.get_document_topics(bow)
            family_topics[fam].append(topic)

    return family_topics


def compare_topics(comparison_topics, test_docs, topic_model):
    """

    :param comparison_topics:
    :param test_docs:
    :param topic_model:
    :return:
    """
    return


def main():
    topic_model, corpus = get_topic_model()

    split = int(len(corpus[corpus.keys()[0]])*0.8)
    comparison_docs, test_docs = split_corpus(corpus, split)

    comparison_topics = get_topics(corpus, topic_model)


if __name__ == '__main__':
    main()
    exit(0)
