import streamlit as st
import ccxt
import sqlite3
import config
import time

exchange = ccxt.binance({
    "apiKey": config.api_key, #st.session_state['api_key'],
   "secret":config.api_secret, #st.session_state['secret'],
   "enableRateLimit": True,
})

tickers= ['USDT','BTC', 'LTC', 'ETH', 'NEO', 'BNB', 'QTUM', 'EOS', 'BNT', 'DNT', 'ZRX', 'OMG', 'WTC', 'LRC', 'TRX', 'FUN', 'KNC', 'XVG', 'IOTA', 'LINK', 'CVC', 'REP', 'MTL', 'NULS', 'STX', 'ADX', 'ETC', 'ZEC', 'BAT', 'DASH', 'POWR', 'BTG', 'REQ', 'XMR', 'ENJ', 'XRP', 'STORJ', 'KMD', 'DATA', 'MANA', 'BTS', 'LSK', 'ADA', 'XLM', 'WAVES', 'GTO', 'ICX', 'ELF', 'AION', 'RLC', 'IOST', 'STEEM', 'BLZ', 'SYS', 'ONT', 'ZIL', 'XEM', 'WAN', 'ZEN', 'THETA', 'IOTX', 'SC', 'KEY', 'MFT', 'DENT', 'ARDR', 'HOT', 'VET', 'DOCK', 'POLY', 'VTHO', 'ONG', 'RVN', 'DCR', 'MITH', 'REN', 'FET', 'TFUEL', 'CELR', 'MATIC', 'ATOM', 'ONE', 'FTM', 'CHZ', 'COS', 'ALGO', 'DOGE', 'DUSK', 'ANKR', 'WIN', 'COCOS', 'PERL', 'TOMO', 'BAND', 'BEAM', 'HBAR', 'XTZ', 'DGB', 'NKN', 'GBP', 'EUR', 'KAVA', 'ARPA', 'CTXC', 'BCH', 'TROY', 'VITE', 'FTT', 'AUD', 'OGN', 'DREP', 'TCT', 'WRX', 'LTO', 'MBL', 'COTI', 'HIVE', 'STPT', 'SOL', 'CTSI', 'CHR', 'HNT', 'JST', 'FIO', 'STMX', 'MDT', 'PNT', 'COMP', 'IRIS', 'MKR', 'SXP', 'SNX', 'DOT', 'RUNE', 'AVA', 'BAL', 'YFI', 'SRM', 'ANT', 'CRV', 'SAND', 'OCEAN', 'NMR', 'LUNA', 'IDEX', 'RSR', 'PAXG', 'WNXM', 'TRB', 'EGLD', 'KSM', 'SUSHI', 'YFII', 'DIA', 'BEL', 'UMA', 'NBS', 'WING', 'UNI', 'OXT', 'SUN', 'AVAX', 'BURGER', 'BAKE', 'FLM', 'SCRT', 'XVS', 'CAKE', 'ALPHA', 'ORN', 'UTK', 'NEAR', 'VIDT', 'AAVE', 'FIL', 'INJ', 'CTK', 'AUDIO', 'AXS', 'AKRO', 'HARD', 'KP3R', 'SLP', 'STRAX', 'UNFI', 'CVP', 'FOR', 'FRONT', 'ROSE', 'MDX', 'SKL', 'GHST', 'DF', 'JUV', 'PSG', 'GRT', 'CELO', 'TWT', 'REEF', 'OG', 'ATM', 'ASR', '1INCH', 'RIF', 'BTCST', 'TRU', 'DEXE', 'CKB', 'FIRO', 'LIT', 'SFP', 'FXS', 'DODO', 'AUCTION', 'ACM', 'PHA', 'TVK', 'BADGER', 'FIS', 'QI', 'OM', 'POND', 'ALICE', 'DEGO', 'BIFI', 'LINA', 'PERP', 'RAMP', 'SUPER', 'CFX', 'TKO', 'AUTO', 'EPS', 'PUNDIX', 'TLM', 'MIR', 'BAR', 'FORTH', 'AR', 'ICP', 'SHIB', 'POLS', 'MASK', 'LPT', 'ATA', 'GTC', 'KLAY', 'TORN', 'ERN', 'BOND', 'MLN', 'C98', 'FLOW', 'QUICK', 'RAY', 'MINA', 'QNT', 'CLV', 'XEC', 'ALPACA', 'FARM', 'VGX', 'MBOX', 'WAXP', 'TRIBE', 'GNO', 'DYDX', 'GALA', 'ILV', 'YGG', 'FIDA', 'AGLD', 'BETA', 'RAD', 'RARE', 'LAZIO', 'MOVR', 'CHESS', 'DAR', 'ACA', 'ASTR', 'BNX', 'CITY', 'ENS', 'PORTO', 'JASMY', 'AMP', 'PLA', 'PYR', 'SANTOS', 'RNDR', 'ALCX', 'MC', 'VOXEL', 'BICO', 'FLUX', 'UST', 'HIGH', 'OOKI', 'CVX', 'PEOPLE', 'SPELL', 'JOE', 'GLMR', 'ACH', 'IMX', 'LOKA', 'BTTC', 'ANC', 'API3', 'XNO', 'WOO', 'ALPINE', 'T', 'NBT', 'KDA', 'APE', 'GMT', 'BSW', 'MULTI']

############
# BUY MODE #
############

def get_balance(tickers):
    try:
        balance_dirty = exchange.fetch_balance()['info']['balances']
    except Exception as e:
        return e
    balance_clean=[]
    for b in balance_dirty:
        if b['asset'] in tickers:
            balance_clean.append(b)
    return balance_clean

balance= get_balance(tickers)

def get_last_price(symbol):
    if symbol != "USDT":
        try:
            last_price = exchange.fetch_ticker(symbol+'/USDT')['last']
            return last_price
        except Exception as e:
            print(e)
    else:
        return 1

def create_table():
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS symbols(symbol TEXT, costed REAL, volume_in_wallet REAL, last_price REAL)")
        con.commit()

def update_table():
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        for pair in balance:
            last_price = get_last_price(pair['asset'])
            cur.execute("INSERT INTO symbols(symbol, costed, volume_in_wallet, last_price) VALUES (?,?,?,?)", (pair['asset'],0,pair['free'],last_price))
            con.commit()

def get_all_symbols():
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("SELECT symbol FROM symbols")
        data = [x[0] for x in cur.fetchall() if x[0] != "USDT"]
        return data

# def get_selected_symbols(position):
#     with sqlite3.connect("data.db") as con:
#         cur = con.cursor()
#         cur.execute(f"SELECT symbol FROM symbols WHERE selected_{position} = 1")
#         data = [x[0] for x in cur.fetchall() if x[0] != "USDT"]
#         return data

# def check_if_selected(symbol,position):
#     with sqlite3.connect("data.db") as con:
#         cur = con.cursor()
#         cur.execute(f"SELECT selected_{position} FROM symbols WHERE symbol = '{symbol}'")
#         data = cur.fetchall()[0][0]
#         if data == 0:
#             return False
#         else:
#             return True

# def update_selected_symbol(symbol,position):
#     with sqlite3.connect("data.db") as con:
#         cur = con.cursor()
#         cur.execute(f"UPDATE symbols SET selected_{position} = CASE WHEN selected_{position} > 0 THEN 0 ELSE 1 END WHERE symbol='{symbol}'")
#         con.commit()

# def update_all_symbols(position,select):
#     with sqlite3.connect("data.db") as con:
#         cur = con.cursor()
#         if select:
#             cur.execute(f"UPDATE symbols SET selected_{position} = 1")
#         else:
#             cur.execute(f"UPDATE symbols SET selected_{position} = 0")
#         con.commit()

# def unselect_all_sell():
#     with sqlite3.connect("data.db") as con:
#         cur = con.cursor()
#         cur.execute("UPDATE symbols SET selected_sell = 0")
#         con.commit()

# def customise_all_symbols(coin_dict,position):
#     with sqlite3.connect("data.db") as con:
#         cur = con.cursor()
#         for key,value in coin_dict.items():
#             if value:
#                 cur.execute(f"UPDATE symbols SET selected_{position} = 1 WHERE symbol = '{key}'")
#             else:
#                 cur.execute(f"UPDATE symbols SET selected_{position} = 0 WHERE symbol = '{key}'")
#         con.commit()

def check_usdt_balance():
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT volume_in_wallet FROM symbols WHERE symbol = 'USDT'")
        data = cur.fetchall()[0][0]
        return data

def update_after_buy(symbol,costed,volume_in_wallet):
    print("costed",costed,"symbol",symbol,"vol",volume_in_wallet)
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(f"UPDATE symbols SET costed = costed + {costed}, volume_in_wallet = volume_in_wallet + {volume_in_wallet} WHERE symbol='{symbol}'")
        con.commit()

def create_buy_order(usdt_amount,order_coins,params):
    selected = order_coins
    if len(selected)  <= 0 :
        st.warning("Please Add coin to buy!")
    else :
        for coin in selected :
            coinusdt =coin + "/USDT"
            try:
                symbol_ticker = exchange.fetch_ticker(coinusdt)
                symbol_price=float(symbol_ticker["last"])
                if symbol_price == 0 :
                    st.warning (f"Please Remove {coin}")
                amount = usdt_amount / symbol_price
            except Exception as e:
                st.warning(f"{e}")
                pass
            
            try:
                order=exchange.create_market_order(symbol=coinusdt, side="buy", amount=amount, params=params)
                st.success(f"We bought {amount} from coin {coin}")
                update_after_buy(symbol=coin,costed=usdt_amount,volume_in_wallet=amount)
                # st.write(order)
                time.sleep(0.5)
            except Exception as e:
                st.write(f"an exception occured - {e}")


#############
# SELL MODE #
#############

def get_wallet_balance():
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM symbols WHERE costed > 0 AND symbol != 'USDT'")
        data = cur.fetchall()
        result=[]
        for x in data:
            
            result.append({
                "symbol":x[0],
                "costed":x[1],
                "volume":x[2],
                "last_price":x[3]
            })
        return result


def update_price(symbol):
    last_price = get_last_price(symbol)
    if last_price:
        with sqlite3.connect("data.db") as con:
            cur = con.cursor()
            cur.execute(f"UPDATE symbols SET last_price = {last_price} WHERE symbol = '{symbol}'")
            con.commit()

# def get_selected_symbols(position):
#     with sqlite3.connect("data.db") as con:
#         cur = con.cursor()
#         cur.execute(f"SELECT symbol FROM symbols WHERE selected_{position} = 1")
#         data = [x[0] for x in cur.fetchall() if x[0] != "USDT"]
#         return data

def update_after_sell(symbol,gained,volume_reduction):
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(f"UPDATE symbols SET costed = costed - {gained}, volume_in_wallet = volume_in_wallet - {volume_reduction} WHERE symbol='{symbol}'")
        con.commit()

def create_sell_order(percentage,options_selected,params):
    print(options_selected)
    if len(options_selected) <= 0:
        st.warning("Please Add coin to buy!")
    else :
        for selected in options_selected :
            amount = selected['volume'] * percentage/100
            symbol = selected['symbol'] +'/USDT'
            USDTgained = amount * selected['last_price']
            
            try:
                order=exchange.create_market_order(symbol=symbol, side="sell", amount=amount, params=params)
                st.success(f"We sold {percentage} from coin {symbol}")
                update_after_sell(symbol=selected['symbol'],gained=USDTgained,volume_reduction=amount)
                # st.write(order)
                time.sleep(0.5)
            except Exception as e:
                st.write(f"an exception occured - {e}")