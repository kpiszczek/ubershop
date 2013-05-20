from django.forms import ModelForm
from board.models import Message, Board, Topic

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ('title',)
        
class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ('name','description')
        
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ('content',)