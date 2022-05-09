import streamlit as st 
import ccxt
# import config
from datetime import datetime
from PIL import Image

if 'buy_dict' not in st.session_state:
               st.session_state['buy_dict'] = {}
if 'sell_dict' not in st.session_state:
               st.session_state['sell_dict'] = {}


image = Image.open('logo.png')
st.set_page_config(page_title='Wholesale Crypto', page_icon = image, initial_sidebar_state = 'auto')
# #skip config
# st.session_state['api_key'] = config.api_key
# st.session_state['secret'] = config.api_secret

# st.title("Wholesale Crypto")
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

if not 'api_key' in st.session_state:
   col1, col2, col3 = st.columns(3)
   col2.image(image)

   login_form = st.form(key='login_form')
   with login_form:
      api_key = st.text_input(label="API Key", placeholder="Enter your API Key ..")
      secret = st.text_input(label="API Secret",placeholder="Enter your API Secret ..")
      
   signin = login_form.form_submit_button(label='sign in')
   if signin:
         try:
            test_exchange = ccxt.binance({
               "apiKey": api_key,
               "secret": secret,
            })
            balance = test_exchange.fetch_balance()
            if 'api_key' not in st.session_state:
               st.session_state['api_key'] = api_key
            if 'secret' not in st.session_state:
               st.session_state['secret'] = secret
               st.write('welcome back..')
         except:
            st.warning("API Key/API Secret is wrong.")

else:
   import model

   img = st.sidebar.image(image)
   Select_menu = st.sidebar.selectbox(
      "Please Select from Menu?",
      ("Buy Trade", "Sell Trade")
   )

   ###########
   test_mode = st.sidebar.checkbox("Test Mode: ",value=True)
   params = {
      "test": test_mode  # test if it"s valid, but don"t actually place it
            }


############
# BUY MODE #
############

   if Select_menu == "Buy Trade":
      st.markdown("""<style> span[data-baseweb="tag"] {background-color: white !important; color:black !important;}</style>""", unsafe_allow_html=True,)

      # Choosing coins
      all_symbols = list(set(model.get_all_symbols()))
      st.subheader("Buy Trade:")
      selection_mode = st.radio("Select your desired coins:", ('Select All', 'Unselect All'))

      if selection_mode == 'Select All':
         default_coins = all_symbols
      elif selection_mode == 'Unselect All':
         default_coins = []
      
      order_coins = st.multiselect(" ",all_symbols,default_coins)
      st.write(order_coins) 
      

      # Balance Info
      usdt_amount = st.number_input("Amount in USDT to trade for each Pair",min_value=0)
      usdt_balance=model.check_usdt_balance()
      st.text("Balance information:")
      st.caption (f"USDT Balance:  {round(usdt_balance)} ")
      st.caption (f"Number of chosen coins:  {len(order_coins)} ")
      st.caption (f"Estimated Cost of purchase order: {len(order_coins)*usdt_amount}")


      execute = st.button("Execute Orders")

      if(execute):
         model.create_buy_order(usdt_amount, order_coins, params)




#############
# SELL MODE #
#############

   if Select_menu == "Sell Trade":
      st.markdown("""<style> span[data-baseweb="tag"] {background-color: white !important; color:black !important;}</style>""", unsafe_allow_html=True,)

      st.subheader("Sell Trade:")
      def update_prices(lst):
         for x in lst:
            model.update_price(x['symbol'])

      coin_list = model.get_wallet_balance()
      print(coin_list)
      col1,col2 =st.columns(2)
      selection_mode = col1.radio("Choose your selection mode:", ('All', 'Winning Coins', 'Losing Coins'))

      if selection_mode == 'All':
         selection_list = coin_list
      elif selection_mode == 'Winning Coins':
         selection_list = [x for x in coin_list if (x['last_price']*x['volume'] - x['costed'])>0]
      else:
         selection_list = [x for x in coin_list if (x['last_price']*x['volume'] - x['costed'])<=0]

      with col2:
         nowtime = datetime.now().strftime("%H:%M:%S")
         st.text("last update: "+ nowtime)
         st.button("Update prices", on_click= update_prices(coin_list))
      
      def modify_list(x):
         if x['last_price']* x['volume'] - x['costed'] > 0:
            label = "🟢  "+ x['symbol'] + "  (+ "  + str(round(x['last_price']*x['volume'] - x['costed'],3))+" )"
         else:
            label = "🔻  "+ x['symbol'] + "  ( "  + str(round(x['last_price']*x['volume'] - x['costed'],3))+" )"
         # label=st.checkbox(label=x['symbol'])
         return label

      order_list = st.multiselect(label=" ",options=selection_list,default=selection_list, format_func=modify_list)
   

      percentage = st.slider("Percentage to sell: ", min_value=0, max_value=100, value=50, step=10)

      submit_button = st.button(label="Execute Orders")
      if submit_button:
         model.create_sell_order(percentage= percentage, options_selected= order_list, params= params)

#############
# Auto SELL #
# #############

#    if Select_menu == "Auto Sell":
#       st.subheader("Auto Sell:")

#       col1,col2 =st.columns(2)
#       mode= col1.radio("choose your auto sell mode:",("wallet total","single coins"))
#       percentage= col2.slider("Select your Minimum Percentage: ", min_value=0, max_value=20, value=2, step=1)
#       start= col1.button("start the bot")
#       stop= col2.button("stop the bot")


#       total_cost = 0
#       total_profit= 0
#       coin_list = model.get_wallet_balance()
#       for coin in coin_list:
#          cost = coin['costed']
#          profit = coin['last_price']*coin['volume'] - coin['costed']
#          total_cost += cost
#          total_profit += profit
         
