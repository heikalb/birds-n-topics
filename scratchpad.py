from nltk.corpus import brown
from nltk.stem import WordNetLemmatizer
from gensim.models import LdaModel
from gensim.corpora import Dictionary

documents = []
lemmatizer = WordNetLemmatizer()

for id in brown.fileids():
    document = brown.tagged_words(id)
    document = [w[0].lower() for w in document if 'NN' in w[1]]
    document = [lemmatizer.lemmatize(w) for w in document]
    documents.append(document)


dictionary = Dictionary(documents)
dictionary.filter_extremes(no_above=0.5, no_below=20)
corpus = [dictionary.doc2bow(doc) for doc in documents]
temp = dictionary[0]
id2word = dictionary.id2token

model = LdaModel(corpus=corpus, id2word=id2word, chunksize=100, alpha='auto',
    eta='auto',
    iterations=100,
    num_topics=50,
    passes=1,
    eval_every=None)

topics = model.top_topics(corpus)

for topic in topics:
    for x in topic[0]:
        print(x)
    print(topic[1], '\n')

sent = "The Whooping Crane is the tallest bird in North America and one of the most awe-inspiring, with its snowy white plumage, crimson cap, bugling call, and graceful courtship dance. It's also among our rarest birds and a testament to the tenacity and creativity of conservation biologists. The species declined to around 20 birds in the 1940s but, through captive breeding, wetland management, and an innovative program that teaches young cranes how to migrate, numbers have risen to about 600 today."
sent = sent.split()
test = [sent]
d = Dictionary(test)
test_doc = [d.doc2bow(s) for s in test]
x = model.get_document_topics(test_doc)

for e in x:
    print(e)

