from datetime import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#from django.views.decorators.csrf import csrf_exempt

from board.forms import TopicForm, MessageForm, BoardForm
from board.models import Board, Message, Topic
from core.models import ShopUser

class BoardView():
    @classmethod
    def show_board(cls, request, board_id):
        # DZIALA
        board = Board.objects.get(pk=board_id)
        topics_list = Topic.objects.filter(board__pk=board_id)
        
        paginator = Paginator(topics_list, 10)
        page = request.GET.get('page')

        try:
            topics = paginator.page(page)
        except PageNotAnInteger:
            topics = paginator.page(1)
        except EmptyPage:
            topics = paginator.page(paginator.num_pages)
        return render_to_response("topic_list.html", 
                                  {'board':board, 'topics': topics },
                                  context_instance=RequestContext(request))
    @classmethod
    def delete_board(cls, request, board_id):
        board = Board.objects.get(pk=board_id)
        board.delete()
        return HttpResponseRedirect("/forum/")
    
    @classmethod
    def show_topic(cls, request, board_id, topic_id):
        # DZIALA
        messages_list = Message.objects.filter(topic__pk=topic_id)
        topic = Topic.objects.get(pk=topic_id)
        #topic = topic_item.title
        topic_id = topic.pk
        board=Board.objects.get(pk=board_id)
        
        paginator = Paginator(messages_list, 10)
        page = request.GET.get('page')

        try:
            messages = paginator.page(page)
        except PageNotAnInteger:
            messages = paginator.page(1)
        except EmptyPage:
            messages = paginator.page(paginator.num_pages)
        
        return render_to_response("topic_detail.html", 
                                  {'messages':messages, 'topic': topic, 'topic_id': topic_id, 'board': board},
                                  context_instance=RequestContext(request))

    @classmethod
    def delete_topic(cls, request, topic_id, board_id):
        topic = Topic.objects.get(pk=topic_id)
        topic.delete()
        return HttpResponseRedirect("/forum/%s/" % (board_id))
    
    @classmethod
    def show_message(cls, request, board_id, topic_id, message_id):
        # DZIALA
        message = Message.objects.get(pk=message_id)
        topic = Topic.objects.get(pk=topic_id)
        board=Board.objects.get(pk=board_id)
        return render_to_response("message_detail.html", 
                                  {'message':message, 'topic': topic, 'board': board},
                                  context_instance=RequestContext(request))
    @classmethod
    def delete_message(cls, request, topic_id, board_id, message_id):
        message=Message.objects.get(pk=message_id)
        message.delete() 
        messages = Message.objects.filter(topic__pk=topic_id)
        return HttpResponseRedirect("/forum/%s/%s/" % (board_id, topic_id))
        if messages.count()==0:
            topic = Topic.objects.get(pk=topic_id)
            topic.delete()
            return HttpResponseRedirect("/forum/%s/" % (board_id))

    @classmethod
    def show_available_board(cls,request):
        # DZIALA
        if request.user.is_staff:
            forums = Board.objects.all()
            return render_to_response("board_list.html",
                                  {'boards': forums},
                                  context_instance=RequestContext(request))
        else:
            forums = Board.objects.exclude(name='news').exclude(name='EShopItem').exclude(name='AuctionItem').exclude(name='GroupOffer')
            return render_to_response("board_list.html",
                                  {'boards': forums},
                                  context_instance=RequestContext(request))
  
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def create_topic(cls, request, board_id):
        # DZIALA
        if request.method == 'POST':
            topic_form = TopicForm(request.POST)
            if topic_form.is_valid():
                title = request.POST['title']
                board = Board.objects.get(pk=board_id)
                date = datetime.now()
                created_by = ShopUser.objects.get(user__pk=request.user.pk)
                #created_by=request.user
                new_topic = Topic(title=title, board=board, created_by=created_by, date=date, is_active=True)
                #new_topic=Topic(title=title, board=board, created_by=created_by, date=date, is_active=True)            
                new_topic.save()
                return HttpResponseRedirect("/forum/%s/%s/" % (board_id, new_topic.pk))
        
        else:
            topic_form = TopicForm()
            board=Board.objects.get(pk=board_id)
        return render_to_response('new_topic.html', 
                                  {'topic_form': topic_form, 'board': board}, 
                                  context_instance=RequestContext(request))
   
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))
    def create_board(cls, request):
        # DZIALA
        if request.method == 'POST':
            board_form = BoardForm(request.POST)
            if board_form.is_valid():
                new_board = board_form.save()
                return HttpResponseRedirect("/forum/" + str(new_board.pk))
        else:
            board_form = BoardForm()
        return render_to_response('new_board.html', 
                                  {'board_form': board_form}, 
                                  context_instance=RequestContext(request)) 
        
    
    @classmethod
    @method_decorator(login_required(login_url='/accounts/login/'))  
    def submit_message(cls, request, board_id, topic_id):
        # DZIALA
        if request.method=='POST':
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                content = request.POST['content']
                submitted_by = request.user
                topic = Topic.objects.get(pk=topic_id)
                submission_date = datetime.now()
                submitted_by=ShopUser.objects.get(user__pk=request.user.pk)
                new_message = Message(topic=topic, submitted_by=submitted_by, submission_date=submission_date, content=content)
                #new_message=Message(topic=topic, submitted_by=submitted_by, submission_date=submission_date, content=content)
                new_message.save()

                return HttpResponseRedirect("/forum/%s/%s/" % (board_id, topic_id))
        else:
            message_form = MessageForm()
            topic = Topic.objects.get(pk=topic_id)
            board=Board.objects.get(pk=board_id)
        return render_to_response('new_message.html', 
                                  {'message_form': message_form, 'board': board, 'topic': topic}, 
                                  context_instance=RequestContext(request))
        #raise NotImplemented
    
    @classmethod
    def show_news_board(cls, request):
        # DZIALA
        board = Board.objects.get(name="news")
        id = board.pk
        topics = Topic.objects.filter(board=id)
        return render_to_response("board_detail.html", 
                                  {'board':board, 'topics': topics },
                                  context_instance=RequestContext(request))