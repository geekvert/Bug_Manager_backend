import json
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import User, Bug, Comment

# User = get_user_model() # Ambiguous

class CommentConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['bug_heading']   # prob
        self.room_group_name = f'group_{self.room_name}'
        print('ROOM NAME: '+self.room_name)
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

    def add_comment(self, data):
        user = User.objects.get(access_token=data['access_token'])
        bug = Bug.objects.get(heading=data['bug_heading'])
        comment = data['comment']
        
        try:
            newComment = Comment(body=comment, buggy=bug, commentator=user)
            newComment.save()
        except:
            # returning error response
            self.send_comment({'command': 'Some error happened in saving comment'})

        content = {
            'command': 'add_comment',
            'comment': self.comment_to_json(newComment),
        }
        self.send_content(content)

    def fetch_comments(self, data):
        comments = Comment.objects.filter(buggy=Bug.objects.get(heading=data['bug_heading']))
        content = {
            'command': 'fetch_comments',
            'comments': self.comments_to_json(comments)
        }
        self.send_content(content)

    commands = {
        'fetch_comments': fetch_comments,   # func to fetch all existing comments associated with a bug
        'add_comment': add_comment,     # func to add a comment for a bug
    }

    def receive(self, text_data):
        data = json.loads(text_data)
        print(repr(data))
        self.commands[data['command']](self, data)

        # incoming text data for add_comment
        # {
        #     access_token,
        #     bug_heading,
        #     comment (body),
        # }

    

    def comments_to_json(self, comments):
        result = []
        for comment in comments:
            result.append(self.comment_to_json(comment))
        return result

    def comment_to_json(self, comment):
        return {
            'id': str(comment.id),
            'body': comment.body,
            'commentator': comment.commentator, # maybe str() krna pade yaha
            'bug': comment.buggy,
            'timesatmp': str(comment.timesatmp),
        }

    # def send_content(self, content):
    #     self.send(text_data=json.dumps(content))

    # functions responsible for sending data
    def send_content(self, content):
        # Send comments to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            content
        )

# user -> room_group pe subscribe -> whenever message send/received sabpe jaayega
# har bug ke liye alag room hoga
