import ant_simulation
import image_processor

import json
import random
import numpy as np
import tkinter
from tkinter import *
# from tkinter.ttk import *
from tkinter import ttk
import tkinter.messagebox
import tkinter.simpledialog
import tkinter.colorchooser
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfilename

window = tkinter.Tk()
window.title("Langton's Ant Creator")

global progress_bar


def progress_setup(max_value):
    global progress_bar
    progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
    progress_bar["value"] = 0
    progress_bar["maximum"] = max_value
    progress_bar.grid(row=8, column=9, columnspan=6)
    progress_bar.config(length=230)


def progress_update(curr_value):
    global progress_bar
    progress_bar["value"] = curr_value
    progress_bar.update()


def prepare_window():
    # Internal Variables

    # Keeps track of row for placing widgets in GUI
    curr_row = 0
    # Where the gif is saved and its filename
    global gif_filename
    gif_filename = ''
    global gif_file_button
    global gif_length_input
    global start_button
    global num_colors_field
    global color_direction_values
    color_direction_values = []
    # Checkbox value for logarithmic scaling
    global log_check
    global log_box
    # Steps input for how many times the ant should move
    global steps_input
    # Inputs for both the height and width of the grid
    global width_input
    width_input = 500
    global height_input
    height_input = 500
    # Total number of colors for simulation
    global num_colors
    num_colors = 2
    # List of buttons for the ant placement grid
    global ant_buttons
    ant_buttons = []
    # List of buttons for the color swatches
    global color_buttons
    color_buttons = []
    # List of buttons for the color direction menus
    global color_direction_button
    color_direction_button = []
    # Hex data for colors
    global color_hex_values
    color_hex_values = ["#ffffff", "#000000", "#ff0000", "#00ff00", "#0000ff",
                        "#ffff00", "#ff00ff", "#00ffff", "#ff7300", "#02007a"]

    # Saves all of the preferences to save time
    def save():
        global num_colors, color_direction_values, width_input, height_input, steps_input
        global log_check, color_hex_values, ant_buttons, gif_filename, gif_length_input
        color_directions = []
        for z in range(0, num_colors):
            color_directions.append(color_direction_values[z].get())
        config = {'Number_Of_Colors': num_colors,
                  'Hex_Value_Colors': color_hex_values,
                  'Gif_Export_Location': gif_filename,
                  # 'Gif_Length': int(gif_length_input.get()),
                  'Grid_Size_X': int(width_input.get()),
                  'Grid_Size_Y': int(height_input.get()),
                  'Number_Of_Steps': int(steps_input.get()),
                  'Log_Check': bool(log_check.get()),
                  'Color_Direction_Values': color_directions,
                  'Ant_Data': translate_ant_data(0, 0)
                  }
        json.dump(config, open('Langton_Ant_Preferences.json', 'w'))

    # Restores previous settings from last session
    def restore():
        global num_colors, width_input, height_input, steps_input, color_direction_values, gif_length_input
        global log_box, color_hex_values, gif_filename, num_colors_field, gif_file_button
        try:
            config = json.load(open('Langton_Ant_Preferences.json'))
            num_colors_field.insert(0, str(config['Number_Of_Colors']))
            color_hex_values = config['Hex_Value_Colors']
            change_num_colors()
            gif_filename = config['Gif_Export_Location']
            image_processor.set_gif_filename(gif_filename)
            gif_file_button.config(text=gif_filename, width=16)
            # gif_length_input.insert(0, config['Gif_Length'])
            gif_length_input.delete(0, 'end')
            gif_length_input.insert(0, 100)
            width_input.insert(0, config['Grid_Size_X'])
            height_input.insert(0, config['Grid_Size_Y'])
            steps_input.insert(0, config['Number_Of_Steps'])
            ant_data = config['Ant_Data']
            if config['Log_Check']:
                log_box.select()
            for z in range(0, num_colors):
                color_direction_values[z].set(config['Color_Direction_Values'][z])
            for i in range(0, len(ant_data)):
                ant_left_click(ant_data[i][1], ant_data[i][0])
                for j in range(0, ant_data[i][2]):
                    ant_right_click(ant_data[i][1], ant_data[i][0])
        except FileNotFoundError:
            restore_default()

    # Most basic settings to show original langton's ant
    def restore_default():
        global ant_buttons, log_box, color_hex_values, gif_length_input
        num_colors_field.delete(0, 'end')
        num_colors_field.insert(0, 2)
        color_hex_values[0] = "#ffffff"
        color_hex_values[1] = "#000000"
        change_num_colors()
        gif_length_input.delete(0, 'end')
        gif_length_input.insert(0, 100)
        width_input.delete(0, 'end')
        width_input.insert(0, 250)
        height_input.delete(0, 'end')
        height_input.insert(0, 250)
        steps_input.delete(0, 'end')
        steps_input.insert(0, 12000)
        color_direction_values[0].set("Right")
        color_direction_values[1].set("Left")
        for i in range(0, 9):
            for j in range(0, 9):
                if ant_buttons[i][j]["text"] != " ":
                    ant_left_click(i, j)
        ant_left_click(4, 4)
        ant_right_click(4, 4)
        ant_right_click(4, 4)
        ant_right_click(4, 4)

    # What happens when the Start Button is Hit
    def start():
        if not check_ints():
            return
        save()

        global num_colors, color_direction_values, width_input, height_input, steps_input
        global log_check, color_hex_values, ant_buttons, start_button, gif_length_input

        start_button.config(text="Processing...")

        # The grid is a numpy array because it needs to stay this fixed size
        grid = np.zeros((int(height_input.get()), int(width_input.get())), dtype=np.uint)
        max_steps = int(steps_input.get())

        width_buffer = int((int(width_input.get()) / 2) - 4)
        height_buffer = int((int(height_input.get()) / 2) - 4)
        ant_data = translate_ant_data(width_buffer, height_buffer)

        if len(ant_data) < 1:
            tkinter.messagebox.showinfo("Ant Warning", "You Must Have At Least One Ant Placed")
            return

        # Gather all of the option menu inputs for the given number of colors
        color_action = []
        for z in range(0, num_colors):
            tmp_text = color_direction_values[z].get()
            # print(tmp_text)
            if tmp_text == "Up":
                color_action.append(0)
            elif tmp_text == "Right":
                color_action.append(1)
            elif tmp_text == "Down":
                color_action.append(2)
            elif tmp_text == "Left":
                color_action.append(-1)
            else:
                tkinter.messagebox.showinfo("Setup Warning", "All Colors Must Have An Action")
                return

        # Send it over to the image processor
        image_processor.set_gif_length(int(gif_length_input.get()))
        image_processor.set_log(bool(log_check.get()))
        image_processor.set_color_hex(color_hex_values)
        image_processor.set_height(int(height_input.get()))
        image_processor.set_width(int(width_input.get()))
        image_processor.set_max_steps(int(steps_input.get()))
        image_processor.setup()

        # Send it all to the run_simulation
        ant_simulation.run_simulation(ant_data, color_action, grid, max_steps)
        start_button.config(text="Start")

    # Creates the top menu bar for adv options and other nested capabilities
    def create_menu():
        menu_bar = tkinter.Menu(window)
        menu_size = tkinter.Menu(window, tearoff=0)
        menu_size.add_command(label="Save", command=lambda: save())
        menu_size.add_command(label="Reset", command=lambda: restore_default())
        menu_size.add_command(label="Custom Image Background", command=lambda: print("Custom Image"))
        # menu_size.add_separator()
        menu_bar.add_cascade(label="File", menu=menu_size)
        menu_bar.add_cascade(label="Info", command=lambda: read_me_display())
        menu_bar.add_cascade(label="Random", command=lambda: random_setup())
        menu_bar.add_command(label="Exit", command=lambda: window.destroy())
        window.config(menu=menu_bar)

    def read_me_display():
        read_me = "Welcome To The Python Langton Ant Generator\n" \
               "Created By : Jacob Leazott\n\n" \
               "------------------------------------------ ANT PLACEMENT ------------------------------------------\n" \
               "Left-Click to place and remove ants on the far left grid\n" \
               "Right-Click to change it's starting direction\n\n" \
               "---------------------------------------- COLORS AND ACTIONS ---------------------------------------\n" \
               "\"Number Of Colors\" - Enter the desired amount of colors here and hit the \"Change\" Button\n" \
               "Right-Click on color swatches to open up a color picker to change these values\n" \
               "Right-Click on the drop down menu's to the right of the color swatch to change it's action\n" \
               "This will be the action that happens when the ant is on a square of this color\n" \
               "Up = No change in direction\n" \
               "Right = Clockwise Turn\n" \
               "Left = Counter-Clockwise turn\n" \
               "Down = A 180 degree turn\n\n" \
               "------------------------------------------- GIF CREATION ------------------------------------------\n" \
               "\"Gif Length\" - Input here how many frames you would like your gif to have\n" \
               "Approximately 10 frames per second on playback\n" \
               "\"Gif File Export Location\" - This will open up the file explorer for you to name\n" \
               "and choose where the gif will be saved\n\n" \
               "------------------------------------------ OTHER FEATURES -----------------------------------------\n" \
               "\"Grid Size X and Y\" - Input the pixel dimensions that the ant will be put in\n" \
               "\"File\" In the file tab you can save your current settings and inputs\n" \
               "They will also save if you hit \"Exit\" or simply run the program\n" \
               "\"Reset\" - Resets your current session to have the default Langton ant setup\n" \
               "\"Random\" - Will somewhat randomly fill in all your inputs and conditions for extra fun"
        win = Toplevel(window)
        display = Label(win, text=read_me)
        display.pack()

    # Checks and throws error windows when inputs are not usable
    def check_ints():
        global width_input, height_input, steps_input, gif_length_input
        try:
            int(gif_length_input.get())
        except ValueError:
            tkinter.messagebox.showinfo("Value Warning", "Your Gif Length Value Is Not An Integer")
            return False
        try:
            int(width_input.get())
        except ValueError:
            tkinter.messagebox.showinfo("Value Warning", "Your Grid X Value Is Not An Integer")
            return False
        try:
            int(height_input.get())
        except ValueError:
            tkinter.messagebox.showinfo("Value Warning", "Your Grid Y Value Is Not An Integer")
            return False
        try:
            int(steps_input.get())
            if int(steps_input.get()) < 1:
                tkinter.messagebox.showinfo("Value Warning", "Your Steps Value Is Too Small\nMin = 1")
                return False
        except ValueError:
            tkinter.messagebox.showinfo("Value Warning", "Your Step Value Is Not An Integer")
            return False
        if int(gif_length_input.get()) > 1000:
            tkinter.messagebox.showinfo("Size Warning", "Your Gif Length Is Too Long\nMax Length: 1000")
            return False
        if int(gif_length_input.get()) < 1:
            tkinter.messagebox.showinfo("Size Warning", "Your Gif Length Is Too Short\nMin Length: 1")
            return False
        if int(width_input.get()) > 2500 or int(height_input.get()) > 2500:
            tkinter.messagebox.showinfo("Size Warning", "Your Grid Size Is Too Large\nMax Size: 2500 x 2500")
            return False
        if int(width_input.get()) < 10 or int(height_input.get()) < 10:
            tkinter.messagebox.showinfo("Size Warning", "Your Grid Size Is Too Small\nMin Size: 10 x 10")
            return False
        return True

    # Takes the ant_buttons and turns them into an array that can be saved for preferences or passed to simulation
    def translate_ant_data(shift_x, shift_y):
        global ant_buttons
        ant_data = []
        for i in range(0, 9):
            for j in range(0, 9):
                if "▲" == ant_buttons[i][j]["text"]:
                    ant_data.append([(shift_y + j), (shift_x + i), 0])
                elif "▶" == ant_buttons[i][j]["text"]:
                    ant_data.append([(shift_y + j), (shift_x + i), 1])
                elif "▼" == ant_buttons[i][j]["text"]:
                    ant_data.append([(shift_y + j), (shift_x + i), 2])
                elif "◀" == ant_buttons[i][j]["text"]:
                    ant_data.append([(shift_y + j), (shift_x + i), 3])
        return ant_data

    # Generates a random setup for the simulation
    def random_setup():
        global ant_buttons, log_box, color_hex_values
        num_colors_field.delete(0, 'end')
        num = random.randint(2, 20)
        num_colors_field.insert(0, num)
        change_num_colors()
        width_input.delete(0, 'end')
        width_input.insert(0, 250)
        height_input.delete(0, 'end')
        height_input.insert(0, 250)
        steps_input.delete(0, 'end')
        steps_input.insert(0, 12000)
        choices = ["Right", "Left", "Up", "Down"]
        for i in range(0, num):
            color_direction_values[i].set(choices[random.randint(0, 3)])
        for i in range(0, 9):
            for j in range(0, 9):
                if ant_buttons[i][j]["text"] != " ":
                    ant_left_click(i, j)
                tmp = random.randint(1, 100)
                if tmp % 10 == 0:
                    ant_left_click(i, j)
                    for z in range(0, random.randint(0, 3)):
                        ant_right_click(i, j)

    # Asks where you would like to save your gif file as well as what its name will be
    def gif_file_input_callback():
        global gif_filename, gif_file_button
        gif_filename = asksaveasfilename(filetypes=[('gif File', '*.gif')])
        image_processor.set_gif_filename(gif_filename)
        gif_file_button.config(text=gif_filename, width=16)

    # Sets up the right side with all of the color inputs and their respective action fields
    def setup_colors():
        global color_buttons, color_direction_button, color_direction_values
        # Up means straight continue going the direction they are facing
        # Right means turn CW
        # Down means do a 180 degree turn
        # Left means turn CCW
        choices = {"Up", "Right", "Down", "Left"}
        col_val = 0
        for i in range(0, num_colors):
            c = tkinter.Button(window, text=" ", width=2, command=lambda z=i: color_left_click(z))
            c.config(bg=color_hex_values[i])
            if i % 10 == 0:
                col_val += 1
            # Some random equations in the row and column variables to make them shift over correctly after 9 colors
            c.grid(row=(i % 9), column=int(15 + 2 * int(i / 9)), padx=5, sticky=W)
            # Labels and boxes for direction
            tmp_var = StringVar(window)
            color_direction_values.append(tmp_var)
            o = OptionMenu(window, color_direction_values[i], *choices)
            o.grid(row=(i % 9), column=int(16 + 2 * int(i / 9)))
            o.configure(width=4, bg='light gray')
            color_direction_button.append(o)
            color_buttons.append(c)

    # Generates a random rgb value for colors not specified
    def rand_rgb():
        return random.randint(0, 255)

    # When you change the number of colors it deletes all of the ant_buttons and recreates them for convenience
    def change_num_colors():
        global num_colors, num_Colors_Field, color_direction_button, color_buttons
        try:
            int(num_colors_field.get())
            if int(num_colors_field.get()) < 2:
                tkinter.messagebox.showinfo("Value Warning", "Your Number Of Colors Value Is Too Small]\nMin = 2")
                return
            if int(num_colors_field.get()) > 99:
                tkinter.messagebox.showinfo("Value Warning", "Your Number Of Colors Value Is Too Large]\nMax = 99")
                return
        except ValueError:
            tkinter.messagebox.showinfo("Value Warning", "Your Number Of Colors Value Is Not An Integer")
            return
        num_colors = int(num_colors_field.get())
        # Generates a random hex color if my presets have run out
        if num_colors > len(color_hex_values):
            for i in range(len(color_hex_values), num_colors):
                color_hex_values.append('#%02X%02X%02X' % (rand_rgb(), rand_rgb(), rand_rgb()))
        # deletes all the ant_buttons and then recalls the function that makes them
        for i in range(0, len(color_buttons)):
            color_direction_button[i].destroy()
            color_buttons[i].destroy()
        color_buttons = []
        color_direction_button = []
        setup_colors()

    # Opens up the color picker menu so you can customize it to your own desire
    def color_left_click(x):
        global color_hex_values, color_buttons
        color = askcolor()
        color_buttons[x].config(bg=color[1], fg='red')
        if color[1] is not None:
            color_hex_values[x] = color[1]

    # What happens if you left click on the ant_buttons - it sets up where an ant will start
    def ant_left_click(x, y):
        global ant_buttons
        if ant_buttons[x][y]["text"] != " ":
            ant_buttons[x][y].config(bg='light gray', disabledforeground='black')
            ant_buttons[x][y]["text"] = " "
        else:
            ant_buttons[x][y]["text"] = "▲"
            ant_buttons[x][y].config(bg='red', disabledforeground='black')

    # What happens on a right click, if the button is an ant it changes its starting direction
    def ant_right_click(x, y):
        global ant_buttons
        if ant_buttons[x][y]["text"] == "▲":
            ant_buttons[x][y]["text"] = "▶"
        elif ant_buttons[x][y]["text"] == "▶":
            ant_buttons[x][y]["text"] = "▼"
        elif ant_buttons[x][y]["text"] == "▼":
            ant_buttons[x][y]["text"] = "◀"
        elif ant_buttons[x][y]["text"] == "◀":
            ant_buttons[x][y]["text"] = "▲"

    ##############################################################################################
    ##############################################################################################
    ##############################################################################################

    # Entry Field For Number of Colors with button to change the window
    tkinter.Label(window, text="Number Of Colors :").grid(row=curr_row, column=10)
    num_colors_field = tkinter.Entry(window)
    num_colors_field.grid(row=curr_row, column=11, padx=5)
    num_colors_field.configure(width=5)
    tkinter.Button(window, text="Change", bg='light gray',
                   command=lambda: change_num_colors()).grid(row=curr_row, column=12, padx=5)

    curr_row += 1

    # Entry Field For Number of Steps
    tkinter.Label(window, text="Number Of Steps :").grid(row=curr_row, column=10)
    steps_input = tkinter.Entry(window)
    steps_input.grid(row=curr_row, column=11, columnspan=2)
    steps_input.configure(width=20)

    curr_row += 1

    # Gif length frames
    Label(window, text="Gif Length :").grid(row=curr_row, column=10, padx=5, sticky="W", columnspan=1)
    gif_length_input = tkinter.Entry(window)
    gif_length_input.grid(row=curr_row, column=10, padx=75, columnspan=3, sticky="W")
    gif_length_input.configure(width=10)

    # Logarithmic Scaling Checkbox
    log_check = BooleanVar()
    log_box = Checkbutton(window, text="Log Scale", variable=log_check)
    log_box.grid(row=curr_row, column=10, sticky="W", padx=160, columnspan=10)

    curr_row += 1

    # Gif File Saver and Button
    Label(window, text="Gif File Export Location").grid(row=curr_row, column=10)
    gif_file_button = Button(window, background='light gray', command=gif_file_input_callback)
    # gif_file_button = Button(window, command=gif_file_input_callback)
    gif_file_button.grid(row=curr_row, column=11, columnspan=2)

    curr_row += 1

    # Grid Size Input Fields
    tkinter.Label(window, text="Grid Size").grid(row=curr_row, column=10, padx=5, columnspan=2, sticky="W")
    Label(window, text="X :").grid(row=curr_row, column=10, padx=60, sticky="W", columnspan=3)
    width_input = tkinter.Entry(window)
    width_input.grid(row=curr_row, column=10, padx=82, columnspan=3, sticky="W")
    width_input.configure(width=10)
    Label(window, text="Y :").grid(row=curr_row, column=11, padx=25,  sticky="W", columnspan=2)
    height_input = tkinter.Entry(window)
    height_input.grid(row=curr_row, column=11, padx=12, ipadx=00, columnspan=5)
    height_input.configure(width=10)

    curr_row += 1

    # Start Button and placement
    start_button = tkinter.Button(window, text="Start", bg='light gray', command=lambda: start())
    start_button.grid(row=7, column=10, padx=5, columnspan=5)
    start_button.config(width=30)

    # Ant grid for placements
    for row in range(0, 9):
        ant_buttons.append([])
        for col in range(0, 9):
            # val is used as a spacer to keep things aligned with the rest of the program
            val = 0
            b = tkinter.Button(window, text=" ", width=2, command=lambda x=row, y=col: ant_left_click(x, y))
            b.config(bg='light gray')
            # binds the right mouse click to an action
            b.bind("<Button-3>", lambda e, x=row, y=col: ant_right_click(x, y))
            if col > num_colors:
                val = 3
            b.grid(row=row, column=col, ipadx=2, ipady=val, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
            ant_buttons[row].append(b)
    create_menu()
    setup_colors()
    restore()
