# -*- coding: utf-8 -*-

import socket
import os


def system_start():
    client = socket.socket()
    client.connect(('localhost', 8888))
    return client


def put(client):
    file_name = input("plz input a file name under root with extended name\n")
    file_size = os.path.getsize(file_name)
    print(file_size)
    client.send(bytes(str(file_size), encoding='UTF-8'))         # 1
    recv_code = int(str(client.recv(1024), encoding="UTF-8"))    # 2

    client.send(bytes(str(file_name), encoding='UTF-8'))
    n = 0
    if recv_code:
        with open(file_name, 'rb') as f:
            for line in f:
                client.send(line)    # 3
                n += 1
                print(n)
        recv_code = int(str(client.recv(1024), encoding="UTF-8"))   # 4
        print(recv_code)
        if recv_code:
            print('upload success')

    data = client.recv(1024)

    print(str(data, encoding='utf-8'))     # 5


def get(client):
    file_name = input("plz input a file name with extended name\n")
    client.send(bytes(str(file_name), encoding="UTF-8"))             # a
    file_size = int(str(client.recv(1024), encoding='UTF-8'))       # b
    print(file_size)
    client.send(b'1')       # c
    with open(file_name, 'wb') as f:
        recv_size = 0
        while True:
            data = client.recv(1024)  # d
            f.write(data)
            recv_size += len(data)
            print("recv_size:", recv_size)
            if recv_size == file_size:
                print(str(recv_size))
                print('file received')
                client.send(b'1')       # e
                break
    client.send(bytes('file received', encoding='UTF-8'))   # f


def lookup():
    loc = input("plz choose 'local' or 'server'\n")
    if loc == 'local':
        client.send(b'0')
        path = os.listdir(os.getcwd())
        print(path)
        return path
    elif loc == 'server':
        client.send(b'1')
        path = client.recv(1024)
        print((str(path, encoding="UTF-8")))
        return path


def new_folder():
    loc = input("@@@\nplz input the root location you want to create a new folder!\n@@@\n")
    client.send(bytes(str(loc), encoding='UTF-8'))   # 1
    folder_name = input("---\nplz input the folder name you want to create!\n---\n")
    client.send(bytes(str(folder_name), encoding='UTF-8'))  # 2
    recv_code = str(client.recv(1024), encoding='UTF-8')   # 3
    print(recv_code)


def remove_folder():
    loc = input("@@@\nplz input the root location you want to delete a folder!\n@@@\n")
    client.send(bytes(str(loc), encoding='UTF-8'))  # 1
    folder_name = input("---\nplz input the folder name you want to delete!\n---\n")
    client.send(bytes(str(folder_name), encoding='UTF-8'))  # 2
    recv_code = str(client.recv(1024), encoding='UTF-8')  # 3
    print(recv_code)


def delete_file():
    loc = input("@@@\nplz input the root location you want to delete a file!\n@@@\n")
    client.send(bytes(str(loc), encoding='UTF-8'))  # 1
    file_name = input("---\nplz input the file name you want to delete!\n---\n")
    client.send(bytes(str(file_name), encoding='UTF-8'))  # 2
    recv_code = str(client.recv(1024), encoding='UTF-8')  # 3
    print(recv_code)


def change_location():
    loc = input("@@@\nplz input the path you want locate\n@@@\n")
    client.send(bytes(str(loc), encoding='UTF-8'))  # 1
    recv_code = str(client.recv(1024), encoding='UTF-8')  # 3
    print(recv_code)


def select(func):
    if func == 'put':
        client.send(bytes(str("put"), encoding="UTF-8"))     # select
        put(client)
    elif func == 'get':
        client.send(bytes(str("get"), encoding="UTF-8"))     # select
        get(client)
    elif func == 'new_folder':
        client.send(bytes(str("new_folder"), encoding="UTF-8"))     # select
        new_folder()
    elif func == 'remove_folder':
        client.send(bytes(str("remove_folder"), encoding="UTF-8"))     # select
        remove_folder()
    elif func == 'lookup':
        client.send(bytes(str("lookup"), encoding="UTF-8"))
        lookup()
    elif func == 'change_location':
        client.send(bytes(str("change_location"), encoding="UTF-8"))
        change_location()
    elif func == 'delete_file':
        client.send(bytes(str("delete_file"), encoding="UTF-8"))
        delete_file()


if __name__ == '__main__':
    while True:
        client = system_start()             # 注意这里，每次连接必须要重新请求
        func = input("***\nplz input a func, choices in <get, put, delete_file, new_folder, remove_folder, lookup, change_location, quit>\n***\n")
        if func == 'quit':
            print("quit")
            client.send(bytes(str("quit"), encoding="UTF-8"))
            break
        select(func)

