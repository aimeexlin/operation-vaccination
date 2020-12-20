# imports
import networkx as nx
import numpy as np
from time import time
from project_utils import *

# function definitions
def nearest_node(network, start, destinations):
    """ Finds nearest node to the start node from a list of possible destination nodes in a network

    Parameters
    ----------
    network : networkx.Graph
        The graph that contains the node and edge information
    start : string
        The name of the start node
    destinations : list
        The list of possible destination nodes
    
    Returns
    -------
    nearest_node : string
        The name of the nearest node
    distance : float
        The distance between the start and the nearest node in hours
    """
    # initialisations
    distances = []
    
    # finds distance between start node and its neighbours
    for destination in destinations:
        d = nx.shortest_path_length(network, start, destination, weight="weight")
        distances.append(d)
    ind = np.argmin(distances) # gets index of shortest distance
    nearest_node = destinations[ind] # uses index to get nearest node name
    distance = distances[ind] # uses index to get distance to nearest node

    return nearest_node, distance

def path_and_distance(network, group, filename):
    """ Finds shortest path and distance for each group of nodes, saves the path as a txt file
        and png image, and returns the distance

        Parameters
        ----------
        network : networkx.Graph
        The graph that contains the node and edge information
        group : list
        The list of nodes to generate a path through
        filename : string
        The name of the file to save to

        Returns
        -------
        total_distance : float
        The total distance of the path in hours

        Notes
        ------
        The filename does not include file extensions because different file types are generated
        eg. for "path_1.txt" the filename would be "path_1"
    """
    # initialisations
    path_names = ["Auckland Airport"]
    path = ["Auckland Airport"]
    path_section = []
    total_distance = 0
    nearest = path[0]

    # gets nearest node to previous nearest node while there are nodes remaining in group
    while len(group) > 0:
        nearest, distance = nearest_node(network, nearest, group)
        path_names.append(nearest)  # adds node to path names
        path_section = nx.shortest_path(network, path_names[-2], nearest, weight="weight")  # adds path
        path += path_section[1:]
        total_distance += distance  # increments total distance
        group.remove(nearest)   # removes node from group

    # adds distance and path for returning to the airport
    path_names.append("Auckland Airport")
    path_section = nx.shortest_path(network, path_names[-2], "Auckland Airport", weight="weight")
    path += path_section[1:]
    total_distance += distance

    # generates txt file of node names
    f = open("%s.txt" %filename, "w")
    for item in path_names:
        f.write("%s\n" %item) # writes node names one on each line (first and last lines are airport)
    f.close()
    
    # generates png image of path
    plot_path(network, path, save="%s.png" %filename) # plots path with airport at start and end

    return total_distance

def main():
    '''Finds four shortest public transportation paths around rest homes in Auckland starting and ending at Auckland Airport'''
    # gets time
    t0 = time()

    # reads network and rest home data
    auckland = read_network("network.graphml")
    rest_homes = get_rest_homes("rest_homes.txt")

    # SPLITTING REST HOMES INTO FOUR GROUPS
    #initialises lists
    north = []
    west = []
    central = []
    south_east = []

    for rest_home in rest_homes:
        if auckland.nodes[rest_home]["lat"] > -36.835:
            north.append(rest_home)
        elif auckland.nodes[rest_home]["lng"] < 174.73:
            west.append(rest_home)
        elif auckland.nodes[rest_home]["lng"] < 174.88 and auckland.nodes[rest_home]["lat"] > -36.924:
            central.append(rest_home)
        else:
            south_east.append(rest_home)

    # PATHS AND DISTANCES FOR EACH GROUP
    # initialises list
    distances = []

    # generates paths (txt and png) and gets distance of each path
    distances.append(path_and_distance(auckland, north, "path_1"))
    distances.append(path_and_distance(auckland, west, "path_2"))
    distances.append(path_and_distance(auckland, central, "path_3"))
    distances.append(path_and_distance(auckland, south_east, "path_4"))

    # gets time
    t1 = time()
    
    # PRINTS RESULTS
    # prints distance of each courier
    print("The time taken by the first courier is %.2f hours" %distances[0])
    print("The time taken by the second courier is %.2f hours" %distances[1])
    print("The time taken by the third courier is %.2f hours" %distances[2])
    print("The time taken by the fourth courier is %.2f hours" %distances[3])

    # prints time taken to compute solution
    print("The total computational time is %.2f minutes" %((t1-t0)/60))

if __name__ == "__main__":
    main()