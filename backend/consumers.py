import json
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import User, Bug, Comment

# User = get_user_model() # Ambiguous

class CommentConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['bug_heading']
        self.room_group_name = f'group_{self.room_name}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # here text_data is incoming as JSON data from frontend
        text_data_json = json.loads(text_data)

        #grabbing info of comment
        user = User.objects.get(access_token=text_data_json['access_token'])
        bug = Bug.objects.get(pk=text_data_json['bug_pk'])    # Ambiguous (thinking of adding one more thing here)
        comment = text_data_json['comment']
        
        # try catch lagana h yaha
        # creating comment
        newComment = Comment(body=comment, buggy=bug, commentator=user)
        newComment.save()

        self.send_comments(bug)

    def send_comments(self, Bug):
        comments = Comment.objects.filter(buggy=Bug)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'meth',
                'comments': json.dumps(comments_list(comments))
            }
        )

    # function to convert comments from queryset to list
    def comments_list(self, comments):
        res = []
        for comment in comments:
            obj = {
                'pk': comment.pk,
                'body': comment.body,
                'bug': str(comment.bug),
                'commentator': comment.commentator,
                'timestamp': str(comment.timestamp),
            }
            res.append(obj)
        return res

    def meth(self, event):
        comments = event['comments']
        self.send(text_data=json.dumps(comments))
