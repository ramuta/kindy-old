from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from userena.models import UserenaSignup
from utils.emails import send_invite_email


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


def invite_new_kindy_user(email, first_name, last_name, inviter, childcare, role):
    password = User.objects.make_random_password()
    username = get_clean_username(first_name, last_name)

    userena_user = UserenaSignup.objects.create_user(email=email,
                                                     password=password,
                                                     username=username,
                                                     active=True,
                                                     send_email=False)
    userena_user.save()
    user = get_object_or_404(User, email=email)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    # set role and permissions
    if role == 'Parent':
        group = Group.objects.get(name='Childcare %s: Parent' % childcare.pk)
        user.groups.add(group)
        childcare.parents.add(user)
    elif role == 'Employee':
        group = Group.objects.get(name='Childcare %s: Employee' % childcare.pk)
        user.groups.add(group)
        childcare.employees.add(user)
    elif role == 'Manager':
        group = Group.objects.get(name='Childcare %s: Manager' % childcare.pk)
        user.groups.add(group)
        childcare.managers.add(user)

    # email
    send_invite_email(inviter=inviter, invitee=user, childcare=childcare, password=password)


def add_current_user(user, role, childcare):
    if role == 'Parent':
        group = Group.objects.get(name='Childcare %s: Parent' % childcare.pk)
        user.groups.add(group)
        childcare.parents.add(user)
    elif role == 'Employee':
        group = Group.objects.get(name='Childcare %s: Employee' % childcare.pk)
        user.groups.add(group)
        childcare.employees.add(user)
    elif role == 'Manager':
        group = Group.objects.get(name='Childcare %s: Manager' % childcare.pk)
        user.groups.add(group)
        childcare.managers.add(user)