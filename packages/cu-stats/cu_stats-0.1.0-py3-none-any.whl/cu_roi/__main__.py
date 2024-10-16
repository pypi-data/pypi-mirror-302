import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--revenue", required=True, type=int)
    parser.add_argument("--costs", required=True, type=int)

    args = parser.parse_args()
    income = args.revenue - args.costs
    print(f"Чистая прибыль: {income}")
    print(f"ROI: {round(income / args.costs * 100)}%")


if __name__ == '__main__':
    main()
