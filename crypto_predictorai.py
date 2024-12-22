import requests
import numpy as np
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Welcome message
print("Welcome to Crypto Prediction AI!")
print("This AI helps you predict the next market price of any cryptocurrency.")
print("Enter the coin symbol (e.g., BTC, ETH, DOGE) to get predictions.")
print("Note: This is for research purposes only and not financial advice.")

# Function to fetch data from CoinGecko
def fetch_coingecko_data(symbol):
    url = f"https://api.coingecko.com/api/v3/coins/{symbol.lower()}/market_chart"
    params = {"vs_currency": "usd", "days": "30"}  # 30 days of historical data
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['prices']
    else:
        print(f"Error fetching data from CoinGecko for {symbol}.")
        return None

# Function to calculate support and resistance
def calculate_support_resistance(prices):
    arr = np.array(prices)
    support = np.min(arr)
    resistance = np.max(arr)
    return support, resistance

# Function to predict next price trend
def predict_next_price(prices):
    recent_prices = np.array(prices[-5:])  # Use last 5 data points for trend analysis
    trend = np.mean(recent_prices) - recent_prices[0]
    return recent_prices[-1] + trend

# Function to generate a chart
def generate_chart(prices, symbol):
    days = list(range(1, len(prices) + 1))
    img = Image.new("RGB", (800, 400), color="white")
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((10, 10), f"{symbol.upper()} Price Chart", fill="black")
    
    # Plot prices
    max_price = max(prices)
    min_price = min(prices)
    scale = 300 / (max_price - min_price)
    x_step = 750 / len(prices)
    prev_point = (50, 350 - int((prices[0] - min_price) * scale))
    for i, price in enumerate(prices[1:], 1):
        new_point = (50 + int(i * x_step), 350 - int((price - min_price) * scale))
        draw.line([prev_point, new_point], fill="blue", width=2)
        prev_point = new_point
    
    # Save chart
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# Main function
def main():
    symbol = input("Enter the cryptocurrency symbol: ").strip()
    data = fetch_coingecko_data(symbol)
    
    if not data:
        print("Failed to fetch data. Please try again.")
        return
    
    # Extract prices
    prices = [price[1] for price in data]
    support, resistance = calculate_support_resistance(prices)
    predicted_price = predict_next_price(prices)
    
    # Display details
    print(f"\n--- Prediction Results for {symbol.upper()} ---")
    print(f"Current Price: ${prices[-1]:.2f}")
    print(f"Support Level: ${support:.2f}")
    print(f"Resistance Level: ${resistance:.2f}")
    print(f"Predicted Next Price: ${predicted_price:.2f}")
    print("\nNote: This is not financial advice. Do your own research.")
    
    # Generate chart
    chart = generate_chart(prices, symbol)
    with open(f"{symbol}_chart.png", "wb") as f:
        f.write(chart.getvalue())
    print(f"Price chart saved as {symbol}_chart.png")

# Run the program
if __name__ == "__main__":
    main()
