#
#   File : main_window_toolbar.py
#   Author : stefano prina <stethewwolf@gmail.com>
#

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sapy_modules.gui.gtk.dialogs.select_lom_dialog import select_lom_dialog_view
from sapy_modules.gui.gtk.dialogs.add_mom_dialog import add_mom_dialog_view
from sapy_modules.gui.gtk.dialogs.del_mom_dialog import del_mom_dialog_view
from sapy_modules.gui.gtk.dialogs.update_mom_dialog import update_mom_dialog_view
from sapy_modules.gui.gtk.dialogs.plot_graph_dialog import plot_graph_dialog_view

from matplotlib.figure import Figure

# -- Buttons
# -- -- Select Lom Button
class sapy_select_lom_button(Gtk.ToolButton):
    def __init__(self, gtkWindow):
        Gtk.ToolButton.__init__(self)
        self.set_label("List")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow

    def on_button_clicked(self, widget):
        dialog = select_lom_dialog_view(self.gtkWindow)

        if dialog.run() == Gtk.ResponseType.OK:
            lom = dialog.get_selected_item()
            if lom: 
                self.gtkWindow.controller.set_list(lom)

        dialog.destroy()


# -- -- Add Mom Button
class sapy_add_mom_button(Gtk.ToolButton):
    def __init__(self, gtkWindow):
        Gtk.ToolButton.__init__(self)
        self.set_label("Add")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow

    def on_button_clicked(self, widget):
        dialog = add_mom_dialog_view(self.gtkWindow)

        if dialog.run() == Gtk.ResponseType.OK:
            new_mom = dialog.get_mom()
            self.gtkWindow.controller.add_mom(new_mom)

        dialog.destroy()

class sapy_del_mom_button(Gtk.ToolButton):
    def __init__(self, gtkWindow):
        Gtk.ToolButton.__init__(self)
        self.set_label("Del")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow

    def on_button_clicked(self, widget):
        dialog = del_mom_dialog_view(self.gtkWindow)

        if dialog.run() == Gtk.ResponseType.OK:
            self.gtkWindow.controller.del_mom()

        dialog.destroy()


class sapy_edit_mom_button(Gtk.ToolButton):
    def __init__(self, gtkWindow):
        Gtk.ToolButton.__init__(self)
        self.set_label("Edit")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow

    def on_button_clicked(self, widget):
        for mom_row in self.gtkWindow.controller.moms_store:
            if mom_row[4] == True:
                mom = self.gtkWindow.controller.lom.get_mom(id=mom_row[0])

                dialog = update_mom_dialog_view(self.gtkWindow,mom)
                
                if dialog.run() == Gtk.ResponseType.OK:
                    dialog.run_update_mom()
        
                dialog.destroy()
        
        self.gtkWindow.controller.rebuild_list()

class sapy_graph_button(Gtk.ToolButton):
    def __init__(self, gtkWindow):
        Gtk.ToolButton.__init__(self)
        self.set_label("Graph")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow

    def on_button_clicked(self, widget):
        dialog = plot_graph_dialog_view(self.gtkWindow)
        dialog.run()
        dialog.destroy()
        pass

class sapy_export_button(Gtk.ToolButton):
    def __init__(self, gtkWindow):
        Gtk.ToolButton.__init__(self)
        self.set_label("Export")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow

    def on_button_clicked(self, widget):
        pass

class sapy_import_button(Gtk.ToolButton):
    def __init__(self, gtkWindow):
        Gtk.ToolButton.__init__(self)
        self.set_label("Import")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow

    def on_button_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Select file to import", self.gtkWindow, Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        if dialog.run() == Gtk.ResponseType.OK:
            self.gtkWindow.controller.lom.csv_import(dialog.get_file())
        
        dialog.destroy()


# ----
class sapy_main_toolbar(Gtk.Toolbar):
    def __init__ (self, window):
        Gtk.Toolbar.__init__(self)
        self.gtkWindow = window

        self.add(sapy_select_lom_button(self.gtkWindow))

        self.add(sapy_add_mom_button(self.gtkWindow))

        self.add(sapy_del_mom_button(self.gtkWindow))

        self.add(sapy_edit_mom_button(self.gtkWindow))

        self.add(sapy_graph_button(self.gtkWindow))

        self.add(sapy_import_button(self.gtkWindow))

        #self.add(sapy_export_button(self.gtkWindow))



