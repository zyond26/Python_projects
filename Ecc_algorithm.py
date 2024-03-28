import tkinter as tk
from timeit import timeit
from tkinter import messagebox
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class ECCApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Elliptic Curve Cryptography")
        self.create_widgets()

    def create_widgets(self):
        mainframe = tk.Frame(self, padx=10, pady=10)
        mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        label_equation = tk.Label(mainframe, text="Let the Elliptic Curve be : y^2 = x^3 + ax + b mod r")
        label_equation.grid(column=0, row=0, columnspan=2, pady=10)

        label_a = tk.Label(mainframe, text="a value:")
        label_a.grid(column=0, row=1, sticky=tk.W, pady=5)
        self.entry_a = tk.Entry(mainframe)
        self.entry_a.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)
        
        label_b = tk.Label(mainframe, text="b value:")
        label_b.grid(column=0, row=2, sticky=tk.W, pady=5)
        self.entry_b = tk.Entry(mainframe)
        self.entry_b.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=5)

        label_r = tk.Label(mainframe, text="r value:")
        label_r.grid(column=0, row=3, sticky=tk.W, pady=5)
        self.entry_r = tk.Entry(mainframe)
        self.entry_r.grid(column=1, row=3, sticky=(tk.W, tk.E), pady=5)

        label_x1P = tk.Label(mainframe, text="x1 value of P:")
        label_x1P.grid(column=0, row=4, sticky=tk.W, pady=5)
        self.entry_x1P = tk.Entry(mainframe)
        self.entry_x1P.grid(column=1, row=4, sticky=(tk.W, tk.E), pady=5)

        label_y1P = tk.Label(mainframe, text="y1 value of P:")
        label_y1P.grid(column=0, row=5, sticky=tk.W, pady=5)
        self.entry_y1P = tk.Entry(mainframe)
        self.entry_y1P.grid(column=1, row=5, sticky=(tk.W, tk.E), pady=5)

        label_a1 = tk.Label(mainframe, text="a value of first person:")
        label_a1.grid(column=0, row=6, sticky=tk.W, pady=5)
        self.entry_a1 = tk.Entry(mainframe)
        self.entry_a1.grid(column=1, row=6, sticky=(tk.W, tk.E), pady=5)

        label_b1 = tk.Label(mainframe, text="a value of second person:")
        label_b1.grid(column=0, row=7, sticky=tk.W, pady=5)
        self.entry_b1 = tk.Entry(mainframe)
        self.entry_b1.grid(column=1, row=7, sticky=(tk.W, tk.E), pady=5)

        button_calculate = tk.Button(mainframe, text="Ecrypt", command=self.calculate_ecc)
        button_calculate.grid(column=0, row=8, columnspan=2, pady=10)

        self.text_output = tk.Text(mainframe, height=20, width=60)
        self.text_output.grid(column=0, row=9, columnspan=2, pady=10)

        run_button = tk.Button(mainframe, text="Run Benchmark", command=self.run_benchmark)
        run_button.grid(column=0, row=11, columnspan=2, pady=10)

        result_label = tk.Label(mainframe, text="")
        result_label.grid(column=0, row=12, columnspan=2, pady=5)
        self.result_label = result_label

    def run_benchmark(self):
        execution_time = timeit(self.my_function, number=10000)
        self.result_label.config(text=f"Benchmark Execution Time: {execution_time:.6f} seconds")

    def my_function(self):
        result = sum(range(10000))
        return result

    def calculate_ecc(self):
        try:
            a = int(self.entry_a.get())
            b = int(self.entry_b.get())
            r = int(self.entry_r.get())
            x1P = int(self.entry_x1P.get())
            y1P = int(self.entry_y1P.get())
            a1 = int(self.entry_a1.get())
            b1 = int(self.entry_b1.get())

            if a < 0 or b < 0 or r <= 0 or x1P < 0 or y1P < 0 or a1 < 0 or b1 < 0:
                raise ValueError("Input values must be positive integers.")

            valueP = {}
            self.get_all_p(a, b, r, x1P, y1P, valueP)

            A = valueP[str(a1) + "P"]
            B = valueP[str(b1) + "P"]

            value_first_person_p = {}
            value_second_person_p = {}
            self.get_all_p(a, b, r, B[0], B[1], value_first_person_p)
            aKey = value_first_person_p[str(a1) + "P"]

            self.get_all_p(a, b, r, A[0], A[1], value_second_person_p)
            bKey = value_second_person_p[str(b1) + "P"]

            output = f"Therefore, first person sends : {A}\n\n"
            output += f"Therefore, second person sends : {B}\n\n"
            output += f"Therefore, from {a1}{B} we get {aKey}\n\n"
            output += f"Therefore, from {b1}{A} we get {bKey}\n\n"

            if aKey[0] == bKey[0]:
                output += f"Shared Key = {aKey[0]}"
            else:
                output += "Error: Keys do not match"

            self.text_output.delete('1.0', tk.END)
            self.text_output.insert(tk.END, output)

            self.plot_elliptic_curve(a, b, r)

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def get_all_p(self, a, b, r, x1P, y1P, valueP):
        x2Q = x1P
        y2Q = y1P

        k = [x1P, y1P]

        print(f"The equation is :  y^2 = x^3 + ({a} * x ) + ({b}) mod {r}")
        print("Points on the Elliptic Curve : ")

        valueP["P"] = k
        print(f"P = {k}")

        for i in range(2, 30):
            if i == 2:
                nextP = self.next_p_value_doubling(a, b, r, x1P, y1P)
            else:
                nextP = self.next_p_value_addition(a, b, r, x1P, y1P, x2Q, y2Q)

            x1P, y1P = nextP[0], nextP[1]

            valueP[str(i) + "P"] = nextP
            print(f"{i}P = {nextP}")

            if nextP[0] == x2Q:
                if self.mod((nextP[1] + y2Q), r) == 0:
                    print(f"{i + 1}P = Point of Infinity")
                    break
        print()

    def next_p_value_addition(self, a, b, r, x1P, y1P, x2Q, y2Q):
        s1 = (y2Q - y1P)
        s2 = (x2Q - x1P)

        if s1 < 0 and s2 < 0:
            s1 = -s1
            s2 = -s2
        elif s2 < 0 and s1 >= 0:
            s1 = -s1
            s2 = -s2

        s1 = self.mod(s1, r)
        s2 = self.mod_inverse(s2, r)
        s = (s1 * s2) % r

        return self.next_p(r, x1P, y1P, x2Q, s)

    def next_p_value_doubling(self, a, b, r, x1P, y1P):
        s1 = self.mod(((3 * (x1P * x1P)) + a), r)
        s2 = self.mod_inverse((2 * y1P), r)
        s = (s1 * s2) % r

        x2Q = x1P
        return self.next_p(r, x1P, y1P, x2Q, s)

    def next_p(self, r, x1P, y1P, x2Q, s):
        x3 = self.mod(((s * s) - x1P - x2Q), r)
        y3 = self.mod(((s * (x1P - x3)) - y1P), r)

        return [x3, y3]

    def mod(self, A, B):
        ans = A % B
        if ans < 0:
            ans = B + ans
        return ans

    def mod_inverse(self, A, M):
        for X in range(1, M):
            if ((A % M) * (X % M)) % M == 1:
                return X
        return 1

    def plot_elliptic_curve(self, a, b, r):
        x = list(range(-r, r + 1))
        y_up = [self.ceil_sqrt(x_val ** 3 + a * x_val + b, r) for x_val in x]
        y_down = [-y for y in y_up]

        plt.clf()
        plt.figure(self.fig.number)
        plt.plot(x, y_up, 'ro', markersize=2)
        plt.plot(x, y_down, 'ro', markersize=2)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Elliptic Curve: y^2 = x^3 + {a}x + {b} mod {r}')
        plt.grid(True)
        self.fig.canvas.draw()

if __name__ == "__main__":
    app = ECCApp()
    app.mainloop()
