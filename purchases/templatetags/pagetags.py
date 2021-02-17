from django import template

from purchases import models as purchases_models
from comments import models as comment_models
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
def check_class(pk):
    try:
        m = purchases_models.Material.objects.get(pk=pk)
        return True 
    except:
        m = purchases_models.Immaterial.objects.get(pk=pk)
        return False

@register.simple_tag
def sort_comment(comment):
    comment = comment.order_by('-created')

    return comment
