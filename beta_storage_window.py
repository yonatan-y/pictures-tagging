import tkinter as tk
from tkinter import messagebox
import storage



class StorageWindow:


    # Start def-------------------------------------------------------------------------------
    def load_images(self, labelslist, name):
        size = labelslist.size()
        res = storage.get_all_documents(name, start=size)
        if res != None:
            for i in res:
                labelslist.insert(tk.END, i)
        #return


    # End def---------------------------------------------------------------------------------





    # Start def------------------------------------------------------------------------------
    def delete_images(self, labelslist, name):
        selected_items = labelslist.curselection()
        selected_items = list(selected_items)
        selected_items.reverse()
        #print(type(selected_items))
        #print(selected_items)
        length = len(selected_items)
        if length == 0:
            return

        if messagebox.askyesno('', 'Are you sure you want to delete the selected items?') is True:
            print('true')
            for i in selected_items:
                storage.delete_data(name, labelslist.get(i))
                #print(labelslist.get(i))
                labelslist.delete(i)




    # End def---------------------------------------------------------------------------------



    def __init__(self, root):
        #root.config(bg='gray87')

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
                text='Load more images',
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
                text='Delete selected images',
                fg='red',
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


