import argparse

def calculate_net_profit(revenue, costs):
    return revenue - costs

def calculate_roi(net_profit, costs):
    if costs == 0:
        return 0
    return (net_profit / costs) * 100

def main():
    parser = argparse.ArgumentParser(description='Расчет чистой прибыли и ROI.')
    parser.add_argument('--revenue', type=float, required=True, help='Доходы компании')
    parser.add_argument('--costs', type=float, required=True, help='Расходы компании')

    args = parser.parse_args()
    revenue = args.revenue
    costs = args.costs

    net_profit = calculate_net_profit(revenue, costs)
    roi = calculate_roi(net_profit, costs)

    print(f'Чистая прибыль: {net_profit:.2f} руб.')
    print(f'ROI: {roi:.2f}%')

if __name__ == '__main__':
    main()
