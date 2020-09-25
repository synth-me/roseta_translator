import tkinter as tk 
import languages_to_use 
from languages_to_use import language_list, change_path
import shell_interpreter
from shell_interpreter import interpreter
import datetime 

main_window = tk.Tk()
main_window.title('node_shell')

# here we get the dictionary with the routes
# that can be changed by the main shell 
# here we evoke the dictionary which have the routes for the file
# in which all specific nodes are storage  
# here we write the commands 
shell = tk.Text(
    master=main_window,
    background='black',
    fg='lime',
    height=5,   
)

# here we run and check the syntax of the commands so that the system 
# can show us if it is structured rightly 
run_btn = tk.Button(
    master=main_window,
    background='seashell3',
    text='run commands',
    fg='black',
    width=90
)

# here the changes are shown 
console = tk.Text(
    master=main_window,
    background='black',
    fg='lime',
    height='5px'
)
head = 'json node root route: {x}'.format(x='/Users/murie/OneDrive/Área de Trabalho/roseta/nodes.json') 

heading = tk.Label(
    master=main_window,
    text=head,
    bg='black',
    fg='lime',
    width=91
)

path_entry = tk.Entry(
    master=main_window,
    bg='black',
    fg='lime',
    width=107
)

# if everything is alright with the syntax we can add the commands 
# to the main structure 
def show_main():
    console.delete('0.0','end')
    l = language_list()
    for lang in l:
        console.insert('0.0','\n'+str(lang)+' : '+str(l[lang].__name__))

def check():
    console.delete('0.0','end')
    i = interpreter.check_syntax(shell.get('0.0','end'))
    console.insert('0.0','\n'+i) 

def main_active():
    console.delete('0.0','end')
    s = interpreter.run(shell.get('0.0','end')) 
    console.insert('0.0',s) 

def change_json():
    c = change_path(path_entry.get())
    heading['text'] = 'json node root route: {x}'.format(x=path_entry.get())
    path_entry.delete(0,'end')


# here we can see the main structure by clicking the button
see_btn = tk.Button(
    master=main_window,
    background='tomato',
    text='see main',
    fg='black',
    width=90,
    command=show_main
)

# here we run and check the syntax of the commands so that the system 
# can show us if it is structured rightly 
run_btn = tk.Button(
    master=main_window,
    background='seashell3',
    text='run commands',
    fg='black',
    width=90,
    command=check
)

add_btn = tk.Button(
    master=main_window,
    background='seashell2',
    text='add to main',
    fg='black',
    width=90,
    command=main_active
)

change = tk.Button(
    master=main_window,
    background='purple1',
    text='Change Path',
    fg='black',
    width=90,
    command=change_json
)

shell.grid()
run_btn.grid()
add_btn.grid()
see_btn.grid()
path_entry.grid()
change.grid()
heading.grid()
console.grid()
main_window.mainloop()
