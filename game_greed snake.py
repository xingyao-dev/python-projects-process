class Point:
    col=0
    row=0
    def __init__(self, col, row):
      self.col=col
      self.row=row
    def cop(self):
        return Point(row=self.row, col=self.col)

import pygame
import random

pygame.init()
w = 800
h = 600
ROW=60
COL=80
size = (w, h)
window = pygame .display.set_mode(size)
pygame.display.set_caption("greedy_snake")

bg_color=(255, 255, 255)
snake_color=(200, 200, 200)

def gen_food():
    while 1:
        pos=Point(row=random.randint(0,ROW-1),col=random.randint(0,COL-1))

        is_coll=False
        if head.row==pos.row and head.col==pos.col:
            is_coll= True
        for snak  in snake:
            if snak.row==pos.row and head.col==pos.col:
                is_coll = True
                break
        if not is_coll :
            break
    return pos


head=Point(row=int(ROW/2), col=int(COL/2))
head_color=(19, 19, 20)
food=Point(row=random.randint(0,ROW-1),col=random.randint(0,COL-1))
food_color=(255, 255, 0)

snake=[
    Point(row=head.row, col=head.col + 1),
    Point(row=head.row, col=head.col + 2),
    Point(row=head.row, col=head.col + 3),
]

direct='left'

def rect(point, color):
    cell_width=w /COL
    cel_height=h /ROW



    left=point.col*cell_width
    top=point.row*cel_height

    pygame.draw.rect(window, color,(left, top, cel_height, cel_height))

    pass



quit =  True
clock=pygame.time.Clock()
while quit:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            quit=False
        elif event.type==pygame.KEYDOWN:
            print(event)

            if event.key==1073741906:
                direct='up'
            elif event.key==1073741903:
                direct='right'
            elif event.key==1073741904:
                direct='left'
            elif event.key==1073741905:
                 direct='down'

    eat=(head.row==food.row and head.col==food.col)

    if eat:
        food  = Point(row=random.randint(0,ROW-1),col=random.randint(0,COL-1))


    snake.insert(0, head.cop())
    if not eat:
        snake .pop()


    if direct=='left':
        head.col -=1
    elif direct=='right':
        head.col  +=1
    elif direct=='down':
        head.row +=1
    elif direct=='up':
        head.row -=1


    pygame.draw.rect(window, bg_color, ( 0, 0, w, h))

    for body in snake:
        rect(body, snake_color   )
    rect(head, head_color )
    rect(food, food_color )

    pygame.display.flip()

    clock.tick(15)



# # for _ in range("key-word"):
# #     if keyword.iskeyword("12345"):
# #         print("You can play the game!")
# # else:
# #     print("You don't play the game!!")





