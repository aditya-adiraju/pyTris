import pygame
import random

screen_x = 250
screen_y = 600
pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("PyTris")
icon = pygame.image.load("Assets/icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


class Player:
    def __init__(self):
        self.grid = [[(0, 0, 0) for x in range(10)] for y in range(24)]

    def check_clear(self):
        flag = True
        for y in range(len(self.grid)):
            if self.grid[y].count((0, 0, 0)) == 0:
                flag = False
                for i in range(y-1, -1, -1):
                    self.grid[i+1] = self.grid[i]
                self.grid[0] = [(0, 0, 0) for x in range(10)]
        if not flag:
            self.check_clear()

    def draw(self, win):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != (0, 0, 0):
                    pygame.draw.rect(win, self.grid[y][x], (((x * 25) + 2, (y * 25) + 2), (23, 23)))


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
            self.center = [self.y + 2, self.x + 0.5]
            self.color = (173, 216, 255)
        elif self.s == 'L':
            self.location = [[self.y, self.x], [self.y + 1, self.x], [self.y + 2, self.x], [self.y + 2, self.x + 1]]
            self.width = 2
            self.height = 3
            self.center = [self.y + 1.5, self.x + 1]
            self.color = (255, 165, 0)
        elif self.s == 'J':
            self.location = [[self.y, self.x + 1], [self.y + 1, self.x + 1], [self.y + 2, self.x + 1],
                             [self.y + 2, self.x]]
            self.width = 2
            self.height = 3
            self.center = [self.y + 1.5, self.x + 1]
            self.color = (0, 0, 255)
        elif self.s == 'S':
            self.location = [[self.y, self.x], [self.y + 1, self.x], [self.y + 1, self.x + 1], [self.y + 2, self.x + 1]]
            self.width = 2
            self.height = 3
            self.center = [self.y + 1.5, self.x + 1]
            self.color = (0, 255, 100)
        elif self.s == 'Z':
            self.location = [[self.y, self.x + 1], [self.y + 1, self.x + 1], [self.y + 1, self.x], [self.y + 2, self.x]]
            self.width = 2
            self.height = 3
            self.center = [self.y + 1.5, self.x + 1]
            self.color = (255, 0, 0)
        elif self.s == 'T':
            self.location = [[self.y, self.x], [self.y + 1, self.x], [self.y + 1, self.x + 1], [self.y + 2, self.x]]
            self.width = 2
            self.height = 3
            self.center = [self.y + 1.5, self.x + 1]
            self.color = (175, 53, 139)
        elif self.s == 'O':
            self.location = [[self.y, self.x], [self.y, self.x + 1], [self.y + 1, self.x], [self.y + 1, self.x + 1]]
            self.width = 2
            self.height = 2
            self.center = [self.y + 1, self.x + 1]
            self.color = (255, 255, 0)
        self.fill(new, self.color)

    def fill(self, player=new, f=(0, 0, 0)):
        for i in self.location:
            player.grid[i[0]][i[1]] = f

    def reset_center(self):
        min_x = self.location[0][1]
        max_x = self.location[0][1]
        for i in self.location:
            if i[1] > max_x:
                max_x = i[1]
            elif i[1] < min_x:
                min_x = i[1]
        self.center[1] = (min_x + max_x + 1) / 2
        self.center[0] = (min(self.location)[0] + max(self.location)[0] + 1) / 2

    def collide(self, player=new):
        for i in self.location:
            if player.grid[i[0]][i[1]] != (0, 0, 0):

                return True
        return False

    def rotate(self):
        self.fill(new, (0, 0, 0))
        tmp = self.width
        self.width = self.height
        self.height = tmp
        for pos in self.location:
            pos[1] -= self.center[1]
            pos[0] -= self.center[0]
            tmp = pos[1]
            pos[1] = int(pos[0] + self.center[1])
            pos[0] = int((-1 * tmp) + self.center[0])
        if self.collide():
            for pos in self.location:
                pos[1] -= self.center[1]
                pos[0] -= self.center[0]
                tmp = pos[1]
                pos[1] = int((-1 * pos[0]) + self.center[1])
                pos[0] = int(tmp + self.center[0])
                tmp = self.width
                self.width = self.height
                self.height = tmp

        else:
            self.reset_center()
            self.x = round(self.center[1] - self.width/2)
            self.y = round(self.center[0] - self.height/2)
        self.fill(new, self.color)

    def move(self, x, y):
        if max(self.location)[0] + y < 24:
            self.fill(new, (0, 0, 0))
            self.x += x
            self.y += y
            self.center[0] += y
            self.center[1] += x

            for i in self.location:
                i[0] += y
                i[1] += x
            if self.collide():
                self.x -= x
                self.y -= y
                self.center[0] -= y
                self.center[1] -= x
                for i in self.location:
                    i[0] -= y
                    i[1] -= x
            self.fill(new, self.color)


minos = ['I', 'L', 'J', 'S', 'Z', 'T', 'O']
block = Tetromino(0, 0, random.choice(minos))
bg = pygame.image.load('Assets/bg.png')


if __name__ == '__main__':
    done = False
    count = 0
    rot = False
    while not done:
        clock.tick(10)
        for event in pygame.event.get():
            if event == pygame.QUIT:
                done = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and (block.center[0] + block.width/2 < 24 and block.center[1] + block.height/2 < 10):
            if block.center[1] - block.height/2 >= 0:
                block.rotate()
                rot = True
        elif keys[pygame.K_RIGHT] and (block.center[1] + block.width/2 <= 9):
            block.move(1, 0)
            count = 0
        elif keys[pygame.K_LEFT] and block.x - 1 >= 0:
            block.move(-1, 0)
            count = 0
        if keys[pygame.K_ESCAPE]:
            break
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))

        new.draw(screen)
        if block.y + block.height < 24:
            prev = block.y
            block.move(0, 1)
            if block.y == 0:
                break
            if prev == block.y:
                count += 1
                if count >= 2:
                    new.check_clear()
                    block = Tetromino(0, 0, random.choice(minos))
        elif block.y + block.height == 24:
            prev = block.y
            if block.y == 0:
                break
            if prev == block.y:
                count += 1
                if count >= 2:
                    new.check_clear()
                    block = Tetromino(0, 0, random.choice(minos))

        else:
            new.check_clear()
            block = Tetromino(0, 0, random.choice(minos))
        pygame.display.flip()
