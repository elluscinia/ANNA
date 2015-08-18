# -*- coding: utf-8 -*-

import auth
import methods
import json
import frases
import random
import getpass

def main(user_id, token):
    connection_LongPollServer = methods.messages_getLongPollServer('0', '0', token)['response']
    ts = connection_LongPollServer.get('ts')
    key = connection_LongPollServer.get('key')
    server = connection_LongPollServer.get('server')
    response_LongPollServer = methods.call_LongPollServer(server, key, ts, '25', '32')

    while True:
        if 'failed' not in response_LongPollServer:
            pts = response_LongPollServer.get('pts')
            ts = response_LongPollServer.get('ts')
            updates = response_LongPollServer.get('updates')

            # обработка updates от сервера
            # TODO: вынести в отдельную функцию
            if response_LongPollServer.get('updates') != []:
                for i in xrange(0, len(response_LongPollServer.get('updates'))):
                    print 'UPDATES:', updates

                    if response_LongPollServer.get('updates')[i][0] == 4 and response_LongPollServer.get('updates')[i][2] == 49:
                        # ANNA воспринимает только текстовые сообщения
                        message = response_LongPollServer.get('updates')[i][6].encode('utf-8')

                        print '=================='
                        print message

                        if 'Hi' in message or 'hi' in message or 'Привет' in message or 'привет' in message:
                            response = methods.messages_send(response_LongPollServer.get('updates')[i][3], random.choice(frases.HelloFrase), token)
                        elif 'How are you' in message or 'how are you' in message or 'Как ты?' in message or 'как ты?' in message or 'Как дела' in message or 'как дела' in message:
                            response = methods.messages_send(response_LongPollServer.get('updates')[i][3], random.choice(frases.HowAreYouFrases), token)
                        elif 'Why' in message or 'why' in message or 'Почему' in message or 'почему' in message:
                            response = methods.messages_send(response_LongPollServer.get('updates')[i][3], random.choice(frases.WhyFrases), token)
                        else:
                            response = methods.messages_sendSticker(response_LongPollServer.get('updates')[i][3], response_LongPollServer.get('updates')[i][3], '0', str(random.choice(frases.StickersCatPeach)), token)

                        if 'response' in response:
                            print 'SERVER RESPONSE:', response.get('response')
                        elif 'error' in response:
                            print 'SERVER ERROR:'
                            print 'error code:', response.get('error').get('error_code')
                            print 'error message:', response.get('error').get('error_msg')
                            methods.messages_markAsRead(response_LongPollServer.get('updates')[i][1], response_LongPollServer.get('updates')[i][3], token)
                        else:
                            print response

                        print '=================='

                    else:
                        pass

            response_LongPollServer = methods.call_LongPollServer(server, key, ts, '25', '32')
        elif 'ts' in response_LongPollServer:
            ts = response_LongPollServer.get('ts')
        else:
            connection_LongPollServer = methods.messages_getLongPollServer('0', '0', token)['response']
            ts = connection_LongPollServer.get('ts')
            key = connection_LongPollServer.get('key')
            server = connection_LongPollServer.get('server')
            response_LongPollServer = methods.call_LongPollServer(server, key, ts, '25', '32')


if __name__ == '__main__':
    email = raw_input('Email: ')
    password = getpass.getpass()
    client_id = '4633060' # ID приложения

    token, user_id = auth.auth(email, password, client_id, ['notify', 'friends', 'photos', 'audio', 'docs', 'wall', 'groups', 'messages', 'notifications', 'offline'])

    print 'user ID: ', user_id
    print 'token: ', token

    main(user_id, token)
else:
    print 'ANNA'
    print 'august, 2015'
    print '(c) SEA'
    print 'personal VK bot'