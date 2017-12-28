# -*- coding: utf-8 -*-

import socket
import os
import shutil
import types
Root = 'F:/python/FTP/server/Root'


def system_start():
    server = socket.socket()
    server.bind(('localhost', 8888))  # host, port
    return server


def create_conn():
    server.listen()
    print('waiting for connect...')
    conn, address = server.accept()  # 调用Accept时会发生阻塞
    print("server ready")
    return conn


def put():
    file_size = int(str(conn.recv(1024), encoding='UTF-8'))  # 1
    print(file_size)
    conn.send(b'1')      # 2

    file_name = conn.recv(1024)
    with open(file_name, 'wb') as f:
        recv_size = 0
        while True:
            data = conn.recv(1024)  # 3
            f.write(data)
            recv_size += len(data)
            print(recv_size)
            if recv_size == file_size:
                print(str(recv_size))
                print('file received')
                conn.send(b'1')       # 4
                break
    conn.send(bytes('file received', encoding='UTF-8'))   # 5


def get():
    file_name = str(conn.recv(1024), encoding="UTF-8")  # a
    file_size = os.path.getsize(file_name)
    print(file_size)
    conn.send(bytes(str(file_size), encoding='UTF-8'))            # b
    recv_code = int(str(conn.recv(1024), encoding="UTF-8"))         # c
    n=0
    if recv_code:
        with open(file_name, 'rb') as f:
            for line in f:
                conn.send(line)    # d
                n += 1
                print(n)
        recv_code = int(str(conn.recv(1024), encoding="UTF-8"))   # e
        print(recv_code)
        if recv_code:
            print('upload success')
    data = conn.recv(1024)        # f
    print(str(data, encoding='utf-8'))


def lookup():
    recv_code = int(str(conn.recv(1024), encoding='UTF-8'))
    if int(str(recv_code)) == 1:
        path = os.listdir(os.getcwd())
        conn.send(bytes(str(path), encoding='UTF-8'))
        print(path)
        return path
    else:
        return 0


def new_folder():
    loc = str(conn.recv(1024), encoding="UTF-8")  # 1
    print(loc[:4])
    if loc[:4] == 'Root':
        print("abs_name")
        new_loc = Root + loc[4:]
        os.chdir(new_loc)
        folder_name = str(conn.recv(1024), encoding="UTF-8")  # 2
        os.mkdir(new_loc + "/" + folder_name)
        conn.send(bytes(str("new folder created!"), encoding="UTF-8"))  # 3
    else:
        print("dir_name")
        os.chdir(loc)
        folder_name = str(conn.recv(1024), encoding="UTF-8")  # 2
        os.mkdir(loc + "/" + folder_name)
        conn.send(bytes(str("new folder created!"), encoding="UTF-8"))  # 3


def remove_folder():
    loc = str(conn.recv(1024), encoding="UTF-8")  # 1
    print(loc[:4])
    if loc[:4] == 'Root':
        print("abs_name")
        new_loc = Root + loc[4:]
        os.chdir(new_loc)
        folder_name = str(conn.recv(1024), encoding="UTF-8")  # 2
        shutil.rmtree(new_loc + "/" + folder_name)                          # 删除非空文件夹
        conn.send(bytes(str("folder deleted!"), encoding="UTF-8"))  # 3
    else:
        print("dir_name")
        os.chdir(loc)
        folder_name = str(conn.recv(1024), encoding="UTF-8")  # 2
        shutil.rmtree(loc + "/" + folder_name)
        conn.send(bytes(str("folder deleted!"), encoding="UTF-8"))  # 3


def delete_file():
    loc = str(conn.recv(1024), encoding="UTF-8")  # 1
    print(loc[:4])
    if loc[:4] == 'Root':
        print("abs_name")
        new_loc = Root + loc[4:]
        os.chdir(new_loc)
        file_name = str(conn.recv(1024), encoding="UTF-8")  # 2
        os.remove(new_loc + "/" + file_name)  # 删除非空文件夹
        conn.send(bytes(str("file deleted!"), encoding="UTF-8"))  # 3
    else:
        print("dir_name")
        os.chdir(loc)
        file_name = str(conn.recv(1024), encoding="UTF-8")  # 2
        os.remove(loc + "/" + file_name)
        conn.send(bytes(str("file deleted!"), encoding="UTF-8"))  # 3


def change_location():
    loc = str(conn.recv(1024), encoding="UTF-8")  # 1
    print(loc[:4])
    if loc[:4] == 'Root':
        print("abs_name")
        new_loc = Root + loc[4:]
        os.chdir(new_loc)
        conn.send(bytes(str("location changed!"), encoding="UTF-8"))  # 3
    else:
        print("dir_name")
        os.chdir(loc)
        conn.send(bytes(str("location changed!"), encoding="UTF-8"))  # 3


def select(func):
    if func == 'lookup':
        lookup()
    elif func == 'get':
        get()
    elif func == 'put':
        put()
    elif func == 'new_folder':
        new_folder()
    elif func == 'remove_folder':
        remove_folder()
    elif func == 'change_location':
        change_location()
    elif func == 'delete_file':
        delete_file()


if __name__ == '__main__':
    server = system_start()
    os.chdir(Root)
    while True:
        conn = create_conn()
        func = str(conn.recv(1024), encoding="UTF-8")    # select
        if func == 'quit':
            continue
        select(func)
