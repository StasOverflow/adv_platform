from users.models import AdvSiteUser


def create_user(username, password):
    try:
        user = AdvSiteUser.objects.get(username=username)
    except Exception as e:
        user = AdvSiteUser.objects.create_user(username=username, email="user1@test.com", )
        user.set_password(password)
        user.save()
    return user
