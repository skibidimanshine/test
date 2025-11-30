import random
import sys

class Entity:
    """Базовый класс для всех существ в игре."""
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        damage = max(0, amount - self.defense)
        self.hp = max(0, self.hp - damage)
        return damage

    def basic_attack(self, target):
        """Обычная атака."""
        base_damage = random.randint(self.attack - 2, self.attack + 2)
        damage = target.take_damage(base_damage)
        return damage


class Player(Entity):
    """Игрок. Наследуется от Entity и добавляет инвентарь и опыт."""
    def __init__(self, name):
        super().__init__(name=name, hp=40, attack=8, defense=2)
        self.potions = 3
        self.exp = 0
        self.level = 1

    def heal(self):
        if self.potions <= 0:
            print("У тебя больше нет зелий!")
            return 0
        self.potions -= 1
        amount = random.randint(12, 20)
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        real_heal = self.hp - old_hp
        print(f"Ты выпил зелье и восстановил {real_heal} HP.")
        return real_heal

    def gain_exp(self, amount):
        self.exp += amount
        print(f"Ты получил {amount} опыта. Всего опыта: {self.exp}.")
        while self.exp >= self.level * 20:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 5
        self.attack += 2
        self.defense += 1
        self.hp = self.max_hp
        print(f"\n⬆ Уровень повышен! Теперь ты {self.level} уровня.")
        print(f"   Новые параметры: HP={self.max_hp}, ATK={self.attack}, DEF={self.defense}\n")


class Enemy(Entity):
    """Базовый враг. От него будем наследоваться."""
    def __init__(self, name, hp, attack, defense, exp_reward):
        super().__init__(name, hp, attack, defense)
        self.exp_reward = exp_reward

    def battle_cry(self):
        """Фраза при начале боя. Переопределяется в дочерних классах."""
        return f"{self.name} угрожающе рычит."


class Goblin(Enemy):
    def __init__(self):
        super().__init__(name="Гоблин", hp=20, attack=6, defense=1, exp_reward=10)

    def battle_cry(self):
        return f"{self.name} визжит: 'Моё золото!'"


class Orc(Enemy):
    def __init__(self):
        super().__init__(name="Орк", hp=30, attack=9, defense=3, exp_reward=18)

    def battle_cry(self):
        return f"{self.name} рычит: 'Сломаю тебя пополам!'"


class Skeleton(Enemy):
    def __init__(self):
        super().__init__(name="Скелет", hp=18, attack=7, defense=2, exp_reward=12)

    def battle_cry(self):
        return f"{self.name} беззвучно стучит костями..."

def choose_action():
    print("\nТвои действия:")
    print("1) Атаковать")
    print("2) Выпить зелье")
    print("3) Защита (временно увеличивает броню)")
    print("4) Попытаться сбежать")

    choice = input("> ").strip()
    return choice


def player_turn(player, enemy):
    choice = choose_action()

    if choice == "1":
        damage = player.basic_attack(enemy)
        print(f"Ты ударил {enemy.name} и нанёс {damage} урона.")
    elif choice == "2":
        player.heal()
    elif choice == "3":
        print("Ты становишься в защитную стойку. Твоя защита выше на этот ход.")
        player.defense += 3
        damage = enemy.basic_attack(player)
        player.defense -= 3
        print(f"{enemy.name} атакует, но ты в защите и получаешь всего {damage} урона.")
        return  # ход врага уже прошёл в этом варианте
    elif choice == "4":
        if random.random() < 0.5:
            print("Тебе удалось сбежать! 🏃")
            return "escaped"
        else:
            print("Сбежать не удалось!")
    else:
        print("Ты промедлил, ничего не сделав...")

    if enemy.is_alive():
        damage = enemy.basic_attack(player)
        print(f"{enemy.name} атакует и наносит тебе {damage} урона.")


def battle(player, enemy):
    print("\n===================================")
    print(f"⚠ На тебя напал {enemy.name}!")
    print(enemy.battle_cry())
    print("===================================\n")

    while player.is_alive() and enemy.is_alive():
        print(f"💚 Твоё HP: {player.hp}/{player.max_hp} | Зелий: {player.potions}")
        print(f"💀 {enemy.name} HP: {enemy.hp}/{enemy.max_hp}")

        result = player_turn(player, enemy)
        if result == "escaped":
            return "escaped"

        if not player.is_alive():
            print("\n☠ Ты пал в бою...")
            return "dead"
        if not enemy.is_alive():
            print(f"\n✅ Ты победил {enemy.name}!")
            player.gain_exp(enemy.exp_reward)
            # шанс получить зелье
            if random.random() < 0.3:
                player.potions += 1
                print("🎁 С противника выпало зелье лечения!")
            return "win"


def random_enemy():
    cls = random.choice([Goblin, Orc, Skeleton])
    return cls()


def explore(player):
    print("\nТы продвигаешься вперёд по туманной тропе...")
    event = random.random()

    if event < 0.5:
        enemy = random_enemy()
        result = battle(player, enemy)
        return result
    elif event < 0.8:
        print("Ты нашёл небольшой сундук. Внутри — зелье лечения!")
        player.potions += 1
    else:
        print("Тихо... никого вокруг. Можно немного передохнуть.")
        if player.hp < player.max_hp:
            heal = random.randint(3, 7)
            player.hp = min(player.max_hp, player.hp + heal)
            print(f"Ты перевёл дух и восстановил {heal} HP.")


def main():
    print("=== ТЕКСТОВОЕ RPG ===")
    name = input("Как зовут твоего героя? ").strip() or "Герой"
    player = Player(name)

    print(f"\nПривет, {player.name}! Ты просыпаешься на заброшенной дороге у входа в тёмный лес.")
    print("Твоя задача — выжить как можно дольше и стать сильнее.\n")

    while True:
        if not player.is_alive():
            print("\nИгра окончена.")
            break

        print("\nЧто будешь делать?")
        print("1) 🚶 Идти дальше")
        print("2) 📜 Посмотреть характеристики")
        print("3) 🚪 Выйти из игры")
        cmd = input("> ").strip()

        if cmd == "1":
            result = explore(player)
            if result == "dead":
                print("\nИгра окончена.")
                break
        elif cmd == "2":
            print("\n====== Твои характеристики ======")
            print(f"Имя: {player.name}")
            print(f"Уровень: {player.level}")
            print(f"HP: {player.hp}/{player.max_hp}")
            print(f"Атака: {player.attack}")
            print(f"Защита: {player.defense}")
            print(f"Опыт: {player.exp}")
            print(f"Зелья: {player.potions}")
            print("================================")
        elif cmd == "3":
            print("Пока! 👋")
            sys.exit(0)
        else:
            print("Не понял команду, попробуй ещё раз.")


if __name__ == "__main__":
    main()
