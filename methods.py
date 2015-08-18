# -*- coding: utf-8 -*-
"""
Модуль, реализующий стандартные API запросы VK
"""

import urllib2
import json
from urllib import urlencode
import httplib

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

    # тут вылезают ошибки из библиотеки. возможно, надо переписать способ обращения к серверу
    try:
        response = urllib2.urlopen(url, timeout = 30).read()
        return json.loads(response)
    except (IOError, httplib.HTTPException):
        response = urllib2.urlopen(url, timeout = 30).read()
        return json.loads(response)

    #return json.loads(urllib2.urlopen(url).read())

def call_LongPollServer(server, key, ts, wait, mode):
    """
    Функция, обеспечивающая работу с Long Poll Server

    :server: адрес сервера, к которому нужно отправлять запрос
    :key: секретный ключ сессии
    :ts: номер последнего события, начиная с которого нужно получать данные
    :wait: время удержания запроса, если не произошло собвтий
    :mode: параметр, определяющий наличие поля прикреплений в получаемых данных с помощью битовой маски
    """
    url = 'http://%s?act=a_check&key=%s&ts=%s&wait=%s&mode=%s' % (server, key, ts, wait, mode)
    return json.loads(urllib2.urlopen(url).read())

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

def messages_markAsRead(message_ids, peer_id, token):
    """
    Функция, помечающая сообщение как прочитанное

    :message_ids: идентификаторы сообщений (спсиок положительных чисел, разделённых запятыми)
    :peer_id: идлентификатор чата или пользователя (в случае диалога)
    :token: токен
    :return: в случае успеха возвращает 1
    """
    return call_api('messages.markAsRead', [('message_ids', message_ids), ('peer_id', peer_id)], token)

def messages_sendSticker(user_id, chat_id, guid, sticker_id, token):
    """
    Функция отправки стикера

    :user_id: идентификатор пользователя
    :chat_id: идентификатор беседы
    :guid: уникальный идентификатор, предназначенный для предотвращения повторной отправки одинакового сообщения
    :sticker_id: идентификатор стикера
    :token: токен
    :return: после успешного выполнения возвращает идентификатор отправленного сообщения
    """
    return call_api('messages.sendSticker', [('user_id', user_id), ('chat_id', chat_id), ('guid', guid), ('sticker_id', sticker_id)], token)

def messages_getLongPollServer(use_ssl, need_pts, token):
    """
    Функция подключения к Long Poll Server.
    Long Poll Server позволяет моментально узнать о приходе новых сообщений и других событиях.

    :use_ssl: 1 - использовать SSL. Флаг принимает значения 1 или 0
    :need_pts: 1 - возвращаеть поле pts, необходимое для работы метода messages.getLongPollHistory 
    :token: токен
    :return: Возвращает объект, который содержит поля key, server, ts. 
    """
    return call_api('messages.getLongPollServer', [('use_ssl', use_ssl), ('need_pts', need_pts)], token)

if __name__ == '__main__':
    pass
else:
    print 'methods - модуль, содержащий функции для работы ANNA'