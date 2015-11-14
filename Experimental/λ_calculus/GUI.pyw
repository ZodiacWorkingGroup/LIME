import io
import codecs
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import *
from tkinter.filedialog import *
from lambda_calculus import *
from GUI_customtext import *

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), sys.stdout.encoding, 'replace')


class LCWin(Tk):
    def __init__(self, conf={}, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        for x in range(1):
            Grid.columnconfigure(self, x, weight=1)
            Grid.rowconfigure(self, x, weight=1)

        self.conf = conf
        self.titlestring = u'LIME \u03BB-calculator'
        self.filename = ''
        self.saved = True

        self.lambdawin = CustomText(self, width=80, height=20, font=(self.conf['formatting']['default.typeface'],
                                                                        int(self.conf['formatting']['size']),
                                                                        self.conf['formatting']['default.font']))

        self.outwin = ScrolledText(self, height=8, background='#CCCCCC', font=(
                                                                        self.conf['formatting']['default.typeface'],
                                                                        int(self.conf['formatting']['size']),
                                                                        self.conf['formatting']['default.font']))

        self.lambdawin.tag_configure('named', foreground='#0000CC', font=(self.conf['formatting']['named.typeface'],
                                                                          int(self.conf['formatting']['size']),
                                                                          self.conf['formatting']['named.font']))
        self.lambdawin.tag_configure('paren', foreground='#FF0000', font=(self.conf['formatting']['paren.typeface'],
                                                                          int(self.conf['formatting']['size']),
                                                                          self.conf['formatting']['paren.font']))
        self.lambdawin.tag_configure('lambda', foreground='#00CC00', font=(self.conf['formatting']['lambda.typeface'],
                                                                           int(self.conf['formatting']['size']),
                                                                           self.conf['formatting']['lambda.font']))
        self.lambdawin.tag_configure('comment', foreground='#CC0000', font=(self.conf['formatting']['comment.typeface'],
                                                                            int(self.conf['formatting']['size']),
                                                                            self.conf['formatting']['comment.font']))

        self.lambdawin.grid(row=0, column=0, sticky=N+E+S+W)
        self.bind_class('Text', '<\\>', self.insertlambda)
        self.bind_class('Text', '<.>', self.insertperiod)
        self.bind_class('Text', '<=>', self.insertequals)
        self.bind_class('Text', '<Control-r>', self.execute)
        self.bind('<Key>', self.keypress)

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

        self.bind_class('Text', '<Control-o>', self.openfile)
        self.bind('<Control-s>', self.savefile)
        self.bind('<Control-Shift-s>', self.saveasfile)

        self.bind('Control-w', self.comns)

        self.updateview()

    def updateview(self, e=None):
        self.title(self.titlestring+' -- '+(self.filename if self.filename else 'Untitled'))

    def insertlambda(self, e):
        if (self.lambdawin.get('insert-1c') != u'\u03BB' and self.lambdawin.get('insert+1c') != u'\u03BB') or not self.conf['checkSyntax'] == 'True':
            self.lambdawin.insert(INSERT, u'\u03BB')

    def insertperiod(self, e):
        if (self.lambdawin.get('insert-1c') != '.' and self.lambdawin.get('insert+1c') != '.') or not self.conf['checkSyntax'] == 'True':
            self.lambdawin.insert(INSERT, '.')

    def insertequals(self, e):
        if self.conf['threeBars'] == 'True':
            if (self.lambdawin.get('insert-1c') != '\u2261' and self.lambdawin.get('insert+1c') != '\u2261') or not self.conf['checkSyntax'] == 'True':
                self.lambdawin.insert(INSERT, '\u2261')
        else:
            if (self.lambdawin.get('insert-1c') != '=' and self.lambdawin.get('insert+1c') != '=') or not self.conf['checkSyntax'] == 'True':
                self.lambdawin.insert(INSERT, '=')

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

        self.outwin.insert(END, '\n\n'.join([str(x) for x in lceval(self.lambdawin.get(1.0, END))]))
        self.outwin.config(state=DISABLED)

    def clear(self, *args):
        self.lambdawin.delete(1.0, END)

    def keypress(self, e=None):
        self.saved = False
        if self.conf['syntaxHighlighting']:
            # self.lambdawin.highlight_pattern(r'([^().=a-z\s\u2261]|\{[^}]+\})', 'named', regexp=True)  # Highlight names
            self.lambdawin.highlight_pattern(r'.(\*+|\[[^\]]+])?|\{[^}]+\}', 'named', regexp=True)
            self.lambdawin.highlight_pattern(u'\u03BB', 'lambda', regexp=True)  # Highlight lambdas
            self.lambdawin.highlight_pattern(r'#.*', 'comment', regexp=True)  # Highlight and italicize commments
            self.lambdawin.highlight_pattern(r'[()]', 'paren', regexp=True)  # Highlight and bold parenthesis

    def comns(self, e=None):  # Command Not Supported
        showerror('Unsupported Command', 'Command not yet supported. Sorry :/.')

    def openfile(self, e=None):
        save = False
        if self.saved == False:
            save = askyesnocancel('Save file?', 'You are about to clear the current project. Would you like to save it?')

        if save != None:
            if save:
                self.savefile()
            self.filename = askopenfilename()

            if self.filename:
                self.lambdawin.delete(1.0, END)
                self.lambdawin.insert(END, codecs.open(str(self.filename), 'r', 'utf-8').read())
                self.updateview()
        self.keypress()

    def savefile(self, e=None):
        if self.filename != '':
            f = codecs.open(str(self.filename), 'w', 'utf-8')
            f.write(self.lambdawin.get(1.0, END)[:-1])
            f.close()
        else:
            self.saveasfile()

    def saveasfile(self, e=None):
        fn = asksaveasfilename()
        if fn:
            self.filename = fn
            f = codecs.open(str(self.filename), 'w', 'utf-8')
            f.write(self.lambdawin.get(1.0, END)[:-1])
            f.close()
            self.updateview()

    def close(self, e=None):
        if not self.saved:
            save = False
            if self.saved == False:
                save = askyesnocancel('Save file?', 'You are about to clear the current project. Would you like to save it?')

            if save != None:
                if save:
                    self.savefile()

        self.destroy()


if __name__ == '__main__':
    def badSetting(setting):
        raise ValueError('Invalid value for '+setting+': '+config[setting])

    config = {x.split(':', 1)[0].strip():x.split(':', 1)[1].strip() for x in open('lambda.cfg').read().split('\n') if x}
    rep = {x.split(':', 1)[0].strip():x.split(':', 1)[1].strip() for x in open('replace.cfg').read().split('\n') if x}
    form = {x.split(':', 1)[0].strip():x.split(':', 1)[1].strip() for x in open('formatting.cfg').read().split('\n') if x}
    config['replace'] = rep
    config['formatting'] = form

    lc = LCWin(config)
    lc.mainloop()
