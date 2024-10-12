from flask import Flask, render_template
import folium
import rasterio

app = Flask(__name__)

# Path to GeoTIFF file
GEO_TIFF_FILE = 'static/ltl_cayman_BROWSE.tif'

@app.route('/')
def index():
    # Use Rasterio to read GeoTIFF file
    with rasterio.open(GEO_TIFF_FILE) as src:
        bounds = src.bounds  # Get bounds of GeoTIFF file
    
    # Calculate center of bounds for map
    center = [(bounds.top + bounds.bottom) / 2, (bounds.left + bounds.right) / 2]

    # Create a folium map centered on GeoTIFF
    my_map = folium.Map(location=center, zoom_start=13)

    # Add GeoTIFF file as a layer
    folium.raster_layers.ImageOverlay(
        image=GEO_TIFF_FILE,
        bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
        opacity=0.6,
        interactive=True,
    ).add_to(my_map)

    # Save map as an HTML file
    my_map.save('templates/map.html')

    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
