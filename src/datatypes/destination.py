
import json
from shapely.ops import nearest_points

# Open yaml config file
with open('config.json') as f:
   config = json.load(f)

class Destination(object):
    id_counter = 0
    def __init__(self, category, usage, provider, geometry, 
                 admin_matters, admin_region, size = 1):
        """
        Origin point for which accessibility is calculted.
        
        Parameters
        ----------
        id : str
            Origin id, usually corresponding grid cell.
        geom : geopandas.geoseries.GeoSeries
            Geometry of origin zone or point.
        network : networkx.Graph
            Network used for routing
        nodes : NodeView
            Nodes connecting links
        edges : EdgeView
            Links between nodes
        """
        self.id = Destination.id_counter
        Destination.id_counter += 1
        self.category = category
        self.usage = usage
        self.admin_matters = admin_matters
        self.admin_region = admin_region
        self.provider = provider
        self.geometry = geometry
        self.centroid = geometry.centroid
        self.crs = config["crs"]
        self.size = size

    def set_access_node(self, network):
        # Find the nearest nodes in a graph
        mask = network.points.within(self.centroid.buffer(config["access_radius"]))
        if any(mask):
            nearby_points = network.points.loc[mask]
            nearest_geoms  = nearest_points(self.centroid, nearby_points.geometry.unary_union)
            nearest_data = nearby_points.loc[nearby_points.geometry == nearest_geoms[1]]
            nearest_value = nearest_data["id"].values[0]
            self.access_node = nearest_value
        else:
            self.access_node = None
        
        
