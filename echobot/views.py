import os
import requests
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

line_bot_api = LineBotApi('q7TWa/81a0nmW9GnqF6+u8qaFoMbi6q3Dq5VK2QM7FV8UIx3nQk5+luk5GpASk/bm5qtAmimAyA2/Ifdg6a0hH3dwMdfdAoRiGE8TF/IiRXriLsK7j9FDHlQUC34zr7EXiktLqyT5btGhtCTJXbTZQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler("57141ec8f7ba725d4fa3fa97a5bd5169")

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            messages = (
                "Invalid signature. Please check your channel access token/channel secret."
            )
            logger.error(messages)
            return HttpResponseBadRequest(messages)
        return HttpResponse("OK")

@handler.add(event=MessageEvent, message=TextMessage)
def handl_message(event):
    outInfo = ''
    outInfo = crawler("content")
    if outInfo != '':
            message = TextSendMessage(text="汪汪")
            line_bot_api.reply_message(
                event.reply_token,
                message)
def crawler(content):
    
    prefs = {  
        'profile.default_content_setting_values' :  {  
            'notifications' : 2  
                }  
            }  
    chrome_options.add_experimental_option('prefs',prefs)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")      #不開啟實體瀏覽器背景執行
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get("https://www.cwb.gov.tw/V8/C/W/Town/Town.html?TID=1000806") #南投名間鄉
    Temp = driver.find_element_by_id('GT_C_T').text #現在溫度
    bodyTemp = driver.find_element_by_id('GT_C_AT').text #體感溫度
    RelativeHumidity = driver.find_element_by_id('GT_RH').text #相對溼度
    Rain = driver.find_element_by_id('GT_Rain').text #降雨量
    Sunrise = driver.find_element_by_id('GT_Sunrise').text #日出時間
    Sunset = driver.find_element_by_id('GT_Sunset').text
    driver.quit()
    # content="\n"+"名間鄉天氣概況"+"\n"+"\n"+"現在溫度 : "+Temp+"°C"+"\n"+"體感溫度 : "+bodyTemp+"°C"+"\n"+"相對溼度 : "+RelativeHumidity+"%"+"\n"+"降雨量 : "+Rain+"mm"+"\n"+"日出時間 : "+Sunrise+"\n"+"日落時間 : "+Sunset
    content = ""
    content= {
        "現在溫度":Temp,
        "體感溫度":bodyTemp,
        "相對溼度":RelativeHumidity,
        "降雨量":Rain,
        "日出時間":Sunrise,
        "日落時間":Sunset
    }
    # print(content)
    return content
    