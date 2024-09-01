import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SATAIS GUI")
        self.geometry("800x500")  # Increased window size
        self.resizable(False, False)  # Make the window non-resizable

        self.create_widgets()
        self.show_home()

    def create_widgets(self):
        # Load and set the logo
        logo_path = "satais.png"
        logo_image = Image.open(logo_path)
        logo_image.thumbnail((40, 40), Image.LANCZOS)  # Resize the image to fit in the top bar
        self.logo = ImageTk.PhotoImage(logo_image)

        # Find the dominant color of the logo for the top bar background
        logo_image_rgb = logo_image.convert("RGB")  # Ensure the image is in RGB mode
        dominant_color = logo_image_rgb.getpixel((0, 0))  # Assuming the top left pixel represents the background color
        self.dominant_color_hex = "#%02x%02x%02x" % dominant_color

        # Darken the dominant color for the background
        self.dominant_color_hex = self.darken_color(self.dominant_color_hex, 0.7)

        # Create a top stripe frame with border
        top_frame = tk.Frame(self, bg=self.dominant_color_hex, height=50, bd=2, relief="solid")
        top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Add logo to the top stripe
        logo_label = tk.Label(top_frame, image=self.logo, bg=self.dominant_color_hex)
        logo_label.pack(side="left", padx=10, pady=5)

        # Add text to the top stripe with a cool font and white color
        cool_font = font.Font(family="Comic Sans MS", size=20, weight="bold")
        top_label = tk.Label(top_frame, text="SATAIS", bg=self.dominant_color_hex, fg="white", font=cool_font)
        top_label.pack(side="left", padx=10, pady=10)

        # Create a left menu frame with a black border
        self.menu_frame = tk.Frame(self, bg=self.dominant_color_hex, width=150, bd=2, relief="solid")
        self.menu_frame.grid(row=1, column=0, sticky="nsew")

        # Add buttons to the menu frame with the same color as the menu background and black edge
        button_bg_color = self.dominant_color_hex
        button_border_color = "black"
        self.home_button = tk.Button(self.menu_frame, text="Home", command=self.show_home,
                                    bg=button_bg_color, highlightbackground=button_bg_color,
                                    bd=2, relief="solid", highlightcolor=button_border_color)
        self.home_button.pack(fill="x", padx=10, pady=5)

        self.settings_button = tk.Button(self.menu_frame, text="Settings", command=self.show_settings,
                                        bg=button_bg_color, highlightbackground=button_bg_color,
                                        bd=2, relief="solid", highlightcolor=button_border_color)
        self.settings_button.pack(fill="x", padx=10, pady=5)

        # Create a main content frame with a scrollbar for chat-like messages
        self.content_frame = tk.Frame(self, bg="grey20")  # Darker background
        self.content_frame.grid(row=1, column=1, sticky="nsew")

        self.canvas = tk.Canvas(self.content_frame, bg="grey20")
        self.scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="grey20")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a bottom frame for the message input
        self.bottom_frame = tk.Frame(self, bg="grey30", height=100, bd=2, relief="solid")  # Darker background
        self.bottom_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # Add a Text widget for message input without outlines or borders
        self.message_text = tk.Text(self.bottom_frame, height=4, wrap="word", bd=0, relief="flat", bg="grey40", highlightthickness=0)
        self.message_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Add a Send button
        self.send_button = tk.Button(self.bottom_frame, text="Send", command=self.send_message,
                                     bg="grey50", highlightbackground="grey50", bd=2, relief="solid", highlightcolor="black")
        self.send_button.pack(side="right", padx=5, pady=5)

        # Adjust the grid layout configuration
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def darken_color(self, color, factor):
        # Darken the given color by the given factor
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    def show_home(self):
        self.clear_content_frame()
        self.set_active_button(self.home_button)
        self.show_message_widgets()

    def show_settings(self):
        self.clear_content_frame()
        self.set_active_button(self.settings_button)
        self.hide_message_widgets()

    def clear_content_frame(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def send_message(self):
        message = self.message_text.get("1.0", "end-1c").strip()  # Get text from the Text widget
        if message:  # Only add non-empty messages
            message_label = tk.Label(self.scrollable_frame, text=message, bg="lightgrey", fg="black", anchor="w", padx=10, pady=5, wraplength=700, justify="left")
            message_label.pack(fill="x", padx=10, pady=5)  # Fill the width of the container
            self.message_text.delete("1.0", "end")  # Clear the text widget after sending

            # Auto-scroll to the latest message
            self.canvas.update_idletasks()
            self.canvas.yview_moveto(1)
        else:
            print("Empty message cannot be sent.")

    def set_active_button(self, active_button):
        # Deactivate both buttons first
        self.home_button.config(relief="solid", bg=self.dominant_color_hex)
        self.settings_button.config(relief="solid", bg=self.dominant_color_hex)

        # Activate the clicked button
        active_button.config(relief="raised", bg="darkgrey")

    def show_message_widgets(self):
        self.message_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.send_button.pack(side="right", padx=5, pady=5)

    def hide_message_widgets(self):
        self.message_text.pack_forget()
        self.send_button.pack_forget()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
