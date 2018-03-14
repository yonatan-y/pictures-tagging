'''This module represents the alpha version - an interactive teminal
menu for pictures tagging and storing, providing number of search options.'''

import sys
import os
import tagging
import storage
import image_options


main_menu = '''\nMain menu - Choose an option:\n
                [1] Tag an image\n
                [2] Get data from storage\n
                [3] Delete data from storage\n'''


tagging_menu = '''\nChoose a tagging option:\n
                    [1] Labels detection\n
                    [2] Landmarks detection\n
                    [3] Logos detection\n
                    [4] Web detection\n
                    [5] Faces detection\n
                    [6] Text detection\n'''


tagging_menu_2 = '''\nChoose a way to provide the wanted image:\n
                    [1] From local memory\n
                    [2] From web\n'''


provide_path = '''Please write the full path of the image: '''

provide_url = '''Please write the URL address of the image: '''

save_results = '''Do you want to save results in storage?\n
                  [1] Yes\n
                  [2] No\n'''


faces_menu = '''Faces were found in the image.\nWhat operation would you like to do?\n
                [1] Drawing\n
                [2] Cropping\n
                [3] Both drawing and cropping\n
                [4] Neither drawing nor cropping\n'''


get_info_menu = '''\nWhat would you like to get from storage?\n
                    [1] All data related to specific image\n
                    [2] All images related to specific word/s\n
                    [3] Number of all stored images\n
                    [4] List of all stored images\n'''


provide_image = 'Please enter full image name\n'

provide_tag = 'Please enter word/s\n'


#Determine what was the detection type for the last session.
detections = {
    'labels':False, 'landmarks':False, 'logos':False,
    'web':False, 'faces':False, 'text':False
    }

last_detection = ''


command = ['tagging.py']


#Check if the elasticsearch client is connected.
if not storage.check_connection():
    print('\nError! Elasticsearch cluster is not up.\n')
    sys.exit(0)



print('\nPictures Tagging And Storing - Alpha Version Fix')
print('---------------------------------------------')

print('\nPress Q at the main menu to quit\n')


while True:

    user_input = input(main_menu)


    if user_input == '1':
        user_input = input(tagging_menu)

        if user_input == '1':
            detections['labels'] = True
            command.append('labels')
            last_detection = 'labels'
            user_input = input(tagging_menu_2)

        elif user_input == '2':
            detections['landmarks'] = True
            command.append('landmarks')
            last_detection = 'landmarks'
            user_input = input(tagging_menu_2)

        elif user_input == '3':
            detections['logos'] = True
            command.append('logos')
            last_detection = 'logos'
            user_input = input(tagging_menu_2)

        elif user_input == '4':
            detections['web'] = True
            command.append('web')
            last_detection = 'web'
            user_input = input(tagging_menu_2)

        elif user_input == '5':
            detections['faces'] = True
            command.append('faces')
            last_detection = 'faces'
            user_input = input(tagging_menu_2)

        elif user_input == '6':
            detections['text'] = True
            command.append('text')
            last_detection = 'text'
            user_input = input(tagging_menu_2)

        else:
            print('Error!\n')
            sys.exit(0)




        if user_input == '1':
            command.append('content')
            user_input = input(provide_path)

        elif user_input == '2':
            command.append('source')
            user_input = input(provide_url)

        else:
            print('Error!\n')
            sys.exit(0)



        command.append(user_input)


        print('Please wait...\n')


        results = tagging.make_request(command)

        path, filename = os.path.split(results[1])

        # Now there is an option to save any data.
        if results[2] is True:
            user_input = input(save_results)

            if user_input == '1':
                print('\nSaving...\n')
                b = storage.store_data(last_detection, results[0], filename)
                if b is True:
                    print('\nResults saved for ', filename, ' successfully.\n')
                else:
                    print('\nResults were not saved!\nImage already exists in storage.\n')

            elif user_input == '2':
                print('\nResults were not saved!\n')

            else:
                print('Error!\n')
                sys.exit(0)


        if detections['faces'] is True and results[2] is True:
            name, extention = os.path.splitext(results[1])

            user_input = input(faces_menu)

            if user_input == '1':
                image_options.draw(results[1], name + '(after_drawing).jpg', results[3])
            elif user_input == '2':
                image_options.crop(results[1], name + '(after_cropping).jpg', results[3])
            elif user_input == '3':
                image_options.draw(results[1], name + '(after_drawing).jpg', results[3])
                image_options.crop(results[1], name + '(after_cropping).jpg', results[3])
            elif user_input == '4':
                continue
            else:
                print('Error!\n')
                sys.exit(0)






    elif user_input == '2':
        user_input = input(get_info_menu)

        if user_input == '1':
            user_input = input(provide_image)
            for i in detections:
                storage.get_data(i, user_input)

        elif user_input == '2':
            user_input = input(provide_tag)
            storage.get_images_by_words(user_input)


        elif user_input == '3':
            for i in detections:
                storage.get_num_of_documents(i)

        elif user_input == '4':
            for i in detections:
                storage.get_all_documents(i)

        else:
            print('Error!\n')
            sys.exit(0)



    elif user_input == '3':
        user_input = input(provide_image)
        for i in detections:
            storage.delete_data(i, user_input)


    elif user_input == 'q':
        print('\nGoodbye\n')
        break

    else:
        print('Error!\n')
        sys.exit(0)


    for i in detections:
        detections[i] = False
    last_detection = ''
    command = ['tagging.py']

