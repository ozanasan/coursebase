from django.shortcuts import render
from django.http import HttpResponse
from coursebase.models import Topic
from coursebase.models import Lesson
from django.contrib.auth.decorators import login_required
from coursebase.forms import TopicForm, LessonForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout

def topics(request):
    topic_list = Topic.objects.values()
    context_dict = {'topics': topic_list}
    return render(request, 'coursebase/topics.html', context_dict)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect('/coursebase/')
        else:
            return render(request, 'coursebase/invalid.html')
    elif request.method == 'GET':
        return render(request, 'coursebase/login.html', {})

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
            'coursebase/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def index(request):
    topic_list = Topic.objects.values()
    popular_topics = [topic for topic in topic_list if topic['likecount'] > 5]
    context_dict = {'topics': popular_topics}
    return render(request, 'coursebase/index.html', context_dict)

def about(request):
    return render(request, 'coursebase/about.html')

def topic(request, topic_name_slug):
    context_dict = {}

    if 'like' in request.POST:
        topic = Topic.objects.get(slug=topic_name_slug)
        topic.likecount = topic.likecount + 1
        topic.save()

    try:
        topic = Topic.objects.get(slug=topic_name_slug)
        context_dict['topic_name'] = topic.name
        context_dict['topic_name_slug'] = topic_name_slug
        lessons = Lesson.objects.filter(topic=topic)
        context_dict['lessons'] = lessons
        context_dict['topic'] = topic
        context_dict['likecount'] = topic.likecount
    except Topic.DoesNotExist:
        pass
    return render(request, 'coursebase/topic.html', context_dict)

def add_topic(request):
    if request.method == 'POST':
        form  =  TopicForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = TopicForm()
    return render(request, 'coursebase/add_topic.html', {'form':form})

def add_lesson(request, topic_name_slug):
    print "%s" % topic_name_slug
    try:
        cat = Topic.objects.get(slug=topic_name_slug)
    except Topic.DoesNotExist:
        print "Topic does not exists"
        cat = None

    if request.method == 'POST':
        print "Debug Ozan: add_lesson POST"
        form = LessonForm(request.POST)
        if form.is_valid():
            print "Debug Ozan: valid"
            if cat:
                print "Debug Ozan: inside cat. And cat is %s" % cat
                lesson = form.save(commit=False)
                lesson.topic = cat
                lesson.views = 0
                lesson.save()
                return topic(request, topic_name_slug)
        else: 
            print "Debug Ozan: error"
            print form.errors
    else:
        print "Debug Ozan: add_lesson GET"
        print "Debug %s" % topic_name_slug
        form = LessonForm()
    
    context_dict = {'form': form, 'topic': cat, 'topic_name_slug': topic_name_slug}
    return render(request, 'coursebase/add_lesson.html', context_dict)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/coursebase/')




