# Birds and topics
*Is an article about Wood Ducks written more like an article about Snow
 Geese than an article about Song Sparrows?*

This project is about using topic similarity for text classification.
The data in this project consist of content of Wikipedia pages of bird
 species from several taxonomic families (e.g. Passerellidae
, Anatidae). The main task involves assigning test documents to one of these
taxonomic families. This is done by comparing the topics of the target
 document to the topics of documents under different families. The motivation
 for this is the hypothesis that similarities between bird species under a
  family should translate into similarities in texts describing them.
  
## Components
- `get_data.py`: gets a corpus of Wikipedia articles on bird species from
two taxonomic families representing waterfowls and sparrows.
- `build_topic_model.py`: builds and trains a Latent Dirichlet Allocation
 (LDA) topic model based on the corpus.
- `run_test.py`: assigns test documents to one of the taxonomic families, 
display results of the test. The first two programs are called upon here.

## Requirements
- beautifulsoup4
- spacy
- nltk
- gensim