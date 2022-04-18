from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory, askopenfile
from time import sleep
import subprocess

from ..models.RTVC.RTVC import RTVC
from ..backend.backend import speech_transcription
from colorama import Fore

ws = Tk()
ws.title("CogNative")
ws.geometry("800x400")

data = {
    "input": {
        "src_lang": None,
        "audio_to_clone": None,
        "use_embedding": None,
    },
    "text": {
        "audio_to_transcribe": None,
        "text_lang": None,
        "text": None,
    },
    "output": {
        "output_audio_path": None,
    },
}

# Dropdown menu options
lang_options = [
    "english",  # default option
    "english",
    "spanish",
    "swedish",
    "german",
]


def open_file(file_type, file_name, label=None):
    data[file_type][file_name] = askopenfile(
        mode="r", filetypes=[("Audio Files", "*wav")]
    ).name

    if label:
        label.config(text=data[file_type][file_name])


def save_path(file_type, file_name, label=None):
    data[file_type][file_name] = askdirectory()
    if label:
        label.config(text=data[file_type][file_name])


def buttonHandle():
    cloneVoice(src_lang_var, text_lang_var)


def displayProgressBar():
    pb1 = Progressbar(ws, orient=HORIZONTAL, length=300, mode="determinate")
    pb1.grid(row=8, columnspan=3, pady=20)
    for i in range(5):
        ws.update_idletasks()
        pb1["value"] += 20
        sleep(0.25)
    pb1.destroy()


def cloneVoice(src_lang_var, text_lang_var):
    data["input"]["src_lang"] = src_lang_var.get()
    data["input"]["use_embedding"] = embed_check.get()

    data["text"]["text_lang"] = text_lang_var.get()
    data["text"]["text"] = text_synthesize_entry.get()

    # If the path has been set already because the directory was selected
    if data["output"]["output_audio_path"]:
        data["output"]["output_audio_path"] = (
            data["output"]["output_audio_path"] + "/" + output_name_entry.get()
        )
    # If it hasn't set directory to file name
    else:
        data["output"]["output_audio_path"] = output_name_entry.get()

    displayProgressBar()

    if data["text"]["text"]:
        synType = "text"
    else:
        synType = "audio"

    cmd = ['python', '-m', 'CogNative.main',
           '-lang', data["input"]["src_lang"],
           '-sampleAudio', data["input"]["audio_to_clone"],
           '-synType', synType,
           '-out', data["output"]["output_audio_path"],
           '-useExistingEmbed', 'y'
           ]
    
    if data["text"]["audio_to_transcribe"]:
        cmd.append('-dialogueLang')
        cmd.append(data["text"]["text_lang"])
        cmd.append('-dialogueAudio')
        cmd.append(data["text"]["audio_to_transcribe"])
    else:
        cmd.append('-dialogueText')
        cmd.append(f'"{data["text"]["text"]}"')
    
    print("=============================================")
    print(' '.join(cmd))
    print("=============================================")

    # Run the command to clone
    process = subprocess.run(cmd, capture_output=True)

    # Collect info on subprocess
    stdout = process.stdout
    
    # Get the last line of the output
    output = stdout.decode('utf-8').split('\n')[-2]

    # Error prone way of stripping color (and symbols) off
    # of the ouput and setting the tkinter display color
    # that the label will use
    if "ERROR" in output:
        # Set color to display in UI
        color = "red"
        # Strip Fore colors off of the printed output
        output = output.split(Fore.RED)[1].split(Fore.RESET)[0]
    else:
        # Set color to display in UI
        color = "green"
        # Strip Fore colors off of the printed output
        output = output.split(Fore.LIGHTGREEN_EX)[1].split(Fore.RESET)[0]

    Label(ws, text=output, foreground=color).grid(
        row=8, columnspan=3, pady=10
    )
    print(f"last line of output: {output}")


# ----- ROW 0 ----- #
input_audio_lbl = Label(ws, text="Select voice to clone:")
input_audio_lbl.grid(row=0, column=0, padx=10, pady=20)

input_audio_btn = Button(
    ws, text="Choose File", command=lambda: open_file("input", "audio_to_clone")
)
input_audio_btn.grid(row=0, column=1, pady=20)

# datatype of menu text
src_lang_var = StringVar()

# initial menu text
src_lang_var.set("english")

# Create Dropdown menu
drop = OptionMenu(ws, src_lang_var, *lang_options)
drop.grid(row=0, column=2, pady=20)

embed_check = IntVar()
embed_check_box = Checkbutton(
    ws,
    text="Use saved embedding?",
    variable=embed_check,
    onvalue=1,
    offvalue=0,
)
embed_check_box.grid(row=0, column=3, pady=20)

# ----- ROW 1 ----- #
text_lang_lbl = Label(ws, text="Text to synthesize:")
text_lang_lbl.grid(row=1, column=0, padx=10)

text_synthesize_entry = Entry(ws)
text_synthesize_entry.grid(row=1, column=1, pady=20)

audio_to_transcribe_lbl = Label(ws, text="OR")
audio_to_transcribe_lbl.grid(row=1, column=2, padx=10, pady=20)

audio_to_transcribe_btn = Button(
    ws, text="Choose File", command=lambda: open_file("text", "audio_to_transcribe")
)
audio_to_transcribe_btn.grid(row=1, column=3, pady=20)

# datatype of menu text
text_lang_var = StringVar()

# initial menu text
text_lang_var.set("english")

# Create Dropdown menu
drop = OptionMenu(ws, text_lang_var, *lang_options)
drop.grid(row=1, column=4, pady=20)


# ----- ROW 2 ----- #
output_path_lbl = Label(ws, text="Output file name:")
output_path_lbl.grid(row=2, column=0, padx=10, pady=20)

output_name_entry = Entry(ws)
output_name_entry.grid(row=2, column=1, pady=20)

output_path_lbl = Label(ws, text="Select output path:")
output_path_lbl.grid(row=2, column=2, padx=10, pady=20)

output_path_btn = Button(
    ws,
    text="Choose Directory",
    command=lambda: save_path("output", "output_audio_path", output_dir_lbl),
)
output_path_btn.grid(row=2, column=3, pady=20)

# ----- ROW 3 ----- #
output_selected_lbl = Label(ws, text="Output path:")
output_selected_lbl.grid(row=3, column=0, padx=10, pady=5)

output_dir_lbl = Label(ws, text="")
output_dir_lbl.grid(row=3, column=1, columnspan=2, padx=20, pady=20)

# ----- ROW 4 ----- #
upld = Button(ws, text="Clone voice", command=buttonHandle)
upld.grid(row=4, columnspan=3, pady=20, padx=20)

ws.mainloop()
