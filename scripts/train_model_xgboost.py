import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
import logging

logging.basicConfig(level=logging.INFO)

def train_xgboost(input_file):
    logging.info(f"Reading processed data from {input_file}")
    
    df = pd.read_csv(input_file)

    # Features and target
    X = df.drop('Amount', axis=1)
    y = df['Amount']

    # Splitting the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scaling the data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Training XGBoost model
    logging.info("Training XGBoost model.")
    model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(X_train_scaled, y_train)

    # Saving model and scaler
    with open('models/final_model_xgboost.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('models/fitted_scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    logging.info("XGBoost model trained and saved successfully.")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Train XGBoost model using preprocessed daily transaction data")
    parser.add_argument('--input_file', required=True, help="Path to the preprocessed data CSV file")
    args = parser.parse_args()

    train_xgboost(args.input_file)
