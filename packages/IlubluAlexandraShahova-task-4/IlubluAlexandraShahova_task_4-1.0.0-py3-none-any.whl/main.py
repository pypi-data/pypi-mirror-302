import json
import argparse

def load_order_data(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_receipt(order_data: dict) -> str:
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

def save_receipt(receipt: str, output_file: str):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(receipt)

def main():
    parser = argparse.ArgumentParser(description="Генерация чека по заказу.")
    parser.add_argument('--input-file', type=str, required=True, help='Путь к входному JSON-файлу с данными о заказе.')
    parser.add_argument('--output-file', type=str, required=True, help='Путь для сохранения текстового файла с чеком.')

    args = parser.parse_args()

    order_data = load_order_data(args.input_file)

    receipt = generate_receipt(order_data)

    save_receipt(receipt, args.output_file)

    print(f"Чек успешно сохранён в {args.output_file}")

if __name__ == "__main__":
    main()
