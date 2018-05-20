import tkinter as tk
from tkinter import messagebox
import storage



class StorageWindow:


    # Start def-------------------------------------------------------------------------------
    def load_images(self, labelslist, name):
        '''This method is called when the user presses the button 'Load more items'.
           The method gets more items from the index 'name' in the storage,
           and displays the items in the screen.'''

        # Get more items, start from position 'size'.
        size = labelslist.size()
        res = storage.get_all_documents(name, start=size)

        # Display the items (if there are).
        if res != None:
            for i in res:
                labelslist.insert(tk.END, i)

    # End def---------------------------------------------------------------------------------





    # Start def------------------------------------------------------------------------------
    def delete_images(self, labelslist, name):
        '''This method is called when the user presses the button 'Delete selected items'.
           The method deletes the marked items from storage and then from the screen.'''

        selected_items = labelslist.curselection()
        selected_items = list(selected_items)
        selected_items.reverse()
        #print(type(selected_items))
        #print(selected_items)

        # If no items were selected, do nothing.
        length = len(selected_items)
        if length == 0:
            return

        if messagebox.askyesno('', 'Are you sure you want to delete the selected items?') is True:
            for i in selected_items:
                storage.delete_data(name, labelslist.get(i))
                #print(labelslist.get(i))
                labelslist.delete(i)


    # End def---------------------------------------------------------------------------------


    # Start constructor-----------------------------------------------------------------------
    def __init__(self, root):

        self.frames = []
        self.names = []
        self.labelslists = []
        self.load_buttons = []
        self.delete_buttons = []
        self.y_scrolls = []
        self.x_scrolls = []

        self.width, self.height = root.winfo_screenwidth(), root.winfo_screenheight()

        names = ['Labels', 'Landmarks', 'Logos', 'Web', 'Faces', 'Text']

        for i in list(range(6)):
            self.frames.append(tk.Frame(
                root,
                width=self.width/7,
                height=self.height/3*2
            ))
            self.frames[i].place(x=self.width/49+(self.width/7*i)+(self.width/49*i), y=self.height/8)
            self.frames[i].pack_propagate(False) # Do not let its children control its size

            self.names.append(tk.Label(
                self.frames[i],
                text=names[i],
                font=('TkDefaultFont', 12, 'bold')
            ))
            self.names[i].pack()


            self.labelslists.append(tk.Listbox(
                self.frames[i],
                selectmode='multiple',
                font=14
            ))
            self.labelslists[i].pack(expand=True, fill='both')
            self.labelslists[i].pack_propagate(False)


            self.y_scrolls.append(tk.Scrollbar(
                self.labelslists[i],
                command=self.labelslists[i].yview
            ))
            self.y_scrolls[i].pack(side='right', fill=tk.Y)
            self.labelslists[i]['yscrollcommand'] = self.y_scrolls[i].set

            self.x_scrolls.append(tk.Scrollbar(
                self.labelslists[i],
                command=self.labelslists[i].xview,
                orient=tk.HORIZONTAL
            ))
            self.x_scrolls[i].pack(side='bottom', fill=tk.X)
            self.labelslists[i]['xscrollcommand'] = self.x_scrolls[i].set




            self.load_buttons.append(tk.Button(
                self.frames[i],
                text='Load more items',
                font=('TkDefaultFont', 10),
                pady=15,
                bd=0
            ))
            self.load_buttons[i].pack(fill='x')
            load_btn = self.load_buttons[i]
            load_btn.bind(
                '<Enter>',
                lambda event, btn=load_btn: btn.config(font=('TkDefaultFont', 10, 'bold'))
            )
            load_btn.bind(
                '<Leave>',
                lambda event, btn=load_btn: btn.config(font=('TkDefaultFont', 10))
            )




            self.delete_buttons.append(tk.Button(
                self.frames[i],
                text='Delete selected items',
                fg='red',
                activeforeground='red',
                font=('TkDefaultFont', 10),
                bd=0
            ))
            self.delete_buttons[i].pack(side='bottom', fill='x')
            dlt_btn = self.delete_buttons[i]
            dlt_btn.bind(
                '<Enter>',
                lambda event, btn=dlt_btn: btn.config(font=('TkDefaultFont', 10, 'bold'))
            )
            dlt_btn.bind(
                '<Leave>',
                lambda event, btn=dlt_btn: btn.config(font=('TkDefaultFont', 10))
            )




            if i == 0:
                self.load_buttons[0].config(
                    command=lambda: self.load_images(self.labelslists[0], 'labels')
                )
                self.delete_buttons[0].config(
                    command=lambda: self.delete_images(self.labelslists[0], 'labels')
                )
            elif i == 1:
                self.load_buttons[1].config(
                    command=lambda: self.load_images(self.labelslists[1], 'landmarks')
                )
                self.delete_buttons[1].config(
                    command=lambda: self.delete_images(self.labelslists[1], 'landmarks')
                )
            elif i == 2:
                self.load_buttons[2].config(
                    command=lambda: self.load_images(self.labelslists[2], 'logos')
                )
                self.delete_buttons[2].config(
                    command=lambda: self.delete_images(self.labelslists[2], 'logos')
                )
            elif i == 3:
                self.load_buttons[3].config(
                    command=lambda: self.load_images(self.labelslists[3], 'web')
                )
                self.delete_buttons[3].config(
                    command=lambda: self.delete_images(self.labelslists[3], 'web')
                )
            elif i == 4:
                self.load_buttons[4].config(
                    command=lambda: self.load_images(self.labelslists[4], 'faces')
                )
                self.delete_buttons[4].config(
                    command=lambda: self.delete_images(self.labelslists[4], 'faces')
                )
            elif i == 5:
                self.load_buttons[5].config(
                    command=lambda: self.load_images(self.labelslists[5], 'text')
                )
                self.delete_buttons[5].config(
                    command=lambda: self.delete_images(self.labelslists[5], 'text')
                )
    # End constructor-------------------------------------------------------------------------

