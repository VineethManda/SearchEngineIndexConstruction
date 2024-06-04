# Search Engine Index Construction

This project involves building a search engine index and evaluating its performance using manually judged relevance judgments. Below are the descriptions and formats of the key files involved:

## Description and Format of 'qrels' file

The 'main.qrels' file contains relevance judgments for each of the topics (queries) present in the 'topics.txt' file. This file is crucial for determining the performance of the search engine system. The format of the 'main.qrels' file is as follows:


- **TOPIC**: The topic number.
- **ITERATION**: Feedback iteration (usually zero and not used).
- **DOCUMENT**: The document name corresponding to the "docno" field in the documents.
- **RELEVANCY**: A binary code where 0 represents not relevant and 1 represents relevant.

Note: Not all documents are manually judged for relevance to a topic. If a document name is not present in the file for any topic, it's assumed to be irrelevant for evaluation.

## Description and Format of the 'topics' file

The 'topics.txt' file contains queries, each enclosed within <top> and </top> tags. The format of each topic (query) is as follows:

