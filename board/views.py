from django.shortcuts import render_to_response
from django.template import RequestContext

from board.forms import TopicForm, MessageForm, BoardForm
from board.models import Board, Message, Topic

class BoardView():
    @classmethod
    def show_board(cls,request, id):
        board=Board.objects.get(pk=id)
        topics=Topic.objects.filter(board=id)
        return render_to_response("topic_list.html", {'board':board, 'topics': topics },context_instance=RequestContext(request))
        #raise NotImplemented
    
    @classmethod
    def show_topic(cls,request, id):
        messages=Message.objects.filter(topic=id)
        topic=Topic.objects.get(pk=id).title
        #topic=topic.title
        return render_to_response("topic_detail.html", {'messages':messages, 'topic':topic},context_instance=RequestContext(request))
        #raise NotImplemented
    
    @classmethod
    def show_message(cls,request, id):
        message=Message.objects.get(pk=id)
        return render_to_response("message_detail.html", {'message':message},context_instance=RequestContext(request))

    @classmethod
    def show_available_board(cls,request):
        forums = Board.objects.all()
        return render_to_response("board_list.html",{'boards': forums},context_instance=RequestContext(request))
        #raise NotImplemented
    
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
        board=Board.objects.get(name="news")
        id=board.pk
        topics=Topic.objects.filter(board=id)
        return render_to_response("board_detail.html", {'board':board, 'topics': topics },context_instance=RequestContext(request))