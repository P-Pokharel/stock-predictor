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
        stock_data = StockData.objects.filter(symbol=stock_symbol).values("date", "close_price", "open_price", "high", "low")

        if not stock_data.exists():
            return render(request, "predictor/result.html", {"error": "No data available for this stock."})

        df = pd.DataFrame.from_records(stock_data)
        df["date"] = pd.to_datetime(df["date"])  # Convert date to datetime
        df = df.sort_values("date")  # Sort by date

        # Load trained model and accuracy
        model_data = joblib.load(model_path)
        clf = model_data["model"]
        accuracy = model_data["accuracy"]

        # Prepare data for prediction
        X = df[["open_price", "high", "low", "close_price"]].values
        prediction = clf.predict(X[-1].reshape(1, -1))[0]
        result = "Increase" if prediction == 1 else "Decrease"

        # Generate line chart for Closing Price trend
        plt.figure(figsize=(8, 4))
        sns.lineplot(x=df["date"], y=df["close_price"], marker="o", linestyle="-", color="blue")
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.title(f"Closing Price Trend for {stock_symbol}")
        plt.xticks(rotation=45)
        plt.grid(True)

        # Save plot to static folder
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)

        plot_path = os.path.join(settings.MEDIA_ROOT, f"{stock_symbol}_trend.png")
        plt.savefig(plot_path)
        plt.close()

        # Pass data to template
        return render(request, "predictor/result.html", {
            "prediction": result,
            "accuracy": round(accuracy * 100, 2),
            "symbol": stock_symbol,
            "plot_url": f"/media/{stock_symbol}_trend.png"
        })