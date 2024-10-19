import argparse

parser = argparse.ArgumentParser()


def calc_income(revenue, costs):
    return revenue - costs

def calc_roi(revenue, costs):
    return (revenue / costs) * 100


def main():
    parser.add_argument(
        '--costs',
        action='store',
        type=float,
        required=True
    )

    parser.add_argument(
        '--revenue',
        action='store',
        type=float,
        required=True
    )

    args = parser.parse_args()

    print(f'Чистая прибыль = {calc_income(args.revenue, args.costs):.3f}')
    print(f'ROI = {calc_roi(args.revenue, args.costs):.3f}%')

