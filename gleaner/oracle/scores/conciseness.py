import pandas as pd 

def get_conciseness_from_nodes(nodes, df: pd.DataFrame):
    return len(df.columns) / len(nodes)