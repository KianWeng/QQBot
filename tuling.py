# coding: utf-8
import logging
import pprint
import requests

from mirai import Marai, Friend, Plain, Member, Image


logger = logging.getLogger(__name__)

class Info:

    def __init__(self, city, province, street) 
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

    def create_payload_json(self, type, text, info):
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
        payload = dict(reqType = type, perception = perception, userInfo = userInfo)
        payloadJson = json.dumps(payload)
        logger.debug('Tuling payload:\n' + pprint.pprint(payload))

        return payloadJson
    
    def post_msg(self, payloadJson):
        """
        从api获取回复消息
        :param payloadJson:API接口 payload json字符串
        """
        def process_answer():
            """
            处理回复的消息
            """
            logger.debug('Tuling answer:\n' + pprint.pprint(answer))
            
            code = -1
            if answer:
                code = answer.get('code', -1)

            if code >= 10000:
                text = answer.get('text')
                if not text:
                    text = '我不明白你的意思'
                url = answer.get('url')
            else
                text = '我不明白你的意思'
                url = ''

            return dict(text = text, url = url)

        try:
            r = self.session.post(self.url, json=payload)
            answer = r.json()
        except:
            answer = None
        finally:
            return process_answer()
    
    def reply_text(self, app: Marai, friend: Friend):
        """
        返回消息的答复文本
        :param msg: Message 对象
        :param at_member: 若消息来自群聊，回复时 @发消息的群成员
        :return: 答复文本
        :rtype: str
        """
       
        create_payload_json(frined.)
        reply = post_msg(payloadJson)
        app.sendFriendMessage(friend, [Plain(text= reply)])

        if not msg.bot:
            raise ValueError('bot not found: {}'.format(msg))

        if not msg.text:
            return

        from wxpy.api.chats import Group
        if at_member and isinstance(msg.chat, Group) and msg.member:
            location = get_location(msg.member)
        else:
            # 使该选项失效，防止错误 @ 人
            at_member = False
            location = get_location(msg.chat)

        user_id = get_context_user_id(msg)

        if location:
            location = location[:30]

        info = str(get_text_without_at_bot(msg))[-30:]

        payload = dict(
            key=self.api_key,
            info=info,
            userid=user_id,
            loc=location
        )

        logger.debug('Tuling payload:\n' + pprint.pformat(payload))

        # noinspection PyBroadException
        try:
            r = self.session.post(self.url, json=payload)
            answer = r.json()
        except:
            answer = None
        finally:
            return process_answer()