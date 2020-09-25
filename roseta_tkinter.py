import tkinter as tk
import roseta_main
from roseta_main import roseta,Peripherals,Analysis,Node,Synthesis

text_sync = []
btn_list = []

native_list = []
target_list = []

main_window = tk.Tk()
main_window.title('Roseta tkinter')

text_show = tk.Text(
    master=main_window,
    bg='seashell2',
    fg='black'
)

time_run = tk.Label(
    master=main_window,
    bg='seashell2',
    fg='black',
    text='run time:'
)

lang_list_0 = tk.Listbox(
    master=main_window,
    bg='white',
    fg='black',
    height=1
)

lang_list_1 = tk.Listbox(
    master=main_window,
    bg='white',
    fg='black',
    height=1
)

native = tk.Label(
    master=main_window,
    bg='seashell2',
    fg='black',
    text='Your language'
)

target = tk.Label(
    master=main_window,
    bg='seashell2',
    fg='black',
    text='Target language'
)


lang = Peripherals.lang_total(None,1)

for l in lang:
    lang_list_0.insert(list(lang.keys()).index(l),l)
    lang_list_1.insert(list(lang.keys()).index(l),l)

def async_run():
    btn_list = []

    counter = 0
    while counter < 3 :
        if len(btn_list) != 0:
            break 
        else:
            audio_file = Peripherals.record(5)
# as mentioned before, we can stop the exception handlers that will say us what is happening in a simpler way 
# for all those expcetions there's a string that represents it and stops the main process 
            text_init = Analysis._init_(audio_file,native_list[len(native_list)-1])
            if text_init == 'error 0':
                print(text_init)
                
            translated = Node._selection_(str(text_init),target_list[len(target_list)-1])
            if translated == 'error 1':
                print(translated)
                
            text_show.insert('0.0','\n'+str(translated))
                
            synth_text = Synthesis._init_(translated,target_list[len(target_list)-1])
            if synth_text == 'error 2':
                print(synth_text) 

        counter+=1        

def stop_func():
    btn_list.append(1)
    print(btn_list)

def insert_func_n():

    n = lang_list_0.get(lang_list_0.curselection())
    print(n)

    native_list.append(n)

def insert_func_t():

    t = lang_list_1.get(lang_list_1.curselection())
    print(t)

    target_list.append(t)

def open_shell():
    import node_shell



select_btn_n = tk.Button(
    master=main_window,
    text='save',
    bg='lightSkyBlue',
    fg='black',
    width=45,
    command=insert_func_n
)

select_btn_t = tk.Button(
    master=main_window,
    text='save',
    bg='lightSkyBlue',
    fg='black',
    width=45,
    command=insert_func_t
)

start_btn = tk.Button(
    master=main_window,
    text='start',
    bg='tomato',
    fg='black',
    width=45,
    command=async_run
)

stop_btn = tk.Button(
    master=main_window,
    text='stop',
    bg='khaki',
    fg='black',
    width=45,
    command=stop_func
)

shell_btn = tk.Button(
    master=main_window,
    text='acess nodes',
    bg='black',
    fg='lime',
    width=45,
    command=open_shell
)

def clear():
    text_show.delete('0.0','end')

clear_console = tk.Button(
    master=main_window,
    text='clear',
    bg='black',
    fg='lime',
    width=45,
    command=clear 
)

native.grid()
lang_list_0.grid()
select_btn_n.grid()

target.grid()
lang_list_1.grid()
select_btn_t.grid()

start_btn.grid()
stop_btn.grid()
shell_btn.grid()
time_run.grid()
text_show.grid()
clear_console.grid()
main_window.mainloop()