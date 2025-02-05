import django
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spp.settings')
django.setup()

from predictor.algorithm import RandomForest
from predictor.models import StockData
import joblib
import pandas as pd
import numpy as np

def train_and_save_model():
    stock_data = StockData.objects.all().values("symbol", "open_price", "high", "low", "close_price", "percent_change")

    if not stock_data.exists():
        print('No data found.')
        return
    
    df = pd.DataFrame.from_records(stock_data)

    stock_symbols = df['symbol'].unique()

    for symbol in stock_symbols:
        print(f"Training model for {symbol}...")

        stock_df = df[df["symbol"] == symbol]

        # Feature selection
        features = ["open_price", "high", "low", "close_price"]
        target = "percent_change"

        # Convert percent change into binary labels
        stock_df.loc[:, target] = (stock_df[target] > 0).astype(int)  # Ensures binary (0,1)

        X = stock_df[features].values
        y = stock_df[target].values.astype(int)

        # Prevent empty dataset errors
        if len(X) == 0 or len(y) == 0:  # ✅ Fix
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

        # Train the model
        clf = RandomForest(n_trees=20)
        clf.fit(X_train, y_train)

        # Calculate accuracy
        predictions = clf.predict(X_test)
        accuracy = np.sum(y_test == predictions) / len(y_test)
        print(f"Accuracy for {symbol}: {accuracy:.2%}")

        # Save model
        model_data = {"model": clf, "accuracy": accuracy}
        model_path = f"predictor/trained_models/{symbol}_model.pkl"
        joblib.dump(model_data, model_path)
        print(f"Model for {symbol} saved at {model_path}")



if __name__ == "__main__":
    train_and_save_model()