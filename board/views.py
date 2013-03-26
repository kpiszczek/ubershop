from board.forms import TopicForm, MessageForm, BoardForm

class BoardView():
    @classmethod
    def show_board(cls,request):
        raise NotImplemented
    
    @classmethod
    def show_topic(cls,request):
        raise NotImplemented
    
    @classmethod
    def show_message(cls,request):
        raise NotImplemented

    @classmethod
    def show_available_board(cls,request):
        raise NotImplemented
    
    @classmethod
    def create_topic(cls,request):
        raise NotImplemented
    
    @classmethod
    def create_board(cls,request):
        raise NotImplemented  
  
    @classmethod
    def submit_message(cls,request):
        raise NotImplemented
    
    @classmethod
    def show_news_board(cls,request):
        raise NotImplemented