import socket
import threading
import queue
import sys
import random
import os

d = "000"
key = 567  # Ключ шифрования


# Код клиента, отправление информации и создание крипта
def ReceiveData(sock):
    global d, key
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            print(data.decode('utf-8'))
            d = data.decode('utf-8')
            crypt = ''
            for i in d:
                crypt += chr(ord(i) ^ key)
            data = crypt
            if d == 'cstop':
                print(d)
            else:
                print(data)
        except:
            pass


# Запуск клиента
def RunClient(serverIP):
    global d, key
    key = input("Введите ключ (567): ")
    if key == '':
        key = 567
    else:
        key = int(key)
    host = socket.gethostbyname(socket.gethostname())
    port = random.randint(6000, 10000)
    print('Клиент IP->' + str(host) + ' Порт->' + str(port))
    server = (str(serverIP), 5000)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    name = input('Введите свое имя: ')
    if name == '':
        name = 'Гость' + str(random.randint(1000, 9999))
        print('Ваше имя ' + name)
    else:
        print('Ваше имя', name)
    print('Введите какую-нибудь информацию: ')
    s.sendto(name.encode('utf-8'), server)
    threading.Thread(target=ReceiveData, args=(s,)).start()
    while True:
        if d == "cstop":
            break
        data = input()
        if data == 'qqq' or data == 'sstop':
            break
        elif data == '':
            continue
        data = '[' + name + ']' + '-> ' + data
        print(data)
        crypt = ''
        for i in data:
            crypt += chr(ord(i) ^ key)
        data = crypt
        print('Crypt ->', data)
        s.sendto(data.encode('utf-8'), server)
    s.sendto(data.encode('utf-8'), server)
    s.close()
    os._exit(1)


# Код сервера на отправку какой-либо информации
def RecvData(sock, recvPackets):
    while True:
        data, addr = sock.recvfrom(1024)
        recvPackets.put((data, addr))


# Запуск сервера
def RunServer():
    host = socket.gethostbyname(socket.gethostname())
    port = 5000
    print('Хостинг сервера по IP-адресу -> ' + str(host))
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    clients = set()
    recvPackets = queue.Queue()

    print('Сервер запускается...')

    threading.Thread(target=RecvData, args=(s, recvPackets)).start()

    while True:
        while not recvPackets.empty():
            data, addr = recvPackets.get()
            if addr not in clients:
                clients.add(addr)
                continue
            clients.add(addr)
            data = data.decode('utf-8')
            if 'sstop' in data:
                for c in clients:
                    s.sendto('cstop'.encode('utf-8'), c)
                s.close()
                os._exit(1)
            if data.endswith('qqq'):
                clients.remove(addr)
                continue
            print(str(addr) + ' crypt ->', data)
            for c in clients:
                if c != addr:
                    s.sendto(data.encode('utf-8'), c)
    s.close()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        RunServer()
    elif len(sys.argv) == 2:
        RunClient(sys.argv[1])
    else:
        print('Запуск сервера:-> python Chat.py')
        print('Запуск клиента:-> python Chat.py <ServerIP>')
