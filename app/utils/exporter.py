import pandas as pd

def export_to_csv(data:list,filename:str):
    """
    Exports list of dicts to csv
    """
    df=pd.DataFrame(data)
    file_path=f"exports/{filenam}.csv"
    df.to_csv(file_path,ibdex=False)
    return file_path

def export_to_excel(data:list,filename:str):
    """
    Exports list of dicts to Excel
    """
    df=pd.DataFrame(data)
    file_path=f"exports/{filename}.xlsx"
    df.to_excel(file_path,index=False)
    return file_path
