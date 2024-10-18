import json
import argparse

def load(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def gen(order_data: dict) -> str:
    customer_name = order_data['customer_name']
    items = order_data['items']

    total_sum = 0
    receipt_lines = [f"Клиент: {customer_name}\n", "Список товаров:\n"]

    for item in items:
        item_name = item['name']
        quantity = item['quantity']
        price = item['price']
        item_total = quantity * price
        total_sum += item_total

        receipt_lines.append(f"- {item_name} (x{quantity}): {price} руб. за единицу, итого: {item_total} руб.\n")

    receipt_lines.append(f"\nОбщая сумма: {total_sum} руб.\n")
    return ''.join(receipt_lines)

def sav(receipt: str, output_file: str):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(receipt)

def main():
    parser = argparse.ArgumentParser(description="Генерация чека.")
    parser.add_argument('--input-file', type=str, required=True, help='Путь к JSON-файлу.')
    parser.add_argument('--output-file', type=str, required=True, help='Путь для сохранения.')

    args = parser.parse_args()

    ord = load(args.input_file)

    rec = gen(ord)

    sav(rec, args.output_file)

    print(f"Чек сохранён в {args.output_file}")

if __name__ == "__main__":
    main()
