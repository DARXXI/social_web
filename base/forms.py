from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

# была убогая форма и чтобы самому не мараться мы подключаем модуль джанги        