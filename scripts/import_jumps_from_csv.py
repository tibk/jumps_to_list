import argparse
import csv

if __name__=='__main__':
    main()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help='/home/thibaultk/Sauts.csv')
    parser.add_argument('dsn', help='host=localhost dbname=base_statistics user=tkarrer')
    args = parser.parse_args()

    insert_jumps(args.file_path, args.dsn)

def insert_jumps(file_path, dsn):
    with open(file_path, 'r') as f:
        pass
