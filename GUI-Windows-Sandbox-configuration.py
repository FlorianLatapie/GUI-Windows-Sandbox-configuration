import webbrowser
from tkinter import Tk, Label, Button, messagebox, StringVar, Radiobutton, Text, filedialog

# Constants
padding_x = 0
padding_y = 5

inner_padding_x = 0
inner_padding_y = 0

left_column_number = 3
right_column_number = 3
total_columns = left_column_number + right_column_number

bold_font = ("Segoe UI", 12, "bold")

# Variables
options = dict()
host_folder = ""


# Methods
def ask_for_host_folder():
    folder = filedialog.askdirectory()

    label_host_folder.config(text=folder)

    global host_folder
    host_folder = folder


def del_host_folder():
    label_host_folder.config(text="Please select a host folder")

    global host_folder
    host_folder = ""


def open_in_web_browser(link):
    webbrowser.open(link)


def assign_value(key, value):
    if not value:
        if key in options:
            del options[key]
        return

    if value == "Default":
        if key in options:
            del options[key]
        return

    options[key] = value


def save_options():
    command = entry_LogonCommand.get("1.0", "end-1c")
    if command == "" and "LogonCommand" in options:
        del options["LogonCommand"]
    elif command != "":
        assign_value("LogonCommand", {"Command": entry_LogonCommand.get("1.0", "end-1c")})

    assign_value("MemoryInMB",
                 get_int_or_error_box(entry_Memory.get("1.0", "end-1c"), "Please enter a valid number for the memory"))

    if host_folder == "" and "MappedFolders" in options:
        del options["MappedFolders"]
    elif host_folder != "":
        assign_value("MappedFolders", {
            "MappedFolder": {
                "HostFolder": host_folder,
                "SandboxFolder": "C:\\Users\\WDAGUtilityAccount\\Desktop\\SharedFolder",
                "ReadOnly": "true"
            }
        })
    print(options)
    save_options_to_file()


def save_options_to_file():
    with open("start Windows Sandbox.wsb", "w") as f:
        f.write("<Configuration>\n")
        for key, value in options.items():
            if type(value) is dict:
                f.write(f"\t<{key}>\n")
                for sub_key, sub_value in value.items():
                    if type(sub_value) is dict:
                        f.write(f"\t\t<{sub_key}>\n")
                        for sub_sub_key, sub_sub_value in sub_value.items():
                            f.write(f"\t\t\t<{sub_sub_key}>{sub_sub_value}</{sub_sub_key}>\n")
                        f.write(f"\t\t</{sub_key}>\n")
                    else:
                        f.write(f"\t\t<{sub_key}>{sub_value}</{sub_key}>\n")
                f.write(f"\t</{key}>\n")
            else:
                f.write(f"\t<{key}>{value}</{key}>\n")
        f.write("</Configuration>\n")
    # messagebox.showinfo("Information", "Options saved")


def get_int_or_error_box(value, error_message="Invalid input"):
    if not value:
        return ""
    try:
        return int(value)
    except ValueError:
        messagebox.showinfo("Error", error_message)
        return ""


# Create a window
root = Tk()
root.title("GUI Windows Sandbox configuration")

label_title = Label(root, text="GUI Windows Sandbox configuration", font=bold_font)
label_title.grid(row=0, column=0, columnspan=total_columns, padx=10, pady=10)

button_Source = Button(
    root,
    text="Microsoft documentation",
    command=lambda: open_in_web_browser(
        "https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-sandbox/windows-sandbox-configure-using-wsb-file"
    )
)
button_Source.grid(row=1, column=0, columnspan=total_columns, padx=padding_x, pady=padding_y)

# Main content

# vGPU
label_vGPU = Label(root, text="vGPU", font=bold_font)
label_vGPU.grid(row=2, column=0, columnspan=left_column_number, padx=padding_x, pady=padding_y)
vGPU_vals = ["Default", "Enable", "Disable"]
vGPU_val = StringVar()
vGPU_val.set(vGPU_vals[0])
assign_value("vGPU", vGPU_val.get())

for i in range(len(vGPU_vals)):
    Radiobutton_vGPU_Enable = Radiobutton(
        root,
        text=vGPU_vals[i],
        variable=vGPU_val,
        value=vGPU_vals[i],
        command=lambda: assign_value("vGPU", vGPU_val.get())
    )
    Radiobutton_vGPU_Enable.grid(row=3, column=i, padx=inner_padding_x, pady=inner_padding_y)

# Networking
label_Networking = Label(root, text="Networking", font=bold_font)
label_Networking.grid(row=4, column=0, columnspan=left_column_number, padx=padding_x, pady=padding_y)
Networking_vals = ["Default", "Disable"]
Networking_val = StringVar()
Networking_val.set(Networking_vals[0])
assign_value("Networking", Networking_val.get())

for i in range(len(Networking_vals)):
    Radiobutton_Networking_Enable = Radiobutton(
        root,
        text=Networking_vals[i],
        variable=Networking_val,
        value=Networking_vals[i],
        command=lambda: assign_value("Networking", Networking_val.get())
    )
    Radiobutton_Networking_Enable.grid(row=5, column=i, padx=inner_padding_x, pady=inner_padding_y)

# Mapped folders
"""
datastructure : 
<MappedFolders>
    <MappedFolder>
        <HostFolder>C:\\Users\\Public\\Downloads</HostFolder>
        <SandboxFolder>C:\\Users\\WDAGUtilityAccount\\Downloads</SandboxFolder>
        <ReadOnly>true</ReadOnly>
    </MappedFolder>
<MappedFolder>
"""

label_MappedFolders = Label(root, text="Mapped folders", font=bold_font)
label_MappedFolders.grid(row=6, column=left_column_number, columnspan=right_column_number, padx=padding_x,
                         pady=padding_y)

label_host_folder_title = Label(root, text="Host folder:")
label_host_folder_title.grid(row=7, column=left_column_number, columnspan=right_column_number, padx=padding_x,
                             pady=padding_y)

label_host_folder = Label(root, text="Please select a host folder")
label_host_folder.grid(row=8, column=left_column_number, columnspan=right_column_number, padx=padding_x, pady=padding_y)

button_host_folder = Button(root, text="Select", command=ask_for_host_folder)
button_host_folder.grid(row=9, column=left_column_number, padx=padding_x, pady=padding_y)

button_del_host_folder = Button(root, text="Delete", command=del_host_folder)
button_del_host_folder.grid(row=9, column=total_columns - 1, padx=padding_x, pady=padding_y)

# Logon command
label_LogonCommand = Label(root, text="Logon command", font=bold_font)
label_LogonCommand.grid(row=2, column=left_column_number, columnspan=right_column_number, padx=padding_x,
                        pady=padding_y)

entry_LogonCommand = Text(root, width=25, height=1)
entry_LogonCommand.grid(row=3, column=left_column_number, columnspan=right_column_number, padx=padding_x,
                        pady=padding_y)

# Audio input
label_AudioInput = Label(root, text="Audio input", font=bold_font)
label_AudioInput.grid(row=6, column=0, columnspan=left_column_number, padx=padding_x, pady=padding_y)
AudioInput_vals = ["Default", "Enable", "Disable"]
AudioInput_val = StringVar()
AudioInput_val.set(AudioInput_vals[0])
assign_value("AudioInput", AudioInput_val.get())

for i in range(len(AudioInput_vals)):
    Radiobutton_AudioInput_Enable = Radiobutton(
        root,
        text=AudioInput_vals[i],
        variable=AudioInput_val,
        value=AudioInput_vals[i],
        command=lambda: assign_value("AudioInput", AudioInput_val.get())
    )
    Radiobutton_AudioInput_Enable.grid(row=7, column=i, padx=inner_padding_x, pady=inner_padding_y)

# Video input
label_VideoInput = Label(root, text="Video input", font=bold_font)
label_VideoInput.grid(row=8, column=0, columnspan=left_column_number, padx=padding_x, pady=padding_y)
VideoInput_vals = ["Default", "Enable", "Disable"]
VideoInput_val = StringVar()
VideoInput_val.set(VideoInput_vals[0])
assign_value("VideoInput", VideoInput_val.get())

for i in range(len(VideoInput_vals)):
    Radiobutton_VideoInput_Enable = Radiobutton(
        root,
        text=VideoInput_vals[i],
        variable=VideoInput_val,
        value=VideoInput_vals[i],
        command=lambda: assign_value("VideoInput", VideoInput_val.get())
    )
    Radiobutton_VideoInput_Enable.grid(row=9, column=i, padx=inner_padding_x, pady=inner_padding_y)

# Protected client
label_ProtectedClient = Label(root, text="Protected client", font=bold_font)
label_ProtectedClient.grid(row=12, column=0, columnspan=left_column_number, padx=padding_x, pady=padding_y)
ProtectedClient_vals = ["Default", "Enable", "Disable"]
ProtectedClient_val = StringVar()
ProtectedClient_val.set(ProtectedClient_vals[0])

for i in range(len(ProtectedClient_vals)):
    Radiobutton_ProtectedClient_Enable = Radiobutton(
        root,
        text=ProtectedClient_vals[i],
        variable=ProtectedClient_val,
        value=ProtectedClient_vals[i],
        command=lambda: assign_value("ProtectedClient", ProtectedClient_val.get())
    )
    Radiobutton_ProtectedClient_Enable.grid(row=13, column=i, padx=inner_padding_x, pady=inner_padding_y)

# Printer redirection
label_PrinterRedirection = Label(root, text="Printer redirection", font=bold_font)
label_PrinterRedirection.grid(row=14, column=0, columnspan=left_column_number, padx=padding_x, pady=padding_y)
PrinterRedirection_vals = ["Default", "Enable", "Disable"]
PrinterRedirection_val = StringVar()
PrinterRedirection_val.set(PrinterRedirection_vals[0])

for i in range(len(PrinterRedirection_vals)):
    Radiobutton_PrinterRedirection_Enable = Radiobutton(
        root,
        text=PrinterRedirection_vals[i],
        variable=PrinterRedirection_val,
        value=PrinterRedirection_vals[i],
        command=lambda: assign_value("PrinterRedirection", PrinterRedirection_val.get())
    )
    Radiobutton_PrinterRedirection_Enable.grid(row=15, column=i, padx=inner_padding_x, pady=inner_padding_y)

# Clipboard redirection
label_ClipboardRedirection = Label(root, text="Clipboard redirection", font=bold_font)
label_ClipboardRedirection.grid(row=16, column=0, columnspan=left_column_number, padx=padding_x, pady=padding_y)
ClipboardRedirection_vals = ["Default", "Enable", "Disable"]
ClipboardRedirection_val = StringVar()
ClipboardRedirection_val.set(ClipboardRedirection_vals[0])

for i in range(len(ClipboardRedirection_vals)):
    Radiobutton_ClipboardRedirection_Enable = Radiobutton(
        root,
        text=ClipboardRedirection_vals[i],
        variable=ClipboardRedirection_val,
        value=ClipboardRedirection_vals[i],
        command=lambda: assign_value("ClipboardRedirection", ClipboardRedirection_val.get())
    )
    Radiobutton_ClipboardRedirection_Enable.grid(row=17, column=i, padx=inner_padding_x, pady=inner_padding_y)

# Memory in MB
label_Memory = Label(root, text="Memory in MB", font=bold_font)
label_Memory.grid(row=4, column=left_column_number, columnspan=right_column_number, padx=padding_x, pady=padding_y)
entry_Memory = Text(root, width=25, height=1)
entry_Memory.grid(row=5, column=left_column_number, columnspan=right_column_number, padx=padding_x, pady=padding_y)

# Buttons on the bottom
button_save = Button(root, text="Save", command=lambda: save_options())
button_save.grid(row=40, column=0, padx=padding_x, pady=padding_y)
button_quit = Button(root, text="Quit", command=root.destroy)
button_quit.grid(row=40, column=total_columns - 1, padx=padding_x, pady=padding_y + padding_y)

root.mainloop()
