# =============================================================================
# SALES ANALYTICS DASHBOARD – READ ONLY (COLAB EXTRACTS)
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
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CONSTANTS & PATHS
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

FILES = {
    "sales": DATA_DIR / "Sales_Analysis_Results.xlsx",
    "sku": DATA_DIR / "SKU_Analysis.xlsx",
    "client": DATA_DIR / "Client_Status_Analysis.xlsx",
    "advanced": DATA_DIR / "Advanced_Sales_Insights.xlsx",
}

# -----------------------------------------------------------------------------
# UTILITY FUNCTIONS
# -----------------------------------------------------------------------------
@st.cache_data
def load_excel(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        st.error(f"❌ Missing file: {label} → `{path.name}`")
        st.stop()
    return pd.read_excel(path)


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.upper()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


# -----------------------------------------------------------------------------
# LOAD DATA (FROM COLAB EXPORTS)
# -----------------------------------------------------------------------------
df_sales = clean_columns(load_excel(FILES["sales"], "Sales Analysis Results"))
df_sku = clean_columns(load_excel(FILES["sku"], "SKU Analysis"))
df_client = clean_columns(load_excel(FILES["client"], "Client Status Analysis"))
df_advanced = clean_columns(load_excel(FILES["advanced"], "Advanced Sales Insights"))

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
st.sidebar.title("📊 Dashboard Controls")
st.sidebar.success("Data source: Colab extracts (GitHub)")

section = st.sidebar.radio(
    "Go to section",
    [
        "Overview",
        "Sales Performance",
        "SKU Analysis",
        "Client Status",
        "Advanced Insights",
    ],
)

# -----------------------------------------------------------------------------
# OVERVIEW
# -----------------------------------------------------------------------------
if section == "Overview":
    st.title("📈 Sales Analytics Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Revenue",
        f"{df_sales['TOTAL_REVENUE'].sum():,.0f}"
    )

    col2.metric(
        "Total Orders",
        f"{df_sales['TOTAL_ORDERS'].sum():,.0f}"
    )

    col3.metric(
        "Active Clients",
        df_client.shape[0]
    )

    st.subheader("Revenue by Region")
    fig = px.bar(
        df_sales,
        x="REGION",
        y="TOTAL_REVENUE",
        title="Revenue per Region",
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# SALES PERFORMANCE
# -----------------------------------------------------------------------------
elif section == "Sales Performance":
    st.title("💰 Sales Performance")

    st.dataframe(df_sales, use_container_width=True)

    fig = px.line(
        df_sales,
        x="DATE",
        y="TOTAL_REVENUE",
        color="REGION",
        title="Revenue Trend",
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# SKU ANALYSIS
# -----------------------------------------------------------------------------
elif section == "SKU Analysis":
    st.title("📦 SKU Analysis")

    st.dataframe(df_sku, use_container_width=True)

    fig = px.bar(
        df_sku,
        x="SKU",
        y="SALES_VALUE",
        title="Top SKU by Sales Value",
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# CLIENT STATUS
# -----------------------------------------------------------------------------
elif section == "Client Status":
    st.title("👥 Client Status Analysis")

    st.dataframe(df_client, use_container_width=True)

    fig = px.pie(
        df_client,
        names="CLIENT_STATUS",
        title="Client Distribution",
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# ADVANCED INSIGHTS
# -----------------------------------------------------------------------------
elif section == "Advanced Insights":
    st.title("🚀 Advanced Sales Insights")

    st.dataframe(df_advanced, use_container_width=True)

    if "INSIGHT_TYPE" in df_advanced.columns:
        fig = px.bar(
            df_advanced,
            x="INSIGHT_TYPE",
            y="VALUE",
            title="Advanced Metrics",
        )
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption("📌 Powered by Colab analytics • Streamlit dashboard (Read-Only)")
