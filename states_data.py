import pandas as pd 
from datetime import date
  
CC_PATH = 'Indian_States/Indian_States_total_confirmed_cases.csv'
RC_PATH = 'Indian_States/Indian_States_total_recovered_cases.csv'
DC_PATH = 'Indian_States/Indian_States_total_Death_toll.csv'

#print(date.today())

df_C = pd.read_csv(CC_PATH) 
df_R = pd.read_csv(RC_PATH) 
df_D = pd.read_csv(DC_PATH)

date_ = date.today()
cur_date = ""
for col_c, col_r, col_d in zip(df_C.columns, df_R.columns, df_D.columns):
    if col_c == date_ and col_r == date_ and col_d == date_:
        cur_date = date_
 

if not cur_date:
    cur_date = df_C.columns[len(df_C.columns) -2]
    
df_CC = df_C[['State', cur_date]]
df_CC.rename(columns = {cur_date: 'Confirmed cases'}, inplace = True)
 
df_RC = df_R[['State', cur_date]]
df_RC.rename(columns = {cur_date: 'Recovered cases'}, inplace = True)

df_DC = df_D[['State', cur_date]]
df_DC.rename(columns = {cur_date: 'Death toll'}, inplace = True)



merged = pd.concat((df_CC.set_index('State'), df_RC.set_index('State'), df_DC.set_index('State')), axis=1)
