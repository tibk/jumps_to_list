import argparse
import csv

import sqlalchemy as db


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

    jumper_table = db.Table('jtl_app_jumper', metadata, autoload=True, autoload_with=engine)
    spot_table = db.Table('jtl_app_spot', metadata, autoload=True, autoload_with=engine)
    suit_table = db.Table('jtl_app_suit', metadata, autoload=True, autoload_with=engine)
    jumpkind_table = db.Table('jtl_app_jump_kind', metadata, autoload=True, autoload_with=engine)
    jump_table = db.Table('jtl_app_jump', metadata, autoload=True, autoload_with=engine)

    jumper_stmt = db.sql.expression.select([jumper_table.c.id]).where(jumper_table.c.name == jumper_name)
    jumper_id = conn.execute(jumper_stmt).fetchone().id

    for row in reader:
        try:
            spot_stmt = db.sql.expression.select([spot_table.c.id]).where(spot_table.c.name == row['Lieu'])
            spot_id = conn.execute(spot_stmt).fetchone().id
        except AttributeError:
            spot_stmt = db.sql.expression.insert(spot_table).values(name=row['Lieu'], location='France', height='100').returning(spot_table.c.id)
            spot_id = conn.execute(spot_stmt).fetchone().id

        try:
            suit_stmt = db.sql.expression.select([suit_table.c.id]).where(suit_table.c.name == row['Combi'])
            suit_id = conn.execute(suit_stmt).fetchone().id
        except AttributeError:
            suit_stmt = db.sql.expression.insert(suit_table).values(name=row['Combi'], brand='', kind='').returning(suit_table.c.id)
            suit_id = conn.execute(suit_stmt).fetchone().id

        try:
            jumpkind_stmt = db.sql.expression.select([jumpkind_table.c.id]).where(jumpkind_table.c.kind == row['Type'])
            jumpkind_id = conn.execute(jumpkind_stmt).fetchone().id
        except AttributeError:
            jumpkind_stmt = db.sql.expression.insert(jumpkind_table).values(kind=row['Type']).returning(jumpkind_table.c.id)
            jumpkind_id = conn.execute(jumpkind_stmt).fetchone().id

        jump_stmt = db.sql.expression.insert(jump_table).values(
            date=row['Date'],
            jumper_id=jumper_id,
            spot_id=spot_id,
            suit_id=suit_id,
            jump_kind_id=jumpkind_id,
            number=row['Numéro'],
            comments=row['Remarque'],
        ).returning(jump_table.c.id)
        try:
            jump_id = conn.execute(jump_stmt).fetchone().id
            jump_msg = 'Inserted jump number: {} with id: {}'.format(row['Numéro'], jump_id)
            print(jump_msg)
        except db.exc.IntegrityError as e:
            print(e)


if __name__ == '__main__':
    main()
