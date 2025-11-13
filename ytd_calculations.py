"""YTD, PYTD, and P1YTD Calculations Module

Calculates Year-to-Date (YTD), Previous Year-to-Date (PYTD), and Prior Year-to-Date (P1YTD)
metrics for e-commerce sales data across multiple fiscal years.

Functions:
    - get_fiscal_year: Determine fiscal year for a given date
    - get_ytd_date_range: Get date range for YTD calculations
    - calculate_ytd_metrics: Calculate YTD, PYTD, P1YTD for products
    - calculate_deltas: Calculate growth/decline metrics
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Tuple, Dict


def get_fiscal_year(date: datetime) -> str:
    """
    Determine fiscal year for a given date.
    Indian fiscal year runs from April 1 to March 31.
    
    Args:
        date: Date to determine fiscal year for
    
    Returns:
        Fiscal year string (e.g., 'FY 2023-24')
    """
    if date.month >= 4:  # April to December
        fy_start = date.year
        fy_end = date.year + 1
    else:  # January to March
        fy_start = date.year - 1
        fy_end = date.year
    
    return f"FY {fy_start}-{str(fy_end)[-2:]}"


def get_ytd_date_range(as_of_date: datetime) -> Tuple[datetime, datetime]:
    """
    Get the date range for YTD calculation based on fiscal year.
    
    Args:
        as_of_date: The "as of" date for YTD calculation
    
    Returns:
        Tuple of (fiscal_year_start, as_of_date)
    """
    if as_of_date.month >= 4:
        fiscal_year_start = datetime(as_of_date.year, 4, 1)
    else:
        fiscal_year_start = datetime(as_of_date.year - 1, 4, 1)
    
    return fiscal_year_start, as_of_date


def calculate_ytd_metrics(df: pd.DataFrame, as_of_date: datetime = None) -> pd.DataFrame:
    """
    Calculate YTD, PYTD, and P1YTD metrics for all products.
    
    Args:
        df: Sales DataFrame with columns: date, product_name, sales_amount, quantity
        as_of_date: Date to calculate YTD as of (default: latest date in data)
    
    Returns:
        DataFrame with YTD, PYTD, P1YTD metrics by product
    """
    # Convert date column to datetime if not already
    df['date'] = pd.to_datetime(df['date'])
    
    # Use latest date if as_of_date not provided
    if as_of_date is None:
        as_of_date = df['date'].max()
    
    # Get fiscal year info
    current_fy = get_fiscal_year(as_of_date)
    
    # Get date ranges for YTD, PYTD, P1YTD
    ytd_start, ytd_end = get_ytd_date_range(as_of_date)
    
    # PYTD: Same period in previous fiscal year
    pytd_start = ytd_start - timedelta(days=365)
    pytd_end = ytd_end - timedelta(days=365)
    
    # P1YTD: Same period two fiscal years ago
    p1ytd_start = ytd_start - timedelta(days=730)
    p1ytd_end = ytd_end - timedelta(days=730)
    
    print(f"\nCalculating metrics as of {as_of_date.strftime('%Y-%m-%d')} ({current_fy})")
    print(f"YTD Period: {ytd_start.strftime('%Y-%m-%d')} to {ytd_end.strftime('%Y-%m-%d')}")
    print(f"PYTD Period: {pytd_start.strftime('%Y-%m-%d')} to {pytd_end.strftime('%Y-%m-%d')}")
    print(f"P1YTD Period: {p1ytd_start.strftime('%Y-%m-%d')} to {p1ytd_end.strftime('%Y-%m-%d')}")
    
    # Filter data for each period
    ytd_data = df[(df['date'] >= ytd_start) & (df['date'] <= ytd_end)]
    pytd_data = df[(df['date'] >= pytd_start) & (df['date'] <= pytd_end)]
    p1ytd_data = df[(df['date'] >= p1ytd_start) & (df['date'] <= p1ytd_end)]
    
    # Aggregate by product
    ytd_summary = ytd_data.groupby('product_name').agg({
        'sales_amount': 'sum',
        'quantity': 'sum'
    }).reset_index()
    ytd_summary.columns = ['product_name', 'ytd_sales', 'ytd_quantity']
    
    pytd_summary = pytd_data.groupby('product_name').agg({
        'sales_amount': 'sum',
        'quantity': 'sum'
    }).reset_index()
    pytd_summary.columns = ['product_name', 'pytd_sales', 'pytd_quantity']
    
    p1ytd_summary = p1ytd_data.groupby('product_name').agg({
        'sales_amount': 'sum',
        'quantity': 'sum'
    }).reset_index()
    p1ytd_summary.columns = ['product_name', 'p1ytd_sales', 'p1ytd_quantity']
    
    # Merge all metrics
    metrics = ytd_summary.merge(pytd_summary, on='product_name', how='outer')
    metrics = metrics.merge(p1ytd_summary, on='product_name', how='outer')
    
    # Fill NaN values with 0
    metrics = metrics.fillna(0)
    
    # Add fiscal year info
    metrics['as_of_date'] = as_of_date
    metrics['fiscal_year'] = current_fy
    
    return metrics


def calculate_deltas(metrics: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate delta/growth metrics comparing YTD with PYTD and P1YTD.
    
    Args:
        metrics: DataFrame from calculate_ytd_metrics
    
    Returns:
        DataFrame with additional delta and growth percentage columns
    """
    df = metrics.copy()
    
    # Sales deltas
    df['delta_ytd_pytd'] = df['ytd_sales'] - df['pytd_sales']
    df['delta_ytd_p1ytd'] = df['ytd_sales'] - df['p1ytd_sales']
    df['delta_pytd_p1ytd'] = df['pytd_sales'] - df['p1ytd_sales']
    
    # Growth percentages
    df['growth_ytd_vs_pytd_pct'] = ((df['ytd_sales'] - df['pytd_sales']) / df['pytd_sales'] * 100).replace([float('inf'), -float('inf')], 0)
    df['growth_ytd_vs_p1ytd_pct'] = ((df['ytd_sales'] - df['p1ytd_sales']) / df['p1ytd_sales'] * 100).replace([float('inf'), -float('inf')], 0)
    
    # Quantity deltas
    df['qty_delta_ytd_pytd'] = df['ytd_quantity'] - df['pytd_quantity']
    df['qty_delta_ytd_p1ytd'] = df['ytd_quantity'] - df['p1ytd_quantity']
    
    # Absolute delta for bubble size in visualizations
    df['abs_delta_ytd_pytd'] = df['delta_ytd_pytd'].abs()
    
    # Performance classification
    df['performance'] = df['delta_ytd_pytd'].apply(
        lambda x: 'Growing' if x > 0 else ('Declining' if x < 0 else 'Stable')
    )
    
    return df


def get_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate monthly sales trends by product.
    
    Args:
        df: Sales DataFrame with date, product_name, sales_amount
    
    Returns:
        DataFrame with monthly aggregated sales by product
    """
    df['date'] = pd.to_datetime(df['date'])
    df['year_month'] = df['date'].dt.to_period('M')
    df['fiscal_year'] = df['date'].apply(get_fiscal_year)
    
    monthly = df.groupby(['year_month', 'fiscal_year', 'product_name']).agg({
        'sales_amount': 'sum',
        'quantity': 'sum'
    }).reset_index()
    
    monthly['year_month'] = monthly['year_month'].dt.to_timestamp()
    
    return monthly


def get_category_performance(df: pd.DataFrame, product_category_map: Dict[str, str]) -> pd.DataFrame:
    """
    Calculate YTD metrics by product category.
    
    Args:
        df: Sales DataFrame
        product_category_map: Dictionary mapping product names to categories
    
    Returns:
        DataFrame with category-level YTD metrics
    """
    # Add category column
    df_with_cat = df.copy()
    df_with_cat['category'] = df_with_cat['product_name'].map(product_category_map)
    
    # Calculate metrics by category
    metrics = calculate_ytd_metrics(df_with_cat.rename(columns={'category': 'product_name'}))
    metrics = calculate_deltas(metrics)
    
    return metrics.rename(columns={'product_name': 'category'})


if __name__ == "__main__":
    # Example usage
    print("YTD Calculations Module")
    print("=" * 50)
    
    # Example: Load generated data and calculate metrics
    try:
        import data_generator
        print("\nGenerating sample sales data...")
        sales_df = data_generator.generate_complete_dataset()
        
        print(f"\nTotal records: {len(sales_df):,}")
        print(f"Date range: {sales_df['date'].min()} to {sales_df['date'].max()}")
        
        # Calculate YTD metrics as of latest date
        print("\nCalculating YTD metrics...")
        ytd_metrics = calculate_ytd_metrics(sales_df)
        ytd_with_deltas = calculate_deltas(ytd_metrics)
        
        print("\nYTD Metrics Summary:")
        print(ytd_with_deltas[['product_name', 'ytd_sales', 'pytd_sales', 'delta_ytd_pytd', 'growth_ytd_vs_pytd_pct', 'performance']].to_string(index=False))
        
        # Calculate monthly trends
        print("\nCalculating monthly trends...")
        monthly_trends = get_monthly_trends(sales_df)
        print(f"Monthly trend records: {len(monthly_trends):,}")
        
    except ImportError:
        print("\nNote: Run data_generator.py first to generate sales data.")
        print("This module provides functions for YTD/PYTD/P1YTD calculations.")
