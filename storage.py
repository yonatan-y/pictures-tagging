'''This module is responsible for communicating with elasticsearch database,
including all actions e.g. save, delete, search and more.'''

import json
import logging
from elasticsearch import Elasticsearch



#Disable all non-ERROR level messages.
#This allows to check the connection without logging traceback.
logging.basicConfig(level=logging.ERROR)

es = Elasticsearch()
#print(es.cluster.health())


#--------------------------------------------------------------------------------------------------#

def store_labels_data(json_package, image):
    '''This function stores labels for a given image.
       If the index does not exist, it will be created first.'''

    es.create(index='labels_data', doc_type='doc', id=image, body=json_package)


#--------------------------------------------------------------------------------------------------#


def get_labels_data(image):
    '''This function gets an image id,
       and prints the labels of the image, if there are such labels.'''

    if not es.indices.exists(index='labels_data'):
        print('\nThere is no index for labels.\n')
        return

    data = es.get(index='labels_data', doc_type='doc', id=image, ignore=404)
    if data['found'] is False:
        print('\nThere are no labels for the given image.\n')
    else:
        print(json.dumps((data), indent=4))


#--------------------------------------------------------------------------------------------------#



def delete_labels_data(image):
    '''This function gets an image id, and deletes the stored labels of the image,
       if there are such labels.'''

    if not es.indices.exists(index='labels_data'):
        print('\nThere is no index for labels.\n')
        return

    delete = es.delete(index='labels_data', doc_type='doc', id=image, ignore=404)
    if delete['result'] == 'not_found':
        print('\nThere are no labels to delete.\n')
    elif delete['result'] == 'deleted':
        print('The labels of', image, 'were deleted successfully.\n')

    if int(es.count(index='labels_data', doc_type='doc')['count']) == 0:
        delete_index('labels_data')


#--------------------------------------------------------------------------------------------------#


def delete_all_indices():
    '''This function deletes all indices.
       The storage will be completely empty after this function(!!!).
       If there are no indices, the function does nothing.'''

    es.indices.delete(index='*', ignore=404)



#--------------------------------------------------------------------------------------------------#

def delete_index(index_name):
    '''This function deletes specific index from storage
       including all documents in the index.'''

    es.indices.delete(index=index_name, ignore=404)



#--------------------------------------------------------------------------------------------------#


def get_images_by_tag(tag):
    '''This function gets a tag name, and prints all related images.'''

    if not es.indices.exists(index='labels_data'):
        print('\nThere is no index for labels_data.\n')
        return
    
    query = {'query' : { 'match' : { 'labelAnnotations.description' : tag } }, 'stored_fields' : [] }

    res = es.search(index='labels_data', doc_type='doc', body=query)

    if int(res['hits']['total']) == 0:
        print('\nThere are no images with the tag \'', tag, '\'.')

    else:
        print('\nAll images with the tag \'', tag, '\' :')
        for i in res['hits']['hits']:
            print (i['_id'])
   


#--------------------------------------------------------------------------------------------------#

def get_num_of_documents(index_name):
    '''This function prints the munber of images in a specific index.'''

    if not es.indices.exists(index=index_name):
        print('\nThere is no index for', index_name, '.\n')
        return
   
    num = es.count(index=index_name, doc_type='doc')
    num = num['count']

    print('\nNumber of images in', index_name, ':', num, '.\n')


#--------------------------------------------------------------------------------------------------#

def get_all_documents(index_name):
    '''This function prints a list of all images in a specific index.'''

    if not es.indices.exists(index=index_name):
        print('\nThere is no index for', index_name, '.\n')
        return

    query = { 'query' : { 'match_all' : {} } , 'stored_fields' : [] }

    res = es.search(index='labels_data', doc_type='doc', body=query, )

    if int(res['hits']['total']) == 0:
        print('\nThere are no images in the index', index_name, '.\n')

    else:
        print('\nAll images in the index', index_name, ':')
        for i in res['hits']['hits']:
            print(i['_id'])


#--------------------------------------------------------------------------------------------------#

def check_connection():
    '''This function determines whether the Elasticsearch cluster is up, or not.'''

    return es.ping()


#--------------------------------------------------------------------------------------------------#

def get_images_by_score(score):
    '''This function gets a score, and prints all images that contains at least
        one tag with same score or higher score.'''
    
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
            print (i['_id'])


#--------------------------------------------------------------------------------------------------#
