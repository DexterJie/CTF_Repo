import random
import socket
import threading
import os

def calculate_level1(m, x, y):
    return (m | x) + (m | y)

def calculate_level2(m, x, y):
    return (m | x) + (m ^ y)

def level(conn, calculate, x, y, guess, description, test_times):
    for _ in range(test_times):
        conn.sendall(b"Enter your number: ")
        
        # 设置 5 秒超时
        conn.settimeout(5)
        
        try:
            data = conn.recv(1024)
            if not data:
                return False
            try:
                test = int(data.strip())
            except:
                conn.sendall(b"Invalid input. Bye.\n")
                return False
            result = calculate(test, x, y)
            conn.sendall(f"Calculation result: {result}\n".encode())
        except socket.timeout:
            conn.sendall(b"Time out! Respond in 5 seconds.\n")
            return False

    conn.sendall(f"\nNow, guess the result of {description} for m = {guess}:\n".encode())
    
    # 设置 5 秒超时
    conn.settimeout(5)
    
    try:
        data = conn.recv(1024)
        if not data:
            return False
        try:
            user_guess = int(data.strip())
        except:
            conn.sendall(b"Invalid input. Bye.\n")
            return False

        correct_result = calculate(guess, x, y)
        if user_guess == correct_result:
            conn.sendall(b"Correct! Proceeding to next level...\n\n")
            return True
        else:
            conn.sendall(b"Wrong guess! Exiting...\n")
            return False
    except socket.timeout:
        conn.sendall(b"Time out! You took too long to respond.\n")
        return False

def handle_client(conn, addr, flag):
    conn.sendall(b"Welcome to Puzzle!\n\n")
    try:
        # Level 1
        x = random.getrandbits(30)
        y = random.getrandbits(30)
        guess = random.getrandbits(30)
        conn.sendall(b"Level 1:\n")
        if not level(conn, calculate_level1, x, y, guess, "(m | x) + (m | y)", test_times=2):
            conn.close()
            return

        # Level 2
        x = random.getrandbits(30)
        y = random.getrandbits(30)
        guess = random.getrandbits(30)
        conn.sendall(b"Level 2:\n")
        if not level(conn, calculate_level2, x, y, guess, "(m | x) + (m ^ y)", test_times=2):
            conn.close()
            return

        # 通关，发flag
        conn.sendall(f"Congratulations! You've passed all levels!\nHere is your flag: {flag}\n".encode())
    except Exception as e:
        conn.sendall(b"An error occurred. Bye.\n")
    finally:
        conn.close()

def main():
    host = "0.0.0.0"
    port = 2227

    flag = os.getenv('FLAG', 'flag{testflag}')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print(f"[+] Listening on {host}:{port}")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr, flag)).start()

if __name__ == "__main__":
    main()