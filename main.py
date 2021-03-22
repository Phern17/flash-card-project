from tkinter import *
from tkinter import messagebox
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
try:
    df = pandas.read_csv('./data/words_to_learn.csv')
except FileNotFoundError:
    df = pandas.read_csv('./data/french_words.csv')
fr_en_dict = df.to_dict(orient='records')
current_card = {}


# ---------------------- Card Functions ----------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(fr_en_dict)
    my_canvas.itemconfig(current_canvas_image, image=canvas_french_image)
    my_canvas.itemconfig(canvas_title, text="French", fill='black')
    my_canvas.itemconfig(canvas_word, text=current_card['French'], fill='black')

    flip_timer = window.after(3000, flip_card)


def pop_card():
    if len(fr_en_dict) == 1:
        messagebox.showinfo(title='Hooray!', message='You have remembered all the words!')
    else:
        fr_en_dict.remove(current_card)
        output_df = pandas.DataFrame(fr_en_dict)
        output_df.to_csv('./data/words_to_learn.csv')
        next_card()


def flip_card():
    my_canvas.itemconfig(current_canvas_image, image=canvas_english_image)
    my_canvas.itemconfig(canvas_title, text="English", fill='white')
    my_canvas.itemconfig(canvas_word, text=current_card['English'], fill='white')


# ----------------------- UI Setup ---------------------- #
# Main Window
window = Tk()
window.title('Flashy')
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(3000, flip_card)

# Canvas
my_canvas = Canvas(width='800', height='528', bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_french_image = PhotoImage(file="./images/card_front.png")
canvas_english_image = PhotoImage(file="./images/card_back.png")
current_canvas_image = my_canvas.create_image(400, 264, image=canvas_french_image)
canvas_title = my_canvas.create_text(400, 150, font=('Ariel', 40, 'italic'), text='French')
canvas_word = my_canvas.create_text(400, 263, font=('Ariel', 60, 'bold'), text='')
next_card()
my_canvas.grid(row=0, column=0, columnspan=2)

# Buttons
right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, borderwidth=0, command=pop_card)
right_button.grid(row=1, column=0)

left_image = PhotoImage(file='./images/wrong.png')
left_button = Button(image=left_image, highlightthickness=0, borderwidth=0, command=next_card)
left_button.grid(row=1, column=1)


window.mainloop()

