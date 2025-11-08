import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

# Function to analyze bacterial growth stage and plot
def analyze_growth():
    try:
        n0 = float(entry_n0.get())      # Initial population
        nt = float(entry_nt.get())      # Current population
        k = float(entry_k.get())        # Carrying capacity
        t = float(entry_t.get())        # Time (hours)
        r = float(entry_r.get())        # Growth rate

        # Determine the growth stage
        if nt < 1.2 * n0:
            stage = "Lag phase"
        elif nt < 0.9 * k:
            stage = "Exponential (Log) phase"
        elif abs(nt - k) / k < 0.1:
            stage = "Stationary phase"
        else:
            stage = "Death phase"

        # Display the stage
        result_label.config(text=f"Stage: {stage}")

        # Generate growth curve data
        time_points = np.linspace(0, t, 200)
        logistic_growth = k / (1 + ((k - n0) / n0) * np.exp(-r * time_points))

        # Plot
        plt.figure(figsize=(6,4))
        plt.plot(time_points, logistic_growth, label="Growth curve")
        plt.scatter([t], [nt], color='red', label="Current point")
        plt.xlabel("Time (hours)")
        plt.ylabel("Population size (N)")
        plt.title(f"Bacterial Growth Curve ({stage})")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers!")

# GUI setup
window = tk.Tk()
window.title("Bacterial Growth Analyzer")

# Title label
tk.Label(window, text="Bacterial Growth Stage Analyzer", font=("Arial", 16, "bold")).pack(pady=10)

# Input fields
tk.Label(window, text="N₀ (Initial population):").pack()
entry_n0 = tk.Entry(window)
entry_n0.pack()

tk.Label(window, text="Nₜ (Current population):").pack()
entry_nt = tk.Entry(window)
entry_nt.pack()

tk.Label(window, text="K (Carrying capacity):").pack()
entry_k = tk.Entry(window)
entry_k.pack()

tk.Label(window, text="r (Growth rate):").pack()
entry_r = tk.Entry(window)
entry_r.pack()

tk.Label(window, text="t (Time in hours):").pack()
entry_t = tk.Entry(window)
entry_t.pack()

# Analyze button
tk.Button(window, text="Analyze Growth", command=analyze_growth, bg="lightblue").pack(pady=10)

# Result label
result_label = tk.Label(window, text="", font=("Arial", 12))
result_label.pack()

# Run the GUI
window.mainloop()
