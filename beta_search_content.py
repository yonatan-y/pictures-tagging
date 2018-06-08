import tkinter as tk
import storage

class SearchContentWindow:
    '''This class represents an object that creates a page for searching
       images metadata in storage.
       The object constructs all widgets ant implements functionality.'''

    results_frames = {'name':[], 'found':[], 'button':[]}
    results_data = []

    # Start def-------------------------------------------------------------------------------
    def add_results_frames(self, options, root):
        '''This method adds the needed frames to the root window.
           Each selected checkbutton creates a new frame.'''

        # Remove old frames if necessary
        for i in options[:6]:
            if i[3] != None:
                i[3].destroy()
                i[3] = None

        SearchContentWindow.results_frames = {'name':[], 'found':[], 'button':[]}
        SearchContentWindow.results_data = []

        temp_y = self.height/3+5

        # If the user selected 'All', select all checkbuttons.
        if options[6][1].get() == 1:
            for i in options[:6]:
                i[1].set(1)

        # For each selected checkbutton create a new frame.
        for i in options[:6]:
            if i[1].get() == 1:
                i[3] = tk.Frame(
                    root,
                    highlightbackground='black',
                    highlightthickness=1,
                    width=self.width,
                    height=self.height/12
                )
                i[3].place(x=0, y=temp_y)
                i[3].pack_propagate(False)

                temp_y = temp_y+self.height/12+5

                # Add frame's name same as the selected checkbutton.
                SearchContentWindow.results_frames['name'].append(tk.Label(
                    i[3],
                    text=i[0]+' : ',
                    font=('Helvetica', 14, 'bold')
                ))

                SearchContentWindow.results_frames['name'][-1].place(x=40, y=15)
    # End def---------------------------------------------------------------------------------


    # Start def-------------------------------------------------------------------------------
    def select_all(self, options, root):
        '''This method selects all checkbuttons and adds all frames.'''

        for i in options:
            if i[0] != 'All':
                i[2].deselect()
        self.add_results_frames(options, root)
    # End def---------------------------------------------------------------------------------


    # Start def-------------------------------------------------------------------------------
    def select_some(self, options, root):
        '''This method selects the wanted checkbuttons and adds their frames.'''

        options[6][2].deselect()
        self.add_results_frames(options, root)
    # End def---------------------------------------------------------------------------------


    # Start def-------------------------------------------------------------------------------
    def focus_in_entry(self, entry):
        '''Clear the search line placeholder when it gets focus.'''
        entry.delete(0, 'end')
        entry.config(fg='black')
    # End def---------------------------------------------------------------------------------


    # Start def-------------------------------------------------------------------------------
    def on_click_search(self, root, entry, options):
        '''This method is being called when the use click on search button.
           The method searchs the entry text (image id) in the selected
           indices and displays the results inside the frames.'''

        # Clear all old frames.
        self.add_results_frames(options, root)

        for i in options[:6]:
            if i[1].get() == 1:
                SearchContentWindow.results_frames['found'].append(tk.Label(
                    i[3]
                ))
                SearchContentWindow.results_frames['found'][-1].place(
                    x=self.width/2-40,
                    y=15
                )

                res = storage.get_data(i[0].lower(), entry.get())
                if res is False:
                    SearchContentWindow.results_frames['found'][-1].config(
                        fg='grey',
                        text='Not found',
                        font=('Helvetica, 16')
                    )
                else:
                    SearchContentWindow.results_data.append(res)
                    SearchContentWindow.results_frames['found'][-1].config(
                        fg='DarkOliveGreen4',
                        text='Found',
                        font=('Helvetica', 16, 'bold')
                    )

                    SearchContentWindow.results_frames['button'].append(tk.Button(
                        i[3],
                        bg='white',
                        bd=1,
                        text='See content',
                        font=('Helvetica', 11),
                        command=lambda data=res: self.show_data(root, data)
                    ))
                    SearchContentWindow.results_frames['button'][-1].place(
                        x=self.width/7*6,
                        y=15
                    )

                    res_btn = SearchContentWindow.results_frames['button'][-1]
                    res_btn.bind(
                        '<Enter>',
                        lambda event, btn=res_btn: btn.config(bg='gray80', bd=2)
                    )
                    res_btn.bind(
                        '<Leave>',
                        lambda event, btn=res_btn: btn.config(bg='white', bd=1)
                    )
    # End def---------------------------------------------------------------------------------


    # Start def-------------------------------------------------------------------------------
    def show_data(self, root, data):
        '''This method is being called when the user clicks the 'see content'
           button.
           The method opens a new window that contains the data about an image
           from an index in the storage.'''

        data_window = tk.Toplevel(root)
        results = tk.Text(
            data_window,
            wrap=tk.NONE,
            font=('Helvetica', 14)
        )

        scroll_y = tk.Scrollbar(data_window, command=results.yview)
        scroll_y.pack(side='right', fill=tk.Y)

        scroll_x = tk.Scrollbar(data_window, command=results.xview, orient=tk.HORIZONTAL)
        scroll_x.pack(side='bottom', fill=tk.X)

        results.pack(expand=True, fill='both')
        results['yscrollcommand'] = scroll_y.set
        results['xscrollcommand'] = scroll_x.set

        results.insert(tk.END, data)
        results.config(state=tk.DISABLED)
    # End def---------------------------------------------------------------------------------

    def enter_check_btn(self, btn):
        btn.config(font=('TkDefaultFont', 10, 'bold'))

    def leave_check_btn(self, btn):
        btn.config(font=('TkDefaultFont', 10))


    # Start constructor-----------------------------------------------------------------------
    def __init__(self, root):

        self.width, self.height = root.winfo_screenwidth(), root.winfo_screenheight()

        self.search_frame = tk.Frame(
            root,
            highlightbackground='black',
            highlightthickness=0,
            width=self.width-300,
            height=self.height/3,
            bg='AntiqueWhite3'
        )
        self.search_frame.place(x=150, y=0)
        #self.search_frame.pack_propagate(False)
        self.search_frame.grid_propagate(False)

        self.options = [
            ['Labels', tk.IntVar()],
            ['Landmarks', tk.IntVar()],
            ['Logos', tk.IntVar()],
            ['Web', tk.IntVar()],
            ['Faces', tk.IntVar()],
            ['Text', tk.IntVar()],
            ['All', tk.IntVar()]
        ]

        self.options_frame = tk.LabelFrame(
            self.search_frame,
            text='Search in:',
            font=('TkDefaultFont', 11),
            bg='AntiqueWhite3',
            width=125,
            height=215
        )
        self.options_frame.grid(column=0, pady=10, padx=self.width/12)
        self.options_frame.pack_propagate(False)

        for i in self.options:
            i.append(tk.Checkbutton(
                self.options_frame,
                text=i[0],
                font=('TkDefaultFont', 10),
                variable=i[1],
                bg='AntiqueWhite3',
                activebackground='AntiqueWhite3'
            ))
            i[2].pack(anchor=tk.W)
            checkbtn = i[2]
            i[2].bind(
                '<Enter>',
                lambda event, btn=checkbtn: btn.config(font=('TkDefaultFont', 10, 'bold'))
            )
            i[2].bind(
                '<Leave>',
                lambda event, btn=checkbtn: btn.config(font=('TkDefaultFont', 10))
            )

            i.append(None)


        for i in self.options:
            if i[0] != 'All':
                i[2].config(command=lambda: self.select_some(self.options, root))
            else:
                i[2].config(command=lambda: self.select_all(self.options, root))

        self.search = {
            'entry': tk.Entry(self.search_frame, width=40, font=('Helvetica', 16)),
            'button': tk.Button(
                self.search_frame,
                text='Search',
                font=13,
                bg='gray98',
                activebackground='AntiqueWhite4',
                activeforeground='white')
        }
        self.search['entry'].insert(0, 'Example: Image.jpg')
        self.search['entry'].config(fg='gray79')
        self.search['entry'].bind(
            '<FocusIn>',
            lambda event: self.focus_in_entry(self.search['entry'])
        )

        self.search['entry'].bind(
            '<Return>',
            lambda event: self.on_click_search(root, self.search['entry'], self.options)
        )

        self.search['button'].config(
            command=lambda: self.on_click_search(root, self.search['entry'], self.options)
        )

        self.search['button'].bind(
            '<Enter>',
            lambda event: self.search['button'].config(bg='AntiqueWhite4', fg='white')
        )

        self.search['button'].bind(
            '<Leave>',
            lambda event: self.search['button'].config(bg='gray98', fg='black')
        )

        self.search['entry'].grid(row=0, column=3, pady=5)
        self.search['button'].grid(row=0, column=5, pady=5, padx=15)
    # End Constructor-------------------------------------------------------------------------
