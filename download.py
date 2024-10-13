import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
import os


def select_file(entry_widget):
    """Function to select a .hccapx file."""
    filename = filedialog.askopenfilename(filetypes=[("HCCAPX Files", "*.hccapx")])
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, filename)


def select_wordlist(entry_widget):
    """Function to select a wordlist file."""
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, filename)


def ask_save_location():
    """Function to ask the user where to save the cracked passwords."""
    save_location = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    return save_location


def check_gpu():
    """Function to check for available GPUs (NVIDIA/AMD) and fallback to CPU if none found."""
    try:
        # Check for NVIDIA or AMD GPU
        result = subprocess.run(['hashcat', '-I'], capture_output=True, text=True)
        if 'NVIDIA' in result.stdout or 'AMD' in result.stdout:
            return '--force'  # Force hashcat to use GPU
        else:
            return '--opencl-device-types=1'  # Fallback to CPU
    except Exception:
        return '--opencl-device-types=1'  # Fallback to CPU if anything goes wrong


def crack_handshake(hccapx_file, wordlist, output_file, progress_label):
    """Function to run the cracking process using hashcat and display hash rate."""
    try:
        # Check for available GPU (NVIDIA/AMD) or fallback to CPU
        gpu_flag = check_gpu()

        # Prepare hashcat command
        progress_label.config(text="Starting the cracking process...")
        crack_command = [
            'hashcat',
            '-m', '2500',  # WPA/WPA2 hash type
            hccapx_file,  # Input file in hccapx format
            wordlist,
            gpu_flag,  # Use GPU if available, otherwise CPU
            '--status',  # Show status and progress
            '--outfile', output_file  # Output file for cracked passwords
        ]

        # Run hashcat and capture output including hash rate
        process = subprocess.Popen(crack_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in process.stdout:
            decoded_line = line.decode('utf-8')
            progress_label.config(text=decoded_line)

        messagebox.showinfo("Success", f"Cracking finished! Check the results in {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI setup
def build_ui():
    root = tk.Tk()
    root.title("Wi-Fi Cracker")

    # HCCAPX file selection
    hccapx_label = tk.Label(root, text="Select HCCAPX file:")
    hccapx_label.grid(row=0, column=0, padx=10, pady=10)
    hccapx_entry = tk.Entry(root, width=50)
    hccapx_entry.grid(row=0, column=1, padx=10, pady=10)
    hccapx_button = tk.Button(root, text="Browse", command=lambda: select_file(hccapx_entry))
    hccapx_button.grid(row=0, column=2, padx=10, pady=10)

    # Wordlist selection
    wordlist_label = tk.Label(root, text="Select Wordlist (or leave empty to generate one):")
    wordlist_label.grid(row=1, column=0, padx=10, pady=10)
    wordlist_entry = tk.Entry(root, width=50)
    wordlist_entry.grid(row=1, column=1, padx=10, pady=10)
    wordlist_button = tk.Button(root, text="Browse", command=lambda: select_wordlist(wordlist_entry))
    wordlist_button.grid(row=1, column=2, padx=10, pady=10)

    # Start cracking button
    start_button = tk.Button(root, text="Start Crack",
                             command=lambda: crack_handshake(hccapx_entry.get(),
                                                            wordlist_entry.get() or ask_save_location(),
                                                            "cracked_password.txt", hccapx_label))
    start_button.grid(row=2, column=1, padx=10, pady=10)

    root.mainloop()


# Run the UI
if __name__ == "__main__":
    build_ui()
