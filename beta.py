import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import beta_tag_window
import beta_storage_window
import beta_search_images
import beta_search_content


def Tag(root_win):
    for i in root_win.winfo_children():
        if i.winfo_class() != 'Menu':
            i.destroy()
            
    global tag_window
    tag_window = beta_tag_window.TagWindow(root)




root = tk.Tk()

root.state('zoomed') #Open in fullscreen.


menu_bar = tk.Menu(root)

options_menu = tk.Menu(menu_bar, tearoff=0, bg='white')
options_menu.add_command(label='Tag', command=lambda: Tag(root))
options_menu.add_command(label='Edit Storage', command=lambda: storage(root))
#options_menu.add_command(label='Search')

menu_bar.add_cascade(label='Options', menu=options_menu)

search_menu = tk.Menu(options_menu, tearoff=0, bg='white')
search_menu.add_command(label='Content by image', command=lambda: search_content(root))
search_menu.add_command(label='Images by content', command=lambda: search_images(root))

options_menu.add_cascade(label='Search', menu=search_menu)





search_images_window = ''

search_content_window = ''

storage_window = ''

tag_window = beta_tag_window.TagWindow(root)

root.config(menu=menu_bar)
root.mainloop()
