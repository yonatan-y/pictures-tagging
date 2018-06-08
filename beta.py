import tkinter as tk
from tkinter import filedialog
import beta_tag_window
import beta_storage_window
import beta_search_images
import beta_search_content



class Beta:
    '''This class represents an object which is the main window in beta version.
       An instance of this class will open the main window with all widgets and
       functionality.
       The main window contains main menu and it is responsible for constructing
       or removing the other objects it imports.'''

    # Start def-------------------------------------------------------------------------------
    def tag(self):
        '''This method deletes all objects from main window and constructs a new object
           from class TagWindow.'''

        for i in self.root.winfo_children():
            if i.winfo_class() != 'Menu':
                i.destroy()

        self.tag_window = beta_tag_window.TagWindow(self.root)
    # End def---------------------------------------------------------------------------------


    # Start def-------------------------------------------------------------------------------
    def storage(self):
        '''This method deletes all objects from main window and constructs a new object
           from class StorageWindow.'''

        for i in self.root.winfo_children():
            if i.winfo_class() != 'Menu':
                i.destroy()

        self.storage_window = beta_storage_window.StorageWindow(self.root)
    # End def---------------------------------------------------------------------------------


    # Start def-------------------------------------------------------------------------------
    def search_images(self):
        '''This method deletes all objects from main window and constructs a new object
           from class SearchImagesWindow.'''

        for i in self.root.winfo_children():
            if i.winfo_class() != 'Menu':
                i.destroy()

        self.search_images_window = beta_search_images.SearchImagesWindow(self.root)
    # End def---------------------------------------------------------------------------------


    # Start def-------------------------------------------------------------------------------
    def search_content(self):
        '''This method deletes all objects from main window and constructs a new object
           from class SearchContentWindow.'''

        for i in self.root.winfo_children():
            if i.winfo_class() != 'Menu':
                i.destroy()

        self.search_content_window = beta_search_content.SearchContentWindow(self.root)
    # End def---------------------------------------------------------------------------------



    # Start constructor-----------------------------------------------------------------------
    def __init__(self):

        self.root = tk.Tk()
        self.root.state('zoomed') #Open in fullscreen.

        self.menu_bar = tk.Menu(self.root)

        self.options_menu = tk.Menu(self.menu_bar, tearoff=0, bg='white')

        self.options_menu.add_command(
            label='Tag',
            command=lambda: self.tag()
        )

        self.options_menu.add_command(
            label='Edit Storage',
            command=lambda: self.storage()
        )

        self.menu_bar.add_cascade(
            label='Options',
            menu=self.options_menu
        )

        self.search_menu = tk.Menu(self.options_menu, tearoff=0, bg='white')

        self.search_menu.add_command(
            label='Content by image',
            command=lambda: self.search_content()
        )

        self.search_menu.add_command(
            label='Images by content',
            command=lambda: self.search_images()
        )

        self.options_menu.add_cascade(label='Search', menu=self.search_menu)

        self.search_images_window = None
        self.search_content_window = None
        self.storage_window = None
        self.tag_window = beta_tag_window.TagWindow(self.root)

        self.root.config(menu=self.menu_bar)
        self.root.title('Pictures tagging')
        self.root.mainloop()

    # End constructor-------------------------------------------------------------------------



# Create instance to initiate the main window.
beta = Beta()
