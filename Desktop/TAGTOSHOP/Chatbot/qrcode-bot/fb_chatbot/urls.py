from django.conf.urls import include, url
from .views import FbChatbotView, WebView

urlpatterns = [
                url(r'^36da0722f66505783e31e2365a7bb3c1b841d13b392d20cf06/?$', FbChatbotView.as_view()),
                url(r'^97941ca540b5833722be169aec1dd31f8233bb2ba541d00e6a/?$', WebView),
               ]

               