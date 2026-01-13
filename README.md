# 📊 Sales Analytics Dashboard

A comprehensive sales analytics dashboard built with Streamlit, featuring real-time KPI tracking, sales rep performance, customer analysis, product insights, and trend analysis.

## 🚀 Features

- **📊 Executive Overview**: KPIs, status distribution, recent activity
- **👔 Sales Rep Analysis**: Performance tracking, client status monitoring
- **⭐ Customer Insights**: Top customers, revenue analysis
- **📦 Product Intelligence**: SKU performance, quantity tracking
- **📈 Trends & Growth**: Monthly trends, growth metrics

## 🎯 Live Demo

[Your Streamlit App URL will be here]

## 📋 Prerequisites

- Python 3.8+
- Git account
- GitHub account
- Streamlit Cloud account (free)

## 🛠️ Local Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/sales-analytics-dashboard.git
cd sales-analytics-dashboard
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run Locally

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## ☁️ Deploy to Streamlit Cloud

### Step 1: Push to GitHub

1. Create a new repository on GitHub
2. Push your code:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/sales-analytics-dashboard.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `YOUR_USERNAME/sales-analytics-dashboard`
5. Set:
   - **Main file path**: `app.py`
   - **Branch**: `main`
6. Click "Deploy"

Your app will be live in 2-3 minutes! 🎉

## 📂 Project Structure

```
sales-analytics-dashboard/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .gitignore            # Git ignore file
```

## 📊 Data Format

### Sales Data (Required)
Upload CSV/Excel with these columns:
- ORDER DATE
- ORDER NUMBER
- CUSTOMER ID
- CUSTOMER NAME
- CITY
- SALE REPRESENTATIVE
- STATUS
- TOTAL VALUES
- TOTAL COMMISSION

### SKU/Product Data (Optional)
Upload CSV/Excel with these columns:
- Order ID
- Product Reference/SKU
- Product Name
- Quantity
- Unit Price
- Total

## 🎨 Features Overview

### Filters
- 📅 Date Range
- 👤 Sales Representatives
- 📊 Status (Paid, Pending, etc.)
- 🌍 Cities

### Analytics
- 💰 Revenue tracking
- 📦 Order volume
- 👥 Customer analysis
- 📈 Growth trends
- 🎯 Client status (Recent/Warm/Cold/Lost)
- 🏷️ Product performance

## 🔧 Customization

### Change Theme
Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#f8f9fa"
secondaryBackgroundColor = "#ffffff"
textColor = "#262730"
font = "sans serif"
```

### Modify KPIs
Edit the `calculate_metrics()` function in `app.py`

### Add New Charts
Add charts in the respective tab sections in `app.py`

## 🐛 Troubleshooting

### Issue: "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "Data not loading"
Check that your CSV/Excel columns match the expected format

### Issue: "App crashes on upload"
Ensure file size < 200MB for Streamlit Cloud

## 📝 License

MIT License - Feel free to use for personal or commercial projects

## 👤 Author

Your Name - [Your GitHub](https://github.com/YOUR_USERNAME)

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

## 📧 Support

For issues or questions, open a GitHub issue or contact: your.email@example.com

---

**Built with ❤️ using Streamlit & Plotly**
