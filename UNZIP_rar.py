import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import rarfile

class RarExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RAR Extractor Pro")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.rar_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.password = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="RAR Extractor", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)

        # RAR file selection
        frame1 = tk.Frame(self.root)
        frame1.pack(pady=5, fill="x", padx=20)

        tk.Label(frame1, text="RAR File:").pack(anchor="w")
        tk.Entry(frame1, textvariable=self.rar_path).pack(side="left", fill="x", expand=True)
        tk.Button(frame1, text="Browse", command=self.browse_rar).pack(side="left", padx=5)

        # Output folder
        frame2 = tk.Frame(self.root)
        frame2.pack(pady=5, fill="x", padx=20)

        tk.Label(frame2, text="Output Folder:").pack(anchor="w")
        tk.Entry(frame2, textvariable=self.output_path).pack(side="left", fill="x", expand=True)
        tk.Button(frame2, text="Browse", command=self.browse_output).pack(side="left", padx=5)

        # Password field
        frame3 = tk.Frame(self.root)
        frame3.pack(pady=5, fill="x", padx=20)

        tk.Label(frame3, text="Password (if required):").pack(anchor="w")
        tk.Entry(frame3, textvariable=self.password, show="*").pack(fill="x")

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=550, mode="determinate")
        self.progress.pack(pady=15)

        # Extract button
        self.extract_btn = tk.Button(
            self.root, text="Extract", font=("Segoe UI", 11, "bold"),
            command=self.start_extraction, bg="#4CAF50", fg="white"
        )
        self.extract_btn.pack(pady=5)

        # Log window
        self.log_text = tk.Text(self.root, height=14, state="disabled", bg="#111", fg="#0f0")
        self.log_text.pack(padx=20, pady=10, fill="both", expand=True)

    def browse_rar(self):
        file = filedialog.askopenfilename(filetypes=[("RAR files", "*.rar")])
        if file:
            self.rar_path.set(file)

    def browse_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)

    def log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def start_extraction(self):
        rar_file = self.rar_path.get()
        output_dir = self.output_path.get()

        if not rar_file or not os.path.exists(rar_file):
            messagebox.showerror("Error", "Please select a valid RAR file.")
            return

        if not output_dir:
            messagebox.showerror("Error", "Please select an output folder.")
            return

        self.extract_btn.config(state="disabled")
        threading.Thread(
            target=self.extract_rar,
            args=(rar_file, output_dir, self.password.get()),
            daemon=True
        ).start()

    def extract_rar(self, rar_file, output_dir, password):
        try:
            self.log(f"Opening archive: {rar_file}")

            with rarfile.RarFile(rar_file) as rf:
                if password:
                    rf.setpassword(password)

                members = rf.infolist()
                total_files = len(members)

                if total_files == 0:
                    raise Exception("Archive is empty.")

                self.progress["maximum"] = total_files

                for idx, member in enumerate(members, start=1):
                    try:
                        rf.extract(member, path=output_dir)
                        self.log(f"Extracted: {member.filename}")
                    except rarfile.BadRarFile:
                        raise
                    except rarfile.RarWrongPassword:
                        raise Exception("Incorrect password.")
                    except rarfile.RarCRCError:
                        raise Exception("Wrong password or corrupted file.")
                    except Exception as e:
                        raise Exception(f"Failed on {member.filename}: {str(e)}")

                    self.progress["value"] = idx

                self.log("Extraction completed successfully.")
                messagebox.showinfo("Success", "RAR extracted successfully!")

        except rarfile.RarWrongPassword:
            messagebox.showerror("Error", "Incorrect password.")
            self.log("Error: Incorrect password.")

        except rarfile.RarCannotExec:
            messagebox.showerror("Error", "Unrar/WinRAR not found. Please install and add to PATH.")
            self.log("Error: Unrar not installed.")

        except rarfile.BadRarFile:
            messagebox.showerror("Error", "Invalid or corrupted RAR file.")
            self.log("Error: Bad RAR file.")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.log(f"Error: {str(e)}")

        finally:
            self.extract_btn.config(state="normal")
            self.progress["value"] = 0


if __name__ == "__main__":
    root = tk.Tk()
    app = RarExtractorGUI(root)
    root.mainloop()
