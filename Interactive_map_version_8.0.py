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
import webbrowser # To automatically open the HTML file

# --- 1. Create a base map ---
# Initialize a Folium map object
# 'location' sets the initial center coordinates (latitude, longitude)
# 'zoom_start' sets the initial zoom level
# 'tiles' specifies the initial map tile style
print("Creating a base map centered near London (global weather enabled)...")
m = folium.Map(
    location=[51.5074, -0.1278], # Centered on London for a more general starting point
    zoom_start=7,
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
markers_group = folium.FeatureGroup(name='Sample Landmarks').add_to(m)
shapes_group = folium.FeatureGroup(name='Area Features').add_to(m)
geojson_group = folium.FeatureGroup(name='Sample GeoJSON Data').add_to(m)
heatmap_group = folium.FeatureGroup(name='Simulated Heatmap').add_to(m)
marker_cluster_group = folium.FeatureGroup(name='Clustered Locations').add_to(m)
timestamp_geojson_group = folium.FeatureGroup(name='Temporal Data (Timestamps)').add_to(m)
image_overlay_group = folium.FeatureGroup(name='Historical Map Overlay').add_to(m)
random_points_group = folium.FeatureGroup(name='Random Points').add_to(m)
clickable_regions_group = folium.FeatureGroup(name='Clickable Regions').add_to(m)
weather_reports_group = folium.FeatureGroup(name='Weather Reports').add_to(m)

# New FeatureGroup for weather overlays
weather_overlays_group = folium.FeatureGroup(name='Weather Overlays').add_to(m)


# --- 4. Add markers to the map within the 'markers_group' ---
# Markers are points on the map, often with popups showing information
print("Adding sample markers...")
# Example 1: Red Fort, Delhi - Keeping Indian landmarks for variety, now on a global map
folium.Marker(
    location=[28.6562, 77.2410], # Latitude, Longitude for Red Fort
    popup=folium.Popup("<b>Red Fort</b><br><i>Historic fort in Delhi, India</i><br><img src='https://placehold.co/100x60/ADD8E6/000000?text=RedFort' width='100px'>", max_width=300),
    tooltip="Click for Red Fort info"
).add_to(markers_group)

# Example 2: Gateway of India, Mumbai
folium.Marker(
    location=[18.9220, 72.8347],
    popup="<b>Gateway of India</b><br>Iconic arch monument in Mumbai, India.",
    icon=folium.Icon(color='blue', icon='camera', prefix='fa'),
    tooltip="Gateway of India"
).add_to(markers_group)

# Example 3: Taj Mahal, Agra
folium.Marker(
    location=[27.1751, 78.0421],
    popup=folium.Popup("<b>Taj Mahal</b><br>Ivory-white marble mausoleum in Agra, India.<br><img src='https://placehold.co/100x60/F0F8FF/000000?text=TajMahal' width='100px'>", max_width=300),
    icon=folium.CustomIcon(
        icon_image='https://placehold.co/32x32/FFD700/000000?text=🕌', # Placeholder for a mosque icon
        icon_size=(32, 32),
        icon_anchor=(16, 32),
        popup_anchor=(0, -20)
    ),
    tooltip="Taj Mahal"
).add_to(markers_group)


# --- 5. Add a CircleMarker for an area of interest within 'shapes_group' ---
print("Adding a circle marker...")
folium.CircleMarker(
    location=[28.5245, 77.1855], # Example: Qutub Minar area in Delhi
    radius=50, # Radius in pixels
    popup="Qutub Minar Area",
    color='#3186cc', # Border color
    fill=True,
    fill_color='#3186cc', # Fill color
    fill_opacity=0.4 # Transparency of the fill
).add_to(shapes_group)


# --- 6. Add a simple Polygon within 'shapes_group' ---
print("Adding a polygon...")
folium.Polygon(
    locations=[
        [28.70, 77.10],
        [28.70, 77.25],
        [28.55, 77.25],
        [28.55, 77.10],
        [28.70, 77.10] # Close the polygon
    ],
    color='purple',
    weight=3,
    fill=True,
    fill_color='lightpink',
    fill_opacity=0.6,
    popup="Sample City Zone (India)"
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
          "name": "Connaught Place",
          "description": "One of the largest financial, commercial and business centers in New Delhi, India.",
          "fillColor": "#008080", # Teal
          "strokeColor": "#008080"
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [
              [77.21, 28.63],
              [77.22, 28.63],
              [77.22, 28.62],
              [77.21, 28.62],
              [77.21, 28.63]
            ]
          ]
        }
      },
      {
        "type": "Feature",
        "properties": {
          "name": "India Gate",
          "description": "War memorial and iconic landmark in Delhi, India.",
          "color": "#FF4500", # Orange Red
          "weight": 5
        },
        "geometry": {
          "type": "Point",
          "coordinates": [77.2295, 28.6129]
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
        'fillOpacity': x['properties'].get('fillOpacity', 0.5) if x['geometry']['type'] == 'Polygon' else 0,
    }
).add_to(geojson_group)


# --- 8. Add a Choropleth Map (sample data for regions) ---
print("Adding a choropleth map...")

# Using simplified global regions now
simplified_global_regions = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "Europe",
            "properties": {"name": "Sample Region: Europe"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [0.0, 50.0], [10.0, 50.0], [10.0, 45.0], [0.0, 45.0], [0.0, 50.0]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "NorthAmerica",
            "properties": {"name": "Sample Region: North America"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-100.0, 40.0], [-90.0, 40.0], [-90.0, 35.0], [-100.0, 35.0], [-100.0, 40.0]
                ]]
            }
        }
    ]
}

data_for_global_regions = [
    {'feature_id': 'Europe', 'value': 180},
    {'feature_id': 'NorthAmerica', 'value': 220}
]

data_df = pd.DataFrame(data_for_global_regions)
colormap = linear.YlGnBu_09.scale(data_df['value'].min(), data_df['value'].max())

choropleth_layer = folium.Choropleth(
    geo_data=simplified_global_regions,
    name='Sample Global Data (Intensity)',
    data=data_df,
    columns=['feature_id', 'value'],
    key_on='feature.id',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Data Value (Sample)',
    highlight=True,
    tooltip=folium.features.GeoJsonTooltip(fields=['name', 'value'], aliases=['Region:', 'Value:'], localize=True, sticky=False)
)

choropleth_layer.add_to(m)
m.add_child(colormap)


# --- 9. Add a Heatmap Layer ---
print("Adding a Heatmap layer...")
# Simulated data points for a heatmap globally
heatmap_data = []
for _ in range(100): # More points for global distribution
    lat = random.uniform(-60.0, 80.0) # Latitude range for global
    lon = random.uniform(-180.0, 180.0) # Longitude range for global
    intensity = random.uniform(0.1, 1.0)
    heatmap_data.append([lat, lon, intensity])

HeatMap(heatmap_data).add_to(heatmap_group)


# --- 10. Add a Marker Cluster Layer ---
print("Adding a Marker Cluster layer...")
# Simulated locations for marker clustering globally
cluster_locations = []
for _ in range(100): # More points for global distribution
    lat = random.uniform(-60.0, 80.0)
    lon = random.uniform(-180.0, 180.0)
    cluster_locations.append([lat, lon])

marker_cluster = MarkerCluster(name='Clustered Locations').add_to(marker_cluster_group)
for i, loc in enumerate(cluster_locations):
    folium.Marker(loc, tooltip=f"Clustered Point {i+1}<br>Lat: {loc[0]:.2f}, Lng: {loc[1]:.2f}").add_to(marker_cluster)


# --- 11. Add a Timestamped GeoJSON Layer ---
print("Adding a Timestamped GeoJSON layer...")
# Sample GeoJSON data with a 'times' property for temporal visualization globally
timestamped_geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [0.0, 0.0] # Null Island
            },
            "properties": {
                "times": ["2024-01-01T00:00:00Z", "2024-02-01T00:00:00Z", "2024-03-01T00:00:00Z"],
                "icon": "circle",
                "iconstyle": {
                    "fillOpacity": 0.8, "stroke": "false", "radius": 8, "fillColor": "blue"
                },
                "popup": "<b>January Event:</b> Global pinpoint.",
                "time_property": "times"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [15.0, 45.0] # Central Europe
            },
            "properties": {
                "times": ["2024-02-15T00:00:00Z", "2024-03-15T00:00:00Z", "2024-04-15T00:00:00Z"],
                "icon": "circle",
                "iconstyle": {
                    "fillOpacity": 0.8, "stroke": "false", "radius": 8, "fillColor": "red"
                },
                "popup": "<b>February Event:</b> European activity.",
                "time_property": "times"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [-70.0, 40.0],
                    [-75.0, 35.0]
                ]
            },
            "properties": {
                "times": ["2024-01-20T00:00:00Z", "2024-02-20T00:00:00Z", "2024-03-20T00:00:00Z", "2024-04-20T00:00:00Z"],
                "icon": "polyline",
                "iconstyle": {
                    "color": "orange", "weight": 5, "opacity": 0.7
                },
                "popup": "<b>March Movement:</b> Path taken over North America.",
                "time_property": "times"
            }
        }
    ]
}

timestamped_geojson_layer = TimestampedGeoJson(
    timestamped_geojson_data,
    period='P1M',
    auto_play=True,
    loop=True,
    transition_time=700,
    date_options='YYYY-MM-DD HH:mm:ss',
)
timestamped_geojson_layer.add_to(m)


# --- 12. Add an Image Overlay ---
print("Adding an Image Overlay...")
# Example: A hypothetical historical map section of the world
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/World_map_1689.jpg/800px-World_map_1689.jpg"
image_bounds = [[-80.0, -180.0], [80.0, 180.0]] # Full global coverage approx
folium.raster_layers.ImageOverlay(
    image=image_url,
    bounds=image_bounds,
    opacity=0.6,
    name='1689 World Map Overlay'
).add_to(image_overlay_group)


# --- 13. Add Random Points with Dynamic Popups/Tooltips & Data-Driven Icons ---
print("Adding random points with dynamic popups and data-driven icons globally...")
for i in range(50): # More points for global distribution
    lat = random.uniform(-60.0, 80.0)
    lon = random.uniform(-180.0, 180.0)
    value = random.randint(10, 100)

    if value > 80:
        icon_color = 'green'
        icon_name = 'cloud-sun'
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
        icon=folium.Icon(color=icon_color, icon=icon_name, prefix='fa')
    ).add_to(random_points_group)


# --- 14. Add Clickable Regions with Custom Popups (using onEachFeature for GeoJson) ---
print("Adding clickable regions with custom popups globally...")
clickable_regions_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "Amazon Rainforest",
                "info": "Vast tropical rainforest in South America, known for its biodiversity.",
                "type": "Biome"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-70.0, -10.0], [-50.0, -10.0], [-50.0, 0.0], [-70.0, 0.0], [-70.0, -10.0]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Mount Everest",
                "info": "Earth's highest mountain above sea level, located in the Himalayas.",
                "type": "Mountain"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [86.925, 27.988]
            }
        }
    ]
}

def clickable_style_function(feature):
    return {
        'fillColor': '#228B22' if feature['properties']['type'] == 'Biome' else '#D3D3D3', # Forest Green or Light Gray
        'color': 'white',
        'weight': 2,
        'fillOpacity': 0.6
    }

folium.GeoJson(
    clickable_regions_geojson,
    name='Clickable Regions',
    style_function=clickable_style_function,
    highlight_function=lambda x: {'fillColor': '#FFFF00', 'color': 'black', 'weight': 5, 'dashArray': '10, 5'},
    tooltip=folium.features.GeoJsonTooltip(fields=['name', 'info']),
    control=True
).add_to(clickable_regions_group)


# --- 15. Add Custom JavaScript Interaction (includes reverse geocoding on click, Weather API Integration, and more) ---
print("Adding custom JavaScript interaction with reverse geocoding, weather API, and control styling...")
js_code = f"""
// ** IMPORTANT: Replace 'YOUR_OPENWEATHERMAP_API_KEY' with your actual API key **
// You can get a free API key from OpenWeatherMap: https://openweathermap.org/api
const OPENWEATHERMAP_API_KEY = ''; // <<< PUT YOUR API KEY HERE

// Function to get address from coordinates using Nominatim (OpenStreetMap)
function getAddressFromLatLng(lat, lng, callback) {{
    var url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${{lat}}&lon=${{lng}}&zoom=18&addressdetails=1`;
    fetch(url)
        .then(response => response.json())
        .then(data => {{
            if (data.display_name) {{
                callback(data.display_name);
            }} else {{
                callback("Address not found.");
            }}
        }})
        .catch(error => {{
            console.error("Error during reverse geocoding:", error);
            callback("Error getting address.");
        }});
}}

// Function to get weather data for given coordinates
function getWeatherData(lat, lon, weatherDisplayElement) {{
    if (!OPENWEATHERMAP_API_KEY) {{
        weatherDisplayElement.innerHTML = '<div style="color: red; font-weight: bold;">Error: Please provide your OpenWeatherMap API Key in the code.</div>';
        return;
    }}

    const weatherApiUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${{lat}}&lon=${{lon}}&appid=${{OPENWEATHERMAP_API_KEY}}&units=metric`;
    weatherDisplayElement.innerHTML = 'Fetching weather...<br><div class="spinner-border spinner-border-sm text-info" role="status"><span class="visually-hidden">Loading...</span></span></div>'; // Added spinner

    fetch(weatherApiUrl)
        .then(response => {{
            if (!response.ok) {{
                if (response.status === 401) {{
                    throw new Error('Unauthorized: Invalid API key. Please check your OpenWeatherMap API Key.');
                }}
                throw new Error(`HTTP error! status: ${{response.status}}`);
            }}
            return response.json();
        }})
        .then(data => {{
            const city = data.name;
            const temp = data.main.temp;
            const description = data.weather[0].description;
            const humidity = data.main.humidity;
            const windSpeed = data.wind.speed;
            const icon = data.weather[0].icon;

            const weatherHtml = `
                <div style="font-family: 'Arial', sans-serif; padding: 5px; background-color: #e0f2f7; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                    <b>${{city}}</b><br>
                    <img src="http://openweathermap.org/img/wn/${{icon}}@2x.png" alt="${{description}}" style="vertical-align: middle; width: 50px; height: 50px;">
                    ${{temp.toFixed(1)}}°C, ${{description}}<br>
                    Humidity: ${{humidity}}%<br>
                    Wind: ${{windSpeed}} m/s
                </div>
            `;
            weatherDisplayElement.innerHTML = weatherHtml;
        }})
        .catch(error => {{
            console.error("Error fetching weather:", error);
            weatherDisplayElement.innerHTML = `<div style="color: red;">Error: ${{error.message}}. Could not retrieve weather.</div>`;
        }});
}}


// Access the map object using its internal Leaflet ID (m._leaflet_id) or global 'm' variable if defined
m.on('click', function(e) {{
    var lat = e.latlng.lat;
    var lng = e.latlng.lng;
    var message = "Map clicked at: Lat " + lat.toFixed(4) + ", Lng " + lng.toFixed(4);
    console.log(message); // Log to browser's developer console

    // Use reverse geocoding to get address
    getAddressFromLatLng(lat, lng, function(address) {{
        var popupContent = `You clicked here!<br>Lat: ${{lat.toFixed(4)}}<br>Lng: ${{lng.toFixed(4)}}<br>Address: ${{address}}`;
        L.popup()
            .setLatLng(e.latlng)
            .setContent(popupContent)
            .openOn(m);

        // Fetch and display weather in the weather control based on click location
        const weatherResultDiv = document.getElementById('weather-result');
        if (weatherResultDiv) {{
            getWeatherData(lat, lng, weatherResultDiv);
        }}
    }});
}});

// Custom button for toggling Heatmap layer (Top Right)
var customButtonHeatmap = L.control({{position: 'topright'}});
customButtonHeatmap.onAdd = function (map) {{
    var div = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
    div.innerHTML = '<button style="background-color: #f8f8f8; width: 30px; height: 30px; line-height: 30px; text-align: center; cursor: pointer; border: 1px solid #ccc; border-radius: 4px;" title="Toggle Simulated Heatmap"><i class="fa fa-fire"></i></button>';
    div.firstChild.onclick = function() {{
        var heatmapLayer = null;
        m.eachLayer(function(layer) {{
            if (layer.options && layer.options.name === 'Simulated Heatmap') {{
                heatmapLayer = layer;
            }}
        }});
        if (heatmapLayer) {{
            if (m.hasLayer(heatmapLayer)) {{
                m.removeLayer(heatmapLayer);
                console.log('Simulated Heatmap layer removed');
            }} else {{
                m.addLayer(heatmapLayer);
                console.log('Simulated Heatmap layer added');
            }}
        }}
    }};
    return div;
}};
customButtonHeatmap.addTo(m);

// --- Custom Weather Control (Top Right) ---
var weatherControl = L.control({{position: 'topright'}});
weatherControl.onAdd = function (map) {{
    var div = L.DomUtil.create('div', 'info legend leaflet-control', 'weather-control-panel');
    div.style.backgroundColor = 'white';
    div.style.padding = '10px';
    div.style.borderRadius = '5px';
    div.style.boxShadow = '0 1px 5px rgba(0,0,0,0.4)';
    div.style.width = '250px';
    div.style.pointerEvents = 'auto'; // Make it clickable/interactable
    div.style.marginTop = '40px'; // Offset from top to avoid overlapping with heatmap toggle

    div.innerHTML = `
        <h4 style="margin-top: 0; font-size: 1.1em; color: #333;"><i class="fa fa-cloud"></i> Weather Report</h4>
        <p style="font-size: 0.8em; margin-bottom: 5px; color: #666;">Click on map for local weather:</p>
        <div id="weather-result" style="font-size: 0.9em; min-height: 50px; border: 1px solid #eee; padding: 5px; border-radius: 3px; background-color: #f9f9f9; display: flex; align-items: center; justify-content: center;">
            Click a location on the map.
        </div>
        <p style="font-size: 0.7em; color: #999; margin-top: 10px;">
            Powered by <a href="https://openweathermap.org/" target="_blank">OpenWeatherMap</a>. <br>
            <span style="color: red; font-weight: bold;">Remember to add your API key in the code!</span>
        </p>
    `;

    L.DomEvent.disableClickPropagation(div);
    return div;
}};
weatherControl.addTo(m);


// Advanced JS for hover styling on 'Sample GeoJSON Features' polygons (client-side)
m.eachLayer(function (layer) {{
    if (layer.feature && layer.feature.properties && (layer.feature.properties.name === 'Connaught Place' || layer.feature.properties.name === 'Hyde Park') && layer.feature.geometry.type === 'Polygon') {{
        var originalStyle = layer.options.style(layer.feature);
        layer.on('mouseover', function () {{
            layer.setStyle({{
                weight: 5,
                color: '#666',
                dashArray: '',
                fillOpacity: 0.7
            }});
        }});
        layer.on('mouseout', function () {{
            layer.setStyle(originalStyle);
        }});
    }}
}});

// JavaScript for 'Clickable Regions' GeoJSON popups and hover effects
m.eachLayer(function(layer) {{
    if (layer.feature && layer.feature.properties) {{
        var feature = layer.feature;
        if (feature.properties.name === 'Jaipur (Pink City)' || feature.properties.name === 'Goa Beaches' || feature.properties.name === 'Amazon Rainforest' || feature.properties.name === 'Mount Everest') {{
            var popupContent = `<b>${{feature.properties.name}}</b><br>${{feature.properties.info}}<br>Type: ${{feature.properties.type}}`;
            layer.bindPopup(popupContent);

            if (feature.geometry.type === 'Polygon') {{
                var originalFillColor = layer.options.fillColor;
                layer.on('mouseover', function () {{
                    layer.setStyle({{
                        fillColor: '#FFFFCC', // Light yellow on hover
                        weight: 3,
                        dashArray: '5, 5'
                    }});
                }});
                layer.on('mouseout', function () {{
                    layer.setStyle({{
                        fillColor: originalFillColor,
                        weight: 2,
                        dashArray: ''
                    }});
                }});
            }}
        }}
    }}
}});
"""
folium.Html(js_code).add_to(m)


# --- NEW: Weather Overlay Layers (Added using OpenWeatherMap API) ---
print("Adding OpenWeatherMap weather overlay layers...")

# IMPORTANT: Ensure you have your OpenWeatherMap API key configured in the JavaScript section above.
# These tile layers will not work without a valid API key.
openweathermap_api_key = '' # This is just a placeholder in Python, the JS one is used.

# Temperature layer
folium.TileLayer(
    tiles=f'https://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid={openweathermap_api_key}',
    attr='Weather data &copy; <a href="https://openweathermap.org/">OpenWeatherMap</a>',
    name='Temperature (ºC)',
    overlay=True,
    control=True,
    opacity=0.6 # Make it semi-transparent
).add_to(weather_overlays_group)

# Precipitation layer
folium.TileLayer(
    tiles=f'https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={openweathermap_api_key}',
    attr='Weather data &copy; <a href="https://openweathermap.org/">OpenWeatherMap</a>',
    name='Precipitation',
    overlay=True,
    control=True,
    opacity=0.6
).add_to(weather_overlays_group)

# Cloud layer
folium.TileLayer(
    tiles=f'https://tile.openweathermap.org/map/clouds_new/{{z}}/{{x}}/{{y}}.png?appid={openweathermap_api_key}',
    attr='Weather data &copy; <a href="https://openweathermap.org/">OpenWeatherMap</a>',
    name='Clouds',
    overlay=True,
    control=True,
    opacity=0.6
).add_to(weather_overlays_group)

# Wind speed layer
folium.TileLayer(
    tiles=f'https://tile.openweathermap.org/map/wind_new/{{z}}/{{x}}/{{y}}.png?appid={openweathermap_api_key}',
    attr='Weather data &copy; <a href="https://openweathermap.org/">OpenWeatherMap</a>',
    name='Wind Speed',
    overlay=True,
    control=True,
    opacity=0.6
).add_to(weather_overlays_group)


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

# Add Geocoder (search bar, top-left)
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


# --- 17. Add the Layer Control to the map ---
# This needs to be added AFTER all TileLayers and FeatureGroups
# so it can properly list them and allow toggling visibility.
print("Adding Layer Control...")
folium.LayerControl(position='bottomright').add_to(m)


# --- 18. Save the map to an HTML file ---
output_file = 'interactive_map.html'
m.save(output_file)
print(f"Advanced map successfully generated and saved to '{output_file}'")

# --- 19. Open the HTML file in the default web browser ---
webbrowser.open(output_file)

# The map is now ready with multiple features, plugins, and enhancements.
