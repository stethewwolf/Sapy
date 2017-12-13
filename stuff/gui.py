#!/usr/bin/env python

from sapy_lib.mom import Mom
from sapy_lib.datamgr import DataMgr
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from matplotlib.figure import Figure
from numpy import arange, pi, random, linspace
import matplotlib.cm as cm
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

_app_title="sapy"

class calendar_dialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self,"Calendar", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        
        self.calendar = Gtk.Calendar()
        box = self.get_content_area()
        box.add(self.calendar)

        self.show_all()

class warning_dialog(Gtk.Dialog):
    def __init__(self, parent, message):
        Gtk.Dialog.__init__(self,"Calendar", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        
        self.label = Gtk.Label(message)
        box = self.get_content_area()
        box.add(self.label)

        self.show_all()


class new_mom_dialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "New Lom", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)
        box = self.get_content_area()
        grid = Gtk.Grid()
        box.add(grid)

        label_price = Gtk.Label("price")
        self.price = Gtk.Entry()
        grid.add(label_price)
        grid.attach_next_to( self.price,label_price, Gtk.PositionType.RIGHT, 2, 1)

        label_cause = Gtk.Label("Cause")
        self.cause = Gtk.Entry()
        grid.attach_next_to(label_cause, label_price, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to( self.cause,label_cause, Gtk.PositionType.RIGHT, 2, 1)
        
        label_agent = Gtk.Label("Agent")
        self.agent = Gtk.Entry()
        grid.attach_next_to(label_agent, label_cause, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to( self.agent,label_agent, Gtk.PositionType.RIGHT, 2, 1)
        
        label_payee = Gtk.Label("Payee")
        self.payee = Gtk.Entry()
        grid.attach_next_to(label_payee, label_agent, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to( self.payee,label_payee, Gtk.PositionType.RIGHT, 2, 1)
        
        label_time = Gtk.Label("Time")
        self.time_button = Gtk.Button("Time")
        self.time_button.connect("clicked",self.display_calendar) 
        grid.attach_next_to(label_time, label_payee, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to( self.time_button,label_time, Gtk.PositionType.RIGHT, 2, 1)
         
        self.show_all()

    def get_mom(self):
        mom = Mom()
        mom.price(float(self.price.get_text()))
        mom.cause(self.cause.get_text())
        mom.agent(self.agent.get_text())
        mom.payee(self.payee.get_text())
        return mom
    
    def display_calendar ( self, widget ):
        dialog = calendar_dialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("do nothing")
        elif response == Gtk.ResponseType.CANCEL:
            print("Reverted")
            dialog.destroy()
            return

        dialog.destroy()

class lom_window ( Gtk.Window ):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.mom_list = Gtk.ListBox() 
        self.connect("delete-event", Gtk.main_quit)
        self.lom=None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.label = Gtk.Label("stuff")
        hbox.add(self.label)
        vbox.add(hbox)

        vbox.add(self.mom_list)

        vbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button = Gtk.Button(label="add mom")
        button.connect("clicked",self.add_mom)
        vbox2.add(button)
        button = Gtk.Button(label="remove mom")
        vbox2.add(button)
        button = Gtk.Button(label="close window")
        button.connect("clicked",self.stop)
        vbox2.add(button)
        vbox.add(vbox2)

        self.add(vbox)
        
    
    def run ( self, lom):
        self.lom=lom
        self.set_title("lom window")
        self.label.set_text(lom.Name)

        for mom in lom.Movements:
            line = Gtk.ListBoxRow()
            vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            label = Gtk.Label(mom.to_string())
            button = Gtk.Button("delete")
            button.lom = lom
            button.mom = mom
            button.box=vbox
            button.connect("clicked",self.rm_mom)
            vbox.add(label)
            vbox.add(button)           
            line.add(vbox)
            self.mom_list.add(line)
        self.show_all()

    def stop ( self, widget):
        self.hide()

    def add_mom ( self, widget ):
        dialog = new_mom_dialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.CANCEL:
            print("Reverted")
            dialog.destroy()
            return
        elif response == Gtk.ResponseType.OK:
            print("going on")
        mom = dialog.get_mom() 

        line = Gtk.ListBoxRow()
        label = Gtk.Label(mom.to_string())
        label.show()
        line.show()
        self.mom_list.add(line)
        self.lom.insert(mom)
        dialog.destroy()

    def rm_mom ( self, widget ):
        widget.box.hide()
        widget.lom.remove(widget.mom)
        pass
class new_lom_dialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "New Lom", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label("Insert the name of the new lom")

        box = self.get_content_area()
        box.add(label)

        self.entry = Gtk.Entry()
        self.entry.set_text("New Lom")
        box.add(self.entry)
        self.show_all()
    
    def get_text(self):
        return self.entry.get_text()

class delete_lom_dialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Delete Lom", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)
        self.parent = parent

        label = Gtk.Label("Select the lom you want delete")
        box = self.get_content_area()
        box.add(label)
        self.lom_list=Gtk.ListBox()
        for lom in parent.data_mgr.Lom_list:
            row = Gtk.ListBoxRow()
            button = Gtk.Button(label=lom.Name)
            button.lom = lom
            button.connect("clicked",self.delete_lom)
            row.add(button)
            self.lom_list.add(row)

        box.add(self.lom_list)
        self.show_all()
    
    def delete_lom(self, widget):
        self.parent.data_mgr.remove_lom(widget.lom)

        for tmp in self.parent.lom_list :
            print (tmp)
            if tmp.lom == widget.lom:
                tmp.hide()

        widget.hide()
    

class main_window(Gtk.Window):
    def __init__ ( self, data_mgr ):
        Gtk.Window.__init__(self,title=_app_title)
        self.connect("delete-event", Gtk.main_quit)
        self.data_mgr=data_mgr
        self.lom_win = lom_window()

        main_grid = Gtk.Grid()

        label=Gtk.Label("LOM")
        main_grid.add(label)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        main_grid.attach_next_to(hbox,label,Gtk.PositionType.BOTTOM,2,6)
        label=Gtk.Label("Name")
        hbox.add(label)
        label=Gtk.Label("Visible")
        hbox.add(label)

        self.lom_list=Gtk.ListBox()
        main_grid.attach_next_to(self.lom_list,hbox,Gtk.PositionType.BOTTOM,2,6)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        button = Gtk.Button(label="add")
        button.connect("clicked",self.create_lom)
        hbox.add(button)
        button = Gtk.Button(label="remove")
        button.connect("clicked",self.delete_lom)
        hbox.add(button)
        main_grid.attach_next_to(hbox,self.lom_list,Gtk.PositionType.BOTTOM,2,6)
        self.scroll = Gtk.ScrolledWindow()
        main_grid.attach_next_to(self.scroll,self.lom_list,Gtk.PositionType.RIGHT,2,6)
        button1 = Gtk.Button(label="stardate")
        button1.connect("clicked",self.set_start_date)

        main_grid.attach_next_to(button1,self.scroll,Gtk.PositionType.BOTTOM,2,6)
        button = Gtk.Button(label="enddate")
        button.connect("clicked",self.set_end_date)
        main_grid.attach_next_to(button,button1,Gtk.PositionType.RIGHT,2,6)
        fig = Figure(figsize=(5,5), dpi=100)
        ax = fig.add_subplot(111, projection='polar')

        N = 20
        theta = linspace(0.0, 2 * pi, N, endpoint=False)
        radii = 10 * random.rand(N)
        width = pi / 4 * random.rand(N)

        bars = ax.bar(theta, radii, width=width, bottom=0.0)

        for r, bar in zip(radii, bars):
            bar.set_facecolor(cm.jet(r / 10.))
            bar.set_alpha(0.5)

        ax.plot()

        canvas = FigureCanvas(fig)
        self.scroll.add_with_viewport(canvas)
        

        self.add(main_grid)
        
    def run(self):
        self.show_all()

    def update_lom_list ( self ):
        for lom in self.data_mgr.Lom_list:
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
            row.add(hbox)
            button = Gtk.Button(label=lom.Name)
            button.lom = lom 
            button.connect("clicked",self.show_lom)
            check = Gtk.CheckButton()
            check.lom = lom
            check.connect("toggled", self.toggle_check)
            hbox.pack_start(button, True, True, 0)
            hbox.pack_start(check, False, True, 0)
            self.lom_list.add(row)


    def create_lom ( self , widget ):
        dialog = new_lom_dialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("Name : "+dialog.get_text())
        elif response == Gtk.ResponseType.CANCEL:
            print("Reverted")
            dialog.destroy()
            return

        tmp = self.data_mgr.new_lom(dialog.get_text())
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        row.lom = tmp
        button = Gtk.Button(label=dialog.get_text())
        check = Gtk.CheckButton()
        hbox.pack_start(button, True, True, 0)
        hbox.pack_start(check, False, True, 0)
        self.lom_list.add(row)
        self.lom_list.show_all()
        dialog.destroy()

    def delete_lom( self, widget) :
        dialog = delete_lom_dialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("Name : ")
        elif response == Gtk.ResponseType.CANCEL:
            print("Reverted")
        dialog.destroy()

    def show_lom(self, widget ):
        self.lom_win.run(widget.lom)

    def toggle_check ( self, widget ):
        if widget.get_active() :
            widget.lom.visible(True)
        else:
            widget.lom.visible(False)

    def set_start_date (self,widget):
        dialog = calendar_dialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("do nothing")
        elif response == Gtk.ResponseType.CANCEL:
            print("Reverted")
            dialog.destroy()
            return

        dialog.destroy()

    def set_end_date (self,widget):
        dialog = calendar_dialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("do nothing")
        elif response == Gtk.ResponseType.CANCEL:
            print("Reverted")
            dialog.destroy()
            return

        dialog.destroy()

class gui():
    def __init__ (self, data_mgr):
        self.main_window=main_window(data_mgr)

    def run(self):
        self.main_window.update_lom_list()
        self.main_window.run()
        Gtk.main()
