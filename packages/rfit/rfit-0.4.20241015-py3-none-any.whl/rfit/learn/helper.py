# __all__ = ('dfchk')
import pandas as pd

#%%
# Standard quick checks
def dfchk(dframe, chkNull=True, info=True, head=True, shape=True, desc=False, valCnt = False): 
  """
  some basic and common checks on dataframes. 
  Args:
      dframe (Pandas.DataFrame): pandas dataframe
      chkNull (bool): check Null option, defaults to True
      info (bool): info option, defaults to True
      head (bool): head option, defaults to True
      shape (bool): shape option, defaults to True
      desc (bool): describe option, defaults to False
      valCnt (bool): value_count option, defaults to False
  Return: None
  """
  cnt = 1
  print('\ndataframe Basic Check function -')
  
  if (chkNull):
    print(f'\n{cnt}: Null values:')
    cnt+=1
    print( dframe.isnull().sum().sort_values(ascending=False) )
  
  if (info):
    try:
      print(f'\n{cnt}: info(): ')
      cnt+=1
      print(dframe.info())
    except: pass
    
  if (desc):
    print(f'\n{cnt}: describe(): ')
    cnt+=1
    print(dframe.describe())
  
  if (head):
    print(f'\n{cnt}: head() -- ')
    cnt+=1
    print(dframe.head())

  if (shape): 
    print(f'\n{cnt}: shape: ')
    cnt+=1
    print(dframe.shape)

  if (valCnt):
    print('\nValue Counts for each feature -')
    for colname in dframe.columns :
      print(f'\n{cnt}: {colname} value_counts(): ')
      print(dframe[colname].value_counts())
      cnt +=1

# examples:
# dfchk(df, desc=True)

#%%