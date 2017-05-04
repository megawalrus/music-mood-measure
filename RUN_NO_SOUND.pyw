import csv
import os
from pygame import event, mouse, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT, init, display, mixer
from pygame.sprite import Sprite
from pygame.image import load
from sys import path
import datetime
from threading import Timer
from Tkinter import *

# Set constants for data storage etc.
os.chdir(path[0])
TOP_FOLDER = os.getcwd()
DATA_FOLDER = os.path.join(TOP_FOLDER, 'Data')
RESOURCES_FOLDER = os.path.join(TOP_FOLDER, 'Resources')
DATA_FILE = os.path.join(DATA_FOLDER, 'Participant_data.csv')
DATA_FILE_HEADER = ['P_ID', 'Date', 'Time', 'Arousal', 'Valence']
ICON = os.path.join(RESOURCES_FOLDER, 'ruler.ico')
SOUND_FILE = os.path.join(RESOURCES_FOLDER, 'sound.mp3')

# Set some constants for arousal/valence window
WHITE = (255, 255, 255)
WIN_CAPTION = 'AV Measure'
AV_WIDTH = 700
AV_HEIGHT = 700
BG = os.path.join(RESOURCES_FOLDER, 'bg.png')
BALL_IMG = 'ball.png'


def centre():

    # Places the window centre-screen
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2) - 100
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def save_id(*args):

    # Saves the ID and closes the window
    global p_ID
    id_input = id_box.get()
    p_ID = id_input
    win.destroy()

# Define ID entry window
win = Tk()
win.bind('<Return>', save_id)
win.resizable(width=False, height=False)  # make window non-resizable
win.title('Participant ID:')
win.iconbitmap(default=os.path.join(TOP_FOLDER, ICON))
id_box = Entry(win, width=35)
id_box.pack()
id_box.focus_set()

# Define ID entry confirm button
id_confirm = Button(win, text='OK', width=10, command=save_id)
id_confirm.pack()

# Launch ID entry window, centred on screen
centre()
mainloop()

# Load images for arousal/valence background and window icon
init()
os.environ['SDL_VIDEO_CENTERED'] = '1'  # centre window on screen
# event.set_grab(True)
BG_IMG = load(os.path.join(BG))
ICON_IMG = load(ICON)

# Set some properties for the ball object
ball = Sprite()
ball.image = load(os.path.join(RESOURCES_FOLDER, BALL_IMG))
ball.image.set_colorkey(WHITE)  # make white background of image transparent
ball.rect = ball.image.get_rect()
ball.rect.x = AV_WIDTH / 2 - ball.rect.width / 2  # get mid point of screen, w.r.t ball
ball.rect.y = AV_HEIGHT / 2 - ball.rect.height / 2

# Display arousal/valence screen
screen = display.set_mode((AV_WIDTH, AV_HEIGHT))
display.set_caption(WIN_CAPTION)
display.set_icon(ICON_IMG)
screen.blit(BG_IMG, [0, 0])
screen.blit(ball.image, (ball.rect.x, ball.rect.y))  # place ball directly in centre, to begin with
display.flip()

# Get time and date info, to include in CSV later
test_date = str(datetime.date.today())


class InfiniteTimer():
    """A Timer class that does not stop, unless you want it to."""

    def __init__(self, seconds, target):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None

    def _handle_target(self):
        self.is_running = True
        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        if self._should_continue: # Code could have been running when cancel was called.
            self.thread = Timer(self.seconds, self._handle_target)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
        else:
            print("Timer already started or running, please wait if you're restarting.")

    def cancel(self):
        if self.thread is not None:
            self._should_continue = False # Just in case thread is running and cancel fails.
            self.thread.cancel()
        else:
            print("Timer never started or failed to initialize.")


av_list = []


def av_grab():
    # Grabs arousal/ valence ratings once per second and writes these to CSV
    global valence
    global arousal
    global test_time
    global av_list

    valence = (ball.rect.x + (ball.rect.width / 2)) - (AV_WIDTH / 2)
    arousal = (AV_HEIGHT - (ball.rect.y + (ball.rect.height / 2))) - (AV_HEIGHT / 2)
    test_time = datetime.datetime.now().time().strftime('%H:%M:%S')
    av_list.append([p_ID, test_date, test_time, arousal, valence])
    # **** Need to get time since opened, too **** !!!!!!!!!!

# Start recording arousal/ valence data
measurement_resolution = 0.1
av_thread = InfiniteTimer(measurement_resolution, av_grab)
av_thread.start()

# Play audio file
mixer.init()
mixer.music.load(SOUND_FILE)
mixer.music.play()

# Set to false until user clicks and drags or exits, respectively
drag = False
EXIT = False

while not EXIT:

    for e in event.get():

        # While user holds mouse down over ball, set ball coordinates equal to mouse position
        if e.type == MOUSEBUTTONDOWN and ball.rect.collidepoint(mouse.get_pos()):
            drag = True

        if drag:

            # Stop updating ball position with mouse position if user lets go of mouse...
            if e.type == MOUSEBUTTONUP and e.button == 1:
                drag = False

            # ...otherwise, keep on draggin'
            else:
                ball.rect.x, ball.rect.y = mouse.get_pos()
                ball.rect.x -= ball.rect.width / 2  # centre ball w.r.t current mouse position
                ball.rect.y -= ball.rect.height / 2

                # Re-draw background and new ball position on screen
                screen.blit(BG_IMG, [0, 0])
                screen.blit(ball.image, (ball.rect.x, ball.rect.y))
                display.flip()

        # Save ball coordinates and timestamp on closing down
        if e.type == QUIT:

            # CLOSE THE THREAD!!!!
            av_thread.cancel()

            # Open a CSV file for writing arousal/ valence ratings
            if p_ID != '0':  # don't log data if ID of 0 is entered

                with open(DATA_FILE, 'ab') as data_file:
                    writer = csv.writer(data_file, delimiter=',')
                    if os.stat(DATA_FILE).st_size == 0:
                        writer.writerow(DATA_FILE_HEADER)  # Add header if file is empty
                    writer.writerows(av_list)

            EXIT = True
