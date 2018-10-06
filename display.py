"""
this module implements GUI
"""
import tkinter
from tkinter import *
from tkinter import ttk

from connectoAnki import addNote
from connectoAnki import data_add_note

# format string
LOCAL_FIRST_LINE = '{}\t{}'
ONLINE_FIRST_LINE = 'YouDao\n\n{}\t{}'

def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    canvas.configure(scrollregion=canvas.bbox('all'))

# forge the root weight and entitle
root = Tk()
root.title("Dict Helper")

# --- create canvas with scrollbar ---

canvas = tkinter.Canvas(root, width=620)
canvas.pack(side=tkinter.LEFT)

scrollbar = tkinter.Scrollbar(root, command=canvas.yview)
scrollbar.pack(side=tkinter.LEFT, fill='y')

canvas.configure(yscrollcommand = scrollbar.set)

# update scrollregion after starting 'mainloop'
# when all widgets are in canvas
canvas.bind('<Configure>', on_configure)

# --- put frame in canvas ---

mainframe = ttk.Frame(canvas, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

canvas.create_window((0,0), window=mainframe, anchor='nw')

# grid row
row = IntVar(value=1)

def newNote(note):
    """new note"""
    fields = data_add_note['params']['note']['fields'].keys()
    for field in fields:
        data_add_note['params']['note']['fields'][field] = note.get(field, '')
    return data_add_note

def send_all_glossary(first_line, glossary):
    """send all glossarys to Anki"""
    note = note_all_glossary(first_line, glossary)
    note = newNote(note)
    # print(note)
    addNote(note)
    

def send_single_glossary(first_line, glossary):
    """send a speical glossary to Anki"""
    note = note_single_glossary(first_line, glossary)
    note = newNote(note)
    # print(note)
    addNote(note)

def _expAndreading(first_line):
    if first_line.startswith('YouDao'):
        first_line = first_line[8:]
    return first_line.split('\t')

def note_all_glossary(first_line, answer):
    """record all glossarys"""
    exp, reading = _expAndreading(first_line)
    return {
        'expression': exp,
        'reading': reading,
        'glossary': answer[-1]
    }
    

def note_single_glossary(first_line, glossary):
    """record single glossarys"""
    exp, reading = _expAndreading(first_line)
    return {
        'expression': exp,
        'reading': reading,
        'glossary': glossary
    }


def make_item(first_line, glossary):
    """make glossary label and accordding Anki button"""
    ttk.Label(
        mainframe, 
        text=glossary, 
        wraplength=500).grid(column=1, row=row.get(), sticky=W)
    ttk.Button(
        mainframe, 
        text="Anki", 
        command=lambda: send_single_glossary(first_line, glossary)
        ).grid(column=2, row=row.get(), sticky=E)

def display(answer): 
    """forge GUI"""

    local_answers = answer.get('local')
    online_answer = answer.get('online')
    
    for local_answer in local_answers:
        if local_answer:
            local_first_line = LOCAL_FIRST_LINE.format(local_answer[0],local_answer[1])
            
            row.set(row.get()+1)
            ttk.Label(
                mainframe, 
                text=local_first_line, 
                foreground='red',
                font="-size 18").grid(column=1, row=row.get(), sticky=W)
            ttk.Button(
                    mainframe, 
                    text="AlltoAnki", 
                    command=lambda: send_all_glossary(local_first_line, local_answer)
                    ).grid(column=2, row=row.get(), sticky=E)
            for glossary in local_answer[-1]:
                row.set(row.get()+1)
                # local_first_line_sigle = local_first_line + '\t\t' + str(row.get())
                # make_item(local_first_line_sigle, glossary)
                make_item(local_first_line, glossary)
    if online_answer:
        row.set(row.get()+1)
        online_first_line = ONLINE_FIRST_LINE.format(online_answer[0],online_answer[1])
        ttk.Label(
            mainframe, 
            text=online_first_line, 
            foreground='red',
            font="-size 18").grid(column=1, row=row.get(), sticky=W)
        ttk.Button(
                mainframe, 
                text="AlltoAnki", 
                command=lambda: send_all_glossary(online_first_line, online_answer)
                ).grid(column=2, row=row.get(), sticky=E)
        
        for glossary in online_answer[-1]:
            row.set(row.get()+1)
            # online_first_line_sigle = online_first_line + '\t\t' + str(row.get())
            # make_item(online_first_line_sigle, glossary)
            make_item(online_first_line, glossary)
    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    root.mainloop()


