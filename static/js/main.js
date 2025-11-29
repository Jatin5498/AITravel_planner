// Initialize map
let map;
let markers = [];
let routeLines = [];

// Custom icons
const hotelIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34]
});

const attractionIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34]
});

const restaurantIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-orange.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34]
});

// Initialize map on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing map...');
    
    try {
        // Check if map div exists
        const mapDiv = document.getElementById('map');
        if (!mapDiv) {
            console.error('Map div not found!');
            return;
        }
        
        // Initialize map centered on Canada
        map = L.map('map').setView([56.1304, -106.3468], 4);
        console.log('Map initialized');
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{s}/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(map);
        console.log('Tiles added');
        
        // Load cities
        loadCities();
        
        // Handle form submission
        const form = document.getElementById('travelForm');
        if (form) {
            form.addEventListener('submit', handleFormSubmit);
            console.log('Form handler attached');
        } else {
            console.error('Travel form not found!');
        }
    } catch (error) {
        console.error('Error initializing map:', error);
    }
});

// Load available cities
async function loadCities() {
    try {
        const response = await fetch('/api/cities');
        const cities = await response.json();
        
        const citySelect = document.getElementById('city');
        cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city.value;
            option.textContent = `${city.name} (${city.hotels} hotels)`;
            citySelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading cities:', error);
    }
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const city = document.getElementById('city').value;
    const days = parseInt(document.getElementById('days').value);
    const budget = parseFloat(document.getElementById('budget').value);
    
    if (!name || !city) {
        alert('Please fill in all required fields');
        return;
    }
    
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
    
    // Clear previous markers and routes
    clearMap();
    
    try {
        const response = await fetch('/api/recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                city: city,
                days: days,
                budget: budget
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data);
            displayMap(data);
        } else {
            alert('Error: ' + (data.error || 'Failed to get recommendations'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error getting recommendations. Please try again.');
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

// Display results in sidebar
function displayResults(data) {
    const plan = data.plan;
    const locations = data.locations || [];
    
    // Show results section
    document.getElementById('results').style.display = 'block';
    
    // Count items
    const hotels = locations.filter(l => l.type === 'hotel');
    const attractions = locations.filter(l => l.type === 'attraction');
    const restaurants = locations.filter(l => l.type === 'restaurant');
    
    document.getElementById('hotelCount').textContent = hotels.length;
    document.getElementById('attractionCount').textContent = attractions.length;
    document.getElementById('restaurantCount').textContent = restaurants.length;
    
    // Display weather
    if (plan.weather && plan.weather.length > 0) {
        const weatherCard = document.getElementById('weatherCard');
        const weatherInfo = document.getElementById('weatherInfo');
        weatherInfo.innerHTML = '';
        
        plan.weather.slice(0, 3).forEach(day => {
            const badge = document.createElement('span');
            badge.className = 'weather-badge';
            badge.innerHTML = `${day.date || 'N/A'}: ${day.temperature || 0}°C, ${day.description || 'N/A'}`;
            weatherInfo.appendChild(badge);
        });
        
        weatherCard.style.display = 'block';
    }
    
    // Display hotels
    if (hotels.length > 0) {
        const hotelsCard = document.getElementById('hotelsCard');
        const hotelsList = document.getElementById('hotelsList');
        hotelsList.innerHTML = '';
        
        hotels.forEach(hotel => {
            const card = createLocationCard(hotel, 'hotel');
            hotelsList.appendChild(card);
        });
        
        hotelsCard.style.display = 'block';
    }
    
    // Display attractions
    if (attractions.length > 0) {
        const attractionsCard = document.getElementById('attractionsCard');
        const attractionsList = document.getElementById('attractionsList');
        attractionsList.innerHTML = '';
        
        attractions.forEach(attraction => {
            const card = createLocationCard(attraction, 'attraction');
            attractionsList.appendChild(card);
        });
        
        attractionsCard.style.display = 'block';
    }
    
    // Display restaurants
    if (restaurants.length > 0) {
        const restaurantsCard = document.getElementById('restaurantsCard');
        const restaurantsList = document.getElementById('restaurantsList');
        restaurantsList.innerHTML = '';
        
        restaurants.forEach(restaurant => {
            const card = createLocationCard(restaurant, 'restaurant');
            restaurantsList.appendChild(card);
        });
        
        restaurantsCard.style.display = 'block';
    }
}

// Create location card
function createLocationCard(location, type) {
    const card = document.createElement('div');
    card.className = 'recommendation-card location-marker';
    card.onclick = () => {
        // Center map on this location
        map.setView([location.lat, location.lng], 15);
    };
    
    const icon = type === 'hotel' ? 'fa-hotel' : 
                 type === 'attraction' ? 'fa-map-pin' : 'fa-utensils';
    const iconColor = type === 'hotel' ? 'hotel-icon' : 
                     type === 'attraction' ? 'attraction-icon' : 'restaurant-icon';
    
    let html = `
        <div class="d-flex justify-content-between align-items-start">
            <div>
                <h6><i class="fas ${icon} ${iconColor}"></i> ${location.name}</h6>
                ${location.rating ? `<small class="text-muted">⭐ ${location.rating}/5.0</small>` : ''}
                ${location.price ? `<small class="text-muted">💰 $${location.price.toFixed(2)}</small>` : ''}
                ${location.address ? `<br><small class="text-muted">📍 ${location.address}</small>` : ''}
            </div>
        </div>
    `;
    
    card.innerHTML = html;
    return card;
}

// Display map with markers and routes
function displayMap(data) {
    const locations = data.locations || [];
    const routes = data.route || {};
    
    if (locations.length === 0) {
        // Center on destination city (approximate)
        const cityCoords = getCityCoordinates(data.destination);
        map.setView(cityCoords, 10);
        return;
    }
    
    // Add markers
    const bounds = [];
    locations.forEach(location => {
        if (location.lat && location.lng && location.lat !== 0 && location.lng !== 0) {
            const marker = addMarker(location);
            bounds.push([location.lat, location.lng]);
        }
    });
    
    // Fit map to show all markers
    if (bounds.length > 0) {
        map.fitBounds(bounds, { padding: [50, 50] });
    }
    
    // Draw routes
    Object.keys(routes).forEach(day => {
        const dayRoute = routes[day];
        if (dayRoute.locations && dayRoute.locations.length > 1) {
            drawRoute(dayRoute.locations, day);
        }
    });
}

// Add marker to map
function addMarker(location) {
    let icon;
    if (location.type === 'hotel') {
        icon = hotelIcon;
    } else if (location.type === 'attraction') {
        icon = attractionIcon;
    } else {
        icon = restaurantIcon;
    }
    
    const marker = L.marker([location.lat, location.lng], { icon: icon })
        .addTo(map);
    
    // Popup content
    let popupContent = `<b>${location.name}</b><br>`;
    if (location.type) popupContent += `Type: ${location.type}<br>`;
    if (location.rating) popupContent += `Rating: ⭐ ${location.rating}/5.0<br>`;
    if (location.price) popupContent += `Price: $${location.price.toFixed(2)}<br>`;
    if (location.address) popupContent += `📍 ${location.address}`;
    
    marker.bindPopup(popupContent);
    markers.push(marker);
    
    return marker;
}

// Draw route on map
function drawRoute(locations, day) {
    const routePoints = locations
        .filter(loc => loc.latitude && loc.longitude && loc.latitude !== 0 && loc.longitude !== 0)
        .map(loc => [loc.latitude, loc.longitude]);
    
    if (routePoints.length < 2) return;
    
    // Create polyline
    const polyline = L.polyline(routePoints, {
        color: '#667eea',
        weight: 4,
        opacity: 0.7,
        smoothFactor: 1
    }).addTo(map);
    
    routeLines.push(polyline);
    
    // Add start/end markers
    if (routePoints.length > 0) {
        L.marker(routePoints[0]).addTo(map)
            .bindPopup(`<b>Start: ${day}</b>`);
        L.marker(routePoints[routePoints.length - 1]).addTo(map)
            .bindPopup(`<b>End: ${day}</b>`);
    }
}

// Clear map
function clearMap() {
    markers.forEach(marker => map.removeLayer(marker));
    routeLines.forEach(line => map.removeLayer(line));
    markers = [];
    routeLines = [];
}

// Get approximate coordinates for cities
function getCityCoordinates(city) {
    const coords = {
        'vancouver': [49.2827, -123.1207],
        'quebec': [46.8139, -71.2080],
        'saskatoon': [52.1332, -106.6700],
        'halifax': [44.6488, -63.5752],
        'montreal': [45.5017, -73.5673],
        'toronto': [43.6532, -79.3832],
        'victoria': [48.4284, -123.3656],
        'banff': [51.1784, -115.5708],
        'calgary': [51.0447, -114.0719],
        'ottawa': [45.4215, -75.6972]
    };
    return coords[city.toLowerCase()] || [56.1304, -106.3468];
}

