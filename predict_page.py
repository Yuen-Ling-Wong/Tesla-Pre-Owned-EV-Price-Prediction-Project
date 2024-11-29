import streamlit as st
import numpy as np
import pickle
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Data
df = pd.read_csv("df_good_for_models.csv")

def loaded_model():
    with open("tesla_model.pkl", "rb") as file:
        data = pickle.load(file)
    return data

data = loaded_model()

le_province = data["le_province"]
le_drivetrain = data["le_drivetrain"]
le_model = data["le_model"]
scaler = data['scaler']
rfmodel = data['model']

# Default value
unique_pr = df['province'].unique()
default_index = list(unique_pr).index('ON')

# Page Show
def show_predict_page():

    st.markdown(
    """
    <style>
    .title {
        font-size: 2.6em;       
        font-weight: bold; 
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    # Title
    st.markdown('<div class="title">Tesla Pre-Owned EV Price Prediction</div>', unsafe_allow_html=True)

    st.divider()

    st.write("""
    ### Looking to buy or sell a pre-owned Tesla?
             
    Are you considering buying a Tesla EV but worried about overpaying? Or perhaps you’re curious about how much your beloved Tesla might be worth when you decide to sell it in the future?
    
    **You’re in the right place!** 
             
    Simply provide the features of your Tesla EV, and get your estimated price now!
             
    """)

    # Part 1 - Price Calculator

    st.write(" ### Price Calculator")

    col1, col2 = st.columns(2)

    with col1:
        model = st.selectbox("Tesla Model", df['model'].unique())
    with col2:   
        drivetrain = st.selectbox("Drivetrain", df['drivetrain'].unique())

    col3, col4 = st.columns(2)

    with col3:
        province = st.selectbox("Province", df['province'].unique(),index=default_index)

    with col4:
        front_legroom = st.selectbox("Front Leg Room (mm)", (1045, 1046, 1062,1063, 1064, 1077, 1085))
    
    col5, col6 = st.columns(2)

    with col5:
        year = st.slider("Year", 2012, 2024)

    with col6:
        mileage = st.slider("Mileage(km)", 300, 304048)

    col7, col8 = st.columns(2)
    
    with col7:
        battery_charge_time = st.slider("Battery Charge Time(hr)", 9, 15)
   
    with col8:
        battery_range = st.slider("Battery Range(km)",335, 652)

    ok = st.button("Calculate Price")

    if ok: 
        X = np.array([[drivetrain, model, year, province, front_legroom, battery_charge_time, battery_range, mileage]])
        X[:,0] = le_drivetrain.transform(X[:,0])
        X[:,1] = le_model.transform(X[:,1])
        X[:,3] = le_province.transform(X[:,3])
        X = X.astype(float)
        X = scaler.transform(X)

        eprice = rfmodel.predict(X)
        eprice = np.exp(eprice)
        eprice = eprice.astype(int)
        eprice = eprice.item()

        st.subheader(f"The estimated price is $ {eprice:,.0f} CAD ")

    st.divider() 

    # Part2 - Tax Calculator
    
    st.write(" ### Tax Calculator")

    def calculate_tesla_tax(price, province, luxury_tax_applicable=True):
        """
        Calculate the total price of a pre-owned Tesla vehicle including taxes.
        
        Args:
            price (float): The base price of the Tesla vehicle.
            province (str): The province where the vehicle is being purchased.
            luxury_tax_applicable (bool): Whether to apply the luxury tax for vehicles over $100,000.

        Returns:
            dict: A dictionary containing tax breakdown and the final price.
        """
        # Tax rates
        tax_rates = {
            'AB': {'GST': 0.05},
            'BC': {'GST': 0.05, 'PST': 0.07},
            'MB': {'GST': 0.05, 'PST': 0.07},
            'NB': {'HST': 0.15},
            'NL': {'HST': 0.15},
            'NT': {'GST': 0.05},
            'NS': {'HST': 0.15},
            'NU': {'GST': 0.05},
            'ON': {'HST': 0.13},
            'PE': {'HST': 0.15},
            'QC': {'GST': 0.05, 'QST': 0.09975},
            'SK': {'GST': 0.05, 'PST': 0.06},
            'YT': {'GST': 0.05}
        }

        # Taxes for the province
        taxes = tax_rates[province]

        # Calculate base taxes
        tax_breakdown = {tax: price * rate for tax, rate in taxes.items()}
        total_tax = sum(tax_breakdown.values())

        # Check and calculate luxury tax
        luxury_tax = 0
        if luxury_tax_applicable and price > 100000:
            luxury_tax = min(0.2 * (price - 100000), 0.1 * price)
            tax_breakdown['Luxury Tax'] = luxury_tax
            total_tax += luxury_tax

        # Final price
        final_price = price + total_tax

        return {
            'Base Price': round(price, 2),
            'Taxes': {k: round(v, 2) for k, v in tax_breakdown.items()},
            'Total Tax': round(total_tax, 2),
            'Final Price': round(final_price, 2)
        }

    # User inputs
    col8, col9 = st.columns(2)

    with col8:
        price = st.number_input("Enter Tesla Vehicle Est. Price (CAD):",min_value=0.0, value=42000.0, step=1000.0)
    with col9:
        province = st.selectbox(
        "Province",
        options=[
            "AB", "BC", "MB", "NB", "NL", "NT", "NS", "NU", "ON", "PE", "QC", "SK", "YT"
        ], index=8)  # Defult as "ON"

    # Calculate and display the results
    if st.button("Calculate Tax"):
        try:
            result = calculate_tesla_tax(price, province)
            st.subheader("Tax and Price Breakdown")
            st.write(f"**Tesla EV Price**: $ {result['Base Price']:,.0f}")
            st.write(f"**Taxes**:")
            for tax, amount in result['Taxes'].items():
                st.write(f"- {tax}: $ {amount:,.0f}")
            st.write(f"**Total Tax**: $ {result['Total Tax']:,.0f}")
            st.write(f"**Final Price**: $ {result['Final Price']:,.0f}")
        except ValueError as e:
            st.error(e)

    st.divider() 

    # Part 3 - Finance Calculator

    def calculate_monthly_payment(loan_amount, down_payment, annual_interest_rate, loan_term_months):
    
        # loan amount after the down payment
        loan_amount_after_down_payment = loan_amount - down_payment
        
        # Convert annual interest rate to a monthly rate
        monthly_interest_rate = annual_interest_rate / 100 / 12
        
        # Monthly payment
        if monthly_interest_rate == 0:
            monthly_payment = loan_amount_after_down_payment / loan_term_months
        else:
            monthly_payment = loan_amount_after_down_payment * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / ((1 + monthly_interest_rate) ** loan_term_months - 1)
        
        return monthly_payment

    # Streamlit app layout
    st.write(" ### Finance Calculator ")
    # Expander for additional information
    with st.expander("Click to calculate Financing Est.", expanded=False):
    
        col10, col11 = st.columns(2)

        with col10:
            tesla_ev_price = st.number_input("Tesla EV Price (CAD):", min_value=0, value=42000, step=1000)

        with col11:
            down_payment = st.number_input("Down Payment (CAD):", min_value=7000,step=100)

        col12, col13 = st.columns(2)

        with col12:
            loan_term = st.selectbox("Term (Months):", options=[36, 48, 60, 72])

        with col13:
            interest_rate = st.number_input("APR %:", min_value=0.0, format="%.2f", value=5.46)

        # Calculate and display the estimated monthly payment
        if st.button("Calculate Mo. Payment"):
            if tesla_ev_price > 0 and down_payment >= 0 and interest_rate >= 0:
                monthly_payment = calculate_monthly_payment(tesla_ev_price, down_payment, interest_rate, loan_term)
                st.subheader(f"Est. monthly payment: ${monthly_payment:,.2f}/mo est.")
            else:
                st.error("Please enter valid values for all inputs.")
        

    # Part 4
    st.divider() 

    st.write(""" ## About the Tesla Price Prediction Tool""")

    st.write(""" 
             
    #### If you're looking for a Tesla Pre-owned EV Price Calculator
    
    We've got a reliable tool here. 
    
    Our **Tesla Pre-Owned EV Price Prediction Tool** is here to simplify the process! With just a few clicks, this user-friendly app provides clear and accurate price estimates based on real-world data and advanced machine learning.

    It can be used by anyone. Whether you’re planning your next Tesla purchase, preparing to sell, or simply exploring the EV market, this tool is designed to save you time and provide practical insights, helping you make confident decisions.
    
    
    #### How Our Tesla Price Prediction Tool Works
    
    Our app is built on an advance Machine Learnning Model - **Random Forest Model**, trained with updated real-world Tesla data from across Canada. It evaluates key factors like Tesla model, mileage, year, battery range and other specifications to deliver precise pricing insights. 

    This tool is designed to save you time and provide practical insights, whether you’re a buyer, seller, or someone curious about Tesla’s pre-owned market. No more guesswork—our app brings clear, data-driven results to support your next steps.             
    
    #### Why Choose This Tool?
    - **Time & Cost Saving:**   We understand how valuable your time is. Instead of scouring multiple websites or seeking quotes from various dealers, you can now save the hassle!
    
    - **Accurate & Reliable:**  Built on machine learning model with verified data sources and high accuracy score.
    
    - **User-Friendly Design:**  Easy to navigate for everyone, from first-time EV buyers to experienced sellers.        
    
             
    #### More about the Trends


    Visit the **Explore** page to view data and trends, learning more about how your EV features influence the price.
    """)

    



