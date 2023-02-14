from tkinter import *
import random
import pandas
import time
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/word_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    #french_dict = pandas.DataFrame.to_dict(data, orient="records")
    french_dict = data.to_dict(orient="records")



def new_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(french_dict)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(show_card_side, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(show_card_side, image=card_back_img)

def is_known():
    known_words = {}
    known_words[current_card["French"]] = current_card["English"]
    print(known_words)
    french_dict.remove(current_card)
    data = pandas.DataFrame(french_dict)
    #index=false doesn't add the record numbers each time 
    data.to_csv("data/word_to_learn.csv", index=False)
    new_word()

window = Tk()
window.title("French Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
show_card_side = canvas.create_image(400, 263, image=card_front_img)
#x= 400, y=150
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"), fill="black")


#remove boarder and window color
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

right_img = PhotoImage(file="images/right.png")
known_button = Button(image=right_img, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

unknown_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=unknown_img, highlightthickness=0, command=new_word)
unknown_button.grid(row=1, column=0)


new_word()



window.mainloop()

