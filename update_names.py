from fbapi import fetch_user_name
import os
import re
import pandas as pd

NAME_FILE = "names_storage.json"

def main():
    ids = pd.Series(map(lambda x: re.match(r'\d+', x).group(0), os.listdir('./log/')), dtype='int64').drop_duplicates()

    if os.path.exists(NAME_FILE):
        known = pd.read_json(NAME_FILE)
    else:
        known = pd.DataFrame(columns=['id', 'name'], dtype=['int64', 'string'])

    ids = pd.DataFrame(ids).rename(columns={0: 'id'})
    unlabeled = pd.merge(ids, known, how='outer', on='id', indicator=True).query('_merge == "left_only"').drop(columns=['_merge']).reset_index()

    friends = len(unlabeled)
    
    if friends > 0:
        print('Updating', friends, 'names')
    else:
        print('All names up to date')

    for i in range(friends):
        t_id = unlabeled.loc[i, 'id']
        t_name = fetch_user_name(t_id)
        print(i + 1, "/", friends, ":", t_id, '->', t_name)
        unlabeled.loc[i, 'name'] = t_name

    all_names = unlabeled.set_index(unlabeled['index']).drop(columns=['index'])
    all_names = pd.merge(known, all_names, how='outer', on='id')
    all_names['name'] = all_names['name_x'].fillna(all_names['name_y'])
    all_names = all_names.drop(columns=['name_x', 'name_y'])

    all_names.to_json(NAME_FILE)
    
    if friends > 0:
        print('All done')

if __name__ == '__main__':
    main()