import argparse
from investhelper.proc import calculate_profit ,calculate_roi


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument( '--revenue')
    parser.add_argument('--costs')

    args = parser.parse_args()

    if args.revenue and args.costs:
        print(calculate_profit(int(args.revenue),int(args.costs)))
        print(calculate_roi(int(args.revenue),int(args.costs)))



if __name__ == '__main__':
    main()