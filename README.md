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

<num> Unique Query Number

<title> Main Query (Max. three words)
<desc> One-sentence description of the query
<narr> Concise description of what makes a document relevant

  The main query is specified within the <title> tag. The <desc> and <narr> sections can be utilized for query expansion or to enhance the precision of the system.

Description and Format of the output of your Query Processor
The Query Processor should process all topics (queries) in batch mode and produce an output file with the following format:

TOPIC: The topic number.
DOCUMENT: The document name corresponding to the "docno" field in the documents.
UNIQUE#: A unique counter representing the number of documents retrieved for each topic.
COSINE_VALUE: The cosine similarity score for each document with respect to the topic (using TF*IDF as the weighting scheme).
Each column is separated by a TAB.

Refer to the 'sample_output.txt' for an example of how the output should look.

