import pandas as pd
import message_process
import json, requests, random, re, urllib
import zbar
from PIL import Image
from pprint import pprint
from django.views import generic
from django.shortcuts import render_to_response
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json, requests
from models import FacebookUser, QRCode, Scan

VERIFY_TOKEN = '143413513'
PAGE_ACCESS_TOKEN = 'EAAUSfBfBC8ABAJjSyeTgkZA8i4GxqzIDQTneVaxrxedxDVWFB47LdmkE8NkN3ctyFLA9idmpSh0cqZBSaAlSAPU03yDOKOGEnKLYWEnvCD7ucZCNsjxdffHppgEZBR3whKaop48ZBPanVsAZCLzDacVCptMVug5XrXcSgAiwZCZBvwZDZD'

def post_facebook_message(fbid, received_message, is_callback):           
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN    
    fbuser, created = FacebookUser.objects.get_or_create(fb_id=fbid)
    
    #graph = facebook.GraphAPI(access_token=PAGE_ACCESS_TOKEN, version='2.9')
    try:
       if fbuser.has_fb_data == False:
            profile = graph.get_object(fbuser.fb_id)
            pprint(profile)
            for key in profile.keys():
                if key == 'first_name': fbuser.first_name = first_name
                if key == 'last_name': fbuser.last_name = last_name
                if key == 'profile_pic': fbuser.profile_pic = profile_pic
                if key == 'locale': fbuser.locale = locale
                if key == 'gender': fbuser.gender = gender
                if key == 'timezone': fbuser.timezone = str(timezone)
                fbuser.has_fb_data = True
                fbuser.save()

    except Exception as e:
        pass

    if received_message in ["GET_STARTED_PAYLOAD","hello","hi", "Hello", "Hi"]:
        response_msg1 = message_process.get_response(fbuser, "get_started_payload", True)
        response_msg2 = message_process.get_response(fbuser, "image_start", True)
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg1) 
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg2) 

    else:
        response_msg = message_process.get_response(fbuser, received_message, is_callback)
        pprint(response_msg)
        status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)


class FbChatbotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))                
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:            
            for message in entry['messaging']:                
                    # Check to make sure the received call is a message call
                    # This might be delivery, optin, postback for other events 
                    sender_id = message['sender']['id']

                    if 'message' in message:  
                        if 'quick_reply' in message['message']:
                            if "seeproduct_" in message['message']['quick_reply']['payload']:
                                post_facebook_message(sender_id, message['message']['quick_reply']['payload'], True)
                            else:
                                post_facebook_message(sender_id, message['message']['quick_reply']['payload'], False)

                        elif 'text' in message['message']:
                            post_facebook_message(sender_id, message['message']['text'], False)
                           

                        elif 'attachments' in message['message']:
                            try:
                                url_image = message['message']['attachments'][0]['payload']['url']
                                img = urllib.urlretrieve(url_image, '/Users/RamonRodriganez/Desktop/TFM/Chatbot/qr.png')

                                # scan the image for barcodes
                                pil = Image.open(img[0]).convert('L')
                                width, height = pil.size
                                raw = pil.tobytes()
                                 
                                # wrap image data
                                image = zbar.Image(width, height, 'Y800', raw)

                                # scan the image for barcodes
                                scanner = zbar.ImageScanner()
                                scanner.scan(image)

                            # extract results
                                for symbol in image:
                                    # print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
                                    response_msg = "qrvalid_" + str(symbol.data)
                                    post_facebook_message(sender_id, response_msg, True)
                                
                            except Exception as e:
                                post_facebook_message(sender_id, 'qrinvalid', True)
                        

                    elif 'postback' in message:
                        post_facebook_message(sender_id, message['postback']['payload'], True)

        return HttpResponse()

def WebView(request):
    pprint(request)
    qrcode = Scan.objects.latest('date').qrcode
    return render_to_response('index.html', {'qrcode': qrcode})
