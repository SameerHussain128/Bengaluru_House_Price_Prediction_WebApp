import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load the model and columns
model = pickle.load(open('bengaluru_home_prices.pickle', 'rb'))
with open('columns.json', 'r') as f:
    import json
    data_columns = json.load(f)['data_columns']
    locations = data_columns[3:]  # Locations start after the first 3 columns

def predict_price(total_sqft, bath, bhk, location):
    # Prepare the input vector
    x = np.zeros(len(data_columns))
    x[0] = total_sqft
    x[1] = bath
    x[2] = bhk
    
    # Find location index
    if location in locations:
        loc_index = data_columns.index(location)
        x[loc_index] = 1
    
    # Predict price
    return model.predict([x])[0]

def main():
    st.set_page_config(page_title="Bengaluru House Price Predictor", page_icon="🏠")
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 30px;
    }
    .stButton>button {
        width: 100%;
        background-color: #3498db;
        color: white;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-title">Bengaluru House Price Predictor</h1>', unsafe_allow_html=True)
    
    # Input columns
    col1, col2 = st.columns(2)
    
    with col1:
        total_sqft = st.number_input('Total Square Feet', min_value=100, value=1000)
        bhk = st.number_input('Number of Bedrooms (BHK)', min_value=1, max_value=10, value=2)
    
    with col2:
        bath = st.number_input('Number of Bathrooms', min_value=1, max_value=10, value=2)
        location = st.selectbox('Location', locations)
    
    # Prediction button
    if st.button('Predict House Price'):
        try:
            price = predict_price(total_sqft, bath, bhk, location)
            st.success(f'Predicted House Price: ₹{price:,.2f} Lakhs')
        except Exception as e:
            st.error(f'An error occurred: {e}')
    
    # Developer Info
    st.markdown("---")
    st.markdown("""
    **Developed by: Mohd Sameer Hussain**
    
    **Email:** mohdsameerhussain28@gmail.com
    
    **Contact/WhatsApp:** 6303452296
    
    [LinkedIn](https://www.linkedin.com/in/mohdsameer28) | 
    [GitHub](https://github.com/SameerHussain128)
    """)

if __name__ == "__main__":
    main()