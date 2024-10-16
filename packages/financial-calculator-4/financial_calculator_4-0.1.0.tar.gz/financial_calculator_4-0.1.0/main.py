import json
import argparse

def load_order_data(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def generate_receipt(order_data):
    customer_name = order_data['customer_name']
    items = order_data['items']

    receipt_lines = []
    receipt_lines.append(f"Чек для клиента: {customer_name}\n")
    receipt_lines.append(f"{'Товар':<20}{'Кол-во':<10}{'Цена за ед.':<15}{'Сумма':<10}")
    receipt_lines.append('-' * 55)

    total = 0
    for item in items:
        name = item['name']
        quantity = item['quantity']
        price = item['price']
        item_total = quantity * price
        total += item_total
        receipt_lines.append(f"{name:<20}{quantity:<10}{price:<15}{item_total:<10}")

    receipt_lines.append('-' * 55)
    receipt_lines.append(f"Итого: {total:.2f} руб.")

    return '\n'.join(receipt_lines)

def save_receipt(receipt, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(receipt)

def main():
    parser = argparse.ArgumentParser(description='Генератор чека для заказа')
    parser.add_argument('--input-file', type=str, required=True, help='Путь к входному JSON-файлу с данными о заказе')
    parser.add_argument('--output-file', type=str, required=True, help='Путь к выходному текстовому файлу для сохранения чека')

    args = parser.parse_args()

    order_data = load_order_data(args.input_file)
    receipt = generate_receipt(order_data)
    save_receipt(receipt, args.output_file)

    print(f"Чек сгенерирован и сохранён в {args.output_file}")

if __name__ == '__main__':
    main()
