# ==============================================================================
# PROJECT: CUSTOMER INTELLIGENCE & SALES PREDICTOR
# FILE 4: 4_churn_prediction_comparison.py (ALGORITHMS 3, 4, 5, 6: Churn Prediction)
# ==============================================================================

import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# Scikit-Learn ke algorithms aur evaluation tools
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_and_compare_models(file_path):
    print("🔄 Loading customer RFM data...")
    rfm = pd.read_csv(file_path)
    
    print("🛠️ Creating Churn Label (Target Variable)...")
    # Rule: Agar customer ki Recency 90 din se zyada hai (pichle 90 din se nahi aaya), 
    # to Churn = 1 (Bhag gaya), warna Churn = 0 (Active)
    rfm['Churn'] = np.where(rfm['Recency'] > 90, 1, 0)
    
    print(f"📊 Data Distribution: {rfm['Churn'].value_counts().to_dict()} (0: Active, 1: Churned)")
    
    # Features (X) aur Target (Y) alag kar rahe hain
    X = rfm[['Recency', 'Frequency', 'Monetary_GBP']]
    y = rfm['Churn']
    
    # Data ko Train (80%) aur Test (20%) mein baant rahe hain
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Charon algorithms ko initialize kar rahe hain
    models = {
        'Logistic Regression': LogisticRegression(random_state=42),
        'K-Nearest Neighbors (KNN)': KNeighborsClassifier(n_neighbors=5),
        'Support Vector Machine (SVM)': SVC(probability=True, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
    }
    
    accuracy_results = {}
    saved_models = {}
    
    print("\n🤖 Training and Evaluating 4 Algorithms...")
    for name, model in models.items():
        print(f"⏳ Training {name}...")
        model.fit(X_train, y_train)
        
        # Predictions nikal rahe hain
        y_pred = model.predict(X_test)
        
        # Accuracy calculate kar rahe hain
        acc = accuracy_score(y_test, y_pred)
        accuracy_results[name] = acc * 100 # Percentage mein convert kiya
        saved_models[name] = model
        
        print(f"✅ {name} Complete! Accuracy: {acc*100:.2f}%")
        
    print("\n🏆 Final Accuracy Comparison:")
    for name, acc in accuracy_results.items():
        print(f" - {name}: {acc:.2f}%")
        
    # 💾 Sab se best performing model ko dhoond kar save karna
    best_model_name = max(accuracy_results, key=accuracy_results.get)
    print(f"\n🥇 Best Model is: '{best_model_name}' with {accuracy_results[best_model_name]:.2f}% accuracy!")
    
    print("💾 Saving the best model for Dashboard...")
    with open('best_churn_model.pkl', 'wb') as f:
        pickle.dump(saved_models[best_model_name], f)
    print("✅ Saved: 'best_churn_model.pkl'")
    
    # 📊 Comparison Graph banana visitor ko dikhane ke liye
    plt.figure(figsize=(10, 5))
    sns.barplot(x=list(accuracy_results.keys()), y=list(accuracy_results.values()), palette='coolwarm')
    plt.title('Algorithm Accuracy Comparison for Customer Churn Prediction')
    plt.ylabel('Accuracy (%)')
    plt.ylim(50, 105) # Graph ko clear dekhne ke liye limit set ki
    for i, v in enumerate(accuracy_results.values()):
        plt.text(i, v + 1, f"{v:.2f}%", ha='center', fontweight='bold')
    plt.tight_layout()
    plt.savefig('model_accuracy_comparison.png')
    print("💾 Saved visualization: model_accuracy_comparison.png")
    plt.close()

if __name__ == "__main__":
    input_file = "customer_rfm_data.csv"
    
    try:
        train_and_compare_models(input_file)
        print("\n🎉 Success! Step 4 complete. Total 6 algorithms are now covered in your project!")
        
    except FileNotFoundError:
        print(f"❌ Error: '{input_file}' nahi mila. Pehle File 2 (2_customer_clustering.py) chalayein.")