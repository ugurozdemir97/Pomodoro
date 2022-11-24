from tkinter import Tk, Canvas, Label, Button, PhotoImage, Frame
from tkinter.constants import FLAT
from winsound import PlaySound, SND_ASYNC
from pygame import mixer
import os

# ------------------------------------- CONSTANTS ----------------------------------- #

BACKGROUND = "#f7c1a2"
RED = "#da3e3e"
PINK = "#da3e3e"
GREEN = "#50a72d"
LIGHT_GREEN = "#50a72d"

STUDY_TIME = 25  # These shouldn't be less than 1 minute for the indicator to work properly
REST_SHORT = 5
REST_LONG = 30
CURRENT_TIME = 0
STEP = 0

FONT = "Ink Free"
MUSIC_ON = "🔊"
MUSIC_OFF = "🔇"
POMODORO = ""

COUNT_DOWN = ""  # These will be used to call function every second
ANIMATION = ""
POS = (126, 125, 128, 135, 130, 125, 128, 115)  # Shape of the indicator
X_POS = 55
MOVE = False


# --------------------------------------- MUSIC ------------------------------------- #

def play_music():
    mixer.init()
    path = "./Music"
    all_mp3 = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.mp3')]

    for i, song in enumerate(all_mp3):
        if i == 0:
            mixer.music.load(song)
            mixer.music.play()
        else:
            mixer.music.queue(song)

    music.config(command=stop_music, text=MUSIC_ON)


def stop_music():
    mixer.music.stop()
    music.config(command=play_music, text=MUSIC_OFF)


# -------------------------------- INDICATOR POSITION ------------------------------- #

# def clicked(event):
#     canvas.itemconfig(coordinates, text=f"You clicked on ({str(event.x)}, {str(event.y)})")

def position(time):
    global ANIMATION, X_POS, MOVE

    if MOVE:

        # ----------- POSITION OF Y ---------- #

        x = int(canvas.coords(indicator)[0])
        y = int((134.5514 + (0.5652235 * x) - 0.002355505 * (x ** 2)) - 10)

        # --------- MOVE THE INDICATOR ------- #

        canvas.moveto(indicator, x, y)
        # Normally this should not change the position of x, but x increases one by one.
        # I know that it will take 125 steps to complete the road in x-axis. And I know how much time it should take.
        # So all I need to do is to divide the time to steps to find how many times to call this function.

    # --------------- HOW MANY TIMES TO CALL ------------- #

    z = int((time * 1000) / 125)
    ANIMATION = window.after(z, position, time)

    MOVE = True

    # Now everytime I click pause and continue indicator move 1 in x-axis but time doesn't change. It's possible to
    # set the time to 10 hours but moving the indication to the end in 1 second. So I will create a constant called
    # MOVE to keep track of the times that clicked pause and continue. And when it sees I've just clicked continue
    # it will not move indicator.


# ----------------------------------- COMMAND LABEL --------------------------------- #

def change_label():
    if STEP == 8:
        command.config(text="REST", fg=GREEN)
    elif STEP % 2 == 0:
        command.config(text="REST", fg=GREEN)
    else:
        command.config(text="WORK", fg=RED)


# --------------------------------------- TIMER ------------------------------------- #

# -------- SEND SECONDS TO START FUNCTION -------- #

def send_time():
    global STEP, CURRENT_TIME, X_POS, POMODORO
    play_btn.config(command=pause, bg=GREEN, activebackground=LIGHT_GREEN, text="Pause")  # Change Button

    # ------- IF PAUSED SEND THE TIME LEFT -------- #

    if CURRENT_TIME:
        change_label()
        position(CURRENT_TIME)
        start(CURRENT_TIME)

    # --- OTHERWISE SEND TIME ACCORDING TO STEP --- #

    else:
        X_POS = 55
        canvas.moveto(indicator, 55, 148)  # Reset the indicator position
        STEP += 1  # Increase the step
        change_label()
        if STEP == 8:
            PlaySound("Flowers.wav", SND_ASYNC)
            POMODORO += "🍅"
            check_mark.config(text=POMODORO)
            position(REST_LONG * 60)
            start(REST_LONG * 60)
        elif STEP % 2 == 0:
            PlaySound("Flowers.wav", SND_ASYNC)
            POMODORO += "🍅"
            check_mark.config(text=POMODORO)
            position(REST_SHORT * 60)
            start(REST_SHORT * 60)
        else:
            position(STUDY_TIME * 60)
            start(STUDY_TIME * 60)


# -------------- TIMER FUNCTION ---------------- #

def start(time):
    global CURRENT_TIME, COUNT_DOWN, ANIMATION

    minutes = time // 60
    seconds = time % 60

    minutes = "{:02}".format(minutes)  # These will add 0 in the beginning if it is just 1 digit
    seconds = "{:02}".format(seconds)
    time_string = f"{minutes}:{seconds}"

    canvas.itemconfig(timer, text=time_string)  # Write the time
    CURRENT_TIME = time  # Set CURRENT_TIME as new tie

    if CURRENT_TIME > 0:
        COUNT_DOWN = window.after(1000, start, time - 1)  # Call this function every second with less time
    else:
        CURRENT_TIME = 0
        window.after_cancel(COUNT_DOWN)
        window.after_cancel(ANIMATION)
        send_time()


# ----------------- PAUSE TIME ------------------ #

def pause():
    global X_POS, MOVE

    play_btn.config(command=send_time, bg=RED, activebackground=PINK, text="Continue")
    command.config(text="PAUSED", fg=GREEN)

    window.after_cancel(ANIMATION)
    window.after_cancel(COUNT_DOWN)

    X_POS = canvas.coords(indicator)[0]
    MOVE = False


# -------------------------------- RESET EVERYTHING --------------------------------- #


def reset():
    global CURRENT_TIME, STEP, X_POS, MOVE

    window.after_cancel(ANIMATION)  # Stop animation
    window.after_cancel(COUNT_DOWN)  # Stop timer

    play_btn.config(command=send_time, bg=RED, activebackground=PINK, text="Start")
    command.config(text="POMODORO", fg=RED)
    check_mark.config(text="")
    canvas.itemconfig(timer, text="00:00")

    CURRENT_TIME = 0
    STEP = 0

    X_POS = 55
    canvas.moveto(indicator, 55, 148)

    MOVE = False


# --------------------------------------- SETUP ------------------------------------- #

# -------------- WINDOW ----------------- #

window = Tk()
window.geometry("400x470+600+200")
window.minsize(width=400, height=470)
window.title("Pomodoro")
window.config(bg=GREEN)

# -------------- IMAGE ----------------- #

tomato = PhotoImage(file="tomato.png")

# ----- FRAME TO HOLD ALL WIDGETS ------ #

frame = Frame(bg=BACKGROUND, pady=20, padx=30)
frame.pack(expand=True)

# ------------- BUTTONS --------------- #

music = Button(frame, text=MUSIC_OFF, font=5, bg=BACKGROUND,
               activebackground=BACKGROUND, relief=FLAT, command=play_music)
play_btn = Button(frame, width=20, text="Start", bg=RED,
                  activebackground=PINK, fg="white", font=(FONT, 10, "bold"), pady=3, command=send_time)
reset_btn = Button(frame, width=20, text="Reset", bg=RED,
                   activebackground=PINK, fg="white", font=(FONT, 10, "bold"), pady=3, command=reset)

# ------------- LABELS ---------------- #

command = Label(frame, text="POMODORO", font=(FONT, 25, "bold"), fg=RED, bg=BACKGROUND)
check_mark = Label(frame, bg=BACKGROUND, text=POMODORO, font=(FONT, 15, "bold"), fg=RED)

# ------------- CANVAS ---------------- #

canvas = Canvas(frame, width=250, height=250, bg=BACKGROUND, highlightthickness=0)
canvas.create_image(125, 125, image=tomato)
indicator = canvas.create_polygon(POS, fill="white", width=0)
canvas.moveto(indicator, 55, 148)
timer = canvas.create_text(125, 125, text="00:00", font=("Calibri", 22), fill="white")

# ------- TO FIND INDICATOR POSITIONS ------- #

# This will tell you the coordinates of the point you clicked.

# coordinates = canvas.create_text(125, 50, text="", fill="black", font=("Arial", 12, "bold"))
# window.bind("<Button-1>", clicked)

# X1 = 55  # Indicator's x and y coordinates in the arc.
# X2 = 180
# Y1 = 160
# Y2 = 165
# Y3 = 170

# ----------- GRID LAYOUT ------------- #

music.grid(row=0, column=0, pady=(30, 20), padx=(0, 100))
command.grid(row=0, column=0, columnspan=3, pady=(30, 20))

canvas.grid(row=1, column=0, columnspan=3, pady=(0, 5))

check_mark.grid(row=2, column=0, columnspan=3)

play_btn.grid(row=3, column=0, pady=(15, 0))
reset_btn.grid(row=3, column=2, pady=(15, 0))

window.mainloop()
