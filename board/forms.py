from django.forms import ModelForm
from board.models import Message, Board, Topic

class TopicForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Temat"
    class Meta:
        model = Topic
        fields = ('title',)
        
class BoardForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BoardForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nazwa dzialu"
        self.fields['description'].label = "Opis dzialu"
    class Meta:
        model = Board
        fields = ('name','description',)
        
class MessageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = "Twoja wiadomosc"
    class Meta:
        model = Message
        fields = ('content',)