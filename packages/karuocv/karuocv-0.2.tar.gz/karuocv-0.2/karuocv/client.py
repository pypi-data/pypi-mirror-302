# _*_ encoding: utf-8 _*_
'''
@文件    :client.py
@说明    :
@时间    :2024/10/15 22:37:26
@作者    :caimmy@hotmail.com
@版本    :0.1
'''

import argparse

def init_command_args():
    parser = argparse.ArgumentParser(description="SACP object train tools")

    parser.add_argument("--task", help="指定任务 train, inference, ETC")
    

    args = parser.parse_args()
    return args

def client_command():
    command_line_args = init_command_args()
    print(command_line_args)
