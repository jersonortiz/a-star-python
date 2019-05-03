#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import sys

class Node():
    """A node class for A* Pathfinding"""

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
## The readImage function takes a file path as argument and returns image in binary form.
## You can copy the code you wrote for section1.py here.
def readImage(filePath):
    #############  Add your Code here   ###############
    img = cv2.imread(filePath, 0)
    ret, binaryImage = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY)
    ###################################################
    return binaryImage

## The findNeighbours function takes a maze image and row and column coordinates of a cell as input arguments
## and returns a stack consisting of all the neighbours of the cell as output.
## Note :- Neighbour refers to all the adjacent cells one can traverse to from that cell provided only horizontal
## and vertical traversal is allowed.
## You can copy the code you wrote for section1.py here.
def findNeighbours(img,row,column):
    neighbours = []
    #############  Add your Code here   ###############
    #print("row: "+str(row)+" col: "+str(column)) 
    i = 0
    #itera hasta termnar el borde 
    while(True):
        if img[i, i] != 0:
            #print("color: "+str(img[i,i])+" pos: "+str(i))
            border = i 
            break
        i += 1
    #print("color: "+str(img[i,i])+" pos: "+str(i))
    #print("border: "+str(i))
    i = border
    cell = 0
    while(True):
        if img[i, i] == 0:
            cell = i
            break
        i += 1
    #print("color: "+str(img[i,i])+" cell: "+str(cell)) 
    if img[cell - border * 2, cell] == 0 or img[cell, cell - border * 2] == 0:
        
        cell = cell + border
    #print("cell: "+str(cell))
    #print("img[cell - border * 2, cell]:"+str(img[cell - border * 2, cell]))
    #print("img[cell, cell - border * 2]:"+str(img[cell, cell - border * 2]))

    #cell=20
    row_new = int((2 * row + 1) * (cell / 2))
    #print("row_new = (2 * row + 1) * (cell / 2): "+str(row_new))
    col_new = int((2 * column + 1) * (cell / 2))
    #print(" col_new = (2 * column + 1) * (cell / 2): "+str(col_new))
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
    ###################################################
    return neighbours

##  colourCell function takes 4 arguments:-
##            img - input image
##            row - row coordinates of cell to be coloured
##            column - column coordinates of cell to be coloured
##            colourVal - the intensity of the colour.
##  colourCell basically highlights the given cell by painting it with the given colourVal. Care should be taken that
##  the function doesn't paint over the black walls and only paints the empty spaces. This function returns the image
##  with the painted cell.
##  You can copy the code you wrote for section1.py here.
def colourCell(img, row, column, flag):   ## Add required arguments here.
    
    #############  Add your Code here   ###############
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
    if flag == 1:
        img[top + 5 : bottom - 4, left + 5 : right - 4] = 0
    ###################################################
    return img

def childrenof(img, current_node):
    childd=findNeighbours(img, current_node.position[0], current_node.position[1])
    children = []
    #Generate children
    for new_position in childd: # Adjacent squares

        # Get node position
        node_position = (new_position[0],new_position[1])

        # Create new node
        new_node = Node(current_node, node_position)

        # Append
        children.append(new_node)
    return children

def eval(open_list,closed_list):
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        return current_node    

def obtainpath(current_node ):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent  
    return path[::-1] # Return reversed path

def calccells(children,open_list ,closed_list , current_node , end_node):
    # Loop through children
    for child in children:
        # Child is on the closed list
        rep=0
        for closed_child in closed_list:
            #print("comparin")
            if child == closed_child:
                #print("repeat")
                rep=1

        # Create the f, g, and h values
        child.g = current_node.g + 1
        child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
        child.f = child.g + child.h
        repp=0

        # Child is already in the open list
        for open_node in open_list:
            if child == open_node and child.g > open_node.g:
                repp=1

        # Add the child to the open list
        if(rep!=1 and repp!=1):
            open_list.append(child) 
    return open_list


def astar( start, end , img):

    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        current_node= eval(open_list,closed_list)
       
        # Found the goal
        if current_node == end_node:
            return obtainpath(current_node)

        #find the chil of the current node 
        children = childrenof(img, current_node)

        #find the 
        open_list= calccells(children, open_list , closed_list,current_node , end_node)


    ###################################################

## This is the main function where all other functions are called. It accepts filepath
## of an image as input. You are not allowed to change any code in this function.
def main(filePath, flag = 0):                 
    img = readImage(filePath)      ## Read image with specified filepath.
    breadth = len(img)/20         ## Breadthwise number of cells
    length = len(img[0])/20           ## Lengthwise number of cells

    if length == 10:
        initial_point = (0,0)      ## Start coordinates for maze solution
        final_point = (9,9)        ## End coordinates for maze solution    
    else:
        initial_point = (0,0)
        final_point = (19,19)

    #graph = buildGraph(img)       ## Build graph from maze image. Pass arguments as required.
    #shortestPath = findPath(graph, initial_point, final_point, img)  ## Find shortest path. Pass arguments as required.
    path=astar(initial_point, final_point ,img)
    print("len: " +str(length))
    #print(shortestPath)             ## Print shortest path to verify

    string = str(path) + "\n"
    for i in path:         ## Loop to paint the solution path.
        img = colourCell(img, i[0], i[1], 200)
    if __name__ == '__main__':     ## Return value for main() function.
        return img
    else:
        if flag == 0:
            return string
        else:
            return graph


## The main() function is called here. Specify the filepath of image in the space given.            
if __name__ == '__main__':

    if len(sys.argv)>=2:
       filePath=str(sys.argv[1])+".jpg"
    else:
        filePath = 'maze01.jpg' 
    img = readImage(filePath)
    img = main(filePath)         ## Main function call
    soname="solved"+filePath
    cv2.imwrite(soname, img) 
    cv2.imshow('imgae',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)



