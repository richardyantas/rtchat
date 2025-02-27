# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ChatMessageCreateForm
from django.views.decorators.csrf import csrf_protect
from app.logger import logger

# Create your views here.


@csrf_protect
@login_required
def chat_view(request):
    logger.info("chat_view called ... ")
    chat_group = get_object_or_404(ChatGroup, group_name="public-chat")
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatMessageCreateForm()

    # if request.method == 'POST':
    if request.htmx:
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {"message": message, "user": request.user}
            # print("entroooooooooo")
            # return redirect('home')
            return render(request, "chat/partials/chat_message_p.html", context)

    return render(
        request, "chat/chat.html", {"chat_messages": chat_messages, "form": form}
    )
