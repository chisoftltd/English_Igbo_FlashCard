from tkinter import *
import pandas
import random

#   --------------------------------------- CONSTANTS -------------------------------------------
FONT_NAME = "Ariel"
BACKGROUND_COLOR = "#B1DDC6"
selected_word = {}
to_learn = {}


try:
    data = pandas.read_csv("data/words_to_know.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/english_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


#   -------------------------------- CARD & WORD FLASHING  MECHANISM -----------------------------

def next_card():
    global selected_word, flip_timer, to_learn
    window.after_cancel(flip_timer)
    selected_word = random.choice(to_learn)
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=selected_word["English"], fill="black")
    canvas.itemconfig(canvas_front, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


#   ------------------------------------ FLIP CARD MECHANISM -------------------------------------
def flip_card():
    canvas.itemconfig(card_title, text="Igbo", fill="white")
    canvas.itemconfig(card_word, text=selected_word["Igbo"], fill="white")
    canvas.itemconfig(canvas_front, image=card_back)


#   --------------------------- REMOVE KNOWN WORD FROM THE DICT ------------------------------------
def is_known():
    to_learn.remove(selected_word)
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("data/words_to_know.csv", index=False)
    next_card()


#   ------------------------------------------ UI SETUP --------------------------------------------
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas = Canvas(width=800, height=526)
canvas_front = canvas.create_image(400, 263, image=card_front)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 150, text="", fill="black", width=500, font=(FONT_NAME, 40, "italic"))
card_word = canvas.create_text(400, 300, text="", fill="black", font=(FONT_NAME, 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

good_image = PhotoImage(file="images/right.png")
canvas_good = Button(image=good_image, highlightthickness=0, command=is_known)
canvas_good.grid(row=1, column=1)

x_image = PhotoImage(file="images/wrong.png")
canvas_x = Button(image=x_image, highlightthickness=0, command=next_card)
canvas_x.grid(row=1, column=0)

next_card()

window.mainloop()
