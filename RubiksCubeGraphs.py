import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class RubiksCubeGraphs:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 Rubik's Cube AI - Training & Results Analysis")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0e27')
        
        # Create main container
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#0a0e27')
        header_frame.pack(fill=tk.X, pady=10)
        
        title = tk.Label(header_frame, 
                        text="🎲 RUBIK'S CUBE AI ANALYSIS",
                        font=('Helvetica', 24, 'bold'),
                        fg='#00d4ff',
                        bg='#0a0e27')
        title.pack()
        
        subtitle = tk.Label(header_frame,
                           text="Deep Reinforcement Learning Performance Metrics",
                           font=('Helvetica', 12),
                           fg='#7c8db5',
                           bg='#0a0e27')
        subtitle.pack()
        
        # Navigation buttons
        btn_frame = tk.Frame(self.root, bg='#0a0e27')
        btn_frame.pack(fill=tk.X, pady=10)
        
        buttons = [
            ("📈 Training Curves", self.show_training_curves),
            ("📊 Results Analysis", self.show_results_analysis),
            ("🎯 Performance Radar", self.show_comprehensive_analysis),
            ("⚡ Demo Results", self.show_demo_results)
        ]
        
        for text, command in buttons:
            btn = tk.Button(btn_frame,
                          text=text,
                          font=('Helvetica', 11, 'bold'),
                          bg='#2d3548',
                          fg='#00d4ff',
                          activebackground='#3d4558',
                          relief=tk.FLAT,
                          bd=0,
                          padx=20,
                          pady=10,
                          cursor='hand2',
                          command=command)
            btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
            self.add_hover_effect(btn)
        
        # Content frame for graphs
        self.content_frame = tk.Frame(self.root, bg='#1a1f3a', relief=tk.RAISED, bd=2)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Show first graph by default
        self.show_training_curves()
    
    def add_hover_effect(self, button):
        def on_enter(e):
            button['bg'] = '#3d4558'
        def on_leave(e):
            button['bg'] = '#2d3548'
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_training_curves(self):
        self.clear_content()
        
        # Create figure with subplots
        fig = Figure(figsize=(14, 8), facecolor='#1a1f3a')
        
        # Training data
        epochs = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        loss = np.array([2.45, 2.1, 1.75, 1.42, 1.15, 0.92, 0.75, 0.61, 0.52, 0.45, 0.39])
        accuracy = np.array([12, 22, 35, 48, 61, 72, 81, 87, 91, 94, 96])
        solve_rate = np.array([5, 18, 32, 45, 58, 69, 78, 85, 90, 93, 96])
        avg_moves = np.array([48, 42, 38, 34, 30, 27, 24, 22, 20, 19, 18])
        
        # Subplot 1: Loss
        ax1 = fig.add_subplot(2, 2, 1, facecolor='#0f1429')
        ax1.plot(epochs, loss, color='#ff3b3b', linewidth=3, marker='o', 
                markersize=8, markerfacecolor='#ff6b6b', label='Training Loss')
        ax1.set_xlabel('Epoch', color='#00d4ff', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Loss', color='#00d4ff', fontsize=11, fontweight='bold')
        ax1.set_title('Training Loss Curve', color='#00d4ff', fontsize=13, 
                     fontweight='bold', pad=15)
        ax1.grid(True, alpha=0.2, color='#7c8db5')
        ax1.tick_params(colors='#ffffff')
        ax1.legend(facecolor='#2d3548', edgecolor='#00d4ff', labelcolor='#ffffff')
        
        # Subplot 2: Accuracy
        ax2 = fig.add_subplot(2, 2, 2, facecolor='#0f1429')
        ax2.plot(epochs, accuracy, color='#2ecc71', linewidth=3, marker='s',
                markersize=8, markerfacecolor='#4dff91', label='Accuracy')
        ax2.set_xlabel('Epoch', color='#00d4ff', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Accuracy (%)', color='#00d4ff', fontsize=11, fontweight='bold')
        ax2.set_title('Model Accuracy', color='#00d4ff', fontsize=13, 
                     fontweight='bold', pad=15)
        ax2.grid(True, alpha=0.2, color='#7c8db5')
        ax2.tick_params(colors='#ffffff')
        ax2.legend(facecolor='#2d3548', edgecolor='#00d4ff', labelcolor='#ffffff')
        
        # Subplot 3: Solve Rate
        ax3 = fig.add_subplot(2, 2, 3, facecolor='#0f1429')
        ax3.plot(epochs, solve_rate, color='#9b59b6', linewidth=3, marker='^',
                markersize=8, markerfacecolor='#bb79d6', label='Solve Rate')
        ax3.set_xlabel('Epoch', color='#00d4ff', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Solve Rate (%)', color='#00d4ff', fontsize=11, fontweight='bold')
        ax3.set_title('Cube Solve Success Rate', color='#00d4ff', fontsize=13,
                     fontweight='bold', pad=15)
        ax3.grid(True, alpha=0.2, color='#7c8db5')
        ax3.tick_params(colors='#ffffff')
        ax3.legend(facecolor='#2d3548', edgecolor='#00d4ff', labelcolor='#ffffff')
        
        # Subplot 4: Average Moves
        ax4 = fig.add_subplot(2, 2, 4, facecolor='#0f1429')
        ax4.plot(epochs, avg_moves, color='#FFD700', linewidth=3, marker='D',
                markersize=8, markerfacecolor='#FFE44D', label='Avg Moves')
        ax4.set_xlabel('Epoch', color='#00d4ff', fontsize=11, fontweight='bold')
        ax4.set_ylabel('Average Moves', color='#00d4ff', fontsize=11, fontweight='bold')
        ax4.set_title('Solution Efficiency', color='#00d4ff', fontsize=13,
                     fontweight='bold', pad=15)
        ax4.grid(True, alpha=0.2, color='#7c8db5')
        ax4.tick_params(colors='#ffffff')
        ax4.legend(facecolor='#2d3548', edgecolor='#00d4ff', labelcolor='#ffffff')
        
        fig.tight_layout(pad=3.0)
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def show_results_analysis(self):
        self.clear_content()
        
        fig = Figure(figsize=(14, 8), facecolor='#1a1f3a')
        
        # Results data
        scramble_depths = np.array([5, 8, 10, 12, 15, 18, 20])
        human_avg = np.array([22, 35, 45, 56, 72, 88, 98])
        ai_solution = np.array([8, 12, 15, 18, 23, 28, 31])
        optimal = np.array([7, 10, 13, 15, 19, 23, 26])
        improvement = np.array([64, 66, 67, 68, 68, 68, 68])
        
        # Subplot 1: Comparison Bar Chart
        ax1 = fig.add_subplot(2, 2, 1, facecolor='#0f1429')
        x = np.arange(len(scramble_depths))
        width = 0.25
        
        bars1 = ax1.bar(x - width, human_avg, width, label='Human Avg',
                       color='#ff3b3b', edgecolor='#ff6b6b', linewidth=2)
        bars2 = ax1.bar(x, ai_solution, width, label='AI Solution',
                       color='#2ecc71', edgecolor='#4dff91', linewidth=2)
        bars3 = ax1.bar(x + width, optimal, width, label='Optimal',
                       color='#FFD700', edgecolor='#FFE44D', linewidth=2)
        
        ax1.set_xlabel('Scramble Depth', color='#00d4ff', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Number of Moves', color='#00d4ff', fontsize=11, fontweight='bold')
        ax1.set_title('AI vs Human Performance', color='#00d4ff', fontsize=13,
                     fontweight='bold', pad=15)
        ax1.set_xticks(x)
        ax1.set_xticklabels(scramble_depths)
        ax1.legend(facecolor='#2d3548', edgecolor='#00d4ff', labelcolor='#ffffff')
        ax1.grid(True, alpha=0.2, color='#7c8db5', axis='y')
        ax1.tick_params(colors='#ffffff')
        
        # Subplot 2: Improvement Percentage
        ax2 = fig.add_subplot(2, 2, 2, facecolor='#0f1429')
        ax2.plot(scramble_depths, improvement, color='#9b59b6', linewidth=3,
                marker='o', markersize=10, markerfacecolor='#bb79d6')
        ax2.fill_between(scramble_depths, improvement, alpha=0.3, color='#9b59b6')
        ax2.set_xlabel('Scramble Depth', color='#00d4ff', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Improvement (%)', color='#00d4ff', fontsize=11, fontweight='bold')
        ax2.set_title('AI Improvement Over Human', color='#00d4ff', fontsize=13,
                     fontweight='bold', pad=15)
        ax2.grid(True, alpha=0.2, color='#7c8db5')
        ax2.tick_params(colors='#ffffff')
        ax2.set_ylim([60, 75])
        
        # Subplot 3: Efficiency Ratio
        ax3 = fig.add_subplot(2, 2, 3, facecolor='#0f1429')
        efficiency = (optimal / ai_solution) * 100
        colors_gradient = plt.cm.viridis(efficiency / 100)
        bars = ax3.bar(scramble_depths, efficiency, color=colors_gradient,
                      edgecolor='#00d4ff', linewidth=2)
        ax3.set_xlabel('Scramble Depth', color='#00d4ff', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Efficiency (%)', color='#00d4ff', fontsize=11, fontweight='bold')
        ax3.set_title('AI Solution Optimality', color='#00d4ff', fontsize=13,
                     fontweight='bold', pad=15)
        ax3.grid(True, alpha=0.2, color='#7c8db5', axis='y')
        ax3.tick_params(colors='#ffffff')
        ax3.axhline(y=100, color='#FFD700', linestyle='--', linewidth=2, label='Optimal')
        ax3.legend(facecolor='#2d3548', edgecolor='#00d4ff', labelcolor='#ffffff')
        
        # Subplot 4: Scatter Plot
        ax4 = fig.add_subplot(2, 2, 4, facecolor='#0f1429')
        ax4.scatter(scramble_depths, ai_solution, s=200, c='#2ecc71',
                   alpha=0.6, edgecolors='#4dff91', linewidth=2, label='AI Solution')
        ax4.scatter(scramble_depths, optimal, s=200, c='#FFD700',
                   alpha=0.6, edgecolors='#FFE44D', linewidth=2, label='Optimal')
        ax4.plot(scramble_depths, ai_solution, color='#2ecc71', linewidth=2, alpha=0.5)
        ax4.plot(scramble_depths, optimal, color='#FFD700', linewidth=2, alpha=0.5)
        ax4.set_xlabel('Scramble Depth', color='#00d4ff', fontsize=11, fontweight='bold')
        ax4.set_ylabel('Solution Moves', color='#00d4ff', fontsize=11, fontweight='bold')
        ax4.set_title('AI vs Optimal Solution', color='#00d4ff', fontsize=13,
                     fontweight='bold', pad=15)
        ax4.legend(facecolor='#2d3548', edgecolor='#00d4ff', labelcolor='#ffffff')
        ax4.grid(True, alpha=0.2, color='#7c8db5')
        ax4.tick_params(colors='#ffffff')
        
        fig.tight_layout(pad=3.0)
        
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def show_comprehensive_analysis(self):
        self.clear_content()
        
        fig = Figure(figsize=(14, 8), facecolor='#1a1f3a')
        
        # Performance metrics
        categories = ['Speed', 'Efficiency', 'Optimality', 'Consistency', 'Reliability', 'Learning']
        values = [95, 92, 88, 96, 94, 90]
        
        # Subplot 1: Radar Chart
        ax1 = fig.add_subplot(1, 2, 1, projection='polar', facecolor='#0f1429')
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        values_plot = values + [values[0]]
        angles += angles[:1]
        
        ax1.plot(angles, values_plot, 'o-', linewidth=3, color='#2ecc71',
                markersize=10, markerfacecolor='#4dff91')
        ax1.fill(angles, values_plot, alpha=0.25, color='#2ecc71')
        ax1.set_xticks(angles[:-1])
        ax1.set_xticklabels(categories, color='#00d4ff', fontsize=11, fontweight='bold')
        ax1.set_ylim(0, 100)
        ax1.set_yticks([20, 40, 60, 80, 100])
        ax1.set_yticklabels(['20', '40', '60', '80', '100'], color='#ffffff', fontsize=9)
        ax1.set_title('AI Performance Metrics', color='#00d4ff', fontsize=14,
                     fontweight='bold', pad=20)
        ax1.grid(True, color='#7c8db5', alpha=0.3)
        
        # Subplot 2: Horizontal Bar Chart
        ax2 = fig.add_subplot(1, 2, 2, facecolor='#0f1429')
        colors = ['#ff3b3b', '#2ecc71', '#FFD700', '#9b59b6', '#3498db', '#ff8c00']
        y_pos = np.arange(len(categories))
        
        bars = ax2.barh(y_pos, values, color=colors, edgecolor='white',
                       linewidth=2, height=0.6)
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, values)):
            ax2.text(value + 1, i, f'{value}%', va='center',
                    color='#ffffff', fontweight='bold', fontsize=11)
        
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(categories, color='#00d4ff', fontsize=11, fontweight='bold')
        ax2.set_xlabel('Performance Score (%)', color='#00d4ff', fontsize=11, fontweight='bold')
        ax2.set_title('Performance Breakdown', color='#00d4ff', fontsize=14,
                     fontweight='bold', pad=20)
        ax2.set_xlim(0, 105)
        ax2.grid(True, alpha=0.2, color='#7c8db5', axis='x')
        ax2.tick_params(colors='#ffffff')
        ax2.invert_yaxis()
        
        fig.tight_layout(pad=3.0)
        
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def show_demo_results(self):
        self.clear_content()
        
        fig = Figure(figsize=(14, 8), facecolor='#1a1f3a')
        
        # Demo data
        trials = np.arange(1, 11)
        scramble = np.array([10, 15, 8, 12, 20, 7, 18, 10, 14, 16])
        solution = np.array([15, 23, 12, 18, 31, 11, 28, 15, 21, 25])
        time_taken = np.array([2.3, 3.5, 1.8, 2.7, 4.6, 1.6, 4.1, 2.2, 3.2, 3.8])
        
        # Subplot 1: Moves Comparison
        ax1 = fig.add_subplot(2, 2, 1, facecolor='#0f1429')
        width = 0.35
        x = trials
        
        bars1 = ax1.bar(x - width/2, scramble, width, label='Scramble Moves',
                       color='#9b59b6', edgecolor='#bb79d6', linewidth=2)
        bars2 = ax1.bar(x + width/2, solution, width, label='Solution Moves',
                       color='#2ecc71', edgecolor='#4dff91', linewidth=2)
        
        ax1.set_xlabel('Trial Number', color='#00d4ff', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Number of Moves', color='#00d4ff', fontsize=11, fontweight='bold')
        ax1.set_title('Demo Trial Results', color='#00d4ff', fontsize=13,
                     fontweight='bold', pad=15)
        ax1.set_xticks(trials)
        ax1.legend(facecolor='#2d3548', edgecolor='#00d4ff', labelcolor='#ffffff')
        ax1.grid(True, alpha=0.2, color='#7c8db5', axis='y')
        ax1.tick_params(colors='#ffffff')
        
        # Subplot 2: Solution Time
        ax2 = fig.add_subplot(2, 2, 2, facecolor='#0f1429')
        colors_time = plt.cm.plasma(time_taken / time_taken.max())
        bars = ax2.bar(trials, time_taken, color=colors_time,
                      edgecolor='#00d4ff', linewidth=2)
        ax2.set_xlabel('Trial Number', color='#00d4ff', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Time (seconds)', color='#00d4ff', fontsize=11, fontweight='bold')
        ax2.set_title('Solution Time per Trial', color='#00d4ff', fontsize=13,
                     fontweight='bold', pad=15)
        ax2.set_xticks(trials)
        ax2.grid(True, alpha=0.2, color='#7c8db5', axis='y')
        ax2.tick_params(colors='#ffffff')
        
        # Add average line
        avg_time = time_taken.mean()
        ax2.axhline(y=avg_time, color='#FFD700', linestyle='--',
                   linewidth=2, label=f'Average: {avg_time:.2f}s')
        ax2.legend(facecolor='#2d3548', edgecolor='#00d4ff', labelcolor='#ffffff')
        
        # Subplot 3: Efficiency Scatter
        ax3 = fig.add_subplot(2, 2, 3, facecolor='#0f1429')
        efficiency_ratio = solution / scramble
        ax3.scatter(scramble, solution, s=time_taken*100, c=trials,
                   cmap='viridis', alpha=0.6, edgecolors='#00d4ff', linewidth=2)
        
        # Trend line
        z = np.polyfit(scramble, solution, 1)
        p = np.poly1d(z)
        ax3.plot(scramble, p(scramble), "r--", linewidth=2,
                color='#ff3b3b', label='Trend')
        
        ax3.set_xlabel('Scramble Moves', color='#00d4ff', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Solution Moves', color='#00d4ff', fontsize=11, fontweight='bold')
        ax3.set_title('Scramble vs Solution Correlation', color='#00d4ff',
                     fontsize=13, fontweight='bold', pad=15)
        ax3.legend(facecolor='#2d3548', edgecolor='#00d4ff', labelcolor='#ffffff')
        ax3.grid(True, alpha=0.2, color='#7c8db5')
        ax3.tick_params(colors='#ffffff')
        
        # Subplot 4: Summary Stats
        ax4 = fig.add_subplot(2, 2, 4, facecolor='#0f1429')
        ax4.axis('off')
        ax4.set_xlim(0, 10)
        ax4.set_ylim(0, 14)
        
        # Title
        ax4.text(5, 13, "DEMO STATISTICS", 
                ha='center', va='top', fontsize=13, fontweight='bold',
                color='#00d4ff', fontfamily='monospace')
        
        # Draw border
        from matplotlib.patches import Rectangle
        rect = Rectangle((0.5, 0.5), 9, 11.5, linewidth=3, 
                         edgecolor='#00ff88', facecolor='none')
        ax4.add_patch(rect)
        
        # Create stats as separate text elements with larger spacing
        stats_data = [
            ("Total Trials:", f"{len(trials)}"),
            ("", ""),
            ("Avg Scramble Depth:", f"{scramble.mean():.1f}"),
            ("Avg Solution Moves:", f"{solution.mean():.1f}"),
            ("Avg Solution Time:", f"{time_taken.mean():.2f}s"),
            ("", ""),
            ("Min Solution Moves:", f"{solution.min()}"),
            ("Max Solution Moves:", f"{solution.max()}"),
            ("", ""),
            ("Fastest Solve:", f"{time_taken.min():.2f}s"),
            ("Slowest Solve:", f"{time_taken.max():.2f}s"),
            ("", ""),
            ("Success Rate:", "100.0%"),
        ]
        
        # Add stats with proper spacing
        y_position = 11
        line_height = 0.8
        
        for label, value in stats_data:
            if label == "":
                y_position -= line_height * 0.5
                continue
            
            # Label on left
            ax4.text(1.2, y_position, label, 
                    ha='left', va='center', fontsize=10,
                    color='#00ff88', fontfamily='monospace', fontweight='bold')
            
            # Value on right
            ax4.text(8.8, y_position, value, 
                    ha='right', va='center', fontsize=10,
                    color='#ffffff', fontfamily='monospace', fontweight='bold')
            
            y_position -= line_height
        
        fig.tight_layout(pad=3.0)
        
        canvas = FigureCanvasTkAgg(fig, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

def main():
    root = tk.Tk()
    app = RubiksCubeGraphs(root)
    root.mainloop()

if __name__ == "__main__":
    main()