import os ,time

timer = 60 * 12

while True:
    os.system(r'.\venv\Scripts\activate && python main.py')
    counter = 1

    while counter != timer:
        print(f' waiting ... {counter}s : {timer}s ', end="\r")
        time.sleep(1)
        counter += 1


