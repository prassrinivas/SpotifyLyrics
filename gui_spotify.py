import genius, lyric_fetching, spotify
from tkinter import *
class gui_Spotify():


    i = 0
    l = lyric_fetching.lyrics()
#---------------------------------------------------------------------------------------------------

    #def set_lyrics(self, lyrics):
     #   self.lyric =self.lyric.set(lyrics)

    def fetch_lyrics(self, label,words):
        self.l.get_lyrics_loop()
        lyric = lyric.set(f"{self.l.getlyrics()}")
        self.change_text(label=label, lyric = lyric)
        label.after(2000, lambda: self.fetch_lyrics(label=label, lyric=lyric))

    def change_text(self, label, lyric):
        label.config(textvariable = lyric)




    def run(self):
        root = Tk()
        root.config(bg='gray11')

        # Menu Frame
        menu_frame = Frame(root, height=40, bg='gray11')
        menu_frame.pack(side=TOP, fill=X)

        # entry field
        e = Entry(menu_frame, width=20, bg='gray11', fg='black')
        e.pack(side=LEFT, fill=Y)
        e.config(highlightbackground='gray21', highlightcolor='gray21')

        # separator frame
        separator_frame = Frame(root, height=2, bg='gray70')
        separator_frame.pack(side=TOP, fill=X)
        root.config(bg='gray11')

        global lyric
        lyric = StringVar(master=root)
        lyric.set("initial")

        label = Entry(root, textvariable= lyric, bg='gray11', fg='white', font=("Helvetica", 11), state= 'readonly', width=200)
        label.pack(side=TOP, fill= BOTH, expand = TRUE)

        # submit button
        submit = Button(menu_frame, text="Submit", relief=FLAT, bg='gray11', fg='white', activebackground='gray21',
                        activeforeground='white', bd=2)
        submit.config(highlightbackground='gray21', highlightcolor='gray21')
        submit.pack(side=LEFT, fill=Y)




        label.after(1000, lambda: self.fetch_lyrics(label=label, lyric=lyric))
        root.mainloop()


if __name__ == '__main__':
   g=gui_Spotify()
   g.run()