import argparse


def calc_profit(revenue, costs):
    return revenue - costs


def calc_roi(revenue, costs):
    return (calc_profit(revenue, costs) / costs) * 100

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--revenue',
        action='store',
        type=float,
        required=True,
    )

    parser.add_argument(
        '--costs',
        action='store',
        type=float,
        required=True,
    )

    args = parser.parse_args()

    print(f'Чистая прибыль: {calc_profit(args.revenue, args.costs)} руб.')
    print(f'ROI: {calc_roi(args.revenue, args.costs)}%')

if __name__== '__main__':
    main()