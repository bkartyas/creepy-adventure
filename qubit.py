from typing import List

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vec2({}, {})'.format(self.x, self.y)

    def __add__(self, other):
        return Vec2(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vec2(self.x-other.x, self.y-other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

DIRECTION_VECTORS = {
    'UP': Vec2(-1, 0),
    'RIGHT': Vec2(0, 1),
    'DOWN': Vec2(1, 0),
    'LEFT': Vec2(0, -1),
    'STAY': Vec2(0, 0),
}

class Item:
    def __init__(self, position: Vec2):
        self.position = position

    def moveToPosition(self, table, position: Vec2):
        table.get(position).add(self)
        table.unset(self)
        self.position = position

    def isMovable(self):
        return True

    def isDeadly(self):
        return False

class Character(Item):
    def __init__(self, position: Vec2):
        super().__init__(position)

    def step(self, Table):
        pass

    def isMovable(self):
        return False

class Table:
    def __init__(self, height, width):
        self.lastColumnIndex = width - 1
        self.lastRowIndex = height - 1
        self.lines = [[Cell() for _ in range(width)] for _ in range(height)]

    def __repr__(self):
        repr = ''
        for line in self.lines:
            repr += str(line) + '\n'

        return repr

    def __getitem__(self, index):
        return self.lines[index]

    def get(self, position: Vec2):
        if self.isOffTheTable(position):
            raise IndexError()

        return self.lines[position.x][position.y]

    def cells(self):
        for line in self.lines:
            for cell in line:
                yield cell

    def isOffTheTable(self, position: Vec2):
        return position.x < 0 or position.x > self.lastRowIndex or position.y < 0 or position.y > self.lastColumnIndex

    def isEmptyStepable(self, position: Vec2):
        return not self.isOffTheTable(position) and self.isEmpty(position)

    def getMovable(self, position: Vec2):
        return self.get(position).getMovable()

    def isEmpty(self, position: Vec2):
        return self.get(position).isEmpty()

    def isFirstRow(self, position: Vec2):
        return position.x == 0

    def isFirstColumn(self, position: Vec2):
        return position.y == 0

    def isLastRow(self, position: Vec2):
        return position.x == self.lastRowIndex

    def isLastColumn(self, position: Vec2):
        return position.y == self.lastColumnIndex

    def downLeftCorner(self):
        return Vec2(self.lastRowIndex, 0)

    def upLeftCorner(self):
        return Vec2(0, 0)

    def upRightCorner(self):
        return Vec2(0, self.lastColumnIndex)

    def downRightCorner(self):
        return Vec2(self.lastRowIndex, self.lastColumnIndex)

    def set(self, item: Item):
        return self.get(item.position).add(item)

    def unset(self, item: Item):
        return self.get(item.position).remove(item)

class Cell:
    def __init__(self):
        self.items = []

    def __repr__(self):
        if self.isEmpty():
            return '_'

        repr = ''
        for character in self.items:
            repr += str(character)

        return repr

    def isEmpty(self):
        return True if len(self.items) == 0 else False

    def has(self, item: Item):
        return item in self.items

    def isDeadly(self):
        for item in self.items:
            if item.isDeadly():
                return True

        return False

    def getMovable(self):
        for item in self.items:
            if item.isMovable():
                return item

        return None

    def add(self, item: Item):
        self.items.append(item)

    def remove(self, item: Item):
        self.items.remove(item)


class Adventurer(Character):
    def __init__(self, position: Vec2):
        super().__init__(position)

    def __repr__(self):
        return 'A'

    def step(self, table: Table, direction_vector: Vec2, bring: bool):
        step_position = self.position + DIRECTION_VECTORS[direction]
        movable = table.getMovable(self.position)
        if not table.isEmptyStepable(step_position) or (bring and movable == None):
            return False

        self.moveToPosition(table, step_position)
        if movable:
            movable.moveToPosition(table, step_position)

        return True


class Ghost(Character):
    def __init__(self, position: Vec2):
        super().__init__(position)

    def __repr__(self):
        return 'G'

    def step(self, table: Table):
        step_position = self.position
        while True:
            step_vector = self.getStepVector(table, step_position)
            step_position = step_position + step_vector
            step_cell = table.get(step_position)

            if step_cell.isEmpty():
                self.moveToPosition(table, step_position)
                return

    def getStepVector(self, table: Table, position: Vec2):
        if table.isFirstRow(position) and not table.isLastColumn(position):
            return DIRECTION_VECTORS['RIGHT']
        elif table.isLastColumn(position) and not table.isLastRow(position):
            return DIRECTION_VECTORS['DOWN']
        elif table.isLastRow(position) and not table.isFirstColumn(position):
            return DIRECTION_VECTORS['LEFT']
        elif table.isFirstColumn(position) and not table.isFirstRow(position):
            return DIRECTION_VECTORS['UP']

class Spider(Character):
    def __init__(self, position: Vec2):
        super().__init__(position)

    def __repr__(self):
        return 'S'

    def isDeadly(self):
        return True

    def step(self, table: Table):
        step_position = self.getStepPosition(table)
        self.moveToPosition(table, step_position)

    def getStepPosition(self, table: Table):
        if self.position == table.upLeftCorner():
            return table.upRightCorner()
        elif self.position == table.upRightCorner():
            return table.downRightCorner()
        elif self.position == table.downRightCorner():
            return table.downLeftCorner()
        elif self.position == table.downLeftCorner():
            return table.upLeftCorner()

class Snake(Character):
    def __init__(self, position: Vec2):
        super().__init__(position)
        self.direction = DIRECTION_VECTORS['LEFT']

    def __repr__(self):
        if self.direction == DIRECTION_VECTORS['LEFT']:
            return '«'
        elif self.direction == DIRECTION_VECTORS['UP']:
            return '^'
        elif self.direction == DIRECTION_VECTORS['RIGHT']:
            return '»'
        elif self.direction == DIRECTION_VECTORS['DOWN']:
            return '.'

    def step(self, table: Table):
        step_position = self.position + self.direction

        if table.isEmptyStepable(step_position):
            self.moveToPosition(table, step_position)
            return

        self.direction = self.getNextDirection()

    def getNextDirection(self):
        if self.direction == DIRECTION_VECTORS['LEFT']:
            return DIRECTION_VECTORS['UP']
        elif self.direction == DIRECTION_VECTORS['UP']:
            return DIRECTION_VECTORS['RIGHT']
        elif self.direction == DIRECTION_VECTORS['RIGHT']:
            return DIRECTION_VECTORS['DOWN']
        elif self.direction == DIRECTION_VECTORS['DOWN']:
            return DIRECTION_VECTORS['LEFT']

class Eye(Character):
    def __init__(self, position: Vec2, snake: Snake):
        super().__init__(position)
        self.snake = snake

    def __repr__(self):
        return 'O'

    def isDeadly(self):
        return True

    def step(self, table: Table):
        step_position = self.position
        if table.isOffTheTable(step_position + self.snake.direction):
            return

        while True:
            step_position = step_position + self.snake.direction
            if table.isOffTheTable(step_position + self.snake.direction) or not table.isEmpty(step_position):
                self.moveToPosition(table, step_position)
                return


class Treasure(Item):
    def __init__(self, position: Vec2):
        super().__init__(position)

    def __repr__(self):
        return '*'


class Gamer(Adventurer):
    def __init__(self, position: Vec2):
        super().__init__(position)

    def possibleSteps(self):
        for direction in DIRECTION_VECTORS.keys():
            for bring in [False, True]:
                yield direction, bring

class Game:
    def __init__(self, table: Table, gamer: Gamer, enemies: List[Character]):
        self.table = table
        self.gamer = gamer
        self.enemies = enemies

    def isWon(self):
        return self.table.getMovable(Vec2(0, 0)) and self.table.getMovable(Vec2(1, 0))

    def isLost(self):
        for cell in self.table.cells():
            if cell.isDeadly() and cell.has(self.gamer):
                return True

        return False

    def step(self, direction: str, bring: bool):
        #print(self.gamer)
        isSuccessful = self.gamer.step(table, direction, bring)
        if not isSuccessful:
            return False
        #print(self.table)

        for enemy in self.enemies:
            #print(enemy)
            enemy.step(table)
            #print(table)

        return True


table = Table(2, 4)

gamer = Gamer(Vec2(1, 0))
ghost = Ghost(Vec2(0, 1))
snake = Snake(Vec2(1, 2))
eye = Eye(Vec2(0, 2), snake)
spider = Spider(Vec2(0, 0))

treasure1 = Treasure(Vec2(0, 3))
treasure2 = Treasure(Vec2(1, 3))

table.set(gamer)
table.set(ghost)
table.set(eye)
table.set(spider)
table.set(snake)
table.set(treasure1)
table.set(treasure2)

enemies = [ghost, eye, spider, snake]

game = Game(table, gamer, enemies)

step_index = 0
possible_steps = [(direction, bring) for direction, bring in gamer.possibleSteps()]
while True:
    print(table)

    if game.isWon() or game.isLost():
        print('END! won: {}, lost: {}'.format(game.isWon(), game.isLost()))
        print(table)
        break

    direction, bring = possible_steps[step_index]
    print('{}, {}'.format(direction, bring))
    print(game.step(direction, bring))

    step_index = step_index + 1
    if step_index == len(possible_steps):
        step_index = 0
