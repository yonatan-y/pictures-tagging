import tkinter as tk
import storage

class SearchContentWindow:

    results_frames = {'name':[], 'found':[], 'button':[]}
    results_data = []


    # Start constructor-----------------------------------------------------------------------
    def __init__(self, root):

        self.width, self.height = root.winfo_screenwidth(), root.winfo_screenheight()

        self.search_frame = tk.Frame(
            root,
            highlightbackground='black',
            highlightthickness=2,
            width=self.width,
            height=self.height/3,
            bg='AntiqueWhite3'
        )
        self.search_frame.place(x=0, y=0)
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
        self.options_frame.grid(column=0, pady=10, padx=self.width/9)
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
