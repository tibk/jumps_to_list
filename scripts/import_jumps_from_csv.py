import argparse
import csv

import sqlalchemy as db
from psycopg2.errors import UniqueViolation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file_path',
        help='/home/thibaultk/Sauts.csv'
    )
    parser.add_argument(
        '--dsn',
        default='postgresql+psycopg2://tkarrer:PWD@localhost/base_statistics',
        help='postgresql+psycopg2://tkarrer:PWD@localhost/base_statistics',
        # default='host=localhost dbname=base_statistics user=tkarrer'
    )
    args = parser.parse_args()

    insert_jumps(args.file_path, args.dsn)

def insert_jumps(file_path, dsn):
    reader = csv.DictReader(
        open(file_path),
        delimiter=';',
    )

    jumper_name = 'thibaultk'
    engine = db.create_engine(dsn)
    conn = engine.connect()
    metadata = db.MetaData()

    jumper_table = db.Table('jumper', metadata, autoload=True, autoload_with=engine)
    spot_table = db.Table('spot', metadata, autoload=True, autoload_with=engine)
    suit_table = db.Table('suit', metadata, autoload=True, autoload_with=engine)
    jumpkind_table = db.Table('jump_kind', metadata, autoload=True, autoload_with=engine)
    jump_table = db.Table('jump', metadata, autoload=True, autoload_with=engine)

    jumper_stmt = db.sql.expression.select([jumper_table.c.id]).where(jumper_table.c.name == jumper_name)
    jumper_id = conn.execute(jumper_stmt).fetchone().id

    import pdb; pdb.set_trace()
    for row in reader:
        try:
            spot_stmt = db.sql.expression.select([spot_table.c.id]).where(spot_table.c.name == row['Lieu'])
            spot_id = conn.execute(spot_stmt).fetchone().id
        except:
            spot_stmt = db.sql.expression.insert(spot_table).values(name=row['Lieu'], location='France', height='100').returning(spot_table.c.id)

        suit_stmt = db.sql.expression.insert(suit_table).values(name=row['Combi'], brand='', kind='')
        jumpkind_stmt = db.sql.expression.insert(jumpkind_table).values(name=row['Type'])
        jump_stmt = db.sql.expression.insert(jump_table).values(name=row[''], jumper_id='', spot_id='', suit_id='', jump_kind_id='', comments=row['Remarque'])
        try:
            conn.execute(insert_stmt)
            print('insert: ', row['Lieu'])
        except db.exc.IntegrityError as e:
            print(e)

if __name__=='__main__':
    main()
# [('Date', '2018-04-02'),
#              ('Numéro', '1'),
#              ('Type', 'PCA'),
#              ('Combi', ''),
#              ('Lieu', 'Kanfanar Bridge '),
#              ('Remarque', '')]
