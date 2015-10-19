#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import with_statement
import Skype4Py
import re
import ConfigParser
import time
import json
import os


CONFIG_FILE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/conf/setting.conf'
conf = ConfigParser.SafeConfigParser()
conf.read(CONFIG_FILE)
chat_room = conf.get('chat_data', 'chat_room')
start_hour = int(conf.get('chat_data', 'start_hour'))
start_minute = int(conf.get('chat_data', 'start_minute'))
absent_fine = int(conf.get('chat_data', 'absent_fine'))
status_json = os.path.abspath(os.pardir + '/date/status_json')


class TardyCounter(object):

    def __init__(self):
        self.skype = Skype4Py.Skype()
        self.skype.Attach()
        self.skype.OnMessageStatus = self.status_handler

    def status_handler(self, msg, event):
        import datetime
        d = datetime.datetime.now()
        delay_time = (msg.Datetime - datetime.datetime(d.year, d.month, d.day, start_hour, start_minute, 0, 0))
        delay_days = delay_time.days
        print msg.Datetime
        print delay_time
        print delay_time.seconds / 60
        if msg.ChatName == chat_room and delay_days >= 0:
            params = re.split(r"\s+", msg.Body)
            command = params.pop(0)
            if command == "@come" and (event == 'RECEIVED' or event == 'SENDING'):
                name = msg.FromDisplayName
                delay_minutes = delay_time.seconds / 60
                fine = None
                msg_body = self.add_fine(name, fine, delay_minutes)
                print msg_body
                msg.Chat.SendMessage(msg_body)

            elif (command == "@plus") and (event == 'SENDING'):
                if len(params) == 2 and msg_body[1].isdigit():
                    name = params[0]
                    fine = int(params[1])
                    delay_minutes = None
                    msg_body = self.add_fine(name, fine, delay_minutes)
                    print msg_body
                    msg.Chat.SendMessage(msg_body)

            elif (command == "@minus") and (event == 'SENDING'):
                if len(params) == 2 and params[1].isdigit():
                    name = params[0]
                    fine = -1 * int(params[1])
                    delay_minutes = None
                    msg_body = self.add_fine(name, fine, delay_minutes)
                    print msg_body
                    msg.Chat.SendMessage(msg_body)

            elif (command == "@absent") and (event == 'SENDING'):
                if len(params) == 1:
                    name = params[0]
                    fine = absent_fine
                    delay_minutes = None
                    msg_body = self.add_fine(name, fine, delay_minutes)
                    print msg_body
                    msg.Chat.SendMessage(msg_body)

            else:
                pass

    def add_fine(self, name, fine, delay_minutes):
        status_list = self.get_status_list()
        for status in status_list:
            if re.search(status['name'], name):
                if delay_minutes is None:
                    status['fine'] += fine
                else:
                    status['fine'] += delay_minutes * status['age_group']
                    fine = delay_minutes * status['age_group']
        msg_body = self.make_message(name, fine, status_list)
        self.set_status(status_list)
        return msg_body

    def make_message(self, name, fine, status_list):
        msg_body = name + "\n"
        if fine > 0:
            msg_body = msg_body + "+" + str(fine)
        else:
            msg_body = msg_body + str(fine)
        msg_body = msg_body + "\n===============\n"
        for status in status_list:
            msg_body = msg_body + status['name'] + ' : ' + str(status['fine']) + '\n'
        return msg_body

    def get_status_list(self):
        print "get"
        with open("status.json") as f:
            status_list = json.load(f)
        print status_list
        return status_list

    def set_status(self, status_list):
        print "set"
        print status_list
        with open('status.json', 'w') as f:
            status_str = json.dumps(status_list)
            f.writelines(status_str)

    def run(self):
        num = 0
        while num < 60 * 60 * 2.5:
            time.sleep(1)
            num += 1


def main():
    bot = TardyCounter()
    bot.run()


if __name__ == "__main__":
    main()
