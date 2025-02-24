# Data Processing Application with Flask and Pandas

This application processes and analyzes data from two distinct sources: **Store Data** and **Shift Work Data**. It is designed for environments where direct database access is unavailable, and data is exported from another application as files. The application uses **Flask** for the web framework and **Pandas** for data manipulation and analysis.

---

## Features

- **Data Integration**: Loads and processes data from two separate files (store data and shift work data).
- **Data Analysis**: Uses Pandas to filter, merge, and aggregate data for meaningful insights.
- **Web Interface**: Provides a user-friendly interface built with Flask for uploading files, viewing processed data, and accessing reports.
- **Flexibility**: Handles exported data files (e.g., CSV, Excel) in environments where direct database access is restricted.

---

## Technology Stack

- **Flask**: A lightweight Python web framework for building the backend and serving the frontend.
- **Pandas**: A powerful Python library for data manipulation and analysis.
- **File Handling**: Supports loading data from CSV, Excel, or other file formats.

---

## Workflow

1. **Data Upload**: Users upload store data (inventory) and shift work data (tasks completed during the shift) via the Flask web interface.
2. **Data Processing**: The application reads the files using Pandas, performs necessary transformations, and merges the datasets as required.
3. **Insights Generation**: Analyzes the processed data to generate reports or summaries, such as:
   - Current inventory status.
   - Tasks completed vs. pending.
   - Efficiency metrics for the shift.
4. **Output**: Displays results in the web interface or exports them for further use.

---

## Use Case Example

A store manager uploads:
- **Store Data**: Inventory levels.
- **Shift Work Data**: Tasks completed during the shift.

The application processes the data to provide insights such as:
- Current inventory status.
- Tasks completed vs. pending.
- Efficiency metrics for the shift.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name