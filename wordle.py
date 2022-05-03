import numpy as np
import tkinter as tk

YELLOW = '#FFFF00'
GREY = '#FFFFFF'
GREEN = '#ADFF2F'
LABEL_LIFE = 2000

class Wordle():
    def __init__(self):
        self.voc = self.vocabulary()
        self.word = self.voc[np.random.randint(0, len(self.voc))] #as a string
        self.letters = set(self.word)
        self.guessedLetters = [(letter, GREY) for letter in self.word]
        self.game_over = False
        self.nguesses = 0

        self.bgcolor = '#FFFFFF'
        self.fgcolor = 'black'
        self.font = 'Verdana 30 bold'
        self.window = tk.Tk()
        self.window.configure(background=self.bgcolor)

        # DEBUG
        # print('The word is: ', self.word)

    def vocabulary(self):
        words = np.loadtxt('words.italian.txt', dtype='str')
        words5letters = np.array([word for word in words if len(word) == 5], dtype='str')
        return words5letters

    def wordle(self, word):
        #check length
        if len(word) != 5: return 'Wrong length, try again'
        #check if word is in vocabulary
        if word not in self.voc: return 'Word not in vocabulary, try again'

        # result is a list of tuples (letter, color)
        result = [(letter, GREY) for letter in word]
        for i in range(len(word)):
            if word[i] in self.letters:
                self.guessedLetters[i] = (word[i], YELLOW)
                result[i] = (word[i], YELLOW)
            if word[i] == self.word[i]:
                self.guessedLetters[i] = (word[i], GREEN)
                result[i] = (word[i], GREEN)
        self.nguesses += 1
        return result

    def play(self):
        self.window.title("Wordle")
        self.window.geometry("400x800")

        def getGuess():
            #clean label
            try :
                label.destroy()
            except:
                pass

            # while not self.game_over:
            print("{} attempts remaining".format(6-self.nguesses))
            guess = entry.get()
            entry.delete(0, 'end')

            start_letters = 1
            r = self.wordle(guess)
            if r == 'Wrong length, try again':
                label = tk.Label(self.window, text=r, font='Verdana 18 bold', bg=self.bgcolor, fg=self.fgcolor)
                label.place(anchor=tk.CENTER, relx=0.5, rely=0.15, relwidth=1, relheight=0.06)
                label.after(LABEL_LIFE, lambda l: l.destroy(), label)
            elif r == 'Word not in vocabulary, try again':
                label = tk.Label(self.window, text=r, font='Verdana 18 bold', bg=self.bgcolor, fg=self.fgcolor)
                label.place(anchor=tk.CENTER, relx=0.5, rely=0.15, relwidth=1, relheight=0.06)
                label.after(LABEL_LIFE, lambda l: l.destroy(), label)

            r = np.array(r).flatten()
            colors = [r[i] for i in range(len(r)) if i%2==1]
            letters = [r[i] for i in range(len(r)) if i%2==0]

            for i in range(int(len(r)/2)):
                label = tk.Label(self.window, text=letters[i], bg=colors[i], fg=self.fgcolor, font=self.font)
                # label.grid(row=self.nguesses, column=i+10)
                label.place( relx=0.08+i/6.5, rely=0.15+self.nguesses/10, relwidth=1/6, relheight=0.06)

            # if the game is over
            if self.nguesses == 6 and colors != [GREEN]*5:
                self.game_over = True
                label = tk.Label(self.window, text='Game Over', font=self.font, bg=self.bgcolor, fg=self.fgcolor)
                label.place(anchor=tk.CENTER, relx=0.3, rely=0.15, relwidth=1, relheight=0.06)
                self.window.after(1000, lambda l: l.destroy(), self.window)
            elif colors == [GREEN]*5:
                self.game_over = True
                label = tk.Label(self.window, text='You win!', font=self.font, bg=self.bgcolor, fg=self.fgcolor)
                label.place(anchor=tk.CENTER, relx=0.3, rely=0.15, relwidth=1, relheight=0.06)
                self.window.after(1000, lambda l: l.destroy(), self.window)

        entry = tk.Entry(self.window, width=5, font=self.font, fg=self.fgcolor, bg=self.bgcolor)
        entry.place(anchor=tk.CENTER, relx=0.3, rely=0.05, relwidth=0.5, relheight=0.06)

        wordGuessBotton = tk.Button(self.window, text="Guess", command=getGuess, fg='#CA0202', 
                                    font=self.font)\
                        .place(anchor=tk.CENTER, relx=0.7, rely=0.05, relwidth=0.5, relheight=0.06)
        self.window.mainloop()



