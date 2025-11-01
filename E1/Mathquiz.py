import tkinter as tk
from tkinter import messagebox
import random

APP_BG_COLOR = "lightgray"
BUTTON_BG_COLOR = "white"

class MathsQuizGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Math Quiz")
        self.root.geometry("300x300")
        self.root.config(bg=APP_BG_COLOR) 
        
        self.score = 0
        self.q_num = 0
        self.diff = 1
        self.answer = 0
        self.attempts = 0
        self.build_menu()

    def build_menu(self):
        self.clear()
        tk.Label(self.root, text="MATHS QUIZ",
                 font=("Helvetica", 16), bg=APP_BG_COLOR).pack(pady=15)
        tk.Label(self.root, text="Select Difficulty Level",
                 font=("Helvetica", 10), bg=APP_BG_COLOR).pack(pady=10)

        self.make_btn("Easy (1-9)", lambda: self.start(1)).pack(pady=5)
        self.make_btn("Moderate (10-99)", lambda: self.start(2)).pack(pady=5)
        self.make_btn("Advanced (1000-9999)", lambda: self.start(3)).pack(pady=5)

    def make_btn(self, text, cmd):
        btn = tk.Button(self.root, text=text, 
                         width=20,
                         bg=BUTTON_BG_COLOR,
                         command=cmd)
        return btn

    def start(self, diff):
        self.diff, self.score, self.q_num = diff, 0, 0
        self.next_q()

    def next_q(self):
        if self.q_num >= 10:
            self.results()
            return
        self.q_num += 1
        self.attempts = 0
        self.num1 = self.rnd(self.diff)
        self.num2 = self.rnd(self.diff)
        self.op = random.choice(["+", "-"])
        self.answer = self.num1 + self.num2 if self.op == "+" else self.num1 - self.num2
        self.show_q()

    def rnd(self, d):
        if d == 1: return random.randint(1, 9)
        if d == 2: return random.randint(10, 99)
        return random.randint(1000, 9999)

    def show_q(self):
        self.clear()
        
        tk.Label(self.root, text=f"Question {self.q_num}/10 | Score: {self.score}",
                 font=("Helvetica", 10), bg=APP_BG_COLOR).pack(pady=5)
        
        tk.Label(self.root, text=f"{self.num1} {self.op} {self.num2} = ?",
                 font=("Helvetica", 18), bg=APP_BG_COLOR).pack(pady=10)
                 
        if self.attempts > 0:
            tk.Label(self.root, text="(Try again for half points!)", bg=APP_BG_COLOR).pack()

        self.entry = tk.Entry(self.root, width=10, justify="center", bg=BUTTON_BG_COLOR)
        self.entry.pack(pady=10)
        self.entry.focus()
        self.entry.bind("<Return>", lambda e: self.check())
        
        self.make_btn("Submit Answer", self.check).pack(pady=5)

    def check(self):
        try:
            user = int(self.entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter a number!")
            return

        if user == self.answer:
            points = 10 if self.attempts == 0 else 5
            self.score += points
            messagebox.showinfo("Correct!", f"Good job! +{points} points")
            self.next_q()
        else:
            self.attempts += 1
            if self.attempts < 2:
                messagebox.showwarning("Wrong", "Try again!")
                self.show_q()
            else:
                messagebox.showinfo("Hint", f"The correct answer was {self.answer}")
                self.next_q()

    def results(self):
        self.clear()
        
        tk.Label(self.root, text="Quiz Finished!",
                 font=("Helvetica", 16), bg=APP_BG_COLOR).pack(pady=15)
        
        tk.Label(self.root, text=f"Final Score: {self.score} out of 100",
                 font=("Helvetica", 12), bg=APP_BG_COLOR).pack(pady=5)
        
        grade_text, col = self.grade() 

        tk.Label(self.root, text=grade_text,
                 font=("Helvetica", 14), fg=col, bg=APP_BG_COLOR).pack(pady=10)
        
        self.make_btn("Play Again", self.build_menu).pack(pady=10)
        self.make_btn("Quit", self.root.quit).pack(pady=5)

    def grade(self):
        s = self.score
        if s >= 80: return "Great Job! (80+)", "green"
        if s >= 50: return "Not Bad (50-79)", "blue"
        return "Needs Practice (<50)", "red"

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    MathsQuizGUI(root)
    root.mainloop()
