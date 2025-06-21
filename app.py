import gradio as gr
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate_loan(loan_amount, interest_rate, emi, start_month, start_year,
                   original_loan_years, prepayment1_amt, prepayment1_month, prepayment1_year):
    
    start_date = datetime(int(start_year), int(start_month), 1)
    original_loan_months = original_loan_years * 12
    monthly_interest_rate = interest_rate / 12 / 100

    def remaining_principal(P, R, EMI, n):
        return P * (1 + R) ** n - EMI * ((1 + R) ** n - 1) / R

    def calculate_remaining_tenure(principal, R, EMI):
        if EMI <= principal * R:
            return float("inf")
        N = -np.log(1 - (principal * R / EMI)) / np.log(1 + R)
        return int(np.ceil(N))

    # Simulate till prepayment
    prepayment_date = datetime(int(prepayment1_year), int(prepayment1_month), 1)
    months_to_prepayment = (prepayment_date.year - start_date.year) * 12 + (prepayment_date.month - start_date.month)

    principal = remaining_principal(loan_amount, monthly_interest_rate, emi, months_to_prepayment)
    principal -= prepayment1_amt

    remaining_months = calculate_remaining_tenure(principal, monthly_interest_rate, emi)
    total_tenure_after_prepayment = months_to_prepayment + remaining_months
    new_closure_date = start_date + relativedelta(months=total_tenure_after_prepayment)
    original_closure_date = start_date + relativedelta(months=original_loan_months)
    months_saved = original_loan_months - total_tenure_after_prepayment

    return (f"📅 Loan Starts: {start_date.strftime('%B %Y')}\n"
            f"💰 EMI: ₹{emi:.0f}/month\n"
            f"🏦 Prepayment: ₹{prepayment1_amt:.0f} in {prepayment_date.strftime('%B %Y')}\n\n"
            f"✅ Remaining Tenure: {remaining_months} months\n"
            f"🎯 New Loan Closure: {new_closure_date.strftime('%B %Y')}\n"
            f"🎉 Tenure Saved: {months_saved} months\n"
            f"🗓️ Original Closure: {original_closure_date.strftime('%B %Y')}"
           )

iface = gr.Interface(
    fn=calculate_loan,
    inputs=[
        gr.Number(label="🏦 Loan Amount (₹)", value=5028000),
        gr.Number(label="📈 Annual Interest Rate (%)", value=8.7),
        gr.Number(label="💸 EMI (₹)", value=41200),
        gr.Number(label="📅 Loan Start Month (1-12)", value=7),
        gr.Number(label="📅 Loan Start Year", value=2023),
        gr.Number(label="📆 Original Tenure (Years)", value=25),
        gr.Number(label="💰 Prepayment Amount (₹)", value=200000),
        gr.Number(label="📅 Prepayment Month (1-12)", value=8),
        gr.Number(label="📅 Prepayment Year", value=2024),
    ],
    outputs="text",
    title="🏡 Home Loan Tenure Calculator with Prepayment",
    description="Enter your home loan details and prepayment to see how much tenure you save!"
)

iface.launch()
