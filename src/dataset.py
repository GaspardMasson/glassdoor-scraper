import pandas as pd

def read_data():
    data_DA = pd.read_csv('datas/GLASSDOOR_DA_LASTMONTH.csv', encoding_errors='ignore')
    data_DE = pd.read_csv('datas/GLASSDOOR_DE_LASTMONTH.csv', encoding_errors='ignore')
    data_DS = pd.read_csv('datas/GLASSDOOR_DS_LASTMONTH.csv', encoding_errors='ignore')


    #Drop the first row
    data_DA = data_DA.drop(data_DA.index[0])
    data_DS = data_DS.drop(data_DS.index[0])

    # append the dataframes
    data = data_DA.append(data_DE, ignore_index=True)
    data = data.append(data_DS, ignore_index=True)

    return data