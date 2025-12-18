# Budget Tracker - Requirements

## Python Version
- **Python 3.6+** (Recommended: Python 3.8 or higher)

## Built-in Modules (No Installation Required)
The following modules come with Python and do not need to be installed:
- `tkinter` - GUI framework
- `json` - JSON data handling
- `os` - Operating system interface
- `datetime` - Date and time handling

## Optional Dependencies

### For Enhanced Features
These packages are optional but recommended for full functionality:

#### 1. Matplotlib
**Purpose:** Generate pie charts and visualizations in the Summary tab

**Installation:**
```bash
pip install matplotlib
```

**Version:** 3.0.0 or higher recommended

#### 2. Pandas
**Purpose:** Enhanced data processing and analysis for expense summaries

**Installation:**
```bash
pip install pandas
```

**Version:** 1.0.0 or higher recommended

## Installation Instructions

### Quick Install (All Optional Dependencies)
```bash
pip install matplotlib pandas
```

### Using requirements.txt (Alternative)
If you prefer using a requirements.txt file, create one with:
```
matplotlib>=3.0.0
pandas>=1.0.0
```

Then install with:
```bash
pip install -r requirements.txt
```

## Notes
- The application will work without matplotlib and pandas, but some features will be limited:
  - **Without matplotlib:** Charts will not be displayed in the Summary tab
  - **Without pandas:** Summary calculations will use basic Python methods (still functional)

## System Requirements
- **Operating System:** Windows, macOS, or Linux
- **Display:** Minimum 1024x768 resolution recommended
- **Storage:** Minimal (application and data files are lightweight)

## Running the Application
```bash
python budget_tracker.py
```

Or on some systems:
```bash
python3 budget_tracker.py
```

