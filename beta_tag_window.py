import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import json
from PIL import Image, ImageTk
import tagging
import storage


class TagWindow:

    # This dictionary represents the needed parameters to store data.
    data_to_store = {'index':None, 'json_package':None, 'image_id':None}

    # Start def------------------------------------------------------------------------------
    def open_image(self, frame, btn):
        '''This method is called when the user wants to open an image.
           The image will be displayed on the screen after choosing.'''

        temp = self.selected_image
        self.selected_image = filedialog.askopenfilename(
            title='Select image',
            filetypes=[('jpeg files', '*.jpg'),
                       ('png files', '*.png')
                      ]
        )

        # If the user did not select any image.
        if self.selected_image == "":
            self.selected_image = temp
            return

        # Open selected image and change its size if needed.
        im = Image.open(self.selected_image)
        width, height = im.size

        if width > self.width/2-10:
            width = self.width/2-10

        if height > self.height/6*5-40:
            height = self.height/6*5-40

        im = im.resize((int(width), int(height)))
        photo = ImageTk.PhotoImage(im)


        # Delete previous label which has image.
        for i in frame.winfo_children():
            if i.winfo_class() == 'Label':
                i.destroy()

        # Create new label with the selected image.
        label = tk.Label(
            frame,
            bg='gray80',
            image=photo,
            width=self.width/2,
            height=self.height/6*5-40
        )
        label.pack()
        label.photo = photo

        # Enable 'Process image' button.
        btn.config(state=tk.NORMAL)

        # Delete previous results.
        self.results.config(state=tk.NORMAL)
        self.results.delete('1.0', tk.END)
        self.results.config(state=tk.DISABLED)

        # Disable 'Store results' button.
        self.save_btn.config(state=tk.DISABLED)

        path, filename = os.path.split(self.selected_image)
        print('full name:', self.selected_image)
        print('id: ', filename)
        print('path: ', path)
    # End def---------------------------------------------------------------------------------



    # Start def-------------------------------------------------------------------------------
    def on_click_process_btn(self, results, variable, btn):
        '''This method is called when the user clicks on 'Process image' button.
           It uses the module 'tagging' to process the image, and displays the
           results on the screen.'''

        # Get detection type for process.
        if variable.get() == 1:
            detect = 'labels'
        elif variable.get() == 2:
            detect = 'landmarks'
        elif variable.get() == 3:
            detect = 'logos'
        elif variable.get() == 4:
            detect = 'web'
        elif variable.get() == 5:
            detect = 'faces'
        elif variable.get() == 6:
            detect = 'text'

        # Process image.
        res = tagging.make_request(['tagging.py', detect, 'content', self.selected_image])

        # Display processing results.
        results.config(state=tk.NORMAL)
        results.delete('1.0', tk.END)
        results.insert(tk.END, 'Image id: '+os.path.split(res[1])[1]+'\n')
        results.insert(
            tk.END,
            '------------------------------------------------------------------\n\n'
        )
        results.insert(tk.END, res[0])
        results.config(state=tk.DISABLED)

        # If there was not a problem while processing and the results are
        # good to be saved, update parameters and enable 'Store results' button.
        if res[2] is True:
            TagWindow.data_to_store['index'] = detect

            # Add Image path to json results.
            res[0] = json.loads(res[0])
            res[0]['Image path'] = os.path.split(res[1])[0]
            res[0] = json.dumps(res[0], indent=4)

            TagWindow.data_to_store['json_package'] = res[0]
            TagWindow.data_to_store['image_id'] = os.path.split(res[1])[1]

            messagebox.showinfo(os.path.split(res[1])[1]+', '+detect, res[0])


            btn.config(state=tk.NORMAL)

        else:
            # Clear parameters and disable button.
            for i in list(TagWindow.data_to_store.keys()):
                TagWindow.data_to_store[i] = None

            btn.config(state=tk.DISABLED)

    # End def---------------------------------------------------------------------------------




    # Start def-------------------------------------------------------------------------------
    def save_results(self, btn):
        '''This method is called when the user wants to save the results after
           the image proccesing (clicks on 'Store results' button).'''

        # Store the results.
        storage.store_data(
            TagWindow.data_to_store['index'],
            TagWindow.data_to_store['json_package'],
            TagWindow.data_to_store['image_id']
        )

        # Clear parameters and disable button.
        for i in list(TagWindow.data_to_store.keys()):
            TagWindow.data_to_store[i] = None

        btn.config(state=tk.DISABLED)
        return

    # End def---------------------------------------------------------------------------------


    # Start def-------------------------------------------------------------------------------
    def enter(self, btn):
        '''Change button's color when mouse enter.'''
        if btn['state'] == 'normal':
            btn.config(bg='white')
    # End def---------------------------------------------------------------------------------


    # Start def-------------------------------------------------------------------------------
    def leave(self, btn):
        '''Change button's color when mouse leave.'''
        if btn['state'] == 'normal':
            btn.config(bg='gray94')
    # End def---------------------------------------------------------------------------------



    # Start constructor-----------------------------------------------------------------------
    def __init__(self, root):

        self.selected_image = ''
        self.width, self.height = root.winfo_screenwidth(), root.winfo_screenheight()


        self.image_frame = tk.Frame(
            root,
            bg='gray80',
            width=self.width/2,
            height=self.height/6*5
        )
        self.image_frame.place(x=10, y=15)
        self.image_frame.pack_propagate(False)


        self.text_frame = tk.Frame(
            root,
            bg='white',
            width=self.width/3,
            height=self.height/6*5
        )
        self.text_frame.place(x=2*self.width/3-30, y=15)
        self.text_frame.pack_propagate(False)


        self.results = tk.Text(
            self.text_frame,
            wrap=tk.NONE,
            font=('Helvetica', 14)
        )


        self.detections_frame = tk.LabelFrame(
            root,
            text='Select detection type',
            font=('TkDefaultFont', 11)
        )
        self.detections_frame.place(x=self.width/2+28, y=self.height/4)


        self.detection_types = [
            ('Labels', 1),
            ('Landmarks', 2),
            ('Logos', 3),
            ('Web', 4),
            ('Faces', 5),
            ('Text', 6)
        ]

        self.variable = tk.IntVar(root) # Value holder for detection type
        self.variable.set(1) # Default value
        self.rbs = list() # List of radio buttons

        for text, mode in self.detection_types:
            self.rbs.append(tk.Radiobutton(
                self.detections_frame,
                text=text,
                variable=self.variable,
                value=mode,
                font=('TkDefaultFont', 10)
            ))
            self.rbs[mode-1].pack(anchor=tk.W)
            self.rbs[mode-1].bind(
                '<Enter>',
                lambda event, r=self.rbs[mode-1]: r.config(font=('TkDefaultFont', 10, 'bold'))
            )
            self.rbs[mode-1].bind(
                '<Leave>',
                lambda event, r=self.rbs[mode-1]: r.config(font=('TkDefaultFont', 10))
            )

        # Update the frame to change its size and do not let
        # its children affect its size.
        self.detections_frame.update()
        self.detections_frame.config(
            width=int(self.detections_frame.winfo_width()),
            height=int(self.detections_frame.winfo_height())+10
        )
        self.detections_frame.pack_propagate(False)


        self.save_btn = tk.Button(
            self.text_frame,
            text='Store results',
            font=10,
            state=tk.DISABLED
        )
        self.save_btn.config(command=lambda: self.save_results(self.save_btn))
        self.save_btn.bind('<Enter>', lambda event: self.enter(self.save_btn))
        self.save_btn.bind('<Leave>', lambda event: self.leave(self.save_btn))


        self.process_btn = tk.Button(
            root,
            text='Process image',
            fg='green',
            bd=0,
            state=tk.DISABLED,
            font=('TkDefaultFont', 14, 'italic'),
            command=lambda: self.on_click_process_btn(self.results, self.variable, self.save_btn)
        )

        self.select_btn = tk.Button(
            self.image_frame,
            text='Select image',
            font=10,
            command=lambda: self.open_image(self.image_frame, self.process_btn)
        )

        self.select_btn.pack(side='bottom', fill='x')
        self.select_btn.bind('<Enter>', lambda event: self.enter(self.select_btn))
        self.select_btn.bind('<Leave>', lambda event: self.leave(self.select_btn))


        self.process_btn.place(x=self.width/2+28, y=self.height/2)
        self.process_btn.bind('<Enter>', lambda event: self.enter(self.process_btn))
        self.process_btn.bind('<Leave>', lambda event: self.leave(self.process_btn))


        self.save_btn.pack(side='bottom', fill=tk.X)

        self.scroll_y = tk.Scrollbar(
            self.text_frame,
            command=self.results.yview
        )
        self.scroll_y.pack(side='right', fill=tk.Y)

        self.scroll_x = tk.Scrollbar(
            self.text_frame,
            command=self.results.xview,
            orient=tk.HORIZONTAL
        )
        self.scroll_x.pack(side='bottom', fill=tk.X)

        self.results.pack(expand=True, fill='both')
        self.results['yscrollcommand'] = self.scroll_y.set
        self.results['xscrollcommand'] = self.scroll_x.set


        self.results.config(state=tk.DISABLED)
    # End constructor-------------------------------------------------------------------------
        
