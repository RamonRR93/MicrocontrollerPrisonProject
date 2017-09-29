import json, random, re, urllib, calendar
from pprint import pprint
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
    

def response_button_start(fbid, output_wording):
    response = json.dumps(
        {"recipient":{"id":fbid}, 
        "message":{
            "attachment":{                            
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "image_aspect_ratio": "square",
                    "elements":[
                        {
                            "title":output_wording,
                            "image_url":"https://uqr.me/wp-content/uploads/2015/10/qr-code-scan-hand.png",
                            "buttons":[
                                {
                                    "type":"postback",
                                    "title":"Help using bot",
                                    "payload":"help"
                                }
                            ]
                        }   
                    ]
                }
            }
        }
    })
    return response


def response_button_help(fbid, output_wording):
    response = json.dumps(
        {"recipient":{"id":fbid},
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":output_wording,
                    "buttons":[
                        {
                            "type":"postback",
                            "title":"See past QRs",
                            "payload":"past_qrs"
                        }
                    ]
                }
            }
        }
    })
    return response



def response_button_other(fbid,output_wording):
    response = json.dumps(
        {"recipient":{"id":fbid},
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":output_wording,
                    "buttons":[
                        {
                            "type":"postback",
                            "title":"Help using bot",
                            "payload":"help"
                        },
                        {
                            "type":"postback",
                            "title":"See past QRs",
                            "payload":"past_qrs"
                        }
                    ]
                }
            }
        }
    })

    return response



def response_msg(fbid, output_wording):
    response = json.dumps(
        {"recipient":{"id":fbid}, 
        "message":{
            "text":output_wording
        }
    })
    return response


def response_sms(fbid, output_wording):
    response = json.dumps(
        {"recipient":{"id":fbid},
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":output_wording,
                    "buttons":[
                        {
                            "type":"web_url",
                            "title":"Send SMS",
                            "url":"https://07768c4e.ngrok.io/fb_chatbot/97941ca540b5833722be169aec1dd31f8233bb2ba541d00e6a"
                        }
                    ]
                }
            }
        }
    })

    return response

def response_email(fbid, output_wording):
    response = json.dumps(
        {"recipient":{"id":fbid},
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":output_wording,
                    "buttons":[
                        {
                            "type":"web_url",
                            "title":"Send Email",
                            "url":"https://07768c4e.ngrok.io/fb_chatbot/97941ca540b5833722be169aec1dd31f8233bb2ba541d00e6a"
                        }
                    ]
                }
            }
        }
    })

    return response

def response_image(fbid, output_wording, url):
    response = json.dumps(
        {"recipient":{"id":fbid}, 
        "message":{
            "attachment":{                            
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "image_aspect_ratio": "square",
                    "elements":[
                        {
                            "title":output_wording,
                            "image_url":url,
                        }   
                    ]
                }
            }
        }
    })
    return response

def response_website(fbid, output_wording, url):
    response = json.dumps(
        {"recipient":{"id":fbid},
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":output_wording,
                    "buttons":[
                        {
                            "type":"web_url",
                            "title":"Open Link",
                            "url":url
                        }
                    ]
                }
            }
        }
    })

    return response

def response_past_scans(fbid, scans):
    elements = []
    for scan in scans:
        elements.append({
                        "title": scan['style'],
                        "subtitle": "Taken on: " + str(scan['date']),
                        "image_url":scan['url'],
                        "buttons":[
                            {
                                "type":"web_url",
                                "title":"Check URL",
                                "url": scan['url']
                            }         
                        ]     
                    })


    response = json.dumps(
        {"recipient":{"id":fbid},
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "image_aspect_ratio": "square",
                    "elements": elements
                    
                }
            }
        }
    })
    
    return response
