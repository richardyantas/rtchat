from django.contrib.auth.models import User
from chat.models import *
from users.models import *

u1 = User.objects.create_user(
    "robert", email="robert@email.com", password="bareco3t@wer"
)
u2 = User.objects.create_user(
    "camilo", email="camilo@email.com", password="bareco3t@wer"
)

pc = ChatGroup(group_name="public-chat")
pc.save()

g1 = GroupMessage(group=pc, author=u1, body="hello there?")
g1.save()

g2 = GroupMessage(group=pc, author=u2, body="whatsapp bro ..")
g2.save()
p1 = Profile.objects.get(pk=2)
p1.image = "avatars/ape1.jpg"
p1.displayname = "roboto"

p2 = Profile.objects.get(pk=3)
p2.image = "avatars/ape2.jpg"
p2.displayname = "dino"

p1.save()
p2.save()
