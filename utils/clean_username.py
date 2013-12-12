from django.contrib.auth.models import User


def get_clean_username(first_name, last_name, random_number=False):
    if random_number:
        ran_num = User.objects.make_random_password(length=10, allowed_chars='123456789')
        username = first_name+last_name+ran_num
    else:
        username = first_name+last_name

    try:
        user = User.objects.get(username=username)
        if user:
            return get_clean_username(first_name, last_name, random_number=True)
    except User.DoesNotExist:
        return username