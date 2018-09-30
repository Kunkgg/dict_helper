
answer = {'local': [['find', '/fa͟ɪnd/', '', ['v.发现…的所在<br> If you <b>find</b> someone or something, you see them or learn where they are. ', 'v.找到；寻得；获得<br> If you <b>find</b> something that you need or want, you succeed inachieving or obtaining it. ', 'v.发现…存在(于)<br> If something <b>is found</b> in a particular place or thing, it exists in that place. ', 'v.发现…处于某种状态；遇见；碰见<br> If you <b>find</b> someone or something in a particular situation, they are in that situation when you see them or come into contact with them. ', 'v.(不知不觉中)发现(自己在做某事)<br> If you <b>find</b> <b>yourself</b> doing something, you are doing it without deciding or intending to do it. ', 'v.(某一时刻或事件)把…置于某种情形中<br> If a time or event <b>finds</b> you in a particular situation, you are in that situation at the time mentioned or when the event occurs. ', 'v.发觉，认识到(某事属实)<br> If you <b>find</b> that something is the case, you become aware of it or realize that it is the case. ', 'v.裁决；判决；判定<br> When a court or jury decides that a person on trial is guilty or innocent, you say that the person <b>has been found</b> guilty or not guilty. ', 'v.觉得；认为<br> You can use <b>find</b> to express your reaction to someone or something. ', 'v.感受到(愉快、安慰等情感)<br> If you <b>find</b> a feeling such as pleasure or comfort <b>in</b> a particular thing or activity, you experience the feeling mentioned as a result of this thing or activity. ', 'v.找出，挤出(时间或金钱)<br> Ifyou <b>find</b> the time or money <b>to</b> do something, you succeed in making or obtaining enough time or money to do it. ', 'n.finding<br><b class="text_blue"></b>；<b class="text_blue"></b>； If you describe someone or something that has been discovered as a <b>find</b>, you mean that they are valuable, interesting, good, or useful. ', 'phrase.找到正确的路(去某处)；成功地到达<br> If you <b>find</b> your <b>way</b> somewhere, you successfully get there by choosingthe right way to go. ', 'phrase.(尤指某物偶然)去到(某处)<br> If something <b>finds</b> its <b>way</b> somewhere, it comes to that place, especially by chance. ', '<br><br/> to <b>find fault with</b><b class="text_blue"></b>； ', '<br>. to <b>find</b> one\'s <b>feet</b><b class="text_blue"></b>； ', 'v.(尤指特意通过努力)发现，找出，查明<br> If you <b>find</b> something <b>out</b>, you learn something that you did not already know, especially by making a deliberate effort to do so. ', 'v.查出…的不轨行为；揭发出<br> If you <b>find</b> someone <b>out</b>, you discover that they have been doing something dishonest. ']]], 'online': ['find', '/faɪnd/', ['n. 发现', 'vi. 裁决', 'vt. 查找，找到；发现；认为；感到；获得', 'n. (Find)人名；(丹)芬']]}
import tkinter
from tkinter import *
from tkinter import ttk

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

row = IntVar(value=1)


def send_all_glossary(first_line, glossary):
    note = note_all_glossary(first_line, glossary)
    print(note)
    

def send_single_glossary(first_line, glossary):
    note = note_single_glossary(first_line, glossary)
    print(note)
    

def note_all_glossary(first_line, answer):
    return {
        'front_card': first_line,
        'back_card': answer[-1]
    }
    

def note_single_glossary(first_line, glossary):
    return {
        'front_card': first_line,
        'back_card': glossary
    }


def make_item(first_line, glossary):
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
            make_item(online_first_line, glossary)

    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

def main():
    display(answer)

if __name__ == '__main__':
    main()

