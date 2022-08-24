import streamlit as st
import pandas as pd
import numpy as np
import pickle 


average_salaries=pd.read_csv('average_salaries.csv')
age_dict = {'Prefer not to say':0,
             '18-24 years old':1,
             '25-34 years old':2,
             '35-44 years old':3,
             '45-54 years old':4,
             '55-64 years old':5,
             '65 years or older':6
              }
page = st.sidebar.selectbox("Explore or Predict", ("Predict", "Explore"))



def load_model():
    with open('salary_model_gb2.pkl', 'rb') as file1:
        gbmod = pickle.load(file1)
    return gbmod

gbmod = load_model()

model = gbmod["model"]



def show_predict_page():
    st.title("Developers Salary Prediction across Europe")

    st.write(""" ### Select your information """ )

    countries = (
        'Albania', 'Austria', 'Belarus', 'Belgium',
       'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus',
       'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France',
       'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy',
       'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta',
       'Monaco', 'Montenegro', 'Netherlands', 'Norway', 'Poland',
       'Portugal', 'Republic of Moldova', 'Romania', 'Russian Federation',
       'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland',
       'Ukraine', 'United Kingdom'
    )

    education = (
        'Less than a Bachelors', 
        'Bachelor’s degree', 
        'Master’s degree',
        'Post Grad'
    )

    age = ('18-24 years old','25-34 years old', '35-44 years old', '45-54 years old',
        '55-64 years old', '65 years or older',
       'Prefer not to say')

    developer_type = ('Academic Reseacher', 'Back-end Developer',
       'Data Scientist or ML Specialist', 'Data or Business Analyst',
       'Database Administrator', 'DevOps Specialist',
       'Engineer, Site Reliability', 'Engineering Manager',
       'Front-end Developer', 'Full-stack Developer', 'Game Developer',
       'Mobile Developer', 'Product Manager', 'QA tester',
       'Senior Executive', 'System Administrator')

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)
    Age = st.selectbox("Age group", age)
    dev_type = st.selectbox("Developer Type", developer_type)
    experience = st.slider("Years of experience", 0, 50, 0)
    
    ok = st.button("Calculate Salary")

    if ok:
        to_predict = pd.DataFrame(columns= ['YearsCodePro', 'DevType_Academic Reseacher',
       'DevType_Back-end Developer',
       'DevType_Data Scientist or ML Specialist',
       'DevType_Data or Business Analyst',
       'DevType_Database Administrator', 'DevType_DevOps Specialist',
       'DevType_Engineer, Site Reliability',
       'DevType_Engineering Manager', 'DevType_Front-end Developer',
       'DevType_Full-stack Developer', 'DevType_Game Developer',
       'DevType_Mobile Developer', 'DevType_Product Manager',
       'DevType_QA tester', 'DevType_Senior Executive',
       'DevType_System Administrator', 'EdLevel_Bachelor’s degree',
       'EdLevel_Less than a Bachelors', 'EdLevel_Master’s degree',
       'EdLevel_Post Grad', 'age_transformed', 'aver_count_salary'])

        
        to_predict.loc[0,f'DevType_{dev_type}'] = 1 
        to_predict.loc[0,f'EdLevel_{education}'] = 1
        if to_predict['EdLevel_Post Grad'][0]==1:
            to_predict.loc[0,"EdLevel_Master’s degree"]=1
            to_predict.loc[0,"EdLevel_Bachelor’s degree"]=1
	
        if to_predict["EdLevel_Master’s degree"][0]==1:
            to_predict.loc[0,"EdLevel_Bachelor’s degree"]=1
        to_predict.loc[0,'YearsCodePro'] =experience
        to_predict.loc[0,'age_transformed'] = age_dict[Age]
        to_predict.loc[0,'aver_count_salary'] = average_salaries[average_salaries['Country'] == country]['aver_count_salary'].values[0]
        to_predict = to_predict.fillna(0)
        
        to_predict = to_predict[['YearsCodePro', 'DevType_Academic Reseacher',
       'DevType_Back-end Developer',
       'DevType_Data Scientist or ML Specialist',
       'DevType_Data or Business Analyst',
       'DevType_Database Administrator', 'DevType_DevOps Specialist',
       'DevType_Engineer, Site Reliability',
       'DevType_Engineering Manager', 'DevType_Front-end Developer',
       'DevType_Full-stack Developer', 'DevType_Game Developer',
       'DevType_Mobile Developer', 'DevType_Product Manager',
       'DevType_QA tester', 'DevType_Senior Executive',
       'DevType_System Administrator', 'EdLevel_Bachelor’s degree',
       'EdLevel_Less than a Bachelors', 'EdLevel_Master’s degree',
       'EdLevel_Post Grad', 'age_transformed', 'aver_count_salary']]
        Xn = to_predict.to_numpy()
        salary = model.predict(Xn)
        st.subheader(f"The average estimate salary is ${salary[0]:.2f}")
        
def show_explore_page():
    st.title("Explore Developers Salaries across Europe")

    st.write("""
    ### Median Salaries by Country
    """)
    data1 = df.groupby(["Country"])["Salary"].median().sort_values(ascending=True)
    st.bar_chart(data1, height=600.9, width=60.5)
    
    st.write(""" ### Median Salary Based on Experience""")
    data= df.groupby(["YearsCodePro"])["Salary"].median().sort_values(ascending=True)
    st.line_chart(data, height=500.9, width=60.5)

    st.write(""" ### Median Salary Based on Education""")
    data4 = df.groupby(["EdLevel"])["Salary"].median().sort_values (ascending = True)
    st.bar_chart(data4, height=400.9, width=60.5)

    st.write(""" ### Median Salary Based on Developer Type""")
    data5 = df.groupby(["DevType"])["Salary"].median().sort_values (ascending = True)
    st.bar_chart(data5, height=600.9, width=60.5, use_container_width=True)

def experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)
def education (x):
    if 'Professional degree' in x or 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if  'Other doctoral degree' in x:
        return 'Post Grad'
    return 'Less than a Bachelors'
def dev_type(x):
    if 'full-stack' in x:
        return 'full-stack Developer'
    if 'back-end' in x:
        return 'back-end Developer'
    if 'front-end' in x:
        return 'front-end Developer'
    if 'mobile' in x:
        return 'Mobile Developer'
    if 'DevOps' in x: 
        return 'DevOps Specialist'
    if 'Data scientist' in x:
        return 'Data Scientist or ML Specialist'
    if 'Data engineer' in x:
        return 'Data Engineer'
    if 'analyst' in x:
        return 'Data or Business Analyst'
    if 'game' in x:
        return 'Game Developer'
    if 'QA' in x:
        return 'QA tester'
    if 'researcher' in x:
        return 'Academic Reseacher'
    if 'Senior Executive' in x:
        return 'Senior Executive'
    if 'System administrator' in x:
        return 'System Administrator'
    if 'reliability' in x:
        return 'Engineer, Site Reliability'
    if 'Product manager' in x:
        return 'Product Manager'
    if 'Database' in x:
        return 'Database Administrator'
    if 'Engineering manager' in x:
        return 'Engineering Manager'
    

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
    df = df[['EdLevel','Country', 'YearsCodePro',"Employment", 'Age','Age1stCode', 'Salary','DevType']]
    df = df[df["Employment"]== "Employed full-time"]
    df= df.dropna()
    df = df[df["Salary"] <=250000]
    df = df[df["Salary"] >= 10000]
    df = df.drop(['Age1stCode'], axis=1)
    df = df.drop("Employment", axis=1)
    df['YearsCodePro'] = df['YearsCodePro'].apply(experience)
    df["EdLevel"] = df['EdLevel'].apply(education)
    df['DevType'] = df['DevType'].apply(dev_type)
    


    return df
    




df= load_data()



if page == "Predict":
    show_predict_page()
else:
    show_explore_page()


st.write('Dataset includes information for 2021 and retrieved from stackoverflow.com')


