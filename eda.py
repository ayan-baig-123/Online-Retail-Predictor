# ==============================================================================
# PROJECT: CUSTOMER INTELLIGENCE & SALES PREDICTOR
# FILE 1: 1_eda_and_cleaning.py (Exploratory Data Analysis & Data Cleaning)
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_clean_data(file_path):
    print("🔄 Step 1: Loading Dataset...")
    # Dataset ko read kar rahe hain (encoding='latin1' ke sath takay Pound symbol ka error na aaye)
    df = pd.read_csv(file_path, encoding='latin1')
    print(f"✅ Data Loaded successfully! Total Rows: {df.shape[0]}, Total Columns: {df.shape[1]}")
    
    print("\n🔄 Step 2: Checking for Missing Values...")
    print(df.isnull().sum())
    
    # Jin rows mein CustomerID khali (NaN) hai unhe remove kar rahe hain
    # Kyunki customer-based algorithms ke liye ID ka hona zaroori hai
    print("\n🧹 Removing rows where CustomerID is missing...")
    df = df.dropna(subset=['CustomerID'])
    df['CustomerID'] = df['CustomerID'].astype(int) # ID ko float se integer mein convert kiya
    
    print("\n🔄 Step 3: Handling Returns & Cancelled Orders...")
    # Agar Quantity zero se kam hai, to wo returned order hai
    # Hum canceled orders ko filter kar rahe hain taake sales prediction accurate ho
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]
    
    print("\n🛠️ Step 4: Feature Engineering (Calculating Total Sales)...")
    # Total Spending (Pound mein) nikal rahe hain
    df['Total_Amount_GBP'] = df['Quantity'] * df['UnitPrice']
    
    # Pakistan Currency (PKR) mein convert karne ke liye column bana rahe hain (Farz karein 1 GBP = 360 PKR)
    df['Total_Amount_PKR'] = df['Total_Amount_GBP'] * 360.0
    
    # InvoiceDate ko datetime format mein convert kar rahe hain
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    print(f"✅ Data Cleaning Complete! Active Rows left: {df.shape[0]}")
    return df

def generate_visualizations(df):
    print("\n📊 Step 5: Generating Visualizations for Dashboard/Presentation...")
    
    # 1. Top 10 Best Selling Products (Quantity ke hisab se)
    plt.figure(figsize=(10, 5))
    top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
    sns.barplot(x=top_products.values, y=top_products.index, palette='viridis')
    plt.title('Top 10 Best Selling Products')
    plt.xlabel('Total Quantity Sold')
    plt.ylabel('Product Description')
    plt.tight_layout()
    plt.savefig('top_products.png')
    print("💾 Saved: top_products.png")
    plt.close()
    
    # 2. Top Countries by Revenue (Excluding UK for better scale comparison if needed, or keeping it)
    plt.figure(figsize=(10, 5))
    top_countries = df.groupby('Country')['Total_Amount_PKR'].sum().sort_values(ascending=False).head(5)
    sns.barplot(x=top_countries.index, y=top_countries.values / 1e6, palette='mako') # Millions mein show karne ke liye
    plt.title('Top 5 Countries by Revenue (in Million PKR)')
    plt.xlabel('Country')
    plt.ylabel('Revenue (Millions Rs.)')
    plt.tight_layout()
    plt.savefig('top_countries_revenue.png')
    print("💾 Saved: top_countries_revenue.png")
    plt.close()

if __name__ == "__main__":
    # Assuming your dataset is named 'data.csv' and is in the same folder
    file_path = "data.csv" 
    
    try:
        cleaned_df = load_and_clean_data(file_path)
        generate_visualizations(cleaned_df)
        
        # Cleaned data ko save kar rahe hain taake agla algorithm (K-Means) ise use kar sake
        cleaned_df.to_csv("cleaned_data.csv", index=False)
        print("\n🎉 Success! Cleaned data saved as 'cleaned_data.csv'. Ready for the next stage.")
        
    except FileNotFoundError:
        print(f"❌ Error: '{file_path}' file nahi mili. Meherbani kar ke check karein ke file ka naam sahi hai.")