import json
import networkx as nx
from shapely.ops import unary_union
import geopandas as gpd
from shapely.geometry import LineString, Point

# Open yaml config file
with open('config.json') as f:
   config = json.load(f)

class Network(object):
    def __init__(self, lines, points):
        """
        Network to use in distance calculations.
        
        Parameters
        ----------
        id : str
            Origin id, usually corresponding grid cell.
        network : shapely.geometry.lines
            Geometries of network.
        """
        # graph
        self.points = points
        self.graph = nx.Graph()
        for index, row in lines.iterrows():
            self.graph.add_edge(row["id_start"], row["id_end"], dist = row['geometry'].length)

    def get_origin_dist(self, o, max_dist):
        try:
            d = nx.single_source_dijkstra_path_length(self.graph, o.access_node, 
                                                      cutoff=max_dist, weight='dist')
            return d
        except nx.exception.NodeNotFound:
            print("Access node not found {}".format(o.id))
            return {}