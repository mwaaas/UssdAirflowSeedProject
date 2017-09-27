from ussd.core import UssdView, UssdRequest
from django.http import HttpResponse
from django.conf import settings
import os


class AfricasTalkingUssdGateway(UssdView):
    customer_journey_conf = os.path.join(settings.BASE_DIR, 'register_app/customer-journey.yml')
    customer_journey_namespace = 'demo-customer-journey'

    def post(self, req):
        list_of_inputs = req.data['text'].split("*")
        text = "*" if len(list_of_inputs) >= 2 and \
                      list_of_inputs[-1] == "" and \
                      list_of_inputs[-2] == "" else list_of_inputs[
            -1]

        session_id = req.data['sessionId']
        if req.data.get('use_built_in_session_management', False):
            session_id = None
        ussd_request = UssdRequest(
            phone_number=req.data['phoneNumber'].strip('+'),
            session_id=session_id,
            ussd_input=text,
            raw_input=req.data['text'],
            service_code=req.data['serviceCode'],
            language=req.data.get('language', 'en'),
            use_built_in_session_management=req.data.get(
                'use_built_in_session_management', False)
        )

        return ussd_request

    def ussd_response_handler(self, ussd_response):
        if self.request.data.get('serviceCode') == 'test':
            return super(AfricasTalkingUssdGateway, self).\
                ussd_response_handler(ussd_response)
        if ussd_response.status:
            res = 'CON' + ' ' + str(ussd_response)
            response = HttpResponse(res)
        else:
            res = 'END' + ' ' + str(ussd_response)
            response = HttpResponse(res)
        return response