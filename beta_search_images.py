import tkinter as tk
from PIL import Image, ImageTk
import storage



class SearchImagesWindow:


    # Start constructor-----------------------------------------------------------------------
    def __init__(self, root):

        self.root = root

        self.width, self.height = root.winfo_screenwidth(), root.winfo_screenheight()

        self.res = [] #Search results
        self.viewed = 0
        self.errors = {'button':None, 'list':[]}
        self.left, self.top, self.left_count = 0, 0, 0
        self.show_more_frame = None
        self.show_more_btn = None

        self.search_frame = tk.Frame(
            root,
            highlightbackground='black',
            highlightthickness=0,
            width=self.width/3*2,
            height=self.height/6
        )
        #self.search_frame.place(x=0, y=0)
        self.search_frame.pack()
        self.search_frame.pack_propagate(False)

        self.search_text = tk.Entry(self.search_frame, width=40, font=('Helvetica', 16))
        #self.search_text.pack(side='left', padx=50)

        self.search_btn = tk.Button(
            self.search_frame,
            text='Search',
            font=13,
            command=lambda: self.search()
        )
        self.search_btn.pack(side='right', padx=60)
        self.search_text.pack(side='right')


        self.results_frame = tk.Frame(
            root,
            highlightbackground='black',
            highlightthickness=0,
            width=self.width,
            height=self.height/6*4
        )
        #self.results_frame.place(x=0, y=self.height/6)
        self.results_frame.pack(side='bottom', expand=True, fill='both')



        self.canvas = tk.Canvas(
            self.results_frame,
            borderwidth=0,
            highlightthickness=0,
            background="#ffffff"
            #width=self.width,
            #height=self.height/6*4
        )

        #self.canvas.place(x=0, y=self.height/6)

        #self.frame = tk.Frame(self.canvas, background="#ffffff")
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
