# ./manage.py shell < dataentry.py

# docker-compose stop
# docker-compose up
# in other terminal
# export DJANGO_SUPERUSER_EMAIL=root@email.com
# export DJANGO_SUPERUSER_PASSWORD=testpass1234
# docker-compose exec web python manage.py createsuperuser --no-input
# docker-compose exec web python manage.py shell < dataentry.py

from django.contrib.auth.models import User
from django.test.client import Client
from django.urls import reverse
from django.templatetags.static import static
from chat.models import * # installed apps
from users.models import *
robert=User.objects.create_user('robert', email="robert@email.com", password='bareco3t@wer')
camilo=User.objects.create_user('camilo', email="camilo@email.com", password='bareco3t@wer')
pc=ChatGroup(group_name="public-chat" )
pc.save()
g1=GroupMessage(group=pc, author=robert, body="hello there?")
g1.save()
g2=GroupMessage(group=pc, author=camilo, body="whatsapp bro ..")
g2.save()
p1=Profile.objects.get(pk=2)
p1.image="avatars/ape1.jpg" # Documents/django-composer/app/static/images/ape1.jpg
p1.displayname="roboto"
p2=Profile.objects.get(pk=3)
p2.image="avatars/ape2.jpg" # Documents/django-composer/app/static/images/ape2.jpg
p2.displayname="dino"
p1.save()
p2.save()

# Profile.objects.all()[1]
# Profile.objects.all()[2]


# Profile(user=robert, image=static("images/ape1.jpg"), displayname="ROBOTO").save()
# Profile(user=camilo, image=static("images/ape2.jpg"), displayname="DINO ").save()

# client = Client()
# client.login(username="john", password="Multicuerpo5@")
# for u in User.objects.all():
#     print(u)

# for p in Profile.objects.all():
#     print(p)
