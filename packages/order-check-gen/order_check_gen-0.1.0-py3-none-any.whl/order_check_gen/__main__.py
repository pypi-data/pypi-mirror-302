import json
import argparse
def main():
    parser = argparse.ArgumentParser(description="Создание чека по данным о заказе")
    parser.add_argument('--input-file', help="Путь к json")
    parser.add_argument('--output-file', help="Выходной путь")
    args = parser.parse_args()

    if args.input_file and args.output_file:
        with open(args.input_file,'r',encoding='UTF-8') as file:
            data = json.loads(file.read())
        string = f"Имя клиента: {data['customer_name']}"
        for i,item in enumerate((data['items'])):
            string += f"\n{i+1}.Товар: {item['name']}; Кол-во: {item['quantity']}; Цена: {item['price']}"
        with open(args.output_file,'w',encoding='UTF-8') as file:
            file.write(string)
if __name__ == '__main__':
    main()