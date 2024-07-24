from random import randint, choice
from abc import ABC, abstractmethod


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'({self.x}, {self.y})'


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return f'Вы пытаетесь выстрелить за доску'


class BoardUsedException(BoardException):
    def __str__(self):
        return f'Вы уже стреляли в эту точку'


class BoardWrongShipException(BoardException):
    pass


class Ship:
    def __init__(self, bow: Dot, length: int, orientation: int):
        self.bow = bow
        self.length = length
        self.orientation = orientation
        self.lives = length

        self.ship_dots = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.orientation == 0:
                cur_x += i
            elif self.orientation == 1:
                cur_y += i
            self.ship_dots.append(Dot(cur_x, cur_y))

    @property
    def dots(self):
        return self.ship_dots


class Board:
    def __init__(self, hid: bool = False, size: int = 6):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [['-' for _ in range(1, size + 1)] for _ in range(1, size + 1)]
        self.busy = []
        self.ships = []

    def add_ship(self, ship: Ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            self.busy.append(d)

        self.contour(ship)
        self.ships.append(ship)

    def out(self, d: Dot):
        return not ((0 <= d.x <= self.size - 1) and (0 <= d.y <= self.size - 1))

    def contour(self, ship: Ship, verb: bool = False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = '*'
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " | "

        if self.hid:
            res = res.replace("■", "-")
        return res

    def shot(self, d: Dot):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль потоплен!")
                    return False
                else:
                    print('Корабль ранен')
                    return True
        self.field[d.x][d.y] = '*'
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []


class Player(ABC):
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    @abstractmethod
    def ask(self):
        pass

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, self.board.size - 1), randint(0, self.board.size - 1))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input('Ваш ход: ').split()

            if len(cords) != 2:
                print('Нужно ввести 2 числа!')
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Вы пытаетесь ввести не числа!")
                print('Введите числа!')
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lengths = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lengths:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, choice([1, 0]))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    @staticmethod
    def greet():
        print('        Морской бой        ')
        print('---------------------------')
        print('       Правила игры:')
        print('Для хода требуется вводить ')
        print('   координаты вида: "Х Y"  ')
        print('     через пробел ,где:    ')
        print('     X - номер строки      ')
        print('     Y - номер столбца ')
        print('  Игра заканчивается полным ')
        print('уничтожением флота противника')

    def loop(self):
        num = 0
        while True:
            print("-" * 27)
            print("Доска в кораблями игрока:")
            print(self.us.board)
            print("-" * 27)
            print("Доска противника:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 27)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 27)
                print("Ходит  'AI' !")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 27)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 27)
                print("  'AI'  выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
