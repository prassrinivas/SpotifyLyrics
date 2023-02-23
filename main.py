import lyric_fetching
from tkinter import *
import tkinter.scrolledtext as tkst

l = lyric_fetching.lyrics()
cachedlyrics = ""
lyric = "--"
root = Tk()
root.config(bg='gray11')
root.geometry("235x650")
root.title("Spotify Lyrics")
#root.iconbitmap("C:/Users/srini/Downloads/favicon.ico")
#root.iconphoto(False, PhotoImage(file='C:/Users/srini/Downloads/favicon.ico'))

cachedruntime = 0
runtime = 0
scroll_rate = 0
#Spotipy
# Menu Frame
menu_frame = Frame(root, height=40, bg='gray11')
menu_frame.pack(side=TOP, fill=X)

# entry field
e = Entry(menu_frame, width=20, bg='gray11', fg='white')
e.pack(side=LEFT, fill=Y)
e.config(highlightbackground='gray21', highlightcolor='gray21', insertbackground = 'lime green')

# separator frame
separator_frame = Frame(root, height=2, bg='lime green')
separator_frame.pack(side=TOP, fill=X)
root.config(bg='gray11')

#body frame
body_frame = Frame(root)
body_frame.pack(side=TOP, fill = BOTH, expand = TRUE)
label = tkst.ScrolledText(body_frame, bg='gray11', fg='white', font=("Helvetica", 11), wrap= WORD,insertbackground = 'lime green')
label.pack(side=TOP, fill= BOTH, expand = TRUE)

# submit button
submit = Button(menu_frame, text="Submit", relief=FLAT, bg='gray11', fg='white', activebackground='gray21',
                activeforeground='white', bd=2, command= lambda :update_search_term(e.get()))
submit.config(highlightbackground='gray21', highlightcolor='gray21')
submit.pack(side=LEFT, fill=Y)


def fetch_lyrics():
    global cachedlyrics
    global lyric
    global label

    l.get_lyrics_loop()
    lyric = l.getlyrics()
    if lyric == "couldn't find song from genius search":
        l.get_lyrics_loop(second_attempt=True)
        lyric = l.getlyrics()
    if not cachedlyrics == lyric:
        change_text()
        cachedlyrics = lyric
        #runtime = int(l.p.currently_playing()['item']['duration_ms'])

    label.after(2000, lambda: fetch_lyrics())
    #label.after(5000, scroll)


def change_text():
    label.delete(1.0, END)
    label.insert(INSERT, l.title+ "\n"+ lyric)

def update_search_term(new_search_term):
    l.refine_search_term(title=l.title, new_search_term=new_search_term)
    e.delete(0,END)

def scroll():
    global scroll_rate
    global cachedruntime
    global label
    if cachedruntime != runtime:
        scroll_rate = 1/runtime
        label.config(yScrollIncrement = '100')
        cachedruntime = runtime
    label.yview_scroll(1, "units")
    #label.after(2000, scroll)
l.update_song_replacement_dict()
label.after(1000, fetch_lyrics)
root.mainloop()
