import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- Page Config ----------
st.set_page_config(page_title="Marketing Intelligence Dashboard", layout="wide")

# ---------- Custom CSS ----------
st.markdown("""
    <style>
        /* App background */
        .stApp { background-color: #1d2233; color: #fff; }

        /* Top header */
        [data-testid="stHeader"] { background-color: #232841; color:#fff; }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #232841 !important;
            color: #fff !important;
        }
        [data-testid="stSidebar"] * { color: #fff !important; }

        /* Headings */
        h1, h2, h3, h4, h5, h6 { color: #3fc1c9 !important; }

        /* Paragraph / text */
        p, span, label { color: #fff !important; }

        /* Metric cards */
        .stMetric-value, .stMetric-label { color:#fff; }

        /* Buttons */
        .stButton>button { background-color:#29335a; color:#fff; border-radius:8px; }

        /* Plotly charts background */
        .stPlotlyChart { background-color:#232841; border-radius:10px; }

        /* Inputs */
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>div>div { background-color:#2b3150; color:#fff; border-radius:5px; }
        .stCheckbox>div, .stRadio>div { color:#fff; }
        .stSlider>div>div>div>input { background-color:#2b3150; color:#fff; }
        .stFileUploader>div>div>div { background-color:#2b3150; color:#fff; }
    </style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Menu")
    pages = ["Dashboard", "Performance", "Funnel", "Campaigns", "States"]
    page = st.radio("Navigate", pages, index=0)
    st.markdown("---")
    st.caption("English")

# ---------- Load & Clean ----------
def load_and_clean(file, channel=None):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip().str.lower()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    if channel:
        df["channel"] = channel
    return df

# Load datasets
fb = load_and_clean("Facebook.csv", "Facebook")
google = load_and_clean("Google.csv", "Google")
tiktok = load_and_clean("TikTok.csv", "TikTok")
business = load_and_clean("business.csv")

# Rename for consistency
for df in [fb, google, tiktok]:
    df.rename(columns={"impression": "impressions", "attributed revenue": "attributed_revenue"}, inplace=True)

business.rename(columns={
    "# of orders": "orders", "# of new orders": "new_orders",
    "new customers": "new_customers", "total revenue": "total_revenue",
    "gross profit": "gross_profit", "cogs": "cogs"
}, inplace=True)

# Merge
marketing = pd.concat([fb, google, tiktok], ignore_index=True)
combined = pd.merge(marketing, business, on="date", how="inner")

# ---------- Aggregate Daily ----------
combined_daily = combined.groupby(["date", "channel", "state", "campaign"]).agg({
    "impressions": "sum", "clicks": "sum", "spend": "sum", "attributed_revenue": "sum",
    "orders": "sum", "new_orders": "sum", "new_customers": "sum",
    "total_revenue": "sum", "gross_profit": "sum"
}).reset_index()

# ---------- Filters ----------
col1, col2 = st.columns([3, 2])
with col1:
    min_date = combined_daily["date"].min()
    max_date = combined_daily["date"].max()
    date_range = st.date_input("Select date range:", [min_date, max_date], min_value=min_date, max_value=max_date)
with col2:
    channels = ["All"] + combined_daily["channel"].unique().tolist()
    selected_channel = st.selectbox("Select channel:", channels)

start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
filtered_data = combined_daily[(combined_daily["date"] >= start_date) & (combined_daily["date"] <= end_date)]
if selected_channel != "All":
    filtered_data = filtered_data[filtered_data["channel"] == selected_channel]

# ---------- Summary Datasets ----------
state_summary_marketing = filtered_data.groupby("state").agg({"impressions": "sum", "attributed_revenue": "sum"}).reset_index()
campaign_data = filtered_data.groupby(["campaign", "channel", "state"]).agg({"spend": "sum", "attributed_revenue": "sum"}).reset_index()

# ---------- KPI Cards ----------
def metric_card(title, value, color="#3fc1c9"):
    st.markdown(
        f"""
        <div style="
            background-color:#232841;
            padding:18px;
            border-radius:12px;
            text-align:center;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        ">
            <h4 style="color:#aaa; font-size:16px; margin-bottom:6px;">{title}</h4>
            <h2 style="color:{color}; font-size:22px; margin:0;">{value}</h2>
        </div>
        """, unsafe_allow_html=True
    )

# ---------- Page Routing ----------
if page == "Dashboard":
    st.title("Dashboard Overview")

    # KPI Rows
    row1 = st.columns(4)
    with row1[0]:
        metric_card("Total Spend", f"${filtered_data['spend'].sum():,.0f}")
    with row1[1]:
        metric_card("Total Revenue", f"${filtered_data['total_revenue'].sum():,.0f}", "#21bf73")
    with row1[2]:
        metric_card("Orders", f"{int(filtered_data['orders'].sum()):,}", "#21bf73")
    with row1[3]:
        metric_card("CTR", f"{(filtered_data['clicks'].sum() / filtered_data['impressions'].sum()):.2%}", "#ff9f43")

    row2 = st.columns(4)
    with row2[0]:
        metric_card("ROAS", f"{(filtered_data['attributed_revenue'].sum() / filtered_data['spend'].sum()):.2f}", "#21bf73")
    with row2[1]:
        metric_card("Avg CPC", f"${(filtered_data['spend'].sum() / filtered_data['clicks'].sum()):.2f}", "#ff6b6b")
    with row2[2]:
        metric_card("Avg Order Value", f"${(filtered_data['total_revenue'].sum() / filtered_data['orders'].sum()):.2f}")
    with row2[3]:
        metric_card("Profit Margin", f"{(filtered_data['gross_profit'].sum() / filtered_data['total_revenue'].sum()):.2%}", "#21bf73")


elif page == "Performance":
    st.title("Performance Trends")
    time_data = filtered_data.groupby("date").agg({"spend": "sum", "total_revenue": "sum"}).reset_index()
    fig = px.line(time_data, x="date", y=["spend", "total_revenue"], template="plotly_dark")
    fig.update_layout(plot_bgcolor="#232841", paper_bgcolor="#232841", font_color="#fff")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Funnel":
    st.title(" Marketing Funnel")
    funnel_data = pd.DataFrame({
        "stage": ["Impressions", "Clicks", "Orders", "Revenue ($)"],
        "value": [
            filtered_data["impressions"].sum(),
            filtered_data["clicks"].sum(),
            filtered_data["orders"].sum(),
            filtered_data["total_revenue"].sum()
        ]
    })
    fig3 = px.funnel(funnel_data, x="value", y="stage", template="plotly_dark")
    fig3.update_layout(plot_bgcolor="#232841", paper_bgcolor="#232841", font_color="#fff")
    st.plotly_chart(fig3, use_container_width=True)

elif page == "Campaigns":
    st.title(" Campaign Analysis")
    fig4 = px.scatter(campaign_data, x="spend", y="attributed_revenue",
                      color="channel", hover_data=["campaign", "state"], template="plotly_dark")
    fig4.update_layout(plot_bgcolor="#232841", paper_bgcolor="#232841", font_color="#fff")
    st.plotly_chart(fig4, use_container_width=True)

elif page == "States":
    st.title(" State Insights")
    colA, colB = st.columns(2)
    fig5 = px.bar(state_summary_marketing, x="state", y="impressions", color="state", template="plotly_dark")
    fig5.update_layout(plot_bgcolor="#232841", paper_bgcolor="#232841", font_color="#fff")
    fig6 = px.bar(state_summary_marketing, x="state", y="attributed_revenue", color="state", template="plotly_dark")
    fig6.update_layout(plot_bgcolor="#232841", paper_bgcolor="#232841", font_color="#fff")
    colA.plotly_chart(fig5, use_container_width=True)
    colB.plotly_chart(fig6, use_container_width=True)

# ---------- Footer ----------
st.markdown(
    "<hr style='border: 1px solid #29335a'><div style='text-align:center;color:#ccc;'>Marketing Intelligence Dashboard &copy; 2025</div>",
    unsafe_allow_html=True
)
