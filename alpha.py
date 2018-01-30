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
                    [1] All tags related to specific image\n
                    [2] All images related to specific tag\n
                    [3] Number of all stored images\n
                    [4] List of all stored images\n'''


provide_image = 'Please enter full image name\n'

provide_tag = 'Please enter tag name\n'




labels = False  #Determine whether labels detection was used for the last session or not.
faces = False #Determine whether faces detection was used for the last session or not.

command = ['tagging.py']


#Check if the elasticsearch client is connected.
if not storage.check_connection():
    print('\nError! Elasticsearch cluster is not up.\n')
    sys.exit(0)



print('\nPictures Tagging And Storing - Alpha Version')
print('---------------------------------------------')

print('\nPress Q at the main menu to quit\n')


while True:

    user_input = input(main_menu)


    if user_input == '1':
        user_input = input(tagging_menu)

        if user_input == '1':
            labels = True
            command.append('labels')
            user_input = input(tagging_menu_2)

        elif user_input == '2':
            command.append('landmarks')
            user_input = input(tagging_menu_2)

        elif user_input == '3':
            command.append('logos')
            user_input = input(tagging_menu_2)

        elif user_input == '4':
            command.append('web')
            user_input = input(tagging_menu_2)

        elif user_input == '5':
            faces = True
            command.append('faces')
            user_input = input(tagging_menu_2)

        elif user_input == '6':
            command.append('text')
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

        # For now, there is an option to save only labels data.
        if labels == True and results[2] == True:
            user_input = input(save_results)

            if user_input == '1':
                print('\nSaving...\n')
                b = storage.store_labels_data(results[0], filename)
                if b is True:
                    print('\nResults saved for ', filename, ' successfully.\n')
                else:
                    print('\nResults were not saved!\nImage already exists in storage.\n')

            elif user_input == '2':
                print('\nResults were not saved!\n')

            else:
                print('Error!\n')
                sys.exit(0)


        if faces == True and results[2] == True:
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
            storage.get_labels_data(user_input)

        elif user_input == '2':
            user_input = input(provide_tag)
            storage.get_images_by_tag(user_input)

        elif user_input == '3':
            storage.get_num_of_documents('labels_data')

        elif user_input == '4':
            storage.get_all_documents('labels_data')

        else:
            print('Error!\n')
            sys.exit(0)



    elif user_input == '3':
        user_input = input(provide_image)
        storage.delete_labels_data(user_input)


    elif user_input == 'q':
        print('\nGoodbye\n')
        break

    else:
        print('Error!\n')
        sys.exit(0)


    labels = False
    faces = False
    command = ['tagging.py']


