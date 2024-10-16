"""
File in charge of containing the functions that update info on GUI elements
"""

import os
import platform
import tkinter as tk


class Set:
    """ The class containing the actions for editing GUI aspects on the fly """

    def set_transparency(self, window: tk.Tk, alpha: int) -> None:
        """ Set the transparency of the window """
        if alpha < 0:
            alpha *= (-1)

        if alpha > 1:
            alpha = float((alpha - 0) / (1 - 0))
        window.attributes('-alpha', alpha)

    def set_colour_transparency(self, window: tk.Tk, colour: str = "grey", transparent: bool = True) -> None:
        """ Make the background of the window transparent"""
        if platform.system() == "Windows":
            if transparent == True:
                window.wm_attributes("-transparentcolor", colour)
            else:
                window.wm_attributes("-transparentcolor", "")
        elif platform.system() == "Java":
            window.wm_attributes("-transparent", transparent)
            if transparent == True:
                window.config(bg='systemTransparent')
            else:
                window.config(bg=colour)

    def set_window_title_bar_visibility(self, window: tk.Tk, visible: bool = False) -> None:
        """ Make the title bar (draggable section of a window) visible or not """
        window.overrideredirect(visible)

    def set_title(self, window: tk.Tk, title: str) -> None:
        """ Set the title of the window """
        window.title(title)

    def set_window_size(self, window: tk.Tk, width: int, height: int, posx: int = -666, posy: int = -666) -> None:
        """ Set the size of the window """
        position = ""
        if posx > -666:
            position += f"+{posx}"
        if posy > -666:
            if posx > -666:
                position += f"+{posy}"
            else:
                position += f"+{window.winfo_x()}+{posy}"

        window.geometry(f"{width}x{height}{position}")

    def set_min_window_size(self, window: tk.Tk, width: int, height: int) -> None:
        """ Set the minimm size for a window """
        window.minsize(width, height)

    def set_max_window_size(self, window: tk.Tk, width: int, height: int) -> None:
        """ Set the maximum size for a window """
        window.maxsize(width, height)

    def set_window_position(self, window: tk.Tk, posx: int, posy: int) -> None:
        """ Set the position of the window """
        window.geometry(f"+{posx}+{posy}")

    def set_window_position_x(self, window: tk.Tk, posx: int) -> None:
        """ Set the x position of the window """
        window.geometry(f"+{posx}+{window.winfo_y()}")

    def set_window_position_y(self, window: tk.Tk, posy: int) -> None:
        """ Set the y position of the window """
        window.geometry(f"+{window.winfo_x()}+{posy}")

    def set_offset_window_position_x(self, window: tk.Tk, posx: int) -> None:
        """ Set the x position of the window """
        window.geometry(f"+{posx+window.winfo_x()}+{window.winfo_y()}")

    def set_offset_window_position_y(self, window: tk.Tk, posy: int) -> None:
        """ Set the y position of the window """
        window.geometry(f"+{window.winfo_x()}+{posy+window.winfo_y()}")

    def set_offset_window_position(self, window: tk.Tk, posx: int, posy: int) -> None:
        """ Set the y position of the window """
        window.geometry(f"+{posx+window.winfo_x()}+{posy+window.winfo_y()}")

    def set_window_width(self, window: tk.Tk, width: int) -> None:
        """ Set the width of the window """
        window.geometry(
            f"{width}x{window.winfo_height()}+{window.winfo_x()}+{window.winfo_y()}")

    def set_window_height(self, window: tk.Tk, height: int) -> None:
        """ Set the width of the window """
        window.geometry(
            f"{window.winfo_width()}x{height}+{window.winfo_x()}+{window.winfo_y()}")

    def set_offset_window_width(self, window: tk.Tk, width: int) -> None:
        """ Set the width of the window """
        window.geometry(
            f"{width+window.winfo_width()}x{window.winfo_height()}+{window.winfo_x()}+{window.winfo_y()}"
        )

    def set_offset_window_height(self, window: tk.Tk, height: int) -> None:
        """ Set the width of the window """
        window.geometry(
            f"{window.winfo_width()}x{height+window.winfo_height()}+{window.winfo_x()}+{window.winfo_y()}"
        )

    def set_offset_window_dims(self, window: tk.Tk, width: int, height: int) -> None:
        """ Set the width of the window """
        window.geometry(
            f"{width+window.winfo_width()}x{height+window.winfo_height()}+{window.winfo_x()}+{window.winfo_y()}"
        )

    def set_window_background_colour(self, window: tk.Tk, colour: str) -> None:
        """ Set the background colour of the window """
        window["bg"] = colour

    def set_icon(self, window: tk.Tk, icon_path: str) -> None:
        """ Set an ico image as the window icon to the window """
        if os.path.exists(icon_path) and os.path.isfile(icon_path):
            if platform.system() == 'nt' or platform.system().lower() == "windows" or platform.system().lower() == "darwin":
                window.iconbitmap(icon_path)
            else:
                print(
                    "This is not a bug, this is in order to prevent the program from crashing on some linux systems"
                )
                print(f"system = {platform.system()}")
                print(f"icon_path = {icon_path}")
        else:
            print(f"The icon path '{icon_path}' is not valid")

    def set_window_always_on_top(self, window: tk.Tk, always_on_top: bool = True) -> None:
        """ Set the window to always be on top """
        window.wm_attributes("-topmost", always_on_top)

    def set_total_transparency(self, window: tk.Tk, colour: str = "grey", transparent: bool = True) -> None:
        """ Make the full conversion of the window so that it is transparent """
        if transparent == True:
            self.set_window_background_colour(window=window, colour=colour)
        else:
            self.set_window_background_colour(window=window, colour=colour)
        self.set_colour_transparency(
            window=window,
            colour=colour,
            transparent=transparent
        )
        self.set_window_title_bar_visibility(
            window=window,
            visible=transparent
        )

    def set_window_visible(self, window: tk.Tk, visible: bool = True) -> None:
        """ Set the window to be visible or not """
        if visible == True:
            window.deiconify()
        else:
            window.withdraw()

    def set_interaction_possible(self, window:tk.Tk, window_interaction_disabled:bool = False) -> None:
        """ If set to False, the elements in the window will be interactible """
        if platform.system() == "Windows":
            if window_interaction_disabled == True:
                window.wm_attributes("-disabled", True)
            else:
                window.wm_attributes("-disabled", False)

# Traceback (most recent call last):
#   File "/run/media/hletellier/8E1C227B1C225E89/Users/Henry_PC/Documents/001_GitHub/Hanra-s-work/Desktop_pet/src/main.py", line 510, in <module>
#     MI.main()
#   File "/run/media/hletellier/8E1C227B1C225E89/Users/Henry_PC/Documents/001_GitHub/Hanra-s-work/Desktop_pet/src/main.py", line 476, in main
#     self.class_ressources["PI"].main(
#   File "/run/media/hletellier/8E1C227B1C225E89/Users/Henry_PC/Documents/001_GitHub/Hanra-s-work/Desktop_pet/src/libs/windows/pet/__init__.py", line 243, in main
#     self.load_ressources.main(
#   File "/run/media/hletellier/8E1C227B1C225E89/Users/Henry_PC/Documents/001_GitHub/Hanra-s-work/Desktop_pet/src/libs/windows/pet/pet_load_ressources.py", line 465, in main
#     self.create_window()
#   File "/run/media/hletellier/8E1C227B1C225E89/Users/Henry_PC/Documents/001_GitHub/Hanra-s-work/Desktop_pet/src/libs/windows/pet/pet_load_ressources.py", line 229, in create_window
#     self.set_interaction_possible(self.character_window, False)
#   File "/run/media/hletellier/8E1C227B1C225E89/Users/Henry_PC/Documents/001_GitHub/Hanra-s-work/Desktop_pet/src/libs/windows/window_asset/window_tools/set.py", line 161, in set_interaction_possible
#     window.wm_attributes("-disabled", False)
#   File "/usr/lib64/python3.9/tkinter/__init__.py", line 1976, in wm_attributes
#     return self.tk.call(args)
# _tkinter.TclError: bad attribute "-disabled": must be -alpha, -topmost, -zoomed, -fullscreen, or -type
