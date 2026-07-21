# ==============================================================================
# PROJECT: CUSTOMER INTELLIGENCE & SALES PREDICTOR
# FILE 2: 2_customer_clustering.py (ALGORITHM 1: K-Means Clustering)
# ==============================================================================

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

def perform_customer_clustering(file_path):
    print("🔄 Loading cleaned data...")
    df = pd.read_csv(file_path)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    print("🛠️ Calculating RFM (Recency, Frequency, Monetary) Features...")
    # Dataset ki aakhri date ko snapshot date maan rahe hain
    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    
    # Customer ke mutabiq group kar ke RFM nikaal rahe hain
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days, # Recency: Kitne din pehle aaya
        'InvoiceNo': 'nunique',                                  # Frequency: Kitni baar khareeda
        'Total_Amount_GBP': 'sum'                                # Monetary: Kitne paise kharch kiye (Base GBP)
    }).reset_index()
    
    # Columns ke naam sahi kar rahe hain
    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary_GBP']
    
    # Pakistan Currency (PKR) mein display karne ke liye conversion (1 GBP = 360 PKR)
    rfm['Monetary_PKR'] = rfm['Monetary_GBP'] * 360.0
    
    print(f"✅ RFM features created for {rfm.shape[0]} unique customers.")
    
    print("\n🔄 Scaling features for K-Means...")
    # K-Means ke liye data ko normalize/scale karna zaroori hota hai
    features = ['Recency', 'Frequency', 'Monetary_GBP']
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(rfm[features])
    
    print("\n🤖 Training K-Means Algorithm (Clusters = 3)...")
    # Hum 3 clusters bana rahe hain (e.g., VIP, Regular, Low-Value)
    kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42, n_init=10)
    rfm['Cluster'] = kmeans.fit_predict(scaled_features)
    
    print("✅ K-Means training complete!")
    
    # Clusters ko samajhne ke liye un ka naam (Label) rakhna
    # Note: K-Means cluster numbers (0,1,2) randomly deta hai, hum average dekh kar name assign kar sakte hain
    cluster_centers = rfm.groupby('Cluster')['Monetary_PKR'].mean().sort_values(ascending=False)
    
    # Mapping logic: Sab se zyada spending wala VIP, sab se kam wala Low-Value
    cluster_mapping = {}
    labels = ['VIP Customer', 'Regular Customer', 'Low-Value / At Risk']
    for i, cluster_id in enumerate(cluster_centers.index):
        cluster_mapping[cluster_id] = labels[i]
        
    rfm['Customer_Segment'] = rfm['Cluster'].map(cluster_mapping)
    
    print("\n📊 Customer Segments Summary (Average PKR Spending):")
    print(rfm.groupby('Customer_Segment')['Monetary_PKR'].mean().to_string())
    
    # 💾 Model aur Scaler ko save kar rahe hain taake Streamlit dashboard par use ho sakein
    print("\n💾 Saving K-Means model and Scaler...")
    with open('kmeans_model.pkl', 'wb') as f:
        pickle.dump(kmeans, f)
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    print("✅ Saved: 'kmeans_model.pkl' and 'scaler.pkl'")
    
    return rfm

def plot_clusters(rfm_df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=rfm_df, 
        x='Frequency', 
        y='Monetary_PKR', 
        hue='Customer_Segment', 
        palette='Set1',
        alpha=0.7
    )
    plt.title('Customer Segments based on K-Means Clustering')
    plt.xlabel('Frequency (Number of Visits)')
    plt.ylabel('Monetary Value (in PKR)')
    plt.yscale('log') # Data ka scale bara hota hai isliye log scale use kiya
    plt.tight_layout()
    plt.savefig('customer_clusters.png')
    print("💾 Saved visualization: customer_clusters.png")
    plt.close()

if __name__ == "__main__":
    input_file = "cleaned_data.csv"
    
    try:
        rfm_data = perform_customer_clustering(input_file)
        plot_clusters(rfm_data)
        
        # Is customer-level data को save kar rahe hain kyunki yeh aage Churn Prediction mein kaam aayega
        rfm_data.to_csv("customer_rfm_data.csv", index=False)
        print("\n🎉 Success! Step 2 complete. 'customer_rfm_data.csv' is ready.")
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mili. Pehle File 1 (1_eda_and_cleaning.py) chalayein.")