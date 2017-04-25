# -*- coding: UTF-8 -*-
'''
summariser.py generates the summary of the given document using TextRank Algorithm
'''
from pattern.text.de import parse, split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import networkx as nx


#with open("original.txt",'r') as f:
 #   document=f.read()

def sentenceTokeniser(text):
    '''
    @sentenceTokeniser tokenises the given document into list of sentences
    :param text: document
    :return: list of sentences
    '''
    result =[]
    document = ' '.join(text.strip().split('\n'))
    taggedSentences = parse(document)
    sentences=split(taggedSentences)
    for sentence in sentences:
        result.append(sentence.string)
    print len(result)
    return result


def normalisedBagofWordsMatrix(sentences):
    '''
    @normalisedBagofWordsMatrix creates a normalised bag of words matrix
    :param sentences: list of sentences
    :return: normalised bag of words array
    '''
    c = CountVectorizer()
    bow_matrix = c.fit_transform(sentences)
    normalized_matrix = TfidfTransformer().fit_transform(bow_matrix)
    return normalized_matrix

def getsimilarityGraph(matrix):
    '''
    @getsimilarityGraph generates similarity graph from given normalised bag of words matrix
    :param matrix: normalised bag of words matrix
    :return: similarity graph
    '''
    similarity_graph = matrix * matrix.T
    nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
    return nx_graph

def getTextRank(sentenceGraph,sentences):
    '''
    @getTextRank ranks the given set of sentences based on similarity
    :param sentenceGraph: similarity graph obtained from @getsimilarityGraph
    :param sentences: list of sentences in the document
    :return: sorted list of tuples containing similarity score and sentence
    '''
    scores = nx.pagerank(sentenceGraph)
    ranked = sorted(((scores[i], s) for i, s in enumerate(sentences)),
                    reverse=True)
    return ranked

def TextRank(document):
    '''
    @TextRank summarises the given document based on similarity between different sentences in the document
    :param document: document to summarise
    :return: document summary
    '''
    sentences = sentenceTokeniser(document)
    matrix = normalisedBagofWordsMatrix(sentences)
    similarityGraph = getsimilarityGraph(matrix)
    rankedSentences = getTextRank(similarityGraph,sentences)
    return rankedSentences


#for sentence in TextRank(document):
 #   print sentence