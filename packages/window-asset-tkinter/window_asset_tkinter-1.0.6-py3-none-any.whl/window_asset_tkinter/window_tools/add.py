"""
File in charge of containing the class that ad GUI elements ot other GUI elements
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


class Add:
    """ The class in charge of adding a GUI element to other GUI elements """

    def add_label(self, window: tk.Tk, text: str, fg: str, bkg: str, width: int = 50, height: int = 50, position_x: int = 0, position_y: int = 0, side: str = "left", anchor: str = "center", fill: str = tk.NONE, font: tuple = ("Times New Roman", 12)) -> tk.Label:
        """ Add a label to the window """
        Label = tk.Label(
            window,
            text=text,
            fg=fg,
            bg=bkg,
            width=width,
            height=height,
            anchor=anchor,
            font=font
        )
        Label.pack(padx=position_x, pady=position_y, side=side, fill=fill)
        return Label

    def add_button(self, window: tk.Tk, text: str, fg: str, bkg: str, side: str, command: any, width: int = 50, height: int = 50, position_x: int = 0, position_y: int = 0, anchor: str = tk.CENTER, fill: str = tk.NONE, column: int = -1, row: int = -1, column_span: int = 1) -> tk.Button:
        """ Add a button to the window """
        button = tk.Button(
            window,
            text=text,
            fg=fg,
            bg=bkg,
            width=width,
            height=height,
            command=command
        )
        if column > (-1) and row > (-1):
            if column_span < 1:
                column_span = 1
            button.grid_configure(
                column=column,
                row=row,
                columnspan=column_span
            )
        else:
            button.pack(
                padx=position_x,
                pady=position_y,
                side=side,
                anchor=anchor,
                fill=fill
            )
        return button

    def add_frame(self, window: tk.Tk, borderwidth: int, relief: str, bkg: str, width: int = 50, height: int = 50, position_x: int = 0, position_y: int = 0, side: str = "top", fill: str = tk.BOTH, anchor: str = tk.CENTER) -> tk.Frame:
        """ Add a frame to the window """
        Frame1 = tk.Frame(
            window,
            borderwidth=borderwidth,
            relief=relief,
            bg=bkg,
            width=width,
            height=height
        )
        Frame1.pack(padx=position_x, pady=position_y,
                    side=side, fill=fill, anchor=anchor)
        return Frame1

    def add_labelframe(self, window: tk.Tk, title: str, padding_x: int, padding_y: int, fill: str, expand: str, width: int = 50, height: int = 50, bkg: str = "#FFFFFF", fg: str = "#000000", font: tuple = ("Times New Roman", 12)) -> tk.LabelFrame:
        """ add a labelframe to the window """
        LabelFrame = tk.LabelFrame(
            window,
            text=title,
            padx=padding_x,
            pady=padding_y,
            width=width,
            height=height,
            bg=bkg,
            fg=fg,
            font=font
        )
        LabelFrame.pack(fill=fill, expand=expand)
        return LabelFrame

    def add_spinbox(self, window: tk.Tk, minimum: int, maximum: int, bkg: str, fg: str, width: int = 50, height: int = 50, position_x: int = 0, position_y: int = 0) -> tk.Spinbox:
        """ Add a spinbox to the window """
        spin = tk.Spinbox(
            window,
            from_=minimum,
            to=maximum,
            fg=fg,
            bg=bkg,
            width=width,
            height=height
        )
        spin.pack(padx=position_x, pady=position_y)
        return spin

    def add_entry(self, window: tk.Tk, text_variable: str = "", width: int = 20, bkg: str = "#FFFFFF", fg: str = "#000000", side: str = tk.LEFT, fill: str = tk.NONE, anchor: str = tk.CENTER, position_x: int = 0, position_y: int = 0, font: tuple = ()) -> tk.Entry:
        """ Add an entry field allowing the user to enter text """
        if isinstance(text_variable, str) == True:
            tmp = text_variable
            text_variable = tk.StringVar()
            text_variable.set(tmp)

        entree = tk.Entry(
            window,
            textvariable=text_variable,
            width=width,
            bg=bkg,
            fg=fg,
            font=font
        )
        entree.pack(
            side=side,
            fill=fill,
            anchor=anchor,
            padx=position_x,
            pady=position_y
        )
        return entree

    def add_paned_window(self, window: tk.Tk, orientation: str, side: str, expand: str, fill: str, vertical_padding: int, horizontal_padding: int) -> tk.PanedWindow:
        """ Add a paned window to the parent window, and configure orientation """
        panned_window = tk.PanedWindow(window, orient=orientation)
        panned_window.pack(
            side=side,
            expand=expand,
            fill=fill,
            pady=vertical_padding,
            padx=horizontal_padding
        )
        return panned_window

    def add_panned_window_node(self, panned_window: tk.PanedWindow, frame_window: tk.Frame) -> None:
        """ Add a node to the Paned window """
        panned_window.add(frame_window)
        panned_window.pack()

    def add_date_field(self, window: tk.Tk, width: int = 16, date_pattern: str = "dd/MM/yyyy", selectmode: str = "day", pady: int = 0, padx: int = 0, bkg: str = "black", fg: str = "white", borderwidth: int = 2, side: str = "left", fill: str = tk.NONE) -> DateEntry:
        """ Add a date field allowing date selection """
        cal = DateEntry(
            window,
            width=width,
            background=bkg,
            foreground=fg,
            bd=borderwidth,
            selectmode=selectmode,
            date_pattern=date_pattern
        )
        cal.pack(
            pady=pady,
            padx=padx,
            side=side,
            fill=fill
        )
        return cal

    def add_dropdown(self, window: tk.Tk, elements: list[str], state: str = "readonly", padx: int = 0, pady: int = 0, anchor: str = "e", side: str = tk.TOP, default_choice: int = 0, fill: str = tk.NONE, bkg: str = "#FFFFFF", fg: str = "#000000", font: tuple = ("Helvetica", 12), height: int = 1, width: int = 4) -> ttk.Combobox:
        """ generate a drop down menu for a window """
        combo = ttk.Combobox(
            window,
            state=state,
            values=elements,
            background=bkg,
            foreground=fg,
            font=font,
            height=height,
            width=width
        )
        combo.current(default_choice)
        combo.pack(
            padx=padx,
            pady=pady,
            anchor=anchor,
            fill=fill,
            side=side
        )
        return combo

    def add_get_data(self, parent_frame: tk.Frame, window_width, window_height, bkg, fg, label_description, button_command) -> dict[any]:
        """ generate a filepath gathering section """
        result = dict()
        button_description = "..."
        description_entry_width = int(
            window_width - (
                len(label_description) + len(button_description) + 4
            )
        )
        data_frame_height = (window_height - 2)
        result['data_frame'] = self.add_frame(
            window=parent_frame,
            borderwidth=0,
            relief=tk.FLAT,
            bkg=bkg,
            width=window_width,
            height=window_height,
            position_x=0,
            position_y=0
        )
        result['description_label'] = self.add_label(
            result['data_frame'],
            label_description,
            fg,
            bkg,
            len(label_description) + 2,
            data_frame_height,
            0,
            0,
            tk.LEFT
        )
        result['description_button'] = self.add_button(
            result['data_frame'],
            button_description,
            fg,
            bkg,
            tk.RIGHT,
            button_command,
            len(button_description) + 2,
            1,
            4,
            0
        )
        result['text_var'] = self.create_text_variable("")
        result['description_entry'] = self.add_text_field(
            result['data_frame'], result['text_var'], description_entry_width, bkg=bkg, fg=fg, side=tk.LEFT)
        return result

    def add_paragraph_field(self, frame: tk.Frame or tk.Tk, fg: str = "black", bkg: str = "white", height: int = 10, width: int = 10, padx_text: int = 0, pady_text: int = 0, block_cursor: bool = False, font: tuple = (), cursor: str = "xterm", export_selection: bool = True, highlight_colour: str = "#0077FF",  relief: str = tk.GROOVE, undo: bool = True, wrap: str = "word", fill: str = tk.BOTH, side: str = tk.TOP, padx_pack: int = 0, pady_pack: int = 0, ipadx: int = 1, ipady: int = 1) -> tk.Text:
        """ add a paragraph (a big zone to enter text) """
        paragraph = tk.Text(
            frame,
            background=bkg,
            foreground=fg,
            blockcursor=block_cursor,
            height=height,
            width=width,
            font=font,
            cursor=cursor,
            exportselection=export_selection,
            highlightcolor=highlight_colour,
            padx=padx_text,
            pady=pady_text,
            relief=relief,
            undo=undo,
            wrap=wrap
        )
        paragraph.pack(
            fill=fill,
            side=side,
            padx=padx_pack,
            pady=pady_pack,
            ipadx=ipadx,
            ipady=ipady
        )
        return paragraph

    def add_text_field(self, frame: tk.Frame or tk.Tk, fg: str = "black", bkg: str = "white", height: int = 10, width: int = 10, padx_text: int = 0, pady_text: int = 0, block_cursor: bool = False, font: tuple = (), cursor: str = "xterm", export_selection: bool = True, highlight_colour: str = "#0077FF",  relief: str = tk.GROOVE, undo: bool = True, wrap: str = "word", fill: str = tk.BOTH, side: str = tk.TOP, padx_pack: int = 0, pady_pack: int = 0, ipadx: int = 1, ipady: int = 1) -> tk.Text:
        """ add a paragraph (a big zone to enter text) """
        return self.add_paragraph_field(frame, fg, bkg, height, width, padx_text, pady_text, block_cursor, font, cursor, export_selection, highlight_colour,  relief, undo, wrap, fill, side, padx_pack, pady_pack, ipadx, ipady)

    def add_grid(self, window: tk.Tk, borderwidth: int, relief: str, bkg: str, width: int = 50, height: int = 50, position_x: int = 0, position_y: int = 0, side: str = "top") -> tk.Frame:
        """ add a grid to a frame """
        frame = self.add_frame(
            window,
            borderwidth,
            relief,
            bkg,
            width,
            height,
            position_x,
            position_y,
            side
        )
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        return frame

    def add_scrollbox(self, window: tk.Tk, grid_borderwidth: int, grid_relief: str, grid_bkg: str, grid_width: int = 50, grid_height: int = 50, grid_position_x: int = 0, grid_position_y: int = 0, grid_side: str = "top", paragraph_fg: str = "black", paragraph_bkg: str = "white", paragraph_height: int = 10, paragraph_width: int = 10, paragraph_padx_text: int = 0, paragraph_pady_text: int = 0, paragraph_block_cursor: bool = False, paragraph_font: tuple = (), paragraph_cursor: str = "xterm", paragraph_export_selection: bool = True, paragraph_highlight_colour: str = "#0077FF",  paragraph_relief: str = tk.GROOVE, paragraph_undo: bool = True, paragraph_wrap: str = "word", paragraph_fill: str = tk.BOTH, paragraph_side: str = tk.TOP, paragraph_padx_pack: int = 0, paragraph_pady_pack: int = 0, paragraph_ipadx: int = 1, paragraph_ipady: int = 1, scroll_orientation: str = tk.VERTICAL) -> dict[any]:
        """ Add a scrollbar to a text entity """
        result = dict()
        result["grid"] = self.add_grid(
            window,
            grid_borderwidth,
            grid_relief,
            grid_bkg,
            grid_width,
            grid_height,
            grid_position_x,
            grid_position_y,
            grid_side
        )
        result["paragraph"] = self.add_paragraph_field(
            frame=result["grid"],
            fg=paragraph_fg,
            bkg=paragraph_bkg,
            height=paragraph_height,
            width=paragraph_width,
            padx_text=paragraph_padx_text,
            pady_text=paragraph_pady_text,
            block_cursor=paragraph_block_cursor,
            font=paragraph_font,
            cursor=paragraph_cursor,
            export_selection=paragraph_export_selection,
            highlight_colour=paragraph_highlight_colour,
            relief=paragraph_relief,
            undo=paragraph_undo,
            wrap=paragraph_wrap,
            fill=paragraph_fill,
            side=paragraph_side,
            padx_pack=paragraph_padx_pack,
            pady_pack=paragraph_pady_pack,
            ipadx=paragraph_ipadx,
            ipady=paragraph_ipady
        )
        result["paragraph"].grid(row=0, column=0, sticky=tk.NS)
        result["scrollbar"] = ttk.Scrollbar(
            result["grid"],
            orient=scroll_orientation,
            command=result["paragraph"].yview
        )
        result["scrollbar"].grid(row=0, column=1, sticky=tk.NS)
        result["paragraph"]['yscrollcommand'] = result["scrollbar"].set
        return result

    def add_scroll_bar(self, frame: tk.Frame, tk_field: tk.Text, scroll_orientation: str = tk.VERTICAL, fill: str = tk.BOTH, side: str = tk.TOP, padx: int = 0, pady: int = 0, anchor: str = tk.CENTER, row: int = -1, column: int = -1, sticky: str = tk.NS) -> ttk.Scrollbar:
        """ Add a scroll bar to a tkinter asset """
        scroll_bar = ttk.Scrollbar(
            master=frame,
            orient=scroll_orientation,
            command=tk_field.yview
        )
        if row > -1 and column > -1:
            scroll_bar.grid(row=row, column=column, sticky=sticky)
        else:
            scroll_bar.pack(
                fill=fill,
                side=side,
                padx=padx,
                pady=pady,
                anchor=anchor
            )
        return scroll_bar

    def add_preloaded_image(self, window: tk.Tk, image_data: dict, bkg: str = "#FFFFFF", fg: str = "#000000", width: int = 10, height: int = 10, fill: str = tk.BOTH, side: str = tk.TOP, padx: int = 0, pady: int = 0, anchor: str = tk.NW, font: tuple = ("Times New Roman", 12)) -> dict[str, any]:
        """ Add an image to a window """
        result = {}
        ratio = 10
        if "err_message" in image_data:
            err_msg = image_data["err_message"]
            result["Label"] = self.add_label(
                window=window,
                text=err_msg,
                fg=fg,
                bkg=bkg,
                width=int(width/ratio),
                height=height,
                position_x=0,
                position_y=0,
                side=side,
                anchor=anchor,
                fill=fill
            )
            result["err_message"] = err_msg
            return result
        try:
            result["panel"] = tk.Label(
                window,
                image=image_data["img"],
                width=width,
                height=height
            )
            result["panel"].image = image_data["img"]
            result["panel"].pack(
                fill=fill,
                side=side,
                padx=padx,
                pady=pady,
                anchor=anchor
            )
            result["panel"].config(bg=bkg)
            result["img"] = image_data["img"]
        except Exception as error:
            result = {}
            result["err_message"] = f"""
            Error adding image to message box.
            Think to check if the window wasn't initialised twice.
            error = {error}
            """
            result["placeholder"] = self.add_paragraph_field(
                frame=window,
                fg=fg,
                bkg=bkg,
                height=len(result["err_message"].split("\n")),
                width=int(width/ratio),
                padx_text=0,
                pady_text=0,
                block_cursor=False,
                font=font,
                cursor="left_ptr",
                export_selection=True,
                highlight_colour=fg,
                relief=tk.FLAT,
                undo=False,
                wrap=tk.WORD,
                fill=tk.BOTH,
                side=tk.LEFT,
                padx_pack=0,
                pady_pack=0,
                ipadx=0,
                ipady=0
            )
            result["placeholder"].insert(tk.END, result["err_message"])
            result["placeholder"].config(state=tk.DISABLED)
        return result

    def add_watermark(self, window: tk.Tk, side: str = tk.BOTTOM, anchor: str = tk.E, bkg: str = "white", fg: str = "black", font: tuple = ("Times New Roman", 12)) -> tk.Label:
        """ Add the watermark to the window """
        text = f"{chr(169)} Created by Henry Letellier"
        watermark = self.add_label(
            window=window,
            text=text,
            bkg=bkg,
            fg=fg,
            width=len(text),
            height=1,
            position_x=0,
            position_y=0,
            side=side,
            anchor=anchor,
            fill=tk.X,
            font=font
        )
        return watermark

    def add_emoji(self, window: tk.Tk, text: str, fg: str, bkg: str, width: int = 50, height: int = 50, position_x: int = 0, position_y: int = 0, side: str = "left", anchor: str = "center", fill: str = tk.NONE, font: tuple = ("noto-color", 12)) -> tk.Label:
        """ Add a label to the window """
        Label = tk.Label(
            window,
            text=text,
            fg=fg,
            bg=bkg,
            width=width,
            height=height,
            anchor=anchor,
            font=font
        )
        Label.pack(padx=position_x, pady=position_y, side=side, fill=fill)
        return Label

    def add_image(self, window: tk.Tk, image_path: str, bkg: str = "#FFFFFF", fg: str = "#000000", width: int = 10, height: int = 10, fill: str = tk.BOTH, side: str = tk.TOP, padx: int = 0, pady: int = 0, anchor: str = tk.NW, font: tuple = ("Times New Roman", 12)) -> dict[any]:
        """ Add an image to a window """
        loaded_image = self.load_image(
            image_path=image_path,
            width=width,
            height=height
        )
        result = self.add_preloaded_image(
            window=window,
            image_data=loaded_image,
            bkg=bkg,
            fg=fg,
            width=width,
            height=height,
            fill=fill,
            side=side,
            padx=padx,
            pady=pady,
            anchor=anchor,
            font=font
        )
        return result
