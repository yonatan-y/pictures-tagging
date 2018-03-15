'''This module is responsible for communicating with elasticsearch database,
including all actions e.g. save, delete, search and more.'''

import json
import logging
from elasticsearch import Elasticsearch, TransportError


#The possible indices in storage:
indices = ['labels', 'landmarks', 'logos', 'web', 'faces', 'text']

#Disable all non-ERROR level messages.
#This allows to check the connection without logging traceback.
logging.basicConfig(level=logging.ERROR)


es = Elasticsearch() #Represents the elasticsearch client.



#--------------------------------------------------------------------------------------------------#

def store_data(index, json_package, image_id):
    '''This function stores data in an index for a given image.
       If the index does not exist, it will be created first.'''

    #If the image already exists in the index, raise exception.
    try:
        es.create(index=index, doc_type='doc', id=image_id, body=json_package)
        return True
    except TransportError:
        return False


#--------------------------------------------------------------------------------------------------#


def get_data(index, image_id):
    '''This function gets an image id and index,
       and prints the data of the image in the index.'''

    if not es.indices.exists(index=index):
        print('\nThere is no', index, 'index.\n')
        return

    data = es.get(index=index, doc_type='doc', id=image_id, ignore=404)
    if data['found'] is False:
        print('\nThere is no data in', index, 'index for the given image.\n')
    else:
        print(json.dumps((data), indent=4))


#--------------------------------------------------------------------------------------------------#



def delete_data(index, image_id):
    '''This function gets an image id, and deletes the stored data of the image
       in the index.'''

    if not es.indices.exists(index=index):
        print('\nThere is no', index, 'index.\n')
        return

    delete = es.delete(index=index, doc_type='doc', id=image_id, ignore=404)

    if delete['result'] == 'not_found':
        print('\nThere is no data to delete in', index, 'index.\n')

    elif delete['result'] == 'deleted':
        print('The data of', image_id, 'were deleted successfully.\n')

    if int(es.count(index=index, doc_type='doc')['count']) == 0:
        delete_index(index)


#--------------------------------------------------------------------------------------------------#


def delete_all_indices():
    '''This function deletes all indices.
       The storage will be completely empty after this function(!!!).
       If there are no indices, the function does nothing.'''

    es.indices.delete(index='*', ignore=404)



#--------------------------------------------------------------------------------------------------#

def delete_index(index):
    '''This function deletes specific index from storage
       including all documents in the index.'''

    es.indices.delete(index=index, ignore=404)



#--------------------------------------------------------------------------------------------------#


def get_images_by_words(words):
    '''This function gets words, and prints all images that contain
       data with the words, at least in one index.'''
    
    query = {
        'query':{
            'bool':{
                'should':[
                    {'match' : { 'labelAnnotations.description' : words} },
                    {'match' : { 'landmarkAnnotations.description' : words} },
                    {'match' : { 'logoAnnotations.description' : words} },
                    {'match' : { 'textAnnotations.description' : words} },
                    {'match' : { 'webDetection.webEntities.description' : words} }
                    ]
                }
            },
        'stored_fields' : []
        }

    res = es.search(index='*', doc_type='doc', body=query, ignore=404)

    if int(res['hits']['total']) == 0:
        print('\nThere are no images with the word/s \'', words, '\'.')

    else:
        print('\nAll images with the word/s \'', words, '\' :')
        for i in res['hits']['hits']:
            print(i['_id'])



#--------------------------------------------------------------------------------------------------#

def get_num_of_documents(index):
    '''This function prints the munber of images in a specific index.'''

    if not es.indices.exists(index=index):
        print('\nThere is no', index,'index.\n')
        return
   
    num = es.count(index=index, doc_type='doc')
    num = num['count']

    print('\nNumber of images in', index, 'index:', num, '.\n')


#--------------------------------------------------------------------------------------------------#

def get_all_documents(index, start=0, size=2):
    '''This function prints a list of all images in a specific index.'''

    if not es.indices.exists(index=index):
        print('\nThere is no', index, 'index.\n')
        return None

    image_ids = []

    query = { 'query' : { 'match_all' : {} } , 'stored_fields' : [] }

    res = es.search(index=index, doc_type='doc', body=query, from_=start, size=size)

    if int(res['hits']['total']) == 0:
        print('\nThere are no images in', index, 'index.\n')

    else:
        print('\nAll images in', index, 'index:')
        for i in res['hits']['hits']:
            print(i['_id'])
            image_ids.append(i['_id'])

    return image_ids


#--------------------------------------------------------------------------------------------------#

def check_connection():
    '''This function determines whether the Elasticsearch cluster is up, or not.'''

    return es.ping()


#--------------------------------------------------------------------------------------------------#

def get_images_by_score(score):
    '''This function gets a score, and prints all images that contains at least
        one description with same score or higher score.'''
    
    if not isinstance(score, (float, int)):
        print('Error! input must be float.\n')
        return

    score = float(score)

    if not es.indices.exists(index='labels_data'):
        print('\nThere is no index for labels_data.\n')
        return

    query = {
        'query':{
            'bool':{
                'must': {'match_all': {}},
                'filter':{
                    'range':{
                        'labelAnnotations.score':{
                            'gte': score
                            }
                        }
                    }
                }
            }
        }

    res = es.search(index='labels_data', doc_type='doc', body=query)
    #print(json.dumps(res, indent=4))
    if int(res['hits']['total']) == 0:
        print('\nThere are no images with the score', score, 'or higher.\n')

    else:
        print('\nAll images with the score', score, 'or higher:')
        for i in res['hits']['hits']:
            print(i['_id'])


#--------------------------------------------------------------------------------------------------#
