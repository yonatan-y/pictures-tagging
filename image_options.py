'''This modules provides options to mark or cut faces
and create new images.'''

from PIL import Image, ImageDraw

#--------------------------------------------------------------------------------------------------#

def draw(input_image, output_image, faces):
    '''This function draws squares around face/s in a given image,
       and saves a new image that contains the drawing/s.'''

    img = Image.open(input_image)
    d = ImageDraw.Draw(img)

    for i in  range(len(faces)):
        face = faces[i]
        d.line([face[0], face[1], face[2], face[3], face[0]], 'grey', 5)

    if output_image is not None:
        try:
            img.save(output_image, 'JPEG')
        except IOError:
            print('Image was not saved\n')

    return img



#--------------------------------------------------------------------------------------------------#



def crop(input_image, output_image, faces):
    '''This function crops face/s in a given image, and saves
       an image/s that contains just the face/s.'''

    im = Image.open(input_image)
    for i in  range(len(faces)):
        face = faces[i]
        im2 = im.crop([face[0][0], face[0][1], face[2][0], face[2][1]])
        try:
            im2.save(output_image[:len(output_image)-4]+
                     str(i)+output_image[len(output_image)-5:len(output_image)], 'JPEG')
        except IOError:
            print('Image', i+1, 'was not saved')


#--------------------------------------------------------------------------------------------------#
