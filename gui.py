import tkinter as tk
import tkinter.font as tkFont
import tkinter.scrolledtext as st
from recognizer import Speech
import threading
import time

class App:
    def __init__(self, root):
        # setting title
        root.title("HVhelfer")
        # setting window size
        width = 1500
        height = 600
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)

        # setting start recognition button
        self.startrButton = tk.Button(root)
        self.startrButton["bg"] = "#13f853"
        ft = tkFont.Font(family='Times', size=13)
        self.startrButton["font"] = ft
        self.startrButton["fg"] = "#000000"
        self.startrButton["justify"] = "center"
        self.startrButton["text"] = "Start recording"
        self.startrButton.place(x=1300, y=180, width=130, height=30)
        self.startrButton["command"] = self.startrButton_command

        # setting stop recognition button
        self.stoprButton = tk.Button(root)
        self.stoprButton["bg"] = "#fb0f0f"
        ft = tkFont.Font(family='Times', size=13)
        self.stoprButton["font"] = ft
        self.stoprButton["fg"] = "#000000"
        self.stoprButton["justify"] = "center"
        self.stoprButton["text"] = "Stop recording"
        self.stoprButton.place(x=1300, y=250, width=130, height=30)
        self.stoprButton["command"] = self.stoprButton_command
        self.stoprButton["state"] = 'disabled'
        
        # setting label
        GLabel_851 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=18)
        GLabel_851["font"] = ft
        GLabel_851["fg"] = "#333333"
        GLabel_851["justify"] = "center"
        GLabel_851["text"] = "Recognized text"
        GLabel_851.place(width=700, height=71)
        GLabel_851.grid(pady=30)

        # setting ScrolledText object for recognised speech
        self.TRmsg = st.ScrolledText(root, width=150, height=13, font=("Calibri", 12))
        self.TRmsg.insert(tk.INSERT, "Start recording...\n")
        self.TRmsg.grid(column=0, row=3, columnspan=3, pady=10, padx=10)
        self.TRmsg.configure(state='disabled')

        #setting ScrolledText object for log messages
        self.logmsg = st.ScrolledText(root, width=150, height=6, font=("Calibri", 12))
        self.logmsg.grid(column=0, pady=40, padx=10, ipady=20)
        self.logmsg.configure(state='disabled')

        self.full_recognized=""
        
    def write_translated_text(self, speech_recognition):
        """
        Write recognised speech in text box
        """
        self.TRmsg.configure(state='normal')
        text = speech_recognition.result.text
        #write full recognised text
        if speech_recognition.result.reason.name == 'RecognizedSpeech':
            # delete all text
            self.TRmsg.delete('1.0', tk.END)
            # append new full recognised text
            self.full_recognized=self.full_recognized + text + '\n'
            # write all full recognised text
            self.TRmsg.insert('1.0', self.full_recognized)
        #write partial recognised text
        else:
            if len(self.full_recognized):
                self.TRmsg.delete('1.0', tk.END)
                out_text = self.full_recognized + text
                self.TRmsg.insert(self.pt_, out_text)
            else:
                self.TRmsg.delete('1.0', tk.END)
                self.TRmsg.insert('1.0', text)
        self.TRmsg.configure(state='disabled')

    def write_logs(self, text):
        """
        Parameters
        ----------
        text : str
        Write log messages in log box    
        """
        self.logmsg.configure(state='normal')
        self.logmsg.insert(tk.INSERT,"{} {}\n".format(time.strftime('%d-%m-%Y %H:%M:%S', time.localtime()), text))
        self.logmsg.configure(state='disabled')
      
    def start_recognition(self):
        """
        Start speech recognition process
        """
        try:
            self.speech = Speech(self.write_logs, self.write_translated_text)
            self.speech.messages()
            self.speech.start_pa_stream()
            self.speech.start_sdk_stream()
        except Exception as e:
            self.write_logs(e)
            self.stoprButton_command()
        finally:
            self.speech.stop_stream()
        

    def startrButton_command(self):
        """
        Command invoked by start button
        """
        self.full_recognized = ""
        self.write_logs('Recording is ON')
        self.logmsg.configure(state='normal')
        self.TRmsg.delete('1.0', tk.END)
        self.logmsg.configure(state='disabled')
        #move recognition process to individual thread to enable to stop the process at any time
        self.Thread = threading.Thread(target=self.start_recognition)
        self.Thread.start()
        self.stoprButton["state"] = 'active'
        self.startrButton["state"] = 'disabled'
        
    def stoprButton_command(self):
        """
        Command invoked by stop button
        """
        # set state to break the stream loop
        self.speech.state = False
        self.write_logs('Recording is OFF')
        self.startrButton["state"] = 'active'
        self.stoprButton["state"] = 'disabled'  
