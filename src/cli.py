"""
cli.py 1.4-dev
"""
# -*- coding:utf-8 -*-

import logging
import socket
import sys
import threading
import time

import pynput
import requests

import utils

VERSION = utils.versions["CLI"]["version"]
mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()
res = utils.Resources(0)

while True:
    print(f"Spam Bot CLI v{VERSION}")
    print("1) Ctrl+V bot")
    print("2) Click Bot")
    print("3) Connect to a Chat Server")
    print("4) Create a Chat Server")
    print("5) Settings")
    print("6) Check for updates")
    print("7) Exit\n")
    choice = input("Function : ")
    if choice == "1":
        while True:
            print("How many times do you want to spam?")
            try:
                spam_times = int(input("SPAM TIMES ="))
                while True:
                    SPAM_INTERVAL = input("Enable spam interval? Y/N : ")
                    if SPAM_INTERVAL in ("Y", "y"):
                        SPAM_INTERVAL = True
                        break
                    if SPAM_INTERVAL in ("N", "n"):
                        SPAM_INTERVAL = False
                        break
                    print("Invalid value, please enter again!")
                spam = utils.SpamBot(spam_times, SPAM_INTERVAL, res)
                time.sleep(4)

                def on_press(key) -> None:
                    """See pynput documentation"""
                    if key == pynput.keyboard.Key.shift:
                        spam.reset()

                def paste() -> None:
                    """Simulate LEFT_CONTROL + V"""
                    while not spam.finished():
                        spam.increase()
                        keyboard.press(pynput.keyboard.Key.ctrl_l)
                        keyboard.press("v")
                        keyboard.release(pynput.keyboard.Key.ctrl_l)
                        keyboard.release("v")
                        keyboard.press(pynput.keyboard.Key.enter)
                        keyboard.release(pynput.keyboard.Key.enter)
                        time.sleep(spam.interval)
                    # Since user can press shift to stop spamming
                    # we help him press shift after the spam ends
                    keyboard.press(pynput.keyboard.Key.shift)
                    keyboard.release(pynput.keyboard.Key.shift)

                paste_thread = threading.Thread(target=paste)
                paste_thread.start()
                with pynput.keyboard.Listener(on_press=on_press) as listener:
                    listener.join()
                paste_thread.join()
                res.sound_effect("finish")
                print("\nSpamming finished, returning to the main menu.")
                break
            except ValueError:
                # User enter a non-integer value (exclude float)
                print("Please enter a valid value.")
    elif choice == "2":
        while True:
            print("How many times do you want to click? ")
            click_times = input("Click Times =")
            try:
                spam = utils.SpamBot(int(click_times), False, res)

                def on_press(key) -> None:
                    """See pynput documentation"""
                    if key == pynput.keyboard.Key.shift:
                        spam.reset()

                def click() -> None:
                    """Spam clicks for specific times"""
                    while not spam.finished():
                        spam.increase()
                        mouse.click(pynput.mouse.Button.left, count=1)
                        time.sleep(0.01)
                    keyboard.press(pynput.keyboard.Key.shift)
                    keyboard.release(pynput.keyboard.Key.shift)

                click_thread = threading.Thread(target=click)
                click_thread.start()
                with pynput.keyboard.Listener(on_press=on_press) as listener:
                    listener.join()
                click_thread.join()
                res.sound_effect("finish")
                print("\nSpamming finished, returning to the main menu.")
                break
            except ValueError:
                print("Please enter a valid value.")
    elif choice == "3":
        print("Loading available servers... Please wait\n")
        try:
            server_get = requests.get(utils.SERVER_URL)
            if server_get.status_code != 200:
                print(f"Status code {server_get.status_code}, do the repo exist?")
            else:
                server_get = server_get.json()
                print("List of available servers:")
                try:
                    for a in server_get:
                        print(
                            f"{list(server_get).index(a) + 1}) {a} "
                            f"{server_get[a]['address']}:{server_get[a]['port']}"
                        )
                except IndexError:
                    print("Error: No server found.")
                ip_address = requests.get("https://httpbin.org/ip").json()["origin"]
                print(f"Your IP address is {ip_address}")
                while True:
                    print("\nWhich server would you like to connect?")
                    selected = input(
                        f"Enter {list(range(1, len(server_get) + 1))}, or 0 for dedicated IP address : "
                    )
                    try:
                        selected = int(selected)
                        if selected == 0:
                            print("\nEnter the chat server IP address.")
                            while True:
                                chat_ip = input("Server IP address =")
                                port = input("Server port number =")
                                try:
                                    port = int(port)
                                    if 0 < port < 65536:
                                        break  # break the next print() line
                                    print("Please enter a valid value.")
                                except ValueError:
                                    print("Please enter a valid value.")
                            break
                        selected_server = server_get[list(server_get)[selected - 1]]
                        chat_ip, port = (
                            selected_server["address"],
                            selected_server["port"],
                        )
                        break
                    except ValueError:
                        print("Please enter a valid value.")
                print(f"\nConnecting to {chat_ip}:{port}")

                def receive() -> None:
                    """Thread for receive incoming TCP packet"""
                    while True:
                        try:
                            message = s.recv(utils.BUFFER)
                            print(message.decode(utils.ENCODING))
                            res.sound_effect("receive")
                        except socket.error:
                            break

                def send() -> None:
                    """Thread for sending outgoing TCP packet"""
                    while True:
                        time.sleep(0.2)
                        message = input()
                        if message == "/exit":
                            s.close()
                        else:
                            s.send(
                                f"{utils.return_time()}[{username}]{message}".encode(
                                    utils.ENCODING
                                )
                            )
                            res.sound_effect("send")

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.settimeout(5)
                    s.connect((chat_ip, port))
                    s.settimeout(None)
                    print("\nSuccessfully connected to the server.")
                    username = input("Username =")
                    receive_thread = threading.Thread(target=receive)
                    receive_thread.start()
                    s.send(
                        f"{utils.return_time()}[{username}]{utils.PING_MESSAGE}".encode(
                            utils.ENCODING
                        )
                    )
                    print(
                        "\nEnter your message below and press enter to send the message."
                    )
                    print(
                        "Type '/clients' to show the existing connections on the server,"
                    )
                    print("type '/exit' to return to the main menu.")
                    send()
                except socket.error as error:
                    print(f"\n{error}\n")
                    s.close()
        except OSError as error:
            print(f"\n{error}\nNetwork access forbidden?")
    elif choice == "4":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("\nWhat is your server name?")
        server_name = input("Server Name : ")

        while True:
            print("\nWhat is your listening port?")
            listen_port = input("Port Number : ")
            try:
                listen_port = int(listen_port)
                if 0 < listen_port < 65536:
                    break
                print("Please enter a valid value.")
            except ValueError:
                print("Please enter a valid value.")

        print("\nEnable logging?")
        while True:
            mode = input("Y/N =")
            if mode in ("Y", "y"):
                LOG_RECORD = 1
                logging.basicConfig(
                    filename=f"[{server_name}]{utils.return_time(True)}",
                    level=logging.INFO,
                )
                break
            if mode in ("N", "n"):
                LOG_RECORD = 0
                break
            print("Invalid value, please enter again!")

        """def log(data: str, printing: bool = False) -> None:
            #Log data if LOG_RECORD == 1
            if LOG_RECORD == 1:
                logging.info(data.strip("\n"))
            if printing:
                print(data)"""

        # log("Logger starts logging.", False)
        try:
            API_IP_address = requests.get("https://httpbin.org/ip").json()["origin"]
            IP_address = f"[{API_IP_address}:{str(listen_port)}]"
        # Get chat server's IP address
        except ConnectionError:
            API_IP_address = ""
            IP_address = "[0.0.0.0:0]"
        print(f"\nYou are listening on all available interfaces and port {listen_port}")
        print("Performing self-reachability test...\n")
        s.bind(("", listen_port))
        # self-reachability test
        if len(API_IP_address) > 6:

            def test_reachability() -> None:
                """Thread for receive self-testing packet"""
                try:
                    s.accept()
                except socket.error:
                    pass

            try:
                test_thread = threading.Thread(target=test_reachability)
                test_thread.start()
                s.settimeout(3)
                s.connect((API_IP_address, listen_port))
                test_thread.join()
                print(
                    "Self-reachability test indicate your listen port is reachable. "
                    "Excellent. Waiting for incoming connections.\n"
                )
                try:
                    s.close()
                except socket.error:
                    pass
            except OSError as error_test:
                print(error_test)
                print(
                    "Self-reachability test failed. Server will continue to listen incoming connections.\n"
                )
        else:
            print(
                "Cannot start self-reachability test. Server will continue to listen incoming connections.\n"
            )
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", listen_port))
        CAPACITY = 20
        s.listen(CAPACITY)
        # log(f"Server running at version {VERSION}", True)
        # log(f"Server name is set to {server_name}", True)
        # log(f"Maximum connections = {CAPACITY}", True)
        # log("Server is up!", True)
        USERNAME = "[Bot]"
        client_list = []
        exist_conn_address = []

        def server_receive() -> None:
            """Server Thread for handling incoming TCP packets
            If received 'Client PING', server will send welcoming message to new client
            """
            while True:
                try:
                    conn, address = s.accept()
                    single_quote = "'"
                    client_address = f"[{str(address[0]).strip(single_quote)}:{str(address[1]).strip()}]"
                    client_list.append(conn)
                    exist_conn_address.append(address)
                    # log(f"New connection from {client_address}", True)
                    # log(f"Client list : {str(client_list)}")
                    # log(f"Client address : {client_address}")
                    client_address_2 = client_address.replace("[", " ").strip("]")
                    broadcast(
                        f"{IP_address}{utils.return_time()}{USERNAME}{client_address_2} is connected."
                    )
                    while True:
                        try:
                            received = conn.recv(utils.BUFFER)
                            received_decoded = received.decode(utils.ENCODING)
                            # log(client_address + received_decoded, True)
                            res.sound_effect("receive")
                            if utils.PING_MESSAGE in received_decoded:
                                conn.send(
                                    f"{IP_address}{utils.return_time()}"
                                    f"{USERNAME} Welcome to {server_name}!".encode(
                                        utils.ENCODING
                                    )
                                )
                                # log(f"{IP_address}{utils.return_time()}" f"{USERNAME} Welcome to {server_name}
                                # server!")
                                conn.send(
                                    f"{IP_address}{utils.return_time()}"
                                    f"{USERNAME} Server version {VERSION}".encode(
                                        utils.ENCODING
                                    )
                                )
                                # log(f"{IP_address}{utils.return_time()}{USERNAME} Server is "
                                #    f"running the version {VERSION}")
                            elif "/clients" in received_decoded:
                                conn.send(
                                    f"{IP_address}{utils.return_time()}"
                                    f"{USERNAME}Existing Connections List:".encode(
                                        utils.ENCODING
                                    )
                                )
                                for index, user_address in enumerate(
                                    exist_conn_address
                                ):
                                    request2 = (
                                        f"{IP_address}{utils.return_time()}"
                                        f"{USERNAME} {index}) {user_address}"
                                    )
                                    conn.send(request2.encode(utils.ENCODING))
                                    time.sleep(0.2)
                            else:
                                broadcast(client_address + received_decoded)
                        except ConnectionError:  # as conn_error:
                            # log(f"{utils.return_time()}{client_address_2}{str(conn_error)}")
                            # log(f"{utils.return_time()}{client_address_2} is disconnected.", True)

                            if conn in client_list and address in exist_conn_address:
                                client_list.remove(conn)
                                exist_conn_address.remove(address)
                                conn.close()
                                broadcast(
                                    IP_address
                                    + utils.return_time()
                                    + USERNAME
                                    + client_address_2
                                    + " is disconnected."
                                )
                            break
                except OSError:
                    break

        server_threads = []
        for a in range(10):
            server_threads.append(threading.Thread(target=server_receive))
            server_threads[a].start()

        def broadcast(message: str) -> None:
            """
            Send the message to all client connected (in client_list)
            (Also the one who send the message, so that send message->no response indicates problem)
            """
            n = 0  # counter of the while loop, starts at 0 because list starts at 0
            while n < len(client_list):
                try:
                    # send the message to nth client in the list
                    client_list[n].send(message.encode(utils.ENCODING))
                    n += 1  # next client
                except (
                    socket.error
                ):  # usually because client was disconnected at that moment
                    client_n = client_list[n]  # store the socket object for close()
                    client_list.remove(client_n)
                    address_n = exist_conn_address[
                        n
                    ]  # store the address for broadcasting who has disconnected
                    exist_conn_address.remove(address_n)
                    # address is more readable than conn
                    broadcast(
                        f"{utils.return_time()}[Server Broadcast]{str(address_n)} is disconnected."
                    )
                    client_n.close()

        def admin_function() -> None:
            """Contains function for the admin to use"""
            print("Enter Command for advanced server control.")
            print("/help   - checking existing connection")
            print("/remove - removing clients")
            print("/close  - shutdown server")
            while True:
                message = input()
                # log(f"{utils.return_time()}[Server Command]{message}")
                if message == "/help":
                    print("Existing Connections List: ")
                    for index, user_address in enumerate(exist_conn_address):
                        print(f"{index}) {user_address}")
                elif message == "/remove":
                    print("Existing Connections List: ")
                    for index, user_address in enumerate(exist_conn_address):
                        print(f"{index}) {user_address}")
                    while True:
                        print("Which client do you want to kick? (Exit with -1)")
                        which_connection = input("Number =")
                        if which_connection == "-1":
                            print("Returning to main menu")
                            break
                        try:
                            which_connection = int(which_connection)
                            try:
                                client_conn = client_list[which_connection]
                                client_list.remove(client_conn)
                                client_address = exist_conn_address[which_connection]
                                exist_conn_address.remove(client_address)
                                client_conn.send(
                                    "You have been kicked from the server.".encode(
                                        utils.ENCODING
                                    )
                                )
                                client_conn.close()
                                broadcast(
                                    f"{client_address} has been kicked by the server."
                                )
                                break
                            except IndexError:  # t
                                print("Invalid value, please enter again!")
                            except ConnectionError:
                                print("Client has already been kicked.")
                        except ValueError:
                            print("Invalid value, please enter again!")
                elif message == "/close":
                    broadcast(
                        f"{utils.return_time()}"
                        f"[Server Broadcast]Server shutdown in 10 seconds."
                    )
                    # log("Server shutdown in 10 seconds. (/close)", True)
                    for countdown in range(10, 0, -1):
                        broadcast(str(countdown))
                        print(countdown)
                        time.sleep(1)
                    for clients in client_list:
                        clients.close()
                    s.close()
                    res.sound_effect("finish")
                    break
                else:
                    print("Invalid command, please enter again!")

        admin_function()
    elif choice in "5":
        while True:
            print("Settings")
            print(f"1) Enable Sound [{res.sound_enable}]")
            print("0) Menu")
            print("\nWhich setting do you want to change?")
            setting_choice = input(
                "Setting =",
            )
            if setting_choice == "1":
                if res.sound_enable:
                    res.sound_enable = False
                else:
                    res.sound_enable = True
                break
            if setting_choice == "0":
                break
            print("Invalid value, please enter again. ")
    elif choice == "6":
        print("\nChecking for updates...")
        try:
            newest_version = requests.get(utils.UPDATE_URL)
            if newest_version.status_code != 200:
                print(f"Status code {newest_version.status_code}, do the repo exist?")
            else:
                newest_version = newest_version.json()
                res.sound_effect("notice")
                for imp in list(newest_version):
                    print(f'{imp}: {newest_version[imp]["version"]}')
                if newest_version["CLI"]["version"] != VERSION:
                    print(
                        f"\nNew version {newest_version['CLI']['version']} is available!"
                    )
                else:
                    print("\nProgram is up-to-date!")
        except OSError as network_error:
            print(f"\n{network_error}\nNetwork access forbidden?")
    elif choice == "7":
        print("\nExiting program...")
        sys.exit(0)
    else:
        print("Please enter a correct number.")
        time.sleep(0.3)
