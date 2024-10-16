#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import sys

SECTION_COMMON = 'common'
SECTIONS = [SECTION_COMMON]

class Config:

    def __init__(self, config_path=None):
        self.host = '127.0.0.1'
        self.port = 22
        self.username = 'root'
        self.password = '123456'
        self.refresh = True

        if config_path:
            self.__update(config_path)

    def update(self, host=None, port=None, username=None, password=None, refresh=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.refresh = refresh

    @property
    def parser(self):
        parser = configparser.ConfigParser()
        variables = vars(self)
        for section in SECTIONS:
            parser[section] = {}
        for k, v in variables.items():
            if k.startswith('cm'):
                pass
            else:
                parser[SECTION_COMMON].update({k: str(v)})
        return parser

    def save_to(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            self.parser.write(f)

    def __update(self, path):
        variables = vars(self)
        parser = configparser.ConfigParser()
        parser.read(path, 'utf-8')
        for section in parser.sections():
            if section in SECTIONS:
                pass
            else:
                # 不要parse 无关的section
                break
            for option in parser.options(section):
                value = parser.get(section, option)
                key = option
                if not self.check_key_valid(key):
                    break
                original_value = variables.get(key)
                type_expr = None
                if original_value:
                    type_of_original_value = type(original_value)
                    if type_of_original_value == str:
                        type_expr = 'str'
                if type_expr:
                    expr = "self.{} = '{}'".format(key, value)
                else:
                    expr = 'self.{} = {}'.format(key, value)
                # print(expr)
                exec(expr)

    def check_key_valid(self, key):
        variables = vars(self)
        for k, _ in variables.items():
            if k == key:
                return True
        return False

    def __str__(self) -> str:
        variables = vars(self)
        info = ''
        for k, v in variables.items():
            temp_str = f"{k} = {v}\n"
            type_of_v = type(v)
            if type_of_v == str:
                temp_str = f"{k} = '{v}'\n"
            info += temp_str
        return info[:-1]

if __name__ == '__main__':
    path = None
    if len(sys.argv) > 1:
        path = sys.argv[1]
    print('config path:', path)
    test_config = Config(path)
    print(test_config)