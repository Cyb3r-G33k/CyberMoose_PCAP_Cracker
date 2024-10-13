import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
import threading
import os
import itertools


def select_file(entry_widget):
    """Function to select a .pcap or .cap file."""
    filename = filedialog.askopenfilename(filetypes=[("Capture Files", "*.pcap *.cap")])
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, filename)


def select_wordlist(entry_widget):
    """Function to select a wordlist file."""
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, filename)


def ask_save_location():
    """Function to ask the user where to save the generated wordlist or output."""
    save_location = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    return save_location


def generate_wordlist(min_len, max_len, charset, output_file, progress_label):
    """Function to generate a wordlist using crunch."""
    try:
        progress_label.config(text="Generating wordlist using crunch...")
        crunch_command = [
            'crunch', min_len, max_len, charset, '-o', output_file
        ]
        process = subprocess.Popen(crunch_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate()  # Wait for crunch to finish

        if process.returncode == 0:
            messagebox.showinfo("Success", f"Wordlist generated successfully: {output_file}")
        else:
            raise Exception("Crunch failed to generate wordlist")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def generate_social_engineered_wordlist(answers, output_file, progress_label):
    """Generate a wordlist using social engineering answers."""
    try:
        progress_label.config(text="Generating social-engineered wordlist...")

        # Create combinations of the answers
        combinations = []
        for length in range(1, len(answers) + 1):
            combinations.extend(itertools.permutations(answers, length))

        # Flatten and write to the wordlist file
        with open(output_file, 'w') as f:
            for combo in combinations:
                f.write(''.join(combo) + '\n')

        progress_label.config(text="Wordlist generation completed")
        messagebox.showinfo("Success", f"Social-engineered wordlist generated successfully: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


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


def brute_force_cracking(pcap_file, output_file, progress_label):
    """Perform brute force cracking using hashcat without creating a wordlist."""
    try:
        # Check if the file is either .pcap or .cap
        if pcap_file.endswith('.pcap') or pcap_file.endswith('.cap'):
            progress_label.config(text="Converting capture file to .hccapx...")
            conversion_command = f"aircrack-ng {pcap_file} -J output"
            os.system(conversion_command)

        # Check for available GPU (NVIDIA/AMD) or fallback to CPU
        gpu_flag = check_gpu()

        # Prepare hashcat brute force command
        progress_label.config(text="Starting brute force cracking...")
        crack_command = [
            'hashcat',
            '-m', '2500',  # WPA/WPA2 hash type
            'output.hccapx',  # Input file after conversion
            '-a', '3',  # Brute force attack mode
            '?a?a?a?a?a?a?a?a',  # Mask for brute force (8 characters in this case, adjustable)
            gpu_flag,  # Use GPU if available, otherwise CPU
            '--outfile', output_file  # Output file for cracked password
        ]

        # Run hashcat and capture output including hash rate
        process = subprocess.Popen(crack_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        hash_rate = None

        for line in process.stdout:
            decoded_line = line.decode('utf-8')
            progress_label.config(text=decoded_line)

            if "H/s" in decoded_line:  # Look for the hash rate in the output
                hash_rate = decoded_line.strip()

        if hash_rate:
            messagebox.showinfo("Hash Rate", f"Current hash rate: {hash_rate}")
        else:
            messagebox.showinfo("Hash Rate", "Unable to retrieve hash rate.")

        messagebox.showinfo("Success", f"Brute force finished! Check the results in {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def crack_handshake(pcap_file, wordlist, output_file, progress_label):
    """Function to run the cracking process using hashcat and display hash rate."""
    try:
        # Check if the file is either .pcap or .cap
        if pcap_file.endswith('.pcap') or pcap_file.endswith('.cap'):
            progress_label.config(text="Converting capture file to .hccapx...")
            conversion_command = f"aircrack-ng {pcap_file} -J output"
            os.system(conversion_command)

        # Check for available GPU (NVIDIA/AMD) or fallback to CPU
        gpu_flag = check_gpu()

        # Prepare hashcat command
        progress_label.config(text="Starting the cracking process...")
        crack_command = [
            'hashcat',
            '-m', '2500',  # WPA/WPA2 hash type
            'output.hccapx',  # Input file after conversion
            wordlist,
            gpu_flag,  # Use GPU if available, otherwise CPU
            '--status',  # Show status and progress
            '--outfile', output_file  # Output file for cracked passwords
        ]

        # Run hashcat and capture output including hash rate
        process = subprocess.Popen(crack_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        hash_rate = None

        for line in process.stdout:
            decoded_line = line.decode('utf-8')
            progress_label.config(text=decoded_line)

            if "H/s" in decoded_line:  # Look for the hash rate in the output
                hash_rate = decoded_line.strip()

        if hash_rate:
            messagebox.showinfo("Hash Rate", f"Current hash rate: {hash_rate}")
        else:
            messagebox.showinfo("Hash Rate", "Unable to retrieve hash rate.")

        messagebox.showinfo("Success", f"Cracking finished! Check the results in {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def start_cracking(pcap_file, wordlist, output_file, progress_label, brute_force_var):
    """Start the cracking process in a separate thread to keep UI responsive."""
    if brute_force_var.get():
        # If brute force is selected, run brute force mode
        threading.Thread(target=brute_force_cracking, args=(pcap_file, output_file, progress_label)).start()
    else:
        threading.Thread(target=crack_handshake, args=(pcap_file, wordlist, output_file, progress_label)).start()


def start_wordlist_generation(min_len, max_len, charset, progress_label, special_chars_var):
    """Start the wordlist generation in a separate thread."""
    if special_chars_var.get():
        charset += '!@#$%^&*()-_=+[]{}|;:<>,.?/'  # Add special characters if checkbox is checked

    output_file = ask_save_location()  # Ask where to save the wordlist
    if output_file:
        threading.Thread(target=generate_wordlist, args=(min_len, max_len, charset, output_file, progress_label)).start()
    else:
        messagebox.showwarning("No file selected", "You need to select a location to save the wordlist!")


def start_social_engineered_wordlist_generation(progress_label):
    """Collect social engineering info and start the wordlist generation."""
    # Pop-up dialogs to collect data for both individuals and companies
    name = simpledialog.askstring("Input", "Enter the target's name (or company name):")
    birth_year = simpledialog.askstring("Input", "Enter the birth year (or year of establishment):")
    favorite_color = simpledialog.askstring("Input", "Enter the target's favorite color (or company color theme):")
    pet_name = simpledialog.askstring("Input", "Enter the target's pet's name (or company mascot):")

    # Collect the answers
    answers = [name, birth_year, favorite_color, pet_name]

    # Ask where to save the wordlist
    output_file = ask_save_location()
    if output_file:
        threading.Thread(target=generate_social_engineered_wordlist, args=(answers, output_file, progress_label)).start()
    else:
        messagebox.showwarning("No file selected", "You need to select a location to save the wordlist!")


def toggle_charset_entry(special_chars_var, charset_entry):
    """Enable/Disable character set entry based on special characters checkbox."""
    if special_chars_var.get():
        charset_entry.delete(0, tk.END)
        charset_entry.insert(0, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+[]{}|;:<>,.?/')
        charset_entry.config(state='disabled')  # Disable manual editing
    else:
        charset_entry.config(state='normal')  # Enable manual editing


def toggle_social_engineering_options(social_engineering_var, progress_label):
    """Toggle between standard wordlist generation and social-engineered wordlist."""
    if social_engineering_var.get():
        start_social_engineered_wordlist_generation(progress_label)


# Build the UI
def build_ui():
    root = tk.Tk()
    root.title("Wi-Fi Cracker")

    # PCAP file selection
    pcap_label = tk.Label(root, text="Select PCAP or CAP file:")
    pcap_label.grid(row=0, column=0, padx=10, pady=10)
    pcap_entry = tk.Entry(root, width=50)
    pcap_entry.grid(row=0, column=1, padx=10, pady=10)
    pcap_button = tk.Button(root, text="Browse", command=lambda: select_file(pcap_entry))
    pcap_button.grid(row=0, column=2, padx=10, pady=10)

    # Wordlist selection or generation options
    wordlist_label = tk.Label(root, text="Select Wordlist (or leave empty to generate one):")
    wordlist_label.grid(row=1, column=0, padx=10, pady=10)
    wordlist_entry = tk.Entry(root, width=50)
    wordlist_entry.grid(row=1, column=1, padx=10, pady=10)
    wordlist_button = tk.Button(root, text="Browse", command=lambda: select_wordlist(wordlist_entry))
    wordlist_button.grid(row=1, column=2, padx=10, pady=10)

    # Wordlist generation options
    min_len_label = tk.Label(root, text="Min length:")
    min_len_label.grid(row=2, column=0, padx=10, pady=10)
    min_len_entry = tk.Entry(root)
    min_len_entry.grid(row=2, column=1, padx=10, pady=10)

    max_len_label = tk.Label(root, text="Max length:")
    max_len_label.grid(row=3, column=0, padx=10, pady=10)
    max_len_entry = tk.Entry(root)
    max_len_entry.grid(row=3, column=1, padx=10, pady=10)

    charset_label = tk.Label(root, text="Character set:")
    charset_label.grid(row=4, column=0, padx=10, pady=10)
    charset_entry = tk.Entry(root, width=50)
    charset_entry.grid(row=4, column=1, padx=10, pady=10)

    # Checkbox for adding special characters
    special_chars_var = tk.BooleanVar()
    special_chars_checkbox = tk.Checkbutton(root, text="Add special characters", variable=special_chars_var,
                                            command=lambda: toggle_charset_entry(special_chars_var, charset_entry))
    special_chars_checkbox.grid(row=5, column=1, padx=10, pady=10)

    # Checkbox for using social engineering
    social_engineering_var = tk.BooleanVar()
    social_engineering_checkbox = tk.Checkbutton(root, text="Use social engineering", variable=social_engineering_var,
                                                 command=lambda: toggle_social_engineering_options(social_engineering_var, progress_label))
    social_engineering_checkbox.grid(row=6, column=1, padx=10, pady=10)

    # Checkbox for brute force attack
    brute_force_var = tk.BooleanVar()
    brute_force_checkbox = tk.Checkbutton(root, text="Brute force attack (without wordlist)", variable=brute_force_var)
    brute_force_checkbox.grid(row=7, column=1, padx=10, pady=10)

    # Progress label
    progress_label = tk.Label(root, text="Progress: Waiting...")
    progress_label.grid(row=8, column=1, padx=10, pady=10)

    # Start cracking button
    start_button = tk.Button(root, text="Start Crack",
                             command=lambda: start_cracking(pcap_entry.get(),
                                                            wordlist_entry.get() or ask_save_location(),
                                                            "cracked_password.txt", progress_label, brute_force_var))
    start_button.grid(row=9, column=1, padx=10, pady=10)

    root.mainloop()


# Run the UI
if __name__ == "__main__":
    build_ui()
