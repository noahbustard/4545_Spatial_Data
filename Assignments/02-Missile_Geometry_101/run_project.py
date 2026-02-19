#!/usr/bin/env python3
"""
Project 01: Missile Geometry 101
World Defense Organization (WDO) — Spatial Defense Analysis

Analyst: Noah Bustard
Course:  CS 4545/5993 — Spatial Data and Mapping, Spring 2026

This script implements all 5 milestones of the Missile Geometry 101 project.
"""

# ============================================================
# Standard library imports
# ============================================================
import sys
import json
import math
from pathlib import Path
from math import radians, degrees, sin, cos, asin, atan2, sqrt

# ============================================================
# Third-party geospatial imports
# ============================================================
import pandas as pd
import geopandas as gpd
import folium
from folium import plugins
from shapely.geometry import Point, LineString, shape, mapping
from shapely.ops import unary_union

# ============================================================
# Add src to path so we can import the WDO toolkit
# ============================================================
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))

from wdo.wdo_geo import (
    haversine_km,
    initial_bearing_deg,
    destination_point,
    trajectory_points,
    LatLon,
    EARTH_RADIUS_KM
)

print('All imports successful.')
print(f'Working directory: {ROOT}')
print(f'Earth radius used: {EARTH_RADIUS_KM} km')

# ============================================================
# CONFIGURATION
# ============================================================
BASE_LAT = 32.7767
BASE_LON = -96.7970
BASE_NAME = 'WDO Command Center — Dallas, TX'

DATA_DIR       = ROOT / 'data'
THREATS_PATH   = DATA_DIR / 'threats' / 'threats.json'
COUNTRIES_PATH = DATA_DIR / 'world_borders' / 'world_borders.geojson'
MAPS_DIR       = ROOT / 'maps'
MAPS_DIR.mkdir(exist_ok=True)

assert DATA_DIR.exists(), f'Missing data/ folder at {DATA_DIR}'
assert THREATS_PATH.exists(), f'Missing threats file at {THREATS_PATH}'
assert COUNTRIES_PATH.exists(), f'Missing world borders geojson at {COUNTRIES_PATH}'
print('All data paths verified.')

# Threat-type color scheme and damage radii
THREAT_STYLES = {
    'alien':    {'color': '#00FF00', 'marker': 'green',  'buffer_km': 150, 'severity': 'High'},
    'orbital':  {'color': '#9400D3', 'marker': 'purple', 'buffer_km': 300, 'severity': 'Critical'},
    'airborne': {'color': '#FF8C00', 'marker': 'orange', 'buffer_km': 100, 'severity': 'Moderate'},
    'kaiju':    {'color': '#FF0000', 'marker': 'red',    'buffer_km': 200, 'severity': 'Severe'},
}

BASE_PROXIMITY_KM = 500

print(f'Base: {BASE_NAME} ({BASE_LAT}, {BASE_LON})')
print(f'Base proximity threshold: {BASE_PROXIMITY_KM} km')

# ============================================================
# DATA LOADING
# ============================================================
with open(THREATS_PATH, 'r') as f:
    threats_raw = json.load(f)

print(f'\nLoaded {len(threats_raw)} threats')
threats_df = pd.DataFrame(threats_raw)
print(threats_df.to_string(index=False))

# Load world country boundaries
world = gpd.read_file(COUNTRIES_PATH)
print(f'\nWorld GeoDataFrame: {len(world)} countries')
print(f'CRS: {world.crs}')
print(f'Columns: {list(world.columns)}')

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def create_base_map(lat, lon, zoom=3):
    """Create a Folium map centered on the WDO base."""
    return folium.Map(
        location=[lat, lon],
        zoom_start=zoom,
        tiles='OpenStreetMap',
        control_scale=True
    )

def add_world_borders(m, world_gdf, name='World Borders'):
    """Add world country boundaries as a GeoJSON layer."""
    style_function = lambda x: {
        'fillColor': '#D4E6F1',
        'color': '#2C3E50',
        'weight': 0.5,
        'fillOpacity': 0.3
    }
    folium.GeoJson(
        world_gdf.__geo_interface__,
        name=name,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['COUNTRY'],
            aliases=['Country:'],
            style='font-size: 12px;'
        )
    ).add_to(m)

def add_base_marker(m, lat, lon, name='WDO Base'):
    """Add the WDO base location as a prominent marker."""
    folium.Marker(
        location=[lat, lon],
        tooltip=name,
        popup=folium.Popup(
            f'<b>{name}</b><br>Lat: {lat}<br>Lon: {lon}',
            max_width=250
        ),
        icon=folium.Icon(color='blue', icon='star', prefix='fa')
    ).add_to(m)

def add_threat_origins(m, threats, threat_styles):
    """Add threat origin markers, color-coded by type."""
    for t in threats:
        style = threat_styles.get(t['type'], {'color': 'gray'})
        folium.CircleMarker(
            location=[t['origin_lat'], t['origin_lon']],
            radius=8,
            color=style['color'],
            fill=True,
            fillColor=style['color'],
            fillOpacity=0.7,
            tooltip=(
                f"{t['id']} ({t['type']})<br>"
                f"Dist to base: {t['dist_to_base_km']:,.0f} km<br>"
                f"Bearing: {t['bearing_deg']}deg<br>"
                f"Speed: {t['speed_kmh']:,.0f} km/h"
            ),
            popup=folium.Popup(
                f"<b>{t['id']}</b> — {t['type'].upper()}<br>"
                f"Origin: ({t['origin_lat']:.4f}, {t['origin_lon']:.4f})<br>"
                f"Distance to base: {t['dist_to_base_km']:,.1f} km<br>"
                f"Heading: {t['bearing_deg']}deg<br>"
                f"Speed: {t['speed_kmh']:,.1f} km/h<br>"
                f"Duration: {t['duration_min']:.0f} min",
                max_width=300
            )
        ).add_to(m)

def add_trajectories(m, threats, threat_styles):
    """Add threat trajectories as colored polylines."""
    for t in threats:
        style = threat_styles.get(t['type'], {'color': 'gray'})
        folium.PolyLine(
            locations=t['trajectory_pts'],
            color=style['color'],
            weight=3,
            opacity=0.8,
            tooltip=(
                f"{t['id']} trajectory ({t['type']})<br>"
                f"Distance: {t['total_distance_km']:,.0f} km<br>"
                f"Bearing: {t['bearing_deg']}deg"
            ),
            dash_array='5 5' if t['type'] == 'kaiju' else None
        ).add_to(m)
        
        # Mark endpoint
        folium.CircleMarker(
            location=[t['dest_lat'], t['dest_lon']],
            radius=6,
            color='black',
            fill=True,
            fillColor=style['color'],
            fillOpacity=0.9,
            tooltip=(
                f"{t['id']} endpoint<br>"
                f"({t['dest_lat']:.4f}, {t['dest_lon']:.4f})"
            )
        ).add_to(m)

# ============================================================
# MILESTONE 1: PLOT THE WORLD
# ============================================================
print('\n' + '='*60)
print('MILESTONE 1: Plot the World')
print('='*60)

m1 = create_base_map(BASE_LAT, BASE_LON, zoom=3)
add_world_borders(m1, world)
add_base_marker(m1, BASE_LAT, BASE_LON, BASE_NAME)
folium.LayerControl().add_to(m1)

m1_path = MAPS_DIR / 'milestone_1_world_map.html'
m1.save(str(m1_path))
print(f'Milestone 1 map saved to: {m1_path}')

# ============================================================
# MILESTONE 2: DISTANCE & BEARING
# ============================================================
print('\n' + '='*60)
print('MILESTONE 2: Distance & Bearing')
print('='*60)

# Sanity check
print('\nSanity Check — Dallas to Houston:')
test_dist = haversine_km(32.7767, -96.7970, 29.7604, -95.3698)
test_bearing = initial_bearing_deg(32.7767, -96.7970, 29.7604, -95.3698)
print(f'  Distance: {test_dist:.2f} km (expected ~362)')
print(f'  Bearing:  {test_bearing:.2f} deg')

dest = destination_point(32.7767, -96.7970, 180, 100)
print(f'  100 km south of Dallas: ({dest.lat:.4f}, {dest.lon:.4f})')

# Compute distances and bearings for all threats
threats = []
for t in threats_raw:
    dist_to_base = haversine_km(
        t['origin_lat'], t['origin_lon'],
        BASE_LAT, BASE_LON
    )
    bearing_to_base = initial_bearing_deg(
        t['origin_lat'], t['origin_lon'],
        BASE_LAT, BASE_LON
    )
    threat = {
        'id': t['id'],
        'type': t['type'],
        'origin_lat': t['origin_lat'],
        'origin_lon': t['origin_lon'],
        'bearing_deg': t['bearing_deg'],
        'speed_kmh': t['speed_kmh'],
        'duration_min': t['duration_min'],
        'dist_to_base_km': round(dist_to_base, 2),
        'bearing_to_base_deg': round(bearing_to_base, 2),
    }
    threats.append(threat)

print('\n=== DISTANCE & BEARING ANALYSIS ===')
for t in threats:
    print(f"  {t['id']} ({t['type']:8s}): {t['dist_to_base_km']:>8,.1f} km to base, bearing {t['bearing_to_base_deg']:>6.1f} deg")

closest = min(threats, key=lambda t: t['dist_to_base_km'])
farthest = max(threats, key=lambda t: t['dist_to_base_km'])
print(f"\nClosest threat:  {closest['id']} ({closest['type']}) at {closest['dist_to_base_km']:,.1f} km")
print(f"Farthest threat: {farthest['id']} ({farthest['type']}) at {farthest['dist_to_base_km']:,.1f} km")

# Build M2 map
m2 = create_base_map(BASE_LAT, BASE_LON, zoom=3)
add_world_borders(m2, world)
add_base_marker(m2, BASE_LAT, BASE_LON, BASE_NAME)
add_threat_origins(m2, threats, THREAT_STYLES)

legend_html = '''
<div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000;
            background-color: white; padding: 10px; border: 2px solid grey;
            border-radius: 5px; font-size: 13px;">
    <b>Threat Types</b><br>
    <i style="background:#00FF00;width:12px;height:12px;display:inline-block;border-radius:50%;"></i> Alien<br>
    <i style="background:#9400D3;width:12px;height:12px;display:inline-block;border-radius:50%;"></i> Orbital<br>
    <i style="background:#FF8C00;width:12px;height:12px;display:inline-block;border-radius:50%;"></i> Airborne<br>
    <i style="background:#FF0000;width:12px;height:12px;display:inline-block;border-radius:50%;"></i> Kaiju<br>
    <i style="background:#3388ff;width:12px;height:12px;display:inline-block;"></i> WDO Base
</div>
'''
m2.get_root().html.add_child(folium.Element(legend_html))
folium.LayerControl().add_to(m2)

m2_path = MAPS_DIR / 'milestone_2_threats.html'
m2.save(str(m2_path))
print(f'Milestone 2 map saved to: {m2_path}')

# ============================================================
# MILESTONE 3: TRAJECTORIES
# ============================================================
print('\n' + '='*60)
print('MILESTONE 3: Trajectories (Point -> Line)')
print('='*60)

for t in threats:
    # Compute trajectory points
    t['trajectory_pts'] = trajectory_points(
        origin_lat=t['origin_lat'],
        origin_lon=t['origin_lon'],
        bearing_deg=t['bearing_deg'],
        speed_kmh=t['speed_kmh'],
        duration_min=t['duration_min'],
        step_min=2.0
    )
    
    # Total distance
    hours = t['duration_min'] / 60.0
    t['total_distance_km'] = round(t['speed_kmh'] * hours, 2)
    
    # Destination point
    dest = destination_point(
        t['origin_lat'], t['origin_lon'],
        t['bearing_deg'], t['total_distance_km']
    )
    t['dest_lat'] = dest.lat
    t['dest_lon'] = dest.lon
    
    # Shapely LineString (lon, lat order)
    line_coords = [(lon, lat) for lat, lon in t['trajectory_pts']]
    t['trajectory_line'] = LineString(line_coords)
    t['num_points'] = len(t['trajectory_pts'])

print('\n=== TRAJECTORY ANALYSIS ===')
for t in threats:
    print(f"  {t['id']} ({t['type']:8s}): {t['total_distance_km']:>8,.1f} km, "
          f"bearing {t['bearing_deg']:>6.1f} deg, "
          f"dest ({t['dest_lat']:.2f}, {t['dest_lon']:.2f}), "
          f"{t['num_points']} pts")

# Build M3 map
m3 = create_base_map(BASE_LAT, BASE_LON, zoom=3)
add_world_borders(m3, world)
add_base_marker(m3, BASE_LAT, BASE_LON, BASE_NAME)
add_threat_origins(m3, threats, THREAT_STYLES)
add_trajectories(m3, threats, THREAT_STYLES)

legend_html_traj = '''
<div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000;
            background-color: white; padding: 10px; border: 2px solid grey;
            border-radius: 5px; font-size: 13px;">
    <b>Threat Trajectories</b><br>
    <span style="color:#00FF00;">&#9644;</span> Alien<br>
    <span style="color:#9400D3;">&#9644;</span> Orbital<br>
    <span style="color:#FF8C00;">&#9644;</span> Airborne<br>
    <span style="color:#FF0000;">- - -</span> Kaiju<br>
    <i style="background:#3388ff;width:12px;height:12px;display:inline-block;"></i> WDO Base<br>
    &#9679; Origin &nbsp; &#9673; Endpoint
</div>
'''
m3.get_root().html.add_child(folium.Element(legend_html_traj))
folium.LayerControl().add_to(m3)

m3_path = MAPS_DIR / 'milestone_3_trajectories.html'
m3.save(str(m3_path))
print(f'Milestone 3 map saved to: {m3_path}')

# ============================================================
# MILESTONE 4: INTERSECTIONS & BORDERS
# ============================================================
print('\n' + '='*60)
print('MILESTONE 4: Intersections & Borders')
print('='*60)

traj_gdf = gpd.GeoDataFrame(
    [{'id': t['id'], 'type': t['type'], 'geometry': t['trajectory_line']} for t in threats],
    crs='EPSG:4326'
)

world_4326 = world.to_crs('EPSG:4326')

print('\n=== COUNTRY INTERSECTION ANALYSIS ===')
all_intersected_countries = set()

for t in threats:
    line = t['trajectory_line']
    intersected = world_4326[world_4326.geometry.intersects(line)]
    country_names = list(intersected['COUNTRY'].values)
    t['intersected_countries'] = country_names
    all_intersected_countries.update(country_names)
    print(f"  {t['id']} ({t['type']:8s}): {', '.join(country_names) if country_names else 'No land intersection'}")

print(f'\nTotal unique countries affected by trajectories: {len(all_intersected_countries)}')
print(f'Countries: {sorted(all_intersected_countries)}')

# Proximity analysis
print(f'\n=== BASE PROXIMITY ANALYSIS (threshold: {BASE_PROXIMITY_KM} km) ===')
for t in threats:
    min_dist = float('inf')
    for lat, lon in t['trajectory_pts']:
        d = haversine_km(lat, lon, BASE_LAT, BASE_LON)
        if d < min_dist:
            min_dist = d
    t['min_dist_to_base_km'] = round(min_dist, 2)
    t['passes_near_base'] = min_dist <= BASE_PROXIMITY_KM
    status = 'ALERT — WITHIN RANGE' if t['passes_near_base'] else 'Outside threshold'
    print(f"  {t['id']} ({t['type']:8s}): closest approach = {min_dist:>8,.1f} km — {status}")

near_threats = [t for t in threats if t['passes_near_base']]
print(f'\nThreats within {BASE_PROXIMITY_KM} km of base: {len(near_threats)}')

# Build M4 map
m4 = create_base_map(BASE_LAT, BASE_LON, zoom=3)

intersected_gdf = world_4326[world_4326['COUNTRY'].isin(all_intersected_countries)]
non_intersected_gdf = world_4326[~world_4326['COUNTRY'].isin(all_intersected_countries)]

folium.GeoJson(
    non_intersected_gdf.__geo_interface__,
    name='Unaffected Countries',
    style_function=lambda x: {
        'fillColor': '#D5D8DC',
        'color': '#2C3E50',
        'weight': 0.5,
        'fillOpacity': 0.3
    },
    tooltip=folium.GeoJsonTooltip(fields=['COUNTRY'], aliases=['Country:'])
).add_to(m4)

folium.GeoJson(
    intersected_gdf.__geo_interface__,
    name='Affected Countries',
    style_function=lambda x: {
        'fillColor': '#E74C3C',
        'color': '#C0392B',
        'weight': 1.5,
        'fillOpacity': 0.45
    },
    tooltip=folium.GeoJsonTooltip(fields=['COUNTRY'], aliases=['Affected Country:'])
).add_to(m4)

add_base_marker(m4, BASE_LAT, BASE_LON, BASE_NAME)
add_threat_origins(m4, threats, THREAT_STYLES)
add_trajectories(m4, threats, THREAT_STYLES)

folium.Circle(
    location=[BASE_LAT, BASE_LON],
    radius=BASE_PROXIMITY_KM * 1000,
    color='blue',
    fill=True,
    fillColor='blue',
    fillOpacity=0.05,
    weight=2,
    dash_array='10 5',
    tooltip=f'Base defense perimeter ({BASE_PROXIMITY_KM} km)'
).add_to(m4)

legend_html_m4 = '''
<div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000;
            background-color: white; padding: 10px; border: 2px solid grey;
            border-radius: 5px; font-size: 13px;">
    <b>Intersection Analysis</b><br>
    <i style="background:#E74C3C;width:12px;height:12px;display:inline-block;"></i> Affected Country<br>
    <i style="background:#D5D8DC;width:12px;height:12px;display:inline-block;"></i> Unaffected Country<br>
    <span style="color:blue;">- - -</span> Base Perimeter (500 km)<br>
    <span style="color:#00FF00;">&#9644;</span> Alien &nbsp;
    <span style="color:#9400D3;">&#9644;</span> Orbital<br>
    <span style="color:#FF8C00;">&#9644;</span> Airborne &nbsp;
    <span style="color:#FF0000;">- -</span> Kaiju
</div>
'''
m4.get_root().html.add_child(folium.Element(legend_html_m4))
folium.LayerControl().add_to(m4)

m4_path = MAPS_DIR / 'milestone_4_intersections.html'
m4.save(str(m4_path))
print(f'Milestone 4 map saved to: {m4_path}')

# ============================================================
# MILESTONE 5: DAMAGE ZONES
# ============================================================
print('\n' + '='*60)
print('MILESTONE 5: Damage Zones (The Bridge)')
print('='*60)

# Create GeoDataFrame of threat endpoints
endpoint_data = []
for t in threats:
    style = THREAT_STYLES[t['type']]
    endpoint_data.append({
        'id': t['id'],
        'type': t['type'],
        'buffer_km': style['buffer_km'],
        'severity': style['severity'],
        'color': style['color'],
        'geometry': Point(t['dest_lon'], t['dest_lat'])
    })

endpoints_gdf = gpd.GeoDataFrame(endpoint_data, crs='EPSG:4326')

# CRITICAL: Project to meter-based CRS before buffering
endpoints_projected = endpoints_gdf.to_crs('EPSG:3857')

# Create buffers in meters
buffer_geoms = endpoints_projected.apply(
    lambda row: row.geometry.buffer(row['buffer_km'] * 1000),
    axis=1
)

# Create new GeoDataFrame with proper CRS
buffers_projected = gpd.GeoDataFrame(
    endpoints_projected.drop(columns='geometry'),
    geometry=buffer_geoms.values,
    crs='EPSG:3857'
)

# Project back to EPSG:4326
buffers_4326 = buffers_projected.to_crs('EPSG:4326')

print('Damage zone buffers created successfully.')
print(f'CRS verification: {buffers_4326.crs}')
for _, row in buffers_4326.iterrows():
    print(f"  {row['id']} ({row['type']}): {row['buffer_km']} km buffer — {row['severity']} severity")

# Determine which countries fall within each damage zone
print('\n=== DAMAGE ZONE COUNTRY ANALYSIS ===')
damage_records = []

for idx, buf_row in buffers_4326.iterrows():
    buffer_geom = buf_row.geometry
    affected = world_4326[world_4326.geometry.intersects(buffer_geom)]
    
    t_id = buf_row['id']
    t_type = buf_row['type']
    severity = buf_row['severity']
    
    for t in threats:
        if t['id'] == t_id:
            t['damage_zone_countries'] = list(affected['COUNTRY'].values)
            break
    
    if len(affected) > 0:
        for _, country_row in affected.iterrows():
            damage_records.append({
                'country': country_row['COUNTRY'],
                'threat_id': t_id,
                'threat_type': t_type,
                'severity': severity,
                'buffer_km': buf_row['buffer_km']
            })
        print(f"  {t_id} ({t_type}, {severity}): {', '.join(affected['COUNTRY'].values)}")
    else:
        print(f"  {t_id} ({t_type}, {severity}): No land in damage zone (ocean impact)")
        damage_records.append({
            'country': 'Ocean (no land)',
            'threat_id': t_id,
            'threat_type': t_type,
            'severity': severity,
            'buffer_km': buf_row['buffer_km']
        })

damage_df = pd.DataFrame(damage_records)
print('\n=== DAMAGE ZONE SUMMARY TABLE ===')
print(damage_df.to_string(index=False))

# Country-level summary
severity_order = {'Critical': 4, 'Severe': 3, 'High': 2, 'Moderate': 1}
country_summary = []
for country in sorted(damage_df['country'].unique()):
    rows = damage_df[damage_df['country'] == country]
    worst = max(rows['severity'].values, key=lambda s: severity_order.get(s, 0))
    types = ', '.join(sorted(rows['threat_type'].unique()))
    threat_ids = ', '.join(sorted(rows['threat_id'].unique()))
    country_summary.append({
        'Country': country,
        'Threat IDs': threat_ids,
        'Threat Types': types,
        'Worst Severity': worst
    })

summary_df = pd.DataFrame(country_summary)
print('\n=== COUNTRY-LEVEL DAMAGE ASSESSMENT ===')
print(summary_df.to_string(index=False))
print(f'\nTotal countries in damage zones: {len(summary_df)}')

# Build M5 map (final comprehensive map)
m5 = create_base_map(BASE_LAT, BASE_LON, zoom=3)
add_world_borders(m5, world)

# Highlight affected countries
damage_countries = set(damage_df[damage_df['country'] != 'Ocean (no land)']['country'].values)
all_affected = all_intersected_countries.union(damage_countries)

affected_gdf = world_4326[world_4326['COUNTRY'].isin(all_affected)]
if len(affected_gdf) > 0:
    folium.GeoJson(
        affected_gdf.__geo_interface__,
        name='Affected Countries',
        style_function=lambda x: {
            'fillColor': '#E74C3C',
            'color': '#C0392B',
            'weight': 1.5,
            'fillOpacity': 0.35
        },
        tooltip=folium.GeoJsonTooltip(fields=['COUNTRY'], aliases=['Affected:'])
    ).add_to(m5)

# Add trajectories
add_trajectories(m5, threats, THREAT_STYLES)

# Add damage zone buffers (semi-transparent)
for idx, buf_row in buffers_4326.iterrows():
    buffer_geojson = mapping(buf_row.geometry)
    style = THREAT_STYLES[buf_row['type']]
    
    folium.GeoJson(
        buffer_geojson,
        name=f"{buf_row['id']} Damage Zone",
        style_function=lambda x, c=style['color']: {
            'fillColor': c,
            'color': c,
            'weight': 1.5,
            'fillOpacity': 0.2,
            'dashArray': '5 3'
        },
        tooltip=f"{buf_row['id']} damage zone ({buf_row['buffer_km']} km)"
    ).add_to(m5)

add_threat_origins(m5, threats, THREAT_STYLES)
add_base_marker(m5, BASE_LAT, BASE_LON, BASE_NAME)

folium.Circle(
    location=[BASE_LAT, BASE_LON],
    radius=BASE_PROXIMITY_KM * 1000,
    color='blue',
    fill=True,
    fillColor='blue',
    fillOpacity=0.05,
    weight=2,
    dash_array='10 5',
    tooltip=f'Base defense perimeter ({BASE_PROXIMITY_KM} km)'
).add_to(m5)

legend_html_m5 = '''
<div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000;
            background-color: white; padding: 12px; border: 2px solid grey;
            border-radius: 5px; font-size: 12px; max-width: 220px;">
    <b>WDO Threat Analysis</b><br><br>
    <b>Trajectories:</b><br>
    <span style="color:#00FF00;">&#9644;</span> Alien (150 km zone)<br>
    <span style="color:#9400D3;">&#9644;</span> Orbital (300 km zone)<br>
    <span style="color:#FF8C00;">&#9644;</span> Airborne (100 km zone)<br>
    <span style="color:#FF0000;">- -</span> Kaiju (200 km zone)<br><br>
    <b>Map Layers:</b><br>
    <i style="background:#E74C3C;width:12px;height:12px;display:inline-block;"></i> Affected Country<br>
    <i style="background:rgba(100,100,100,0.2);width:12px;height:12px;display:inline-block;border:1px dashed;"></i> Damage Zone<br>
    <span style="color:blue;">- - -</span> Base Perimeter<br>
    <i style="background:#3388ff;width:12px;height:12px;display:inline-block;"></i> WDO Base
</div>
'''
m5.get_root().html.add_child(folium.Element(legend_html_m5))
folium.LayerControl().add_to(m5)

m5_path = MAPS_DIR / 'milestone_5_damage_zones.html'
m5.save(str(m5_path))
print(f'\nMilestone 5 map saved to: {m5_path}')

# ============================================================
# FINAL SUMMARY
# ============================================================
print('\n' + '='*70)
print('       WORLD DEFENSE ORGANIZATION — THREAT ASSESSMENT REPORT')
print('='*70)
print(f'Base: {BASE_NAME}')
print(f'Base Coordinates: ({BASE_LAT}, {BASE_LON})')
print(f'Defense Perimeter: {BASE_PROXIMITY_KM} km')
print(f'Total Threats Analyzed: {len(threats)}')

type_counts = {}
for t in threats:
    type_counts[t["type"]] = type_counts.get(t["type"], 0) + 1
print('\nThreat Breakdown by Type:')
for ttype, count in sorted(type_counts.items()):
    print(f'  {ttype.capitalize():10s}: {count}')

print('\n' + '-'*70)
for t in threats:
    print(f"\n{t['id']} — {t['type'].upper()}")
    print(f"  Origin:          ({t['origin_lat']:.4f}, {t['origin_lon']:.4f})")
    print(f"  Destination:     ({t['dest_lat']:.4f}, {t['dest_lon']:.4f})")
    print(f"  Bearing:         {t['bearing_deg']} deg")
    print(f"  Speed:           {t['speed_kmh']:,.1f} km/h")
    print(f"  Duration:        {t['duration_min']:.0f} min")
    print(f"  Total Distance:  {t['total_distance_km']:,.1f} km")
    print(f"  Dist to Base:    {t['dist_to_base_km']:,.1f} km")
    print(f"  Closest to Base: {t['min_dist_to_base_km']:,.1f} km", end='')
    if t['passes_near_base']:
        print(' *** ALERT ***', end='')
    print()
    print(f"  Countries Crossed: {', '.join(t['intersected_countries']) if t['intersected_countries'] else 'None'}")
    dmg = t.get('damage_zone_countries', [])
    print(f"  Damage Zone:     {', '.join(dmg) if dmg else 'Ocean only'}")

print('\n' + '='*70)
print('                    END OF THREAT ASSESSMENT')
print('='*70)

# Save CSV data for Project 02
csv_path = ROOT / 'data' / 'damage_zone_summary.csv'
damage_df.to_csv(csv_path, index=False)
print(f'\nDamage zone summary saved to: {csv_path}')

summary_csv_path = ROOT / 'data' / 'country_damage_assessment.csv'
summary_df.to_csv(summary_csv_path, index=False)
print(f'Country assessment saved to: {summary_csv_path}')

print('\nAll maps saved to:', MAPS_DIR)
for f in sorted(MAPS_DIR.glob('*.html')):
    print(f'  - {f.name}')

print('\nProject 01 complete.')
