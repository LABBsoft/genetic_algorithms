from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import math

def plotRosen():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xA = np.linspace(6,-6,50)
    yA = np.linspace(-10,10,50)
    X, Y = np.meshgrid(xA, yA)
    Z = [[0 for i in range(len(X))] for j in range(len(Y))]
    for x in range(len(X)):
        for y in range(len(Y)):
            Z[x][y] = pow(1 - (x - (len(X) / 2)),2) + (100 * pow(((y - (len(Y) / 2)) - pow((x - (len(X) / 2)),2)),2))
    print(X, Y)
    ax.plot_wireframe(np.array(X),np.array(Y),np.array(Z),rstride=1, cstride=1)
    plt.show()

def plotDejong():
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')

    xA = np.linspace(10,-10,50)
    yA = np.linspace(-10,10,50)
    X, Y = np.meshgrid(xA, yA)
    Z = [[0 for i in range(len(X))] for j in range(len(Y))]
    for x in range(len(X)):
        for y in range(len(Y)):
            Z[x][y] = pow(x - (len(X)/2),2) + pow(y - (len(Y)/2),2)
    ax.plot_wireframe(np.array(X),np.array(Y),np.array(Z),rstride=1, cstride=1)
    plt.show()