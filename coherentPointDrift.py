import numpy as np
import matplotlib.pyplot as plt
import json
from functools import partial
from pycpd import AffineRegistration


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

def plotContourCoordinates(contour_coordinates):
    x = []
    y = []
    for item in contour_coordinates:
        x.append(item[0])
        y.append(item[1])

    fig = plt.figure()
    # plt.plot(x, y, linestyle='-', color='black')
    plt.plot(x, y, 'o', color='red')
    plt.draw()
    plt.pause(0.001)

def getCoordinatesFromObjFile(fileName):
    file1 = open(fileName, 'r')
    Lines = file1.readlines()

    coordinates = []
    # Strips the newline character
    for line in Lines:
        splitedLine = line.strip().split()
        if splitedLine[0] == "v":
            coordinates.append([(float(splitedLine[1])+14)*6000, (float(splitedLine[3])+20)*4667])
    return np.array(coordinates)

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
    # X = np.loadtxt('test.txt')
    # plotContourCoordinates(X)
    coordinatesFromObj = getCoordinatesFromObjFile('C.obj')
    # print(coordinatesFromObj)
    plotContourCoordinates(coordinatesFromObj)

    # read file
    with open('FALL-Y-1-C_GeoJSON.json', 'r') as jsonFile:
        data = jsonFile.read()

    # parse file
    jsonObject = json.loads(data)

    info_array = jsonObject['INFO']
    ## get contour
    contour = list(filter(lambda x: x["properties"]["classification"]["name"] == "Region*", info_array))
    contour_coordinates = np.array(contour[0]["geometry"]["coordinates"][0])
    #plotContourCoordinates(contour_coordinates)
    #
    contour_coordinates = rotate(contour_coordinates, -1.66)
    #plotContourCoordinates(contour_coordinates)

    X = contour_coordinates
    Y = coordinatesFromObj

    fig = plt.figure()
    fig.add_axes([0, 0, 1, 1])
    callback = partial(visualize, ax=fig.axes[0])

    reg = AffineRegistration(**{'X': X, 'Y': Y})
    reg.register(callback)
    plt.show()


if __name__ == '__main__':
    main()
