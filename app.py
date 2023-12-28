
import pickle
import pandas as pd
import streamlit as st 
from PIL import Image
import os

# Loading the Model
pickle_in = open("RF.pkl", "rb")
classifier = pickle.load(pickle_in)

# Function to predict attrition
def predict_attrition(Age, OverTime_Yes, MonthlyIncome, TotalWorkingYears, DailyRate, HourlyRate, MonthlyRate, YearsAtCompany):
    prediction = classifier.predict([[Age, OverTime_Yes, MonthlyIncome, TotalWorkingYears, DailyRate, HourlyRate, MonthlyRate, YearsAtCompany]])
    return prediction

# Function to get prediction justification
def get_prediction_justification(prediction, years_of_experience, monthly_income, total_working_years, overtime, daily_rate, hourly_rate, monthly_rate):
    if prediction == 1:
        justification = "The model predicts that the employee is likely to be attrited. Possible reasons include:"
        justification += f"\n- The employee has {years_of_experience} years of experience, and it might be an indication of seeking new challenges or opportunities."
        justification += f"\n- The monthly income is {monthly_income}, which might be lower than industry standards, potentially leading to dissatisfaction."
        justification += f"\n- The total working years are {total_working_years}, and it could be a sign of burnout or a desire for a change."
        justification += f"\n- The employee is working overtime ({'Yes' if overtime == 1 else 'No'}), which may contribute to work-related stress and attrition."
        justification += f"\n- Other factors such as daily rate ({daily_rate}), hourly rate ({hourly_rate}), and monthly rate ({monthly_rate}) are also considered in the prediction."

    else:
        justification = "The model predicts that the employee is not likely to be attrited. Possible reasons include:"
        justification += f"\n- The employee has {years_of_experience} years of experience, indicating stability and familiarity with the company."
        justification += f"\n- The monthly income is {monthly_income}, and it aligns well with industry standards, contributing to job satisfaction."
        justification += f"\n- The total working years are {total_working_years}, showcasing a commitment to the company and potential loyalty."
        justification += f"\n- The employee is not working overtime ({'No' if overtime == 1 else 'Yes'}), which may contribute to a healthy work-life balance."
        justification += f"\n- Other features like daily rate ({daily_rate}), hourly rate ({hourly_rate}), and monthly rate ({monthly_rate}) are also considered in the prediction."

    return justification

# Function to save result to CSV file
def save_to_csv(result, justification):
    if not os.path.exists('history.csv'):
        df = pd.DataFrame(columns=['Result', 'Justification'])
    else:
        df = pd.read_csv('history.csv')

    df = df.append({'Result': 'Employee is Attrited' if result == 1 else 'Employee is Not Attrited', 'Justification': justification}, ignore_index=True)
    df.to_csv('history.csv', index=False)

# Function to display history in column 2
def display_history_col2():
    st.write("## Prediction History")
    if os.path.exists('history.csv'):
        df = pd.read_csv('history.csv')
        st.table(df)

# Function to display app
def main():
    st.set_page_config(
        page_title="Predicting Employee Attrition",
        layout="wide",
        page_icon=":bar_chart:",
        initial_sidebar_state="expanded",
    )

    # Set background image
    st.markdown(
        """
        <style>
        body {
            background-image: url("your_image_url.jpg");  /* Add the URL of your image */
            background-size: cover;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    image = Image.open('Banner.png')

    st.title("Code Rush 23 National Level Hackathon by IBM")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(image)

    with col2:
        st.markdown(
            'Our app gives the best prediction about the attrition.')
        st.markdown(
            'Among all the 3 various Algorithms **Random Forest** has the best accuracy with 84.6%.')
        st.markdown("**Team Name:** Cracking Coders from KARE")

        

    html_temp = """
    <div style="background: linear-gradient(135deg, #3494e6, #ec6ead);padding:10px">
    <h3 style="color:white;text-align:center;">Streamlit Predicting Employee Attrition ML Web App </h3>
    </div>
    <br>
    """

    st.markdown(html_temp, unsafe_allow_html=True)

    # Display history in column 2
    if st.button("Get History"):
        display_history_col2()

    with st.sidebar:
        Age = st.text_input("Age", placeholder="Enter the Age of Employee:")
        OverTime_Yes = st.text_input("OverTime_Yes", placeholder="If the Employee Works Overtime (1 or 0): ")
        MonthlyIncome = st.text_input("MonthlyIncome", placeholder="Enter the Monthly Income of the Employee:")
        TotalWorkingYears = st.text_input("TotalWorkingYears", placeholder="Enter the total Working Years of the Employee:")
        DailyRate = st.text_input("DailyRate", placeholder="Enter the Daily Working rate of the Employee:")
        HourlyRate = st.text_input("HourlyRate", placeholder="Enter the Hourly Working Rate of the Employee:")
        MonthlyRate = st.text_input("MonthlyRate", placeholder="Enter the Monthly Working Rate of the Employee:")
        YearsAtCompany = st.text_input("YearsAtCompany", placeholder="Enter the amount of years employee worked at the Company:")

        if st.button("Predict"):
            result = predict_attrition(Age, OverTime_Yes, MonthlyIncome, TotalWorkingYears, DailyRate, HourlyRate, MonthlyRate, YearsAtCompany)
            justification = get_prediction_justification(result, int(YearsAtCompany), int(MonthlyIncome), int(TotalWorkingYears), int(OverTime_Yes), int(DailyRate), int(HourlyRate), int(MonthlyRate))

            if result == 1:
                st.success('Employee is Attrinated')
            else:
                st.success('Employee is Not Attrinated')

            # Save result to CSV file
            save_to_csv(result, justification)

            st.write(justification)

if __name__ == '__main__':
    main()
