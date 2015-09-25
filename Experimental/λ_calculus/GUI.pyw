import io
import codecs
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import *
from tkinter.filedialog import *
from lambda_calculus import *

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'replace')


class LCWin(Tk):
    def __init__(self, cs=True, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        for x in range(1):
            Grid.columnconfigure(self, x, weight=1)
            Grid.rowconfigure(self, x, weight=1)

        self.checkSyntax = cs
        self.titlestring = u'LIME \u03BB-calculator'
        self.filename = ''
        self.saved = False

        self.lambdawin = ScrolledText(self, width=80, height=20)
        self.outwin = ScrolledText(self, height=8, background='#CCCCCC')

        self.lambdawin.grid(row=0, column=0, sticky=N+E+S+W)
        self.bind_class('Text', '<\\>', self.insertlambda)
        self.bind_class('Text', '<.>', self.insertperiod)
        self.bind_class('Text', '<Control-r>', self.execute)
        self.bind('<Key>', self.unsaved)

        self.mb = Menu(self)

        self.filemenu = Menu(self.mb, tearoff=0)
        self.filemenu.add_command(label='New', command=self.comns, accelerator='Ctrl+N')
        self.filemenu.add_command(label='Open', command=self.openfile, accelerator='Ctrl+O')
        self.filemenu.add_command(label='Save', command=self.savefile, accelerator='Ctrl+S')
        self.filemenu.add_command(label='Save as', command=self.saveasfile, accelerator='Ctrl+Shift+S')
        self.filemenu.add_command(label='Save Copy as', command=self.comns)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.close, accelerator='Ctrl+W')
        self.mb.add_cascade(menu=self.filemenu, label='File')

        self.editmenu = Menu(self.mb, tearoff=0)
        self.editmenu.add_command(label='Copy', command=self.comns, accelerator='Ctrl+C')
        self.editmenu.add_command(label='Cut', command=self.comns, accelerator='Ctrl+X')
        self.editmenu.add_command(label='Paste', command=self.comns, accelerator='Ctrl+V')
        self.editmenu.add_command(label='Delete', accelerator='Backspace')
        self.editmenu.add_separator()
        self.editmenu.add_command(label='Undo', command=self.comns, accelerator='Ctrl+Z')
        self.editmenu.add_command(label='Redo', command=self.comns, accelerator='Ctrl+Shift+Z')
        self.editmenu.add_separator()
        self.editmenu.add_command(label='Find', command=self.comns, accelerator='Ctrl+F')
        self.editmenu.add_command(label='Replace', command=self.comns, accelerator='Ctrl+H')
        self.mb.add_cascade(menu=self.editmenu, label='Edit')

        self.config(menu=self.mb)
        self.updateview()

    def updateview(self, e=None):
        self.title(self.titlestring+' -- '+(self.filename if self.filename else 'Untitled'))

    def insertlambda(self, e):
        if (self.lambdawin.get('insert-1c') != u'\u03BB' and self.lambdawin.get('insert+1c') != u'\u03BB') or not self.checkSyntax:
            self.lambdawin.insert(INSERT, u'\u03BB')

    def insertperiod(self, e):
        if (self.lambdawin.get('insert-1c') != '.' and self.lambdawin.get('insert+1c') != '.') or not self.checkSyntax:
            self.lambdawin.insert(INSERT, '.')

    def execute(self, e):
        self.config(height=self.lambdawin.winfo_reqheight()-8)
        self.outwin.grid(row=1, column=0, sticky=N+E+S+W)

        def killOutWin(event):
            self.outwin.frame.destroy()
            self.config(height=self.lambdawin.winfo_reqheight()+8)
            self.unbind('<Escape>', funcid=None)
            self.outwin = ScrolledText(self, height=8, background='#CCCCCC')

        self.outwin.kill = killOutWin
        self.bind('<Escape>', self.outwin.kill)

        self.outwin.insert(END, lceval(self.lambdawin.get(1.0, END)))
        self.outwin.config(state=DISABLED)

    def clear(self, *args):
        self.lambdawin.delete(1.0, END)

    def unsaved(self, e=None):
        self.saved = False

    def comns(self, e=None):  # Command Not Supported
        showerror('Unsupported Command', 'Command not yet supported. Sorry :/.')

    def openfile(self, e=None):
        if self.saved == False:
            save = askyesnocancel('Save file?', 'You are about to clear the current project. Would you like to save it?')

        if self.saved != None:
            if save:
                self.savefile()
            self.filename = askopenfile()

            if self.filename:
                self.lambdawin.delete(1.0, END)
                self.lambdawin.insert(END, codecs.open(str(self.filename), 'r', 'cp1252').read())
                self.update()

    def savefile(self, e=None):
        if self.filename != '':
            open(str(self.filename), 'w').write(self.lambdawin.get(1.0, END))
        else:
            self.saveasfile()

    def saveasfile(self, e=None):
        fn = asksaveasfilename()
        if fn:
            self.filename = fn
            open(str(self.filename), 'w').write(self.lambdawin.get(1.0, END))
            self.update()

    def close(self, e=None):
        pass


def badSetting(setting):
    raise ValueError('Invalid value for '+setting+': '+config[setting])

config = {x.split(':', 1)[0].strip():x.split(':', 1)[1].strip() for x in open('lambda.cfg').read().split('\n')}
lc = LCWin(True if config['checkSyntax'] == 'True' else (False if config['checkSyntax'] == 'False' else badSetting('checkSyntax')))
lc.mainloop()
