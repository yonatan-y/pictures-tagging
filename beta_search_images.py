import tkinter as tk
from PIL import Image, ImageTk
import storage



class SearchImagesWindow:
    '''This class represents an object that creates a page for searching
       images by keywords.
       It actually simulate a search engine for the images.
       The object constructs all widgets ant implements functionality.'''

    # Start def-------------------------------------------------------------------------------
    def clear(self):
        '''Clear all old images if there is a need, and reset variables.'''

        self.res = []
        if self.errors['button'] is not None:
            self.errors['button'].destroy()
            self.errors['button'] = None
        self.errors['list'] = []
        self.viewed = 0
        self.left, self.top, self.left_count = 0, 0, 0

        self.show_more_frame = None

        for i in self.canvas.winfo_children():
            i.destroy()

    # End def---------------------------------------------------------------------------------


    # Start def-------------------------------------------------------------------------------
    def search(self):
        '''This method reads input text of the user and displays on the screen all results
           from storage, i.e. all images with metadata that match to the input text.'''

        # Delete results of previous search if there is a need.
        self.clear()

        # Scroll back to the top of the window if there is a need.
        self.canvas.update()
        self.canvas.config(scrollregion=(0, 0, 0, 0))

        # Search and display results.
        self.show_results()

    # End def---------------------------------------------------------------------------------



    # Start def-------------------------------------------------------------------------------
    def add_button(self):
        '''This method displays a button that enables to load
           more images that match to the search.'''

        self.show_more_frame = tk.Frame(
            self.canvas,
            width=self.canvas.winfo_width()/4,
            height=self.height/5,
        )
        self.show_more_frame.pack_propagate(False)

        self.show_more_btn = tk.Button(
            self.show_more_frame,
            text='Show\nmore',
            font=('Helvetica', 16),
            bg='gray85',
            bd=0,
            command=lambda: self.show_results()
        )
        self.show_more_btn.pack(expand=True, fill='both')

        # Change button's color when mouse enter.
        self.show_more_btn.bind(
            '<Enter>',
            lambda event: self.show_more_btn.config(bg='gray91')
        )

        # Change back button's color when mouse leave.
        self.show_more_btn.bind(
            '<Leave>',
            lambda event: self.show_more_btn.config(bg='gray85')
        )

        self.canvas.create_window(self.left, self.top, window=self.show_more_frame, anchor='nw')

        self.canvas.config(scrollregion=self.canvas.bbox('all'))
    # End def---------------------------------------------------------------------------------





    # Start def-------------------------------------------------------------------------------
    def show_results(self):
        '''This method gets results from storage and displays results on the screen.'''

        # Get results from storage.
        self.res = storage.get_images_by_words(self.search_text.get(), start=self.viewed)

        # Delete button that enables to load more images.
        if self.show_more_frame is not None:
            self.show_more_frame.destroy()
            self.show_more_frame = None

        # Display results.
        for i in self.res[0]:
            self.viewed += 1
            try:
                im = Image.open(i)
            # If there was a problem to open the image
            except IOError:
                self.errors['list'].append(i)
                if self.errors['button'] is None:
                    self.errors['button'] = tk.Button(
                        self.search_frame,
                        text='Errors: ',
                        bd=0,
                        fg='red',
                        activeforeground='red',
                        font=('TkDefaultFont', 13, 'bold'),
                        command=lambda: self.show_errors()
                    )
                    self.errors['button'].pack(side='bottom')
                    self.errors['button'].bind(
                        '<Enter>',
                        lambda evenet: self.errors['button'].config(bd=1)
                    )
                    self.errors['button'].bind(
                        '<Leave>',
                        lambda evenet: self.errors['button'].config(bd=0)
                    )
                self.errors['button'].config(text='Errors: '+(str(len(self.errors['list']))))
                continue

            im = im.resize((int(self.canvas.winfo_width()/4), int(self.height/5)))
            photo = ImageTk.PhotoImage(im)


            frame = tk.Frame(
                self.canvas,
                width=self.canvas.winfo_width()/4,
                height=self.height/5
            )


            self.canvas.create_window(self.left, self.top, window=frame, anchor='nw')
            self.canvas.config(scrollregion=self.canvas.bbox('all'))

            # Update position variables.
            self.left = self.left + self.canvas.winfo_width()/4
            self.left_count = self.left_count + 1
            if self.left_count == 4:
                self.top = self.top + self.height/5
                self.left = 0
                self.left_count = 0


            label = tk.Label(
                frame,
                image=photo,
                width=self.canvas.winfo_width()/4,
                height=self.height/5
            )
            label.photo = photo

            label.pack()

            label.bind(
                '<Double-Button-1>',
                lambda event, path=i: self.full_size_image(path)
            )

        self.canvas.config(scrollregion=self.canvas.bbox('all'))

        # If there are more results that are not displayed yet.
        if self.res[1] > self.viewed:
            self.add_button()

    # End def---------------------------------------------------------------------------------



    # Start def-------------------------------------------------------------------------------
    def full_size_image(self, path):
        '''This method opens a new window and displays the image with original size.'''

        image_window = tk.Toplevel(self.root) # New window
        image_window.state('zoomed') # Full screen
        image_window.title(path)

        img = ImageTk.PhotoImage(Image.open(path))
        panel = tk.Label(image_window, image=img)
        panel.photo = img

        panel.pack(fill='both', expand=True)

    # End def---------------------------------------------------------------------------------




    # Start def-------------------------------------------------------------------------------
    def show_errors(self):
        '''This method is called when the user presses the 'Errors' button.
           The method opens a new window with a list of all images that could not
           be open at the given search.'''

        data_window = tk.Toplevel(self.root)

        results = tk.Text(
            data_window,
            wrap=tk.NONE,
            font=('Helvetica', 12)
        )
        scroll_y = tk.Scrollbar(data_window, command=results.yview)
        scroll_y.pack(side='right', fill=tk.Y)

        scroll_x = tk.Scrollbar(data_window, command=results.xview, orient=tk.HORIZONTAL)
        scroll_x.pack(side='bottom', fill=tk.X)

        results.pack(expand=True, fill='both')
        results['yscrollcommand'] = scroll_y.set
        results['xscrollcommand'] = scroll_x.set


        results.insert(tk.END, 'Cannot open the following images:\n\n')

        for i in self.errors['list']:
            results.insert(tk.END, i+'\n')

        results.config(state=tk.DISABLED)

    # End def---------------------------------------------------------------------------------




    # Start constructor-----------------------------------------------------------------------
    def __init__(self, root):

        self.root = root

        self.width, self.height = root.winfo_screenwidth(), root.winfo_screenheight()

        self.res = [] # Search results
        self.viewed = 0 # How many images are open
        self.errors = {'button':None, 'list':[]}
        self.left, self.top, self.left_count = 0, 0, 0 # Counters for images position
        self.show_more_frame = None
        self.show_more_btn = None

        self.search_frame = tk.Frame(
            root,
            width=self.width/3*2,
            height=self.height/6
        )
        self.search_frame.pack()
        self.search_frame.pack_propagate(False)

        self.search_text = tk.Entry(self.search_frame, width=40, font=('Helvetica', 16))
        #self.search_text.pack(side='left', padx=50)

        # Enable search when the user presses on enter key.
        self.search_text.bind(
            '<Return>',
            lambda event: self.search()
        )

        self.search_btn = tk.Button(
            self.search_frame,
            text='Search',
            bg='gray94',
            font=13,
            command=lambda: self.search()
        )

        self.search_btn.bind(
            '<Enter>',
            lambda event: self.search_btn.config(bg='white')
        )

        self.search_btn.bind(
            '<Leave>',
            lambda event: self.search_btn.config(bg='gray94')
        )

        self.search_btn.pack(side='right', padx=70)
        self.search_text.pack(side='right')


        self.results_frame = tk.Frame(
            root,
            width=self.width,
            height=self.height/6*4
        )
        self.results_frame.pack(side='bottom', expand=True, fill='both')


        self.canvas = tk.Canvas(
            self.results_frame,
            borderwidth=0,
            highlightthickness=0,
            background="#ffffff"
            #width=self.width,
            #height=self.height/6*4
        )

        self.vsb = tk.Scrollbar(
            self.results_frame,
            orient="vertical",
            command=self.canvas.yview
        )

        self.vsb.pack(side="right", fill="y")

        self.canvas.pack(side='left', fill='both', expand=True)

        self.canvas.configure(yscrollcommand=self.vsb.set)


        self.canvas.config(scrollregion=self.canvas.bbox('all'))
    # End Constructor-------------------------------------------------------------------------
