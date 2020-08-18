import pandas as pd 
from datetime import date
  


FOLDER ='Indian_Cities_Stateswise'
CC_EXT = '_total_confirmed_cases.csv'
RC_EXT = '_total_recovered_cases.csv'
DC_EXT = '_total_Death_toll.csv'


def notify_app_city_data(city,state):
    
    CC_PATH = FOLDER + '/' + state + '/' + state + CC_EXT
    RC_PATH = FOLDER + '/' + state + '/' + state + RC_EXT
    DC_PATH = FOLDER + '/' + state + '/' + state + DC_EXT
    
    #CC_PATH = 'Indian_Cities_Stateswise/Maharashtra/Maharashtra'
    
    
    #print(date.today())
    
    df_C = pd.read_csv(CC_PATH) 
    df_R = pd.read_csv(RC_PATH) 
    df_D = pd.read_csv(DC_PATH)
    
    # Drop State and State Code Columns
    #df_C.drop(df_C.columns[[0, 1]], axis = 1, inplace = True) 
    #df_R.drop(df_C.columns[['State', 'State Code']], axis = 1, inplace = True)
    #df_D.drop(df_C.columns[[0, 1]], axis = 1, inplace = True) 
    
    
    date_ = date.today()
    cur_date = ""
    for col_c, col_r, col_d in zip(df_C.columns, df_R.columns, df_D.columns):
        if col_c == date_ and col_r == date_ and col_d == date_:
            cur_date = date_
     
    
    if not cur_date:
        cur_date = df_C.columns[len(df_C.columns) -2]
        
    df_CC = df_C[['Cities', cur_date]]
    df_CC.rename(columns = {cur_date: 'Confirmed cases'}, inplace = True)
     
    df_RC = df_R[['Cities', cur_date]]
    df_RC.rename(columns = {cur_date: 'Recovered cases'}, inplace = True)
    
    df_DC = df_D[['Cities', cur_date]]
    df_DC.rename(columns = {cur_date: 'Death toll'}, inplace = True)
    
    
    
    merged_city_data = pd.concat((df_CC.set_index('Cities'), df_RC.set_index('Cities'), df_DC.set_index('Cities')), axis=1)
    
  
    return merged_city_data
    
