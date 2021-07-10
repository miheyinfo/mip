import numpy as np
import matplotlib.pyplot as plt
import json
from functools import partial
from pycpd import AffineRegistration
from pycpd import DeformableRegistration


def visualize(iteration, error, X, Y, ax):
    plt.cla()
    ax.scatter(X[:, 0], X[:, 1], color='red', label='Target')
    ax.scatter(Y[:, 0], Y[:, 1], color='blue', label='Source')
    plt.text(0.87, 0.92, 'Iteration: {:d}\nQ: {:06.4f}'.format(
        iteration, error), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
             fontsize='x-large')
    ax.legend(loc='upper left', fontsize='x-large')
    plt.draw()
    plt.pause(0.001)


def createSimplePlot(figure, char, color):
    x = []
    y = []
    for item in figure:
        x.append(item[0])
        y.append(item[1])
    plt.plot(x, y, char, color=color)
    return plt

def plotTwoFigures(X, Y):
    createSimplePlot(X, 'o', 'green')
    createSimplePlot(Y, 'o', 'black')
    plt.draw()
    plt.pause(0.001)

def plotContourCoordinates(contour_coordinates):
    x = []
    y = []
    for item in contour_coordinates:
        x.append(item[0])
        y.append(item[1])

    # plt.plot(x, y, linestyle='-', color='black')
    plt.plot(x, y, 'o')
    plt.pause(0.001)

def getCoordinatesFromObjFile(fileName):
    file1 = open(fileName, 'r')
    Lines = file1.readlines()

    coordinates = []
    # Strips the newline character
    for line in Lines:
        splitedLine = line.strip().split()
        if splitedLine[0] == "v":
            coordinates.append([(float(splitedLine[1])), (float(splitedLine[3]))])
    return np.array(coordinates)

def getContourCoordinatesFromJSONFile(fileName):
    with open(fileName, 'r') as jsonFile:
        data = jsonFile.read()

    # parse file
    jsonObject = json.loads(data)

    info_array = jsonObject['INFO']
    ## get contour
    contour = list(filter(lambda x: x["properties"]["classification"]["name"] == "Region*", info_array))
    contour_coordinates = contour[0]["geometry"]["coordinates"][0]
    for item in contour_coordinates:
        item[0] = float(item[0])/10000
        item[1] = float(item[1])/10000
    return contour_coordinates


def rotate(data, theta):
    ox, oy = 0, 0  # point to rotate about
    A = np.matrix([[np.cos(theta), -np.sin(theta)],
                   [np.sin(theta), np.cos(theta)]])

    w = np.zeros(data.shape)
    airfoil_shifted = data - np.array([ox, oy])
    for i, v in enumerate(airfoil_shifted):
        w[i] = A @ v
    return w

def main():

    objectNames = ['C','D','E','F','G','H']
    for name in objectNames:
        coordinatesFromObj = getCoordinatesFromObjFile(name + '.obj')
        coordinatesFromJSON = np.array(getContourCoordinatesFromJSONFile('FALL-Y-1-' + name + '_GeoJSON.json'))

        # if name == 'C':
        #     coordinatesFromJSON = rotate(coordinatesFromJSON, -1.66)
        # #if name == 'D':
        # # neeed to edit source qpath file
        # if name == 'E':
        #     coordinatesFromJSON = rotate(coordinatesFromJSON, 3.1)
        # if name == 'F':
        #     coordinatesFromJSON = rotate(coordinatesFromJSON, 3.5)
        # if name == 'H':
        #     coordinatesFromJSON = rotate(coordinatesFromJSON, 3.1)

        # plotTwoFigures(coordinatesFromJSON, coordinatesFromObj)

        reg = AffineRegistration(**{'X': np.array(coordinatesFromObj), 'Y': np.array(coordinatesFromJSON)})
        poly_wsi_reg = reg.register()[0]

        plotTwoFigures(coordinatesFromObj, poly_wsi_reg)


if __name__ == '__main__':
    main()
