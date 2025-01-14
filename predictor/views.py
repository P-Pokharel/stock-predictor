from django.shortcuts import render
from django.views import View
from .algorithm import RandomForest
from .models import StockData
import numpy as np

# Create your views here.

class HomeView(View):
    def get(self, request):
        # Fetch all unique stock symbols
        stock_symbols = StockData.objects.values('symbol').distinct()
        context = {
            'stock_symbols': stock_symbols
        }
        return render(request, 'predictor/home.html', context)
    

class PredictionView(View):
    def get(self, request):
        stock_symbol = request.GET.get('stockSymbol', None)

        # Validate the stock symbol
        if not stock_symbol:
            return render(request, 'predictor/result.html', {
                'error': 'No stock symbol selected.'
            })
        
        # Fetch data for the selected stock symbol using ORM
        stock_data = StockData.objects.filter(symbol=stock_symbol).values(
            'open_price', 'high', 'low', 'close_price', 'percent_change'
        )

        if not stock_data.exists():
            return render(request, 'predictor/result.html', {
                'error': f'No data found for the stock symbol: {stock_symbol}.'
            })
        
        data = np.array([[
            record['open_price'],
            record['high'],
            record['low'],
            record['close_price'],
            record['percent_change']
        ] for record in stock_data])

        # Extract features and target
        X = data[:, :-1]  # Features (Open, High, Low, Close)
        y = (data[:, -1] > 0).astype(int)  # Target (Positive Percent Change)

        # Split data into training and testing sets
        np.random.seed(1234)
        indices = np.arange(X.shape[0])
        np.random.shuffle(indices)
        split_idx = int(0.8 * len(indices))
        train_indices, test_indices = indices[:split_idx], indices[split_idx:]
        X_train, X_test = X[train_indices], X[test_indices]
        y_train, y_test = y[train_indices], y[test_indices]

        # Train RandomForest
        clf = RandomForest(n_trees=20)
        clf.fit(X_train, y_train)

        # Predict on test set
        predictions = clf.predict(X_test)

        # Calculate accuracy
        accuracy = np.sum(y_test == predictions) / len(y_test)

        # Predict next movement for the last row in the dataset
        last_row = X[-1].reshape(1, -1)
        next_movement = clf.predict(last_row)[0]
        result = "Yes" if next_movement == 1 else "No"

        # Pass data to template
        return render(request, 'predictor/result.html', {
            'result': result,
            'accuracy': round(accuracy * 100, 2),
            'symbol': stock_symbol
        })