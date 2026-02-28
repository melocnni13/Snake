#Знаменитая игра под название змейка в терминале
import random
import keyboard
import time
import os

score = 0  # Счёт
len_room = 18  # Длина комнаты
height_room = 10  # Ширина комнаты
snake = [(5, 1), (5, 2), (5, 3)]  # Сама змейка
speed = 0.5  # Скорость игры
direction = 'S'  # Начальное направление змейки

#Перезапуск всех данных
def reset():
    global direction, snake, food, score, speed
    direction = 'S'
    snake = [(5, 1), (5, 2), (5, 3)]
    food = random_cor_food(snake, len_room, height_room)
    score = 0
    speed = 0.5

#Проигрыш
def over_game():
    print("Вы проиграли")
    print("Ваш счёт:", score)
    print("Продолжить (Нажмите цифру 1)")
    print("Выход из игры (Нажмите любую другую кнопку)")
    choice = input()
    if choice == "1":
        reset()
        return True
    return False

#Меню
def menu():
    print("Добро пожаловать в игру змейка!")
    print('_' * 75)
    print('Управление: W(Вверх) A(Влево) S(Вниз) D(Вправо) Q(Досрочный выход из игры)')
    print('_' * 75)
    print("Начать игру (Нажмите цифру 1)")
    print('_' * 75)
    print("Выход из игры (Нажмите любую другую кнопку)")
    choice = input()
    if choice == "1":
        reset()
        return True
    return False

#Очистка экрана
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#Проверка на столкновение со стеной
def game_over_from_fall(head, lens, height):
    x, y = head
    if x < 1 or x > lens:
        return True
    elif y < 1 or y > height:
        return True
    else:
        return False

#Проверка на столкновение с телом
def game_over_from_body(snakes, head):
    if head in snakes:
        return True
    return False

#Функция для задачи координат еде
def random_cor_food(snakes, length, height):
    foods = (random.randint(1, length), random.randint(1, height))
    if foods in snakes:
        while foods in snakes:
            foods = (random.randint(1, length), random.randint(1, height))
    return foods

#Создаём комнату
def room(snakes, foods, length, height):
    print('Счёт:', score)
    for y in range(1, height + 1):
        for x in range(1, length + 1):
            if (x, y) == snakes[-1]:  # Голова змейки
                print('\033[93m@\033[0m', end="")
            elif (x, y) in snakes:  # Туловище змейки
                print('\033[92mo\033[0m', end="")
            elif (x, y) == foods:  # Еда
                print('\033[91m*\033[0m', end="")
            else:
                print('.', end='')
        print()

food = random_cor_food(snake, len_room, height_room)  # Еда

if menu():
    # Игровой цикл
    while True:
        clear_screen()
        
        # Управление с защитой от разворота на 180°
        if keyboard.is_pressed('w') and direction != 'S':
            direction = 'W'
        elif keyboard.is_pressed('s') and direction != 'W':
            direction = 'S'
        elif keyboard.is_pressed('a') and direction != 'D':
            direction = 'A'
        elif keyboard.is_pressed('d') and direction != 'A':
            direction = 'D'
        elif keyboard.is_pressed('q'):
            break

        x_head, y_head = snake[-1]

        if direction == "W":
            new_head = (x_head, y_head - 1)
        elif direction == "A":
            new_head = (x_head - 1, y_head)
        elif direction == "S":
            new_head = (x_head, y_head + 1)
        elif direction == "D":
            new_head = (x_head + 1, y_head)

        # Случаи проигрыша
        if game_over_from_fall(new_head, len_room, height_room) or game_over_from_body(snake, new_head):
            if over_game():
                continue
            else:
                break

        # Проверка на съедение еды
        if new_head == food:
            score += 10
            if speed > 0.2:
                speed -= 0.01
            food = random_cor_food(snake, len_room, height_room)
            snake.append(new_head)
        else:
            snake.append(new_head)
            snake.pop(0)

        room(snake, food, len_room, height_room)
        time.sleep(speed)
