import pandas as pd
import re

import logging
logging.basicConfig(level=logging.DEBUG)

# 
def get_data(filename: str, sep: str = ";", header=None) -> pd.DataFrame:
    return pd.read_csv(filename, sep=sep, encoding="iso-8859-1")

def safe_split(x):
    parts = re.split(r"-|A|B", x)
    return (parts[0] if len(parts) > 0 else "", parts[1] if len(parts) > 1 else "")

# this function return dataFrame from Lagerspiegel_full.txt
def get_regal_data() -> pd.DataFrame:
    df_regal = get_data("./uploads/Lagerspiegel_full.txt", sep=";")
    exclude_patterns = "leer|empty|n/a"
    df_regal_clean = df_regal[~df_regal["Artikel"].str.contains(exclude_patterns, na=False, case=False)].copy()
    df_regal_clean[["artikel_split", "artikel_split_2"]] = df_regal_clean["Artikel"].apply(
        lambda x: safe_split(x) 
    ).apply(pd.Series)
    df_regal_clean = df_regal_clean[["Artikel", "artikel_split" , "artikel_split_2", "Menge", "FachName"]]
    return df_regal_clean

# this function return dataFrame from P4Xe.txt

def get_job_data() -> pd.DataFrame:
    df_work = pd.read_csv("./uploads/P4Xe.txt", sep="\t", encoding="iso-8859-1", header=None)
    m_df_clean = df_work[[1,2,4,5,10,27,21,22,23]].copy()
    m_df_clean.columns = ['artikel', 'description', 'menge', 'datum', 'note', 'time_work', 'w', 'h', 'w2']
    m_df_clean['time_work'] = m_df_clean['time_work'].str.replace(',', '.', regex=False)
    m_df_clean['time_work'] = pd.to_numeric(m_df_clean['time_work'], errors='coerce')
    m_df_clean['time_work'] = (m_df_clean['time_work'] / 60).round(2)
    m_df_clean[["artikel_split", "artikel_split_2"]] = m_df_clean["artikel"].apply(
        lambda x: safe_split(x)).apply(pd.Series)
    return m_df_clean

def merge_data(df_regal = get_regal_data(), df_job = get_job_data()) -> pd.DataFrame:
    merged_df = pd.merge(df_job,df_regal, on='artikel_split', how='left')
    merged_df['note'] = merged_df['note'].fillna('')
    # merged_df.sort_values(by='datum', inplace=True)
    merged_df.to_csv('./uploads/merged_data.csv', index=False, sep=';')
    return merged_df


#  responce data for stations
def get_stations() -> list:
    df = get_regal_data()
    filter_condition = df['FachName'].str.contains(r'Station 0[1-9]|Station 1[0-2]')
    sorted_df = df[filter_condition][["Artikel", "Menge", "FachName"]].sort_values(by='FachName')
    result = (
        sorted_df.groupby('FachName', as_index=False)  
        .agg(list) 
    )
    response = [
        {
            "Station": row.FachName, 
            "material": [{"artikel": artikel, "menge": menge} for artikel, menge in zip(row.Artikel, row.Menge)]
        }
        for row in result.itertuples(index=False)
    ]
    return response

def get_final_data(df: pd.DataFrame = merge_data()) -> list:
    # # Group by 'artikel'
    grouped_df = df.groupby('artikel', as_index=False)
    response = []
    filtered_materials = []
    logging.debug(f"Initial DataFrame: {df.head(10)}")
    for article, group in grouped_df:
        # logging.debug(f"Processing group for article: {article}")
        description = group['description'].iloc[0]  
        menge = group['menge'].iloc[0]
        dataWork = group['datum'].iloc[0]
        note = group['note'].iloc[0] if not pd.isna(group['note'].iloc[0]) else ""
        time_work = group['time_work'].iloc[0]
        
        # Extract materials
        materials = group[['Artikel', 'FachName', 'Menge', 'artikel_split_2_x', 'artikel_split_2_y']].copy()
        
        # Split the article number
        article_parts = re.split("-|B", article)
        
        # Filter materials based on the article parts
        if article_parts[1].isdigit():
            filtered_materials = materials[
                materials['artikel_split_2_y'].notna() &  # Ensure not NaN
                materials['artikel_split_2_y'].astype(str).str.isdigit()  # Check if digit
            ]
        else:
            filtered_materials = materials[
                materials['artikel_split_2_y'].notna() &  # Ensure not NaN
                materials['artikel_split_2_y'].astype(str).str.contains('E')  # Check if contains 'E'
            ]
        
            # Convert filtered_materials to a list of dictionaries for JSON serialization
        filtered_materials_list = filtered_materials.to_dict(orient='records')
        # Append to response
        response.append({
            "artikel": article,
            "description": description,
            "menge": int(menge),
            "dataWork": str(dataWork),  # Ensure date is serializable
            "note": note,
            "time_work": time_work,
            "materials": filtered_materials_list
        })
    
    return response

