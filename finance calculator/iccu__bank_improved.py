# -*- coding: utf-8 -*-
"""iccu _bank_improved.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17S1GPAlZQzhixfTEn4_4ZE-_DihNtA_6
"""

import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration for ICCU Bank theme and mobile optimization
st.set_page_config(page_title="ICCU Bank Financial Calculators", page_icon="💼", layout="centered")

# Apply custom CSS for red, white, and black theme and mobile optimization
st.markdown(
    """
    <style>
    .main {
        background-color: #ffffff;
        color: #000000;
    }
    .stButton > button {
        color: #ffffff;
        background-color: #ff0000;
        border-color: #ff0000;
    }
    .stTextInput, .stNumberInput, .stSlider {
        border-color: #ff0000;
    }
    @media (max-width: 768px) {
        .main {
            padding: 0 1em;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and navigation
st.title("ICCU Bank Financial Calculators")
st.write("Plan your financial future with ICCU Bank's comprehensive calculators.")

# Sidebar for navigation
st.sidebar.title("Navigate")
calculator_type = st.sidebar.radio("Choose a Calculator", ["Retirement", "Loan", "Savings"])

if calculator_type == "Retirement":
    st.header("Retirement Calculator")

    # User inputs for the retirement calculator
    current_age = st.number_input("Current Age", min_value=18, max_value=100, value=35)
    retirement_age = st.number_input("Retirement Age", min_value=current_age, max_value=100, value=65)
    current_savings = st.number_input("Current Savings ($)", min_value=0, value=50000)
    annual_income = st.number_input("Annual Income ($)", min_value=0, value=80000)
    savings_rate = st.slider("Expected Annual Savings Rate (%)", min_value=0, max_value=100, value=15)
    annual_return = st.slider("Expected Annual Return on Investments (%)", min_value=0.0, max_value=20.0, value=6.0)
    inflation_rate = st.slider("Expected Inflation Rate (%)", min_value=0.0, max_value=10.0, value=2.0)
    desired_retirement_income = st.number_input("Desired Annual Retirement Income ($)", min_value=0, value=60000)
    years_in_retirement = st.number_input("Years in Retirement", min_value=1, max_value=50, value=25)
    social_security_income = st.number_input("Social Security or Pension Income ($)", min_value=0, value=20000)

    # Additional inputs for retirement expense breakdown
    st.subheader("Retirement Expense Breakdown")
    housing_expenses = st.number_input("Estimated Housing Expenses ($ per year)", min_value=0, value=15000)
    healthcare_expenses = st.number_input("Estimated Healthcare Expenses ($ per year)", min_value=0, value=8000)
    travel_expenses = st.number_input("Estimated Travel Expenses ($ per year)", min_value=0, value=5000)
    other_expenses = st.number_input("Other Expenses ($ per year)", min_value=0, value=10000)
    total_expenses = housing_expenses + healthcare_expenses + travel_expenses + other_expenses

    # Withdrawal strategy options
    st.subheader("Withdrawal Strategies")
    withdrawal_strategy = st.selectbox("Choose a Withdrawal Strategy", ["Fixed Percentage (e.g., 4% rule)", "Fixed Dollar Amount", "Dynamic Withdrawals Based on Portfolio Performance"])

    # Convert percentage inputs to decimals for calculations
    savings_rate /= 100
    annual_return /= 100
    inflation_rate /= 100

    # Retirement calculations
    years_until_retirement = retirement_age - current_age
    annual_savings = annual_income * savings_rate
    fv_current_savings = current_savings * ((1 + annual_return) ** years_until_retirement)
    fv_annual_contributions = annual_savings * (((1 + annual_return) ** years_until_retirement - 1) / annual_return)
    total_retirement_savings = fv_current_savings + fv_annual_contributions
    future_retirement_income = desired_retirement_income * ((1 + inflation_rate) ** years_until_retirement)
    annual_return_after_inflation = annual_return - inflation_rate
    required_fund = (total_expenses - social_security_income) / annual_return_after_inflation * \
        (1 - (1 / ((1 + annual_return_after_inflation) ** years_in_retirement)))
    shortfall_or_surplus = total_retirement_savings - required_fund

    # Visualization enhancement: Retirement savings growth over time
    st.subheader("Retirement Savings Growth Over Time")
    savings_growth = [current_savings]
    for i in range(1, years_until_retirement + 1):
        savings_growth.append(savings_growth[-1] * (1 + annual_return) + annual_savings)
    st.line_chart(savings_growth)

    # Display retirement results
    st.subheader("Retirement Results")
    st.write(f"Projected Savings at Retirement Age: ${total_retirement_savings:,.2f}")
    st.write(f"Required Retirement Fund: ${required_fund:,.2f}")
    if shortfall_or_surplus < 0:
        st.write(f"**You have a shortfall of: ${-shortfall_or_surplus:,.2f}. Consider increasing your savings rate or adjusting your retirement age or income expectations.**")
    else:
        st.write(f"**You have a surplus of: ${shortfall_or_surplus:,.2f}. You are on track for retirement!**")

elif calculator_type == "Loan":
    st.header("Loan Calculator")

    # User inputs for the loan calculator
    loan_type = st.selectbox("Select Loan Type", ["Personal Loan", "Auto Loan", "Mortgage"])
    loan_amount = st.number_input("Loan Amount ($)", min_value=0, value=10000)
    annual_interest_rate = st.slider("Annual Interest Rate (%)", min_value=0.0, max_value=30.0, value=5.0)
    loan_term_years = st.number_input("Loan Term (Years)", min_value=1, max_value=30, value=10)
    extra_payments = st.number_input("Extra Monthly Payments ($)", min_value=0, value=0)

    # Convert percentage inputs to decimals for calculations
    monthly_interest_rate = (annual_interest_rate / 100) / 12
    total_payments = loan_term_years * 12

    # Loan calculation (monthly payment)
    if monthly_interest_rate > 0:
        monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
    else:
        monthly_payment = loan_amount / total_payments

    # Calculate total cost and new loan term with extra payments
    if extra_payments > 0:
        remaining_balance = loan_amount
        months = 0
        while remaining_balance > 0:
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = monthly_payment + extra_payments - interest_payment
            remaining_balance -= principal_payment
            months += 1
        total_cost_of_loan = monthly_payment * months
    else:
        total_cost_of_loan = monthly_payment * total_payments
        months = total_payments

    # Generate amortization schedule
    st.subheader("Amortization Schedule")
    schedule = pd.DataFrame(columns=["Month", "Interest Payment", "Principal Payment", "Remaining Balance"])
    balance = loan_amount
    for month in range(1, months + 1):
        interest_payment = balance * monthly_interest_rate
        principal_payment = monthly_payment + extra_payments - interest_payment
        balance -= principal_payment
        schedule = pd.concat([schedule, pd.DataFrame([[month, interest_payment, principal_payment, balance]], columns=schedule.columns)], ignore_index=True)
    st.dataframe(schedule)

    # Display loan results
    st.subheader("Loan Results")
    st.write(f"Monthly Payment: ${monthly_payment:,.2f}")
    st.write(f"Total Cost of the Loan: ${total_cost_of_loan:,.2f}")

elif calculator_type == "Savings":
    st.header("Savings Calculator")

    # User inputs for the savings calculator
    num_accounts = st.number_input("Number of Savings Accounts", min_value=1, max_value=5, value=1)
    total_future_value = 0
    for i in range(num_accounts):
        st.subheader(f"Savings Account {i+1}")
        initial_deposit = st.number_input(f"Initial Deposit for Account {i+1} ($)", min_value=0, value=1000)
        monthly_contribution = st.number_input(f"Monthly Contribution for Account {i+1} ($)", min_value=0, value=100)
        savings_annual_return = st.slider(f"Annual Return Rate for Account {i+1} (%)", min_value=0.0, max_value=20.0, value=5.0)
        savings_years = st.number_input(f"Years to Save for Account {i+1}", min_value=1, max_value=50, value=10)
        risk_profile = st.selectbox(f"Risk Profile for Account {i+1}", ["Conservative", "Balanced", "Aggressive"])

        # Adjust return based on risk profile
        if risk_profile == "Conservative":
            adjusted_return = savings_annual_return - 1
        elif risk_profile == "Balanced":
            adjusted_return = savings_annual_return
        else:  # Aggressive
            adjusted_return = savings_annual_return + 1

        # Inflation adjustment
        inflation_adjustment = st.checkbox(f"Adjust for Inflation for Account {i+1}")
        if inflation_adjustment:
            adjusted_return -= inflation_rate

        # Convert percentage inputs to decimals for calculations
        savings_monthly_return = adjusted_return / 100 / 12
        total_months = savings_years * 12

        # Compound savings calculation
        future_value_savings = initial_deposit * ((1 + savings_monthly_return) ** total_months) + \
                               monthly_contribution * (((1 + savings_monthly_return) ** total_months - 1) / savings_monthly_return)
        total_future_value += future_value_savings
        st.write(f"Future Value of Savings for Account {i+1}: ${future_value_savings:,.2f}")

    st.subheader("Total Savings")
    st.write(f"Total Future Value of All Savings Accounts: ${total_future_value:,.2f}")

# Thank you message
st.write("Thank you for using ICCU Bank's Financial Calculators. Plan wisely for a secure financial future!")