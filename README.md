# 💰 Personal Budget Tracker

A modern, elegant desktop application for tracking personal expenses and managing your budget. Built with Python and Tkinter, featuring a beautiful user interface with scrollable tabs, elegant typography, and comprehensive expense management.

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

### Core Functionality
- **Add Expenses** - Record expenses with amount, category, description, and date
- **View Expenses** - Browse all expenses in a sortable table view
- **Delete Expenses** - Remove unwanted entries with a single click
- **Budget Summary** - Get detailed insights into your spending patterns
- **Category Management** - Organize expenses by categories (Food, Transport, Entertainment, Utilities, Other)
- **Auto-save** - Data is automatically saved to JSON file

### UI/UX Features
- **Modern Design** - Elegant color scheme with premium styling
- **Scrollable Interface** - All tabs support smooth scrolling
- **Responsive Layout** - Clean, organized interface with card-based design
- **Elegant Typography** - Professional fonts (Georgia, Palatino, Garamond, Segoe UI)
- **Visual Charts** - Pie charts showing spending by category (requires matplotlib)
- **Compact View** - Optimized font sizes for better information density

## 📋 Requirements

### Python Version
- Python 3.6 or higher (Python 3.8+ recommended)

### Built-in Modules (No Installation Required)
- `tkinter` - GUI framework
- `json` - Data persistence
- `os` - File operations
- `datetime` - Date handling

### Optional Dependencies
For enhanced features, install:
- **matplotlib** - For generating pie charts in the Summary tab
- **pandas** - For advanced data processing (optional, basic calculations work without it)

See [requirements.md](requirements.md) for detailed installation instructions.

## 🚀 Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd projects
   ```

2. **Install optional dependencies** (recommended)
   ```bash
   pip install matplotlib pandas
   ```

   Or install individually:
   ```bash
   pip install matplotlib
   pip install pandas
   ```

3. **Run the application**
   ```bash
   python budget_tracker.py
   ```

   On Linux/macOS:
   ```bash
   python3 budget_tracker.py
   ```

## 📖 Usage Guide

### Adding an Expense

1. Navigate to the **"Add Expense"** tab
2. Enter the expense amount (e.g., `25.50`)
3. Select or type a category (Food, Transport, Entertainment, Utilities, Other, or create a new one)
4. Add a description (e.g., "Lunch at restaurant")
5. Click **"Add Expense"** button
6. The expense is automatically saved and added to your list

### Viewing Expenses

1. Go to the **"View Expenses"** tab
2. Browse all your expenses in the table
3. Expenses are sorted by date (newest first)
4. Use scrollbars or mousewheel to navigate through long lists
5. Select an expense and click **"Delete Selected"** to remove it

### Generating Summary

1. Open the **"Summary"** tab
2. Click **"Generate Summary"** button
3. View:
   - Total spending amount
   - Spending breakdown by category
   - Percentage distribution
   - Visual pie chart (if matplotlib is installed)

### File Menu

- **Save** - Manually save your data (auto-save is enabled by default)
- **Load** - Reload data from file
- **Exit** - Close the application

## 📁 File Structure

```
projects/
│
├── budget_tracker.py      # Main application file
├── budget_data.json       # Data file (auto-generated)
├── requirements.md        # Detailed requirements documentation
└── README.md             # This file
```

## 🎨 Design Features

### Color Scheme
- **Primary Background**: Dark navy (#1A1F2E)
- **Secondary Background**: Slate gray (#2D3748)
- **Light Background**: Off-white (#F7FAFC)
- **Accent Color**: Blue (#4A90E2)
- **Success**: Green (#48BB78)
- **Danger**: Red (#F56565)

### Typography
- **Title**: Georgia (20pt, bold)
- **Headings**: Palatino Linotype (16pt, bold)
- **Body**: Segoe UI (9pt)
- **Buttons**: Segoe UI (10pt, bold)

## 💾 Data Storage

- All expense data is stored in `budget_data.json`
- Data is automatically saved when:
  - Adding a new expense
  - Deleting an expense
  - Manually saving via File menu
- The JSON file format is human-readable and can be edited manually if needed

### Data Structure
```json
{
    "expenses": [
        {
            "id": 1,
            "amount": 25.50,
            "category": "Food",
            "description": "Lunch at restaurant",
            "date": "2024-01-15"
        }
    ],
    "categories": ["Food", "Transport", "Entertainment", "Utilities", "Other"]
}
```

## 🔧 Troubleshooting

### Application won't start
- Ensure Python 3.6+ is installed
- Check that tkinter is available: `python -m tkinter`

### Charts not showing
- Install matplotlib: `pip install matplotlib`
- Restart the application after installation

### Data not saving
- Check file permissions in the project directory
- Ensure you have write access to the folder

### Fonts look different
- The application uses system fonts with fallbacks
- If specific fonts aren't available, it will use system defaults

## 🚧 Limitations

- Data is stored locally (no cloud sync)
- No budget limits or alerts
- No export to CSV/Excel (can be added)
- No multi-currency support
- No recurring expense tracking

## 🔮 Future Enhancements

Potential features for future versions:
- [ ] Budget limits and alerts
- [ ] Export to CSV/Excel
- [ ] Import from CSV
- [ ] Multi-currency support
- [ ] Recurring expenses
- [ ] Expense search and filtering
- [ ] Monthly/yearly reports
- [ ] Data backup and restore
- [ ] Dark/Light theme toggle


---

**Enjoy managing your budget! 💰📊**

