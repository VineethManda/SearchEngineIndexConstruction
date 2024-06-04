import os
import re
from nltk.stem import PorterStemmer
import math
# from porterStemm import PorterStemmer

# reading stop words
f = open('stopwordlist.txt', 'r')
stop_words = [word.lstrip(" ") for word in f.read().split('\n')]
f.close()

# defining the Stemmer
porter_stemmer = PorterStemmer()


# Defining the tokenizer
def tokenize(document):
    # document = re.sub(r"^\d+| \d+|[.,:;]\d+|\d+[.,:;]", '', document)
    document = re.sub(r"(^|\s|.|,|:)\d+($|\s|.|,|:|%)", r'\1\2', document)
    tokens = re.findall(r'\w+', document.lower())
    # tokens = re.split(r'\W|\s',document.lower())
    return tokens

# forward index generator
word_to_id = {}
def forward_index(docs):
    forward_index = {}
    current_id = 0
    for doc, text in docs.items():
        forward_index[doc] = []
        freq_word = {}
        # iterating over each word in the text corpus
        for word in text:
            if word not in word_to_id:
                word_to_id[word] = current_id
                current_id += 1
            wordID = word_to_id[word]
            if wordID not in freq_word:
                freq_word[wordID] = 0
            freq_word[wordID] += 1
        
        # adding the forward_index value to the dictionary
        for wordID, freq in freq_word.items():
            forward_index[doc].append(f"wordId{wordID}: {freq}")
    
    return forward_index

# Inverted Index Generator
def inverted_index(docs):
    inverted_index = {}
    for doc, words in docs.items():
        for word in words:
            wordID = "wordID" + str(word_to_id[word])
            # adding an instance for the wordID if not exist in inverted_index
            if wordID not in inverted_index:
                inverted_index[wordID] = {}

            #initializing the value for WordID and Document in inverted_index 
            if doc not in inverted_index[wordID]:
                inverted_index[wordID][doc] = 0
            inverted_index[wordID][doc] += 1
    
    return inverted_index


#reading the TREC input
def read_trec(filename):
    docs_datas = {}
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        docs = re.findall(r'<DOC>.*?</DOC>', content, re.DOTALL)
        for doc in docs:
            #extracting document Name
            doc_name = re.findall(r'<DOCNO>(.*?)</DOCNO>', doc, re.DOTALL)
            doc_name = re.sub(r'\s','', doc_name[0])

            # Extracting the document "text"
            text = re.search(r'<TEXT>(.*?)</TEXT>', doc, re.DOTALL).group(1).strip()

            # Tokenizing the document into words
            words = tokenize(text.lower())

            # Removing stop words and stemming the remaining words
            words = [porter_stemmer.stem(word) for word in words if word not in stop_words]
            # print(f"{doc_name}",words)
            docs_datas[doc_name] = words
    
    return docs_datas

from collections import defaultdict

def extract_query(text):
    num = None
    title = None
    result = {}

    for line in text.split('\n'):
        if '<num>' in line:
            num = line.split(':')[-1].strip()
        elif '<title>' in line:
            title = line.split(':')[-1].strip()
        elif '</top>' in line:
            if num and title:
                result[num] = title
            num = None
            title = None
    
    return result



def search_index(query, inverted_index, docs, num):
    query = [porter_stemmer.stem(word) for word in tokenize(query) if word not in stop_words]

    scores = defaultdict(float)
    idf_values = {}
    for term in query:
        try:
            if term in word_to_id:
                term_id = "wordID" + str(word_to_id[term])
                n = len(inverted_index[term_id])
                idf_values[term] = math.log(len(docs) / n)
        except:
            continue

    for term, idf in idf_values.items():
        term_id = "wordID" + str(word_to_id[term])
        postings = inverted_index.get(term_id, {})
        for doc, freq in postings.items():
            if doc in docs:
                max_tf = max(postings.values())
                tf = (1 + math.log10(freq)) / (1 + math.log10(max_tf))
                scores[doc] += tf * idf
    ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    output_str = ""
    for i, (doc_id, score) in enumerate(ranked_docs):
        doc = docs[doc_id]
        output_str += f"\n{num}    {doc_id}    {i+1}    {score:.6f}"

    return output_str.strip() 


f = open('topics.txt', 'r')
topics = f.read()
queries = extract_query(topics)
f.close

k = open('search_index_output.txt', 'w')

root = './ft911'
output_data = {}
for filename in os.listdir(root):
    if filename.startswith('ft911'):
        docs = read_trec("./ft911/"+str(filename))
        FI = forward_index(docs)
        II = inverted_index(docs)

        # extacting the query :
        for num,query in queries.items():
            result = search_index(query, II, docs, num)
            k.write(result)
k.close()