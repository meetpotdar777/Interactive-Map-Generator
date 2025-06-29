# Import the folium library for creating interactive maps
import folium
# Import plugins for more advanced features
from folium.plugins import Fullscreen, MiniMap, Draw, Geocoder, MousePosition, MeasureControl
# Import pandas for data manipulation, especially for Choropleth data
import pandas as pd
# Import branca for colormaps
from branca.colormap import linear

# --- 1. Create a base map ---
# Initialize a Folium map object
# 'location' sets the initial center coordinates (latitude, longitude)
# 'zoom_start' sets the initial zoom level
# 'tiles' specifies the initial map tile style
print("Creating a base map centered near London...")
m = folium.Map(
    location=[51.5074, -0.1278],
    zoom_start=10,
    tiles='OpenStreetMap',
    attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' # Added attribution
)

# --- 2. Add multiple Tile Layers for base map switching ---
# These layers will be available through the LayerControl
print("Adding additional tile layers...")
folium.TileLayer('CartoDB positron', name='Light Mode', attr='&copy; <a href="https://carto.com/attributions">CartoDB</a>').add_to(m)
folium.TileLayer('CartoDB dark_matter', name='Dark Mode', attr='&copy; <a href="https://carto.com/attributions">CartoDB</a>').add_to(m)
folium.TileLayer('Stamen Toner', name='Toner', attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors').add_to(m)
folium.TileLayer('Stamen Terrain', name='Terrain', attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors').add_to(m)


# --- 3. Add FeatureGroups for better layer organization ---
# FeatureGroup allows grouping related markers/polygons to be toggled together in LayerControl
markers_group = folium.FeatureGroup(name='London Landmarks').add_to(m)
shapes_group = folium.FeatureGroup(name='Area Features').add_to(m)
geojson_group = folium.FeatureGroup(name='Sample GeoJSON Data').add_to(m)
# For Choropleth, we will add it directly to the map, but LayerControl will still manage its visibility by name.
# So we don't necessarily need a specific FeatureGroup for Choropleth if it's added directly to the map,
# but we'll keep the variable name for clarity if you wish to group other choropleths later.


# --- 4. Add markers to the map within the 'markers_group' ---
# Markers are points on the map, often with popups showing information

# Example 1: London Eye
print("Adding markers to the map...")
folium.Marker(
    location=[51.5033, -0.1196], # Latitude, Longitude
    popup=folium.Popup("<b>London Eye</b><br><i>Famous Ferris wheel</i><br><img src='https://placehold.co/100x60/ADD8E6/000000?text=Eye' width='100px'>", max_width=300), # Popup with HTML and image
    tooltip="Click for London Eye info" # Text that appears on hover
).add_to(markers_group) # Add to the markers_group

# Example 2: British Museum with custom Font Awesome icon
folium.Marker(
    location=[51.5194, -0.1269],
    popup="<b>British Museum</b><br>World-renowned museum of human history, art and culture.",
    icon=folium.Icon(color='red', icon='info-sign', prefix='glyphicon'), # Using 'glyphicon' prefix for info-sign
    tooltip="British Museum"
).add_to(markers_group)

# Example 3: Buckingham Palace with a custom image icon
print("Adding custom image marker...")
folium.Marker(
    location=[51.5014, -0.1419],
    popup=folium.Popup("<b>Buckingham Palace</b><br>The King's official London residence.<br><img src='https://placehold.co/100x60/FFF8DC/000000?text=Palace' width='100px'>", max_width=300),
    icon=folium.CustomIcon(
        icon_image='https://placehold.co/32x32/FFD700/000000?text=👑', # Placeholder for a crown icon
        icon_size=(32, 32),
        icon_anchor=(16, 32),
        popup_anchor=(0, -20)
    ),
    tooltip="Buckingham Palace"
).add_to(markers_group)


# --- 5. Add a CircleMarker for an area of interest within 'shapes_group' ---
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
).add_to(shapes_group)


# --- 6. Add a simple Polygon within 'shapes_group' ---
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
).add_to(shapes_group)


# --- 7. Add a sample GeoJSON layer (FeatureCollection) within 'geojson_group' ---
# GeoJSON is a format for encoding a variety of geographic data structures.
print("Adding a GeoJSON layer...")
sample_geojson_data = {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "properties": {
          "name": "Hyde Park",
          "description": "A large park in Central London",
          "fillColor": "#6a0dad", # Purple
          "strokeColor": "#6a0dad"
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [
              [-0.18, 51.51],
              [-0.15, 51.51],
              [-0.15, 51.50],
              [-0.18, 51.50],
              [-0.18, 51.51]
            ]
          ]
        }
      },
      {
        "type": "Feature",
        "properties": {
          "name": "Westminster Bridge",
          "description": "Bridge over the River Thames",
          "color": "#000000", # Black line
          "weight": 5
        },
        "geometry": {
          "type": "LineString",
          "coordinates": [
            [-0.122, 51.500],
            [-0.118, 51.501]
          ]
        }
      }
    ]
}

folium.GeoJson(
    sample_geojson_data,
    name='Sample GeoJSON Features',
    tooltip=folium.features.GeoJsonTooltip(fields=['name', 'description']),
    style_function=lambda x: {
        'fillColor': x['properties'].get('fillColor', '#0000ff'),
        'color': x['properties'].get('strokeColor', '#0000ff') if x['geometry']['type'] == 'Polygon' else x['properties'].get('color', '#0000ff'),
        'weight': x['properties'].get('weight', 3),
        'fillOpacity': x['properties'].get('fillOpacity', 0.5) if x['geometry']['type'] == 'Polygon' else 0, # Only fill for polygons
    }
).add_to(geojson_group)


# --- 8. Add a Choropleth Map (sample data for simplified 'boroughs') ---
print("Adding a choropleth map...")

# Simplified GeoJSON for two "mock boroughs" in London. In reality, you'd load a detailed GeoJSON file.
# Note: Ensure the 'id' field in geo_data matches 'key_on' in folium.Choropleth
simplified_london_boroughs = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "BoroughA",  # This ID must match the 'feature_id' in your data
            "properties": {"name": "Mock Borough A"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-0.05, 51.52], [-0.03, 51.52], [-0.03, 51.50], [-0.05, 51.50], [-0.05, 51.52]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "BoroughB",
            "properties": {"name": "Mock Borough B"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-0.08, 51.53], [-0.06, 51.53], [-0.06, 51.51], [-0.08, 51.51], [-0.08, 51.53]
                ]]
            }
        }
    ]
}

# Corresponding population data for the simplified boroughs
# 'feature_id' here matches the 'id' in the GeoJSON features
population_data = [
    {'feature_id': 'BoroughA', 'population': 80000},
    {'feature_id': 'BoroughB', 'population': 120000}
]

# Convert population_data to a pandas DataFrame to ensure correct data types for Choropleth
population_df = pd.DataFrame(population_data)

# Create a colormap for the choropleth
# It's important to use the min/max of the 'population' column from the DataFrame
colormap = linear.YlGnBu_09.scale(population_df['population'].min(), population_df['population'].max())

# Create the Choropleth layer
choropleth_layer = folium.Choropleth(
    geo_data=simplified_london_boroughs,
    name='Sample Population Density',
    data=population_df, # Pass the pandas DataFrame here
    columns=['feature_id', 'population'],
    key_on='feature.id', # Link data to GeoJSON features by their 'id' property
    fill_color='YlGnBu', # Color scheme (Yellow-Green-Blue)
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Population (Sample Data)',
    highlight=True, # Highlight feature on hover
    # Tooltip for displaying data on hover for choropleth regions
    tooltip=folium.features.GeoJsonTooltip(fields=['name', 'population'], aliases=['Borough:', 'Population:'], localize=True, sticky=False)
)

# Add the choropleth layer directly to the map to satisfy the assertion
# This is the primary fix for "Choropleth must be added to a Map object."
choropleth_layer.add_to(m)

# You can still add it to the FeatureGroup if you want it explicitly nested in LayerControl
# However, for Choropleth, adding directly to map and relying on LayerControl's auto-discovery
# of named layers is often more robust.
# If you absolutely need it nested in the choropleth_group for a specific reason,
# you would generally do: choropleth_layer.add_to(choropleth_group) INSTEAD of add_to(m),
# but this can sometimes lead to the assertion error with certain Folium versions/setups.
# For now, we prioritize fixing the assertion.


# Add the colormap to the map so its legend is visible
m.add_child(colormap)


# --- 9. Add various plugins for enhanced interactivity ---

# Add Fullscreen button to expand the map to full screen
print("Adding Fullscreen plugin...")
Fullscreen().add_to(m)

# Add MiniMap (an overview map in the corner)
print("Adding MiniMap plugin...")
MiniMap(toggle_display=True).add_to(m) # toggle_display allows collapsing the minimap

# Add Draw tools
# This allows users to draw markers, polygons, circles, rectangles, and lines on the map.
# Drawn items can be exported as GeoJSON.
print("Adding Draw plugin...")
Draw(
    export=True, # Allows downloading drawn features as GeoJSON
    filename='drawn_features.geojson', # Default filename for export
    position='topleft',
    draw_options={
        'polyline': {'allowIntersection': False}, # Prevent polyline self-intersections
        'polygon': {'allowIntersection': False}, # Prevent polygon self-intersections
        'rectangle': True,
        'circle': True,
        'marker': True,
        'circlemarker': True
    },
    edit_options={
        'edit': True,
        'remove': True
    }
).add_to(m)

# Add Geocoder (search bar) to search for locations on the map
print("Adding Geocoder plugin...")
Geocoder(position='topright').add_to(m)

# Add Mouse Position display to show coordinates of the mouse pointer
print("Adding MousePosition plugin...")
MousePosition(
    position='bottomright',
    separator=' | ',
    empty_string='LatLng',
    lng_first=False,
    num_digits=4,
    prefix='Coordinates: '
).add_to(m)

# Add Measure Control to measure distances and areas on the map
print("Adding MeasureControl plugin...")
MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles').add_to(m)

# Add LatLngPopup: Clicking on the map will display the latitude and longitude
print("Adding LatLngPopup...")
m.add_child(folium.LatLngPopup())


# --- 10. Add the Layer Control to the map ---
# This needs to be added AFTER all TileLayers and FeatureGroups
# so it can properly list them and allow toggling visibility.
print("Adding Layer Control...")
folium.LayerControl().add_to(m)


# --- 11. Save the map to an HTML file ---
output_file = 'interactive_map.html'
m.save(output_file)
print(f"Advanced map successfully generated and saved to '{output_file}'")
