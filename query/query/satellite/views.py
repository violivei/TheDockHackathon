from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from mapbox import Static
import json


@csrf_exempt
def satellite(request):
    data = {}

    if request.method == "POST":
        try:
            body = json.loads(request.body)

            if "lat" in body and "lon" in body:
                lat = body['lat']
                lon = body['lon']

                service = Static()
                service_response = service.image('mapbox.satellite', lon=lon, lat=lat, z=18)

                with open('/Users/s.hamiti/Desktop/wd/hackathon/tmp/test.jpg', 'wb') as output:
                    output.write(service_response.content)
                  


                response = body['lat']

            else:
                data["error"] = "Please input lat and lon"
                return JsonResponse(data)

        except Exception as e:
            response = str(e)

        data.update({'response': response})

    return JsonResponse(data)



