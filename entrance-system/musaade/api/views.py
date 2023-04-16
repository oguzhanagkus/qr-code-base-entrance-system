import json
import logging
import datetime

from django.utils import timezone
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from .serializers import LocationSerializer, PersonnelActivitySerializer, HESActivitySerializer
from entrance_system import utils
from entrance_system.models import Personnel, Location, PersonnelActivity, HESActivity
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

@csrf_exempt
def make_query(request):
    response = {"result": False}
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            api_token = data["api_token"]
            qr_code_data = data["qr_code_data"]

            location = Location.objects.all().filter(api_token=api_token).first()
            if location:
                if location.active:
                    if location.get_qr_code_type_display() == "Personnel":
                        personnel = Personnel.objects.all().filter(qr_code_data=qr_code_data).first()
                        if personnel:
                            activity = PersonnelActivity(personnel=personnel, location=location)
                            if personnel.active:
                                if len(location.departments.filter(name=personnel.department.name)) > 0:
                                    response["result"] = True
                                    activity.result = True
                                    activity.message = "Entrance allowed."
                                else:
                                    activity.message = "Personnel is not allowed to enter this location."
                            else:
                                activity.message = "Personnel is not active."
                            activity.save()
                            personnel.last_activity = activity.time
                            personnel.save()
                            location.last_activity = activity.time
                            location.save()
                        else:
                            logging.warning("QR code is not belong any personnel: {}".format(qr_code_data))
                    else:
                        api_response = utils.ask_to_hes_api(qr_code_data)
                        if api_response["success"]:
                            response["result"] = api_response["data"]["citizen"]["health_status"]
                            activity = HESActivity(
                                first_name=api_response["data"]["citizen"]["first_name"],
                                last_name=api_response["data"]["citizen"]["last_name"],
                                result=api_response["data"]["citizen"]["health_status"],
                                location=location)
                            activity.save()
                            location.last_activity = activity.time
                            location.save()
                        else:
                            logging.warning("API request failed.")
                else:
                    logging.warning("Location is not active: {}".format(location.name))
            else:
                logging.warning("API token is not belong any location: {}".format(api_token))
    except Exception as exception:
        logging.exception("Exception occurred while handling query. Error: {}".format(str(exception)))
    finally:
        return JsonResponse(response)


class LocationsView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        data = []
        try:
            query = Location.objects.all().filter(active=True).order_by("id")
            serializer = LocationSerializer(query, many=True)
            for location in serializer.data:
                data.append(location)
        except:
            pass
        finally:
            return Response(data)


class ActivityView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def post(self, request):
        data = {}
        try:
            location_id = json.loads(request.body)["id"]
            location = Location.objects.get(id=location_id)
            if location.get_qr_code_type_display() == "Personnel":
                activity = PersonnelActivity.objects.all().order_by("-id").first()
                if activity.time > (timezone.now() - datetime.timedelta(seconds=5)):
                    serializer = PersonnelActivitySerializer(activity, many=False)
                    data = serializer.data
            else:
                activity = HESActivity.objects.all().order_by("-id").first()
                if activity.time > (timezone.now() - datetime.timedelta(seconds=5)):
                    serializer = HESActivitySerializer(activity, many=False)
                    data = serializer.data
        except:
            pass
        finally:
            print(data)
            return Response(data)
