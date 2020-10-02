import os
from pathlib import Path
import json
from pathlib import Path
import argparse
from pprint import pprint
from tabulate import tabulate

from app.db_connector import *

at_dir = Path('frontend/src')

def language_settings():
    languages = [
        'en',
        'ja'
    ]
    dictionary = {k: {} for k in languages}
    for p in (at_dir / 'lang').glob('*.csv'):
        with p.open(mode='r') as f:
            for line in f.read().split('\n')[1:]:
                keys = line.split(',')
                if len(keys) < 2:
                    continue
                for i, lang in enumerate(languages):
                    dictionary[lang].setdefault(p.stem.capitalize(), {})
                    dictionary[lang][p.stem.capitalize()][keys[0]] = keys[i + 1].replace('~', ',')
    with open(at_dir / 'lang/dictionary.json', 'w') as f:
        f.write(json.dumps(dictionary))
        pprint(dictionary)

def db_init():
    if input('Going to delete all data in DB. Are you sure what you are doing? [y/N] ') == 'y':
        print('initializing DB')
        import app.app as backapp
        from app.db_connector import Base, engine
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        backapp.signup({
            'user_name': 'pysan3',
            'user_password': '000',
            'email': 'hogehoge@test.com',
            'phone_number': '000-0000-0000',
            'nick_name': 'pysan3',
            'real_name': 'pysan3',
            'zipcode': ['000', '0000'],
            'address': ['hoge', 'fuga'],
            'ocupation': []
        })
    else:
        print('Not initializing the DB.')

def show_all_data(name:str, columns, data):
    print(name.upper())
    print(tabulate([[d[col] for col in columns] for d in data], columns, tablefmt='github'))

def find_tables():
    tables = []
    g = globals()
    names = engine.table_names()
    for t in g:
        if t.lower() in names:
            # if input(t + ' [Y/n]: ') == 'n':
            #     continue
            tables.append(g[t])
    return tables

def db_show():
    with SessionContext() as session:
        for t in find_tables():
            show_all_data(t, t.__table__.c.keys(), [DBtoDict(s) for s in session.query(t).all()])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='upload .md to your webpage')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--db', type=str, help='delete all data in DB')
    group.add_argument('-g', '--git', type=str, help='git push with [commit message]')
    parser.add_argument('-p', '--prod', action='store_true', help='npm run prod')
    parser.add_argument('-b', '--build', action='store_true', help='npm run local')
    parser.add_argument('-t', '--test', action='store_true', help='npm run dev')
    parser.add_argument('-r', '--run', action='store_true', help='python run.py')
    parser.add_argument('-l', '--lang', action='store_true', help='language json')

    args = parser.parse_args()

    if args.db:
        if args.db == 'init':
            db_init()
        elif args.db == 'show':
            db_show()
        else:
            print('Couldn\'t find a corresponding command')
            print('init\tclear all data in DB')
            print('show\tshow all data in DB')

    if args.lang:
        language_settings()

    if args.build:
        os.system('cd frontend; npm run local')
    if args.prod:
        os.system('cd frontend; npm run prod')
    if args.test:
        os.system('cd frontend; npm run dev')
    if args.run:
        os.system('python run.py')

    if args.git:
        os.system('git add .')
        os.system(f'git commit -m "{args.git}"')
        os.system('git push origin master')
