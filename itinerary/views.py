from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Pandit, Temple, LunchSpot, Booking
from .services import OptimizationService, AIService
from datetime import datetime

def landing(request):
    return render(request, 'itinerary/landing.html')

def index(request):
    # Fetch all locations initially
    temples = Temple.objects.all()
    lunch_spots = LunchSpot.objects.all()
    
    # Pandits might be filtered by date via AJAX, but load all for now
    pandits = Pandit.objects.all()

    context = {
        'pandits': pandits,
        'temples': temples,
        'lunch_spots': lunch_spots,
    }
    return render(request, 'itinerary/index.html', context)

def generate_itinerary(request):
    if request.method == 'POST':
        pandit_id = request.POST.get('pandit')
        temple_ids = request.POST.getlist('temples')
        lunch_spot_id = request.POST.get('lunch_spot')
        
        start_location_lat = float(request.POST.get('start_lat', 28.6139)) # Default Delhi
        start_location_lng = float(request.POST.get('start_lng', 77.2090))
        start_location_name = request.POST.get('start_location', 'New Delhi')
        
        date_str = request.POST.get('date')
        
        # Fetch objects
        pandit = Pandit.objects.get(id=pandit_id) if pandit_id else None
        temples = Temple.objects.filter(id__in=temple_ids)
        lunch_spot = LunchSpot.objects.get(id=lunch_spot_id) if lunch_spot_id else None

        selected_locations = []
        if pandit: selected_locations.append(pandit)
        selected_locations.extend(list(temples))
        if lunch_spot: selected_locations.append(lunch_spot)

        start_location_data = {
            'lat': start_location_lat,
            'lng': start_location_lng,
            'name': start_location_name
        }

        # 1. Optimize Route
        optimization_service = OptimizationService()
        optimized_itinerary, route_matrix = optimization_service.optimize_route(start_location_data, selected_locations)

        # 2. Generate AI Summary
        ai_service = AIService()
        summary = ai_service.generate_summary(optimized_itinerary)

        context = {
            'itinerary': optimized_itinerary,
            'summary': summary,
            'route_matrix': route_matrix,
            'pandit': pandit,
            'date': date_str,
            'start_location': start_location_name
        }
        return render(request, 'itinerary/result.html', context)
    
    return redirect('index')

def book_pandit(request):
    if request.method == 'POST':
        pandit_id = request.POST.get('pandit_id')
        user_name = request.POST.get('user_name')
        date_str = request.POST.get('date')
        
        if not all([pandit_id, user_name, date_str]):
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'})
            
        try:
            booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            pandit = get_object_or_404(Pandit, id=pandit_id)
            
            # Check availability
            if Booking.objects.filter(pandit=pandit, booking_date=booking_date).exists():
                 return JsonResponse({'status': 'error', 'message': 'Pandit is already booked for this date'})

            Booking.objects.create(
                pandit=pandit,
                user_name=user_name,
                booking_date=booking_date
            )
            return JsonResponse({'status': 'success', 'message': 'Booking confirmed!'})
        except ValueError:
             return JsonResponse({'status': 'error', 'message': 'Invalid date format'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def pandit_dashboard(request):
    bookings = Booking.objects.all().order_by('-booking_date')
    return render(request, 'itinerary/pandit_dashboard.html', {'bookings': bookings})
