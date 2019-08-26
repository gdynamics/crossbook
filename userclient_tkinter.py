from tkinter import Tk, Frame, Listbox, Scrollbar, Text, LEFT, RIGHT, TOP, BOTTOM, YES, NO, BOTH, X, Y, END, NORMAL, DISABLED
# from os import startfile

class CrossbookGUI:
    def __init__(self, root, **options):
        # Initialize default states for internal structures
        self.dialogs = {}
        self.cache = {}
        self.dialog_max_title = 32
        
        # Apply options
        for option,value in options.items():
            if option == 'dialog_max_title':
                if isinstance(value, int) and value > 5:
                    self.dialog_max_title = value
                else:
                    print('Warning: dialog_max_title must be an int greater than 5. Ignoring')
            else:
                print('Warning: Option', option, 'is not a valid option. Ignoring')

        # Initial creation
        self.root = root
        self.root.geometry('640x480')
        self.root.title('Crossbook')

        # High level structure
        self.dialogs_frame = Frame(self.root, width=200)
        self.chat_frame = Frame(self.root)
        self.dialogs_frame.pack(side=LEFT, expand=NO, fill=BOTH)
        self.chat_frame.pack(side=RIGHT, expand=YES, fill=BOTH)

        # Add listbox of dialogs
        self.dialogs_frame.pack_propagate(False) # Prevent children from changing parent's size
        self.dialogs_list = Listbox(self.dialogs_frame)
        self.dialogs_list.pack(expand=YES, fill=BOTH)
        self.dialogs_list.config(height=50)

        # Create messages and input frames
        self.messages_frame = Frame(self.chat_frame, bg='red')
        self.input_frame = Frame(self.chat_frame, height=48, bg='green')
        self.messages_frame.pack(side=TOP, expand=YES, fill=BOTH)
        self.input_frame.pack(side=BOTTOM, expand=NO, fill=BOTH)

        # Setup messages portion of chat frame
        self.messages_scrollbar = Scrollbar(self.messages_frame)
        self.messages = Text(self.messages_frame)
        self.messages_scrollbar.pack(side=RIGHT, fill=Y)
        self.messages.pack(side=LEFT, fill=Y)
        self.messages_scrollbar.config(command=self.messages.yview)
        self.messages.config(yscrollcommand=self.messages_scrollbar.set)
        for i in range(500):
            self.messages.insert(END, str(i)+'\n')
        self.messages.config(state=DISABLED)

        # Event bindings
        self.dialogs_list.bind('<<ListboxSelect>>', self.load_dialog)

        # Launch crypto-stego engine
        #startfile('enc.py')
    
    def fill_dialogs_test(self):
        """ Fill the dialogs with some test values.
        """
        self.dialogs = {
            'secret' : [['john', 'hi'], ['dog', 'bark']],
            'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' : [],
            'это программа' : [['алекс', 'привет русскоговорящие']]
        }

    def get_dialog_title(self, dialog_name):
        """ Return the proper title of a dialog given its name and number of unread messages.
        """
        #return dialog_name[:self.dialog_max_title] # TODO: Figure out a way to prevent keyerrors when pulling name for later indexing
        return dialog_name
    
    def fill_dialogs(self):
        """ Fill dialogs list with known dialogs.
        """
        for dialog in self.dialogs:
            self.dialogs_list.insert(END, self.get_dialog_title(dialog))
    
    def load_dialog(self, event):
        """ Load a dialog after the user selected it.
        """
        # Get the name of the chat
        diags = event.widget
        index = int(diags.curselection()[0])
        name = diags.get(index)

        # Enable editing, empty the text box, and fill it with the correct text
        self.messages.config(state=NORMAL)
        self.messages.delete(1.0, END)
        if not name in self.cache:
            for log in self.dialogs[name]:
                message = log[0] + ': ' + log[1]
                self.messages.insert(END, message+'\n\n')
            self.cache[name] = self.messages.get(1.0, END)
        else:
            self.messages.insert(END, self.cache[name])
        self.messages.config(state=DISABLED)


def main():
    # Initialization
    root = Tk()
    client = CrossbookGUI(root)
    client.fill_dialogs_test()
    client.fill_dialogs()

    # Start
    root.mainloop()

if __name__ == '__main__':
    main()
