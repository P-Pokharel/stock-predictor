from django.shortcuts import render
from django.views import View
from .models import StockData
import os
import pandas as pd
import joblib
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import seaborn as sns
from django.conf import settings

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

        # Check if the trained model exists
        model_path = f"predictor/trained_models/{stock_symbol}_model.pkl"
        if not os.path.exists(model_path):
            return render(request, "predictor/result.html", {"error": f"No trained model found for {stock_symbol}."})

        # Fetch stock data (including date and close price)
        stock_data = StockData.objects.filter(symbol=stock_symbol).values("date", "close_price", "open_price", "high", "low", "volume")

        if not stock_data.exists():
            return render(request, "predictor/result.html", {"error": "No data available for this stock."})

        df = pd.DataFrame.from_records(stock_data)
        df["date"] = pd.to_datetime(df["date"])  # Convert date to datetime
        df = df.sort_values("date")  # Sort by date

        # Load trained model and metrics
        model_data = joblib.load(model_path)
        clf = model_data["model"]
        r2_score = model_data["r2_score"]
        mape = model_data["mape"]

        # Prepare data for prediction (using the last day's data)
        X = df[["open_price", "high", "low", "close_price", "volume"]].values
        # Get predictions for all data points
        all_predictions = clf.predict(X)
        
        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(df['date'][-30:], df['close_price'][-30:], label='Actual', color='blue')
        plt.plot(df['date'][-30:], all_predictions[-30:], label='Predicted', color='red', linestyle='--')
        
        # Add the future prediction point
        next_date = df['date'].iloc[-1] + pd.Timedelta(days=1)
        predicted_price = clf.predict(X[-1].reshape(1, -1))[0]
        current_price = df["close_price"].iloc[-1]
        
        # Calculate percentage change
        price_change = ((predicted_price - current_price) / current_price) * 100
        
        # Add the future prediction point
        plt.plot([df['date'].iloc[-1], next_date], 
                [df['close_price'].iloc[-1], predicted_price], 
                color='red', linestyle='--')
        plt.scatter(next_date, predicted_price, color='red', s=100, label='Next Day Prediction')
        
        plt.title(f'Stock Price Trend for {stock_symbol}')
        plt.xlabel('Date')
        plt.ylabel('Price ($)')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the plot
        plot_path = os.path.join(settings.MEDIA_ROOT, f'{stock_symbol}_trend.png')
        plt.savefig(plot_path)
        plt.close()
        
        # Pass data to template
        return render(request, "predictor/result.html", {
            "predicted_price": round(predicted_price, 2),
            "current_price": round(current_price, 2),
            "price_change": round(price_change, 2),
            "r2_score": round(r2_score * 100, 2),
            "mape": round(mape, 2),
            "symbol": stock_symbol,
            "plot_url": f"/media/{stock_symbol}_trend.png"
        })