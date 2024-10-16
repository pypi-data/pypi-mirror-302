#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from os import path
import re
import paramiko
import iup
from iup.config import Config
import ipaddress


HOSTNAME_PATTERN = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
CMD_TEMPLATE = 'iup {}'
CMD_DNSMASQ = '/etc/init.d/dnsmasq restart'
CMD_CHNDNS = '/etc/init.d/chinadns-ng restart'
MAGIC_STR = "update rule to"
MAGIC_STR2 = "update blk"

def is_domain_name(string: str):
    if re.match(HOSTNAME_PATTERN, string):
        return True
    else:
        return False

def is_ip_address(ip_str: str):
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip is not None
    except ValueError:
        return False

def parse_host_name(hostname_str: str):
    if is_domain_name(hostname_str) or is_ip_address(hostname_str):
        return hostname_str
    return None

def parse_port(port: str):
    if port.isdigit():
        port_num = int(port)
        if port_num > 1 and port_num < 65535:
            return port
    return None


def parse_yes_or_no(msg: str):
    msg = msg.upper()
    if msg in ['Y', 'YES', 'T', 'TRUE']:
        return True
    if msg in ['N', 'NO', 'F', 'FALSE']:
        return False
    return None


def read_hostname_from_file(path: str):
    hostnames = []
    with open(path, 'r') as f:
        for line in f:
            host_name_str = line.strip()
            if is_domain_name(host_name_str):
                hostnames.append(host_name_str)
    hostnames = list(dict.fromkeys(hostnames))
    return hostnames

def load_and_overlay_config() -> Config:
    parser = argparse.ArgumentParser(description='参数说明')
    parser.add_argument("-nr", "--no_refresh", action='store_true', default=False, help="是否刷新")
    parser.add_argument("sources", nargs='+', help='域名或者域名文件路径')
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s version {iup.__version__} installed in {path.dirname(__file__)}",
    )
    args = parser.parse_args()
    config_path = path.join(path.dirname(__file__), 'config.ini')
    if not path.exists(config_path):
        gen_config()
    print('当前配置文件路径为:', config_path)
    config = Config(config_path)
    if args.no_refresh:
        config.refresh = False
    print('是否重启相关服务:', config.refresh)
    return args.sources, config

def update_rule_by_ssh(hostnames: list, config: Config):
    need_restart_dns = False
    need_restart_cdns = False
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(config.host, port=config.port, username=config.username, password=config.password)
    for hostname in hostnames:
        cmd = CMD_TEMPLATE.format(hostname)
        _, stdout, stderr = ssh.exec_command(cmd)
        msg = stdout.readlines()
        err = stderr.readlines()
        if MAGIC_STR in str(msg):
            need_restart_dns = True
        if MAGIC_STR2 in str(msg):
            need_restart_cdns = True
        print('msg', msg) if msg else print()
        print('err', err) if err else print()
    if config.refresh:
        if need_restart_dns:
            print('reboot dnsmasq')
            _, stdout, stderr = ssh.exec_command(CMD_DNSMASQ)
            msg = stdout.readlines()
            err = stderr.readlines()
            print('msg', msg) if msg else print()
            print('err', err) if err else print()
        if need_restart_cdns:
            print('reboot chinadns')
            _, stdout, stderr = ssh.exec_command(CMD_CHNDNS)
            msg = stdout.readlines()
            err = stderr.readlines()
            print('msg', msg) if msg else print()
            print('err', err) if err else print()
    ssh.close()

def gen_hostnames_by_sources(sources):
    hostnames = []
    for source in sources:
        if not path.exists(source):
            if is_domain_name(source):
                hostnames.append(source)
        elif path.isfile(source):
            hostnames += read_hostname_from_file(source)
    return list(dict.fromkeys(hostnames))

def main():
    sources, config = load_and_overlay_config()
    print('sources:', sources)
    hostnames = gen_hostnames_by_sources(sources)
    if hostnames:
        update_rule_by_ssh(hostnames, config)
    else:
        print('没有读取到有效域名，请检查！！！')

def read_info_from_input(prompt, parser=None):
    while True:
        info = input(prompt)
        if parser:
            info = parser(info)
            if not info is None:
                break
            else:
                print('输入有误，请重新输入！')
                continue
        break
    return info

def gen_config():
    print('配置向导，请按提示输入信息...')
    host = read_info_from_input('请输入有效主机名:\n', parse_host_name)
    port = int(read_info_from_input('请输入有效端口:\n', parse_port))
    username = read_info_from_input('请输入openwrt用户名:\n')
    password = read_info_from_input('请输入openwrt密码:\n')
    refresh = read_info_from_input('是否重启相关服务(dnsmasq、chinadns),Y(es)/N(o)/T(rue)/F(alse):\n', parse_yes_or_no)
    config = Config()
    config.update(host, port, username, password, refresh)
    config_path = path.join(path.dirname(__file__), 'config.ini')
    config.save_to(config_path)
    print('已生成配置文件写入到{}'.format(config_path))


if __name__ == '__main__':
    gen_config()





