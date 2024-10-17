import argparse

def main():
    parser = argparse.ArgumentParser(description="Расчет финансовых показателей")
    parser.add_argument('--revenue',type=int, help="Доходы")
    parser.add_argument('--costs',type=int, help="Расходы")

    args = parser.parse_args()

    if args.revenue and args.costs:
        profit = args.revenue - args.costs
        roi = (profit / args.costs)*100
        print(f"Чистая прибыль: {profit} руб.\nROI: {roi}%")
if __name__ == '__main__':
    main()