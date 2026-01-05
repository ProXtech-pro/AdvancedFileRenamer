import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import re

class EnhancedFileRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced File Renamer Pro (MultiPattern)")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        self.selected_files = []
        self.case_sensitive = tk.BooleanVar(value=True)
        self.replace_spaces = tk.BooleanVar(value=False)
        self.replace_diacritics = tk.BooleanVar(value=False)
        self.simulation_mode = tk.BooleanVar(value=False)
        self.use_regex = tk.BooleanVar(value=False)

        self.create_main_layout()

    def create_main_layout(self):
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        file_frame = ttk.LabelFrame(main_container, text="Select Files")
        file_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        list_container = ttk.Frame(file_frame)
        list_container.pack(fill=tk.BOTH, expand=True)

        self.file_listbox = tk.Listbox(list_container, selectmode=tk.EXTENDED)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_container, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="Add Files", command=self.add_files).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Add Folder", command=self.add_folder).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Remove Selected", command=self.remove_files).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_files).pack(side=tk.RIGHT, padx=2)
        ttk.Button(btn_frame, text="Export List", command=self.export_file_list).pack(side=tk.RIGHT, padx=2)
        ttk.Button(btn_frame, text="Import List", command=self.import_file_list).pack(side=tk.RIGHT, padx=2)

        pattern_frame = ttk.LabelFrame(main_container, text="Renaming Options")
        pattern_frame.pack(fill=tk.X, padx=5, pady=5)

        row = ttk.Frame(pattern_frame)
        row.pack(fill=tk.X, pady=5)
        ttk.Label(row, text="Patterns to remove (comma, | or newline):").pack(side=tk.LEFT, padx=5)
        self.pattern_box = tk.Text(row, height=2, width=50)
        self.pattern_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.pattern_box.bind("<KeyRelease>", lambda e: self.update_preview())

        options_frame = ttk.Frame(pattern_frame)
        options_frame.pack(fill=tk.X, pady=5)
        ttk.Checkbutton(options_frame, text="Case Sensitive", variable=self.case_sensitive, command=self.update_preview).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(options_frame, text="Clean Extra Spaces", variable=self.replace_spaces, command=self.update_preview).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(options_frame, text="Replace Diacritics (RO)", variable=self.replace_diacritics, command=self.update_preview).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(options_frame, text="Use Regex", variable=self.use_regex, command=self.update_preview).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(options_frame, text="Simulation Mode", variable=self.simulation_mode).pack(side=tk.LEFT, padx=5)

        preview_frame = ttk.LabelFrame(main_container, text="Preview Changes")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

        action_frame = ttk.Frame(main_container)
        action_frame.pack(fill=tk.X, pady=5)
        ttk.Button(action_frame, text="Update Preview", command=self.update_preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Start Renaming", command=self.rename_files).pack(side=tk.RIGHT, padx=5)

    def get_patterns(self):
        raw = self.pattern_box.get("1.0", tk.END).strip()
        return [p.strip() for p in re.split(r'[,\n|]+', raw) if p.strip()]

    def add_files(self):
        files = filedialog.askopenfilenames()
        for f in files:
            if f not in self.selected_files:
                self.selected_files.append(f)
                self.file_listbox.insert(tk.END, os.path.basename(f))
        self.update_preview()

    def add_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            for root, _, files in os.walk(folder):
                for name in files:
                    path = os.path.join(root, name)
                    if path not in self.selected_files:
                        self.selected_files.append(path)
                        self.file_listbox.insert(tk.END, os.path.basename(path))
        self.update_preview()

    def remove_files(self):
        for i in reversed(self.file_listbox.curselection()):
            del self.selected_files[i]
            self.file_listbox.delete(i)
        self.update_preview()

    def clear_files(self):
        self.selected_files.clear()
        self.file_listbox.delete(0, tk.END)
        self.update_preview()

    def export_file_list(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                for file in self.selected_files:
                    f.write(file + '\n')
            self.status_var.set(f"Exported {len(self.selected_files)} files")

    def import_file_list(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if os.path.isfile(line.strip())]
            self.selected_files = lines
            self.file_listbox.delete(0, tk.END)
            for f in lines:
                self.file_listbox.insert(tk.END, os.path.basename(f))
            self.update_preview()

    def update_preview(self, event=None):
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete(1.0, tk.END)
        patterns = self.get_patterns()

        if not self.selected_files:
            self.preview_text.insert(tk.END, "No files selected")
        elif not patterns and not self.replace_spaces.get() and not self.replace_diacritics.get():
            self.preview_text.insert(tk.END, "Enter a pattern or select an option (Spaces/Diacritics) to preview changes")
        else:
            self.preview_text.insert(tk.END, "Original File Name ⟶ New File Name\n" + "-"*60 + "\n")
            for file_path in self.selected_files:
                original = os.path.basename(file_path)
                new_name = self.generate_new_name(original, patterns)
                self.preview_text.insert(tk.END, f"{original}\n⟶ {new_name}\n{'-'*60}\n")
        self.preview_text.config(state=tk.DISABLED)

    def generate_new_name(self, filename, patterns):
        base, ext = os.path.splitext(filename)
        try:
            for pattern in patterns:
                if self.use_regex.get():
                    flags = 0 if self.case_sensitive.get() else re.IGNORECASE
                    base = re.sub(pattern, '', base, flags=flags)
                else:
                    if not self.case_sensitive.get():
                        pattern = pattern.lower()
                        base_lower = base.lower()
                        result = ''
                        i = 0
                        while i < len(base):
                            if base_lower[i:i+len(pattern)] == pattern:
                                i += len(pattern)
                            else:
                                result += base[i]
                                i += 1
                        base = result
                    else:
                        base = base.replace(pattern, '')
            if self.replace_spaces.get():
                base = re.sub(r'\s+', ' ', base).strip()
            
            if self.replace_diacritics.get():
                replacements = {
                    'ă': 'a', 'Ă': 'A',
                    'â': 'a', 'Â': 'A',
                    'î': 'i', 'Î': 'I',
                    'ș': 's', 'Ș': 'S',
                    'ț': 't', 'Ț': 'T'
                }
                base = re.sub(r'[ăĂâÂîÎșȘțȚ]', lambda m: replacements[m.group(0)], base)

            base = ''.join(c for c in base if c not in '<>:"/\\|?*')
        except re.error:
            return "[INVALID REGEX]"
        return base + ext

    def rename_files(self):
        patterns = self.get_patterns()
        if not patterns and not self.replace_spaces.get() and not self.replace_diacritics.get():
            messagebox.showwarning("Missing Options", "Please enter a pattern or select an option (Spaces/Diacritics)")
            return
        if not self.selected_files:
            messagebox.showwarning("No Files", "No files selected for renaming")
            return
        if not messagebox.askyesno("Confirm", f"Proceed with renaming {len(self.selected_files)} files?"):
            return

        success = 0
        for i, path in enumerate(self.selected_files):
            try:
                original = os.path.basename(path)
                new_name = self.generate_new_name(original, patterns)
                if new_name == original or new_name == "[INVALID REGEX]":
                    continue
                new_path = os.path.join(os.path.dirname(path), new_name)
                if os.path.exists(new_path):
                    self.status_var.set(f"Skipped: {new_name} already exists")
                    continue
                if self.simulation_mode.get():
                    print(f"[SIMULATION] {original} ➜ {new_name}")
                    success += 1
                    continue
                os.rename(path, new_path)
                self.selected_files[i] = new_path
                self.file_listbox.delete(i)
                self.file_listbox.insert(i, new_name)
                success += 1
            except Exception as e:
                self.status_var.set(f"Error renaming {original}: {e}")
        self.update_preview()
        messagebox.showinfo("Done", f"Renamed {success} files successfully.")
        self.status_var.set("Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedFileRenamer(root)
    root.mainloop()
