import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import geopandas as gpd
import json

# Open yaml config file
with open('config.json') as f:
   config = json.load(f)

config_map = config["basemap"]


def plot_grid(data, colname, service_geom, cmap = "viridis", discrete = False, min = 0, max = 3000, interval = 500, label = "Accessibility Index", title = ""):
    """
    Plot function for accessibility graphs.
    
    Parameters
    ----------
    discrete : bool
        Discrete or continuous mapping color scheme.
    min, max, interval (optional) = int
        Variables for discrete legend style 
    """

    # Create one subplot. Control figure size in here.
    fig, ax = plt.subplots(figsize=(12, 8))
    #plt.style.use('dark_background')

    if not discrete:
        # Visualize travel times into continuous coloring scheme
        data.plot(
            ax=ax,
            column=colname, 
            linewidth=0.03,
            cmap=cmap,
            alpha=0.9,
            legend=True,
            legend_kwds={"label": label, "orientation": "vertical"},
        )

    else:
        discrete_cmap = plt.cm.get_cmap(cmap)
        norm = mpl.colors.BoundaryNorm(np.arange(min, max + interval, interval), discrete_cmap.N)  # set bins to defined intervals
            
        # Visualize travel times into discrete coloring scheme with predefined intervals
        data.plot(
            ax=ax,
            column=colname, 
            linewidth=0.03,
            cmap=discrete_cmap,
            norm=norm,
            alpha=0.9,
            legend=True,
            legend_kwds={"label": label, "orientation": "vertical"},
        )

    # Add roads on top of the grid
    # (use ax parameter to define the map on top of which the second items are plotted)

    paths = gpd.read_file(config_map["paths"], engine = "pyogrio")
    paths = paths.to_crs(config["crs"])
    highway = gpd.read_file(config_map["roads"], engine = "pyogrio")
    highway = highway.to_crs(config["crs"])
    railways = gpd.read_file(config_map["railways"], engine = "pyogrio")
    railways = railways.to_crs(config["crs"])
    names = gpd.read_file(config_map["names"]["file"], engine = "pyogrio")
    names = names.to_crs(config["crs"])
    names["geometry"] = names.geometry.centroid
    names = names.loc[names.centroid.within(data.unary_union)]

    paths.plot(ax=ax, color="white", linewidth=0.1)
    highway.plot(ax=ax, color="white", linewidth=0.5)
    railways.plot(ax=ax, color="white", linestyle="-", linewidth=0.8)
    railways.plot(ax=ax, color="black", linestyle="--", linewidth=0.5)
    for x, y, label in zip(names.geometry.x, names.geometry.y, names[config_map["names"]["column"]]):
        ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points", fontsize=8, color='white')
    
    # Plot services
    if service_geom is not None:
        service_geom = service_geom.loc[service_geom.within(data.unary_union)]
        service_geom.plot(ax=ax, color="black", markersize=2.0)
        service_geom.plot(ax=ax, color="white", markersize=1.0)

    # Remove the empty white-space around the axes
    ax.set_axis_off()
    plt.title(title, fontdict = {'fontsize':15})
    plt.tight_layout()

    # Set axis bb
    xmin, ymin, xmax, ymax = data.total_bounds
    pad = 0.05  # add a padding around the geometry
    ax.set_xlim(xmin-pad, xmax+pad)
    ax.set_ylim(ymin-pad, ymax+pad)

    # Save the figure as png file with resolution of 300 dpi
    outfp = "results/" + colname + ".png"
    plt.savefig(outfp, dpi=500)

    print("Exported {} accessibility map ..".format(colname))
