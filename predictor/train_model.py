import django
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spp.settings')
django.setup()

from predictor.models import StockData
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def train_and_save_model():
    stock_data = StockData.objects.all().values("symbol", "open_price", "high", "low", "close_price", "volume")

    if not stock_data.exists():
        print('No data found.')
        return
    
    df = pd.DataFrame.from_records(stock_data)

    stock_symbols = df['symbol'].unique()

    for symbol in stock_symbols:
        print(f"Training model for {symbol}...")

        stock_df = df[df["symbol"] == symbol].copy()  # Added .copy() to avoid SettingWithCopyWarning
        
        # Create target variable as next day's closing price
        stock_df['next_day_close'] = stock_df['close_price'].shift(-1)
        
        # Drop the last row since it won't have a next day's close price
        stock_df = stock_df.dropna()

        # Feature selection
        features = ["open_price", "high", "low", "close_price", "volume"]
        target = "next_day_close"

        X = stock_df[features].values
        y = stock_df[target].values

        # Prevent empty dataset errors
        if len(X) == 0 or len(y) == 0: 
            print(f"Skipping {symbol} because it has no valid data.")
            continue

        # Train-test split
        np.random.seed(42)
        indices = np.arange(len(X))
        np.random.shuffle(indices)
        split_idx = int(0.8 * len(indices))
        train_idx, test_idx = indices[:split_idx], indices[split_idx:]

        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        # Train the model using sklearn's RandomForestRegressor
        clf = RandomForestRegressor(n_estimators=100, random_state=42)  # Increased n_estimators for better performance
        clf.fit(X_train, y_train)

        # Calculate R-squared score
        r2_score = clf.score(X_test, y_test)
        
        # Calculate Mean Absolute Percentage Error (MAPE)
        y_pred = clf.predict(X_test)
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

        # Save model
        model_data = {
            "model": clf, 
            "r2_score": r2_score,
            "mape": mape
        }
        model_path = f"predictor/trained_models/{symbol}_model.pkl"
        joblib.dump(model_data, model_path)
        print(f"Model for {symbol} saved at {model_path}")



if __name__ == "__main__":
    train_and_save_model()