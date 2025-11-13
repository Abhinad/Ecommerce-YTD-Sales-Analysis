"""Visualization Functions for YTD Sales Analysis

Provides comprehensive visualization functions for e-commerce sales analysis including:
- Scatter plots with conditional coloring (red/green for negative/positive)
- Time series line charts
- Seasonal decomposition
- Heatmaps for month-over-month comparison
- Bar charts for YTD vs PYTD vs P1YTD comparison
""\

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)


def plot_ytd_scatter_with_delta(metrics_df, save_path=None):
    """
    Create scatter plot with YTD on X-axis, Delta on Y-axis.
    Negative deltas in RED, Positive deltas in GREEN.
    Bubble size represents absolute delta value.
    
    Args:
        metrics_df: DataFrame with ytd_sales, delta_ytd_pytd, product_name
        save_path: Optional path to save the figure
    """
    df = metrics_df.copy()
    
    # Create color column based on delta
    df['color'] = df['delta_ytd_pytd'].apply(lambda x: 'red' if x < 0 else 'green')
    df['size'] = df['abs_delta_ytd_pytd']
    
    # Create figure
    fig = go.Figure()
    
    # Add traces for negative (red) and positive (green) separately
    for color_val, color_name in [('red', 'Declining'), ('green', 'Growing')]:
        df_subset = df[df['color'] == color_val]
        
        fig.add_trace(go.Scatter(
            x=df_subset['ytd_sales'],
            y=df_subset['delta_ytd_pytd'],
            mode='markers+text',
            name=color_name,
            marker=dict(
                size=df_subset['size'] / 100000,  # Scale for visibility
                color=color_val,
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            text=df_subset['product_name'],
            textposition='top center',
            textfont=dict(size=9),
            hovertemplate='<b>%{text}</b><br>' +
                         'YTD Sales: ₹%{x:,.0f}<br>' +
                         'Delta: ₹%{y:,.0f}<br>' +
                         '<extra></extra>'
        ))
    
    # Add zero line
    fig.add_hline(y=0, line_dash='dash', line_color='black', opacity=0.5)
    
    fig.update_layout(
        title='YTD Sales vs Delta (YTD - PYTD)<br><sub>Bubble size = Absolute Delta | Red = Declining | Green = Growing</sub>',
        xaxis_title='YTD Sales (₹)',
        yaxis_title='Delta: YTD - PYTD (₹)',
        height=600,
        showlegend=True,
        hovermode='closest',
        font=dict(size=12)
    )
    
    if save_path:
        fig.write_html(save_path)
    
    fig.show()
    return fig


def plot_ytd_comparison_bars(metrics_df, save_path=None):
    """
    Create grouped bar chart comparing YTD, PYTD, and P1YTD for each product.
    
    Args:
        metrics_df: DataFrame with ytd_sales, pytd_sales, p1ytd_sales
        save_path: Optional path to save figure
    """
    df = metrics_df.copy()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='YTD (Current)',
        x=df['product_name'],
        y=df['ytd_sales'],
        marker_color='#2E86AB'
    ))
    
    fig.add_trace(go.Bar(
        name='PYTD (Previous Year)',
        x=df['product_name'],
        y=df['pytd_sales'],
        marker_color='#A23B72'
    ))
    
    fig.add_trace(go.Bar(
        name='P1YTD (2 Years Ago)',
        x=df['product_name'],
        y=df['p1ytd_sales'],
        marker_color='#F18F01'
    ))
    
    fig.update_layout(
        title='YTD vs PYTD vs P1YTD Sales Comparison by Product',
        xaxis_title='Product',
        yaxis_title='Sales Amount (₹)',
        barmode='group',
        height=500,
        showlegend=True,
        hovermode='x unified'
    )
    
    if save_path:
        fig.write_html(save_path)
    
    fig.show()
    return fig


def plot_time_series_by_product(monthly_df, products=None, save_path=None):
    """
    Plot time series of monthly sales for selected products.
    
    Args:
        monthly_df: DataFrame with year_month, product_name, sales_amount
        products: List of products to plot (None = all)
        save_path: Optional save path
    """
    df = monthly_df.copy()
    
    if products:
        df = df[df['product_name'].isin(products)]
    
    fig = px.line(
        df,
        x='year_month',
        y='sales_amount',
        color='product_name',
        title='Monthly Sales Trends by Product',
        labels={'year_month': 'Month', 'sales_amount': 'Sales (₹)', 'product_name': 'Product'},
        markers=True
    )
    
    fig.update_layout(
        height=600,
        hovermode='x unified',
        xaxis=dict(tickangle=-45)
    )
    
    if save_path:
        fig.write_html(save_path)
    
    fig.show()
    return fig


def plot_seasonal_decomposition(sales_series, period=12, save_path=None):
    """
    Create seasonal decomposition plot.
    
    Args:
        sales_series: Time series of sales data
        period: Seasonality period (default 12 for monthly)
        save_path: Optional save path
    """
    # Perform seasonal decomposition
    decomposition = seasonal_decompose(sales_series, model='additive', period=period)
    
    # Create subplots
    fig, axes = plt.subplots(4, 1, figsize=(14, 10))
    
    # Original
    decomposition.observed.plot(ax=axes[0], color='blue')
    axes[0].set_ylabel('Observed')
    axes[0].set_title('Seasonal Decomposition of Sales Data')
    
    # Trend
    decomposition.trend.plot(ax=axes[1], color='orange')
    axes[1].set_ylabel('Trend')
    
    # Seasonal
    decomposition.seasonal.plot(ax=axes[2], color='green')
    axes[2].set_ylabel('Seasonal')
    
    # Residual
    decomposition.resid.plot(ax=axes[3], color='red')
    axes[3].set_ylabel('Residual')
    axes[3].set_xlabel('Date')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
    return fig


def plot_heatmap_monthly_sales(monthly_df, save_path=None):
    """
    Create heatmap showing sales by month and product.
    
    Args:
        monthly_df: DataFrame with year_month, product_name, sales_amount
        save_path: Optional save path
    """
    # Pivot data
    pivot_df = monthly_df.pivot_table(
        index='product_name',
        columns='year_month',
        values='sales_amount',
        aggfunc='sum'
    )
    
    # Create heatmap
    plt.figure(figsize=(16, 8))
    sns.heatmap(
        pivot_df,
        annot=False,
        fmt='.0f',
        cmap='YlOrRd',
        cbar_kws={'label': 'Sales Amount (₹)'},
        linewidths=0.5
    )
    
    plt.title('Monthly Sales Heatmap by Product', fontsize=16, pad=20)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Product', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_growth_percentage(metrics_df, save_path=None):
    """
    Plot growth percentage comparing YTD vs PYTD.
    
    Args:
        metrics_df: DataFrame with growth_ytd_vs_pytd_pct
        save_path: Optional save path
    """
    df = metrics_df.copy().sort_values('growth_ytd_vs_pytd_pct', ascending=True)
    
    # Color based on positive/negative
    colors = ['green' if x >= 0 else 'red' for x in df['growth_ytd_vs_pytd_pct']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['growth_ytd_vs_pytd_pct'],
        y=df['product_name'],
        orientation='h',
        marker=dict(color=colors),
        text=df['growth_ytd_vs_pytd_pct'].round(1).astype(str) + '%',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Growth: %{x:.1f}%<extra></extra>'
    ))
    
    fig.add_vline(x=0, line_dash='dash', line_color='black')
    
    fig.update_layout(
        title='YTD Growth Rate vs PYTD by Product (%)',
        xaxis_title='Growth Rate (%)',
        yaxis_title='Product',
        height=500,
        showlegend=False
    )
    
    if save_path:
        fig.write_html(save_path)
    
    fig.show()
    return fig


if __name__ == '__main__':
    print('Visualization Functions Module')
    print('=' * 50)
    print('\nAvailable functions:')
    print('1. plot_ytd_scatter_with_delta() - Scatter plot with red/green coloring')
    print('2. plot_ytd_comparison_bars() - Bar chart YTD vs PYTD vs P1YTD')
    print('3. plot_time_series_by_product() - Time series line charts')
    print('4. plot_seasonal_decomposition() - Seasonal decomposition')
    print('5. plot_heatmap_monthly_sales() - Monthly sales heatmap')
    print('6. plot_growth_percentage() - Growth percentage comparison')
    print('\nUsage: Import functions and pass calculated metrics DataFrames')
