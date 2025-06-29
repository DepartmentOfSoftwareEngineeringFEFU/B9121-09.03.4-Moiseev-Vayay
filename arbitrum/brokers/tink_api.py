import os
from datetime import datetime, timedelta
from tinkoff.invest import CandleInterval
import pandas as pd
from tinkoff.invest import Client

#графиик
import plotly.graph_objs as go
from plotly.offline import plot

TOKEN = 't.mm4Yd8ystZ4erLgjgi4qXqYZA-Bq2XKhdNB7qsZ5p-3O6j4xcpzs1S3EJ7gub_FADrO4Le9dyPzihETCXfWGvg'

def get_price_by_figi(figi: str):
    with Client(TOKEN) as client:
        orderbook = client.market_data.get_order_book(
            figi=figi,
            depth=1
        )
        return float(orderbook.last_price.units) + orderbook.last_price.nano / 1e9
    
def get_price_history(figi: str, days: int = 5):
    with Client(TOKEN) as client:
        now = datetime.now()
        from_ = now - timedelta(days=days)

        candles = client.market_data.get_candles(
            figi=figi,
            from_=from_,
            to=now,
            interval=CandleInterval.CANDLE_INTERVAL_15_MIN  # 15 минут
        ).candles

        df = pd.DataFrame([{
            "time": c.time,
            "price": c.close.units + c.close.nano / 1e9
        } for c in candles])

        return df
    
def generate_price_chart(figi: str):
    df = get_price_history(figi)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["time"], y=df["price"], mode='lines', name='Цена'))
    fig.update_layout(title="История цены", xaxis_title="Время", yaxis_title="Цена")
    return plot(fig, output_type='div')