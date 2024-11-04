# views 

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
class ChatConsumer(WebsocketConsumer):
    #initial req from client 
    def connect(self):
        self.room_group_name ='test' # to add the message of the user in the group call add group method
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, #create auto 
            self.channel_name
        )

        self.accept()
        # self.accept()
        # self.send(text_data=json.dumps({
        #     'type':'connection_established',
        #     'message':'You are now connected!',
        # }))

    def receive(self,text_data):
        text_data_json =json.loads(text_data)
        #data sentt by client
        message =text_data_json['message']
        # print('message',message)

        # to send message to everyone in that group call send message method
        async_to_sync(self.channel_layer.group_send)(
        self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )

        # self.send(text_data=json.dumps({
        #     'type':'chat',
        #     'message':message
        # }))
    def chat_message(self, event):
        #retriev message
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))