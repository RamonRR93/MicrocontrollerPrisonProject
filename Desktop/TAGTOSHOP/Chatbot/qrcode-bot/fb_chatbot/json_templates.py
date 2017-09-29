    
    response = json.dumps(
        {"recipient":{"id":FBID},
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "image_aspect_ratio": "square",
                    "elements": [
                        {
                        "title": TITLE,
                        "image_url": URL IMAGE,
                        "buttons":[
                            {
                            "type":"payment",
                            "title":"buy",
                            "payload":"checkout",
                            "payment_summary":{
                                "currency":"USD",
                                "payment_type":"FIXED_AMOUNT",
                                "is_test_payment" : True, 
                                "merchant_name":"TFM - ICAI",
                                "requested_user_info":[
                                    "contact_name",
                                    "contact_phone",
                                    "contact_email"
                                    ],
                                    "price_list": PRODUCT PRICE LIST
                                }
                            }
                        ]     
                    }
                    ]                   
                }
            }
        }
    })

    return response




    GROUPS = []
    for ELEMENT in LIST:
        GROUPS.append({
                        "title":TÍTULO,
                        "subtitle":SUBTÍTULO,
                        "image_url":URL IMAGEN,
                        "buttons":[
                            {
                                "type":"postback",
                                "title":TEXTO BOTON1,
                                "payload":CALLBACK1
                            },{
                                "type":"postback",
                                "title":TEXTO BOTON2,
                                "payload":CALLBACK2
                            },{
                                "type":"postback",
                                "title":TEXTO BOTON3,
                                "payload":CALLBACK3
                            }
                        ]    
                    })

    response = json.dumps(
        {"recipient":{"id":FBID},
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "image_aspect_ratio": "square",
                    "elements": GROUPS
                }
            }
        }
    })
    
    return response
    


    GROUPS = []
    for ELEMENT in LIST:
        GROUPS.append({
                        "content_type":"text",TÍTULO,
                        "payload":CALLBACK,
                        "image_url":URL IMAGEN
                        })

    response = json.dumps(
        {"recipient":{"id":FBID},
        "message":{
            "text":"Pick a color:",
            "quick_replies":GROUPS
        }
    })

    return response




    response = json.dumps(
        {"recipient":{"id":FBID}, 
        "message":{
            "attachment":{                            
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "image_aspect_ratio": "square",
                    "elements":[
                        {
                            "title":TÍTULO,
                            "subtitle":SUBTÍTULO,
                            "image_url":URL IMAGEN,
                            "buttons":[
                                {
                                    "type":"postback",
                                    "title":TEXTO BOTON1,
                                    "payload":CALLBACK1
                                },{
                                    "type":"postback",
                                    "title":TEXTO BOTON2,
                                    "payload":CALLBACK2
                                },{
                                    "type":"postback",
                                    "title":TEXTO BOTON3,
                                    "payload":CALLBACK3
                                }
                            ]
                        }   
                    ]
                }
            }
        }
    })
    return response




    response = json.dumps(
        {"recipient":{"id":FBID}, 
        "message":{
            "text":TEXTO
        }
    })
    return response




    response = json.dumps(
        {"recipient":{"id":FBID},
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":TEXTO,
                    "buttons":[
                        {
                            "type":"postback",
                            "title":TEXTO BOTON1,
                            "payload":CALLBACK1
                        },{
                            "type":"postback",
                            "title":TEXTO BOTON2,
                            "payload":CALLBACK2
                        },{
                            "type":"postback",
                            "title":TEXTO BOTON3,
                            "payload":CALLBACK3
                        }
                    ]
                }
            }
        }
    })
    return response

   




