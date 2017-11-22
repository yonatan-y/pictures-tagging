
import json
import io

# Import sys module which provides access to any command-line arguments
import sys

# Import the base64 encoding library.
import base64

# Import http library.
import requests

#----------------------------------------------------------------------------------------------------#


def add_image_content(image_location) :
    # Read image from this device and represent the image as a stream of bytes, by using
    # 'rb' option, which is reading in binary format.
    with io.open(image_location, 'rb') as image_file:
        content = image_file.read()
    # Perform base64 encoding of the image data.
    content = base64.b64encode(content)
    content = str(content, 'utf-8')

    content_dict = {'content' : content}
    return content_dict


#----------------------------------------------------------------------------------------------------#


def add_image_source(image_uri) :
    source_dict = {'source' : {'imageUri' : image_uri}}
    return source_dict

#----------------------------------------------------------------------------------------------------#




api_file = io.open('api_key.txt', 'r')
api_key = api_file.read()
url = 'https://vision.googleapis.com/v1/images:annotate?key=' + api_key
req = {'requests' : [ {'image' : None, 'features' : [{'type' : 'LABEL_DETECTION'}]}]}


if(sys.argv.__len__() == 3) :
    if(sys.argv[1] == 'content') :
        req['requests'][0]['image'] = add_image_content(sys.argv[2])
    elif(sys.argv[1] == 'source') :
        req['requests'][0]['image'] = add_image_source(sys.argv[2])

else :
    sys.exit(0)




# Make a post request and print the response package.
r = requests.post(url, data=json.dumps(req))
print(r)
print(r._content)
print(json.dumps(json.loads(r._content), indent=4))




print('\n\n\ndone')