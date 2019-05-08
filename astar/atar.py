#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def  astar(maze, start, end):

    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while len(open_list) > 0:

        current_node= eval(open_list,closed_list)
       
        if current_node == end_node:
            return obtainpath(current_node)

        children = childrenof(maze, current_node)

        open_list= calccells(children, open_list , closed_list,current_node , end_node)

def calccells(children,open_list ,closed_list , current_node , end_node):

    for child in children:
        rep=0

        for closed_child in closed_list:
            if child == closed_child:
                rep=1

        child.g = current_node.g + 1
        child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
        child.f = child.g + child.h
        repp=0

        for open_node in open_list:
            if child == open_node and child.g > open_node.g:
                repp=1

        if(rep!=1 and repp!=1):
            open_list.append(child)

    return open_list

def eval(open_list,closed_list):

    current_node = open_list[0]
    current_index = 0

    for index, item in enumerate(open_list):
        if item.f < current_node.f:
            current_node = item
            current_index = index

    open_list.pop(current_index)
    closed_list.append(current_node)
    return current_node    

def obtainpath(current_node ):
    path = []
    current = current_node

    while current is not None:
        path.append(current.position)
        current = current.parent  
        
    return path[::-1]

def childrenof(maze,  current_node):

    children = []
    pathso= [(0, -1), (0, 1), (-1, 0), (1, 0)]
    pathsd= [ (-1, -1), (-1, 1), (1, -1), (1, 1)]
    paths=pathso+pathsd

    for new_position in paths:
        node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

        if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
            continue

        if maze[node_position[0]][node_position[1]] != 0:
            continue

        new_node = Node(current_node, node_position)
        children.append(new_node)

    return children

def printMaze(maze , start , end , path):
    for fil in path:
        maze[fil[0]][fil[1]]='*'

    maze[start[0]][start[1]]="I"
    maze[end[0]][end[1]]="F"

    for ma in maze:
        strin=""
        for ch in ma:
            strin= strin+str(ch)+" "
        print(strin)


def main():

    ma =    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    mb =   [[0, 0, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
            [0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 1, 0],
            [1, 1, 0, 0, 0, 1, 0, 1, 1, 0]]   

    mc =   [[0, 0, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
            [0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 1, 0],
            [1, 1, 0, 0, 0, 1, 0, 1, 1, 0]]   

    maze=ma

    start = (0, 0)
    end = (9,9)

    path = astar(maze, start, end)
    printMaze(maze,start,end,path)

if __name__ == '__main__':
    main()