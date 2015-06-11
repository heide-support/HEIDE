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

from tkinter import *
from enum import Enum

from file_module import  File_Type


class Editor(Enum):
    PARAM_EDITOR, DATA_EDITOR, ALG_EDITOR = range(3)


class editor_module:
    def __init__(self, heide):
        self.heide = heide

        self.editor_dic = {Editor.PARAM_EDITOR: None,
                           Editor.DATA_EDITOR: None,
                           Editor.ALG_EDITOR: None}

        self.keys_pressed = {}

        self.param_bold = False
        self.data_bold = False
        self.alg_bold = False

    def set_editors(self, param_editor, data_editor, alg_editor):
        self.editor_dic[Editor.PARAM_EDITOR] = param_editor
        self.editor_dic[Editor.DATA_EDITOR] = data_editor
        self.editor_dic[Editor.ALG_EDITOR] = alg_editor

    def clr_and_fill_editor(self, which_editor, contents):
        editor = self.editor_dic[which_editor]
        self.clr_editor(editor)
        self.fill_editor(editor, contents)

    def get_editor_contents(self, which_editor):
        editor = self.editor_dic[which_editor]
        return editor.get("0.0", END)

    def clr_editors(self):
        for which_editor in self.editor_dic:
            self.clr_editor(self.editor_dic[which_editor])

    def clr_editor(self, editor):
        editor.delete("0.0", END)

    def fill_editor(self, editor, contents):
        editor.insert(INSERT, contents)

    def key_press(self, event):
        key = repr(event.keysym)

        self.keys_pressed[key] = 1
        dict_len = len(self.keys_pressed)

        # if the key pressed was F1 and there is no other keys being pressed
        # then run
        if key == "'F1'" and dict_len == 1:
            self.keys_pressed.clear()
            self.heide.heide_run()

        # If there is one thing in the dictionary then no command will be
        # executed. If there is more than two things then don't execute because
        # there should only be two.
        if dict_len != 2:
            return

        try:
            if self.keys_pressed["'Control_L'"] or \
                    self.keys_pressed["'Control_R'"]:
                if key == "'s'":
                    self.heide.heide_save(File_Type.PROJ_FILE)
                elif key == "'p'":
                    self.heide.heide_save(File_Type.PARAM_FILE)
                elif key == "'P'":
                    self.heide.heide_save_as(File_Type.PARAM_FILE)
                elif key == "'d'":
                    self.heide.heide_save(File_Type.DATA_FILE)
                elif key == "'D'":
                    self.heide.heide_save_as(File_Type.DATA_FILE)
                elif key == "'a'":
                    self.heide.heide_save(File_Type.ALG_FILE)
                elif key == "'A'":
                    self.heide.heide_save_as(File_Type.ALG_FILE)
                elif key == "'o'":
                    self.heide.heide_open(File_Type.PROJ_FILE, None)
                elif key == "'n'":
                    self.heide.heide_new_project()
                elif key == "'C'":
                    self.heide.heide_close_project()
                elif key == "'q'":
                    self.heide.heide_quit()

                valid_keys = ["'s'", "'p'", "'P'", "'d'", "'D'", "'a'", "'A'",
                              "'o'", "'n'", "'C'", "'q'"]

                if key in valid_keys:
                    self.keys_pressed.clear()
        except KeyError:
            pass

    def key_release(self, event):
        keys = self.keys_pressed.keys()
        if repr(event.keysym) in keys:
            del self.keys_pressed[repr(event.keysym)]

    def param_edit_modified(self, event):
        if not self.param_bold:
            self.heide.gui_mod.param_custom_font.configure(weight="bold")
            self.param_bold = True

    def data_edit_modified(self, event):
        if not self.data_bold:
            self.heide.gui_mod.data_custom_font.configure(weight="bold")
            self.data_bold = True

    def alg_edit_modified(self, event):
        if not self.alg_bold:
            self.heide.gui_mod.alg_custom_font.configure(weight="bold")
            self.alg_bold = True