# ==============================================================================
# PROJECT: CUSTOMER INTELLIGENCE & SALES PREDICTOR
# FILE 3: 3_product_recommendation.py (ALGORITHM 2: Apriori Algorithm - UPDATED)
# ==============================================================================

import pandas as pd
import numpy as np
import pickle
# Note: Is algorithm ke liye 'mlxtend' library zaroori hai. 
from mlxtend.frequent_patterns import apriori, association_rules

def generate_product_recommendations(file_path):
    print("🔄 Loading cleaned data...")
    df = pd.read_csv(file_path)
    
    print("🛠️ Grouping transactions by Invoice and Description...")
    # Har bill (InvoiceNo) mein kaun sa item (Description) kitni baar aaya, us ka matrix bana rahe hain
    # Hum sirf top 500 best selling items par focus karenge taake processing fast ho aur memory crash na ho
    top_products = df['Description'].value_counts().head(500).index
    df_filtered = df[df['Description'].isin(top_products)]
    
    basket = (df_filtered.groupby(['InvoiceNo', 'Description'])['Quantity']
              .sum().unstack().reset_index().fillna(0)
              .set_index('InvoiceNo'))
    
    print("🧹 Converting quantities to Binary (0 or 1) for Apriori...")
    # Apriori ko sirf haan (1) ya naa (0) chahiye hota hai, quantity se farq nahi parta
    def encode_units(x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1
    
    # UPDATED: Pandas naye version ke liye applymap ki jagah map() use kiya hai
    basket_sets = basket.map(encode_units)
    print(f"✅ Market Basket Matrix Created! Shape: {basket_sets.shape}")
    
    print("\n🤖 Training Apriori Algorithm (Finding Frequent Itemsets)...")
    # min_support = 0.02 (Yani wo items jo kam se kam 2% bills mein sath aaye hon)
    frequent_itemsets = apriori(basket_sets, min_support=0.02, use_colnames=True)
    
    print("🔮 Generating Association Rules...")
    # Lift metric ke zariye hum strong connections dhoond rahe hain
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    
    # Rules ko clear aur sorting ke sath arrange kar rahe hain
    rules = rules.sort_values('lift', ascending=False).reset_index(drop=True)
    
    print(f"✅ Rules Generated successfully! Total strong relationships found: {rules.shape[0]}")
    
    # Visitor ko top 5 relationships print kar ke dikhana
    print("\n📊 Sample of Frequently Bought Together Products (Top 5 Rules):")
    for idx, row in rules.head(5).iterrows():
        antecedents = list(row['antecedents'])[0]
        consequents = list(row['consequents'])[0]
        print(f"👉 Agar log [{antecedents}] khareedte hain -> To wo [{consequents}] bhi khareedte hain! (Confidence: {row['confidence']:.2%})")
        
    # 💾 Recommendation Rules ko save kar rahe hain taake Streamlit Dashboard par use ho sakein
    print("\n💾 Saving Apriori Recommendation Rules...")
    # Hum sirf zaroori columns save kar rahe hain taake file ka size chota rahe
    final_rules_df = rules[['antecedents', 'consequents', 'confidence', 'lift']]
    with open('recommendation_rules.pkl', 'wb') as f:
        pickle.dump(final_rules_df, f)
    print("✅ Saved: 'recommendation_rules.pkl'")
    
    return final_rules_df

if __name__ == "__main__":
    input_file = "cleaned_data.csv"
    
    try:
        recommend_rules = generate_product_recommendations(input_file)
        print("\n🎉 Success! Step 3 complete. Recommendation engine model is saved.")
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mili. Pehle File 1 (1_eda_and_cleaning.py) chalayein.")