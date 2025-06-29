# Import the folium library for creating interactive maps
import folium

# --- 1. Create a base map ---
# Initialize a Folium map object
# 'location' sets the initial center coordinates (latitude, longitude)
# 'zoom_start' sets the initial zoom level
# 'tiles' specifies the map tile style (e.g., OpenStreetMap, Stamen Terrain, CartoDB positron)
print("Creating a base map centered near London...")
m = folium.Map(location=[51.5074, -0.1278], zoom_start=10, tiles='OpenStreetMap')

# --- 2. Add markers to the map ---
# Markers are points on the map, often with popups showing information

# Example 1: London Eye
print("Adding markers to the map...")
folium.Marker(
    location=[51.5033, -0.1196], # Latitude, Longitude
    popup="<b>London Eye</b><br>Famous Ferris wheel on the South Bank of the River Thames.", # Text that appears when clicked
    tooltip="Click for info" # Text that appears on hover
).add_to(m)

# Example 2: British Museum
folium.Marker(
    location=[51.5194, -0.1269],
    popup="<b>British Museum</b><br>World-renowned museum of human history, art and culture.",
    icon=folium.Icon(color='red', icon='info-sign') # Custom icon with a specific color and symbol
).add_to(m)

# Example 3: Buckingham Palace with a custom icon
folium.Marker(
    location=[51.5014, -0.1419],
    popup="<b>Buckingham Palace</b><br>The King's official London residence.",
    icon=folium.Icon(color='purple', icon='home', prefix='fa') # Using Font Awesome icon 'home'
).add_to(m)

# --- 3. Add a CircleMarker for an area of interest ---
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
).add_to(m)


# --- 4. Add a simple Polygon (e.g., representing a small park area) ---
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
).add_to(m)


# --- 5. Save the map to an HTML file ---
output_file = 'interactive_map.html'
m.save(output_file)
print(f"Map successfully generated and saved to '{output_file}'")

