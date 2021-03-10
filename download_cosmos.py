import create_dataframe
import pandas

df = create_dataframe.read_from_cosmos()
df.to_json(path_or_buf='data.json')

