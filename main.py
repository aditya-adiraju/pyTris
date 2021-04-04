import pygame
import random

screen_x = 250
screen_y = 600
pygame.init()
screen = pygame.display.set_mode((screen_x + 150, screen_y))
pygame.display.set_caption("PyTris")
icon = pygame.image.load("Assets/icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


class Player:
    def __init__(self):
        self.grid = [[0 for x in range(10)] for y in range(24)]

    def check_clear(self):
        flag = True
        for y in range(len(self.grid)):
            if self.grid[y].count(0) == 0:
                flag = False
                for i in range(y-1, -1, -1):
                    self.grid[i+1] = self.grid[i]
                self.grid[0] = [0 for x in range(10)]
        if not flag:
            self.check_clear()

    def draw(self, win):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 1:
                    pygame.draw.rect(win, (255, 0, 0), ((x * 25, y * 25), (25, 25)))


new = Player()


class Tetromino:
    def __init__(self, x, y, s):
        self.s = s
        self.x = x
        self.y = y
        global new
        if self.s == 'I':
            self.location = [[self.y, self.x], [self.y + 1, self.x], [self.y + 2, self.x], [self.y + 3, self.x]]
            self.width = 1
            self.height = 4
        elif self.s == 'L':
            self.location = [[self.y, self.x], [self.y + 1, self.x], [self.y + 2, self.x], [self.y + 2, self.x + 1]]
            self.width = 2
            self.height = 3
        elif self.s == 'J':
            self.location = [[self.y, self.x + 1], [self.y + 1, self.x + 1], [self.y + 2, self.x + 1],
                             [self.y + 2, self.x]]
            self.width = 2
            self.height = 3
        elif self.s == 'S':
            self.location = [[self.y, self.x], [self.y + 1, self.x], [self.y + 1, self.x + 1], [self.y + 2, self.x + 1]]
            self.width = 2
            self.height = 3
        elif self.s == 'Z':
            self.location = [[self.y, self.x + 1], [self.y + 1, self.x + 1], [self.y + 1, self.x], [self.y + 2, self.x]]
            self.width = 2
            self.height = 3
        elif self.s == 'T':
            self.location = [[self.y, self.x], [self.y + 1, self.x], [self.y + 1, self.x + 1], [self.y + 2, self.x]]
            self.width = 2
            self.height = 3
        elif self.s == 'O':
            self.location = [[self.y, self.x], [self.y, self.x + 1], [self.y + 1, self.x], [self.y + 1, self.x + 1]]
            self.width = 2
            self.height = 2
        self.fill(new)

    def fill(self, player=new, f=1):
        for i in self.location:
            player.grid[i[0]][i[1]] = f

    def collide(self, player=new):
        for i in self.location:
            if player.grid[i[0]][i[1]] == 1:
                return True
        return False

    def rotate(self):
        self.fill(new, 0)
        for mino in self.location:
            mino[1] -= self.x
            mino[0] -= self.y
            tmp = mino[0]
            mino[0] = mino[1] + self.y
            mino[1] = -tmp + self.x
        if self.collide():
            for mino in self.location:
                mino[1] -= self.x
                mino[0] -= self.y
                tmp = mino[0]
                mino[0] = -mino[1] + self.y
                mino[1] = tmp + self.x
        else:
            minimum_y = self.location[0][0]
            min_cols = [self.location[0][1]]
            for i in range(1, 4):
                if self.location[i][0] < minimum_y:
                    minimum_y = self.location[i][0]
                    min_cols = [self.location[i][1]]
                if self.location[i][0] == minimum_y:
                    min_cols.append(self.location[i][1])

            minimum_x = min(min_cols)

            self.x = minimum_x
            self.y = minimum_y
            tmp = self.width
            self.width = self.height
            self.height = tmp
            self.fill(new)

    def move(self, x, y):
        self.fill(new, 0)
        self.x += x
        self.y += y
        for i in self.location:
            i[0] += y
            i[1] += x

        if self.collide():
            self.x -= x
            self.y -= y
            for i in self.location:
                i[0] -= y
                i[1] -= x
        self.fill(new)


minos = ['I', 'L', 'J', 'S', 'Z', 'T', 'O']
block = Tetromino(0, 0, random.choice(minos))
bg = pygame.image.load('Assets/bg.png')


if __name__ == '__main__':
    done = False
    while not done:
        clock.tick(15)
        for event in pygame.event.get():
            if event == pygame.QUIT:
                done = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and block.x + block.height < len(new.grid[0]):
            block.rotate()
            if block.x - block.width < 0:
                block.move(abs(block.x-block.width), 0)
        if keys[pygame.K_LEFT] and block.x != 0:
            block.move(-1, 0)
        if keys[pygame.K_RIGHT] and block.x + block.width < len(new.grid[0]):
            block.move(1, 0)
        if keys[pygame.K_ESCAPE]:
            break
        screen.fill(0)
        new.draw(screen)
        if block.y + block.height < 24:
            prev = block.y
            block.move(0, 1)
            if block.y == 0:
                break
            if prev == block.y:
                new.check_clear()
                block = Tetromino(0, 0, random.choice(minos))
        else:
            new.check_clear()
            block = Tetromino(0, 0, random.choice(minos))
        pygame.display.flip()
