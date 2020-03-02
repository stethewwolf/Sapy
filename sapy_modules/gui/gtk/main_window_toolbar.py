import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from sapy_modules.gui.gtk.dialogs.select_lom_dialog_view import select_lom_dialog_view


class sapy_select_lom_button(Gtk.ToolButton):
    def __init__(self, gtkWindow):
        Gtk.ToolButton.__init__(self)
        self.set_label("select lom")
        self.connect("clicked",self.on_button_clicked)
        self.gtkWindow = gtkWindow

    def on_button_clicked(self, widget):
        dialog = select_lom_dialog_view(self.gtkWindow)
        dialog.run()
        dialog.get_selected_item()
        dialog.destroy()


class sapy_main_toolbar(Gtk.Toolbar):
    def __init__ (self, window):
        Gtk.Toolbar.__init__(self)
        self.gtkWindow = window

        self.add(sapy_select_lom_button(self.gtkWindow))



