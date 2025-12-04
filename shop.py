products = {
    "яблоко": 50,
    "банан": 30,
    "хлеб": 40,
    "молоко": 60
}

cart = []      
history = []   


def show_products():
    print("Магазин: Доступные товары:")
    for name, price in products.items():
        print(f"  {name} — {price} руб.")
    history.append("просмотрены товары")


def show_cart():
    if not cart:
        print("Магазин: Ваша корзина пуста.")
        history.append("показана пустая корзина")
        return

    totals = {}
    for item in cart:
        totals[item] = totals.get(item, 0) + 1

    print("Магазин: В корзине:")
    total_sum = 0
    for name, count in totals.items():
        price = products.get(name, 0)
        line_sum = price * count
        total_sum += line_sum
        if count == 1:
            print(f"  {name} — {line_sum} руб.")
        else:
            print(f"  {name} x{count} — {line_sum} руб.")

    print(f"  Общая сумма: {total_sum} руб.")
    history.append(f"показана корзина (сумма {total_sum} руб.)")


def add_to_cart(product):
    product = product.lower()
    if product in products:
        cart.append(product)
        print(f'Магазин: Товар "{product}" добавлен в корзину.')
        history.append(f'добавлен товар "{product}"')
    else:
        print(f'Магазин: Товар "{product}" не найден.')
        history.append(f'попытка добавить несуществующий товар "{product}"')


def remove_from_cart(product):
    product = product.lower()
    if product in cart:
        cart.remove(product)
        print(f'Магазин: Товар "{product}" удалён из корзины.')
        history.append(f'удалён товар "{product}"')
    else:
        print(f'Магазин: Товар "{product}" нет в корзине.')
        history.append(f'попытка удалить отсутствующий товар "{product}"')


def checkout(user_name):
    if not cart:
        print("Магазин: Корзина пуста, оформить заказ нельзя.")
        history.append("попытка оформить заказ с пустой корзиной")
        return

    total_sum = sum(products[item] for item in cart)
    print(f"Магазин: Ваш заказ оформлен! Сумма: {total_sum} руб.")
    print("         Корзина очищена.")
    history.append(f"оформлен заказ на сумму {total_sum} руб.")
    cart.clear()


def show_help():
    print("Магазин: Доступные команды:")
    print("  товары   — показать список доступных товаров с ценами")
    print("  корзина  — показать содержимое корзины и общую сумму")
    print("  добавить — добавить товар в корзину по названию")
    print("  удалить  — удалить товар из корзины")
    print("  заказать — оформить заказ и очистить корзину")
    print("  помощь   — показать список команд")
    print("  выход    — завершить работу")
    history.append("показана справка по командам")


def main():
    print("Магазин: Привет! Как тебя зовут?")
    user_name = input("Пользователь: ").strip()
    if not user_name:
        user_name = "Покупатель"

    print(f'Магазин: Привет, {user_name}! Введи "помощь", чтобы узнать команды.')

    while True:
        command = input("Пользователь: ").strip().lower()

        if command == "товары":
            show_products()
        elif command == "корзина":
            show_cart()
        elif command == "добавить":
            product = input("Введите название товара: ").strip().lower()
            add_to_cart(product)
        elif command == "удалить":
            product = input("Введите название товара для удаления: ").strip().lower()
            remove_from_cart(product)
        elif command == "заказать":
            checkout(user_name)
        elif command == "помощь":
            show_help()
        elif command == "выход":
            print(f"Магазин: Спасибо за покупку, {user_name}!")
            break
        else:
            print('Магазин: Неизвестная команда. Введи "помощь", чтобы увидеть список команд.')
            history.append(f'введена неизвестная команда "{command}"')


if __name__ == "__main__":
    main()