#!/usr/bin/env python3

from tkinter import *
from tkinter.scrolledtext import *
import tkinter.messagebox
from enum import Enum
import json
import tkinter.font
import os

from MyLabel import MyLabel
from file_module import File_Type


class Window(Enum):
    START_UP, HEIDE, SETTINGS, CONSOLE, NEW_PROJECT = range(5)


class gui_module:
    def __init__(self, heide):
        self.heide = heide
        self.active_window = None

        self.heide_version = "HEIDE v0.5"
        self.root = Tk()

        self.logo = None

        self.key_bindings()
        self.root.protocol("WM_DELETE_WINDOW", self.heide.heide_quit)

        self.param_custom_font = tkinter.font.Font()
        self.data_custom_font = tkinter.font.Font()
        self.alg_custom_font = tkinter.font.Font()

        self.param_label = Label
        self.data_label = Label
        self.alg_label = Label

        self.__command_label = Label
        self.__command_label_txt = StringVar()

        self.output_window = Toplevel
        self.output_text = ScrolledText
        self.__photo = PhotoImage
        self.load_bar_label = MyLabel

        self.settings_window = Toplevel
        self.__he_src_entry = Entry
        self.__max_num_subpr_entry = Entry
        self.__display_mem_usage = IntVar
        self.__display_mem_usage_checkbutton = Checkbutton

        self.__new_project_window = Toplevel
        self.he_src_entry_np = Entry
        self.project_name_entry = Entry
        self.project_loc_entry = Entry
        self.existing_params_entry = Entry
        self.existing_data_entry = Entry
        self.existing_alg_entry = Entry

    def key_bindings(self):
        keys =["Control_L", "Control_R",
               "s",
               "p", "P",
               "d", "D",
               "a", "A",
               "o",
               "n",
               "C",
               "q",
               "F1"]
        for key in keys:
            self.root.bind("<KeyPress-" + key + ">",
                           self.heide.edit_mod.key_press)
            self.root.bind("<KeyRelease-" + key + ">",
                           self.heide.edit_mod.key_release)


    def spawn_start_up_window(self):
        self.active_window = Window.START_UP

        # Root widget creation for startup window
        self.root.wm_title(self.heide_version + " Startup Window")
        self.root.wm_minsize(height=250, width=500)
        self.root.wm_maxsize(height=250, width=500)
        self.logo = Image("photo", file="./imgs/logo.gif")
        self.root.tk.call("wm", "iconphoto", self.root._w,
                          "-default", self.logo)

        logo_frame = Frame(self.root, height=250, width=250, padx=10, pady=50)
        logo_frame.grid(row=0, column=0)
        Label(logo_frame, image=self.logo).pack()

        text_frame = Frame(self.root, height=250, width=250, padx=10, pady=0)
        text_frame.grid(row=0, column=1)
        Label(text_frame, text=self.heide_version,
              font=("Helvetica", 30)).pack(anchor=W)

        self.__command_label = Label(text_frame,
                                     textvariable=self.__command_label_txt,
                                     wraplength=250, justify=LEFT)
        self.__command_label.pack()

        self.set_command_label("Initializing HEIDE ...")

        self.root.update()


    def set_command_label(self, text):
        self.__command_label_txt.set(text)

    def display_start_up_error(self, set_txt):
        self.__command_label.configure(fg="red")
        self.set_command_label(set_txt)

        self.root.update()

        self.root.wait_window()
        self.root.quit()

        sys.exit()

    def display_error(self, error_type, error):
        tkinter.messagebox.showerror(error_type, error)
        return

    def spawn_heide_window(self):
        self.active_window = Window.HEIDE
        # Root widget creation for HEIDE GUI
        self.root.wm_title(self.heide_version)
        self.root.wm_minsize(height=927, width=1500)
        self.root.wm_maxsize(height=927, width=1500)

        # Create the root widgets menubar
        menubar = Menu(self.root)

        # add 'File' dropdown menu to menubar
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="New Project   CTRL+n",
                              command=self.heide.heide_new_project)

        # create submenu for opening files or projects
        open_menu = Menu(file_menu, tearoff=0)
        open_menu.add_command(label="Open Project       CTRL+o",
                              command=lambda: self.heide.heide_open(
                                  File_Type.PROJ_FILE, None))
        open_menu.add_command(label="Open Param File",
                              command=lambda: self.heide.heide_open(
                                  File_Type.PARAM_FILE, None))
        open_menu.add_command(label="Open Data File",
                              command=lambda: self.heide.heide_open(
                                  File_Type.DATA_FILE, None))
        open_menu.add_command(label="Open Alg File",
                              command=lambda: self.heide.heide_open(
                                  File_Type.ALG_FILE, None))
        file_menu.add_cascade(label="Open", menu=open_menu, underline=0)

        # create submenu for saving files
        save_menu = Menu(file_menu, tearoff=0)
        save_menu.add_command(label="Save Project".ljust(20) + "CTRL+s",
                              command=lambda: self.heide.heide_save(
                                  File_Type.PROJ_FILE))
        save_menu.add_command(label="Save Params".ljust(18) + "CTRL+p",
                              command=lambda: self.heide.heide_save(
                                  File_Type.PARAM_FILE))
        save_menu.add_command(label="Save Data".ljust(20) + "CTRL+d",
                              command=lambda: self.heide.heide_save(
                                  File_Type.DATA_FILE))
        save_menu.add_command(label="Save Alg".ljust(21) + "CTRL+a",
                              command=lambda: self.heide.heide_save(
                                  File_Type.ALG_FILE))
        file_menu.add_cascade(label="Save", menu=save_menu, underline=0)

        # create submenu for save as
        save_as_menu = Menu(file_menu, tearoff=0)
        save_as_menu.add_command(label="Save Params As...".ljust(20) + "CTRL+P",
                                 command=lambda: self.heide.heide_save_as(
                                     File_Type.PARAM_FILE))
        save_as_menu.add_command(label="Save Data As...".ljust(22) + "CTRL+D",
                                 command=lambda: self.heide.heide_save_as(
                                     File_Type.DATA_FILE))
        save_as_menu.add_command(label="Save Alg As...".ljust(23) + "CTRL+A",
                                 command=lambda: self.heide.heide_save_as(
                                     File_Type.ALG_FILE))
        file_menu.add_cascade(label="Save As...", menu=save_as_menu,
                              underline=0)

        # create submenu for import
        import_menu = Menu(file_menu, tearoff=0)
        import_menu.add_command(label="Import Params",
                                command=lambda: self.heide.heide_import(
                                    File_Type.PARAM_FILE))
        import_menu.add_command(label="Import Data",
                                command=lambda: self.heide.heide_import(
                                    File_Type.DATA_FILE))
        import_menu.add_command(label="Import Alg",
                                command=lambda: self.heide.heide_import(
                                    File_Type.ALG_FILE))
        file_menu.add_cascade(label="Import", menu=import_menu,
                              underline=0)

        file_menu.add_command(label="Close Project   CTRL+C",
                              command=self.heide.heide_close_project)

        file_menu.add_command(label="Settings",
                              command=self.spawn_settings_window)

        file_menu.add_separator()

        file_menu.add_command(label="Quit               CTRL+q",
                              command=self.heide.heide_quit)

        # Add 'Run' dropdown menu to menubar
        run_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Run", menu=run_menu)

        run_menu.add_command(label="Run    F1",
                             command=self.heide.heide_run)

        # Tell root to display menubar
        self.root.config(menu=menubar)

        """
        The GUI is split into 3 frames: the parameter frame, data frame, the
        algorithm frame.

            - Parameter and Data Frame -
                Contains 'editors' where HElib setup parameters and data with
                which to perform computations on can be specified

            - Algorithm Frame -
                Contains an 'editor' where the algorithm for computation is
                specified. The algorithm will be run on the data in the 'data
                editor' after it has been encrypted using the parameters
                specified in the 'parameter editor'
        """
        param_and_data_frame = Frame(self.root, height=25, width=50, pady=15,
                                     padx=20)
        param_and_data_frame.grid(row=0, column=0)

        alg_frame = Frame(self.root, height=25, width=50, pady=15, padx=20)
        alg_frame.grid(row=0, column=1)

        keyboard_keys = ["Cancel",
                         "BackSpace",
                         "Tab",
                         "Return",
                         "Shift_L",
                         "Control_L",
                         "Alt_L",
                         "Shift_R",
                         "Control_R",
                         "Alt_R",
                         "Escape",
                         "Insert",
                         "Delete"]

        self.param_label = Label(param_and_data_frame,
                                 text="Parameter Editor",
                                 font=self.param_custom_font).pack(anchor=W)
        param_editor = ScrolledText(param_and_data_frame, height=25, width=85,
                                    undo=True)
        param_editor.bind("<Key>", self.heide.edit_mod.param_edit_modified)
        for key in keyboard_keys:
            param_editor.bind(key, self.heide.edit_mod.param_edit_modified)
        param_editor.pack()

        Frame(param_and_data_frame, height=50).pack()

        self.data_label = Label(param_and_data_frame,
                                text="Data Editor",
                                font=self.data_custom_font).pack(anchor=W)
        data_editor = ScrolledText(param_and_data_frame, height=25, width=85,
                                   undo=True)
        data_editor.bind("<Key>", self.heide.edit_mod.data_edit_modified)
        for key in keyboard_keys:
            data_editor.bind(key, self.heide.edit_mod.data_edit_modified)
        data_editor.pack()

        self.alg_label = Label(alg_frame,
                               text="Algorithm Editor",
                               font=self.alg_custom_font).pack(anchor=W)
        alg_editor = ScrolledText(alg_frame, height=55, width=113, undo=True)
        alg_editor.bind("<Key>", self.heide.edit_mod.alg_edit_modified)
        for key in keyboard_keys:
            alg_editor.bind(key, self.heide.edit_mod.alg_edit_modified)
        alg_editor.pack()

        # set editor manager variables
        self.heide.edit_mod.set_editors(param_editor, data_editor, alg_editor)

        """
        Start mainloop, which will wait for user to do something
        """
        self.root.mainloop()

    def spawn_settings_window(self):
        self.active_window = Window.SETTINGS
        self.settings_window = Toplevel(padx=20, pady=20)
        self.settings_window.title("HEIDE Settings")
        self.settings_window.minsize(height=225, width=375)
        self.settings_window.maxsize(height=225, width=375)

        # setting window spawn location
        w = self.settings_window.winfo_screenwidth()
        h = self.settings_window.winfo_screenheight()
        settings_size = \
            tuple(int(_) for _ in
                  self.settings_window.geometry().split('+')[0].split('x'))
        x = w/2 - settings_size[0]/2
        y = h/2 - settings_size[1]/2
        self.settings_window.geometry("%dx%d+%d+%d" % (settings_size + (x, y)))

        self.settings_window.grab_set()

        Label(self.settings_window, text="Makefile Locations",
              font=("Helvetica", 15), anchor=W).grid(row=0, column=0)

        Label(self.settings_window, text="HE Source Code:").grid(row=1,
                                                                   column=0,
                                                                   sticky=W)
        self.__he_src_entry = Entry(self.settings_window)
        self.__he_src_entry.grid(row=1, column=1, sticky=W)
        self.__he_src_entry.insert(0, self.heide.set_mod.he_src)

        Label(self.settings_window, text="Run Settings",
              font=("Helvetica", 15), anchor=W).grid(row=2, column=0)

        Label(self.settings_window, text="Max # Subprocesses:").grid(row=3,
                                                                   column=0,
                                                                   sticky=W)
        self.__max_num_subpr_entry = Entry(self.settings_window)
        self.__max_num_subpr_entry.grid(row=3, column=1, sticky=W)
        self.__max_num_subpr_entry.insert(0, self.heide.set_mod.max_num_subpr)

        self.__display_mem_usage = IntVar()
        Label(self.settings_window, text="Display Memory Usage:").grid(row=4,
                                                                   column=0,
                                                                   sticky=W)
        self.__display_mem_usage_checkbutton = Checkbutton(self.settings_window,
                               variable=self.__display_mem_usage)
        if self.heide.set_mod.display_mem_usage:
            self.__display_mem_usage_checkbutton.select()
        self.__display_mem_usage_checkbutton.grid(row=4, column=1, sticky=W)

        Button(self.settings_window, text="Close",
               command=self.close_settings).grid(row=5, column=0, pady=20)
        Button(self.settings_window, text="Apply",
               command=self.heide.set_mod.apply_settings).grid(row=5, column=1,
                                                               pady=30)

        self.settings_window.update()

    def close_settings(self):
        self.active_window = Window.HEIDE
        self.settings_window.destroy()

    def get_settings(self):
        return json.dumps({"he_src": self.__he_src_entry.get(),
                           "max_num_subpr" :
                               int(self.__max_num_subpr_entry.get()),
                           "display_mem_usage" :
                               bool(self.__display_mem_usage.get())})

    def spawn_heide_console_window(self):
        self.active_window = Window.CONSOLE

        self.output_window = Toplevel()
        self.output_window.title("HEIDE Console")
        self.output_window.minsize(height=425, width=650)
        self.output_window.maxsize(height=425, width=650)

        self.output_window.protocol("WM_DELETE_WINDOW", self.close_console)

        # console window spawn location
        w = self.output_window.winfo_screenwidth()
        h = self.output_window.winfo_screenheight()
        output_wind_size = \
            tuple(int(_) for _ in
                  self.output_window.geometry().split('+')[0].split('x'))
        x = w/2 - output_wind_size[0]/2
        y = h/2 - output_wind_size[1]/2
        self.output_window.geometry("%dx%d+%d+%d" %
                                       (output_wind_size + (x, y)))

        self.output_window.grab_set()

        text_frame = Frame(self.output_window, padx=20)
        text_frame.grid(row=0, column=0)

        Label(text_frame, text="Output").pack(anchor=W)

        self.output_text = ScrolledText(text_frame, height=23, width=85)
        self.output_text.pack()

        load_bar_frame = Frame(self.output_window, padx=20)
        load_bar_frame.grid(row=1, column=0)

        self.load_bar_label = MyLabel(load_bar_frame,
                                         "../imgs/loading_bar.gif")
        self.load_bar_label.pack()

        button_frame = Frame(self.output_window, padx=20)
        button_frame.grid(row=2, column=0)

        Button(button_frame, text="Close",
               command=self.close_console).grid(row=0, column=0)
        Button(button_frame, text="Save",
               command=self.heide.heide_save_console_output).grid(row=0,
                                                                  column=1)

        self.output_text.configure(state="disabled")

        self.output_window.update()


    def close_console(self):
        self.active_window = Window.HEIDE
        self.output_window.destroy()

        os.chdir(self.heide.og_dir)

        # terminate all currently running processes
        for proc in self.heide.running_processes:
            proc.terminate()

    def heide_console_display_result(self, config, ret_val, out, err):
        if ret_val == 0:
            self.output_text.configure(state="normal")
            self.output_text.insert("end",
                                        "/***** CONFIGURATION *****/\n\n")
            self.output_text.insert("end", config)

            self.output_text.insert("end",
                                        "\n/***** OUTPUT *****/\n\n")
            self.output_text.insert("end", out)
            self.output_text.insert("end", "\n" + "#" * 80 + "\n")
            self.output_text.configure(state="disabled")
        else:
            self.output_text.configure(state="normal")
            self.output_text.insert("end",
                                        "/***** CONFIGURATION *****/\n\n")
            self.output_text.insert("end", config)
            self.output_text.insert("end", out)
            self.output_text.insert("end", "\n" + "#" * 80 + "\n")
            self.output_text.insert("end",
                                        "/***** An ERROR has occurred *****/\n")
            self.output_text.insert("end", err)
            self.output_text.insert("end", "\n" + "#" * 80 + "\n")
            self.output_text.configure(state="disabled")

        self.output_window.update()

    def spawn_new_project_window(self):
        self.active_window = Window.NEW_PROJECT
        self.__new_project_window = Toplevel(padx=20, pady=20)
        self.__new_project_window.title("New Project")
        self.__new_project_window.minsize(height=350, width=405)
        self.__new_project_window.maxsize(height=350, width=405)

        # new project window spawn location
        w = self.__new_project_window.winfo_screenwidth()
        h = self.__new_project_window.winfo_screenheight()
        new_proj_wind_size = \
            tuple(int(_) for _ in
                  self.__new_project_window.geometry().split('+')[0].split('x'))
        x = w/2 - new_proj_wind_size[0]/2
        y = h/2 - new_proj_wind_size[1]/2
        self.__new_project_window.geometry("%dx%d+%d+%d" %
                                       (new_proj_wind_size + (x, y)))

        self.__new_project_window.grab_set()

        Label(self.__new_project_window, text="Makefile Locations",
              font=("Helvetica", 15)).grid(row=0, column=0, sticky=W)

        Label(self.__new_project_window,
              text="HE Source Code:").grid(row=1, column=0, sticky=W)
        self.he_src_entry_np = Entry(self.__new_project_window)
        self.he_src_entry_np.grid(row=1, column=1, sticky=W)
        self.he_src_entry_np.insert(0, self.heide.set_mod.he_src)

        Label(self.__new_project_window, text="Project Details",
              font=("Helvetica", 15)).grid(row=2, column=0, sticky=W)

        Label(self.__new_project_window,
              text="Project Name:").grid(row=3, column=0, sticky=W)
        self.project_name_entry = Entry(self.__new_project_window)
        self.project_name_entry.grid(row=3, column=1, sticky=W)

        Label(self.__new_project_window,
              text="Project Location:").grid(row=4, column=0, sticky=W)
        self.project_loc_entry = Entry(self.__new_project_window)
        self.project_loc_entry.grid(row=4, column=1, sticky=W)
        self.project_loc_entry.insert(0, self.heide.set_mod.heide_proj_dir)

        Label(self.__new_project_window, text="Existing Sources",
              font=("Helvetica", 15)).grid(row=5, column=0, sticky=W)

        Label(self.__new_project_window,
              text="Existing Parameter File:").grid(row=6, column=0, sticky=W)
        self.existing_params_entry = Entry(self.__new_project_window)
        self.existing_params_entry.grid(row=6, column=1, sticky=W)
        Button(self.__new_project_window, text="...",
               command=lambda:
               self.heide.file_mod.get_existing_loc(self.existing_params_entry)
              ).grid(row=6, column=3)

        Label(self.__new_project_window,
              text="Existing Data File:").grid(row=7, column=0, sticky=W)
        self.existing_data_entry = Entry(self.__new_project_window)
        self.existing_data_entry.grid(row=7, column=1, sticky=W)
        Button(self.__new_project_window, text="...",
               command=lambda:
               self.heide.file_mod.get_existing_loc(self.existing_data_entry)
              ).grid(row=7, column=3)

        Label(self.__new_project_window,
              text="Existing Algorithm File:").grid(row=8, column=0, sticky=W)
        self.existing_alg_entry = Entry(self.__new_project_window)
        self.existing_alg_entry.grid(row=8, column=1, sticky=W)
        Button(self.__new_project_window, text="...",
               command=lambda:
               self.heide.file_mod.get_existing_loc(self.existing_alg_entry)
              ).grid(row=8, column=3)

        Button(self.__new_project_window, text="Close",
               command=self.close_new_proj).grid(row=9, column=0, pady=20)
        Button(self.__new_project_window, text="Create",
               command=self.heide.create_new_proj).grid(row=9,
                                                              column=1,
                                                              pady=30)

        self.__new_project_window.update()

    def close_new_proj(self):
        self.active_window = Window.HEIDE
        self.__new_project_window.destroy()