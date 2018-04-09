#!/usr/bin/env python3
import wx, os, effects
from PIL import Image
import time

class MainGUI(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(1000,600))
        self.panel = wx.Panel(self)
        self.filePath = ""
        self.wildcard = "images (*.jpeg,*.jpg,*.png)|*.jpeg;*.jpg;*.png"
        self.photoWidth = 600
        self.photoHeight = 800
        self.wxImage = wx.Image(self.photoWidth,self.photoHeight)
        self.imageFrame = wx.StaticBitmap(self.panel,wx.ID_ANY,wx.Bitmap(self.wxImage))
        self.PIL_image = None
        #self.OG_bands = None
        self.old_shift = 0

        #File Menu
        fileMenu = wx.Menu()
        menuOpen = fileMenu.Append(wx.ID_OPEN,"Choose Image","Open an image to edit")
        menuSave = fileMenu.Append(wx.ID_SAVE,"Save Image","Save the image over itself")
        menuSaveAs = fileMenu.Append(wx.ID_SAVEAS,"Save Image As","Save a new image")
        menuExit = fileMenu.Append(wx.ID_EXIT,"Exit","Close this program")

        #Help Menu
        helpMenu = wx.Menu()
        menuAbout = helpMenu.Append(wx.ID_ABOUT,"About","Information about this program")

        menu = wx.MenuBar()
        menu.Append(fileMenu,"File")
        menu.Append(helpMenu,"Help")
        self.SetMenuBar(menu)
        
        #Button
        resetButton = wx.Button(self.panel,label="Reset Image")
        saveButton = wx.Button(self.panel,label="Save Image")
        openButton = wx.Button(self.panel,label="Open Image")

        #StaticText
        Xlabel = wx.StaticText(self.panel,label="X")
        Ylabel = wx.StaticText(self.panel,label="Y")
        Rlabel = wx.StaticText(self.panel,label="Red:")
        Glabel = wx.StaticText(self.panel,label="Green:")
        Blabel = wx.StaticText(self.panel,label="Blue:")

        #SpinCtrl
        self.RslideX = wx.SpinCtrl(self.panel,min=-500,max=500)
        self.RslideY = wx.SpinCtrl(self.panel,min=-500,max=500)

        self.GslideX = wx.SpinCtrl(self.panel,min=-500,max=500)
        self.GslideY = wx.SpinCtrl(self.panel,min=-500,max=500)
        
        self.BslideX = wx.SpinCtrl(self.panel,min=-500,max=500)
        self.BslideY = wx.SpinCtrl(self.panel,min=-500,max=500)

        self.RslideX.name = "redX"
        self.RslideY.name = "redY"
        self.GslideX.name = "greenX"
        self.GslideY.name = "greenY"
        self.BslideX.name = "blueX"
        self.BslideY.name = "blueY"

        #Layout
        topLayout = wx.BoxSizer(wx.HORIZONTAL)
        labelLayout = wx.BoxSizer(wx.HORIZONTAL)
        controlLayout = wx.BoxSizer(wx.VERTICAL)
        RLayout = wx.BoxSizer(wx.HORIZONTAL)
        GLayout = wx.BoxSizer(wx.HORIZONTAL)
        BLayout = wx.BoxSizer(wx.HORIZONTAL)
        ButtonLayout = wx.BoxSizer(wx.HORIZONTAL)

        labelLayout.AddSpacer(125)
        labelLayout.Add(Xlabel,0,wx.ALL,5)
        labelLayout.AddSpacer(125)
        labelLayout.Add(Ylabel,0,wx.ALL,5)

        RLayout.Add(Rlabel,0,wx.ALL|wx.ALIGN_LEFT,5)
        RLayout.AddSpacer(12)
        RLayout.Add(self.RslideX,0,wx.ALL|wx.ALIGN_RIGHT,5)
        RLayout.Add(self.RslideY,0,wx.ALL|wx.ALIGN_RIGHT,5)

        GLayout.Add(Glabel,0,wx.ALL|wx.ALIGN_LEFT,5)
        GLayout.Add(self.GslideX,0,wx.ALL|wx.ALIGN_RIGHT,5)
        GLayout.Add(self.GslideY,0,wx.ALL|wx.ALIGN_RIGHT,5)

        BLayout.Add(Blabel,0,wx.ALL|wx.ALIGN_LEFT,5)
        BLayout.AddSpacer(10)
        BLayout.Add(self.BslideX,0,wx.ALL|wx.ALIGN_RIGHT,5)
        BLayout.Add(self.BslideY,0,wx.ALL|wx.ALIGN_RIGHT,5)

        ButtonLayout.Add(openButton,5)
        ButtonLayout.Add(saveButton,5)
        ButtonLayout.Add(resetButton,5)

        controlLayout.Add(labelLayout,0,wx.ALL|wx.EXPAND,5)
        controlLayout.Add(RLayout,0,wx.ALL|wx.EXPAND,5)
        controlLayout.Add(GLayout,0,wx.ALL|wx.EXPAND,5)
        controlLayout.Add(BLayout,0,wx.ALL|wx.EXPAND,5)
        controlLayout.Add(ButtonLayout,0,wx.ALL|wx.EXPAND,5)

        topLayout.Add(controlLayout,0,wx.ALL|wx.EXPAND,5)
        topLayout.Add(self.imageFrame,0,wx.ALL|wx.EXPAND,5)

        self.panel.SetSizer(topLayout)
        topLayout.Fit(self)

        #Events
        self.Bind(wx.EVT_MENU,self.OnOpen,menuOpen)
        self.Bind(wx.EVT_MENU,self.OnAbout,menuAbout)
        self.Bind(wx.EVT_MENU,self.OnExit,menuExit)
        self.Bind(wx.EVT_MENU,self.OnSave,menuSave)
        self.Bind(wx.EVT_MENU,self.OnSaveAs,menuSaveAs)
        self.Bind(wx.EVT_SPINCTRL,self.shiftColors,self.RslideX)
        self.Bind(wx.EVT_SPINCTRL,self.shiftColors,self.RslideY)
        self.Bind(wx.EVT_SPINCTRL,self.shiftColors,self.GslideX)
        self.Bind(wx.EVT_SPINCTRL,self.shiftColors,self.GslideY)
        self.Bind(wx.EVT_SPINCTRL,self.shiftColors,self.BslideX)
        self.Bind(wx.EVT_SPINCTRL,self.shiftColors,self.BslideY)
        self.Bind(wx.EVT_BUTTON,self.resetImage,resetButton)
        self.Bind(wx.EVT_BUTTON,self.OnSaveAs,saveButton)
        self.Bind(wx.EVT_BUTTON,self.OnOpen,openButton)

        self.Show(True)

    def shiftColors(self,e):
        if self.PIL_image != None:
            spin = e.GetEventObject()
            color = spin.name[:-1]

            if spin.GetValue() > self.old_shift:
                shift_value = 1
            else:
                shift_value = -1
            old_shift = spin.GetValue()

            if spin.name.endswith("X"):
                self.PIL_image = effects.shiftColor(self.PIL_image,color,shift_value,0)
            else:
                self.PIL_image = effects.shiftColor(self.PIL_image,color,0,shift_value)
            self.showImage(None,False)  
        else:
            pass

    def resetImage(self,e):
        self.showImage(self.filePath,True)
        self.resetSliders()

    def resetSliders(self):
        self.RslideX.SetValue(0)
        self.RslideY.SetValue(0)
        self.GslideX.SetValue(0)
        self.GslideY.SetValue(0)
        self.BslideX.SetValue(0)
        self.BslideY.SetValue(0)

    def OnOpen(self,e):
        with wx.FileDialog(self,"Choose a file",defaultDir=os.path.expanduser('~'),wildcard=self.wildcard,style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.resetSliders()
                self.filePath = dlg.GetPath()
                self.showImage(self.filePath,True)

    def OnSave(self,e):
        self.SaveImage(self.PIL_image,self.filePath)

    def OnSaveAs(self,e):
        dlg = wx.FileDialog(self,"Save Image", wildcard=self.wildcard,style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        result = dlg.ShowModal()
        path = dlg.GetPath()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.SaveImage(self.PIL_image,path)

    def OnAbout(self,e):
        dlg = wx.MessageDialog(self,("A practice image editing application made using Python and wxWidgets\n\n"  
                                "https://gitlab.com/bunu/aesthetic-image"),"About Progam",wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self,e):
        self.Close(True)

    def SaveImage(self,imageData,directory):
        try:
            imageData.save(directory)
        except PermissionError as p:
            dlg = wx.MessageDialog(self,"You do not have permission to save to this location\n\n" + repr(p),"Permission Error",wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        except IOError as e:
            dlg = wx.MessageDialog(self,"Something went wrong when writing to this location\n\n" + repr(e),"I/O Error",wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        except ValueError as v:
            dlg = wx.MessageDialog(self,"Add a file extension to the end of name such as .jpg or .png\n\n" + repr(v),"I/O Error",wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        except AttributeError:
            pass 


    def showImage(self,filepath,fromOpen):
        if fromOpen:
            img = wx.Image(filepath,wx.BITMAP_TYPE_ANY)
            self.PIL_image = Image.open(filepath)
            dim = self.findScale(img.GetWidth(),img.GetHeight())
            img.Rescale(dim[0],dim[1])
        else:
            img = effects.PIL_to_wx(self.PIL_image)
            img = wx.Bitmap.ConvertToImage(img)
            dim = self.findScale(img.GetWidth(),img.GetHeight())
            img.Rescale(dim[0],dim[1])
        
        self.imageFrame.SetBitmap(wx.Bitmap(img))
        self.panel.Refresh()

    def findScale(self,w,h):
        h_ratio = h/self.photoHeight
        w_ratio = w/self.photoWidth

        if h_ratio > w_ratio:
            return (w/h_ratio,h/h_ratio)
        else:
            return (w/w_ratio,h/w_ratio)


if __name__ == '__main__':
    app = wx.App(False)
    gui = MainGUI(None,"aesthetic-image")
    app.MainLoop()