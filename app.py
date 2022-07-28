
import streamlit as st 
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import pandas as pd 
import openpyxl
import streamlit.components.v1 as components
from streamlit_echarts import st_pyecharts
from pyecharts import options as opts
from pyecharts.charts import Bar, Line,Pie



# set app layout 
st.set_page_config(layout='wide'
                )
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)
#------Set cards style------------------
st.markdown(
    """
    <style>
    div[data-testid="metric-container"] {
    background-color: #EEFAFC;
    border: 3px solid rgba(28, 131, 225, 0.1);
    padding: 5% 5% 5% 5%;
    text-align: center;
    border-radius: 10px;
    border-color: #F0567A;
    color: #26547C;
    font-weight: bold;
    overflow-wrap: break-word;
    
    
    }
    

    /* breakline for metric text         */
    div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
    overflow-wrap: break-word;
    white-space: break-spaces;
    color: #C00000;
    font-weight: bold;
    font-size:17px;
    
    }
    h3 { 
        font-family: Quicksand ;
        font-weight : bold;
    }
    h1 { 
        font-family: Quicksand ;
        font-weight : bold;
    }
    </style>
    
    
    """
    , unsafe_allow_html=True)
#----------------------------------------------------------
#Image
st.image('2.png')
#bold line separator
st.markdown("""<hr style="height:4px;border:none;color:#C00000;background-color:#C00000;" /> """, unsafe_allow_html=True)
#title
st.markdown("<h1 style='text-align: center; font-weight:bold; color: #C00000;'> CIT Time Sheet Report - June 2022    </h1> " ,unsafe_allow_html=True)
st.write("#")
#----------------------------------------------------------
#Reading DF
@st.experimental_memo(ttl=24*60*60)
def get_df():
    df = pd.read_excel('june full.xlsx', engine='openpyxl')
    df.fillna(0,inplace=True)
    return df
df = get_df()
#----------------------------------------------------------
#Crete Metric Cards
#data----------
emp_coun = df['User'].nunique()
hour_coun = round(df['Total'].sum())
avg_hh_emp = round(hour_coun/ emp_coun) 
dep_count = df['Dept'].nunique()
#cards--------
car1, car2, car3,car4 = st.columns(4)
car1.metric(
    label = 'Total  Working Hours',
    value = hour_coun)
car2.metric(
    label = 'Total  Employees',
    value = emp_coun)
car3.metric(
    label = 'Total Departments',
    value = dep_count)
car4.metric(
    label = 'Average Working Hours for Employee',
    value = avg_hh_emp)
# Radio Buttons style
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;border:2px solid #C00000;border-radius:10px} </style>', unsafe_allow_html=True)
st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:20px;font-size:19px;color:#000;}</style>', unsafe_allow_html=True)

#-----Employees & Time-----------------------------------
#------Preparing Data-------------
dep_tim = df.groupby(['Dept']).sum()[['Total']].reset_index().sort_values(by=['Total'],ascending=False)
dep_tim['PCT'] = round(dep_tim['Total'] / dep_tim['Total'].sum(),2) * 100
dep_tim = dep_tim.rename(columns={'Total':'Total_Hours', 'PCT':'Hours_PCT'})
dep_tim['Total_Hours'] = dep_tim['Total_Hours'].astype(int)
dep_tim = dep_tim.round({'Hours_PCT':1})
dep_tim['Hours_PCT'] = dep_tim['Hours_PCT'].astype(str) + '%'
dep_tim = dep_tim.round({'Hours_PCT':1})
#-------
emp_dep = df.groupby(['Dept']).count()[['User']].reset_index().sort_values(by=['User'],ascending=False)
emp_dep['PCT'] = round(emp_dep['User'] / emp_dep['User'].sum(),2) * 100
emp_dep = emp_dep.rename(columns={'PCT':'User_Count_PCT', 'User':'User_count'})
emp_dep = emp_dep.round({'User_Count_PCT':1})
emp_dep['User_Count_PCT'] = emp_dep['User_Count_PCT'].astype(str) + '%'
emp_dep = emp_dep.round({'User_Count_PCT    ':1})
#-------
#------------Pie1_chart_data----------------------------
x = emp_dep['Dept'].unique().tolist() 
y = emp_dep['User_count'].values.tolist()
    
#------------------------------------------------------
data_pair = [list(z) for z in zip(x, y)]
data_pair.sort(key=lambda x: x[1])
pie1 = (
    Pie(init_opts=opts.InitOpts( width="650px", height="400px",bg_color="#f9f9f9"))
    .add("", data_pair=data_pair)
    .set_global_opts(title_opts=opts.TitleOpts(title=""))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        
    
    
    )
#------------Pie2_chart_data----------------------------
x = dep_tim['Dept'].unique().tolist() 
y = dep_tim['Total_Hours'].values.tolist()
    
#------------------------------------------------------
data_pair = [list(z) for z in zip(x, y)]
data_pair.sort(key=lambda x: x[1])
pie2 = (
    Pie(init_opts=opts.InitOpts( width="650px", height="400px",bg_color="#f9f9f9"))
    .add("", data_pair=data_pair)
    .set_global_opts(title_opts=opts.TitleOpts(title=""))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        
    
    
    )
#------------------------------------------------------------
d1,d2 = st.columns(2)
with d1:
    st.markdown("<h3 style='text-align: center; font-weight:bold; color: #2E2E3A;'> Employees Dis by Department  </h3> " ,unsafe_allow_html=True)

    gb = GridOptionsBuilder.from_dataframe(emp_dep)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    #gb.configure_side_bar() #Add a sidebar
    #gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
    emp_dep,
    gridOptions=gridOptions,
    data_return_mode='FILTERED', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=True,
    theme='blue', #Add theme color to the table
    enable_enterprise_modules=True,
    height=175, 
    width='100%',
    reload_data=True
)
    st_pyecharts(
    pie1, key="echarts1"
)
    
    
with d2:
    st.markdown("<h3 style='text-align: center; font-weight:bold; color: #2E2E3A;'> Time Dis by Department  </h3> " ,unsafe_allow_html=True)

    gb = GridOptionsBuilder.from_dataframe(dep_tim)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    #gb.configure_side_bar() #Add a sidebar
    #gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
    dep_tim,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=True,
    theme='blue', #Add theme color to the table
    enable_enterprise_modules=True,
    height=175, 
    width='100%',
    reload_data=True
)
    st_pyecharts(
    pie2, key="echarts"
)
#bold line separator
st.markdown("""<hr style="height:2px;border:none;color:#26547C;background-color:#26547C;" /> """, unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-weight:bold; color: #2E2E3A;'> Time Dis by Employee  </h3> " ,unsafe_allow_html=True)
#------Preparing Data-------------
emp_tim = df.groupby(['User','Dept']).sum()[['Total']].reset_index().sort_values(by=['Total'],ascending=False)
emp_tim['PCT'] = round(emp_tim['Total'] / emp_tim['Total'].sum(),2) * 100
emp_tim['PCT'] = emp_tim['PCT'].astype(str) + '%'
emp_tim = emp_tim.round({'PCT    ':1})
#--------------------
gb = GridOptionsBuilder.from_dataframe(emp_tim)
gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
#gb.configure_side_bar() #Add a sidebar
#gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(
emp_tim,
gridOptions=gridOptions,
data_return_mode='FILTERED', 
update_mode='MODEL_CHANGED', 
fit_columns_on_grid_load=True,
theme='blue', #Add theme color to the table
enable_enterprise_modules=True,
height=500, 
width='100%',
reload_data=True
)



#bold line separator
st.markdown("""<hr style="height:1px;border:none;color:#26547C;background-color:#26547C;" /> """, unsafe_allow_html=True)   
#-----Employees most aVG time-----------------------------------
#------Preparing Data-------------
emp_dep = emp_dep.rename(columns={'PCT':'User_Count_PCT', 'User':'User_count','Dept':'Deptt'})
all = pd.concat([dep_tim, emp_dep], axis=1)
all.drop(['Deptt'],axis=1, inplace=True)
all['Avg_User_Time'] = round(all['Total_Hours'] / all['User_count'])
all.sort_values(by=['Avg_User_Time'] , ascending = False)

st.markdown("<h3 style='text-align: center; font-weight:bold; color: #2E2E3A;'> Which Department has the most Avg Working Time for Employees? </h3> " ,unsafe_allow_html=True)

gb = GridOptionsBuilder.from_dataframe(all)
gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
#gb.configure_side_bar() #Add a sidebar
#gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(
all,
gridOptions=gridOptions,
data_return_mode='FILTERED', 
update_mode='MODEL_CHANGED', 
fit_columns_on_grid_load=True,
theme='blue', #Add theme color to the table
enable_enterprise_modules=True,
height=200, 
width='100%',
reload_data=True
)
#------------Employees most aVG time Data & Visual----------------------------
dept = all['Dept'].unique().tolist()
tot_h = all['Total_Hours'].values.tolist()
tot_em = all['User_count'].values.tolist()
tot_avg = all['Avg_User_Time'].values.tolist()
bar1 = (
    Bar(init_opts=opts.InitOpts(bg_color="#f9f9f9"))
        .add_xaxis(dept)
        .add_yaxis('Total hours',tot_h)
        .add_yaxis('User Count',tot_em)
        .add_yaxis('Avg User Time',tot_avg)
        .set_global_opts(
            title_opts=opts.TitleOpts(subtitle=''),
            toolbox_opts=opts.ToolboxOpts(),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")]
        )
        
        )
st_pyecharts(
    bar1, height=500 , 
)
