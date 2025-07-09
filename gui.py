import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from threading import Thread
from chatbot_backend import ChatbotBackend  # Import your backend class

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Exit Interview Chatbot")
        self.root.geometry("700x600")
        self.root.configure(bg='#f5f5f5')
        
        # Initialize backend
        self.chatbot = ChatbotBackend()
        
        # User info variables
        self.name_var = tk.StringVar()
        self.dept_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.years_var = tk.StringVar()
        
        # Chat variables
        self.user_input_var = tk.StringVar()
        self.interview_started = False
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#f5f5f5')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # User info frame (shown at start)
        self.user_info_frame = tk.LabelFrame(main_frame, text=" Your Information ", 
                                          bg='#f5f5f5', font=('Arial', 11))
        self.user_info_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(self.user_info_frame, text="Full Name:", bg='#f5f5f5').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Entry(self.user_info_frame, textvariable=self.name_var, width=40).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.user_info_frame, text="Department:", bg='#f5f5f5').grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Entry(self.user_info_frame, textvariable=self.dept_var, width=40).grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self.user_info_frame, text="Job Title:", bg='#f5f5f5').grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Entry(self.user_info_frame, textvariable=self.title_var, width=40).grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(self.user_info_frame, text="Years Worked:", bg='#f5f5f5').grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Entry(self.user_info_frame, textvariable=self.years_var, width=40).grid(row=3, column=1, padx=5, pady=5)
        
        # Start button
        tk.Button(self.user_info_frame, text="Start Interview", command=self.start_interview,
                 bg='#4CAF50', fg='white', relief=tk.FLAT).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Chat area (hidden until interview starts)
        self.chat_frame = tk.Frame(main_frame, bg='#f5f5f5')
        
        # Chat history
        self.chat_history = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, 
                                                    state='disabled', height=20,
                                                    font=('Arial', 10))
        self.chat_history.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input area
        input_frame = tk.Frame(self.chat_frame, bg='#f5f5f5')
        input_frame.pack(fill=tk.X, pady=5)
        
        self.user_input = tk.Entry(input_frame, textvariable=self.user_input_var, 
                                 width=50, font=('Arial', 10))
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Button(input_frame, text="Send", command=self.send_message,
                bg='#2196F3', fg='white', relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        tk.Button(input_frame, text="Speak", command=self.start_listening,
                bg='#FF9800', fg='white', relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Please enter your information to begin")
        tk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN,
                anchor=tk.W, bg='#e0e0e0').pack(fill=tk.X, pady=(10,0))
    
    def start_interview(self):
        if not all([self.name_var.get(), self.dept_var.get(), 
                   self.title_var.get(), self.years_var.get()]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        user_info = {
            'Name': self.name_var.get(),
            'Department': self.dept_var.get(),
            'Job Title': self.title_var.get(),
            'Years Worked': self.years_var.get()
        }
        
        # Initialize interview
        welcome_msg = self.chatbot.start_interview(user_info)
        
        # Switch to chat interface
        self.user_info_frame.pack_forget()
        self.chat_frame.pack(fill=tk.BOTH, expand=True)
        self.interview_started = True
        
        # Display welcome message
        self.display_message("Bot", welcome_msg)
        self.status_var.set("Interview started - respond to the questions")
        
        # Focus on input field
        self.user_input.focus()
    
    def display_message(self, sender, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_history.config(state='disabled')
        self.chat_history.see(tk.END)
    
    def send_message(self):
        user_input = self.user_input_var.get().strip()
        if not user_input:
            return
            
        self.user_input_var.set("")
        self.display_message("You", user_input)
        
        # Process in background
        Thread(target=self.process_user_input, args=(user_input,), daemon=True).start()
    
    def start_listening(self):
        if not self.interview_started:
            return
            
        self.status_var.set("Listening...")
        Thread(target=self.listen_and_process, daemon=True).start()
    
    def listen_and_process(self):
        transcript = self.chatbot.listen()
        self.root.after(0, self.process_speech_result, transcript)
    
    def process_speech_result(self, transcript):
        self.status_var.set("Ready")
        if transcript.lower() in ["sorry, i didn't hear anything", "sorry, i didn't catch that", "speech service error"]:
            self.display_message("System", transcript)
        else:
            self.user_input_var.set(transcript)
            self.send_message()
    
    def process_user_input(self, user_input):
        # Get bot response
        bot_response = self.chatbot.continue_conversation(user_input)
        
        # Update GUI
        self.root.after(0, self.display_message, "Bot", bot_response)
        
        # Check if interview is complete
        if "thank you for your time" in bot_response.lower():
            self.root.after(0, self.end_interview)
    
    def end_interview(self):
        self.user_input.config(state='disabled')
        self.status_var.set("Interview completed - you may close the window")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()