#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import sys

class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return ((self.position[0] == other.position[0]) and (self.position[1] == other.position[1])) 

class Link():
    value = 0
    parent = 0
    def __init__(self, a, b):
        self.value = a
        self.parent = b

def readImage(filePath):
    img = cv2.imread(filePath, 0)
    ret, binaryImage = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY)
    return binaryImage

def findNeighbours(img,row,column):
    
    neighbours = []
    i = 0

    while(True):
        if img[i, i] != 0:
            border = i 
            break
        i += 1

    i = border
    cell = 0

    while(True):
        if img[i, i] == 0:
            cell = i
            break
        i += 1

    if img[cell - border * 2, cell] == 0 or img[cell, cell - border * 2] == 0:
        cell = cell + border

    row_new = int((2 * row + 1) * (cell / 2))
    col_new = int((2 * column + 1) * (cell / 2))
    top = int(row_new - (cell / 2) + 1)
    bottom = int(row_new + (cell / 2) - 2)
    left = int(col_new - (cell / 2) + 1)
    right = int(col_new + (cell / 2) - 2)

    if img[top, col_new] != 0:
        neighbours.append([row - 1, column])

    if img[bottom, col_new] != 0:
        neighbours.append([row + 1, column])

    if img[row_new, left] != 0:
        neighbours.append([row, column - 1])

    if img[row_new, right] != 0:
        neighbours.append([row, column + 1])

    return neighbours

def colourCell(img, row, column ):

    neighbours = findNeighbours(img, row, column)
    
    i = 0
    
    while(True):
        if img[i, i] != 0:
            border = i
            break
        i += 1

    i = border
    cell = 0

    while(True):
        if img[i, i] == 0:
            cell = i 
            break
        i += 1

    if img[cell - border * 2, cell] == 0 or img[cell, cell - border * 2] == 0:
        cell = cell + border

    row_new = int((2 * row + 1) * (cell / 2))
    col_new = int((2 * column + 1) * (cell / 2))
    top =int( row_new - (cell / 2) + 1)
    bottom = int(row_new + (cell / 2) - 2)
    left = int(col_new - (cell / 2) + 1)
    right = int(col_new + (cell / 2) - 2)

    for i in neighbours:
        if i[0] == row + 1:
            img[top + 1 : bottom + 2, left + 1 : right] = 150
        if i[0] == row - 1:
            img[top - 1 : bottom, left + 1 : right] = 150
        if i[1] == column + 1:
            img[top + 1 : bottom, left + 1 : right + 2] = 150
        if i[1] == column - 1:
            img[top + 1 : bottom, left - 1 : right] = 150

    return img

def childrenof(img, current_node):

    childd=findNeighbours(img, current_node.position[0], current_node.position[1])
    children = []

    for new_position in childd:
        node_position = (new_position[0],new_position[1])
        new_node = Node(current_node, node_position)
        children.append(new_node)

    return children

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


def astar( start, end , img):

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

        children = childrenof(img, current_node)
        open_list= calccells(children, open_list , closed_list,current_node , end_node)


def fielmaze():
    if len(sys.argv)>=2:
        filePath=str(sys.argv[1])
    else:
        filePath = 'maze00.jpg' 
    return filePath


def pointt(length):


    if len(sys.argv)>=6:

        a=int(sys.argv[2])
        b=int(sys.argv[3])
        c=int(sys.argv[4])
        d=int(sys.argv[5])

        if (((a<length or a>=0 ) and (b<length or b>=0) ) and ((c<length or c>=0 ) and (d<length or d>=0))):

            final_point = (c,d)
            initial_point = (a,b)
        

    elif len(sys.argv)>=4:

        a=int(sys.argv[2])
        b=int(sys.argv[3])
        c=d=length-1

        if((a<length or a>=0 ) and (b<length or b>=0)):
            initial_point = (a,b)
        final_point = (c,d)
    else:
        initial_point = (0,0)
        final_point = (length-1,length-1)

    return (initial_point , final_point)

def main():

    filePath = fielmaze()

    img = readImage(filePath)
    breadth = len(img)/20
    length = len(img[0])/20 

    point = pointt(length)

    path=astar(point[0], point[1] ,img)
    string = str(path) + "\n"

    for i in path:
        img = colourCell(img, i[0], i[1])

    soname="solved"+filePath
    cv2.imwrite(soname, img) 
    cv2.imshow('imgae',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

if __name__ == '__main__':
    main()




