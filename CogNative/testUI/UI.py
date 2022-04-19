from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory, askopenfile
from time import sleep
import subprocess
import threading
from pathlib import Path

from ..models.RTVC.utils.printing import colorize
from colorama import Fore

ws = Tk()
ws.title("CogNative")
ws.geometry("1000x600")

data = {
    "input": {
        "audio_to_clone": None,
        "use_embedding": None,
    },
    "text": {
        "audio_to_transcribe": None,
        "text": None,
    },
    "output": {
        "output_audio_path": None,
        "output_dir": ""
    },
}

output_dir = ""

# Variable tracks whether the program is currently
# running a clone process
global run_lock
run_lock = False

def open_file(file_type, file_name):
    data[file_type][file_name] = askopenfile(
        mode="r", filetypes=[("Audio Files", "*wav"), ("Text Files", "*txt")]
    ).name

    if file_name == "audio_to_clone":
        audio_path_lbl.config(text=data[file_type][file_name])
    elif file_name == "audio_to_transcribe":
        data["text"]["text"] = None
        if Path(data[file_type][file_name]).suffix == ".txt":
            with open(data[file_type][file_name]) as f:
                lines = f.readlines()
            text_from_file = ' '.join(lines)
            data["text"]["text"] = text_from_file
            data[file_type][file_name] = None
        
        if data[file_type][file_name]:
            text_to_syn_lbl.config(text=data[file_type][file_name])
        elif file_name == "audio_to_transcribe" and not data[file_type][file_name]:
            len_data = len(data["text"]["text"])
            n_chars = 80 if len_data > 80 else len_data
            text_to_display = data["text"]["text"][:n_chars]
            if n_chars == 80:
                text_to_display += "..."
            text_to_syn_lbl.config(text=text_to_display)


def save_path(file_type, file_name):
    data[file_type][file_name] = askdirectory()

    # Set output file path
    output_dir = data["output"]["output_dir"]
    output_dir_lbl.config(text=f"{output_dir}/{output_name_entry.get()}")


def buttonHandle():
    cloneVoice()


def displayProgressBar():
    pb1 = Progressbar(ws, orient=HORIZONTAL, length=300, mode="determinate")
    pb1.grid(row=8, columnspan=3, pady=20)
    for i in range(5):
        ws.update_idletasks()
        pb1["value"] += 20
        sleep(0.25)
    pb1.destroy()


def cloneVoice():
    data["input"]["use_embedding"] = embed_check.get()

    text_in_entry = text_synthesize_entry.get()
    if text_in_entry:
        data["text"]["text"] = text_in_entry

    output_dir = data["output"]["output_dir"]
    data["output"]["output_audio_path"] = f"{output_dir}/{output_name_entry.get()}"
    output_dir_lbl.config(text=data["output"]["output_audio_path"])

    embedding_check = 'y' if data["input"]["use_embedding"] else 'n'

    cmd = ['python', '-m', 'CogNative.main',
           '-sampleAudio', data["input"]["audio_to_clone"],
           '-out', data["output"]["output_audio_path"],
           '-useExistingEmbed', embedding_check
           ]
    
    if data["text"]["audio_to_transcribe"]:
        cmd.append('-dialogueAudio')
        cmd.append(data["text"]["audio_to_transcribe"])
        cmd.append('-synType')
        cmd.append('audio')
    elif data["text"]["text"]:
        cmd.append('-dialogueText')
        cmd.append(f'"{data["text"]["text"]}"')
        cmd.append('-synType')
        cmd.append('text')
    else:
        print(colorize("Missing text to synthesize.", "error"))
        raise Exception("Must enter text or audio to be synthesized.")

    def run_main():
        global run_lock
        if not run_lock:
            run_lock = True
            try:
                print("=============================================")
                print(' '.join(cmd))
                print("=============================================")

                # Set status label
                status_lbl = Label(ws, text="Cloning voice...").grid(
                    row=8, columnspan=3, pady=10
                )
            except Exception:
                run_lock = False
                print(colorize("Missing input.", "error"))
            
            try:
                # Run the command to clone
                process = subprocess.run(cmd, capture_output=True)
            except Exception:
                run_lock = False
                print(colorize("Error in main.", "error"))
                raise Exception

            try:
                # Collect info on subprocess
                stdout = process.stdout

                # Get the last line of the output
                output = stdout.decode('utf-8').split('\n')[-2]

                # Strip Fore colors off of the printed output
                # IF the Fore information is contained in the output
                if Fore.LIGHTGREEN_EX in output:
                    color = "green"
                    output = output.split(Fore.LIGHTGREEN_EX)[1]
                elif Fore.RED in output:
                    color = "red"
                    output = output.split(Fore.RED)[1]
                elif Fore.YELLOW in output:
                    color = "yellow"
                    output = output.split(Fore.YELLOW)[1]
                elif Fore.CYAN in output:
                    color = "blue"
                    output = output.split(Fore.CYAN)[1]
                else:
                    color = "red"

                # If there is a Fore.RESET, strip it off too
                if Fore.RESET in output:
                    output = output.split(Fore.RESET)[0]

                # Set status label to output
                status_lbl = Label(ws, text=output, foreground=color).grid(
                    row=8, columnspan=3, pady=10
                )
                print(f"last line of output: {output}")
            except Exception:
                run_lock = False
                print(colorize("Error while processing stdout.", "error"))
                raise Exception

            run_lock = False
        else:
            locked_error = "ERROR: Another voice is already being cloned right now."
            print(colorize(locked_error, "error"))

    thr = threading.Thread(target=run_main)
    thr.daemon = True # close pipe if GUI exits
    # Run main, given the user inputs
    thr.start()

# ----- ROW 0 ----- #
input_audio_lbl = Label(ws, text="Select voice to clone:")
input_audio_lbl.grid(row=0, column=0, padx=10, pady=20)

input_audio_btn = Button(
    ws, text="Choose File", command=lambda: open_file("input", "audio_to_clone")
)
input_audio_btn.grid(row=0, column=1, pady=20)

embed_check = IntVar()
embed_check_box = Checkbutton(
    ws,
    text="Use saved embedding?",
    variable=embed_check,
    onvalue=1,
    offvalue=0,
)
embed_check_box.grid(row=0, column=2, pady=20)

# ----- ROW 1 ----- #
audio_selected_lbl = Label(ws, text="Voice to clone:")
audio_selected_lbl.grid(row=1, column=0, padx=10, pady=5)

audio_path_lbl = Label(ws, text="^^^ Select audio file ^^^")
audio_path_lbl.grid(row=1, column=1, columnspan=2, padx=20, pady=20)

# ----- ROW 2 ----- #
text_lang_lbl = Label(ws, text="Text to synthesize:")
text_lang_lbl.grid(row=2, column=0, padx=10)

text_synthesize_entry = Entry(ws)
text_synthesize_entry.grid(row=2, column=1, columnspan=2, pady=20, ipadx=100)

audio_to_transcribe_lbl = Label(ws, text="OR")
audio_to_transcribe_lbl.grid(row=2, column=3, padx=15, pady=20)

audio_to_transcribe_btn = Button(
    ws, text="Choose *.wav or *.txt", command=lambda: open_file("text", "audio_to_transcribe")
)
audio_to_transcribe_btn.grid(row=2, column=5, pady=20)

# ----- ROW 3 ----- #
text_to_syn_intro = Label(ws, text="Text being synthesized:")
text_to_syn_intro.grid(row=3, column=0, padx=10, pady=5)

text_to_syn_lbl = Label(ws, text="^^^ Enter text   OR   select a .wav or .txt file ^^^")
text_to_syn_lbl.grid(row=3, column=1, columnspan=2, padx=20, pady=20)

# ----- ROW 4 ----- #
output_path_lbl = Label(ws, text="Output file name:")
output_path_lbl.grid(row=4, column=0, padx=10, pady=20)

output_name_entry = Entry(ws)
output_name_entry.grid(row=4, column=1, pady=20)

output_path_lbl = Label(ws, text="Select output path:")
output_path_lbl.grid(row=4, column=2, padx=10, pady=20)

output_path_btn = Button(
    ws,
    text="Choose Directory",
    command=lambda: save_path("output", "output_dir"),
)
output_path_btn.grid(row=4, column=3, pady=20)

# ----- ROW 5 ----- #
output_selected_lbl = Label(ws, text="Output path:")
output_selected_lbl.grid(row=5, column=0, padx=10, pady=5)

output_dir_lbl = Label(ws, text="")
output_dir_lbl.grid(row=5, column=1, columnspan=2, padx=20, pady=20)

# ----- ROW 6 ----- #
upld = Button(ws, text="Clone voice", command=buttonHandle)
upld.grid(row=6, columnspan=3, pady=20, padx=20, ipadx=25, ipady=12)

# ----- ROW 8 ----- #
status_lbl = Label(ws, text="").grid(
    row=8, columnspan=3, pady=10
)

ws.mainloop()
