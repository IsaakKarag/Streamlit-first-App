import streamlit as st
import pandas as pd
import numpy as np
import pickle 
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st



page = st.sidebar.selectbox("Explore or Predict", ("Predict", "Explore"))



def load_model():
    with open('salary_test.pkl', 'rb') as file:
        data = pickle.load(file)
    return data 

data = load_model()

rfr = data["model"]
le_country = data["le_country"]
le_ed = data["le_ed"]

def show_predict_page():
    st.title("Software Developer Salary Prediction in Europe")

    st.write(""" ### Select your information """ )

    countries = (
        'Slovakia', 'Netherlands', 'Russian Federation', 'Austria',
       'United Kingdom of Great Britain and Northern Ireland', 'Sweden',
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

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)

    experience = st.slider("Years of experience", 0, 50, 3)

    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[country, education, experience]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_ed.transform(X[:,1])
        X = X.astype(float)

        salary = rfr.predict(X)
        st.subheader(f"The estimate salary is ${salary[0]:.2f}")


def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write("""
    ### Stack Overflow Developer Survey 2021
    """)
    data1 = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data1)

    st.write("Mean Salary Based on Experience")
    data= df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)

    fig= plt.figure(figsize=(15,8))

    sns.barplot(x='Country', y='Salary', data=df)
    plt.suptitle('Salary per Country barplot')
    plt.xticks(rotation=90)

    st.pyplot(fig)




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
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["Employment"]== "Employed full-time"]
    df= df.dropna()
    df = df.drop("Employment", axis=1)
    df = df[df["Salary"] <=250000]
    df = df[df["Salary"] >= 10000]
    df['YearsCodePro'] = df['YearsCodePro'].apply(experience)
    df["EdLevel"] = df['EdLevel'].apply(education)
    return df 


df= load_data()

df = df[df['Country'].isin(['Slovakia', 'Netherlands','Russian Federation', 'Austria', 'United Kingdom of Great Britain and Northern Ireland',
                           'Sweden','Spain','Germany','France', 'Switzerland', 'Poland', 'Ukraine','Portugal', 'Italy', 'Bulgaria', 'Greece',
                           'Ireland','Hungary', 'Belgium','Albania','Romania','Lithuania', 'Slovenia','Croatia','Czech Republic','Denmark',
                            'Serbia','Estonia','Finland','Bosnia and Herzegovina','Norway','Belarus','Luxembourg','Malta','Cyprus',
                            'Latvia','Iceland','Republic of Moldova','Montenegro','Monaco','Liechtenstein'])]

if page == "Predict":
    show_predict_page()
else:
    show_explore_page()


st.write(" Mean Salary Based on Country")



