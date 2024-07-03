from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Search
from .forms import SearchForm
import folium
import geocoder

# Create your views here.


def index(request):
    m = folium.Map(location=[19, -12], zoom_start=10)

    form = SearchForm()
    m = m._repr_html_()
    
    context = {
        "form": form,
        "m": m
    }

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        address = Search.objects.all().last()

        if address:
            location = geocoder.osm(address)
            lat = location.lat
            lng = location.lng
            country = location.country
        
            if (lat == None or lng == None) and bool(address):
                print(address)
                address.delete()
                return HttpResponse('You address input is invalid')

            # Create Map Object

            folium.Marker([lat, lng], tooltip='Click for more',
                        popup=country).add_to(m)
            # Get HTML Representation of Map Object

    return render(request, 'index.html', context)
