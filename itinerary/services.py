import random
import math
import google.generativeai as genai
from django.conf import settings

class OptimizationService:
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees) using Haversine formula.
        """
        # Convert decimal degrees to radians 
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r

    def optimize_route(self, start_location_data, locations):
        """
        Optimizes the route based on distance:
        Start -> Closest Temple -> Next Closest -> ... -> Lunch -> Start
        """
        
        # Separate locations by type
        temples = [loc for loc in locations if hasattr(loc, 'deity')]
        lunch_spots = [loc for loc in locations if hasattr(loc, 'cuisine')]
        pandits = [loc for loc in locations if hasattr(loc, 'specialization')]
        
        # Start point
        current_lat = start_location_data['lat']
        current_lng = start_location_data['lng']
        
        optimized_itinerary = []
        
        # 1. Add Pandit (if any) - They accompany the whole trip
        if pandits:
            pandit = pandits[0]
            optimized_itinerary.append({
                'location': pandit,
                'type': 'pandit',
                'arrival_time': "Start",
                'departure_time': "End",
                'activity': f"Accompanied by Pandit {pandit.name} ({pandit.specialization})",
                'distance_from_prev': 0
            })

        # 2. Sort Temples by distance from current location
        # Greedy approach: Find closest unvisited temple from current point
        unvisited_temples = list(temples)
        current_time_hour = 9 # Start at 9 AM
        
        while unvisited_temples:
            unvisited_temples.sort(key=lambda t: self.calculate_distance(current_lat, current_lng, t.latitude, t.longitude))
            next_temple = unvisited_temples.pop(0)
            
            dist = self.calculate_distance(current_lat, current_lng, next_temple.latitude, next_temple.longitude)
            
            optimized_itinerary.append({
                'location': next_temple,
                'type': 'temple',
                'arrival_time': f"{current_time_hour}:00 AM" if current_time_hour < 12 else f"{current_time_hour-12}:00 PM" if current_time_hour > 12 else "12:00 PM",
                'departure_time': f"{current_time_hour+1}:00 AM" if current_time_hour+1 < 12 else f"{current_time_hour+1-12}:00 PM" if current_time_hour+1 > 12 else "12:00 PM",
                'activity': f"Visit {next_temple.name}",
                'distance_from_prev': round(dist, 2)
            })
            
            # Update current location and time
            current_lat = next_temple.latitude
            current_lng = next_temple.longitude
            current_time_hour += 1.5 # Assume 1.5 hours per temple
            
        # 3. Add Lunch Spot (if any)
        if lunch_spots:
            lunch = lunch_spots[0]
            dist = self.calculate_distance(current_lat, current_lng, lunch.latitude, lunch.longitude)
            
            optimized_itinerary.append({
                'location': lunch,
                'type': 'lunch',
                'arrival_time': "1:00 PM", # Fixed lunch time for simplicity or calculated
                'departure_time': "2:00 PM",
                'activity': f"Lunch at {lunch.name} ({lunch.cuisine})",
                'distance_from_prev': round(dist, 2)
            })
            # Update current location to lunch spot
            current_lat = lunch.latitude
            current_lng = lunch.longitude

        # 4. Return to Start
        dist_to_start = self.calculate_distance(current_lat, current_lng, start_location_data['lat'], start_location_data['lng'])
        optimized_itinerary.append({
            'location': {'name': start_location_data['name'], 'address': 'End of Journey'}, # Mock object
            'type': 'end',
            'arrival_time': "Evening",
            'departure_time': "-",
            'activity': f"Return to {start_location_data['name']}",
            'distance_from_prev': round(dist_to_start, 2)
        })
        
        # Generate Route Matrix for Map
        route_matrix = [{'lat': start_location_data['lat'], 'lng': start_location_data['lng'], 'name': 'Start Location'}]
        for item in optimized_itinerary:
            if item['type'] not in ['pandit', 'end']:
                route_matrix.append({
                    'lat': item['location'].latitude,
                    'lng': item['location'].longitude,
                    'name': item['location'].name
                })
        # Add start location at the end to complete the loop
        route_matrix.append({'lat': start_location_data['lat'], 'lng': start_location_data['lng'], 'name': 'End Location'})

        return optimized_itinerary, route_matrix

class AIService:
    def generate_summary(self, itinerary):
        """
        Generates a summary of the itinerary using Gemini API.
        """
        # TODO: Use environment variable for API key
        genai.configure(api_key="[add your API key here]")
        model = genai.GenerativeModel('gemini-2.0-flash')

        places = []
        pandit_info = ""

        for item in itinerary:
            if item['type'] == 'pandit':
                loc = item['location']
                pandit_info = f"Pandit {loc.name} (Specialization: {loc.specialization}) will accompany you to the temples and help with rituals."
            elif item['type'] == 'end':
                continue
            else:
                loc = item['location']
                places.append(loc.name)

        prompt = f"Create a short, engaging summary for a pilgrimage itinerary that visits these places in order: {', '.join(places)}. Mention the spiritual significance. {pandit_info} Treat the Pandit as a person accompanying the user, not a place."
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"
