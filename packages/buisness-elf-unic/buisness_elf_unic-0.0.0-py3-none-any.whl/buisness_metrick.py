import argparse

def culc_income(revenu, costs):
    return revenu - costs


def culc_roi(revenu, costs):
    return 100 * ((revenu - costs) / costs)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--revenu',
        type=float,
        action='store',
        required=True
    )
    parser.add_argument(
        '--costs',
        type=float,
        action='store',
        required=True
    )
    args = parser.parse_args()
    print(culc_income(args.revenu, args.costs))
    print(culc_roi(args.revenu, args.costs))

if __name__ == '__main__':
    main()