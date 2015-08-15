# -*- coding: utf-8 -*-
"""
Модуль, реализующий стандартные API запросы VK
"""
import urllib2
import json
from urllib import urlencode

def call_api(method, params, token):
    """
    Функция создания url-запроса

    :method: реализуемый из API VK метод
    :params: параметры, передающиеся с методом
    :token: токен
    :return: возвращается ответ сервера на запрос
    """
    params.append(('access_token', token))
    url = 'https://api.vk.com/method/%s?%s' % (method, urlencode(params))
    return json.loads(urllib2.urlopen(url).read())['response']

def wall_post(owner_id, message, token):
    """
    Функция отправки сообщения на стену пользователю

    :owner_id: ID стены
    :message: сообщение
    :token: токен
    :return: возвращается ответ сервера на запрос
    """
    return call_api("wall.post", [('owner_id', owner_id), ('message', message)], token)

def friends_add(user_id, text, token):
    """
    Функция добавления в друзья по ID пользователя

    :user_id: ID пользователя
    :text: текст сообщения, отправляемого с заявкой
    :token: токен
    :return: возвращается ответ сервера на запрос
    """
    return call_api('friends.add', [('user_id', user_id), ('text', text)], token)

def messages_send(user_id, message, token):
    """
    Функция отправки сообщения

    :user_id: ID пользователя
    :message: текст сообщения
    :token: токен
    :return: возвращается ответ сервера на запрос
    """
    return call_api('messages.send', [('user_id', user_id), ('message', message)], token)

def messages_get(out, count, time_offset, token):
    """
    Функция чтения отправленных/полученных сообщений

    :out: если параметр равен 1, сервер вернёт отправленные сообщения
    :count: кол-во сообщений, которое необходимо получить, defaul 20, max 200
    :time_offset: max время, прошедшее с момента отправки сообещения до текущего момента в секундах. 
                  0, если хотим получить все сообщения
    :token: токен
    :return: возвращается список объектов сообщений
    """
    return call_api('messages.get', [('out', out), ('count', count), ('time_offset', time_offset)], token)

if __name__ == '__main__':
    pass
else:
    print 'methods - модуль, содержащий функции для работы ANNA'
    print 'SEA, august, 2015'