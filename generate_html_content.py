
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Generate html page for transcribed audios', add_help=False)
parser.add_argument('--path-info-file', type=str, help='information for titles and links to be generated')

args = parser.parse_args()
df_data = pd.read_csv(args.path_info_file, header=0)

for i in range(len(df_data)):
    # print(df_data.loc[i, "Url_page"], df_data.loc[i, "Links"])
    print(f"<div><a href=\"{df_data.loc[i, 'Links']}\">{i+1}</a>  {df_data.loc[i, 'Titles']}  &nbsp; | <a href = \"\"> caption </a> </div>")
