from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required

#from django.views.decorators.csrf import csrf_exempt

from board.forms import TopicForm, MessageForm, BoardForm
from board.models import Board, Message, Topic

class BoardView():
    @classmethod
    def show_board(cls,request, id):
        board = Board.objects.get(pk=id)
        topics = Topic.objects.filter(board__pk=id)
        return render_to_response("topic_list.html", 
                                  {'board':board, 'topics': topics },
                                  context_instance=RequestContext(request))
    
    @classmethod
    def show_topic(cls,request, id):
        messages = Message.objects.filter(topic__pk=id)
        topic_item = Topic.objects.get(pk=id)
        topic = topic_item.title
        topic_id = topic_item.pk
        return render_to_response("topic_detail.html", 
                                  {'messages':messages, 'topic': topic, 'topic_id': topic_id},
                                  context_instance=RequestContext(request))

    
    @classmethod
    def show_message(cls,request, id):
        message = Message.objects.get(pk=id)
        return render_to_response("message_detail.html", 
                                  {'message':message},
                                  context_instance=RequestContext(request))

    @classmethod
    def show_available_board(cls,request):
        forums = Board.objects.all()
        return render_to_response("board_list.html",
                                  {'boards': forums},
                                  context_instance=RequestContext(request))

    

    @classmethod
    #@login_required
    def create_topic(cls,request,id):
        if request.method == 'POST':
            topic_form = TopicForm(request.POST)
            title = request.POST['title']
            board = Board.objects.get(pk=id)
            date = datetime.now()
            #created_by=request.user
            new_topic = Topic(title=title, board=board, date=date, is_active=True)
            #new_topic=Topic(title=title, board=board, created_by=created_by, date=date, is_active=True)            
            new_topic.save()
            
            return HttpResponseRedirect("/forum/board/topic/"+str(new_topic.pk))
        else:
            topic_form = TopicForm()
        return render_to_response('new_topic.html', 
                                  {'topic_form': topic_form}, 
                                  context_instance=RequestContext(request))
   
    @classmethod
    #@login_required
    def create_board(cls,request):
        if request.method == 'POST':
            board_form = BoardForm(request.POST)
            new_board = board_form.save()
            url = "/forum/board/"+str(new_board.pk)
            return HttpResponseRedirect("/forum/board/" + str(new_board.pk))
        else:
            board_form = BoardForm()
        return render_to_response('new_board.html', 
                                  {'board_form': board_form}, 
                                  context_instance=RequestContext(request)) 
  
    @classmethod
    #@login_required
    def submit_message(cls,request, id):
        if request.method=='POST':
            message_form = MessageForm(request.POST)
            
            content = request.POST['content']
            submitted_by = request.user
            topic = Topic.objects.get(pk=id)
            submission_date = datetime.now()
            new_message = Message(topic=topic, submission_date=submission_date, content=content)
            #new_message=Message(topic=topic, submitted_by=submitted_by, submission_date=submission_date, content=content)
            new_message.save()

            return HttpResponseRedirect("/forum/board/topic/"+str(id))
        else:
            message_form = MessageForm()
        return render_to_response('new_message.html', 
                                  {'message_form': message_form}, 
                                  context_instance=RequestContext(request))
        #raise NotImplemented
    
    @classmethod
    def show_news_board(cls,request):
        board = Board.objects.get(name="news")
        id = board.pk
        topics = Topic.objects.filter(board=id)
        return render_to_response("board_detail.html", 
                                  {'board':board, 'topics': topics },
                                  context_instance=RequestContext(request))