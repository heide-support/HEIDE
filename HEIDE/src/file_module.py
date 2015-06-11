#    Copyright (C) 2015  Grant Frame
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from tkinter import filedialog
import datetime
from enum import Enum
import sys
import os
import traceback

class File_Type(Enum):
    PROJ_FILE, PARAM_FILE, DATA_FILE, ALG_FILE, CONFIG_FILE = range(5)

class file_module:
    def __init__(self, heide):
        self.heide = heide
        self.config_file = None
        self.proj_file = None
        self.param_file = None
        self.data_file = None
        self.alg_file = None

    def get_existing_loc(self, entry):
        entry.insert(0, filedialog.askopenfilename())

    def read_file(self, file_name, file_type):
        # 1. open file "file_name"
        # 2. read file
        # 3. set internal variable to keep track of open files
        try:
            file = open(file_name)
            contents = file.read()

            if file_type == File_Type.CONFIG_FILE:
                self.config_file = file_name
            elif file_type == File_Type.PROJ_FILE:
                self.proj_file = file_name
            elif file_type == File_Type.PARAM_FILE:
                self.param_file = file_name
            elif file_type == File_Type.DATA_FILE:
                self.data_file = file_name
            elif file_type == File_Type.ALG_FILE:
                self.alg_file = file_name
            else:
                error = ["Unexpected Error",
                         "Invalid File_Type",
                         ''.join(traceback.format_stack())]
                self.heide.gui_mod.display_error(error[0], error[1])
                self.write_to_error_log_internal(error)
                return ""

            return contents
        except:
            error = sys.exc_info()
            self.heide.gui_mod.display_error(error[0], error[1])
            self.write_to_error_log_internal(error)
            return ""

    def write_file(self, file_name, contents):
        try:
            file = open(file_name, "w")
            file.write(contents)
        except:
            error = sys.exc_info()
            self.heide.gui_mod.display_error(error[0], error[1])
            self.write_to_error_log_internal(error)
            return

    # used when writing errors that occured during a subprocess execution
    def write_to_error_log_subprocess(self, out, err):
        self.write_to_error_log("SUBPROCESS ERROR\n" +
                        "\nSTDOUT: \n" +
                        out.decode("utf-8") +
                        "\nSTDERR: \n" +
                        err.decode("utf-8"))

    # used for errors that occurred internally to heide
    def write_to_error_log_internal(self, error):
        self.write_to_error_log("INTERNAL ERROR\n" +
                                str(error[0]) + "\n" +
                                str(error[1]) + "\n" +
                                str(error[2]) + "\n")

    def write_to_error_log(self, message):
        now = datetime.datetime.now()

        try:
            error_log = open("./logs/error_log", "a")
            error_log.write("-" * 80 + "\n" +
                            str(now) + "\n" +
                            message)
            error_log.close()
        except:
            self.heide.gui_mod.display_error("File Write Error",
                                             "Error while writing to "
                                             "error log.\n" +
                                             str(sys.exc_info()[0]) + "\n")
            self.heide.gui_mod.root.quit()
            sys.exit()


    def open_file_proj(self):
        return self.open_read_file((("HEIDE proj files", "*.heide_proj"),
                               ("All Files", "*")), File_Type.PROJ_FILE)

    def open_file_param(self):
        return self.open_read_file((("HEIDE param files", "*.heide_params"),
                               ("All Files", "*")), File_Type.PARAM_FILE)

    def open_file_data(self):
        return self.open_read_file((("HEIDE data file", "*.heide_data"),
                               ("All Files", "*")), File_Type.ALG_FILE)

    def open_file_alg(self):
        return self.open_read_file((("HEIDE alg files", "*.heide_alg"),
                               ("All Files", "*")), File_Type.DATA_FILE)

    def open_read_file(self, file_types, file_type):
        file_name = filedialog.askopenfilename(filetypes=file_types)

        # For some reason if the user selects cancel on filedialog, the first
        # time it returns as () but then on subsequent calls it is empty.
        if str(file_name) == "" or str(file_name) == "()":
            return ""
        else:
            return self.read_file(file_name, file_type)

    def save_params(self, contents):
        self.save_to_file(File_Type.PARAM_FILE, self.param_file, contents)

    def save_data(self, contents):
        self.save_to_file(File_Type.DATA_FILE, self.data_file, contents)

    def save_alg(self, contents):
        self.save_to_file(File_Type.ALG_FILE, self.alg_file, contents)

    def save_as_params(self, contents):
        self.save_to_file(File_Type.PARAM_FILE, None, contents)

    def save_as_data(self, contents):
        self.save_to_file(File_Type.DATA_FILE, None, contents)

    def save_as_alg(self, contents):
        self.save_to_file(File_Type.ALG_FILE, None, contents)

    def save_to_file(self, file_type, file_name, contents):
        if file_name == None:
            file_name = filedialog.asksaveasfilename()

            # For some reason if the user selects cancel on filedialog, the first
            # time it returns as () but then on subsequent calls it is empty.
            # TODO look into this more?
            if str(file_name) == "" or str(file_name) == "()":
                return

            if file_type == File_Type.PARAM_FILE:
                self.param_file = file_name
                self.heide.gui_mod.param_custom_font.configure(weight="normal")
                self.heide.gui_mod.param_bold = False
            elif file_type == File_Type.DATA_FILE:
                self.data_file = file_name
                self.heide.gui_mod.data_custom_font.configure(weight="normal")
                self.heide.gui_mod.data_bold = False
            elif file_type == File_Type.ALG_FILE:
                self.alg_file = file_name
                self.heide.gui_mod.alg_custom_font.configure(weight="normal")
                self.heide.gui_mod.alg_bold = False
            else:
                error = ["Unexpected Error",
                         "Invalid File_Type.",
                         ''.join(traceback.format_stack())]
                self.heide.gui_mod.display_error(error[0], error[1])
                self.write_to_error_log_internal(error)
                return

        self.write_file(file_name, contents)

        if file_type == File_Type.PARAM_FILE:
            self.heide.gui_mod.param_custom_font.configure(weight="normal")
            self.heide.edit_mod.param_bold = False
        elif file_type == File_Type.DATA_FILE:
            self.heide.gui_mod.data_custom_font.configure(weight="normal")
            self.heide.edit_mod.data_bold = False
        elif file_type == File_Type.ALG_FILE:
            self.heide.gui_mod.alg_custom_font.configure(weight="normal")
            self.heide.edit_mod.alg_bold = False
        else:
            error = ["Unexpected Error",
                     "Invalid File_Type.",
                     ''.join(traceback.format_stack())]
            self.heide.gui_mod.display_error(error[0], error[1])
            self.write_to_error_log_internal(error)
            return

    def create_proj(self, he_src, proj_loc, proj_name,
                    existing_param, existing_data, existing_alg):

        # format file contents so that it is the string form of the
        # json object which holds the data.
        file_contents = "{\n\t" + self.format_settings_entry(he_src) + \
                        "\n\t\"param_file\": " + \
                        self.format_file_entry(proj_loc, proj_name,
                                          File_Type.PARAM_FILE) + \
                        ",\n\t\"data_file\": " + \
                        self.format_file_entry(proj_loc, proj_name,
                                          File_Type.DATA_FILE) + \
                        ",\n\t\"alg_file\": " + \
                        self.format_file_entry(proj_loc, proj_name,
                                          File_Type.ALG_FILE) + \
                        "\n}"

        try:
            os.mkdir(proj_loc + "/" + proj_name)
        except:
            error = sys.exc_info()
            self.heide.gui_mod.display_error(error[0], error[1])
            return

        base_file_name = proj_loc + "/" + proj_name + "/" + proj_name
        proj_file_name = base_file_name + ".heide_proj"
        params_file_name = base_file_name + ".heide_params"
        data_file_name = base_file_name + ".heide_data"
        alg_file_name = base_file_name + ".heide_alg"

        # write project file and set internal variable to keep track of open
        # file
        self.write_file(proj_file_name, file_contents)
        self.proj_file = proj_file_name

        # for the param, data, and alg file
        #   if importing from an existing file read existing file's contents
        #   and then write to project file
        # set internal variable to keep track of open file
        if existing_param != "":
            contents = self.read_file(existing_param, File_Type.PARAM_FILE)
        else:
            contents = "pd = {\t\"p\" : 65537,\n" \
                       "\t\"r\" : 1, \n" \
                       "\t\"L\" : 15, \n" \
                       "\t\"w\" : 64, \n" \
                       "\t\"d\" : 0, \n" \
                       "\t\"security\" : 128} \n" \
                       "\n%+pd\n"

        self.write_file(params_file_name, contents)
        self.param_file = params_file_name

        if existing_data != "":
            contents = self.read_file(existing_data, File_Type.DATA_FILE)
        else:
            contents = ""

        self.write_file(data_file_name, contents)
        self.data_file = data_file_name

        if existing_alg != "":
            contents = self.read_file(existing_alg, File_Type.ALG_FILE)
        else:
            contents = ""

        self.write_file(alg_file_name, contents)
        self.alg_file = alg_file_name

    def format_settings_entry(self, he_src):
        return "\"settings\": {\n\t\t\"he_src\": \"" + he_src + "\"\n\t},"


    def format_file_entry(self, proj_loc, proj_name, file_type):
        if file_type == File_Type.PARAM_FILE:
            return "\"" + proj_loc + "/" + proj_name + "/" + proj_name + \
                   ".heide_params\""
        elif file_type == File_Type.DATA_FILE:
            return "\"" + proj_loc + "/" + proj_name + "/" + proj_name + \
                   ".heide_data\""
        elif file_type == File_Type.ALG_FILE:
            return "\"" + proj_loc + "/" + proj_name + "/" + proj_name + \
                   ".heide_alg\""
        else:
            error = ["Unexpected Error",
                     "Invalid File_Type.",
                     ''.join(traceback.format_stack())]
            self.heide.gui_mod.display_error(error[0], error[1])
            self.write_to_error_log_internal(error)
            return

    def clear_files(self):
        self.proj_file = None
        self.param_file = None
        self.data_file = None
        self.param_file = None
