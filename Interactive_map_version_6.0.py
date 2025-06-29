# Import the folium library for creating interactive maps
import folium
# Import plugins for more advanced features
from folium.plugins import (
    Fullscreen, MiniMap, Draw, Geocoder, MousePosition, MeasureControl,
    HeatMap, MarkerCluster, TimestampedGeoJson, LocateControl
)
# Import pandas for data manipulation, especially for Choropleth data
import pandas as pd
# Import branca for colormaps
from branca.colormap import linear
import json # To handle GeoJSON data with timestamps
import random # For generating random data for new features

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
heatmap_group = folium.FeatureGroup(name='Simulated Heatmap').add_to(m)
marker_cluster_group = folium.FeatureGroup(name='Clustered Locations').add_to(m)
timestamp_geojson_group = folium.FeatureGroup(name='Temporal Data (Timestamps)').add_to(m)
image_overlay_group = folium.FeatureGroup(name='Historical Map Overlay').add_to(m)
random_points_group = folium.FeatureGroup(name='Random Points').add_to(m)
clickable_regions_group = folium.FeatureGroup(name='Clickable Regions').add_to(m) # New group for clickable GeoJSON

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
        'color': x['properties'].get('strokeColor', '#0000ff'),
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
            "properties": {"name": "Mock Borough A", "population": 80000},
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
            "properties": {"name": "Mock Borough B", "population": 120000},
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
    name='Sample Population Density', # Name for LayerControl
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
choropleth_layer.add_to(m)


# Add the colormap to the map so its legend is visible
m.add_child(colormap)


# --- 9. Add a Heatmap Layer ---
print("Adding a Heatmap layer...")
# Simulated data points for a heatmap (latitude, longitude, intensity)
# These points represent areas of higher "intensity" (e.g., more incidents, higher density)
heatmap_data = [
    [51.50, -0.12, 0.5], # Central London, medium intensity
    [51.51, -0.13, 0.8], # West End, high intensity
    [51.505, -0.11, 0.6], # Medium intensity
    [51.49, -0.10, 0.9], # South Bank, very high intensity
    [51.52, -0.14, 0.7], # North London, high intensity
    [51.515, -0.125, 1.0], # Very high intensity hotspot
    [51.50, -0.08, 0.4], # East London, low intensity
    [51.51, -0.09, 0.7], # Medium-high intensity
    [51.505, -0.07, 0.5], # Medium intensity
    [51.53, -0.10, 0.6], # North-east, medium intensity
    [51.525, -0.095, 0.9], # High intensity
    # Adding some more diverse points
    [51.48, -0.05, 0.3], [51.47, -0.06, 0.2], # Further southeast, low
    [51.58, -0.01, 0.5], [51.57, 0.0, 0.4] # Far north, medium
]
HeatMap(heatmap_data).add_to(heatmap_group)


# --- 10. Add a Marker Cluster Layer ---
print("Adding a Marker Cluster layer...")
# Simulated locations for marker clustering
cluster_locations = [
    # Group 1
    [51.50, -0.05], [51.505, -0.055], [51.502, -0.048], [51.503, -0.051],
    # Group 2
    [51.55, -0.15], [51.552, -0.153], [51.551, -0.148], [51.548, -0.151],
    # Group 3
    [51.54, -0.16], [51.541, -0.162], [51.539, -0.158],
    # Scattered points
    [51.58, -0.02], [51.45, -0.2], [51.56, 0.05], [51.49, -0.01], [51.52, -0.03]
]
marker_cluster = MarkerCluster(name='Clustered Locations').add_to(marker_cluster_group)
for i, loc in enumerate(cluster_locations):
    folium.Marker(loc, tooltip=f"Clustered Point {i+1}<br>Lat: {loc[0]:.2f}, Lng: {loc[1]:.2f}").add_to(marker_cluster)


# --- 11. Add a Timestamped GeoJSON Layer ---
print("Adding a Timestamped GeoJSON layer...")
# Sample GeoJSON data with a 'times' property for temporal visualization
# Features will appear/disappear based on the time slider.
timestamped_geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-0.12, 51.5]
            },
            "properties": {
                "times": ["2024-01-01T00:00:00Z", "2024-02-01T00:00:00Z", "2024-03-01T00:00:00Z"],
                "icon": "circle", # Can be 'marker' or 'circle' or 'polyline'
                "iconstyle": {
                    "fillOpacity": 0.8, "stroke": "false", "radius": 8, "fillColor": "blue"
                },
                "popup": "<b>January Event:</b> Initial sighting.",
                "time_property": "times" # Explicitly define time property if not 'times'
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-0.1, 51.51]
            },
            "properties": {
                "times": ["2024-02-15T00:00:00Z", "2024-03-15T00:00:00Z", "2024-04-15T00:00:00Z"],
                "icon": "circle",
                "iconstyle": {
                    "fillOpacity": 0.8, "stroke": "false", "radius": 8, "fillColor": "red"
                },
                "popup": "<b>February Event:</b> Red dot appears.",
                "time_property": "times"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [-0.13, 51.50],
                    [-0.11, 51.505]
                ]
            },
            "properties": {
                "times": ["2024-01-20T00:00:00Z", "2024-02-20T00:00:00Z", "2024-03-20T00:00:00Z", "2024-04-20T00:00:00Z"],
                "icon": "polyline",
                "iconstyle": {
                    "color": "orange", "weight": 5, "opacity": 0.7
                },
                "popup": "<b>March Movement:</b> Path taken.",
                "time_property": "times"
            }
        }
    ]
}

# Create the TimestampedGeoJson layer
timestamped_geojson_layer = TimestampedGeoJson(
    timestamped_geojson_data,
    period='P1M', # Period between timestamps (e.g., P1D for 1 day, P1M for 1 month)
    auto_play=True,
    loop=True,
    transition_time=700, # 0.7 seconds per step
    date_options='YYYY-MM-DD HH:mm:ss',
)

# Add the timestamped_geojson_layer directly to the map
timestamped_geojson_layer.add_to(m)


# --- 12. Add an Image Overlay ---
print("Adding an Image Overlay...")
# Replace with a URL to an image you want to overlay.
# The bounds define the geographical coordinates for the image corners: [[south, west], [north, east]]
# You'd typically use a known image with defined geo-coordinates for precise alignment.
# Example: a hypothetical old map section of London
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/1843_London_Map_-_North_West_Quadrant_%28Stanford%29.jpg/800px-1843_London_Map_-_North_West_Quadrant_%28Stanford%29.jpg"
# These bounds are approximate for a specific section of London covered by the image.
# You would need precise GIS data for a real-world scenario.
image_bounds = [[51.505, -0.14], [51.52, -0.09]] # Approximate area covering parts of central London
folium.raster_layers.ImageOverlay(
    image=image_url,
    bounds=image_bounds,
    opacity=0.6, # Make it slightly transparent to see map underneath
    name='1843 London Map Overlay'
).add_to(image_overlay_group)


# --- 13. Add Random Points with Dynamic Popups/Tooltips & Data-Driven Icons ---
print("Adding random points with dynamic popups and data-driven icons...")
for i in range(20):
    lat = 51.45 + (random.random() * 0.15) # Random lat within a range
    lon = -0.2 + (random.random() * 0.15) # Random lon within a range
    value = random.randint(10, 100) # Example data value

    # Data-driven icon styling
    if value > 80:
        icon_color = 'green'
        icon_name = 'star'
        popup_text = f"High Value: {value}"
    elif value > 40:
        icon_color = 'orange'
        icon_name = 'info-circle'
        popup_text = f"Medium Value: {value}"
    else:
        icon_color = 'red'
        icon_name = 'exclamation-triangle'
        popup_text = f"Low Value: {value}"

    html_popup = f"""
    <h4>Random Point {i+1}</h4>
    <p>Value: <b>{value}</b></p>
    <p>Coordinates: {lat:.4f}, {lon:.4f}</p>
    <p>{popup_text}</p>
    <small>Data generated randomly.</small>
    """
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(html_popup, max_width=250),
        tooltip=f"Point {i+1} (Value: {value})",
        icon=folium.Icon(color=icon_color, icon=icon_name, prefix='fa') # Use Font Awesome icons
    ).add_to(random_points_group)


# --- 14. Add Clickable Regions with Custom Popups (using onEachFeature for GeoJson) ---
print("Adding clickable regions with custom popups...")
# Sample GeoJSON data for clickable regions
clickable_regions_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "Soho District",
                "info": "A lively entertainment and shopping district.",
                "type": "District"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-0.138, 51.515], [-0.13, 51.515], [-0.13, 51.509], [-0.138, 51.509], [-0.138, 51.515]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Trafalgar Square",
                "info": "Public square with Nelson's Column and famous fountains.",
                "type": "Landmark"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [-0.128, 51.507]
            }
        }
    ]
}

# Define a function to be executed for each feature
def style_function(feature):
    return {
        'fillColor': '#4CAF50' if feature['properties']['type'] == 'District' else '#FFC107',
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.5
    }

def on_each_feature(feature, layer):
    # Bind popup with dynamic content from feature properties
    popup_content = f"<b>{feature['properties']['name']}</b><br>{feature['properties']['info']}<br>Type: {feature['properties']['type']}"
    layer.bind_popup(popup_content)

    # Add hover interaction for polygons (highlight on hover)
    if feature['geometry']['type'] == 'Polygon':
        layer.on('mouseover', lambda x: layer.setStyle({'fillOpacity': 0.8, 'weight': 3}))
        layer.on('mouseout', lambda x: layer.setStyle({'fillOpacity': 0.5, 'weight': 2}))


folium.GeoJson(
    clickable_regions_geojson,
    name='Clickable Regions',
    style_function=style_function,
    highlight_function=lambda x: {'fillColor': '#00F', 'color': 'red', 'weight': 5, 'dashArray': '10, 5'}, # Highlight on hover for all GeoJson
    tooltip=folium.features.GeoJsonTooltip(fields=['name', 'info']),
    # 'on_each_feature' is a powerful way to add custom JS logic to each feature
    control=True # Ensure it appears in LayerControl
).add_to(clickable_regions_group)


# --- 15. Add Custom JavaScript Interaction (includes reverse geocoding on click) ---
# This adds a simple click listener to the map that logs coordinates to the browser console
# and attempts a reverse geocoding lookup.
print("Adding custom JavaScript interaction with reverse geocoding...")
js_code = """
// Function to get address from coordinates using Nominatim (OpenStreetMap)
function getAddressFromLatLng(lat, lng, callback) {
    var url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.display_name) {
                callback(data.display_name);
            } else {
                callback("Address not found.");
            }
        })
        .catch(error => {
            console.error("Error during reverse geocoding:", error);
            callback("Error getting address.");
        });
}

// Access the map object using its internal Leaflet ID (m._leaflet_id) or global 'm' variable if defined
m.on('click', function(e) {
    var lat = e.latlng.lat;
    var lng = e.latlng.lng;
    var message = "Map clicked at: Lat " + lat.toFixed(4) + ", Lng " + lng.toFixed(4);
    console.log(message); // Log to browser's developer console

    // Use reverse geocoding to get address
    getAddressFromLatLng(lat, lng, function(address) {
        var popupContent = `You clicked here!<br>Lat: ${lat.toFixed(4)}<br>Lng: ${lng.toFixed(4)}<br>Address: ${address}`;
        L.popup()
            .setLatLng(e.latlng)
            .setContent(popupContent)
            .openOn(m);
    });
});

// Custom button functionality (example: toggling a specific layer)
// This demonstrates adding a fully custom HTML button that interacts with the map.
var customButton = L.control({position: 'topright'});
customButton.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
    div.innerHTML = '<button style="background-color: #f8f8f8; width: 30px; height: 30px; line-height: 30px; text-align: center; cursor: pointer; border: 1px solid #ccc; border-radius: 4px;" title="Toggle Heatmap"><i class="fa fa-fire"></i></button>';
    div.firstChild.onclick = function() {
        // Find the heatmap layer by name and toggle its visibility
        var heatmapLayer = null;
        m.eachLayer(function(layer) {
            if (layer.options && layer.options.name === 'Simulated Heatmap') {
                heatmapLayer = layer;
            }
        });

        if (heatmapLayer) {
            if (m.hasLayer(heatmapLayer)) {
                m.removeLayer(heatmapLayer);
                console.log('Heatmap layer removed');
            } else {
                m.addLayer(heatmapLayer);
                console.log('Heatmap layer added');
            }
        }
    };
    return div;
};
customButton.addTo(m);

// Advanced JS for hover styling on GeoJSON polygons (client-side)
// This will make 'Sample GeoJSON Features' polygons highlight on hover with different styles
m.eachLayer(function (layer) {
    if (layer.feature && layer.feature.properties && layer.feature.properties.name === 'Hyde Park' && layer.feature.geometry.type === 'Polygon') {
        var originalStyle = layer.options.style(layer.feature);
        layer.on('mouseover', function () {
            layer.setStyle({
                weight: 5,
                color: '#666',
                dashArray: '',
                fillOpacity: 0.7
            });
        });
        layer.on('mouseout', function () {
            layer.setStyle(originalStyle); // Revert to original style
        });
    }
});
"""
folium.Html(js_code).add_to(m)


# --- 16. Add core plugins for enhanced interactivity (re-ordered for logical flow and placement) ---

# Add Fullscreen button to expand the map to full screen (top-left)
print("Adding Fullscreen plugin...")
Fullscreen(position='topleft').add_to(m)

# Add MiniMap (an overview map in the corner, bottom-right)
print("Adding MiniMap plugin...")
MiniMap(toggle_display=True, position='bottomright').add_to(m)

# Add Draw tools (bottom-left, which includes the export button)
print("Adding Draw plugin...")
Draw(
    export=True, # Allows downloading drawn features as GeoJSON
    filename='drawn_features.geojson', # Default filename for export
    position='bottomleft', # Explicitly placed Draw tools (with export) to bottom-left
    draw_options={
        'polyline': {'allowIntersection': False},
        'polygon': {'allowIntersection': False},
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

# Add Geocoder (search bar, top-left - to separate from Draw if it shifts)
print("Adding Geocoder plugin...")
Geocoder(position='topleft').add_to(m) # Explicitly placed search bar to top-left

# Add Locate Control (button to find user's current location, top-left)
print("Adding LocateControl plugin...")
LocateControl(position='topleft').add_to(m)


# Add Mouse Position display to show coordinates of the mouse pointer (bottom-right)
print("Adding MousePosition plugin...")
MousePosition(
    position='bottomright',
    separator=' | ',
    empty_string='LatLng',
    lng_first=False,
    num_digits=4,
    prefix='Coordinates: '
).add_to(m)

# Add Measure Control to measure distances and areas on the map (bottom-left, will stack with Draw)
print("Adding MeasureControl plugin...")
MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles').add_to(m)

# Add LatLngPopup: Clicking on the map will display the latitude and longitude (handled by custom JS now)
# This was commented out in previous versions because custom JS handles it, keeping it that way.


# --- 17. Add the Layer Control to the map ---
# This needs to be added AFTER all TileLayers and FeatureGroups
# so it can properly list them and allow toggling visibility.
print("Adding Layer Control...")
folium.LayerControl(position='bottomright').add_to(m) # Moved LayerControl to bottom-right


# --- 18. Save the map to an HTML file ---
output_file = 'interactive_map.html'
m.save(output_file)
print(f"Advanced map successfully generated and saved to '{output_file}'")
