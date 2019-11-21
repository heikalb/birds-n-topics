from build_topic_model import get_topic_model
from build_topic_model import preprocess_documents
from gensim.corpora import Dictionary


def split_corpus(corpus, split_idx):
    comparison_docs = dict()
    test_docs = dict()

    for fam in corpus:
        comparison_docs[fam] = corpus[fam][:split_idx]
        test_docs[fam] = corpus[fam][split_corpus:]

    return comparison_docs, test_docs



def get_topics(corpus, topic_model):
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


def main():
    topic_model, corpus = get_topic_model()
    comparison_docs, test_docs

if __name__ == '__main__':
    main()
    exit()