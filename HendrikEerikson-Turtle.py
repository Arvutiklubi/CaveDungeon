__author__ = 'hendrik.eerikson'

import turtle, math

t = turtle.Turtle()
w = turtle.Screen()

t.speed(0)
w.delay(0)

t.up()
t.goto(-250, -250)
t.down()

delta_pos = 0

def pen_color(dx):
    return (1.0, (math.sin(dx*0.05)+1)*0.5, (math.cos(dx*0.05)+1)*0.5)

def tri_A(len, depth):
    global delta_pos
    if depth == 0:
        t.color(pen_color(delta_pos)[0], pen_color(delta_pos)[1], pen_color(delta_pos)[2])
        t.fd(len)
        delta_pos += len

    else:
        tri_B(len/2, depth-1)
        t.right(60)
        tri_A(len/2, depth-1)
        t.right(60)
        tri_B(len/2, depth-1)



def tri_B(len, depth):
    global delta_pos
    if depth == 0:
        t.color(pen_color(delta_pos)[0], pen_color(delta_pos)[1], pen_color(delta_pos)[2])
        t.fd(len)
        delta_pos += len

    else:
        tri_A(len/2, depth-1)
        t.left(60)
        tri_B(len/2, depth-1)
        t.left(60)
        tri_A(len/2, depth-1)



tri_A(500, 6)

w.exitonclick()