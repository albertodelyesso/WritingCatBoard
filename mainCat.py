import tkinter as tk
from tkinter import Label, Menu, Toplevel
from PIL import Image, ImageTk
from pynput import keyboard

class GifOverlayApp:
    def __init__(self, master):
        self.master = master
        self.master.title("GIF Overlay")
        self.master.geometry("90x90")  # Establecer tamaño máximo de la ventana
        self.master.overrideredirect(True)  # Eliminar barra de título y botones de minimizar, cerrar y maximizar
        self.master.attributes('-topmost', True)  # Mantener la ventana en la parte superior

        self.image_label = Label(self.master)
        self.image_label.pack()

        self.gif_path = 'animated.png'
        self.not_animated_path = 'notanimated.png'

        self.load_images()

        self.show_static_image()

        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

        self.create_context_menu()

        # Variables para el arrastre de la ventana
        self.dragging = False
        self.start_x = None
        self.start_y = None

        # Eventos del ratón para arrastrar la ventana
        self.master.bind("<ButtonPress-1>", self.start_drag)
        self.master.bind("<B1-Motion>", self.drag)
        self.master.bind("<ButtonRelease-1>", self.stop_drag)

    def load_images(self):
        self.gif_image = Image.open(self.gif_path)
        self.gif_image = self.gif_image.resize((90, 90))
        self.gif_image = ImageTk.PhotoImage(self.gif_image)

        self.static_image = Image.open(self.not_animated_path)
        self.static_image = self.static_image.resize((90, 90))
        self.static_image = ImageTk.PhotoImage(self.static_image)

    def show_static_image(self):
        self.image_label.config(image=self.static_image)

    def show_animated_image(self):
        self.image_label.config(image=self.gif_image)

    def on_press(self, key):
        self.show_animated_image()

    def on_release(self, key):
        self.show_static_image()

    def create_context_menu(self):
        self.context_menu = Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Cerrar", command=self.close_window)
        self.master.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def close_window(self):
        self.master.destroy()

    def start_drag(self, event):
        if event.widget == self.image_label:
            self.dragging = True
            self.start_x = event.x
            self.start_y = event.y

    def drag(self, event):
        if self.dragging:
            x = self.master.winfo_x() + event.x - self.start_x
            y = self.master.winfo_y() + event.y - self.start_y
            self.master.geometry(f"+{x}+{y}")

    def stop_drag(self, event):
        self.dragging = False

def main():
    root = tk.Tk()
    app = GifOverlayApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
