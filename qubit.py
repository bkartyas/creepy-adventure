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
        self.size = Vec2(height, width)
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

    def isStepOrMovable(self, position: Vec2):
        return not self.isOffTheTable(position) and self.isOnlyMovable(position)

    def getMovable(self, position: Vec2):
        return self.get(position).getMovable()

    def isEmpty(self, position: Vec2):
        return self.get(position).isEmpty()

    def isOnlyMovable(self, position: Vec2):
        return self.get(position).isOnlyMovable()

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

    def isOnlyMovable(self):
        return self.isEmpty() or len(self.items) == 1 and self.getMovable() != None

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

    def step(self, table: Table, direction: str, bring: bool):
        step_position = self.position + DIRECTION_VECTORS[direction]
        movable = table.getMovable(self.position)
        if step_position != self.position and not table.isStepOrMovable(step_position) or (bring and (not movable or table.getMovable(step_position))):
            return False

        self.moveToPosition(table, step_position)
        if bring:
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
    def __init__(self, position: Vec2, direction: Vec2):
        super().__init__(position)
        self.direction = direction

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
            for bring in [True, False]:
                yield direction, bring

class Game:
    def __init__(
        self,
        tableSize: Vec2 = Vec2(2, 4),
        gamerPosition: Vec2 = Vec2(1, 0),
        ghostPosition: Vec2 = Vec2(0, 1),
        snakePosition: Vec2 = Vec2(1, 2), snakeDirection: Vec2 = DIRECTION_VECTORS['LEFT'],
        eyePosition: Vec2 = Vec2(0, 2),
        spiderPosition: Vec2 = Vec2(0, 0),
        treasure1Position: Vec2 = Vec2(0, 3),
        treasure2Position: Vec2 = Vec2(1, 3)
    ):
        self.table = Table(tableSize.x, tableSize.y)
        self.gamer = Gamer(gamerPosition)

        self.ghost = Ghost(ghostPosition)
        self.snake = Snake(snakePosition, snakeDirection)
        self.eye = Eye(eyePosition, self.snake)
        self.spider = Spider(spiderPosition)

        self.treasure1 = Treasure(treasure1Position)
        self.treasure2 = Treasure(treasure2Position)

        self.table.set(self.gamer)
        self.table.set(self.ghost)
        self.table.set(self.eye)
        self.table.set(self.spider)
        self.table.set(self.snake)
        self.table.set(self.treasure1)
        self.table.set(self.treasure2)

        self.enemies = [self.ghost, self.eye, self.spider, self.snake]

    def __repr__(self):
        return str(self.table)

    def clone(self):
        return Game(
            self.table.size,
            self.gamer.position,
            self.ghost.position,
            self.snake.position, self.snake.direction,
            self.eye.position,
            self.spider.position,
            self.treasure1.position,
            self.treasure2.position
        )

    def state(self):
        return str(self)

    def isWon(self):
        return self.table.getMovable(Vec2(0, 0)) and self.table.getMovable(Vec2(1, 0))

    def isLost(self):
        for cell in self.table.cells():
            if cell.isDeadly() and cell.has(self.gamer):
                return True

        return False

    def possibleSteps(self):
        return self.gamer.possibleSteps()

    def step(self, direction: str, bring: bool):
        if not self.gamer.step(self.table, direction, bring):
            return False

        for enemy in self.enemies:
            enemy.step(self.table)

        return True


class GamePossibility:
    def isWin(self):
        return False

    def __repr__(self):
        return 'Win: {}, Lose: {}'.format(self.isWin(), self.isLose())

    def isLose(self):
        return False

class GameWinPossibility(GamePossibility):
    def __init__(self, steps_to_win, next_state):
        self.steps_to_win = steps_to_win
        self.next_state = next_state

    def __repr__(self):
        return 'Steps to win: {}'.format(self.steps_to_win)

    def isWin(self):
        return True

class GameLosePossibility(GamePossibility):
    def isLose(self):
        return True

class GameSolver:
    stack = []
    best_possibilities = {}

    def printResult(self, game):
        print(len(self.best_possibilities))
        game_state_str = game.state()
        print(self.best_possibilities[game_state_str].steps_to_win)
        print(game_state_str)
        while self.best_possibilities[game_state_str].next_state != None:
            game_state_str = self.best_possibilities[game_state_str].next_state
            print(game_state_str)

    def solve(self, game: Game):
        self.stack.append(game)
        while len(self.stack) != 0:
            game_state = self.stack[-1]
            game_state_str = game_state.state()

            if not game_state_str in self.best_possibilities:
                self.best_possibilities[game_state_str] = GamePossibility()

            if game_state.isLost():
                print('LOSE')
                self.setLose(game_state_str)
                self.stack.pop()
                continue

            if game_state.isWon() or game.isLost():
                print('WIN')

                self.setWin()

                self.stack.pop()
                continue

            appended = False
            for step in game_state.possibleSteps():
                game_clone = game_state.clone()
                success = game_clone.step(*step)
                if not success:
                    continue

                state_after_step = game_clone.state()
                if state_after_step in self.best_possibilities:
                    if self.best_possibilities[state_after_step].isWin() == True:
                        self.setWin(self.best_possibilities[state_after_step].steps_to_win + 1, state_after_step)

                    continue

                self.stack.append(game_clone)
                appended = True
                break

            if not appended:
                self.stack.pop()

    def setWin(self, steps_to_win = 0, next_state = None):
        for state in self.stack[::-1]:
            state_str = state.state()
            if self.best_possibilities[state_str].isWin() == True and steps_to_win > self.best_possibilities[state_str].steps_to_win:
                break

            self.best_possibilities[state_str] = GameWinPossibility(steps_to_win, next_state)

            steps_to_win = steps_to_win + 1
            next_state = state_str

    def setLose(self, game_state):
        if self.best_possibilities[game_state].isWin():
            return

        self.best_possibilities[game_state] = GameLosePossibility()


game = Game()
gameSolver = GameSolver()

gameSolver.solve(game)
gameSolver.printResult(game)
