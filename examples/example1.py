import colorgram
import turtle
from turtle import Turtle, Screen
import random

colour_list = [(203, 165, 109),  (152, 74, 49), (53, 92, 122), (223, 201, 137), (165, 151, 45), (134, 33, 23), (133, 162, 184), (197, 93, 73), (49, 120, 87), (16, 97, 73), (72, 47, 40), (93, 73, 75), (147, 178, 148), (233, 176, 166), (160, 142, 158), (54, 47, 50), (184, 205, 173), (23, 84, 88), (151, 18, 21), (42, 61, 73), (86, 144, 129), (43, 66, 87), (186, 83, 85), (18, 71, 69), (107, 128, 152), (177, 192, 210)]
start_pos_x = -250
start_pos_y = -250

timmy = Turtle()
turtle.colormode(255)
timmy.color()
timmy.penup()
timmy.setpos(start_pos_x, start_pos_y)
timmy.speed(0)

dot_count = 0
timmy.hideturtle()
def movement():
    for _ in range(10):
        timmy.color(random.choice(colour_list))
        timmy.dot(20)
        timmy.forward(50)


for _ in range(10):
    timmy.setpos(start_pos_x, start_pos_y)
    movement()
    start_pos_y += 50


screen = Screen()
screen.exitonclick()



