#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import traceback

from gui_module import Window


class settings_module:
    def __init__(self, heide):
        self.heide = heide

        self.heide_proj_dir = "./HEIDE Projects"

        # default code source locations
        self.he_src = "../HElib_master/src"

        # max number of subprocess that can be spawned
        self.max_num_subpr = 4

        # should memory usage data be collected and displayed
        self.display_mem_usage = False


    def apply_settings(self):
        self.set_params(self.heide.gui_mod.get_settings())
        self.run_makefiles()

        self.heide.gui_mod.settings_window.destroy()
        self.heide.gui_mod.active_window = Window.HEIDE

    def set_params(self, contents):
        if contents == "":
            return

        data = json.loads(contents)

        for param in data:
            if param == "he_src":
                self.he_src = data[param]
            elif param == "max_num_subpr":
                self.max_num_subpr = data[param]
            elif param == "display_mem_usage":
                self.display_mem_usage = data[param]
            else:
                if self.heide.gui_mod.active_window == Window.START_UP:
                    self.heide.gui_mod.display_start_up_error(
                        "Invalid parameter '" + param + "' detected. "
                                                        "Stopping setup.")
                else:
                    self.heide.gui_mod.display_error("")

    def run_makefiles(self):
        cwd = os.getcwd()

        # change to proper directory and open subprocess to run makefile in
        # that directory
        # then wait for response and if it failed then display error and don't
        # continue
        for command in [self.he_src]:

            if self.heide.gui_mod.active_window == Window.START_UP:
                self.heide.gui_mod.set_command_label(
                    "Changing working directory "
                    "to " + command)
                self.heide.gui_mod.root.update()

            try:
                os.chdir(command)
            except FileNotFoundError:
                if self.heide.gui_mod.active_window == Window.START_UP:
                    self.heide.gui_mod.display_start_up_error("No such file or "
                                                              "directory: '" +
                                                              command + "'")
                    return
                elif self.heide.gui_mod.active_window == Window.SETTINGS:
                    error = sys.exc_info()
                    self.heide.gui_mod.display_error(error[0], error[1])
                    self.heide.file_mod.write_to_error_log_internal(error)
                    return
                else:
                    error = ["Unexpected Error",
                             "Invalid active_window.",
                             ''.join(traceback.format_stack())]
                    self.heide.gui_mod.display_error(error[0], error[1])
                    self.heide.file_mod.write_to_error_log_internal(error)
                    return
            except:
                if self.heide.gui_mod.active_window == Window.START_UP:
                    self.heide.gui_mod.display_start_up_error(
                        "Unexpected error" +
                        sys.exc_info()[0])
                    return
                elif self.heide.gui_mod.active_window == Window.SETTINGS:

                    self.heide.gui_mod.display_error("Compilation Error",
                                                     "Error running makefile")
                    self.heide.file_mod.write_to_error_log_internal(
                        sys.exc_info())
                    return
                else:
                    error = ["Unexpected Error",
                             "Invalid active_window.",
                             ''.join(traceback.format_stack())]
                    self.heide.gui_mod.display_error(error[0], error[1])
                    self.heide.file_mod.write_to_error_log_internal(error)
                    return

            if self.heide.gui_mod.active_window == Window.START_UP:
                self.heide.gui_mod.set_command_label("Running makefile in "
                                                     + command)
                self.heide.gui_mod.root.update()

            sub_pr = subprocess.Popen(["make"],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

            ret_val = sub_pr.wait()

            out, err = sub_pr.communicate()

            os.chdir(cwd)

            if ret_val != 0:
                self.heide.file_mod.write_to_error_log_subprocess(
                    self.heide.gui_mod.root, out, err)

                self.heide.gui_mod.display_start_up_error(
                    "An error occurred while"
                    " running the makefile "
                    "in " + command + ". The"
                                      " error was recorded in "
                                      "./logs/error_log")