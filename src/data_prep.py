import os
import pandas as pd
import numpy as np

def load_or_create_agriculture_data():
    """
    Simulates Phase 2 (Data Acquisition) by loading the agriculture dataset.
    If the CSV isn't in data/raw/, it generates a mock dataset to allow 
    immediate pipeline testing.
    """
    raw_data_path = os.path.join("data", "raw", "india_agriculture_data.csv")
    
    if os.path.exists(raw_data_path):
        print(f"📦 Found dataset locally at: {raw_data_path}")
        df = pd.read_csv(raw_data_path)
    else:
        print("⚠️ Local dataset not found. Generating mock DALC dataset for testing...")
        
        # Seed for reproducibility
        np.random.seed(42)
        n_samples = 500
        
        # Core 10 variables from the DALC project architecture[cite: 2]
        data = {
            "Crop": np.random.choice(["Rice", "Wheat", "Cotton", "Sugarcane", "Maize"], n_samples),
            "State": np.random.choice(["Punjab", "Uttar Pradesh", "Madhya Pradesh", "Andhra Pradesh", "Gujarat"], n_samples),
            "Soil Type": np.random.choice(["Clay", "Loamy", "Sandy", "Black", "Alluvial"], n_samples),
            "Rainfall": np.round(np.random.uniform(400, 1500, n_samples), 2),      # mm[cite: 2]
            "Temperature": np.round(np.random.uniform(20, 38, n_samples), 2),     # °C[cite: 2]
            "Humidity": np.round(np.random.uniform(40, 90, n_samples), 2),        # %[cite: 2]
            "Fertilizer": np.round(np.random.uniform(50, 200, n_samples), 2),     # kg/ha[cite: 2]
            "Irrigation": np.random.choice(["Tube Well", "Canal", "Rainfed", "Drip"], n_samples),
            "Yield": np.round(np.random.uniform(1.2, 5.5, n_samples), 2),         # tonnes/ha (Target)[cite: 2]
            "Mkt Price": np.round(np.random.uniform(1500, 4500, n_samples), 2)    # ₹ per tonne[cite: 2]
        }
        
        df = pd.DataFrame(data)
        
        # Inject a few intentional missing values to test Phase 3 cleaning tomorrow[cite: 2]
        df.loc[df.sample(frac=0.05).index, "Yield"] = np.nan
        df.loc[df.sample(frac=0.03).index, "Rainfall"] = np.nan
        
        # Save to raw directory
        os.makedirs(os.path.dirname(raw_data_path), exist_ok=True)
        df.to_csv(raw_data_path, index=False)
        print(f"✅ Generated mock dataset and saved to: {raw_data_path}")
        
    print("\n📝 --- Dataset Structure Analysis ---")
    print(f"Total Records: {df.shape[0]} | Total Features: {df.shape[1]}")
    print("\nColumns and Data Types:")
    print(df.dtypes)
    return df

if __name__ == "__main__":
    load_or_create_agriculture_data()

import os
import pandas as pd
import numpy as np

def load_or_create_agriculture_data():
    """Loads or generates the raw agriculture dataset (Phase 2)."""
    raw_data_path = os.path.join("data", "raw", "india_agriculture_data.csv")
    if os.path.exists(raw_data_path):
        df = pd.read_csv(raw_data_path)
    else:
        # Fallback generator if file doesn't exist
        np.random.seed(42)
        n_samples = 500
        data = {
            "Crop": np.random.choice(["Rice", "Wheat", "Cotton", "Sugarcane", "Maize"], n_samples),
            "State": np.random.choice(["Punjab", "Uttar Pradesh", "Madhya Pradesh", "Andhra Pradesh", "Gujarat"], n_samples),
            "Soil Type": np.random.choice(["Clay", "Loamy", "Sandy", "Black", "Alluvial"], n_samples),
            "Rainfall": np.round(np.random.uniform(400, 1500, n_samples), 2),
            "Temperature": np.round(np.random.uniform(20, 38, n_samples), 2),
            "Humidity": np.round(np.random.uniform(40, 90, n_samples), 2),
            "Fertilizer": np.round(np.random.uniform(50, 200, n_samples), 2),
            "Irrigation": np.random.choice(["Tube Well", "Canal", "Rainfed", "Drip"], n_samples),
            "Yield": np.round(np.random.uniform(1.2, 5.5, n_samples), 2),
            "Mkt Price": np.round(np.random.uniform(1500, 4500, n_samples), 2)
        }
        df = pd.DataFrame(data)
        df.loc[df.sample(frac=0.05).index, "Yield"] = np.nan
        df.loc[df.sample(frac=0.03).index, "Rainfall"] = np.nan
        os.makedirs(os.path.dirname(raw_data_path), exist_ok=True)
        df.to_csv(raw_data_path, index=False)
    return df

def clean_and_transform_data(df):
    """Executes Phase 3: Data Cleaning, Transformation, and Feature Engineering."""
    print("\n🧹 --- Starting Phase 3: Data Preparation ---")
    
    # 1. Handle Missing Values (Imputation using Median/Mean)
    print(f"Missing values before cleaning:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    
    df["Yield"] = df["Yield"].fillna(df["Yield"].median())
    df["Rainfall"] = df["Rainfall"].fillna(df["Rainfall"].mean())
    
    # 2. Feature Engineering
    print("\n⚙️ Engineering features...")
    # Profit = Yield * Market Price
    df["Profit"] = np.round(df["Yield"] * df["Mkt Price"], 2)
    # Rainfall-to-Humidity Ratio
    df["Rainfall_Humidity_Ratio"] = np.round(df["Rainfall"] / df["Humidity"], 4)
    
    # 3. Save processed dataset
    processed_path = os.path.join("data", "processed", "cleaned_agriculture_data.csv")
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    df.to_csv(processed_path, index=False)
    
    print(f"✅ Processed data successfully exported to: {processed_path}")
    print(f"New Data Shape: {df.shape}")
    return df

if __name__ == "__main__":
    raw_df = load_or_create_agriculture_data()
    cleaned_df = clean_and_transform_data(raw_df)