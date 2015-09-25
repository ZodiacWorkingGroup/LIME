import io
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from lambda_calculus import *

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'replace')


class LCWin(Tk):
    def __init__(self, cs=True, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        for x in range(1):
            Grid.columnconfigure(self, x, weight=1)
            Grid.rowconfigure(self, x, weight=1)

        self.checkSyntax = cs

        self.lambdawin = ScrolledText(self, width=80, height=20)
        self.outwin = ScrolledText(self, height=8, background='#CCCCCC')

        self.lambdawin.grid(row=0, column=0, sticky=N+E+S+W)
        self.bind_class('Text', '<\\>', self.insertlambda)
        self.bind_class('Text', '<.>', self.insertperiod)
        self.bind_class('Text', '<Control-r>', self.execute)

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


def badSetting(setting):
    raise ValueError('Invalid value for '+setting+': '+config[setting])

config = {x.split(':', 1)[0].strip():x.split(':', 1)[1].strip() for x in open('lambda.cfg').read().split('\n')}
lc = LCWin(True if config['checkSyntax'] == 'True' else (False if config['checkSyntax'] == 'False' else badSetting('checkSyntax')))
lc.mainloop()
