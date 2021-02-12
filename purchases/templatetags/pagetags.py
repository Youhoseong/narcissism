from django import template

register = template.Library()


@register.simple_tag
def page_range(current, last):
    print("current")
    print(last)
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
