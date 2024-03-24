import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from cva.views import processText

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # self.room_group_name = 'test'
        self.accept()

        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )

        # self.accept()
        self.send(text_data=json.dumps({
            'type':'connection_established',
            'message':'Your are now connected'
        }))
   

    def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        print("Debugging:",text_data_json)
        message = text_data_json['message']
        print(message)
        res = processText(message)
        print(res)
        self.send(text_data=json.dumps({
            'type':'message_received',
            'message':res
        }))