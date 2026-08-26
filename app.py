import streamlit as st
import streamlit.components.v1 as components
import json
import math
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Uber Angola", page_icon="🚗", layout="wide")

# ========== CSS STYLING ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background-color: #0a0a0a !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #0a0a0a !important;
        border-right: 1px solid #1a1a1a !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: white !important;
    }
    
    .uber-card {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        border: 1px solid #2a2a2a;
    }
    
    .uber-card-green {
        background: linear-gradient(135deg, #00b140, #008c33);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        color: white;
    }
    
    .stat-card {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #2a2a2a;
        margin: 4px;
    }
    
    .stat-value {
        font-size: 28px;
        font-weight: 700;
        color: #00b140 !important;
    }
    
    .stat-label {
        font-size: 12px;
        color: #888 !important;
        margin-top: 4px;
    }
    
    .driver-card {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        border: 1px solid #2a2a2a;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .driver-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00b140, #008c33);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        color: white;
    }
    
    .ride-status {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        border-left: 4px solid #00b140;
    }
    
    .rating-stars {
        display: flex;
        gap: 8px;
        justify-content: center;
        margin: 16px 0;
    }
    
    .star {
        font-size: 32px;
        cursor: pointer;
        color: #333;
        transition: color 0.2s;
    }
    
    .star.active {
        color: #ffd700;
    }
    
    .price-tag {
        font-size: 24px;
        font-weight: 700;
        color: #00b140 !important;
        text-align: center;
    }
    
    .online-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    
    .online {
        background: #00b140;
        box-shadow: 0 0 10px #00b140;
    }
    
    .offline {
        background: #ff4444;
    }
    
    .eta-badge {
        background: #00b140;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
    }
    
    .nav-btn {
        width: 100%;
        padding: 12px;
        border-radius: 8px;
        border: none;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        margin: 4px 0;
        transition: all 0.2s;
    }
    
    .nav-btn-primary {
        background: linear-gradient(135deg, #00b140, #008c33);
        color: white;
    }
    
    .nav-btn-secondary {
        background: #1a1a1a;
        color: white;
        border: 1px solid #2a2a2a;
    }
    
    .chart-bar {
        display: inline-block;
        background: linear-gradient(180deg, #00b140, #008c33);
        border-radius: 4px 4px 0 0;
        min-width: 30px;
        margin: 0 4px;
    }
    
    .payment-option {
        background: #1a1a1a;
        border-radius: 8px;
        padding: 12px;
        margin: 4px 0;
        cursor: pointer;
        border: 2px solid transparent;
        transition: all 0.2s;
    }
    
    .payment-option.selected {
        border-color: #00b140;
    }
    
    .location-input {
        background: #1a1a1a;
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #2a2a2a;
        color: white;
    }
    
    .ride-request-card {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        border: 1px solid #2a2a2a;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .history-item {
        background: #1a1a1a;
        border-radius: 8px;
        padding: 12px;
        margin: 4px 0;
        border: 1px solid #2a2a2a;
    }
    
    .history-route {
        color: #888 !important;
        font-size: 12px;
    }
    
    .history-price {
        color: #00b140 !important;
        font-weight: 600;
    }
    
    .status-procurando {
        background: #ff9800;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
    }
    
    .status-caminho {
        background: #2196f3;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
    }
    
    .status-viagem {
        background: #00b140;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
    }
    
    .status-chegou {
        background: #9c27b0;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
    }
    
    .bottom-panel {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #1a1a1a;
        padding: 16px;
        border-top: 1px solid #2a2a2a;
        z-index: 1000;
    }
    
    .map-container {
        height: calc(100vh - 200px);
        width: 100%;
        border-radius: 12px;
        overflow: hidden;
    }
    
    .stSelectbox > div > div {
        background-color: #1a1a1a !important;
        color: white !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #1a1a1a !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00b140, #008c33) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #008c33, #006622) !important;
    }
    
    .stRadio > div {
        background: #1a1a1a !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: #1a1a1a !important;
        border-radius: 8px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: white !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #00b140 !important;
        color: white !important;
    }
    
    div[data-testid="stExpander"] {
        background: #1a1a1a !important;
        border-radius: 8px !important;
        border: 1px solid #2a2a2a !important;
    }
    
    div[data-testid="stExpander"] summary {
        color: white !important;
    }
    
    .stSelectbox label, .stTextInput label, .stSlider label {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== CONSTANTS ==========
LUANDA_CENTER = {"lat": -8.8399, "lng": 13.2894}

PREDEFINED_LOCATIONS = {
    "Cidade Alta": {"lat": -8.8385, "lng": 13.2346},
    "Talatona": {"lat": -8.9167, "lng": 13.1833},
    "Viana": {"lat": -8.9000, "lng": 13.3667},
    "Ingombota": {"lat": -8.8333, "lng": 13.2500},
    "Maianga": {"lat": -8.8333, "lng": 13.2833},
    "Samba": {"lat": -8.8500, "lng": 13.2667},
    "Kinaxixi": {"lat": -8.8167, "lng": 13.2333},
    "Ilha de Luanda": {"lat": -8.7833, "lng": 13.2667},
    "Marginal": {"lat": -8.8167, "lng": 13.2667},
    "Aeroporto 4 de Fevereiro": {"lat": -8.8734, "lng": 13.2572},
    "Miramar": {"lat": -8.8000, "lng": 13.2000},
    "Rangel": {"lat": -8.8333, "lng": 13.2333},
    "Maculusso": {"lat": -8.8333, "lng": 13.2667},
    "Praia do Forte": {"lat": -8.8167, "lng": 13.2833},
    "Corimba": {"lat": -8.8667, "lng": 13.2333},
    "Catete": {"lat": -8.8500, "lng": 13.2500},
    "Estalagem": {"lat": -8.8333, "lng": 13.2167},
    "Prenda": {"lat": -8.8833, "lng": 13.2167},
    "Zango": {"lat": -8.9167, "lng": 13.3333},
    "Kilamba": {"lat": -8.9333, "lng": 13.3000}
}

PRICING = {
    "base_fare": 500,
    "per_km": 200,
    "per_minute": 50,
    "minimum": 300
}

DRIVER_NAMES = [
    "Carlos Silva", "João Santos", "Manuel Ferreira", "António Costa",
    "Pedro Neto", "Ricardo Almeida", "Fernando Lima", "Paulo Martins",
    "Miguel Torres", "André Rodrigues", "Rui Oliveira", "Diogo Pinto"
]

CAR_MODELS = [
    "Toyota Corolla", "Toyota Hilux", "Hyundai Accent", "Kia Picanto",
    "Toyota Prado", "Nissan Sentra", "Honda Civic", "Mazda 3",
    "Volkswagen Golf", "Renault Logan", "Chevrolet Onix", "Ford Fiesta"
]

def initialize_session_state():
    defaults = {
        "current_view": "passenger",
        "ride_requests": [],
        "active_ride": None,
        "ride_history": [],
        "driver_online": False,
        "driver_requests": [],
        "active_driver_ride": None,
        "driver_earnings": {"today": 0, "week": 0, "total": 0},
        "driver_rides_today": 0,
        "passenger_location": LUANDA_CENTER.copy(),
        "ride_status": None,
        "current_driver_info": None,
        "selected_payment": "Dinheiro",
        "ride_counter": 0,
        "drivers": generate_drivers(),
        "completed_rides": 0,
        "total_revenue": 0,
        "admin_rides": [],
        "from_location": "",
        "to_location": "",
        "map_click_mode": None,
        "pickup_coords": None,
        "dropoff_coords": None,
        "rating": 0,
        "show_rating": False,
        "ride_completed": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def generate_drivers():
    drivers = []
    for i in range(8):
        lat = LUANDA_CENTER["lat"] + random.uniform(-0.05, 0.05)
        lng = LUANDA_CENTER["lng"] + random.uniform(-0.05, 0.05)
        drivers.append({
            "id": i + 1,
            "name": DRIVER_NAMES[i % len(DRIVER_NAMES)],
            "car": CAR_MODELS[i % len(CAR_MODELS)],
            "plate": f"LD-{random.randint(1000, 9999)}-{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}",
            "rating": round(random.uniform(4.0, 5.0), 1),
            "lat": lat,
            "lng": lng,
            "online": random.choice([True, False]),
            "rides_completed": random.randint(50, 500)
        })
    return drivers

initialize_session_state()

# ========== HELPER FUNCTIONS ==========
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def calculate_price(distance_km, duration_minutes):
    price = PRICING["base_fare"] + (distance_km * PRICING["per_km"]) + (duration_minutes * PRICING["per_minute"])
    return max(price, PRICING["minimum"])

def get_location_coords(location_name):
    if location_name in PREDEFINED_LOCATIONS:
        return PREDEFINED_LOCATIONS[location_name]
    lat = LUANDA_CENTER["lat"] + random.uniform(-0.03, 0.03)
    lng = LUANDA_CENTER["lng"] + random.uniform(-0.03, 0.03)
    return {"lat": lat, "lng": lng}

def generate_eta():
    return random.randint(3, 12)

def generate_map_html(center_lat, center_lng, markers=None, route=None, show_pickup=False, show_dropoff=False, pickup=None, dropoff=None, passenger_marker=None):
    if markers is None:
        markers = []
    
    markers_json = json.dumps(markers)
    route_json = json.dumps(route) if route else "null"
    pickup_json = json.dumps(pickup) if pickup else "null"
    dropoff_json = json.dumps(dropoff) if dropoff else "null"
    passenger_json = json.dumps(passenger_marker) if passenger_marker else "null"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            body {{ margin: 0; padding: 0; background: #0a0a0a; }}
            #map {{ width: 100%; height: 600px; }}
            .custom-marker {{
                background: #00b140;
                border: 3px solid white;
                border-radius: 50%;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            }}
            .driver-marker {{
                background: #00b140;
                width: 24px;
                height: 24px;
                border-radius: 50%;
                border: 2px solid white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                color: white;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            }}
            .passenger-marker {{
                background: #2196f3;
                width: 28px;
                height: 28px;
                border-radius: 50%;
                border: 3px solid white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 14px;
                color: white;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                animation: pulse 2s infinite;
            }}
            .pickup-marker {{
                background: #00b140;
                width: 28px;
                height: 28px;
                border-radius: 50%;
                border: 3px solid white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 14px;
                color: white;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            }}
            .dropoff-marker {{
                background: #ff4444;
                width: 28px;
                height: 28px;
                border-radius: 50%;
                border: 3px solid white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 14px;
                color: white;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            }}
            @keyframes pulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.1); }}
                100% {{ transform: scale(1); }}
            }}
            .leaflet-control-zoom a {{
                background: #1a1a1a !important;
                color: white !important;
                border-color: #2a2a2a !important;
            }}
            .leaflet-control-zoom a:hover {{
                background: #2a2a2a !important;
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script>
            var map = L.map('map', {{
                zoomControl: true,
                attributionControl: false
            }}).set([{center_lat}, {center_lng}], 13);
            
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 19,
                attribution: '© OpenStreetMap'
            }}).addTo(map);
            
            var markers = {markers_json};
            var route = {route_json};
            var pickup = {pickup_json};
            var dropoff = {dropoff_json};
            var passenger = {passenger_json};
            
            markers.forEach(function(m) {{
                var icon = L.divIcon({{
                    className: 'driver-marker',
                    html: '🚕',
                    iconSize: [24, 24],
                    iconAnchor: [12, 12]
                }});
                L.marker([m.lat, m.lng], {{icon: icon}}).addTo(map)
                    .bindPopup('<b>' + m.name + '</b><br>' + m.car + '<br>⭐ ' + m.rating);
            }});
            
            if (passenger) {{
                var icon = L.divIcon({{
                    className: 'passenger-marker',
                    html: '📍',
                    iconSize: [28, 28],
                    iconAnchor: [14, 14]
                }});
                L.marker([passenger.lat, passenger.lng], {{icon: icon}}).addTo(map)
                    .bindPopup('<b>A sua localização</b>');
            }}
            
            if (pickup) {{
                var icon = L.divIcon({{
                    className: 'pickup-marker',
                    html: '🟢',
                    iconSize: [28, 28],
                    iconAnchor: [14, 14]
                }});
                L.marker([pickup.lat, pickup.lng], {{icon: icon}}).addTo(map)
                    .bindPopup('<b>Local de recolha</b>');
            }}
            
            if (dropoff) {{
                var icon = L.divIcon({{
                    className: 'dropoff-marker',
                    html: '🔴',
                    iconSize: [28, 28],
                    iconAnchor: [14, 14]
                }});
                L.marker([dropoff.lat, dropoff.lng], {{icon: icon}}).addTo(map)
                    .bindPopup('<b>Destino</b>');
            }}
            
            if (route && route.length > 0) {{
                L.polyline(route, {{
                    color: '#00b140',
                    weight: 4,
                    opacity: 0.8,
                    dashArray: '10, 10'
                }}).addTo(map);
            }}
            
            map.on('click', function(e) {{
                var data = {{
                    lat: e.latlng.lat,
                    lng: e.latlng.lng
                }};
                window.parent.postMessage({{type: 'map_click', data: data}}, '*');
            }});
            
            var bounds = [];
            if (passenger) bounds.push([passenger.lat, passenger.lng]);
            if (pickup) bounds.push([pickup.lat, pickup.lng]);
            if (dropoff) bounds.push([dropoff.lat, dropoff.lng]);
            markers.forEach(function(m) {{ bounds.push([m.lat, m.lng]); }});
            
            if (bounds.length > 1) {{
                map.fitBounds(bounds, {{padding: [50, 50]}});
            }}
        </script>
    </body>
    </html>
    """
    return html

def create_admin_chart_html(data, labels):
    if not data:
        return "<p style='color: #888; text-align: center;'>Sem dados</p>"
    
    max_val = max(data) if data else 1
    bars_html = ""
    for i, (val, label) in enumerate(zip(data, labels)):
        height = (val / max_val * 150) if max_val > 0 else 0
        bars_html += f"""
        <div style="display: inline-block; margin: 0 4px; text-align: center;">
            <div class="chart-bar" style="height: {max(height, 5)}px;"></div>
            <div style="color: #888; font-size: 10px; margin-top: 4px;">{label}</div>
            <div style="color: #00b140; font-size: 10px;">{val}Kz</div>
        </div>
        """
    
    return f"""
    <div style="display: flex; align-items: flex-end; justify-content: center; padding: 16px; background: #1a1a1a; border-radius: 8px; min-height: 200px;">
        {bars_html}
    </div>
    """

def create_earnings_chart_html(earnings_data, labels):
    if not earnings_data:
        return "<p style='color: #888; text-align: center;'>Sem dados</p>"
    
    max_val = max(earnings_data) if earnings_data else 1
    bars_html = ""
    for val, label in zip(earnings_data, labels):
        height = (val / max_val * 120) if max_val > 0 else 0
        bars_html += f"""
        <div style="display: inline-block; margin: 0 6px; text-align: center;">
            <div style="background: linear-gradient(180deg, #00b140, #008c33); height: {max(height, 8)}px; width: 30px; border-radius: 4px 4px 0 0;"></div>
            <div style="color: #888; font-size: 11px; margin-top: 4px;">{label}</div>
        </div>
        """
    
    return f"""
    <div style="display: flex; align-items: flex-end; justify-content: center; padding: 16px; background: #1a1a1a; border-radius: 8px; min-height: 180px;">
        {bars_html}
    </div>
    """

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #00b140; font-size: 28px; margin-bottom: 4px;">🚗 Uber Angola</h1>
        <p style="color: #888; font-size: 12px;">Luanda, Angola</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    view = st.radio(
        "Navegação",
        ["🚗 Passageiro", "🚕 Motorista", "📊 Admin"],
        index=0 if st.session_state.current_view == "passenger" else (1 if st.session_state.current_view == "driver" else 2)
    )
    
    if view == "🚗 Passageiro":
        st.session_state.current_view = "passenger"
    elif view == "🚕 Motorista":
        st.session_state.current_view = "driver"
    else:
        st.session_state.current_view = "admin"
    
    st.markdown("---")
    
    if st.session_state.current_view == "driver":
        online = st.session_state.driver_online
        st.markdown(f"""
        <div style="text-align: center; padding: 12px;">
            <span class="online-indicator {'online' if online else 'offline'}"></span>
            <span style="color: {'#00b140' if online else '#ff4444'}; font-weight: 600;">
                {'Online' if online else 'Offline'}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; color: #555; font-size: 11px;">
        <p>Uber Angola © 2024</p>
        <p>Versão 1.0.0</p>
    </div>
    """, unsafe_allow_html=True)

# ========== PASSENGER VIEW ==========
def render_passenger_view():
    st.markdown("""
    <div style="padding: 12px 16px; background: #1a1a1a; border-bottom: 1px solid #2a2a2a;">
        <h2 style="margin: 0; font-size: 20px;">🚗 Pedir Corrida</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col_map, col_form = st.columns([2, 1])
    
    with col_map:
        online_drivers = [d for d in st.session_state.drivers if d.get("online", False)]
        
        driver_markers = []
        for d in online_drivers:
            driver_markers.append({
                "lat": d["lat"],
                "lng": d["lng"],
                "name": d["name"],
                "car": d["car"],
                "rating": d["rating"]
            })
        
        passenger_marker = st.session_state.passenger_location
        
        pickup_coords = st.session_state.pickup_coords
        dropoff_coords = st.session_state.dropoff_coords
        
        route = None
        if pickup_coords and dropoff_coords:
            mid_lat = (pickup_coords["lat"] + dropoff_coords["lat"]) / 2
            mid_lng = (pickup_coords["lng"] + dropoff_coords["lng"]) / 2
            route = [
                [pickup_coords["lat"], pickup_coords["lng"]],
                [mid_lat + 0.005, mid_lng + 0.005],
                [dropoff_coords["lat"], dropoff_coords["lng"]]
            ]
        
        map_html = generate_map_html(
            st.session_state.passenger_location["lat"],
            st.session_state.passenger_location["lng"],
            markers=driver_markers,
            route=route,
            pickup=pickup_coords,
            dropoff=dropoff_coords,
            passenger_marker=passenger_marker
        )
        
        st.components.v1.html(map_html, height=600, scrolling=False)
    
    with col_form:
        if st.session_state.ride_status is None:
            st.markdown("""
            <div class="uber-card">
                <h3 style="margin: 0 0 12px 0;">📍 Destino</h3>
            </div>
            """, unsafe_allow_html=True)
            
            locations_list = list(PREDEFINED_LOCATIONS.keys())
            
            from_loc = st.selectbox(
                "De (Partida)",
                ["当前位置 (Luanda Centro)"] + locations_list,
                index=0
            )
            
            to_loc = st.selectbox(
                "Para (Destino)",
                locations_list,
                index=0
            )
            
            if from_loc != "当前位置 (Luanda Centro)":
                st.session_state.pickup_coords = get_location_coords(from_loc)
            else:
                st.session_state.pickup_coords = st.session_state.passenger_location.copy()
            
            st.session_state.dropoff_coords = get_location_coords(to_loc)
            
            if st.session_state.pickup_coords and st.session_state.dropoff_coords:
                distance = haversine(
                    st.session_state.pickup_coords["lat"],
                    st.session_state.pickup_coords["lng"],
                    st.session_state.dropoff_coords["lat"],
                    st.session_state.dropoff_coords["lng"]
                )
                duration = int(distance * 2.5)
                price = calculate_price(distance, duration)
                
                st.markdown(f"""
                <div class="uber-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <p style="color: #888; margin: 0;">Distância estimada</p>
                            <p style="font-size: 18px; font-weight: 600; margin: 0;">{distance:.1f} km</p>
                        </div>
                        <div>
                            <p style="color: #888; margin: 0;">Tempo estimado</p>
                            <p style="font-size: 18px; font-weight: 600; margin: 0;">{duration} min</p>
                        </div>
                    </div>
                    <hr style="border-color: #2a2a2a; margin: 12px 0;">
                    <div style="text-align: center;">
                        <p style="color: #888; margin: 0;">Preço estimado</p>
                        <p class="price-tag" style="margin: 4px 0;">{price:.0f} Kz</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="uber-card">
                <h4 style="margin: 0 0 8px 0;">💳 Pagamento</h4>
            </div>
            """, unsafe_allow_html=True)
            
            payment = st.radio(
                "Método de pagamento",
                ["Dinheiro", "Multicaixa Express", "Unitel Money"],
                horizontal=True
            )
            st.session_state.selected_payment = payment
            
            if st.button("Pedir Corrida", use_container_width=True, type="primary"):
                online_drivers_list = [d for d in st.session_state.drivers if d.get("online", False)]
                if online_drivers_list:
                    selected_driver = random.choice(online_drivers_list)
                    eta = generate_eta()
                    
                    st.session_state.current_driver_info = {
                        "name": selected_driver["name"],
                        "car": selected_driver["car"],
                        "plate": selected_driver["plate"],
                        "rating": selected_driver["rating"],
                        "eta": eta
                    }
                    st.session_state.ride_status = "procurando"
                    st.session_state.pickup_coords = st.session_state.pickup_coords
                    st.session_state.dropoff_coords = st.session_state.dropoff_coords
                    st.session_state.ride_counter += 1
                    st.rerun()
                else:
                    st.error("Nenhum motorista disponível no momento.")
        
        elif st.session_state.ride_status == "procurando":
            driver = st.session_state.current_driver_info
            st.markdown(f"""
            <div class="ride-status">
                <span class="status-procurando">Procurando motorista</span>
                <div style="margin-top: 12px;">
                    <p style="color: #888;">A procurar o motorista mais próximo...</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Cancelar", use_container_width=True):
                st.session_state.ride_status = None
                st.session_state.current_driver_info = None
                st.session_state.pickup_coords = None
                st.session_state.dropoff_coords = None
                st.rerun()
            
            import time
            time.sleep(2)
            st.session_state.ride_status = "a_caminho"
            st.rerun()
        
        elif st.session_state.ride_status == "a_caminho":
            driver = st.session_state.current_driver_info
            st.markdown(f"""
            <div class="ride-status">
                <span class="status-caminho">Motorista a caminho</span>
            </div>
            
            <div class="driver-card">
                <div class="driver-avatar">👤</div>
                <div style="flex: 1;">
                    <h4 style="margin: 0;">{driver['name']}</h4>
                    <p style="color: #888; margin: 2px 0;">{driver['car']} • {driver['plate']}</p>
                    <p style="margin: 2px 0;">⭐ {driver['rating']}</p>
                </div>
                <div>
                    <span class="eta-badge">{driver['eta']} min</span>
                </div>
            </div>
            
            <div class="uber-card">
                <p style="color: #888; margin: 0;">Chegada estimada</p>
                <p style="font-size: 20px; font-weight: 600; margin: 4px 0;">{driver['eta']} minutos</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Ligar ao Motorista", use_container_width=True):
                    st.info("A ligar... +244 923 456 789")
            with col2:
                if st.button("Cancelar", use_container_width=True):
                    st.session_state.ride_status = None
                    st.session_state.current_driver_info = None
                    st.session_state.pickup_coords = None
                    st.session_state.dropoff_coords = None
                    st.rerun()
            
            import time
            time.sleep(3)
            st.session_state.ride_status = "em_viagem"
            st.rerun()
        
        elif st.session_state.ride_status == "em_viagem":
            driver = st.session_state.current_driver_info
            
            distance = haversine(
                st.session_state.pickup_coords["lat"],
                st.session_state.pickup_coords["lng"],
                st.session_state.dropoff_coords["lat"],
                st.session_state.dropoff_coords["lng"]
            )
            duration = int(distance * 2.5)
            price = calculate_price(distance, duration)
            
            progress = random.uniform(0.1, 0.9)
            current_lat = st.session_state.pickup_coords["lat"] + (st.session_state.dropoff_coords["lat"] - st.session_state.pickup_coords["lat"]) * progress
            current_lng = st.session_state.pickup_coords["lng"] + (st.session_state.dropoff_coords["lng"] - st.session_state.pickup_coords["lng"]) * progress
            
            st.markdown(f"""
            <div class="ride-status">
                <span class="status-viagem">Em viagem</span>
            </div>
            
            <div class="driver-card">
                <div class="driver-avatar">👤</div>
                <div style="flex: 1;">
                    <h4 style="margin: 0;">{driver['name']}</h4>
                    <p style="color: #888; margin: 2px 0;">{driver['car']} • {driver['plate']}</p>
                </div>
            </div>
            
            <div class="uber-card">
                <div style="text-align: center;">
                    <p style="color: #888; margin: 0;">Progresso da viagem</p>
                    <div style="background: #2a2a2a; border-radius: 4px; height: 8px; margin: 8px 0;">
                        <div style="background: #00b140; height: 100%; width: {progress*100:.0f}%; border-radius: 4px;"></div>
                    </div>
                    <p style="color: #00b140; font-weight: 600; margin: 0;">{progress*100:.0f}% concluído</p>
                </div>
            </div>
            
            <div class="uber-card">
                <p style="color: #888; margin: 0;">Preço atual</p>
                <p class="price-tag" style="margin: 4px 0;">{price:.0f} Kz</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Finalizar Viagem", use_container_width=True, type="primary"):
                st.session_state.ride_status = "chegou"
                st.session_state.show_rating = True
                st.session_state.ride_completed = True
                st.rerun()
        
        elif st.session_state.ride_status == "chegou":
            driver = st.session_state.current_driver_info
            
            distance = haversine(
                st.session_state.pickup_coords["lat"],
                st.session_state.pickup_coords["lng"],
                st.session_state.dropoff_coords["lat"],
                st.session_state.dropoff_coords["lng"]
            )
            duration = int(distance * 2.5)
            price = calculate_price(distance, duration)
            
            st.markdown(f"""
            <div class="ride-status">
                <span class="status-chegou">Chegou ao destino!</span>
            </div>
            
            <div class="uber-card">
                <div style="text-align: center;">
                    <h3 style="color: #00b140; margin: 0;">🎉 Viagem Concluída</h3>
                    <p style="color: #888; margin: 8px 0;">Obrigado por viajar connosco!</p>
                </div>
            </div>
            
            <div class="driver-card">
                <div class="driver-avatar">👤</div>
                <div style="flex: 1;">
                    <h4 style="margin: 0;">{driver['name']}</h4>
                    <p style="color: #888; margin: 2px 0;">{driver['car']} • {driver['plate']}</p>
                    <p style="margin: 2px 0;">⭐ {driver['rating']}</p>
                </div>
            </div>
            
            <div class="uber-card">
                <div style="display: flex; justify-content: space-around;">
                    <div style="text-align: center;">
                        <p style="color: #888; margin: 0;">Distância</p>
                        <p style="font-weight: 600; margin: 4px 0;">{distance:.1f} km</p>
                    </div>
                    <div style="text-align: center;">
                        <p style="color: #888; margin: 0;">Duração</p>
                        <p style="font-weight: 600; margin: 4px 0;">{duration} min</p>
                    </div>
                    <div style="text-align: center;">
                        <p style="color: #888; margin: 0;">Pagamento</p>
                        <p style="font-weight: 600; margin: 4px 0;">{st.session_state.selected_payment}</p>
                    </div>
                </div>
                <hr style="border-color: #2a2a2a; margin: 12px 0;">
                <div style="text-align: center;">
                    <p style="color: #888; margin: 0;">Total</p>
                    <p class="price-tag" style="margin: 4px 0;">{price:.0f} Kz</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.show_rating:
                st.markdown("""
                <div class="uber-card">
                    <h4 style="text-align: center; margin: 0 0 12px 0;">Avaliar motorista</h4>
                </div>
                """, unsafe_allow_html=True)
                
                rating = st.slider("Classificação", 1, 5, 5)
                
                if st.button("Enviar Avaliação", use_container_width=True, type="primary"):
                    ride_record = {
                        "id": st.session_state.ride_counter,
                        "driver": driver["name"],
                        "car": driver["car"],
                        "from": "Localização atual",
                        "to": "Destino",
                        "distance": distance,
                        "duration": duration,
                        "price": price,
                        "payment": st.session_state.selected_payment,
                        "rating": rating,
                        "time": datetime.now().strftime("%H:%M"),
                        "date": datetime.now().strftime("%d/%m/%Y")
                    }
                    st.session_state.ride_history.append(ride_record)
                    st.session_state.admin_rides.append(ride_record)
                    st.session_state.completed_rides += 1
                    st.session_state.total_revenue += price
                    
                    st.session_state.ride_status = None
                    st.session_state.current_driver_info = None
                    st.session_state.show_rating = False
                    st.session_state.pickup_coords = None
                    st.session_state.dropoff_coords = None
                    st.session_state.rating = 0
                    st.success("Avaliação enviada! Obrigado!")
                    st.rerun()
    
    if st.session_state.ride_status in ["a_caminho", "em_viagem"]:
        driver = st.session_state.current_driver_info
        distance = haversine(
            st.session_state.pickup_coords["lat"],
            st.session_state.pickup_coords["lng"],
            st.session_state.dropoff_coords["lat"],
            st.session_state.dropoff_coords["lng"]
        )
        duration = int(distance * 2.5)
        price = calculate_price(distance, duration)
        
        st.markdown(f"""
        <div style="position: fixed; bottom: 0; left: 0; right: 0; background: #1a1a1a; padding: 16px; border-top: 1px solid #2a2a2a; z-index: 1000;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <p style="color: #888; margin: 0; font-size: 12px;">Preço estimado</p>
                    <p style="color: #00b140; font-size: 20px; font-weight: 700; margin: 0;">{price:.0f} Kz</p>
                </div>
                <div style="text-align: right;">
                    <p style="color: #888; margin: 0; font-size: 12px;">ETA</p>
                    <p style="font-size: 20px; font-weight: 700; margin: 0;">{driver['eta']} min</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ========== DRIVER VIEW ==========
def render_driver_view():
    st.markdown("""
    <div style="padding: 12px 16px; background: #1a1a1a; border-bottom: 1px solid #2a2a2a;">
        <h2 style="margin: 0; font-size: 20px;">出租车 Motorista</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col_main, col_sidebar = st.columns([2, 1])
    
    with col_main:
        if st.session_state.active_driver_ride:
            ride = st.session_state.active_driver_ride
            
            status_map = {
                "accepted": "accepted",
                "in_progress": "in_progress",
                "completed": "completed"
            }
            
            status_text = {
                "accepted": "accepted",
                "in_progress": "em viagem",
                "completed": "concluída"
            }
            
            st.markdown(f"""
            <div class="ride-status">
                <span class="status-{'caminho' if ride['status'] == 'accepted' else 'viagem' if ride['status'] == 'in_progress' else 'chegou'}">
                    {status_text.get(ride['status'], ride['status'])}
                </span>
            </div>
            
            <div class="driver-card">
                <div class="driver-avatar">👤</div>
                <div style="flex: 1;">
                    <h4 style="margin: 0;">{ride['passenger_name']}</h4>
                    <p style="color: #888; margin: 2px 0;">⭐ {ride['passenger_rating']}</p>
                    <p style="margin: 2px 0;">📞 {ride['passenger_phone']}</p>
                </div>
            </div>
            
            <div class="uber-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="color: #00b140;">●</span>
                    <span>{ride['from']}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: #ff4444;">●</span>
                    <span>{ride['to']}</span>
                </div>
                <hr style="border-color: #2a2a2a; margin: 12px 0;">
                <div style="display: flex; justify-content: space-around;">
                    <div style="text-align: center;">
                        <p style="color: #888; margin: 0;">Distância</p>
                        <p style="font-weight: 600; margin: 4px 0;">{ride['distance']:.1f} km</p>
                    </div>
                    <div style="text-align: center;">
                        <p style="color: #888; margin: 0;">Preço</p>
                        <p style="color: #00b140; font-weight: 600; margin: 4px 0;">{ride['price']:.0f} Kz</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if ride['status'] == "accepted":
                    if st.button("Iniciar Viagem", use_container_width=True, type="primary"):
                        st.session_state.active_driver_ride['status'] = "in_progress"
                        st.rerun()
                elif ride['status'] == "in_progress":
                    if st.button("Finalizar Viagem", use_container_width=True, type="primary"):
                        st.session_state.active_driver_ride['status'] = "completed"
                        st.session_state.driver_earnings["today"] += ride['price']
                        st.session_state.driver_earnings["week"] += ride['price']
                        st.session_state.driver_earnings["total"] += ride['price']
                        st.session_state.driver_rides_today += 1
                        
                        ride_record = {
                            "id": len(st.session_state.ride_history) + 1,
                            "driver": "Você",
                            "passenger": ride['passenger_name'],
                            "from": ride['from'],
                            "to": ride['to'],
                            "distance": ride['distance'],
                            "price": ride['price'],
                            "payment": ride['payment'],
                            "time": datetime.now().strftime("%H:%M"),
                            "date": datetime.now().strftime("%d/%m/%Y")
                        }
                        st.session_state.ride_history.append(ride_record)
                        st.session_state.admin_rides.append(ride_record)
                        st.session_state.total_revenue += ride['price']
                        
                        st.session_state.active_driver_ride = None
                        st.success("Viagem concluída! Ganhou {:.0f} Kz".format(ride['price']))
                        st.rerun()
            
            with col2:
                if ride['status'] != "completed":
                    if st.button("Cancelar", use_container_width=True):
                        st.session_state.active_driver_ride = None
                        st.rerun()
        else:
            if st.session_state.driver_online:
                st.markdown("""
                <div class="uber-card">
                    <h3 style="margin: 0 0 12px 0;">📡 Aguardando pedidos...</h3>
                    <p style="color: #888; margin: 0;">Você receberá notificações de novos pedidos</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.driver_requests:
                    for i, req in enumerate(st.session_state.driver_requests[:3]):
                        st.markdown(f"""
                        <div class="ride-request-card">
                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                <div>
                                    <h4 style="margin: 0;">{req['passenger_name']}</h4>
                                    <p style="color: #888; margin: 4px 0;">⭐ {req['passenger_rating']}</p>
                                </div>
                                <span class="eta-badge">{req['eta']} min</span>
                            </div>
                            <div style="margin: 12px 0;">
                                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                                    <span style="color: #00b140;">●</span>
                                    <span>{req['from']}</span>
                                </div>
                                <div style="display: flex; align-items: center; gap: 8px;">
                                    <span style="color: #ff4444;">●</span>
                                    <span>{req['to']}</span>
                                </div>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <p style="color: #00b140; font-weight: 600; margin: 0;">{req['price']:.0f} Kz</p>
                                <div style="display: flex; gap: 8px;">
                                    <button onclick="window.parent.postMessage({{type: 'reject_ride', index: {i}}}, '*')" 
                                            style="background: #ff4444; color: white; border: none; padding: 8px 16px; border-radius: 8px; cursor: pointer;">
                                        Rejeitar
                                    </button>
                                    <button onclick="window.parent.postMessage({{type: 'accept_ride', index: {i}}}, '*')" 
                                            style="background: #00b140; color: white; border: none; padding: 8px 16px; border-radius: 8px; cursor: pointer;">
                                        Aceitar
                                    </button>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"Aceitar #{i+1}", key=f"accept_{i}", use_container_width=True, type="primary"):
                                st.session_state.active_driver_ride = req
                                st.session_state.active_driver_ride['status'] = "accepted"
                                st.session_state.driver_requests.pop(i)
                                st.rerun()
                        with col2:
                            if st.button(f"Rejeitar #{i+1}", key=f"reject_{i}", use_container_width=True):
                                st.session_state.driver_requests.pop(i)
                                st.rerun()
                else:
                    if random.random() < 0.3:
                        passenger_name = random.choice(["Maria Silva", "Ana Costa", "Pedro Almeida", "Sofia Santos", "Lucas Ferreira"])
                        passenger_rating = round(random.uniform(4.0, 5.0), 1)
                        locations = list(PREDEFINED_LOCATIONS.keys())
                        from_loc = random.choice(locations)
                        to_loc = random.choice([l for l in locations if l != from_loc])
                        
                        from_coords = get_location_coords(from_loc)
                        to_coords = get_location_coords(to_loc)
                        distance = haversine(from_coords["lat"], from_coords["lng"], to_coords["lat"], to_coords["lng"])
                        price = calculate_price(distance, int(distance * 2.5))
                        
                        new_request = {
                            "id": len(st.session_state.driver_requests) + 1,
                            "passenger_name": passenger_name,
                            "passenger_rating": passenger_rating,
                            "passenger_phone": f"+244 9{random.randint(10000000, 99999999)}",
                            "from": from_loc,
                            "to": to_loc,
                            "distance": distance,
                            "price": price,
                            "payment": random.choice(["Dinheiro", "Multicaixa Express", "Unitel Money"]),
                            "eta": generate_eta(),
                            "from_coords": from_coords,
                            "to_coords": to_coords
                        }
                        st.session_state.driver_requests.append(new_request)
                        st.rerun()
            else:
                st.markdown("""
                <div class="uber-card" style="text-align: center; padding: 40px;">
                    <h3 style="margin: 0 0 12px 0;">Offline</h3>
                    <p style="color: #888; margin: 0;">Ative o modo online para receber pedidos</p>
                </div>
                """, unsafe_allow_html=True)
    
    with col_sidebar:
        st.markdown("""
        <div class="uber-card">
            <h4 style="margin: 0 0 12px 0;">Status</h4>
        </div>
        """, unsafe_allow_html=True)
        
        online = st.toggle("Modo Online", value=st.session_state.driver_online)
        st.session_state.driver_online = online
        
        if online:
            st.markdown(f"""
            <div class="uber-card-green" style="text-align: center;">
                <p style="margin: 0; font-size: 14px;">🟢 Online e pronto</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="uber-card">
            <h4 style="margin: 0 0 12px 0;">Ganhos de Hoje</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{st.session_state.driver_earnings['today']:.0f} Kz</div>
            <div class="stat-label">Ganhos hoje</div>
        </div>
        
        <div class="stat-card">
            <div class="stat-value">{st.session_state.driver_rides_today}</div>
            <div class="stat-label">Corridas hoje</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="uber-card">
            <h4 style="margin: 0 0 12px 0;">Ganhos da Semana</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{st.session_state.driver_earnings['week']:.0f} Kz</div>
            <div class="stat-label">Ganhos esta semana</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="uber-card">
            <h4 style="margin: 0 0 12px 0;">Ganhos Totais</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{st.session_state.driver_earnings['total']:.0f} Kz</div>
            <div class="stat-label">Ganhos totais</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="uber-card">
            <h4 style="margin: 0 0 12px 0;">📊 Ganhos Diários</h4>
        </div>
        """, unsafe_allow_html=True)
        
        days = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
        daily_earnings = [random.randint(2000, 8000) for _ in range(7)]
        chart_html = create_earnings_chart_html(daily_earnings, days)
        components.html(chart_html, height=200, scrolling=False)
        
        if st.session_state.ride_history:
            st.markdown("""
            <div class="uber-card">
                <h4 style="margin: 0 0 12px 0;">📋 Histórico</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for ride in reversed(st.session_state.ride_history[-5:]):
                st.markdown(f"""
                <div class="history-item">
                    <div style="display: flex; justify-content: space-between;">
                        <span class="history-route">{ride.get('from', 'N/A')} → {ride.get('to', 'N/A')}</span>
                        <span class="history-price">{ride.get('price', 0):.0f} Kz</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 4px;">
                        <span style="color: #888; font-size: 12px;">{ride.get('time', 'N/A')}</span>
                        <span style="color: #888; font-size: 12px;">{ride.get('date', 'N/A')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ========== ADMIN VIEW ==========
def render_admin_view():
    st.markdown("""
    <div style="padding: 12px 16px; background: #1a1a1a; border-bottom: 1px solid #2a2a2a;">
        <h2 style="margin: 0; font-size: 20px;">📊 Painel Admin</h2>
    </div>
    """, unsafe_allow_html=True)
    
    total_rides = len(st.session_state.admin_rides)
    active_drivers = len([d for d in st.session_state.drivers if d.get("online", False)])
    total_revenue = st.session_state.total_revenue
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{total_rides}</div>
            <div class="stat-label">Total Corridas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{active_drivers}</div>
            <div class="stat-label">Motoristas Ativos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{total_revenue:.0f}</div>
            <div class="stat-label">Receita Total (Kz)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_price = total_revenue / total_rides if total_rides > 0 else 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{avg_price:.0f}</div>
            <div class="stat-label">Preço Médio (Kz)</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_chart, col_drivers = st.columns([2, 1])
    
    with col_chart:
        st.markdown("""
        <div class="uber-card">
            <h4 style="margin: 0 0 12px 0;">📈 Receita Semanal</h4>
        </div>
        """, unsafe_allow_html=True)
        
        days = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
        revenue_data = [random.randint(15000, 45000) for _ in range(7)]
        chart_html = create_admin_chart_html(revenue_data, days)
        components.html(chart_html, height=220, scrolling=False)
    
    with col_drivers:
        st.markdown("""
        <div class="uber-card">
            <h4 style="margin: 0 0 12px 0;">🚗 Motoristas</h4>
        </div>
        """, unsafe_allow_html=True)
        
        for driver in st.session_state.drivers[:6]:
            status = "Online" if driver.get("online") else "Offline"
            status_color = "#00b140" if driver.get("online") else "#ff4444"
            st.markdown(f"""
            <div class="history-item">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="margin: 0; font-weight: 500;">{driver['name']}</p>
                        <p style="color: #888; margin: 2px 0; font-size: 12px;">{driver['car']}</p>
                    </div>
                    <span style="color: {status_color}; font-size: 12px;">● {status}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 4px;">
                    <span style="color: #888; font-size: 11px;">⭐ {driver['rating']}</span>
                    <span style="color: #888; font-size: 11px;">{driver['rides_completed']} corridas</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_map, col_rides = st.columns([1, 1])
    
    with col_map:
        st.markdown("""
        <div class="uber-card">
            <h4 style="margin: 0 0 12px 0;">🗺️ Mapa de Motoristas</h4>
        </div>
        """, unsafe_allow_html=True)
        
        driver_markers = []
        for d in st.session_state.drivers:
            if d.get("online"):
                driver_markers.append({
                    "lat": d["lat"],
                    "lng": d["lng"],
                    "name": d["name"],
                    "car": d["car"],
                    "rating": d["rating"]
                })
        
        map_html = generate_map_html(
            LUANDA_CENTER["lat"],
            LUANDA_CENTER["lng"],
            markers=driver_markers
        )
        st.components.v1.html(map_html, height=350, scrolling=False)
    
    with col_rides:
        st.markdown("""
        <div class="uber-card">
            <h4 style="margin: 0 0 12px 0;">📋 Corridas Recentes</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.admin_rides:
            for ride in reversed(st.session_state.admin_rides[-8:]):
                st.markdown(f"""
                <div class="history-item">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="font-weight: 500;">{ride.get('driver', 'N/A')}</span>
                        <span class="history-price">{ride.get('price', 0):.0f} Kz</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 4px;">
                        <span class="history-route">{ride.get('from', 'N/A')} → {ride.get('to', 'N/A')}</span>
                        <span style="color: #888; font-size: 11px;">{ride.get('time', 'N/A')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="uber-card" style="text-align: center;">
                <p style="color: #888;">Nenhuma corrida registada</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("⚙️ Configurações de Preços", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.number_input("Tarifa Base (Kz)", value=PRICING["base_fare"], key="base_fare_input")
        with col2:
            st.number_input("Por Km (Kz)", value=PRICING["per_km"], key="per_km_input")
        with col3:
            st.number_input("Por Minuto (Kz)", value=PRICING["per_minute"], key="per_minute_input")
        with col4:
            st.number_input("Mínimo (Kz)", value=PRICING["minimum"], key="minimum_input")
        
        if st.button("Atualizar Preços", type="primary"):
            PRICING["base_fare"] = st.session_state.base_fare_input
            PRICING["per_km"] = st.session_state.per_km_input
            PRICING["per_minute"] = st.session_state.per_minute_input
            PRICING["minimum"] = st.session_state.minimum_input
            st.success("Preços atualizados!")
    
    with st.expander("📊 Estatísticas Detalhadas", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="uber-card">
                <h4 style="margin: 0 0 12px 0;">Métodos de Pagamento</h4>
            </div>
            """, unsafe_allow_html=True)
            
            payment_data = {
                "Dinheiro": random.randint(30, 50),
                "Multicaixa Express": random.randint(20, 40),
                "Unitel Money": random.randint(10, 30)
            }
            
            for method, count in payment_data.items():
                st.markdown(f"""
                <div class="history-item">
                    <div style="display: flex; justify-content: space-between;">
                        <span>{method}</span>
                        <span style="color: #00b140;">{count}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="uber-card">
                <h4 style="margin: 0 0 12px 0;">Horas Mais Movimentadas</h4>
            </div>
            """, unsafe_allow_html=True)
            
            hours = ["06-09", "09-12", "12-15", "15-18", "18-21", "21-00"]
            hourly_data = [random.randint(5, 25) for _ in range(6)]
            chart_html = create_earnings_chart_html(hourly_data, hours)
            components.html(chart_html, height=150, scrolling=False)

# ========== MAIN RENDER ==========
if st.session_state.current_view == "passenger":
    render_passenger_view()
elif st.session_state.current_view == "driver":
    render_driver_view()
else:
    render_admin_view()
