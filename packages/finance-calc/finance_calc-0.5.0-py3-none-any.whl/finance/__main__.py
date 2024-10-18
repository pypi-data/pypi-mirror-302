import argparse
def calculate_profit(revenues,costs):
    return revenues - costs
def calculate_ROI(profit, costs):
    return (profit / costs) * 100
def main():
    parser = argparse.ArgumentParser(description="Расчет финансовых показателей")
    parser.add_argument('--revenue',type=int, help="Доходы")
    parser.add_argument('--costs',type=int, help="Расходы")

    args = parser.parse_args()

    if args.revenue and args.costs:
        profit = calculate_profit(args.revenue,args.costs)
        roi = calculate_ROI(profit,args.costs)
        print(f"Чистая прибыль: {profit} руб.\nROI: {roi}%")
if __name__ == '__main__':
    main()