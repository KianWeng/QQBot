# coding: utf-8
import logging
import pprint
import requests
import json

logger = logging.getLogger(__name__)

class Info:

    def __init__(self, city = None, province = None, street = None): 
        self.city = city
        self.province = province
        self.street = street


class Tuling(object):
    """
    图灵机器人
    """

    url = 'http://www.tuling123.com/openapi/api/v2'

    def __init__(self, api_key=None):
        self.session = requests.Session()
        # noinspection SpellCheckingInspection
        self.api_key = api_key or '7c8cdb56b0dc4450a8deef30a496bd4c'

    def _create_payload_json(self, type, text, info):
        """
        根据消息类型生成对应的json报文
        """

        if type == 0:
            perception = dict(inputText = dict(text = text))
            selfInfo = dict(location = dict(city = info.city, province = info.province, street = info.street))
        elif type == 1:
            perception = dict(inputImage = dict(url = text))
            selfInfo = dict(location = dict(city = info.city, province = info.province, street = info.street))
        elif type == 2:
            perception = dict(inputMedia = dict(url = text))
            selfInfo = dict(location = dict(city = info.city, province = info.province, street = info.street))
        
        userInfo = dict(apiKey = self.api_key, userId = '123456789')
        payload = dict(reqType = type, perception = perception, selfInfo = selfInfo, userInfo = userInfo)
        payloadJson = json.dumps(payload)
        #logger.debug('Tuling payload:\n' + pprint.pformat(payload))
        print('Tuling payload:\n' + pprint.pformat(payload))

        return payloadJson
    
    def _post_msg(self, payloadJson):
        """
        从api获取回复消息
        :param payloadJson:API接口 payload json字符串
        """
        def process_answer():
            """
            处理回复的消息
            """
            #logger.debug('Tuling answer:\n' + pprint.pformat(answer))
            print('Tuling answer:\n' + pprint.pformat(answer))
            
            code = -1
            resultUrl = ''
            resultText = ''
            if answer:
                code = answer['intent']['code']
                #print('code is ')
                #print(code)

            if code >= 10000:
                resultsList = answer['results']
                for result in resultsList:
                    resultType = result['resultType']
                    resultValue = result['values']
                    if resultType == 'url':
                        resultUrl = resultValue['url']
                    elif resultType == 'text':
                        resultText = resultValue['text']

                if not resultText:
                    resultText = '我不明白你的意思'
            else:
                resultText = '我不明白你的意思'

            return dict(text = resultText, url = resultUrl)

        try:
            r = self.session.post(self.url, data=payloadJson)
            answer = r.json()
        except:
            answer = None
        finally:
            return process_answer()
    
    def reply_text(self, type, msg, info):
        """
        返回消息的答复文本
        :param type: 消息类型 0：text 1：图片 2：音频
        :param msg: text文本或者url
        :param info: 用户参数
        :return: 答复文本
        :rtype: dict
        """

        payloadJson = self._create_payload_json(type, msg, info)
        reply = self._post_msg(payloadJson)

        return reply