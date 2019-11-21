"""

Heikal Badrulhisham, 2019 <heikal93@gmail.com>
"""
from build_topic_model import get_topic_model
from build_topic_model import preprocess_documents
from gensim.corpora import Dictionary


def split_corpus(corpus, split_idx):
    """
    Split the corpus into comparison and test sets
    :param corpus: list of documents
    :param split_idx: index of the split
    :return: list of comparison documents, list of test documents
    """
    comparison_docs = dict()
    test_docs = dict()

    for fam in corpus:
        comparison_docs[fam] = corpus[fam][:split_idx]
        test_docs[fam] = corpus[fam][split_idx:]

    return comparison_docs, test_docs


def get_topics(corpus, topic_model):
    """
    Get the topics of each document in a corpus
    :param corpus: list of documents
    :param topic_model: LDA topic model
    :return: list of list of topics of each document
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


def compare_topics(comparison_topics, test_topics, topic_model):
    """

    :param comparison_topics:
    :param test_docs:
    :param topic_model:
    :return:
    """
    predictions = []

    for fam in test_topics:
        for doc in test_topics[fam]:
            prediction = closest_category(doc, comparison_topics)
            predictions.append((fam, prediction))

    return


def closest_category(document, comparison_topics):
    closest_family = ''
    highest_similarity = 0

    for fam in comparison_topics:
        for comp_doc in comparison_topics[fam]:
            similarity = cosine_similaity(document, comp_doc)

            if similarity > highest_similarity:
                closest_family = fam
                highest_similarity = similarity

    return closest_family


def cosine_similaity(topic_1, topic_2):
    sum_ab = 0
    sum_a_2 = 0
    sum_b_2 = 0

    for i in range(len(topic_1)):
        sum_ab += topic_1[i][1]*topic_2[i][1]
        sum_a_2 += topic_1[i][1]**2
        sum_b_2 += topic_2[i][1]**2

    return sum_ab/(sum_a_2*sum_b_2)




def main():
    # Get topic model and the corpus
    topic_model, corpus = get_topic_model()

    # Split corpus into comparison and test sets
    keys = [k for k in corpus]
    split = int(len(corpus[keys[0]])*0.8)
    comparison_docs, test_docs = split_corpus(corpus, split)

    # Get the topics of the documents in the comparison set
    comparison_topics = get_topics(comparison_docs, topic_model)
    test_topics = get_topics(test_docs, topic_model)

    for f in comparison_topics:
        for d in comparison_topics[f]:
            for t in d:
                print(t)


    # Compare the topics of the test set to the comparison set
    compare_topics(comparison_topics, test_topics, topic_model)

if __name__ == '__main__':
    main()
    exit(0)
