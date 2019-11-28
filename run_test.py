"""
Classify documents using topic similarity. The documents are Wikipedia articles
on bird species. The categories are bird taxonomic families (e.g. Passerellidae
, Anatidae). Documents in a comparison list are divided by taxonomic families.
Documents in the test list are to be classified on the taxonomic family of the
bird species that the article is about. Test documents are assigned to a bird
family based on its topic similarity to the other articles under that category.
Heikal Badrulhisham, 2019 <heikal93@gmail.com>
"""
from get_data import get_data
import random
from build_topic_model import get_topic_model
from build_topic_model import preprocess_documents
from gensim.corpora import Dictionary
from collections import defaultdict


def split_corpus(corpus, train_proportion):
    """
    Split the corpus into comparison and test lists. Helper method for main()
    :param corpus: list of documents
    :param test_proportion: proportion of documents to go into the training set
    :return: list of documents up to the split index, list of documents
    starting from the split index
    """
    # Find index to split on
    num_docs = [len(corpus[fam]) for fam in corpus]
    split = int(min(num_docs)*train_proportion)

    comparison_docs = dict()
    test_docs = dict()

    for fam in corpus:
        comparison_docs[fam] = corpus[fam][:split]
        test_docs[fam] = corpus[fam][split:]

    return comparison_docs, test_docs


def get_topics(corpus, topic_model):
    """
    Get the topics of each document in a corpus. Helper method for main().
    :param corpus: list of documents
    :param topic_model: LDA topic model
    :return: list of list of topics of each document
    """
    family_topics = dict()

    for fam in corpus:
        family_topics[fam] = []

        for doc in corpus[fam]:
            # Get topic of the document based on the topic model
            doc = preprocess_documents([doc])
            dictionary = Dictionary(doc)
            bow = [dictionary.doc2bow(d) for d in doc]
            topic = topic_model.get_document_topics(bow)
            family_topics[fam].append(topic)

    return family_topics


def compare_topics(comparison_topics, test_topics):
    """
    For every document in the test list, find the category of documents in the
    comparison list that it is most similar with. Helper method for main().
    :param comparison_topics: list of topics of documents in the comparison
    list
    :param test_topics: list of topics of documents in the test list
    :return: list of tuples where tuple[0] is the expected category and
    tuple[1] is the predicted category of the test documents
    """
    predictions = []

    for fam in test_topics:
        for doc in test_topics[fam]:
            prediction = closest_category(doc, comparison_topics)
            predictions.append((fam, prediction))

    return predictions


def closest_category(document, comparison_topics):
    """
    For the given document, find the category of documents in the comparison
    list that it is most similar with. Helper method for compare_topics()
    :param document: the list of topics of the target document
    :param comparison_topics: list of topics of documents in the comparison
    list
    :return: category label for the target document, i.e. the bird family
    """
    fam_similarity = defaultdict(int)

    # Sum up cosine similarity of the target document topics with the
    # comparison documents. Average the sum
    for fam in comparison_topics:
        for comp_doc in comparison_topics[fam]:
            #fam_similarity[fam] += cosine_similaity(document, comp_doc)
            fam_similarity[fam] += count_similarity(document, comp_doc)

        fam_similarity[fam] = fam_similarity[fam]/len(comparison_topics[fam])

    # Find the category of documents with which the target document has the
    # highest average cosine similarity
    max_sim = 0
    closest_family = ''

    for fam in fam_similarity:
        if fam_similarity[fam] >= max_sim:
            max_sim = fam_similarity[fam]
            closest_family = fam

    return closest_family


def count_similarity(topics_1, topics_2):
    """
    Count the number of common topics in two lists of topics. Helper method for
    closest_category().
    :param topics_1: list of topics of the first document
    :param topics_2: list of topics of the second document
    :return: Number of common topics in the two topic lists
    """
    # Deal with quirk of TransformedCorpus object in Gensim
    topics_1 = [t[0] for t in topics_1[0]]
    topics_2 = [t[0] for t in topics_2[0]]

    return len([t for t in topics_1 if t in topics_2])


def cosine_similaity(topics_1, topics_2):
    """
    Calculate the cosine similarity of two list of topics. Helper method for
    closest_category().
    :param topics_1: list of topics of the first document
    :param topics_2: list of topics of the second document
    :return: cosine similarity of the topics of the two document
    """
    # Deal with quirk of TransformedCorpus object in Gensim
    topics_1 = topics_1[0]
    topics_2 = topics_2[0]

    # Components of cosine similarity
    sum_ab = 0
    sum_a_2 = 0
    sum_b_2 = 0

    # Add up vector components
    for t1 in topics_1:
        counterpart = [t2 for t2 in topics_2 if t1[0] == t2[0]]

        # Skip vector components without a value in either topic list
        if counterpart:
            t2 = counterpart[0]
            sum_ab += t1[1]*t2[1]
            sum_a_2 += t1[1]**2
            sum_b_2 += t2[1]**2

    if not sum_ab:
        return 0

    return sum_ab/(sum_a_2*sum_b_2)


def evaluate_predictions(predictions):
    """
    Evaluate the accuracy of predicted document categories and display
    the results. Helper method for main().
    :param predictions: list of tuples where tuple[0] is the expected category
     and tuple[1] is the predicted category of the test documents
    :return:
    """
    # Print results for each test case
    for prediction in predictions:
        print(f'Expected: {prediction[0]}\tPredicted: {prediction[1]}')

    # Display overall accuracy
    num_matches = len([p for p in predictions if p[0] == p[1]])
    total = len(predictions)
    percentage = round(num_matches/total*100, 2)
    print(f'Matches: {num_matches}/{total} ({percentage}%)')


def main():
    """
    Get corpus and an LDA topic model based on it. Assign documents in the test
    list to a document category based on similarity in topics.
    """
    # Get corpus
    corpus = get_data()

    # Randomize document order
    for fam in corpus:
        random.shuffle(corpus[fam])

    # Split corpus into comparison and test lists
    comparison_docs, test_docs = split_corpus(corpus, 0.5)

    # Train an LDA topic model on the comparison documents
    topic_model = get_topic_model(comparison_docs, 100, 50)

    # Get the topics of the documents in the comparison list
    comparison_topics = get_topics(comparison_docs, topic_model)
    test_topics = get_topics(test_docs, topic_model)

    # Get predictions of category labels of test documents
    predictions = compare_topics(comparison_topics, test_topics)

    # Display results
    evaluate_predictions(predictions)


if __name__ == '__main__':
    main()
    exit(0)
