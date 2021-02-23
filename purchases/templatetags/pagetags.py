from django import template
from purchases import models as purchases_models
from comments import models as comment_models
from alarms import models as alarm_models
from users import models as user_models
import datetime
from pytz import timezone

register = template.Library()


@register.simple_tag
def page_range(current, last):
    begin = current
    end = current
    for i in range(0, 9):
        if i % 2 == 0:
            if begin > 1:
                begin -= 1
            else:
                if end < last:
                    end += 1
        else:
            if end < last:
                end += 1
            else:
                if begin > 1:
                    begin -= 1

    return range(begin, end + 1)


@register.simple_tag
def slide_range(photos):
    return range(1, photos.count() + 1)


@register.simple_tag
def check_pk(pk):
    try:
        m = purchases_models.Material.objects.get(pk=pk)
        print(m)
        return m
    except:
        m = purchases_models.Immaterial.objects.get(pk=pk)
        print(m)
        return m


@register.simple_tag
def test(field):
    sm_list = ("closed", "category", "max_people", "price", "total", "unit")
    if field.name in sm_list:
        return "w-1/3"
    else:
        return "w-full"


@register.simple_tag
def check_class(pk):
    try:
        m = purchases_models.Material.objects.get(pk=pk)
        return True
    except:
        m = purchases_models.Immaterial.objects.get(pk=pk)
        return False


@register.simple_tag
def sort_comment(comment):
    comment = comment.order_by("-created")

    return comment


@register.simple_tag
def related_alarm(pk, userpk):
    alarm = alarm_models.Alarm.objects.get(pk=pk)
    sender = alarm.sender
    receiver = alarm.receiver

    related_alarm1 = alarm_models.Alarm.objects.filter(sender=sender, receiver=receiver)
    related_alarm2 = alarm_models.Alarm.objects.filter(sender=receiver, receiver=sender)

    related_alarm = (related_alarm1 | related_alarm2).order_by("-created")

    for r in related_alarm.all():
        if r.receiver.pk == userpk:
            r.ischeck = True
            r.save()

    return related_alarm


@register.simple_tag
def return_alarm(pk):
    alarm = alarm_models.Alarm.objects.get(pk=pk)

    return alarm


@register.simple_tag
def isSelfMessage(pk):
    alarm = alarm_models.Alarm.objects.get(pk=pk)

    if alarm.sender.pk == alarm.receiver.pk:
        return True
    else:
        return False


@register.simple_tag
def user_alarm_count(pk):
    user = user_models.User.objects.get(pk=pk)
    count = 0
    for alarm in user.alarm_receiver.all():
        if alarm.ischeck == False:
            count = count + 1

    return count


@register.simple_tag
def new_message_check(pk, userpk):
    alarm = alarm_models.Alarm.objects.get(pk=pk)
    sender = alarm.sender
    receiver = alarm.receiver

    related_alarm1 = alarm_models.Alarm.objects.filter(sender=sender, receiver=receiver)
    related_alarm2 = alarm_models.Alarm.objects.filter(sender=receiver, receiver=sender)

    related_alarm = (related_alarm1 | related_alarm2).order_by("-created")

    for r in related_alarm.all():
        if r.receiver.pk == userpk:
            if r.ischeck == False:
                return True

    return False


@register.simple_tag
def is_expired(purchase):
    now = datetime.datetime.now(timezone("Asia/Seoul"))
    closed = purchase.closed.replace(tzinfo=timezone("Asia/Seoul"))
    if now > closed:
        purchase.status = purchases_models.Purchase.status_expired
        purchase.save()
        return True

    return False
