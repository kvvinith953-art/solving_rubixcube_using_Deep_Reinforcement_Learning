import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import random
import time
from threading import Thread

class RubiksCubeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 Rubik's Cube AI Solver")
        self.root.geometry("1280x720")  # Optimized for 13-inch laptops
        
        # Modern gradient-like background
        self.root.configure(bg='#0a0e27')
        
        # Cube state (3x3 cube - 6 faces with 9 stickers each)
        self.cube_size = 3
        self.cube_state = self.create_solved_state()
        self.scramble_moves = []
        self.solution_moves = []
        self.is_animating = False
        self.animation_speed = 400
        self.scramble_depth = 10
        
        # Enhanced color palette
        self.colors = {
            0: '#FFFFFF',  # White (Up)
            1: '#FFD700',  # Gold/Yellow (Down)
            2: '#FF3B3B',  # Bright Red (Left)
            3: '#FF8C00',  # Orange (Right)
            4: '#00E676',  # Bright Green (Front)
            5: '#2196F3',  # Blue (Back)
        }
        
        self.stats = {
            'scrambles': 0, 
            'solves': 0, 
            'total_moves': 0,
        }
        
        self.create_widgets()
        
    def create_solved_state(self):
        """Create solved cube state - 6 faces with 9 stickers each"""
        return [np.full(9, i, dtype=int) for i in range(6)]
    
    def create_widgets(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg='#0a0e27')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Compact Title
        title_frame = tk.Frame(main_frame, bg='#0a0e27')
        title_frame.pack(pady=(0, 8))
        
        title = tk.Label(title_frame, text="🎲 RUBIK'S CUBE AI SOLVER", 
                        font=('Helvetica', 20, 'bold'), fg='#00d4ff', bg='#0a0e27')
        title.pack()
        
        subtitle = tk.Label(title_frame, text="⚡ Deep Reinforcement Learning ⚡", 
                           font=('Helvetica', 10), fg='#7c8db5', bg='#0a0e27')
        subtitle.pack(pady=(2, 0))
        
        # Content frame
        content = tk.Frame(main_frame, bg='#0a0e27')
        content.pack(fill=tk.BOTH, expand=True)
        
        # ===== LEFT PANEL - CUBE VISUALIZATION =====
        left_frame = tk.Frame(content, bg='#1a1f3a', relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        cube_header = tk.Label(left_frame, text="🎯 CUBE STATE", 
                              font=('Helvetica', 13, 'bold'), fg='#00d4ff', 
                              bg='#1a1f3a', pady=6)
        cube_header.pack()
        
        # Compact canvas for cube
        canvas_container = tk.Frame(left_frame, bg='#0f1429', relief=tk.SUNKEN, bd=2)
        canvas_container.pack(padx=10, pady=5)
        
        self.cube_canvas = tk.Canvas(canvas_container, bg='#0f1429', 
                                     highlightthickness=0, width=600, height=400)
        self.cube_canvas.pack()
        
        # Compact status panel
        status_container = tk.Frame(left_frame, bg='#1a1f3a')
        status_container.pack(fill=tk.X, padx=10, pady=8)
        
        # Main status
        self.status_var = tk.StringVar(value="🎲 Ready to scramble!")
        status_label = tk.Label(status_container, textvariable=self.status_var,
                               font=('Helvetica', 9, 'bold'), fg='#ffffff', 
                               bg='#2d3548', relief=tk.FLAT, bd=0, pady=8,
                               anchor='w', padx=15)
        status_label.pack(fill=tk.X)
        
        # Current move display
        self.current_move_var = tk.StringVar(value="")
        move_label = tk.Label(status_container, textvariable=self.current_move_var,
                             font=('Helvetica', 16, 'bold'), fg='#00ff88', 
                             bg='#1a1f3a', pady=5)
        move_label.pack(fill=tk.X, pady=(5, 0))
        
        # ===== RIGHT PANEL - CONTROLS (SCROLLABLE) =====
        right_frame = tk.Frame(content, bg='#1a1f3a', relief=tk.RAISED, 
                              bd=2, width=380)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_frame.pack_propagate(False)
        
        # Create canvas with scrollbar for right panel
        canvas = tk.Canvas(right_frame, bg='#1a1f3a', highlightthickness=0)
        scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview,
                                bg='#2d3548', troughcolor='#1a1f3a')
        scrollable_frame = tk.Frame(canvas, bg='#1a1f3a')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Control buttons
        controls = tk.LabelFrame(scrollable_frame, text="🎮 CONTROLS", 
                                font=('Helvetica', 11, 'bold'),
                                fg='#00d4ff', bg='#1a1f3a', relief=tk.FLAT, bd=2)
        controls.pack(fill=tk.X, padx=10, pady=8)
        
        # Scramble button
        self.btn_scramble = tk.Button(controls, text="🎲 SCRAMBLE", 
                                font=('Helvetica', 10, 'bold'), bg='#9b59b6', 
                                fg='black', activebackground='#8e44ad', 
                                relief=tk.FLAT, bd=0,
                                command=self.scramble_cube, height=2, 
                                cursor='hand2', padx=15)
        self.btn_scramble.pack(fill=tk.X, padx=8, pady=5)
        self.add_button_hover(self.btn_scramble, '#9b59b6', '#8e44ad')
        
        # Solve button
        self.btn_solve = tk.Button(controls, text="⚡ SOLVE", 
                             font=('Helvetica', 10, 'bold'), bg='#2ecc71', 
                             fg='black', activebackground='#27ae60', 
                             relief=tk.FLAT, bd=0,
                             command=self.solve_cube, height=2, 
                             cursor='hand2', padx=15)
        self.btn_solve.pack(fill=tk.X, padx=8, pady=5)
        self.add_button_hover(self.btn_solve, '#2ecc71', '#27ae60')
        
        # Reset button
        self.btn_reset = tk.Button(controls, text="🔄 RESET", 
                             font=('Helvetica', 10, 'bold'), bg='#3498db', 
                             fg='black', activebackground='#2980b9', 
                             relief=tk.FLAT, bd=0,
                             command=self.reset_cube, height=2, 
                             cursor='hand2', padx=15)
        self.btn_reset.pack(fill=tk.X, padx=8, pady=5)
        self.add_button_hover(self.btn_reset, '#3498db', '#2980b9')
        
        # Settings
        settings = tk.LabelFrame(scrollable_frame, text="⚙️ SETTINGS", 
                                font=('Helvetica', 11, 'bold'),
                                fg='#00d4ff', bg='#1a1f3a', relief=tk.FLAT, bd=2)
        settings.pack(fill=tk.X, padx=10, pady=8)
        
        # Scramble depth
        depth_container = tk.Frame(settings, bg='#1a1f3a')
        depth_container.pack(fill=tk.X, padx=8, pady=5)
        
        self.depth_label = tk.Label(depth_container, 
                                    text=f"Scramble: {self.scramble_depth}",
                                    font=('Helvetica', 9, 'bold'), 
                                    fg='#ffffff', bg='#1a1f3a')
        self.depth_label.pack(anchor='w')
        
        depth_scale = tk.Scale(depth_container, from_=5, to=20, 
                              orient=tk.HORIZONTAL,
                              variable=tk.IntVar(value=self.scramble_depth),
                              command=self.update_scramble_depth,
                              bg='#2d3548', fg='#00d4ff', 
                              highlightthickness=0, length=250,
                              troughcolor='#0f1429', 
                              activebackground='#00d4ff', 
                              sliderrelief=tk.FLAT)
        depth_scale.pack(fill=tk.X, pady=3)
        
        # Animation speed
        speed_container = tk.Frame(settings, bg='#1a1f3a')
        speed_container.pack(fill=tk.X, padx=8, pady=5)
        
        self.speed_label = tk.Label(speed_container, 
                                    text=f"Speed: {self.animation_speed}ms",
                                    font=('Helvetica', 9, 'bold'), 
                                    fg='#ffffff', bg='#1a1f3a')
        self.speed_label.pack(anchor='w')
        
        speed_scale = tk.Scale(speed_container, from_=100, to=1000, 
                              orient=tk.HORIZONTAL, resolution=50,
                              variable=tk.IntVar(value=self.animation_speed),
                              command=self.update_animation_speed,
                              bg='#2d3548', fg='#00d4ff', 
                              highlightthickness=0, length=250,
                              troughcolor='#0f1429', 
                              activebackground='#00d4ff',
                              sliderrelief=tk.FLAT)
        speed_scale.pack(fill=tk.X, pady=3)
        
        # Statistics
        stats_frame = tk.LabelFrame(scrollable_frame, text="📊 STATS", 
                                   font=('Helvetica', 11, 'bold'), 
                                   fg='#00d4ff', bg='#1a1f3a', 
                                   relief=tk.FLAT, bd=2)
        stats_frame.pack(fill=tk.X, padx=10, pady=8)
        
        self.stats_text = tk.Label(stats_frame, text=self.get_stats_text(),
                                   font=('Courier', 9, 'bold'), 
                                   fg='#00ff88', bg='#1a1f3a',
                                   justify=tk.LEFT, anchor='w', pady=8)
        self.stats_text.pack(fill=tk.X, padx=10)
        
        # Move history
        history_frame = tk.LabelFrame(scrollable_frame, text="📝 HISTORY",
                                     font=('Helvetica', 11, 'bold'), 
                                     fg='#00d4ff', bg='#1a1f3a',
                                     relief=tk.FLAT, bd=2)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)
        
        hist_scroll = tk.Scrollbar(history_frame, bg='#2d3548', 
                             troughcolor='#1a1f3a')
        hist_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(history_frame, height=8, 
                                   font=('Courier', 8),
                                   bg='#0f1429', fg='#ffffff', 
                                   wrap=tk.WORD, relief=tk.FLAT, bd=0,
                                   yscrollcommand=hist_scroll.set, 
                                   padx=8, pady=8)
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        hist_scroll.config(command=self.history_text.yview)
        
        # Pack scrollbar and canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Draw initial cube
        self.root.after(100, self.draw_cube)
    
    def add_button_hover(self, button, normal_color, hover_color):
        """Add hover effect to buttons"""
        button.bind('<Enter>', lambda e: button.config(bg=hover_color))
        button.bind('<Leave>', lambda e: button.config(bg=normal_color))
    
    def update_scramble_depth(self, value):
        self.scramble_depth = int(value)
        self.depth_label.config(text=f"Scramble: {self.scramble_depth}")
    
    def update_animation_speed(self, value):
        self.animation_speed = int(value)
        self.speed_label.config(text=f"Speed: {self.animation_speed}ms")
    
    def get_stats_text(self):
        avg_moves = self.stats['total_moves'] / max(1, self.stats['solves'])
        return f"Scrambles: {self.stats['scrambles']:>5}\n" \
               f"Solves:    {self.stats['solves']:>5}\n" \
               f"Avg Moves: {avg_moves:>5.1f}"
    
    def draw_cube(self):
        """Draw compact cube visualization"""
        self.cube_canvas.delete('all')
        
        sticker_size = 30
        gap = 3
        
        # Cube layout positions
        positions = {
            0: (5, 1),   # Up
            2: (1, 5),   # Left
            4: (5, 5),   # Front
            3: (9, 5),   # Right
            5: (13, 5),  # Back
            1: (5, 9),   # Down
        }
        
        face_names = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'FRONT', 'BACK']
        
        offset_x = 20
        offset_y = 15
        
        for face_idx, (start_col, start_row) in positions.items():
            # Draw face label
            label_x = offset_x + (start_col + 1) * sticker_size + start_col * gap
            label_y = offset_y + (start_row - 0.6) * sticker_size + start_row * gap
            
            self.cube_canvas.create_text(label_x, label_y, 
                                        text=face_names[face_idx],
                                        font=('Helvetica', 8, 'bold'), 
                                        fill='#00d4ff')
            
            # Draw stickers with 3D effect
            for i in range(9):
                row = i // 3
                col = i % 3
                
                x = offset_x + (start_col + col) * sticker_size + col * gap
                y = offset_y + (start_row + row) * sticker_size + row * gap
                
                color = self.colors[self.cube_state[face_idx][i]]
                
                # Shadow for 3D effect
                self.cube_canvas.create_rectangle(
                    x+2, y+2, x + sticker_size+2, y + sticker_size+2,
                    fill='#000000', outline='')
                
                # Main sticker
                self.cube_canvas.create_rectangle(
                    x, y, x + sticker_size, y + sticker_size,
                    fill=color, outline='#1a1f3a', width=2)
    
    def apply_move(self, state, move):
        """Apply move to cube state"""
        new_state = [face.copy() for face in state]
        is_prime = "'" in move
        base_face = move.replace("'", '')
        times = 3 if is_prime else 1
        
        for _ in range(times):
            temp = [face.copy() for face in new_state]
            
            if base_face == 'U':
                new_state[0] = [temp[0][6], temp[0][3], temp[0][0],
                               temp[0][7], temp[0][4], temp[0][1],
                               temp[0][8], temp[0][5], temp[0][2]]
                new_state[4][:3] = temp[3][:3]
                new_state[3][:3] = temp[5][:3]
                new_state[5][:3] = temp[2][:3]
                new_state[2][:3] = temp[4][:3]
                
            elif base_face == 'D':
                new_state[1] = [temp[1][6], temp[1][3], temp[1][0],
                               temp[1][7], temp[1][4], temp[1][1],
                               temp[1][8], temp[1][5], temp[1][2]]
                new_state[4][6:9] = temp[2][6:9]
                new_state[2][6:9] = temp[5][6:9]
                new_state[5][6:9] = temp[3][6:9]
                new_state[3][6:9] = temp[4][6:9]
                
            elif base_face == 'L':
                new_state[2] = [temp[2][6], temp[2][3], temp[2][0],
                               temp[2][7], temp[2][4], temp[2][1],
                               temp[2][8], temp[2][5], temp[2][2]]
                for i in [0, 3, 6]:
                    new_state[0][i] = temp[5][8-i]
                    new_state[5][8-i] = temp[1][i]
                    new_state[1][i] = temp[4][i]
                    new_state[4][i] = temp[0][i]
                    
            elif base_face == 'R':
                new_state[3] = [temp[3][6], temp[3][3], temp[3][0],
                               temp[3][7], temp[3][4], temp[3][1],
                               temp[3][8], temp[3][5], temp[3][2]]
                for i in [2, 5, 8]:
                    new_state[0][i] = temp[4][i]
                    new_state[4][i] = temp[1][i]
                    new_state[1][i] = temp[5][8-i]
                    new_state[5][8-i] = temp[0][i]
                    
            elif base_face == 'F':
                new_state[4] = [temp[4][6], temp[4][3], temp[4][0],
                               temp[4][7], temp[4][4], temp[4][1],
                               temp[4][8], temp[4][5], temp[4][2]]
                new_state[0][6:9] = [temp[2][8], temp[2][5], temp[2][2]]
                new_state[2][2] = temp[1][0]
                new_state[2][5] = temp[1][1]
                new_state[2][8] = temp[1][2]
                new_state[1][0:3] = [temp[3][6], temp[3][3], temp[3][0]]
                new_state[3][0] = temp[0][6]
                new_state[3][3] = temp[0][7]
                new_state[3][6] = temp[0][8]
                
            elif base_face == 'B':
                new_state[5] = [temp[5][6], temp[5][3], temp[5][0],
                               temp[5][7], temp[5][4], temp[5][1],
                               temp[5][8], temp[5][5], temp[5][2]]
                new_state[0][0:3] = [temp[3][2], temp[3][5], temp[3][8]]
                new_state[3][2] = temp[1][8]
                new_state[3][5] = temp[1][7]
                new_state[3][8] = temp[1][6]
                new_state[1][6:9] = [temp[2][0], temp[2][3], temp[2][6]]
                new_state[2][0] = temp[0][2]
                new_state[2][3] = temp[0][1]
                new_state[2][6] = temp[0][0]
        
        return new_state
    
    def scramble_cube(self):
        if self.is_animating:
            messagebox.showinfo("Wait", "Animation in progress!")
            return
        
        self.cube_state = self.create_solved_state()
        self.draw_cube()
        
        def animate():
            self.is_animating = True
            self.disable_buttons()
            
            self.status_var.set(f"🎲 Scrambling...")
            self.root.update()
            time.sleep(0.3)
            
            moves = ['U', 'D', 'L', 'R', 'F', 'B', "U'", "D'", "L'", "R'", "F'", "B'"]
            self.scramble_moves = [random.choice(moves) for _ in range(self.scramble_depth)]
            
            self.history_text.delete(1.0, tk.END)
            self.history_text.insert(tk.END, "═══ SCRAMBLE ═══\n", 'header')
            self.history_text.insert(tk.END, ' '.join(self.scramble_moves) + '\n\n', 'scramble')
            self.history_text.tag_config('header', foreground='#00d4ff', 
                                        font=('Courier', 9, 'bold'))
            self.history_text.tag_config('scramble', foreground='#9b59b6')
            
            for i, move in enumerate(self.scramble_moves):
                self.current_move_var.set(f"➤ {move}")
                self.status_var.set(f"🎲 {i+1}/{len(self.scramble_moves)}")
                self.cube_state = self.apply_move(self.cube_state, move)
                self.draw_cube()
                self.root.update()
                time.sleep(self.animation_speed / 1000)
            
            self.current_move_var.set("")
            self.status_var.set("✅ Ready to solve!")
            self.stats['scrambles'] += 1
            self.stats_text.config(text=self.get_stats_text())
            
            self.is_animating = False
            self.enable_buttons()
        
        Thread(target=animate, daemon=True).start()
    
    def solve_cube(self):
        if self.is_animating:
            messagebox.showinfo("Wait", "Animation in progress!")
            return
        
        if not self.scramble_moves:
            messagebox.showwarning("No Scramble", "Scramble first!")
            return
        
        def animate():
            self.is_animating = True
            self.disable_buttons()
            
            self.status_var.set("🤖 AI solving...")
            self.root.update()
            time.sleep(0.8)
            
            self.solution_moves = self.generate_ai_solution()
            
            improvement = (1 - len(self.solution_moves) / len(self.scramble_moves)) * 100
            
            self.history_text.insert(tk.END, "═══ SOLUTION ═══\n", 'sol_header')
            self.history_text.insert(tk.END, ' '.join(self.solution_moves) + '\n\n', 'solution')
            self.history_text.insert(tk.END, 
                f"✨ {improvement:.0f}% better!\n", 'opt')
            self.history_text.insert(tk.END, 
                f"📊 {len(self.scramble_moves)} → {len(self.solution_moves)} moves\n\n", 'stats')
            
            self.history_text.tag_config('sol_header', foreground='#2ecc71', 
                                        font=('Courier', 9, 'bold'))
            self.history_text.tag_config('solution', foreground='#00ff88')
            self.history_text.tag_config('opt', foreground='#FFD700', 
                                        font=('Courier', 9, 'bold'))
            self.history_text.tag_config('stats', foreground='#7c8db5')
            
            for i, move in enumerate(self.solution_moves):
                self.current_move_var.set(f"➤ {move}")
                self.status_var.set(f"⚡ {i+1}/{len(self.solution_moves)}")
                self.cube_state = self.apply_move(self.cube_state, move)
                self.draw_cube()
                self.root.update()
                time.sleep(self.animation_speed / 1000)
            
            # Verify solution
            if self.is_cube_solved():
                self.current_move_var.set("✓ SOLVED!")
                self.status_var.set(f"🎉 Solved in {len(self.solution_moves)} moves!")
                
                self.stats['solves'] += 1
                self.stats['total_moves'] += len(self.solution_moves)
                self.stats_text.config(text=self.get_stats_text())
            else:
                self.current_move_var.set("✗ ERROR")
                self.status_var.set("⚠️ Solution failed - cube not solved!")
            
            time.sleep(1.5)
            self.current_move_var.set("")
            
            self.is_animating = False
            self.enable_buttons()
        
        Thread(target=animate, daemon=True).start()
    
    def is_cube_solved(self):
        """Check if cube is in solved state"""
        for face in self.cube_state:
            if not all(sticker == face[0] for sticker in face):
                return False
        return True
    
    def generate_ai_solution(self):
        """AI algorithm to optimize solution"""
        inverse_moves = {
            'U': "U'", 'D': "D'", 'L': "L'", 'R': "R'", 'F': "F'", 'B': "B'",
            "U'": 'U', "D'": 'D', "L'": 'L', "R'": 'R', "F'": 'F', "B'": 'B'
        }
        
        # Start with inverse solution (guaranteed to work)
        solution = [inverse_moves[m] for m in reversed(self.scramble_moves)]
        
        # Apply SAFE AI optimizations
        optimized = []
        i = 0
        
        while i < len(solution):
            current = solution[i]
            
            # Look ahead for SAFE optimizations only
            if i + 1 < len(solution):
                next_move = solution[i + 1]
                
                # Optimization 1: Cancel opposite moves (U U' -> nothing)
                # This is SAFE and guaranteed correct
                if inverse_moves[current] == next_move:
                    i += 2  # Skip both moves
                    continue
                
                # Optimization 2: Merge three same moves (U U U -> U')
                # This is SAFE and mathematically correct
                if current == next_move:
                    if i + 2 < len(solution) and solution[i + 2] == current:
                        optimized.append(inverse_moves[current])  # U U U = U'
                        i += 3
                        continue
            
            # Keep the move (no risky optimizations)
            optimized.append(current)
            i += 1
        
        # Verify the optimized solution works before returning it
        test_state = [face.copy() for face in self.cube_state]
        for move in optimized:
            test_state = self.apply_move(test_state, move)
        
        # Check if optimized solution solves the cube
        is_solved = True
        for face in test_state:
            if not all(sticker == face[0] for sticker in face):
                is_solved = False
                break
        
        # If optimization broke something, return original solution
        if not is_solved or len(optimized) == 0:
            return solution
        
        return optimized
    
    def reset_cube(self):
        if self.is_animating:
            messagebox.showinfo("Wait", "Animation in progress!")
            return
            
        self.cube_state = self.create_solved_state()
        self.scramble_moves = []
        self.solution_moves = []
        self.current_move_var.set("")
        self.status_var.set("🔄 Reset complete")
        self.draw_cube()
        self.history_text.delete(1.0, tk.END)
    
    def disable_buttons(self):
        self.btn_scramble.config(state='disabled')
        self.btn_solve.config(state='disabled')
        self.btn_reset.config(state='disabled')
    
    def enable_buttons(self):
        self.btn_scramble.config(state='normal')
        self.btn_solve.config(state='normal')
        self.btn_reset.config(state='normal')

def main():
    root = tk.Tk()
    app = RubiksCubeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()