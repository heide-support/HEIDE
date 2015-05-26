#!/usr/bin/env python3

import json
import subprocess
from tkinter import messagebox
from io import StringIO
import ast
import psutil
from time import sleep
from time import time

from file_module import *
from editor_module import *
from gui_module import gui_module
from settings_module import settings_module
from gui_module import Window

class heide:
    def __init__(self):
        # HEIDE modules
        self.file_mod = file_module(self)
        self.edit_mod = editor_module(self)
        self.gui_mod = gui_module(self)
        self.set_mod = settings_module(self)

        self.running_processes = []

        # Create and display startup window
        self.gui_mod.spawn_start_up_window()

        # On startup:
        #   1. read config.heide to get HEIDE default parameter values
        #   2. build latest HE code by running makefiles
        self.set_mod.set_params(
            self.file_mod.read_file("config.heide", File_Type.CONFIG_FILE))
        self.set_mod.run_makefiles()

        # Everything worked so display HEIDE window
        self.gui_mod.set_command_label("Everything up to date. "
                                       "Starting HEIDE.")
        self.gui_mod.root.update()

        self.gui_mod.spawn_heide_window()

    def heide_run(self):
        # get run params
        run_configs = self.get_run_params()
        if not run_configs:
            return

        # get data
        data = self.get_data()
        if data == "":
            return

        # build AST from alg editor code
        alg = self.get_alg()
        if alg is "":
            return

        og_dir = os.getcwd()
        os.chdir("./tmp")

        try:
            # run a subprocess for each configuration
            self.gui_mod.spawn_heide_console_window()

            run_cnt = 0
            num_configs = len(run_configs)
            if self.set_mod.display_mem_usage:
                mem_usages = [[[], []] for _ in run_configs]
            out_vals = []
            err_vals = []
            ret_vals = []
            while run_cnt < num_configs:
                # if the console window was closed then stop running and
                # just return
                if self.gui_mod.active_window == Window.HEIDE:
                    return

                rng = min(self.set_mod.max_num_subpr, num_configs - run_cnt)
                for _ in range(rng):
                    command = "python2.7"
                    sub_pr = subprocess.Popen([command,
                                               "alg_run_file.py",
                                               str(run_configs[run_cnt]),
                                               str(data)],
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
                    self.running_processes.append(sub_pr)

                    run_cnt += 1

                # make a copy so that after deleting you can still get
                # the correct index of elements in original list
                run_proc_cpy = self.running_processes.copy()

                while self.running_processes:
                    for sub_pr in self.running_processes:
                        if self.set_mod.display_mem_usage:
                            proc = psutil.Process(sub_pr.pid)
                            mem = proc.get_memory_info()[0] / float(2 ** 20)

                        # get location within running processes
                        idx = run_proc_cpy.index(sub_pr)
                        # reset to be location within overall run
                        idx = (run_cnt - rng) + idx

                        if self.set_mod.display_mem_usage:
                            mem_usages[idx][0].append(int(round(time() * 1000)))
                            mem_usages[idx][1].append(mem)

                        if sub_pr.poll() is None:
                            self.gui_mod.output_window.update()
                            sleep(.05)
                        else:
                            out, err = sub_pr.communicate()
                            ret_val = sub_pr.returncode

                            out_vals.insert(idx, out)
                            err_vals.insert(idx, err)
                            ret_vals.insert(idx, ret_val)

                            self.running_processes.remove(sub_pr)

            l = len(run_configs)
            for i in range(l):
                config_str = "RUN_PARAMS: " + str(run_configs[i]) + "\n"
                self.gui_mod.heide_console_display_result(config_str,
                                                          ret_vals[i],
                                                          out_vals[i],
                                                          err_vals[i])
                self.gui_mod.load_bar_label.after_cancel(
                    self.gui_mod.load_bar_label.cancel)
                self.gui_mod.load_bar_label.pack_forget()
                self.gui_mod.output_window.update()

            os.chdir(og_dir)

        except Exception as excp:
            # go back to original directory
            os.chdir(og_dir)

            # close the console window if open
            if self.gui_mod.active_window == Window.CONSOLE:
                self.gui_mod.close_console()

            # this error has to do with the animation that was displayed
            # on the console window so ignore it
            if excp.args[0][:len("invalid command name")] == \
                    "invalid command name":
                return


            e = sys.exc_info()
            error = ["Runtime Error",
                     e[1],
                     ''.join(traceback.format_stack())]
            self.gui_mod.display_error(error[0], error[1])
            self.file_mod.write_to_error_log_internal(error)
            return


        if self.set_mod.display_mem_usage:
            # plot memory usage
            import matplotlib.pyplot as plt
            for i in range(l):
                # scale 'time' info back so axis is 0 based
                smallest_time = min(mem_usages[i][0])
                mem_usages[i][0] = [(elt - smallest_time) / 1000
                                    for elt in mem_usages[i][0]]

                plt.figure(i + 1)
                plt.plot(mem_usages[i][0], mem_usages[i][1])
                plt.ylabel("Memory Usage (MBs)")
                plt.xlabel("Real Time (Seconds)")
                config_str = "RUN_PARAMS: " + str(run_configs[i]) + "\n"
                plt.title(config_str)

            # reset back to first plot and show all plots
            plt.figure(1)
            plt.show()

    def get_run_params(self):
        contents = self.edit_mod.editor_dic[Editor.PARAM_EDITOR].get(0.0, END)

        # replace all cases of %+ with RUN_PARAMS.append(<var>)
        # unless this line is a comment
        vars = list(set(re.findall("(?<=\%\+).+", contents)))
        if vars is not None:
            for var in vars:
                while True:
                    old_contents = contents
                    contents = re.sub(r"^(?!#)(.*)\%\+" + re.escape(var),
                                      r"\1RUN_PARAMS.append(" + var + ")",
                                      contents, flags=re.M)

                    if old_contents == contents:
                        break

        old_stdout = sys.stdout
        new_stdout = sys.stdout = StringIO()

        code = "RUN_PARAMS = []\n" + \
               contents + \
               "print(RUN_PARAMS)"
        try:
            exec(code)
        except:
            error = sys.exc_info()
            self.gui_mod.display_error("Param Editor Error", error[1])
            return

        sys.stdout = old_stdout

        try:
            run_configs = ast.literal_eval(new_stdout.getvalue())
        except:
            error = sys.exc_info()
            self.gui_mod.display_error("Param Editor Error", error[1])
            return

        if not run_configs:
            return

        required_params = ["p", "r", "L", "d", "w", "security"]
        optional_params_dic_int = {"c": 2, "m": -1}
        optional_params_dic_list = { "gens": [], "ords": []}

        for configuration in run_configs:
            for param in configuration.keys():
                if (param not in required_params) and \
                   (param not in optional_params_dic_int.keys()) and \
                   (param not in optional_params_dic_list.keys()):
                        error = ["Invalid Parameter",
                                 param + " is an invalid parameter.",
                                 ''.join(traceback.format_stack())]
                        self.gui_mod.display_error(error[0], error[1])
                        return

            for req_param in required_params:
                if req_param not in configuration.keys():
                    error = ["Unspecified Parameter",
                             "Required parameter " + req_param + " has no value.",
                             ''.join(traceback.format_stack())]
                    self.gui_mod.display_error(error[0], error[1])
                    return
                elif type(configuration[req_param]) is not int:
                    error = ["Invalid Parameter",
                             req_param + " must be an integer.",
                             ''.join(traceback.format_stack())]
                    self.gui_mod.display_error(error[0], error[1])
                    return

            for opt_param in optional_params_dic_int.keys():
                if opt_param not in configuration.keys():
                    configuration[opt_param] = optional_params_dic_int[opt_param]
                elif type(configuration[opt_param]) is not int:
                    error = ["Invalid Parameter",
                             opt_param + " must be an integer.",
                             ''.join(traceback.format_stack())]
                    self.gui_mod.display_error(error[0], error[1])
                    return

            for opt_param in optional_params_dic_list.keys():
                if opt_param not in configuration.keys():
                    configuration[opt_param] = optional_params_dic_list[opt_param]
                elif type(configuration[opt_param]) is not list:
                    error = ["Invalid Parameter",
                             opt_param + " must be an list.",
                             ''.join(traceback.format_stack())]
                    self.gui_mod.display_error(error[0], error[1])
                    return

        return run_configs

    def get_data(self):
        data = {}

        # read contents of data editor
        contents = self.edit_mod.editor_dic[Editor.DATA_EDITOR].get("0.0", END)

        # if no contents then don't run
        if contents == "":
            return data

        # replace all cases of $.<var> with DATA["<var>"]
        # unless this line is a comment
        vars = list(set(re.findall("(?<=\$\.)\w+", contents)))
        if vars is not None:
            for var in vars:
                while True:
                    old_contents = contents
                    contents = re.sub(r"^(?!#)(.*)\$\." + re.escape(var),
                                      r"\1DATA['" + var + "']",
                                      contents, flags=re.M)

                    if old_contents == contents:
                        break

        # replace all cases of $+<var> with DATA[<var>]
        # unless this line is a comment
        vars = list(set(re.findall("(?<=\$\+)\w+", contents)))
        if vars is not None:
            for var in vars:
                while True:
                    old_contents = contents
                    contents = re.sub(r"^(?!#)(.*)\$\+" + re.escape(var),
                                      r"\1DATA[" + var + "]",
                                      contents, flags=re.M)

                    if old_contents == contents:
                        break

        old_stdout = sys.stdout
        new_stdout = sys.stdout = StringIO()
        code = "DATA = {}\n" + \
               contents + \
               "print(DATA)"
        try:
            exec(code)
        except:
            error = sys.exc_info()
            self.gui_mod.display_error("Data Editor Error", error[1])
            return

        sys.stdout = old_stdout

        try:
            data = ast.literal_eval(new_stdout.getvalue())
        except:
            error = sys.exc_info()
            self.gui_mod.display_error("Data Editor Error", error[1])
            return

        return data

    def get_alg(self):

        # read contents of alg editor
        contents = self.edit_mod.editor_dic[Editor.ALG_EDITOR].get("0.0", END)

        if contents == "":
            return contents

        extra_cmds = "\n\tfor key in DATA:\n" + \
                     "\t\tDATA[key] = PyPtxt(DATA[key], HE)\n\n"


        # replace all cases of := <var> with = _set_(<var>)
        # unless this line is a comment
        vars = list(set(re.findall("(?<=:= )\w+", contents)))
        if vars is not None:
            for var in vars:
                while True:
                    old_contents = contents
                    contents = re.sub(r"^(?!#)(.*):= " + re.escape(var),
                                      "= _set_(" + var + ")",
                                      contents, flags=re.M)

                    if old_contents == contents:
                        break

        # replace all cases of &<var> with <var> = HE.encrypt(<var>)
        # unless this line is a comment
        vars = list(set(re.findall("(?<=\&)[a-zA-Z0-9_$.]+", contents)))
        if vars is not None:
            for var in vars:
                if var == "$":
                    while True:
                        old_contents = contents
                        contents = re.sub(r"^(?!#)(.*)\&" + re.escape(var),
                                          "for key in DATA:\n"
                                          "\tDATA[key] = HE.encrypt(DATA[key])\n",
                                          contents, flags=re.M)

                        if old_contents == contents:
                            break
                else:
                    while True:
                        old_contents = contents
                        contents = re.sub(r"^(?!#)(.*)\&" + re.escape(var),
                                          r"\1" + var + " = HE.encrypt(" + var + ")",
                                          contents, flags=re.M)

                        if old_contents == contents:
                            break

        # replace all cases of *<var> with HE.decrypt(<var>)
        # unless this line is a comment
        vars = list(set(re.findall("(?<=\*)[a-zA-Z0-9_$.]+", contents)))
        if vars is not None:
            for var in vars:
                if var == "$":
                    while True:
                        old_contents = contents
                        contents = re.sub(r"^(?!#)(.*)\*" + re.escape(var),
                                          "for key in DATA:\n"
                                          "\tDATA[key] = HE.decrypt(DATA[key])\n",
                                          contents, flags=re.M)
                        if old_contents == contents:
                            break
                else:
                    while True:
                        old_contents = contents
                        contents = re.sub(r"^(?!#)(.*)\*" + re.escape(var),
                                          r"\1HE.decrypt(" + var + ")",
                                          contents, flags=re.M)

                        if old_contents == contents:
                            break

        # replace all cases of $.<var> with DATA["<var>"]
        # unless this line is a comment
        vars = list(set(re.findall("(?<=\$\.)\w+", contents)))
        if vars is not None:
            for var in vars:
                while True:
                    old_contents = contents
                    contents = re.sub(r"^(?!#)(.*)\$\." + re.escape(var),
                                      r"\1DATA['" + var + "']",
                                      contents, flags=re.M)

                    if old_contents == contents:
                        break

        # replace all cases of $@<ref> with DATA[DATA.keys()[<ref>]]
        # unless this line is a comment
        # NOTE: <ref> can't have spaces in it currently TODO change that?
        vars = list(set(re.findall("(?<=\$\@)[a-zA-z0-9\+\-\*\/]+",
                                   contents)))
        # reorder list so that longest vars are matched first
        vars.sort(key=len)
        vars = list(reversed(vars))
        if vars is not None:
            for var in vars:
                while True:
                    old_contents = contents
                    contents = re.sub(r"^^(?!#)(.*)\$\@" +  re.escape(var),
                                      r"\1DATA[DATA.keys()[" + var + "]]",
                                      contents, flags=re.M)

                    if old_contents == contents:
                        break



        while True:
            old_contents = contents
            contents = re.sub(r"^(?!#)(.*)\$", r"\1DATA", contents, flags=re.M)

            if old_contents == contents:
                break

        lines = contents.split("\n")

        new_lines = ["\t" + line + "\n" for line in lines]

        alg_file_contents = "import sys\n" + \
                            "import ast\n" + \
                            "sys.path.append('../../PyHE/')\n" + \
                            "from PyHE import PyHE\n" + \
                            "from PyPtxt import PyPtxt\n" + \
                            "from PyCtxt import PyCtxt\n" + \
                            "_set_ = lambda c: c.set()" + \
                            "\ndef run_heide_alg(RUN_PARAMS, DATA):\n" + \
                            "\tHE = PyHE()\n" + \
                            "\tHE.keyGen(RUN_PARAMS)\n" + \
                            extra_cmds + \
                            "".join(new_lines) + \
                            "\n\n" + \
                            "if __name__ == '__main__':\n" + \
                            "\trun_heide_alg(ast.literal_eval(sys.argv[1]), \n" \
                             "\t\t\tast.literal_eval(sys.argv[2]))\n"

        f = open("tmp/alg_run_file.py", "w")
        f.write(alg_file_contents)
        f.close()

        return alg_file_contents

    def heide_save_console_output(self):
        contents = self.gui_mod.output_text.get("0.0", END)

        file_name = filedialog.asksaveasfilename()

        self.file_mod.write_file(file_name, contents)

    def heide_open(self, file_type, contents):
        # 1. if opening a:
        #   1. project file, first check if:
        #       1. you have read the contents of the file, if not then read
        #       the file.
        #       2. then
        #           1. if the file was empty, return (nothing to do)
        #           2. else parse the json object in the file and
        #               1. change setting params to those in file
        #               2. open the param file, data file, and alg file
        #   2. else if opening a project file, data file, or algorithm file
        #       1. if you haven't read contents of the file then read them
        #       2. fill the appropriate editor with the contents
        #   3. else throw an error
        if file_type == File_Type.PROJ_FILE:
            if contents is None:
                contents = self.file_mod.open_file_proj()

            if contents == "":
                return
            else:
                try:
                    data = json.loads(contents)

                    self.set_mod.set_params(
                        str(data["settings"]).replace("'", "\""))
                    self.set_mod.run_makefiles()

                    self.heide_open(
                        File_Type.PARAM_FILE,
                        self.file_mod.read_file(data["param_file"],
                                                File_Type.PARAM_FILE))
                    self.heide_open(
                        File_Type.DATA_FILE,
                        self.file_mod.read_file(data["data_file"],
                                                File_Type.DATA_FILE))
                    self.heide_open(
                        File_Type.ALG_FILE,
                        self.file_mod.read_file(data["alg_file"],
                                                File_Type.ALG_FILE))
                except:
                    self.gui_mod.display_error(sys.exc_info()[0],
                                               sys.exc_info()[1])

                    self.file_mod.write_to_error_log_internal(sys.exc_info())
                    return


        elif file_type == File_Type.PARAM_FILE:
            if contents is None:
                contents = self.file_mod.open_file_param()

            self.edit_mod.clr_and_fill_editor(Editor.PARAM_EDITOR, contents)
        elif file_type == File_Type.DATA_FILE:
            if contents is None:
                contents = self.file_mod.open_file_data()

            self.edit_mod.clr_and_fill_editor(Editor.DATA_EDITOR, contents)
        elif file_type == File_Type.ALG_FILE:
            if contents is None:
                contents = self.file_mod.open_file_alg()

            self.edit_mod.clr_and_fill_editor(Editor.ALG_EDITOR, contents)
        else:
            error = ["Unexpected Error",
                     "Invalid File_Type.",
                     ''.join(traceback.format_stack())]
            self.gui_mod.display_error(error[0], error[1])
            self.file_mod.write_to_error_log_internal(error)
            return

    def heide_save(self, file_type):
        # 1. if saving a project
        #   1. make sure one is open first
        #   2. if one is open then save the param, data, and algorithm editor
        #       contents
        # 2. else if saving a param, data, or alg file
        #   1. get the contents of the appropriate editor window
        #   2. save the contents to the appropriate file
        # 3. else report an error
        if file_type == File_Type.PROJ_FILE:
            if self.file_mod.proj_file == None:
                self.gui_mod.display_error("No Project Open",
                                           "Please create a new or open an "
                                           "existing project before saving.")
                return
            else:
                self.heide_save(File_Type.PARAM_FILE)
                self.heide_save(File_Type.DATA_FILE)
                self.heide_save(File_Type.ALG_FILE)
        elif file_type == File_Type.PARAM_FILE:
            contents = self.edit_mod.get_editor_contents(Editor.PARAM_EDITOR)

            self.file_mod.save_params(contents)
        elif file_type == File_Type.DATA_FILE:
            contents = self.edit_mod.get_editor_contents(Editor.DATA_EDITOR)

            self.file_mod.save_data(contents)
        elif file_type == File_Type.ALG_FILE:
            contents = self.edit_mod.get_editor_contents(Editor.ALG_EDITOR)

            self.file_mod.save_alg(contents)
        else:
            error = ["Unexpected Error",
                     "Invalid File_Type.",
                     ''.join(traceback.format_stack())]
            self.gui_mod.display_error(error[0], error[1])
            self.file_mod.write_to_error_log_internal(error)
            return

    def heide_save_as(self, file_type):
        # save as takes the same form as save except call save_as_<filetype>
        # instead of save_<filetype>
        if file_type == File_Type.PARAM_FILE:
            contents = self.edit_mod.get_editor_contents(Editor.PARAM_EDITOR)

            self.file_mod.save_as_params(contents)
        elif file_type == File_Type.DATA_FILE:
            contents = self.edit_mod.get_editor_contents(Editor.DATA_EDITOR)

            self.file_mod.save_as_data(contents)
        elif file_type == File_Type.ALG_FILE:
            contents = self.edit_mod.get_editor_contents(Editor.ALG_EDITOR)

            self.file_mod.save_as_alg(contents)
        else:
            error = ["Unexpected Error",
                     "Invalid File_Type.",
                     ''.join(traceback.format_stack())]
            self.gui_mod.display_error(error[0], error[1])
            self.file_mod.write_to_error_log_internal(error)
            return

    def heide_new_project(self):
        self.gui_mod.spawn_new_project_window()

    def create_new_proj(self):
        # 1. read the entries provided on the new_project_window
        # 2. make sure required entries are filled out
        # 3. create the project file
        # 4. close the new project window
        # 5. open the new project
        he_src, proj_loc, proj_name = \
            [self.gui_mod.he_src_entry_np.get(),
             self.gui_mod.project_loc_entry.get(),
             self.gui_mod.project_name_entry.get()]

        existing_param, existing_data, existing_alg = \
            [self.gui_mod.existing_params_entry.get(),
             self.gui_mod.existing_data_entry.get(),
             self.gui_mod.existing_alg_entry.get()]

        for entry in [he_src, proj_loc, proj_name]:
            if entry == "":
                self.gui_mod.display_error("Invalid Entry",
                                           "Cannot leave entry blank")
                return

        self.file_mod.create_proj(he_src, proj_loc,
                                        proj_name, existing_param,
                                        existing_data, existing_alg)
        self.gui_mod.close_new_proj()

        self.heide_open(File_Type.PROJ_FILE,
                        self.file_mod.read_file("./" + proj_loc +
                                                "/" + proj_name +
                                                "/" + proj_name +
                                                ".heide_proj",
                                                File_Type.PROJ_FILE))

    def heide_import(self, file_type):
        # can't import to a project unless one is open
        if self.file_mod.proj_file == None:
            self.gui_mod.display_error("No Project Open",
                                       "A project must be open "
                                       "before importing.")
            return

        # 1. if file is a param, data, or alg file
        #   1. write to the projects file the contents of the chosen
        #       import file
        #   2. read from the projects file to get new contents
        #   3. display those new contents in appropriate editor
        # 2. else report error
        if file_type == File_Type.PARAM_FILE:
            self.file_mod.write_file(self.file_mod.param_file,
                                     self.file_mod.read_file(
                                         filedialog.askopenfilename(),
                                         File_Type.PARAM_FILE))
            contents = self.file_mod.read_file(self.file_mod.param_file,
                                               File_Type.PARAM_FILE)
            self.edit_mod.clr_and_fill_editor(Editor.PARAM_EDITOR, contents)
        elif file_type == File_Type.DATA_FILE:
            self.file_mod.write_file(self.file_mod.data_file,
                                     self.file_mod.read_file(
                                         filedialog.askopenfilename(),
                                         File_Type.DATA_FILE))
            contents = self.file_mod.read_file(self.file_mod.data_file,
                                               File_Type.DATA_FILE)
            self.edit_mod.clr_and_fill_editor(Editor.DATA_EDITOR, contents)
        elif file_type == File_Type.ALG_FILE:
            self.file_mod.write_file(self.file_mod.alg_file,
                                     self.file_mod.read_file(
                                         filedialog.askopenfilename(),
                                         File_Type.ALG_FILE))
            contents = self.file_mod.read_file(self.file_mod.alg_file,
                                               File_Type.ALG_FILE)
            self.edit_mod.clr_and_fill_editor(Editor.ALG_EDITOR, contents)
        else:
            error = ["Unexpected Error",
                     "Invalid File_Type.",
                     ''.join(traceback.format_stack())]
            self.gui_mod.display_error(error[0], error[1])
            self.file_mod.write_to_error_log_internal(error)
            return

    def heide_close_project(self):
        # can't close a project unless one is open
        if self.file_mod.proj_file == None:
            self.gui_mod.display_error("No Project Open",
                                       "A project must be open "
                                       "to close it.")
            return

        # 1. save the project
        # 2. clear the editors
        # 3. clear internal variables that point to which files are open
        self.heide_save(File_Type.PROJ_FILE)
        self.edit_mod.clr_editors()
        self.file_mod.clear_files()

    def heide_quit(self):

        ret = messagebox.askokcancel("Are you sure?",
                                     "Clicking Ok will erase "
                                     "all unsaved changes.")

        if ret:
            self.gui_mod.root.quit()

if __name__ == '__main__':
    try:
        heide()
    except:
        error = sys.exc_info()
        print(str(error[0]) + "\n" +
              str(error[1]) + "\n" +
              str(error[2]) + "\n")
