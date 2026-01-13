# ============================================================================
# COMPLETE SALES ANALYTICS DASHBOARD - STREAMLIT APP
# Save this file as: app.py
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")


# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stMetric {background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
    .css-1d391kg {padding-top: 2rem;}
    h1 {color: #667eea;}
    h2 {color: #3498db;}
    h3 {color: #2ecc71;}
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_data
def load_sales_data(file):
    """Load and clean main sales data"""
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    
    # Standardize columns
    df.columns = df.columns.str.strip().str.upper().str.replace(' ', '_')
    
    # Convert date
    date_cols = ['ORDER_DATE', 'DATE', 'CREATION_DATE']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            df['ORDER_DATE'] = df[col]
            break
    
    # Convert numeric
    numeric_cols = ['TOTAL_ITEM', 'TOTAL_VALUES', 'TOTAL_COMMISSION']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Add time dimensions
    if 'ORDER_DATE' in df.columns:
        df['YEAR_MONTH'] = df['ORDER_DATE'].dt.to_period('M').astype(str)
        df['YEAR'] = df['ORDER_DATE'].dt.year
        df['MONTH'] = df['ORDER_DATE'].dt.month
        df['QUARTER'] = df['ORDER_DATE'].dt.quarter
    
    return df

@st.cache_data
def load_sku_data(file):
    """Load and clean SKU/product data"""
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    
    df.columns = df.columns.str.strip().str.upper()
    
    # Smart column mapping
    column_mapping = {
        'MATRIX_ORDER_ID': 'ORDER_ID',
        'CREATION_DATE': 'ORDER_DATE',
        'ORDER_LINES/PRODUCT/REFERENCE': 'SKU',
        'ORDER_LINES/PRODUCT/NAME': 'PRODUCT_NAME',
        'ORDER_LINES/QUANTITY': 'QUANTITY',
        'ORDER_LINES/UNIT_PRICE': 'UNIT_PRICE',
        'ORDER_LINES/TOTAL': 'LINE_TOTAL',
    }
    
    for old, new in column_mapping.items():
        if old in df.columns:
            df.rename(columns={old: new}, inplace=True)
    
    # Convert numeric
    for col in ['QUANTITY', 'UNIT_PRICE', 'LINE_TOTAL']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Calculate total if missing
    if 'LINE_TOTAL' in df.columns and df['LINE_TOTAL'].sum() == 0:
        if 'QUANTITY' in df.columns and 'UNIT_PRICE' in df.columns:
            df['LINE_TOTAL'] = df['QUANTITY'] * df['UNIT_PRICE']
    
    # Dates
    if 'ORDER_DATE' in df.columns:
        df['ORDER_DATE'] = pd.to_datetime(df['ORDER_DATE'], errors='coerce')
        df['YEAR_MONTH'] = df['ORDER_DATE'].dt.to_period('M').astype(str)
    
    return df

def calculate_metrics(df):
    """Calculate key metrics"""
    metrics = {
        'total_revenue': df['TOTAL_VALUES'].sum() if 'TOTAL_VALUES' in df.columns else 0,
        'total_orders': len(df),
        'total_commission': df['TOTAL_COMMISSION'].sum() if 'TOTAL_COMMISSION' in df.columns else 0,
        'unique_customers': df['CUSTOMER_ID'].nunique() if 'CUSTOMER_ID' in df.columns else 0,
        'avg_order_value': df['TOTAL_VALUES'].mean() if 'TOTAL_VALUES' in df.columns else 0,
        'unique_reps': df['SALE_REPRESENTATIVE'].nunique() if 'SALE_REPRESENTATIVE' in df.columns else 0
    }
    return metrics

def create_kpi_cards(metrics):
    """Display KPI metrics in cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Revenue", f"${metrics['total_revenue']:,.2f}")
    with col2:
        st.metric("📦 Total Orders", f"{metrics['total_orders']:,}")
    with col3:
        st.metric("👥 Unique Customers", f"{metrics['unique_customers']:,}")
    with col4:
        st.metric("📊 Avg Order Value", f"${metrics['avg_order_value']:,.2f}")

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Header
    st.title("📊 Sales Analytics Dashboard")
    st.markdown("### Comprehensive Sales Intelligence System")
    
    # Sidebar
    st.sidebar.header("📁 Data Upload")
    
    sales_file = st.sidebar.file_uploader(
        "Upload Sales Data (Main Orders)",
        type=['csv', 'xlsx'],
        help="Upload your main sales/orders file"
    )
    
    sku_file = st.sidebar.file_uploader(
        "Upload SKU/Product Data (Optional)",
        type=['csv', 'xlsx'],
        help="Upload your order lines/SKU file"
    )
    
    if not sales_file:
        st.info("👈 Please upload your sales data file to begin")
        st.markdown("""
        ### Expected Columns for Sales Data:
        - ORDER DATE
        - ORDER NUMBER
        - CUSTOMER ID / CUSTOMER NAME
        - SALE REPRESENTATIVE
        - STATUS
        - TOTAL VALUES
        - TOTAL COMMISSION
        
        ### Expected Columns for SKU Data (Optional):
        - Order ID
        - Product Reference / SKU
        - Product Name
        - Quantity
        - Unit Price
        - Total
        """)
        return
    
    # Load data
    with st.spinner("Loading data..."):
        df_sales = load_sales_data(sales_file)
        df_sku = load_sku_data(sku_file) if sku_file else None
    
    st.success(f"✅ Loaded {len(df_sales):,} sales records")
    if df_sku is not None:
        st.success(f"✅ Loaded {len(df_sku):,} product lines")
    
    # Sidebar Filters
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filters")
    
    # Date filter
    if 'ORDER_DATE' in df_sales.columns:
        min_date = df_sales['ORDER_DATE'].min().date()
        max_date = df_sales['ORDER_DATE'].max().date()
        date_range = st.sidebar.date_input(
            "📅 Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            df_sales = df_sales[
                (df_sales['ORDER_DATE'].dt.date >= date_range[0]) &
                (df_sales['ORDER_DATE'].dt.date <= date_range[1])
            ]
    
    # Sales Rep filter
    if 'SALE_REPRESENTATIVE' in df_sales.columns:
        all_reps = ['All'] + sorted(df_sales['SALE_REPRESENTATIVE'].dropna().unique().tolist())
        selected_reps = st.sidebar.multiselect(
            "👤 Sales Representatives",
            options=all_reps,
            default=['All']
        )
        
        if 'All' not in selected_reps:
            df_sales = df_sales[df_sales['SALE_REPRESENTATIVE'].isin(selected_reps)]
    
    # Status filter
    if 'STATUS' in df_sales.columns:
        all_status = ['All'] + sorted(df_sales['STATUS'].dropna().unique().tolist())
        selected_status = st.sidebar.multiselect(
            "📊 Status",
            options=all_status,
            default=['All']
        )
        
        if 'All' not in selected_status:
            df_sales = df_sales[df_sales['STATUS'].isin(selected_status)]
    
    # City filter
    if 'CITY' in df_sales.columns:
        all_cities = ['All'] + sorted(df_sales['CITY'].dropna().unique().tolist())
        selected_cities = st.sidebar.multiselect(
            "🌍 Cities",
            options=all_cities,
            default=['All']
        )
        
        if 'All' not in selected_cities:
            df_sales = df_sales[df_sales['CITY'].isin(selected_cities)]
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "👔 Sales Reps",
        "⭐ Customers",
        "📦 Products (SKU)",
        "📈 Trends"
    ])
    
    # ========================================================================
    # TAB 1: OVERVIEW
    # ========================================================================
    with tab1:
        st.header("📊 Executive Overview")
        
        # KPI Cards
        metrics = calculate_metrics(df_sales)
        create_kpi_cards(metrics)
        
        st.markdown("---")
        
        # Additional metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💵 Total Commission", f"${metrics['total_commission']:,.2f}")
        with col2:
            commission_rate = (metrics['total_commission'] / metrics['total_revenue'] * 100) if metrics['total_revenue'] > 0 else 0
            st.metric("📊 Commission Rate", f"{commission_rate:.2f}%")
        with col3:
            st.metric("👔 Active Reps", f"{metrics['unique_reps']:,}")
        with col4:
            if 'CITY' in df_sales.columns:
                st.metric("🌍 Cities", f"{df_sales['CITY'].nunique():,}")
        
        st.markdown("---")
        
        # Status breakdown
        if 'STATUS' in df_sales.columns:
            st.subheader("📋 Order Status Distribution")
            status_data = df_sales['STATUS'].value_counts().reset_index()
            status_data.columns = ['Status', 'Count']
            
            fig = px.pie(
                status_data,
                values='Count',
                names='Status',
                title='Orders by Status',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent activity
        st.subheader("📅 Recent Orders")
        recent_cols = ['ORDER_DATE', 'CUSTOMER_NAME', 'SALE_REPRESENTATIVE', 
                      'STATUS', 'TOTAL_VALUES']
        available_cols = [col for col in recent_cols if col in df_sales.columns]
        st.dataframe(df_sales[available_cols].head(20), use_container_width=True)
    
    # ========================================================================
    # TAB 2: SALES REPS
    # ========================================================================
    with tab2:
        st.header("👔 Sales Representative Performance")
        
        if 'SALE_REPRESENTATIVE' in df_sales.columns:
            # Top N selector
            top_n = st.slider("Show Top N Reps", 5, 50, 10, 5)
            
            # Rep performance
            rep_perf = df_sales.groupby('SALE_REPRESENTATIVE').agg({
                'TOTAL_VALUES': 'sum',
                'ORDER_NUMBER': 'count',
                'CUSTOMER_ID': 'nunique',
                'TOTAL_COMMISSION': 'sum'
            }).sort_values('TOTAL_VALUES', ascending=False).head(top_n).reset_index()
            
            rep_perf.columns = ['Sales_Rep', 'Revenue', 'Orders', 'Customers', 'Commission']
            
            # Chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=rep_perf['Sales_Rep'],
                y=rep_perf['Revenue'],
                marker_color='#3498db',
                text=rep_perf['Revenue'].apply(lambda x: f'${x:,.0f}'),
                textposition='outside'
            ))
            fig.update_layout(
                title=f'Top {top_n} Sales Reps by Revenue',
                xaxis_title='Sales Representative',
                yaxis_title='Revenue ($)',
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Data table
            st.subheader("📊 Detailed Performance")
            st.dataframe(
                rep_perf.style.format({
                    'Revenue': '${:,.2f}',
                    'Orders': '{:,}',
                    'Customers': '{:,}',
                    'Commission': '${:,.2f}'
                }),
                use_container_width=True
            )
            
            # Client Status Analysis
            st.markdown("---")
            st.subheader("🎯 Client Status Analysis")
            
            if 'ORDER_DATE' in df_sales.columns:
                max_date = df_sales['ORDER_DATE'].max()
                
                customer_last = df_sales.groupby(['CUSTOMER_ID', 'SALE_REPRESENTATIVE']).agg({
                    'ORDER_DATE': 'max',
                    'CUSTOMER_NAME': 'first'
                }).reset_index()
                
                customer_last['Days_Since'] = (max_date - customer_last['ORDER_DATE']).dt.days
                
                def assign_status(days):
                    if days < 30: return '🟢 Recent'
                    elif days < 90: return '🟡 Warm'
                    elif days < 180: return '🟠 Cold'
                    else: return '🔴 Lost'
                
                customer_last['Status'] = customer_last['Days_Since'].apply(assign_status)
                
                status_summary = customer_last.groupby(['SALE_REPRESENTATIVE', 'Status']).size().reset_index(name='Count')
                
                fig = px.bar(
                    status_summary,
                    x='SALE_REPRESENTATIVE',
                    y='Count',
                    color='Status',
                    title='Client Status by Sales Rep',
                    color_discrete_map={
                        '🟢 Recent': '#27ae60',
                        '🟡 Warm': '#f39c12',
                        '🟠 Cold': '#e67e22',
                        '🔴 Lost': '#e74c3c'
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # TAB 3: CUSTOMERS
    # ========================================================================
    with tab3:
        st.header("⭐ Customer Analysis")
        
        if 'CUSTOMER_ID' in df_sales.columns:
            top_n_cust = st.slider("Show Top N Customers", 5, 50, 10, 5, key='cust_slider')
            
            cust_perf = df_sales.groupby(['CUSTOMER_ID', 'CUSTOMER_NAME']).agg({
                'TOTAL_VALUES': 'sum',
                'ORDER_NUMBER': 'count',
                'CITY': 'first'
            }).sort_values('TOTAL_VALUES', ascending=False).head(top_n_cust).reset_index()
            
            cust_perf.columns = ['Customer_ID', 'Customer_Name', 'Revenue', 'Orders', 'City']
            
            # Chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=cust_perf['Customer_Name'],
                y=cust_perf['Revenue'],
                marker_color='#e67e22',
                text=cust_perf['Revenue'].apply(lambda x: f'${x:,.0f}'),
                textposition='outside'
            ))
            fig.update_layout(
                title=f'Top {top_n_cust} Customers by Revenue',
                xaxis_title='Customer',
                yaxis_title='Revenue ($)',
                height=500,
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Customer table
            st.subheader("📊 Customer Details")
            st.dataframe(
                cust_perf.style.format({
                    'Revenue': '${:,.2f}',
                    'Orders': '{:,}'
                }),
                use_container_width=True
            )
    
    # ========================================================================
    # TAB 4: PRODUCTS (SKU)
    # ========================================================================
    with tab4:
        st.header("📦 Product & SKU Analysis")
        
        if df_sku is not None:
            # Overall metrics
            total_sku_revenue = df_sku['LINE_TOTAL'].sum() if 'LINE_TOTAL' in df_sku.columns else 0
            total_qty = df_sku['QUANTITY'].sum() if 'QUANTITY' in df_sku.columns else 0
            unique_skus = df_sku['SKU'].nunique() if 'SKU' in df_sku.columns else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 Total Revenue", f"${total_sku_revenue:,.2f}")
            with col2:
                st.metric("📦 Units Sold", f"{total_qty:,.0f}")
            with col3:
                st.metric("🏷️ Unique SKUs", f"{unique_skus:,}")
            
            st.markdown("---")
            
            if 'SKU' in df_sku.columns:
                top_n_sku = st.slider("Show Top N Products", 5, 30, 15, 5, key='sku_slider')
                
                # Product performance
                sku_cols = ['SKU']
                if 'PRODUCT_NAME' in df_sku.columns:
                    sku_cols.append('PRODUCT_NAME')
                
                sku_perf = df_sku.groupby(sku_cols).agg({
                    'QUANTITY': 'sum',
                    'LINE_TOTAL': 'sum',
                    'UNIT_PRICE': 'mean'
                }).sort_values('LINE_TOTAL', ascending=False).head(top_n_sku).reset_index()
                
                display_name = 'PRODUCT_NAME' if 'PRODUCT_NAME' in sku_perf.columns else 'SKU'
                
                # Revenue chart
                fig1 = go.Figure()
                fig1.add_trace(go.Bar(
                    x=sku_perf[display_name],
                    y=sku_perf['LINE_TOTAL'],
                    marker_color='#3498db',
                    text=sku_perf['LINE_TOTAL'].apply(lambda x: f'${x:,.0f}'),
                    textposition='outside'
                ))
                fig1.update_layout(
                    title=f'Top {top_n_sku} Products by Revenue',
                    xaxis_title='Product',
                    yaxis_title='Revenue ($)',
                    height=500,
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig1, use_container_width=True)
                
                # Quantity chart
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(
                    x=sku_perf[display_name],
                    y=sku_perf['QUANTITY'],
                    marker_color='#2ecc71',
                    text=sku_perf['QUANTITY'].apply(lambda x: f'{x:,.0f}'),
                    textposition='outside'
                ))
                fig2.update_layout(
                    title=f'Top {top_n_sku} Products by Quantity',
                    xaxis_title='Product',
                    yaxis_title='Units Sold',
                    height=500,
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig2, use_container_width=True)
                
                # Data table
                st.subheader("📊 Product Performance Details")
                st.dataframe(
                    sku_perf.style.format({
                        'QUANTITY': '{:,.0f}',
                        'LINE_TOTAL': '${:,.2f}',
                        'UNIT_PRICE': '${:,.2f}'
                    }),
                    use_container_width=True
                )
        else:
            st.info("📦 Upload SKU/Product data to view product analysis")
    
    # ========================================================================
    # TAB 5: TRENDS
    # ========================================================================
    with tab5:
        st.header("📈 Sales Trends")
        
        if 'YEAR_MONTH' in df_sales.columns:
            monthly = df_sales.groupby('YEAR_MONTH').agg({
                'TOTAL_VALUES': 'sum',
                'ORDER_NUMBER': 'count'
            }).reset_index()
            
            monthly.columns = ['Month', 'Revenue', 'Orders']
            
            # Revenue trend
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=monthly['Month'],
                y=monthly['Revenue'],
                mode='lines+markers',
                line=dict(color='#3498db', width=3),
                fill='tozeroy',
                name='Revenue'
            ))
            fig1.update_layout(
                title='Monthly Revenue Trend',
                xaxis_title='Month',
                yaxis_title='Revenue ($)',
                height=500
            )
            st.plotly_chart(fig1, use_container_width=True)
            
            # Orders trend
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=monthly['Month'],
                y=monthly['Orders'],
                marker_color='#2ecc71'
            ))
            fig2.update_layout(
                title='Monthly Order Volume',
                xaxis_title='Month',
                yaxis_title='Number of Orders',
                height=500
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            # Growth metrics
            if len(monthly) > 1:
                monthly['Revenue_Growth'] = monthly['Revenue'].pct_change() * 100
                avg_growth = monthly['Revenue_Growth'].mean()
                
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📈 Avg Monthly Growth", f"{avg_growth:.2f}%")
                with col2:
                    st.metric("💰 Best Month", f"${monthly['Revenue'].max():,.2f}")
                with col3:
                    best_month = monthly.loc[monthly['Revenue'].idxmax(), 'Month']
                    st.metric("📅 Peak Month", best_month)

# ============================================================================
# FOOTER
# ============================================================================
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Sales Analytics Dashboard")
    st.sidebar.markdown("Built with Streamlit & Plotly")
    st.sidebar.markdown("Version 1.0")

if __name__ == "__main__":
    main()
