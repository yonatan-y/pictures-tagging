import tkinter as tk
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
        for i in selected_items:
            storage.delete_data(name, labelslist.get(i))
            #print(labelslist.get(i))
            labelslist.delete(i)




    # End def---------------------------------------------------------------------------------



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
                highlightbackground='black',
                highlightthickness=2,
                width=self.width/8,
                height=self.height/2
            ))
            self.frames[i].place(x=10+(self.width/8*i)+(10*i), y=20)
            self.frames[i].pack_propagate(False) # Do not let its children control its size

            self.names.append(tk.Label(
                self.frames[i],
                text=names[i]
            ))
            self.names[i].pack()


            self.labelslists.append(tk.Listbox(
                self.frames[i],
                selectmode='multiple'
            ))
            self.labelslists[i].pack(expand=True, fill='both')
            self.labelslists[i].pack_propagate(False)
            '''for item in ['one', 'two', 'three', 'four',
                         'one', 'two', 'three', 'four',
                         'one', 'two', 'three', 'four']:
                self.labelslists[i].insert(tk.END, item)'''




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
            ))
            self.load_buttons[i].pack()
            



            self.delete_buttons.append(tk.Button(
                self.frames[i],
                text='Delete selected images',
                fg='red'
            ))
            self.delete_buttons[i].pack(side='bottom')
            
            


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

        

