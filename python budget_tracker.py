import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB = True
except ImportError:
    MATPLOTLIB = False
try:
    import pandas as pd
    PANDAS = True
except ImportError:
    PANDAS = False

DATA_FILE = 'budget_data.json'

# Premium color scheme with elegant tones
COLORS = {
    'bg_primary': '#1A1F2E',
    'bg_secondary': '#2D3748',
    'bg_light': '#F7FAFC',
    'bg_card': '#FFFFFF',
    'accent': '#4A90E2',
    'accent_hover': '#357ABD',
    'success': '#48BB78',
    'danger': '#F56565',
    'text_primary': '#1A202C',
    'text_secondary': '#718096',
    'text_light': '#A0AEC0',
    'white': '#FFFFFF',
    'border': '#E2E8F0',
    'shadow': '#00000015'
}

# Elegant font families with smaller sizes (fallback to system fonts)
FONTS = {
    'title': ('Georgia', 20, 'bold'),  # Elegant serif for main title
    'heading': ('Palatino Linotype', 16, 'bold'),  # Classy serif for headings
    'subheading': ('Garamond', 12, 'bold'),  # Refined serif for subheadings
    'body': ('Segoe UI', 9),  # Clean sans-serif for body
    'body_bold': ('Segoe UI', 9, 'bold'),
    'button': ('Segoe UI', 10, 'bold'),
    'label': ('Segoe UI', 9, 'bold'),
    'tab': ('Segoe UI', 10, 'bold'),
    'treeview': ('Segoe UI', 8),
    'treeview_heading': ('Segoe UI', 9, 'bold')
}

class BudgetTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Budget Tracker")
        self.root.geometry("1000x700")
        self.root.configure(bg=COLORS['bg_light'])
        self.expenses = []
        self.categories = set(['Food', 'Transport', 'Entertainment', 'Utilities', 'Other'])
        self.load_data()
        
        # Configure style
        self.setup_styles()
        
        # Header frame with elegant gradient effect
        header_frame = tk.Frame(root, bg=COLORS['bg_primary'], height=70)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Decorative line
        decor_line = tk.Frame(header_frame, bg=COLORS['accent'], height=3)
        decor_line.pack(fill=tk.X, side=tk.BOTTOM)
        
        title_label = tk.Label(
            header_frame, 
            text="Personal Budget Tracker", 
            font=FONTS['title'],
            bg=COLORS['bg_primary'],
            fg=COLORS['white']
        )
        title_label.pack(pady=18)
        
        # Tabs with modern styling
        self.tab_control = ttk.Notebook(root, style='Custom.TNotebook')
        self.add_tab = tk.Frame(self.tab_control, bg=COLORS['bg_light'])
        self.view_tab = tk.Frame(self.tab_control, bg=COLORS['bg_light'])
        self.summary_tab = tk.Frame(self.tab_control, bg=COLORS['bg_light'])
        self.tab_control.add(self.add_tab, text="Add Expense")
        self.tab_control.add(self.view_tab, text="View Expenses")
        self.tab_control.add(self.summary_tab, text="Summary")
        self.tab_control.pack(expand=1, fill="both", padx=10, pady=10)
        
        self.setup_add_tab()
        self.setup_view_tab()
        self.setup_summary_tab()
        
        # Menu with elegant styling
        menubar = tk.Menu(root, font=FONTS['body'], bg=COLORS['bg_card'], fg=COLORS['text_primary'])
        filemenu = tk.Menu(menubar, tearoff=0, font=FONTS['body'], bg=COLORS['bg_card'], fg=COLORS['text_primary'])
        filemenu.add_command(label="Save", command=self.save_data)
        filemenu.add_command(label="Load", command=lambda: self.load_data(show_message=True))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)
    
    def create_scrollable_frame(self, parent):
        """Create a scrollable frame with canvas and scrollbar"""
        # Create main container
        container = tk.Frame(parent, bg=COLORS['bg_light'])
        container.pack(fill="both", expand=True)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(container, bg=COLORS['bg_light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_light'])
        
        # Configure scrollable frame
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        scrollable_frame.bind("<Configure>", configure_scroll_region)
        
        # Create window in canvas
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Make canvas window resize with canvas
        def configure_canvas_width(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        canvas.bind('<Configure>', configure_canvas_width)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas (Windows)
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
        # Linux/Unix
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        
        return scrollable_frame, canvas
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Notebook style with elegant customization
        style.configure('Custom.TNotebook', 
                       background=COLORS['bg_light'], 
                       borderwidth=0,
                       tabmargins=[2, 5, 2, 0])
        style.configure('Custom.TNotebook.Tab', 
                       padding=[20, 10],
                       font=FONTS['tab'],
                       background=COLORS['bg_secondary'],
                       foreground=COLORS['white'],
                       borderwidth=0,
                       focuscolor='none')
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', COLORS['accent']), 
                           ('active', COLORS['accent_hover'])],
                 expand=[('selected', [1, 1, 1, 0])])
        
        # Treeview style with refined appearance
        style.configure('Custom.Treeview',
                       background=COLORS['bg_card'],
                       foreground=COLORS['text_primary'],
                       fieldbackground=COLORS['bg_card'],
                       font=FONTS['treeview'],
                       rowheight=24,
                       borderwidth=0)
        style.configure('Custom.Treeview.Heading',
                       background=COLORS['bg_secondary'],
                       foreground=COLORS['white'],
                       font=FONTS['treeview_heading'],
                       relief=tk.FLAT,
                       borderwidth=0)
        style.map('Custom.Treeview',
                 background=[('selected', COLORS['accent'])],
                 foreground=[('selected', COLORS['white'])])
        
        # Combobox style
        style.configure('Custom.TCombobox',
                       fieldbackground=COLORS['bg_card'],
                       background=COLORS['bg_card'],
                       borderwidth=1,
                       relief=tk.FLAT)

    def load_data(self, show_message=False):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.expenses = data.get('expenses', [])
                    self.categories.update(data.get('categories', []))
                if show_message:
                    messagebox.showinfo("Loaded", "Data loaded successfully.")
            except:
                if show_message:
                    messagebox.showerror("Error", "Failed to load data.")

    def save_data(self):
        data = {'expenses': self.expenses, 'categories': list(self.categories)}
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            messagebox.showinfo("Success", "💾 Data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

    def setup_add_tab(self):
        # Create scrollable frame
        scrollable_frame, canvas = self.create_scrollable_frame(self.add_tab)
        
        # Main container frame
        main_frame = tk.Frame(scrollable_frame, bg=COLORS['bg_light'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)
        
        # Form container with elegant card-like appearance
        form_frame = tk.Frame(main_frame, bg=COLORS['bg_card'], relief=tk.FLAT, bd=0)
        form_frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        # Decorative top border
        top_border = tk.Frame(form_frame, bg=COLORS['accent'], height=2)
        top_border.pack(fill=tk.X, pady=(0, 18))
        
        # Title with elegant typography
        title_label = tk.Label(
            form_frame,
            text="Add New Expense",
            font=FONTS['heading'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary']
        )
        title_label.pack(pady=(18, 20))
        
        # Form fields container
        fields_frame = tk.Frame(form_frame, bg=COLORS['bg_card'])
        fields_frame.pack(expand=True, padx=50, pady=20)
        
        # Amount field
        amount_label = tk.Label(
            fields_frame,
            text="Amount ($)",
            font=FONTS['label'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            anchor='w'
        )
        amount_label.grid(row=0, column=0, padx=15, pady=12, sticky='w')
        self.amount_entry = tk.Entry(
            fields_frame,
            font=FONTS['body'],
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightcolor=COLORS['accent'],
            highlightbackground=COLORS['border'],
            width=32,
            bg=COLORS['bg_card'],
            insertbackground=COLORS['text_primary']
        )
        self.amount_entry.grid(row=0, column=1, padx=15, pady=12, ipady=6, sticky='ew')
        
        # Category field
        category_label = tk.Label(
            fields_frame,
            text="Category",
            font=FONTS['label'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            anchor='w'
        )
        category_label.grid(row=1, column=0, padx=15, pady=12, sticky='w')
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            fields_frame,
            textvariable=self.category_var,
            values=sorted(self.categories),
            font=FONTS['body'],
            width=29,
            state='readonly',
            style='Custom.TCombobox'
        )
        self.category_combo.grid(row=1, column=1, padx=15, pady=12, ipady=6, sticky='ew')
        
        # Description field
        desc_label = tk.Label(
            fields_frame,
            text="Description",
            font=FONTS['label'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            anchor='w'
        )
        desc_label.grid(row=2, column=0, padx=15, pady=12, sticky='w')
        self.desc_entry = tk.Entry(
            fields_frame,
            font=FONTS['body'],
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightcolor=COLORS['accent'],
            highlightbackground=COLORS['border'],
            width=32,
            bg=COLORS['bg_card'],
            insertbackground=COLORS['text_primary']
        )
        self.desc_entry.grid(row=2, column=1, padx=15, pady=12, ipady=6, sticky='ew')
        
        fields_frame.grid_columnconfigure(1, weight=1)
        
        # Button frame
        button_frame = tk.Frame(form_frame, bg=COLORS['bg_card'])
        button_frame.pack(pady=25)
        
        add_button = tk.Button(
            button_frame,
            text="Add Expense",
            command=self.add_expense,
            font=FONTS['button'],
            bg=COLORS['success'],
            fg=COLORS['white'],
            relief=tk.FLAT,
            bd=0,
            padx=35,
            pady=10,
            cursor='hand2',
            activebackground='#38A169',
            activeforeground=COLORS['white'],
            width=18
        )
        add_button.pack()

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_var.get().strip().title()
            desc = self.desc_entry.get().strip()
            if amount <= 0 or not category or not desc:
                raise ValueError
            if category not in self.categories:
                self.categories.add(category)
                self.category_combo['values'] = sorted(self.categories)
            date = datetime.now().strftime("%Y-%m-%d")
            self.expenses.append({
                'id': len(self.expenses) + 1,
                'amount': amount,
                'category': category,
                'description': desc,
                'date': date
            })
            self.save_data()
            self.amount_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.category_var.set('')
            messagebox.showinfo("Success", f"✅ Expense of ${amount:,.2f} added successfully!")
            self.refresh_view()
        except ValueError:
            messagebox.showerror("Error", "❌ Invalid input. Please check:\n• Amount must be a positive number\n• Category is required\n• Description is required")

    def setup_view_tab(self):
        # Create scrollable frame
        scrollable_frame, canvas = self.create_scrollable_frame(self.view_tab)
        
        # Main container
        main_frame = tk.Frame(scrollable_frame, bg=COLORS['bg_light'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Expense History",
            font=FONTS['heading'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_primary']
        )
        title_label.pack(pady=(12, 18))
        
        # Treeview container with elegant styling
        tree_frame = tk.Frame(main_frame, bg=COLORS['bg_card'], relief=tk.FLAT, bd=0)
        tree_frame.pack(expand=True, fill=tk.BOTH, padx=12, pady=12)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Date", "Description", "Amount", "Category"),
            show="headings",
            style='Custom.Treeview',
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        # Configure scrollbars
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        
        self.tree.column("ID", width=50, anchor='center')
        self.tree.column("Date", width=120, anchor='center')
        self.tree.column("Description", width=300, anchor='w')
        self.tree.column("Amount", width=120, anchor='e')
        self.tree.column("Category", width=150, anchor='center')
        
        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        self.refresh_view()
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=COLORS['bg_light'])
        button_frame.pack(pady=12)
        
        delete_button = tk.Button(
            button_frame,
            text="Delete Selected",
            command=self.delete_expense,
            font=FONTS['button'],
            bg=COLORS['danger'],
            fg=COLORS['white'],
            relief=tk.FLAT,
            bd=0,
            padx=25,
            pady=8,
            cursor='hand2',
            activebackground='#E53E3E',
            activeforeground=COLORS['white'],
            width=16
        )
        delete_button.pack()

    def refresh_view(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        # Sort by date descending (newest first)
        sorted_expenses = sorted(self.expenses, key=lambda x: x['date'], reverse=True)
        for exp in sorted_expenses:
            self.tree.insert("", tk.END, values=(
                exp['id'],
                exp['date'],
                exp['description'],
                f"${exp['amount']:,.2f}",
                exp['category']
            ))

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "❌ Please select an expense to delete.")
            return
        item = self.tree.item(selected[0])
        exp_id = item['values'][0]
        exp_desc = item['values'][2]
        self.expenses = [e for e in self.expenses if e['id'] != exp_id]
        self.save_data()
        self.refresh_view()
        messagebox.showinfo("Deleted", f"✅ Expense '{exp_desc}' deleted successfully.")

    def setup_summary_tab(self):
        # Create scrollable frame
        scrollable_frame, canvas = self.create_scrollable_frame(self.summary_tab)
        
        # Main container
        main_frame = tk.Frame(scrollable_frame, bg=COLORS['bg_light'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Budget Summary",
            font=FONTS['heading'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_primary']
        )
        title_label.pack(pady=(12, 18))
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=COLORS['bg_light'])
        button_frame.pack(pady=10)
        
        summary_button = tk.Button(
            button_frame,
            text="Generate Summary",
            command=self.show_summary,
            font=FONTS['button'],
            bg=COLORS['accent'],
            fg=COLORS['white'],
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2',
            activebackground=COLORS['accent_hover'],
            activeforeground=COLORS['white'],
            width=18
        )
        summary_button.pack()
        
        # Summary text container with elegant styling
        text_frame = tk.Frame(main_frame, bg=COLORS['bg_card'], relief=tk.FLAT, bd=0)
        text_frame.pack(expand=True, fill=tk.BOTH, padx=12, pady=12)
        
        self.summary_text = tk.Text(
            text_frame,
            height=10,
            width=50,
            font=FONTS['body'],
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightcolor=COLORS['accent'],
            highlightbackground=COLORS['border'],
            wrap=tk.WORD,
            padx=15,
            pady=15,
            selectbackground=COLORS['accent'],
            selectforeground=COLORS['white']
        )
        self.summary_text.pack(expand=True, fill=tk.BOTH, padx=12, pady=12)
        
        if MATPLOTLIB:
            self.chart_frame = tk.Frame(main_frame, bg=COLORS['bg_card'], relief=tk.FLAT, bd=0)
            self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

    def show_summary(self):
        if PANDAS:
            df = pd.DataFrame(self.expenses)
            total = df['amount'].sum() if not df.empty else 0
            cat_totals = df.groupby('category')['amount'].sum().to_dict() if not df.empty else {}
        else:
            total = sum(e['amount'] for e in self.expenses)
            cat_totals = {}
            for e in self.expenses:
                cat_totals[e['category']] = cat_totals.get(e['category'], 0) + e['amount']
        
        self.summary_text.delete(1.0, tk.END)
        if not self.expenses:
            self.summary_text.insert(tk.END, "No expenses recorded yet.\n\n", ('empty',))
            self.summary_text.insert(tk.END, "Add some expenses to see your budget summary here.", ('empty',))
            self.summary_text.tag_config('empty', foreground=COLORS['text_secondary'], font=FONTS['body'])
        else:
            # Configure text tags for elegant formatting
            self.summary_text.tag_config('total', font=FONTS['body_bold'], foreground=COLORS['text_primary'])
            self.summary_text.tag_config('header', font=FONTS['body_bold'], foreground=COLORS['text_primary'])
            self.summary_text.tag_config('category', font=FONTS['body'], foreground=COLORS['text_primary'])
            self.summary_text.tag_config('amount', font=FONTS['body'], foreground=COLORS['accent'])
            
            self.summary_text.insert(tk.END, "Total Spending: ", 'total')
            self.summary_text.insert(tk.END, f"${total:,.2f}\n\n", 'amount')
            self.summary_text.insert(tk.END, "Spending by Category:\n\n", 'header')
            # Sort by amount descending
            sorted_cats = sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)
            for cat, amt in sorted_cats:
                percentage = (amt / total * 100) if total > 0 else 0
                self.summary_text.insert(tk.END, f"  • {cat}: ", 'category')
                self.summary_text.insert(tk.END, f"${amt:,.2f} ", 'amount')
                self.summary_text.insert(tk.END, f"({percentage:.1f}%)\n", 'category')
        
        # Clear previous chart
        if MATPLOTLIB:
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            
            if cat_totals:
                # Modern chart styling
                try:
                    plt.style.use('seaborn-v0_8-darkgrid')
                except:
                    try:
                        plt.style.use('seaborn-darkgrid')
                    except:
                        pass
                fig, ax = plt.subplots(figsize=(8, 6), facecolor='white')
                
                # Color palette
                colors = ['#3498DB', '#27AE60', '#E74C3C', '#F39C12', '#9B59B6', '#1ABC9C', '#E67E22']
                
                wedges, texts, autotexts = ax.pie(
                    cat_totals.values(),
                    labels=cat_totals.keys(),
                    autopct='%1.1f%%',
                    colors=colors[:len(cat_totals)],
                    startangle=90,
                    textprops={'fontsize': 8, 'fontweight': 'bold'}
                )
                
                ax.set_title("Spending by Category", fontsize=12, fontweight='bold', pad=20, 
                            fontfamily='serif', color=COLORS['text_primary'])
                
                # Make percentage text more visible
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                
                plt.tight_layout()
                canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()