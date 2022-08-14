import streamlit as st
import pandas as pd
import numpy as np
import pickle 
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import seaborn as sns
import matplotlib.pyplot as plt




page = st.sidebar.selectbox("Explore or Predict", ("Predict", "Explore"))



def load_model():
    with open('salary_test_n.pkl', 'rb') as file:
        forest = pickle.load(file)
    return forest

forest = load_model()

rfr2 = forest["model"]
le_coun = forest["le_coun"]
le_ed = forest["le_ed"]
le_age = forest["le_age"]

def show_predict_page():
    st.title("Developers Salary Prediction in Europe")

    st.write(""" ### Select your information """ )

    countries = (
        'Slovakia', 'Netherlands', 'Russian Federation', 'Austria',
       'United Kingdom', 'Sweden',
       'Spain', 'Germany', 'France', 'Switzerland', 'Poland', 'Ukraine',
       'Portugal', 'Italy', 'Bulgaria', 'Greece', 'Ireland', 'Hungary',
       'Belgium', 'Albania', 'Romania', 'Lithuania', 'Slovenia',
       'Croatia', 'Czech Republic', 'Denmark', 'Serbia', 'Estonia',
       'Finland', 'Bosnia and Herzegovina', 'Norway', 'Belarus',
       'Luxembourg', 'Malta', 'Cyprus', 'Latvia', 'Iceland',
       'Republic of Moldova', 'Montenegro', 'Monaco', 'Liechtenstein'
    )

    education = (
        'Master’s degree', 
        'Bachelor’s degree', 
        'Less than a Bachelors',
       'Post Grad'
    )

    age = ( '25-34 years old', '35-44 years old', '45-54 years old',
       '18-24 years old', '55-64 years old', '65 years or older',
       'Prefer not to say', 'Under 18 years old')

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)
    Age = st.selectbox("Age group", age)

    experience = st.slider("Years of experience", 0, 50, 3)
    
    ok = st.button("Calculate Salary")

    if ok:
        X1 = np.array([[country, education, Age, experience]])
        X1[:, 0] = le_coun.transform(X1[:, 0])
        X1[:, 1] = le_ed.transform(X1[:,1])
        X1[:, 2] = le_age.transform(X1[:,2])
        X1 = X1.astype(float)

        salary = rfr2.predict(X1)
        st.subheader(f"The estimate salary is ${salary[0]:.2f}")


def show_explore_page():
    st.title("Explore Developers Salaries in Europe")

    st.write("""
    ### Mean Salaries by Country
    """)
    data1 = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data1, height=600.9, width=60.5)
    

    st.write(""" ### Mean Salary Based on Experience""")
    data= df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data, height=500.9, width=60.5)

    st.write(""" ### Mean Salary Based on Education""")
    data4 = df.groupby(["EdLevel"])["Salary"].median().sort_values (ascending = True)
    st.bar_chart(data4, height=400.9, width=60.5)

def experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)
def education (x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral degree' in x:
        return 'Post Grad'
    return 'Less than a Bachelors'
@st.cache
def load_data():
    df= pd.read_csv("survey_results_public.csv")
    df['EdLevel'].fillna('Something else', axis=0, inplace=True)
    df.drop(['US_State', 'UK_Country', 'ResponseId', 'CompTotal'], axis=1, inplace=True)
    df['Country'] = df['Country'].replace(['United Kingdom of Great Britain and Northern Ireland'], 'United Kingdom')
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df['Country'].isin(['Slovakia', 'Netherlands','Russian Federation', 'Austria', 'United Kingdom',
                           'Sweden','Spain','Germany','France', 'Switzerland', 'Poland', 'Ukraine','Portugal', 'Italy', 'Bulgaria', 'Greece',
                           'Ireland','Hungary', 'Belgium','Albania','Romania','Lithuania', 'Slovenia','Croatia','Czech Republic','Denmark',
                            'Serbia','Estonia','Finland','Bosnia and Herzegovina','Norway','Belarus','Luxembourg','Malta','Cyprus',
                            'Latvia','Iceland','Republic of Moldova','Montenegro','Monaco','Liechtenstein'])]
    df = df[['EdLevel','Country', 'YearsCodePro',"Employment", 'Age','Age1stCode', 'Salary']]
    df = df[df["Employment"]== "Employed full-time"]
    df= df.dropna()
    df = df[df["Salary"] <=250000]
    df = df[df["Salary"] >= 10000]
    df = df.drop(['Age1stCode'], axis=1)
    df = df.drop("Employment", axis=1)
    df['YearsCodePro'] = df['YearsCodePro'].apply(experience)
    df["EdLevel"] = df['EdLevel'].apply(education)
    X = df.drop("Salary", axis=1)
    y = df["Salary"]
    
    return df 


df= load_data()



if page == "Predict":
    show_predict_page()
else:
    show_explore_page()






