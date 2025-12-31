import os
import random
import sys
import json
import time

# Завантаження статистики з файлу якщо існує   
def load_stats():
    if os.path.exists("stats.json"):
            with open("stats.json", "r", encoding="utf-8") as f:
                return json.load(f)
    return {"total_wins": 0, "total_losses": 0, "total_draws": 0}

# Збереження статистики у файл
def save_stats(stats):
    with open("stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=4)

# Головний клас гри
class Game:
    def __init__(self):
        # Ініціалізація (запуск при створенні об'єкта)
        self.total_stats = load_stats()  # Загальна статистика з файлу
        self.session_stats = {"wins": 0, "losses": 0, "draws": 0}  # Статистика поточної сесії
        self.choices_map = {1: "Ножниці", 2: "Камінь", 3: "Папір"}  # Мапа вибору гравця

    def clear_screen(self):
        # Очищення консолі від зайвого тексту
        os.system('cls||clear')

    def save_progress(self):
        # Зберігає прогрес у файл
        save_stats(self.total_stats)

    def get_player_choice(self):
        # Отримання вибору гравця з перевіркою введення
        while True:
            print("\n1. Ножниці | 2. Камінь | 3. Папір")
            try:
                choice = int(input("Ваш вибір >> "))
                if choice in self.choices_map:
                    return choice
                print("Оберіть від 1 до 3!")
            except ValueError:
                # Обробка помилки введення
                print("Введіть число!")


# Визначення переможця
    def determine_winner(self, p, c):
        if p == c: return "draw"
        if (p == 2 and c == 1) or (p == 3 and c == 2) or (p == 1 and c == 3):
            return "player"
        return "computer"


# Функції оновлення статистики
    def update_stats(self, result):
        if result == "draw":
            self.session_stats["draws"] += 1
            self.total_stats["total_draws"] += 1
            print("Нічия!")
        elif result == "player":
            self.session_stats["wins"] += 1
            self.total_stats["total_wins"] += 1
            print("Ви перемогли!")
        else:
            self.session_stats["losses"] += 1
            self.total_stats["total_losses"] += 1
            print("Поразка!")
        
        self.save_progress()

    # РЕЖИМИ ГРИ 

    def mode_classic(self):
        # Класичний режим: один раунд
        self.clear_screen()
        print("=== КЛАСИЧНИЙ РЕЖИМ ===")
        player = self.get_player_choice()
        computer = random.randint(1, 3)
        
        print(f"Ви: {self.choices_map[player]} VS Комп'ютер: {self.choices_map[computer]}")
        res = self.determine_winner(player, computer)
        self.update_stats(res)
        input("\nНатисніть Enter...")

    def mode_tournament(self):
        # Турнірний режим:
        self.clear_screen()
        try:
            limit = int(input("Турнір до скількох перемог? >> "))
        except ValueError: limit = 3
        
        p_score = 0
        c_score = 0
        
        while p_score < limit and c_score < limit:
            self.clear_screen()
            print(f"ТУРНІР ({p_score}:{c_score}) | Ціль: {limit}")
            player = self.get_player_choice()
            computer = random.randint(1, 3)
            
            res = self.determine_winner(player, computer)
            if res == "player": 
                p_score += 1
                print(f"Комп'ютер: {self.choices_map[computer]}")
                print(">>> Ви взяли раунд!")
                time.sleep(1)
            elif res == "computer": 
                c_score += 1
                print(f"Комп'ютер: {self.choices_map[computer]}")
                print(">>> Комп'ютер взяв раунд!")
                time.sleep(1)
            else: 
                print(">>> Нічия!")
            time.sleep(1)

        print("\n--- РЕЗУЛЬТАТ ТУРНІРУ ---")
        if p_score == limit:
            self.update_stats("player")
        else:
            self.update_stats("computer")
        input("\nНатисніть Enter...")
    
    def menu_battle(self):
        # Меню режиму битви
        self.clear_screen()
        print("""=== РЕЖИМ БИТВА ===
В цьому режимі генерується шлях розміром від 20 до 100 км.
Один кілометр проходиться за 0.3 секунди, в випадковому місці може бути засідка(битва) в якій на реакцію треба перемогти комп'ютера.
Час щоб зробити хід 5 секунд, якщо ви не встигните зробити хід або зробите не правильний вибір у вас забереться 1 життя. 
Подорожуйте шляхом з випадковими боями.
У вас є 3 життя. Виживіть до кінця шляху!""")
        input("Натисніть Enter, щоб почати...")
        self.mode_battle()

    def mode_battle(self):
        # Режим битви
        path_len = random.randint(20, 100) # Генерація довжини шляху
        num_battles = max(1, int(path_len * 0.1)) # Кількість засідок (битв)
        battle_spots = set(random.sample(range(1, path_len), num_battles)) # Випадкові позиції засідок
        
        self.clear_screen()
        print(f"Генерація шляху: {path_len} км. Засідок: {num_battles}")
        time.sleep(1.5)
        
        hp = 3
        
        for i in range(path_len + 1):
            self.clear_screen()
            path_str = "[" + "-" * i + "*" + "-" * (path_len - i) + "]"
            print(f"РЕЖИМ БИТВА | Життя: {'♥'*hp}\nШлях: {path_str}")
            
            if i in battle_spots:
                print("\n!!! ЗАСІДКА !!!")
                time.sleep(2)
                
                # Режим бою
                comp_move = random.randint(1, 3)
                print(f"Ворог атакує: >> {self.choices_map[comp_move].upper()} <<")
                print("ЩО ЙОГО Б'Є? (1-3)")
                print("\n1. Ножниці | 2. Камінь | 3. Папір")
                
                start_t = time.time()
                try:
                    p_move = int(input(">> "))
                    elapsed = time.time() - start_t
                except ValueError:
                    p_move = 0; elapsed = 999
                
                # Логіка урону
                success = False
                if elapsed <= 4.0:
                    if self.determine_winner(p_move, comp_move) == "player":
                        print("Успішний блок!")
                        success = True
                
                if not success:
                    print("ПОРАНЕННЯ! (-1 життя)")
                    hp -= 1
                    time.sleep(1)
                
                if hp <= 0:
                    print("\nВИ ЗАГИНУЛИ...")
                    self.update_stats("computer")
                    input("Enter..."); return

                time.sleep(1)
            else:
                time.sleep(0.3) # Швидкість ходьби

        print("\nШЛЯХ ПРОЙДЕНО!")
        self.update_stats("player")
        input("Enter...")

    def menu(self):
        # Головне меню гри
        while True:
            self.clear_screen()
            print("1. Нова гра\n2. Інформація\n3. Рахунок\n4. Вихід")
            m = input(">>>> ")
            
            if m == "1":
                self.clear_screen()
                print("1. Класика\n2. Турнір\n3. Битва")
                mode = input(">>>> ")
                if mode == "1": self.mode_classic()
                elif mode == "2": self.mode_tournament()
                elif mode == "3": self.menu_battle()
            elif m == "2":
                self.clear_screen()
                print("Dev: Лихач Дмитро Михайлович\nГрупа: ПРМ-11")
                input("Назад...")
            elif m == "3":
                self.clear_screen()
                print(f'СЕСІЯ: {self.session_stats["draws"]} нічиї, {self.session_stats["wins"]} перемог, {self.session_stats["losses"]} поразок')
                print(f'ЗАГАЛОМ: {self.total_stats["total_draws"]} нічиї, {self.total_stats["total_wins"]} перемог, {self.total_stats["total_losses"]} поразок')
                input("Назад...")
            elif m == "4":
                sys.exit()

# Запуск програми
if __name__ == "__main__":
    Game().menu()