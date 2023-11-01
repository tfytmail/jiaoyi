import ccxt
import time

# 初始化币安API
exchange = ccxt.binance({
    'apiKey': '',
    'secret': 'YourAPISecret',
})

# 定义策略
def simple_moving_average_strategy(symbol, timeframe, short_period, long_period):
    while True:
        try:
            # 获取K线数据
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
            closes = [data[4] for data in ohlcv]

            # 计算短期和长期移动平均
            short_ma = sum(closes[-short_period:]) / short_period
            long_ma = sum(closes[-long_period:]) / long_period

            # 获取未完成订单
            open_orders = exchange.fetch_open_orders(symbol)

            # 策略逻辑
            if short_ma > long_ma:
                if not open_orders:
                    # 实施交易逻辑（示例为市价买入）
                    buy_order = exchange.create_market_buy_order(symbol, amount=1)
                    print(f"Bought {symbol} at {buy_order['price']}")
                else:
                    print("There are open orders. Waiting for execution.")
            elif short_ma < long_ma:
                if not open_orders:
                    # 实施交易逻辑（示例为市价卖出）
                    sell_order = exchange.create_market_sell_order(symbol, amount=1)
                    print(f"Sold {symbol} at {sell_order['price']}")
                else:
                    print("There are open orders. Waiting for execution")

            # 检查并处理订单状态
            for order in open_orders:
                order_status = exchange.fetch_order(symbol, order['id'])
                if order_status['status'] == 'closed':
                    print(f"Order {order['id']} has been executed.")
                elif order_status['status'] == 'canceled':
                    print(f"Order {order['id']} has been canceled.")
                # 还可以添加其他状态的处理逻辑

            # 休眠，定期执行策略
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

# 主函数
if __name__ == '__main__':
    symbol = 'BTC/USDT'
    timeframe = '1h'
    short_period = 20
    long_period = 50

    simple_moving_average_strategy(symbol, timeframe, short_period, long_period)
