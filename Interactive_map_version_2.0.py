# Import the folium library for creating interactive maps
import folium
# Import plugins for more advanced features
from folium.plugins import Fullscreen, MiniMap, Draw, Geocoder

# --- 1. Create a base map ---
# Initialize a Folium map object
# 'location' sets the initial center coordinates (latitude, longitude)
# 'zoom_start' sets the initial zoom level
# 'tiles' specifies the map tile style (e.g., OpenStreetMap, Stamen Terrain, CartoDB positron)
print("Creating a base map centered near London...")
m = folium.Map(location=[51.5074, -0.1278], zoom_start=10, tiles='OpenStreetMap')

# --- 2. Add Layer Control for toggling layers ---
# This is typically added at the end, but defining it early allows grouping
# FeatureGroup allows grouping related markers/polygons to be toggled together
markers_group = folium.FeatureGroup(name='London Landmarks').add_to(m)
shapes_group = folium.FeatureGroup(name='Area Features').add_to(m)
geojson_group = folium.FeatureGroup(name='Sample GeoJSON Data').add_to(m)


# --- 3. Add markers to the map within the 'markers_group' ---
# Markers are points on the map, often with popups showing information

# Example 1: London Eye
print("Adding markers to the map...")
folium.Marker(
    location=[51.5033, -0.1196], # Latitude, Longitude
    popup="<b>London Eye</b><br>Famous Ferris wheel on the South Bank of the River Thames.", # Text that appears when clicked
    tooltip="Click for info" # Text that appears on hover
).add_to(markers_group) # Add to the markers_group

# Example 2: British Museum
folium.Marker(
    location=[51.5194, -0.1269],
    popup="<b>British Museum</b><br>World-renowned museum of human history, art and culture.",
    icon=folium.Icon(color='red', icon='info-sign') # Custom icon with a specific color and symbol
).add_to(markers_group) # Add to the markers_group

# Example 3: Buckingham Palace with a custom icon
folium.Marker(
    location=[51.5014, -0.1419],
    popup="<b>Buckingham Palace</b><br>The King's official London residence.",
    icon=folium.Icon(color='purple', icon='home', prefix='fa') # Using Font Awesome icon 'home'
).add_to(markers_group) # Add to the markers_group


# --- 4. Add a CircleMarker for an area of interest within 'shapes_group' ---
# Circle markers can represent areas or points with a defined radius
print("Adding a circle marker...")
folium.CircleMarker(
    location=[51.51, -0.09], # Center of the circle
    radius=50, # Radius in pixels
    popup="City of London Financial District",
    color='#3186cc', # Border color
    fill=True,
    fill_color='#3186cc', # Fill color
    fill_opacity=0.4 # Transparency of the fill
).add_to(shapes_group) # Add to the shapes_group


# --- 5. Add a simple Polygon (e.g., representing a small park area) within 'shapes_group' ---
# Polygons require a list of coordinates that define its boundaries
print("Adding a polygon...")
folium.Polygon(
    locations=[
        [51.509, -0.10],
        [51.509, -0.09],
        [51.508, -0.09],
        [51.508, -0.10],
        [51.509, -0.10] # Close the polygon
    ],
    color='green',
    weight=3,
    fill=True,
    fill_color='lightgreen',
    fill_opacity=0.6,
    popup="Small Park Area"
).add_to(shapes_group) # Add to the shapes_group


# --- 6. Add a sample GeoJSON layer ---
# GeoJSON is a format for encoding a variety of geographic data structures.
# Here's a simple example for a polygon. In a real application, this would come from a file or API.
print("Adding a GeoJSON layer...")
sample_geojson_data = {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "properties": {
          "name": "Sample Area 1",
          "description": "An example polygon from GeoJSON",
          "fillColor": "#ff0000",
          "strokeColor": "#ff0000"
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [
              [-0.15, 51.50],
              [-0.12, 51.50],
              [-0.12, 51.48],
              [-0.15, 51.48],
              [-0.15, 51.50]
            ]
          ]
        }
      }
    ]
}

folium.GeoJson(
    sample_geojson_data,
    name='Sample GeoJSON Polygon',
    tooltip=folium.features.GeoJsonTooltip(fields=['name', 'description']),
    style_function=lambda x: {
        'fillColor': x['properties']['fillColor'] if 'fillColor' in x['properties'] else '#0000ff',
        'color': x['properties']['strokeColor'] if 'strokeColor' in x['properties'] else '#0000ff',
        'weight': 3,
        'fillOpacity': 0.5
    }
).add_to(geojson_group) # Add to the geojson_group

# --- 7. Add plugins for enhanced interactivity ---

# Add Fullscreen button
print("Adding Fullscreen plugin...")
Fullscreen().add_to(m)

# Add MiniMap (overview map)
print("Adding MiniMap plugin...")
MiniMap().add_to(m)

# Add Draw tools
# This allows users to draw markers, polygons, circles, rectangles, and lines on the map.
# Drawn items can be printed to the console (in the browser's developer tools)
print("Adding Draw plugin...")
Draw(export=True).add_to(m) # export=True allows downloading drawn features as GeoJSON

# Add Geocoder (search bar)
print("Adding Geocoder plugin...")
# 'position' can be 'topleft', 'topright', 'bottomleft', 'bottomright'
Geocoder(position='topleft').add_to(m)

# Add the Layer Control to the map. This needs to be added AFTER all FeatureGroups
# so it can properly list them.
print("Adding Layer Control...")
folium.LayerControl().add_to(m)


# --- 8. Save the map to an HTML file ---
output_file = 'interactive_map.html'
m.save(output_file)
print(f"Enhanced map successfully generated and saved to '{output_file}'")
