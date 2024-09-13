import time
import threading
from random import randint

class Bank:
    def __init__(self, balance=0):
        self.balance = balance
        self.lock = threading.Lock()

    def deposit(self):
        for _ in range(100):
            rnd_num_1 = randint(50, 500)
            with self.lock:
                self.balance += rnd_num_1
                print(f'Пополнение: {rnd_num_1}. Баланс: {self.balance}')
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            time.sleep(0.001)

    def take(self):
        for _ in range(100):
            rnd_num_2 = randint(50, 500)
            print(f'Запрос на {rnd_num_2}')
            with self.lock:
                if rnd_num_2 <= self.balance:
                    self.balance -= rnd_num_2
                    print(f'Снятие: {rnd_num_2}. Баланс: {self.balance}')
                else:
                    print(f'Запрос отклонён, недостаточно средств')
                    self.lock.acquire()
            time.sleep(0.001)

bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()

th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
