# =============================================================================
# SALES ANALYTICS DASHBOARD – SAFE MODE (NO DATA / AUTO FILE DETECT)
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    layout="wide"
)

# -----------------------------------------------------------------------------
# PATHS
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# -----------------------------------------------------------------------------
# FILE FINDER (handles (3), (6), etc.)
# -----------------------------------------------------------------------------
def find_excel_file(keyword):
    for file in DATA_DIR.glob("*.xlsx"):
        if keyword.lower() in file.name.lower():
            return file
    return None

FILES = {
    "sales": find_excel_file("sales_analysis_results"),
    "sku": find_excel_file("sku_analysis"),
    "client": find_excel_file("client_status_analysis"),
    "advanced": find_excel_file("advanced_sales_insights"),
}

# -----------------------------------------------------------------------------
# SAFE DATA LOADER
# -----------------------------------------------------------------------------
@st.cache_data
def safe_load_excel(path):
    if path is None or not path.exists():
        return pd.DataFrame()

    try:
        df = pd.read_excel(path)
        if df.empty:
            return pd.DataFrame()
        df.columns = (
            df.columns.str.strip()
            .str.upper()
            .str.replace(" ", "_")
            .str.replace("-", "_")
        )
        return df
    except Exception:
        return pd.DataFrame()

# -----------------------------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------------------------
df_sales = safe_load_excel(FILES["sales"])
df_sku = safe_load_excel(FILES["sku"])
df_client = safe_load_excel(FILES["client"])
df_advanced = safe_load_excel(FILES["advanced"])

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
st.sidebar.title("📊 Navigation")
st.sidebar.info("Data source: GitHub (Colab extracts)")

section = st.sidebar.radio(
    "Select section",
    [
        "Overview",
        "Sales Performance",
        "SKU Analysis",
        "Client Status",
        "Advanced Insights",
    ]
)

# -----------------------------------------------------------------------------
# OVERVIEW
# -----------------------------------------------------------------------------
if section == "Overview":
    st.title("📈 Overview")

    if df_sales.empty:
        st.warning("No sales data available")
    else:
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Revenue", f"{df_sales.select_dtypes('number').sum().sum():,.0f}")
        col2.metric("Rows", len(df_sales))
        col3.metric("Active Clients", len(df_client) if not df_client.empty else 0)

# -----------------------------------------------------------------------------
# SALES PERFORMANCE
# -----------------------------------------------------------------------------
elif section == "Sales Performance":
    st.title("💰 Sales Performance")

    if df_sales.empty:
        st.warning("No sales data available")
    else:
        st.dataframe(df_sales, use_container_width=True)

        numeric_cols = df_sales.select_dtypes("number").columns
        if len(numeric_cols) >= 1:
            fig = px.line(
                df_sales,
                y=numeric_cols[0],
                title="Sales Trend"
            )
            st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# SKU ANALYSIS
# -----------------------------------------------------------------------------
elif section == "SKU Analysis":
    st.title("📦 SKU Analysis")

    if df_sku.empty:
        st.warning("No SKU data available")
    else:
        st.dataframe(df_sku, use_container_width=True)

# -----------------------------------------------------------------------------
# CLIENT STATUS
# -----------------------------------------------------------------------------
elif section == "Client Status":
    st.title("👥 Client Status")

    if df_client.empty:
        st.warning("No client status data available")
    else:
        st.dataframe(df_client, use_container_width=True)

        if "CLIENT_STATUS" in df_client.columns:
            fig = px.pie(
                df_client,
                names="CLIENT_STATUS",
                title="Client Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# ADVANCED INSIGHTS
# -----------------------------------------------------------------------------
elif section == "Advanced Insights":
    st.title("🚀 Advanced Insights")

    if df_advanced.empty:
        st.warning("No advanced insights data available")
    else:
        st.dataframe(df_advanced, use_container_width=True)

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption("Read-only dashboard • Safe mode enabled • No data = no crash")
