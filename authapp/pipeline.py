import os
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile

from geekshop import settings


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = f"https://api.vk.com/method/user.get?fields=bdate,sex,about,photo_max&access_token={response['access_token']}&v=5.92"

    # api_url = urlunparse(('https',
    #                       'api.vk.com',
    #                       '/method/user.get',
    #                       None,
    #                       urlencode(OrderedDict(fields=','.join('bdate', 'sex', 'about')), access_token=response['access_token'], v='5.92')),
    #                       None
    #                       ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]

    if data['sex']:
        if data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE

    if data['photo_max'] and not user.avatar:
        photo = data['photo_max']
        image_name = photo.split("/")[-1].split("?")[0]
        pars = requests.get(photo)
        with open(os.path.join(settings.BASE_DIR, f'media/users_avatars/{image_name}'), "wb") as f:
            f.write(pars.content)

        user.avatar = f'users_avatars/{image_name}'

    if data['about']:
        user.shopuserprofile.aboutMe = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = datetime.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    user.save()
