# 📊 Marketing Intelligence Dashboard

A **Streamlit-based Marketing Intelligence Dashboard** that integrates marketing data from **Facebook, Google, TikTok**, and business KPIs into one unified platform.  
It helps visualize spend, revenue, ROAS, funnel performance, and state-level insights in a clean dark-themed interface.
Link to website: https://ahkvqmjgbarzg7stqoyad.streamlit.app

---

## 🚀 Features

- 📈 **Performance Trends**: Spend vs Revenue over time  
- 🔻 **Marketing Funnel**: From impressions to revenue  
- 📌 **Campaign Analysis**: Spend vs Attributed Revenue per campaign  
- 🌍 **State Insights**: Compare impressions and revenue across states  
- 💰 **KPI Cards**: CTR, ROAS, Profit Margin, Avg CPC, AOV  
- 🎨 **Custom Dark Theme**: Modern BI-style visuals with teal highlights  
- 📂 **Sidebar Navigation**: Dashboard | Performance | Funnel | Campaigns | States | Settings  
- ⬇️ **Download Data**: Export filtered dataset as CSV  

---

## 🛠️ Tech Stack

- **Python 3.10+**
- [Streamlit](https://streamlit.io/) (Frontend UI)  
- [Pandas](https://pandas.pydata.org/) (Data processing)  
- [Plotly Express](https://plotly.com/python/plotly-express/) (Charts & Visualizations)  

---

## 📂 Project Structure

```
Marketing-Intelligence-Dashboard/
│── app.py               # Main Streamlit app
│── Facebook.csv         # Facebook ads data
│── Google.csv           # Google ads data
│── TikTok.csv           # TikTok ads data
│── business.csv         # Business KPIs
│── logo.png             # (Optional) Dashboard logo
│── README.md            # Documentation
```

---

## ⚙️ Installation

1. **Clone the repository** (or copy project files):
   ```bash
   git clone https://github.com/your-username/marketing-intelligence-dashboard.git
   cd marketing-intelligence-dashboard
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   *(If no requirements.txt exists, install manually)*:
   ```bash
   pip install streamlit pandas plotly
   ```

---

## ▶️ Usage

Run the app locally:

```bash
streamlit run app.py
```

The dashboard will be available at:  
👉 `http://localhost:8501`

---


## 🧑‍💻 Author

- **Your Name**  
- [LinkedIn](https://linkedin.com/) | [GitHub](https://github.com/)  

---

## 📜 License

This project is for **educational purposes** as part of a marketing analytics assignment.  
Not intended for commercial use.
