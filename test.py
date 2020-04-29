from mirai import Mirai, Plain, MessageChain, Friend, At, Group
import asyncio

qq = 3538826616 # 字段 qq 的值
authKey = 'adhekYgFgrf' # 字段 authKey 的值
mirai_api_http_locate = 'localhost:8080/ws' # httpapi所在主机的地址端口,如果 setting.yml 文件里字段 "enableWebsocket" 的值为 "true" 则需要将 "/" 换成 "/ws", 否则将接收不到消息.

app = Mirai(host="localhost", port="8080", authKey=authKey, qq=qq, websocket=True)

@app.receiver("FriendMessage")
async def event_gm(app: Mirai, friend: Friend, message: MessageChain):
    print(message.toString())
    if message.hasComponent(At):
        print('at me')

    await app.sendFriendMessage(friend, [
        Plain(text="Hello, world!")
    ])

@app.receiver("GroupMessage")
async def event_gm(app: Mirai, group: Group, message: MessageChain):
    print(message.toString())
    if message.hasComponent(At):
        print('at me')

    await app.sendGroupMessage(group.id, [
        Plain(text="Hello, world!")
    ])



if __name__ == "__main__":
    print("start test damon")
    app.run()