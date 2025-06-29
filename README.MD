Interactive Map Generator with AI Insights 🗺️✨

This project generates a highly interactive HTML map using Python's folium library, integrating various mapping features, real-time weather overlays, and AI-powered location insights, including conceptual traffic information.

Features 🚀

The generated map includes a rich set of features for geographical data visualization and interaction:

Multiple Tile Layers: Switch between different base map styles (OpenStreetMap, CartoDB Positron/Dark Matter, Stamen Toner/Terrain). 🌍

Sample Landmarks: Predefined markers for iconic global locations with popups. 📍

Area Features: Circle markers and polygons to highlight specific regions. 🔵🔶

GeoJSON Data: Displays custom geographical data in GeoJSON format. 🔗

Choropleth Map: Visualizes data intensity across simplified global regions. 📊

Simulated Heatmap: Shows density of simulated data points across the globe. 🔥

Marker Clusters: Groups dense markers into clusters that expand on zoom. 🎯

Timestamped GeoJSON: Animates geographical data over time (e.g., events moving across regions). 🕰️

Historical Map Overlay: Overlays an old world map for historical context. 📜

Random Points (AI Powered): Randomly generated points across the map. Clicking on these (or any location) will trigger an AI-generated insight. 💡

Interesting Locations (AI Powered): Predefined major landmarks with custom icons. Clicking on these also triggers AI-generated insights. 🏛️

Clickable Regions: Interactive geographical polygons (e.g., Amazon Rainforest, Mount Everest) with custom popups and hover effects. 👆

Integrated Map Controls: 🎮

Fullscreen: Expand the map to fill the screen. 📺

MiniMap: A small overview map in the corner. 🗺️

Draw Tools: Allows drawing points, lines, polygons, circles, and rectangles, with an option to export drawn features as GeoJSON. ✍️

Geocoder (Search Bar): Search for locations directly on the map. 🔍

Locate Control: Finds and centers the map on your current geographical location. 🧭

Mouse Position: Displays live latitude and longitude of the mouse pointer. 🖱️

Measure Control: Measure distances and areas directly on the map. 📏

Weather Overlays (OpenWeatherMap): Toggle layers for Temperature, Precipitation, Clouds, and Wind Speed (requires OpenWeatherMap API Key). ☁️🌡️💧💨

AI-Powered Insights Panel: A custom control panel on the map that provides: 🧠

Local Weather Report: Fetches real-time weather for clicked locations or the map center. ☀️

AI Location Insight: Uses Google Gemini AI to provide a comprehensive description of any clicked location, including: 🗣️

Identified main city/region.

2-3 famous historical, cultural, or natural landmarks/characteristics.

A conceptual insight into potential traffic conditions or transportation aspects for that area (not real-time traffic).

AI Route Analysis: Allows setting start and end points to get an AI-generated conceptual description or analysis of a hypothetical journey between them. 🛣️

Toast Notifications: Provides non-intrusive feedback for user actions and API key warnings. 🍞

Requirements 🛠️

To run this project, you need:

Python 3.x 🐍

folium library

pandas library

branca library

json (built-in)

random (built-in)

webbrowser (built-in)

You can install the Python libraries using pip:

pip install folium pandas branca

API Keys (Crucial for Full Functionality) 🔑

The map's dynamic weather and AI insight features require API keys. You MUST replace the placeholder keys in the generated HTML's JavaScript section with your own valid keys.

OpenWeatherMap API Key: ☁️

Purpose: For fetching local weather data and enabling weather overlay layers.

Get it from: https://openweathermap.org/api (Free tier available).

Location in Code: Open the generated interactive_map.html file in a text editor. Look for the JavaScript block (usually towards the end, after the Python script has run) and find the line:

const OPENWEATHERMAP_API_KEY = ''; // <<< SET YOUR OPENWEATHERMAP API KEY HERE

Replace the empty single quotes ('') with your actual key.

Google Gemini API Key: ♊

Purpose: For AI-powered location insights and route analysis.

Get it from: Google AI Studio (Free tier available).

Location in Code: In the same JavaScript block within interactive_map.html, find the line:

const GEMINI_API_KEY = ''; // <<< SET YOUR GOOGLE GEMINI API KEY HERE

Replace the empty single quotes ('') with your actual key.

Warning: If these API keys are missing or invalid, the weather and AI sections of the map's "Map Insights" control will display error messages. ⚠️

How to Run ▶️

Save the Python Code: Save the provided Python script (e.g., interactive_map_generator.py).

Run the Python Script: Open your terminal or command prompt, navigate to the directory where you saved the script, and run it:

python interactive_map_generator.py

Open the Map: The script will print messages as it generates the map and will automatically open the interactive_map.html file in your default web browser once finished. 🌐

Insert API Keys: As mentioned above, open the interactive_map.html file (generated in the same directory as your Python script) in a text editor and insert your OpenWeatherMap and Google Gemini API keys into the specified JavaScript variables.

Refresh Browser: After saving changes to interactive_map.html, refresh your web browser to see the weather and AI features enabled. 🔄

Usage 🗺️👆

Layer Control: Use the layer control (usually at the bottom-right) to toggle different base maps and data layers (e.g., Heatmap, Marker Clusters, Weather Overlays). 📊

Click for Insights: Click anywhere on the map, on a "Random Point (AI Powered)" marker, or an "Interesting Location (AI Powered)" marker to get an AI-generated insight and local weather report in the "Map Insights" panel. 📍🧠

Map Insights Panel:

Use the "Get Insights for Map Center" button to get data for the current view's center. 🎯

Use "Set Start" and "Set End" to define a route. Once both are set, click "Analyze Route with AI" for a conceptual description of the journey. 🛣️

Draw Tools: Use the tools in the bottom-left corner to draw shapes or markers, and export them. ✍️

Search and Locate: Use the geocoder search bar or the locate control (top-left) for navigation. 🔍🧭

Limitations 🚧

Real-time Traffic: This map does not provide real-time traffic data like commercial mapping services (e.g., Google Maps). The AI-generated traffic insight is conceptual, based on general knowledge of the area, not live conditions. 🚦❌

POI Database: The AI insights are based on general knowledge and reverse geocoding. For a comprehensive database of businesses, restaurants, and other points of interest (POIs) with detailed information, a dedicated Places API would be required, which is beyond the scope of this project. 🏢🍽️