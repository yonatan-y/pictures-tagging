'''This module's main purpose is to process an image by using Google Vision API.'''

import json
import io
import os
import sys  # provides access to any command-line arguments.
import base64  # base64 encoding library.
import requests  # http library.

#-------------------------------------------------------------------------------------------------#


def add_image_content(image_location):
    '''This function returns the image content to add to the request body
       that will be sent to the vision api.'''

    # Read image from this device and represent the image as a stream of bytes, by using
    # 'rb' option, which is reading in binary format.
    try:
        with io.open(image_location, 'rb') as image_file:
            content = image_file.read()

    except:
        print('\nError! can\'t find image or read data.\n')
        sys.exit(3)


    # Perform base64 encoding of the image data.
    content = base64.b64encode(content)
    content = str(content, 'utf-8')

    content_dict = {'content' : content}
    return content_dict


#-------------------------------------------------------------------------------------------------#


def add_image_source(image_uri):
    '''This function returns the image URL to add to the request body
       that will be sent to the vision api.'''

    source_dict = {'source' : {'imageUri' : image_uri}}
    return source_dict

#-------------------------------------------------------------------------------------------------#

def add_detection_type(detection_type):
    '''This function returns the type of detection to add to the request body
       that will be sent to the vision api.'''

    types = {'labels' : 'LABEL_DETECTION', 'landmarks' : 'LANDMARK_DETECTION',
             'logos' : 'LOGO_DETECTION', 'web' : 'WEB_DETECTION',
             'faces' : 'FACE_DETECTION', 'text' : 'DOCUMENT_TEXT_DETECTION'}

    if detection_type == 'labels':
        return types['labels']
    elif detection_type == 'landmarks':
        return types['landmarks']
    elif detection_type == 'logos':
        return types['logos']
    elif detection_type == 'web':
        return types['web']
    elif detection_type == 'faces':
        return types['faces']
    elif detection_type == 'text':
        return types['text']
    else:
        print('\nError! unknown detection type.\n')
        sys.exit(3)





#-------------------------------------------------------------------------------------------------#



def extract_faces(response):
    '''This function gets the response with the faces annotations,
       and returns a list of faces.
       Each face is a list of coordinates around the face.'''

    faces_quantity = len(response['faceAnnotations'])
    faces = []
    for i in range(faces_quantity) :
        face = response['faceAnnotations'][i]['boundingPoly']['vertices']
        for j in range(4) :
            face[j] = (face[j]['x'] , face[j]['y'])
        faces.append(face)


    return faces



#-------------------------------------------------------------------------------------------------#

def make_request(args):
    '''This function builds the wanted request, sends the request to the
       vision api for processing, and returns the response.'''

    try:
        api_file = io.open('api_key.txt', 'r')
        api_key = api_file.read()
    except:
        print('\nError! can\'t find or read api key.\n')
        sys.exit(3)

    url = 'https://vision.googleapis.com/v1/images:annotate?key=' + api_key
    req = {'requests' : [{'image' : None, 'features' : [{'type' : None}]}]}

    if len(args) == 4:
        if args[2] == 'content':
            req['requests'][0]['image'] = add_image_content(args[3])
        elif args[2] == 'source':
            req['requests'][0]['image'] = add_image_source(args[3])

        request_features_type = req['requests'][0]['features'][0]
        request_features_type['type'] = add_detection_type(args[1])

    else:
        print('\nError! arguments length is not valid.\n')
        sys.exit(3)


    # Make a post request and print the response package.
    r = requests.post(url, data=json.dumps(req))
    #print(r)
    #print('status code:' ,r.status_code)
    print(json.dumps(json.loads(r._content), indent=4))
    #print('size:', r._content.__sizeof__())



    #The last cell of the returned list determines whether an actual data received,
    #or not (because of an error).
    if r.status_code != 200:
        print('\n\n dont save data\n\n\n')
        return [json.dumps(json.loads(r._content), indent=4), args[3], False]

    keys = list(json.loads(r._content)['responses'][0].keys())
    if keys.__len__() == 0 or (keys.__len__() > 0 and keys[0] == 'error'):
        print('\n\n dont save data\n\n\n')
        return [json.dumps(json.loads(r._content), indent=4), args[3], False]


    if args[1] == 'faces':
        faces = extract_faces(json.loads(r._content)['responses'][0])
        return [json.dumps(json.loads(r._content)['responses'][0], indent=4), args[3], True, faces]

    return [json.dumps(json.loads(r._content)['responses'][0], indent=4), args[3], True]



#-------------------------------------------------------------------------------------------------#




