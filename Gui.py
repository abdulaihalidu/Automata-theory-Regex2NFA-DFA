import tkinter as tk
from PIL import Image, ImageTk
import FA


# class to display main page of the program
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # creating a border frame to make our gui look nice
        border = tk.LabelFrame(self, bg="ivory")
        border.pack(fill="both", expand="yes", padx=200, pady=200)
        # title label
        label = tk.Label(self, text="Automata Teory Donem Projesi", font=("Arial Bold", 20), bg="#808080")
        label.place(x=420, y=50)

        # text field entry to get regex from user
        instruction_lb = tk.Label(border, text="Please Enter regex in the text box below", font=("Arial black", 18), bg="ivory")
        instruction_lb.place(x=170, y=100)
        regex_tx_bx = tk.Entry(border, width=30,  bd=5, font=("Arial", 18))
        regex_tx_bx.place(x=240, y=150)

        def convert2fa(btn_name):
            if btn_name == "NFA":
                NfaPage.regex = regex_tx_bx.get()
                AnalysisPage.regex = regex_tx_bx.get()
                controller.display_frame(NfaPage)
            elif btn_name == "DFA":
                DfaPage.regex = regex_tx_bx.get()
                AnalysisPage.regex = regex_tx_bx.get()
                controller.display_frame(DfaPage)

        # button to lead us to regex2 NFA page
        nfa_btn = tk.Button(self, text="Convert to NFA", font=("Arial", 18),
                            command=lambda: convert2fa("NFA"), bg="#20bebe")
        nfa_btn.place(x=100, y=600)

        # button to lead us to regex2DFA page
        dfa_btn = tk.Button(self, text="Convert to DFA", font=("Arial", 18),
                            command=lambda: convert2fa("DFA"), bg="#20bebe")
        dfa_btn.place(x=1000, y=600)


class NfaPage(tk.Frame):
    regex = ""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # title label
        label = tk.Label(self, text="Regex to NFA", font=("Arial Bold", 20), bg="#808080")
        label.place(x=500, y=10)
        # instruction label
        instruction_label = tk.Label(self, text="Please click on 'clear page' before leaving this page ⚠", font=("Arial Bold", 15), bg="#808080")
        instruction_label.place(x=350, y=50)
        # This button will lead us back to the main page
        homepg_btn = tk.Button(self, text="Home page", font=("Arial", 18),
                                            command=lambda: controller.display_frame(MainPage), bg="#20bebe")
        homepg_btn.place(x=1060, y=600)

        clear_btn = tk.Button(self, text="Clear page", font=("Arial", 18),
                                command=lambda: self.clear_window(), bg="#20bebe")
        clear_btn.place(x=1050, y=60)

        proceed_btn = tk.Button(self, text="Proceed to see NFA", font=("Arial", 18), bg="#20bebe",
                                command=lambda: self.display_regex())
        proceed_btn.place(x=1000, y=10)

        # A button to lead us to the analysis page
        analysi_btn = tk.Button(self, text="Analyse regex", font=("Arial", 18),
                            command=lambda: controller.display_frame(AnalysisPage), bg="#20bebe")
        analysi_btn.place(x=1040, y=110)

    def display_regex(self):
        global text_label
        text_label = tk.Label(self, text=self.regex, font=("Arial Bold", 20))
        text_label.place(x=50, y=250)
        self.show_nfa()

    def show_nfa(self):
        a = FA.Regex2NFA(self.regex)
        a.create_nfa()
        nfa = Image.open('nfa.gv.png')
        nfa = ImageTk.PhotoImage(nfa)

        global nfa_label
        nfa_label = tk.Label(image=nfa)
        nfa_label.image = nfa
        nfa_label.place(x=50, y=300)
        
    def clear_window(self):
        text_label.place_forget()
        nfa_label.place_forget()


class DfaPage(tk.Frame):
    regex = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Regex to DFA", font=("Arial Bold", 20), bg="#808080")
        label.place(x=500, y=10)

        instruction_label = tk.Label(self, text="Please click on 'clear page' before leaving this page ⚠", font=("Arial Bold", 15), bg="#808080")
        instruction_label.place(x=350, y=50)
        # This button will lead us back to the main page
        homepg_btn = tk.Button(self, text="Home page", font=("Arial", 18),
                            command=lambda: controller.display_frame(MainPage), bg="#20bebe")
        homepg_btn.place(x=1060, y=600)

        clear_btn = tk.Button(self, text="Clear page", font=("Arial", 18),
                                command=lambda: self.clear_page(), bg="#20bebe")
        clear_btn.place(x=1050, y=60)

        proceed_btn = tk.Button(self, text="Proceed to see DFA", font=("Arial", 18), bg="#20bebe",
                                command=lambda: self.display_regex())
        proceed_btn.place(x=1000, y=10)

        # A button to lead us to the analysis page
        analysi_btn = tk.Button(self, text="Analyse regex", font=("Arial", 18),
                                command=lambda: controller.display_frame(AnalysisPage), bg="#20bebe")
        analysi_btn.place(x=1040, y=110)

    def display_regex(self):
        global text_label
        text_label = tk.Label(self, text=self.regex, font=("Arial Bold", 20))
        text_label.place(x=50, y=250)
        self.show_dfa()

    def show_dfa(self):
        a = FA.Regex2NFA(self.regex)
        b = FA.NFA2DFA(a.nfa)
        b.create_dfa()

        dfa = Image.open('dfa.gv.png')
        dfa = ImageTk.PhotoImage(dfa)
        global dfa_label
        dfa_label = tk.Label(image=dfa)
        dfa_label.image = dfa
        dfa_label.place(x=50, y=300)


    def clear_page(self):
        text_label.place_forget()
        dfa_label.place_forget()


class AnalysisPage(tk.Frame):
    regex = ""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global match_string_regex_label
        match_string_regex_label = tk.Label(self, text="",
                                       font=("Arial black", 18))
        # This functions checks to see if the entered string matches with the given regex

        def check_string():
            match_string_regex_label.place_forget()
            global string
            string = string_tx_bx.get()
            a = FA.Regex2NFA(self.regex)
            b = FA.NFA2DFA(a.nfa)
            if(b.analysis(string)):
                match_string_regex_label.config(text=f"The string '{string}' matches with the given regex: "
                                                     f"{self.regex}", bg="green")
                match_string_regex_label.place(x=300, y=250)
            else:
                match_string_regex_label.config(text=f"The string '{string}' doesn't match with the given regex:"
                                                     f" {self.regex}", bg="red")
                match_string_regex_label.place(x=290, y=250)

        # text field entry to get string from user
        instruction_lb = tk.Label(self, text="Please enter your string  in the text box below", font=("Arial black", 18), bg="ivory")
        instruction_lb.place(x=320, y=50)
        string_tx_bx = tk.Entry(self, width=30,  bd=5, font=("Arial", 18))
        string_tx_bx.place(x=420, y=100)

        # This button will take the use back to the main page
        homepg_btn = tk.Button(self, text="Home page", font=("Arial", 18),
                               command=lambda: controller.display_frame(MainPage), bg="#20bebe")
        homepg_btn.place(x=1060, y=600)

        # click on this button after entering string
        proceed_btn = tk.Button(self, text="Proceed", font=("Arial", 18),
                               command=lambda: check_string(), bg="#20bebe")
        proceed_btn.place(x=560, y=150)

class Gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Creating a window
        window = tk.Frame(self)
        window.pack()

        window.grid_rowconfigure(0, minsize=720)
        window.grid_columnconfigure(0, minsize=1280)

        self.frames = {}
        for f in [MainPage, NfaPage, DfaPage, AnalysisPage]:
            frame = f(window, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.display_frame(MainPage)

    def display_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


if __name__ == '__main__':
    win = Gui()
    win.title("Automata Teory Donem Projesi")
    win.mainloop()




