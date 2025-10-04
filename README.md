# Portfolio Analyzer

-----

## 📊 Overview

The **Portfolio Analyzer** is a simple, lightweight web application built with **Python** and **Flask** for analyzing stock price history. It allows users to upload a CSV file containing their portfolio data, automatically calculate key statistics for each stock (like volatility and price change), and generate interactive line plots to visualize price trends over time.

This project is ideal for local, quick data analysis without the need for external financial APIs.

-----

## ✨ Features

  * **CSV Upload Interface:** A dedicated page (`/upload`) to easily submit portfolio data.
  * **Intelligent Data Mapping:** The application automatically detects common column names like `Symbol`, `Ticker`, `Close`, and `Value`, and maps them to **Stock**, **Date**, and **Price**.
  * **Comprehensive Summary:**
      * **Top-level metrics** (Total records, unique stocks, overall average price).
      * **Per-stock Analysis** table, including Min/Max/Average Price, Volatility (Standard Deviation), and Total Price Change.
  * **Interactive Visualization:** A dedicated page (`/plots`) to select a stock and view its price trend visualized as an embedded Matplotlib chart.
  * **Sample Data:** Includes a `sample_portfolio.csv` file for testing the application immediately after setup.

-----

## 💻 Getting Started

### Prerequisites

You need **Python 3.x** installed on your system.

### Installation

1.  **Clone the Repository** (or download and unzip the file):

    ```bash
    git clone https://github.com/YourUsername/Portfolio-Analyzer.git
    cd Portfolio-Analyzer
    ```

2.  **Create a Virtual Environment** (Highly Recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**

    Install the required Python libraries using `pip`:

    ```bash
    pip install Flask pandas matplotlib
    ```

-----

## 🚀 Running the Application

1.  Ensure you are in the main project directory (`Portfolio-Analyzer/`).

2.  Run the Flask application from your terminal:

    ```bash
    python app.py
    ```

3.  Open your web browser and navigate to the address shown in the terminal. By default, this is:

    ```
    http://127.0.0.1:5000/
    ```

-----

## 📁 Project Structure

The repository has the following structure:

```
Portfolio Analyzer/
├── app.py                      # Main Flask application logic and data processing
├── sample_portfolio.csv        # Example CSV file for testing
├── templates/                  # HTML templates for the web interface
│   ├── base.html               # Base layout with navigation (uses Bootstrap CDN)
│   ├── error.html              # Template for displaying errors
│   ├── plots.html              # Stock selection and chart visualization page
│   ├── summary.html            # Portfolio summary and statistics page
│   └── upload.html             # CSV upload form page
└── uploads/                    # Directory for temporary storage of uploaded files
    └── uploaded_portfolio.csv
```

-----

## 📋 Data Format

The application requires a CSV file with at least three columns for Stock, Date, and Price.

| Data Field | Primary Name | Auto-Detected Alternatives | Expected Format |
| :--- | :--- | :--- | :--- |
| **Stock** | `Stock` | `Symbol`, `Ticker`, `Stock Name` | Text |
| **Date** | `Date` | `Date` | YYYY-MM-DD or standard formats |
| **Price** | `Price` | `Close`, `Value` | Numeric |

### `sample_portfolio.csv` Example:

```csv
Stock,Date,Price
Reliance,2024-01-01,2500.00
Reliance,2024-01-10,2520.50
HDFC,2024-01-01,1600.25
HDFC,2024-01-10,1610.75
# ... and so on
```
