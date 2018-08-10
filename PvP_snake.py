#! usr/bin/env/python
# coding = utf-8
# Author = 0Villian0
# Date = 8|9|2018
# Version = 0.1

import curses
import random
import threading
from multiprocessing import Process


def initialize_windows():
    global w, H, W, food, snake, snake_1, score, score_1, key, key_1
    w = curses.initscr()                                                                                                # initialize the Windows
    curses.start_color()                                                                                                # 开启颜色显示
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)                                                           # 自定义颜色方案组
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.curs_set(0)                                                                                                  # 关闭光标显示
    curses.cbreak()                                                                                                     # 开启cbreak模式，键盘输入立即执行，而不是缓冲输入模式那样等待回车后才执行
    curses.noecho()                                                                                                     # 关闭键盘输入屏幕回显
    w.keypad(True)                                                                                                      # 开启特殊键位输入处理功能 如：上下左右键等
    w.timeout(1000)                                                                                                        # 设置读取键盘输入等待时间 单位：毫秒
    H, W = w.getmaxyx()                                                                                                 # 获取w窗口的长宽
    # H, W = 11, 11                                                                                                     # 把窗口设为固定值 调试用
    food = [[int(H / 2), int(W / 2)]]                                                                                   # initialize the position of food
    w.addch(food[0][0], food[0][1], '$', curses.color_pair(2))                                                          # 在窗口中的坐标点使用颜色组2打印字符
    snake = [[int(H / 2), int(W * 2 / 10)]]                                                                             # initialize the position of snake
    w.addch(snake[0][0], snake[0][1], 'X', curses.color_pair(1))
    snake_1 = [[int(H / 2), int(W * 8 / 10)]]
    w.addch(snake_1[0][0], snake_1[0][1], 'X', curses.color_pair(3))
    score, score_1 = 0, 0                                                                                               # 分数值
    key, key_1 = curses.KEY_RIGHT, 97                                                                                   # 运动方向键值


def recover_windows():                                                                                                  # 恢复原始窗口设置，退出
    # global w                                                                                                          # 错误点：python中列表、字典、对象是明确的，不需要显式的声明global
    w.keypad(False)
    curses.echo()
    curses.nocbreak()
    curses.endwin()


# def player():                                                                                                           # 玩家操控贪吃蛇
#     global key
#     while True:
#         next_key = w.getch()                                                                                            # 获取下一个方向键
#         if next_key == 27:                                                                                              # 按下Esc鍵或者發生error則恢復窗口後退出
#             recover_windows()
#             print('QUIT GAME! \nScore:' + str(score))
#             return
#
#         if next_key == curses.KEY_RIGHT and key != curses.KEY_LEFT \
#                 or next_key == curses.KEY_LEFT and key != curses.KEY_RIGHT \
#                 or next_key == curses.KEY_UP and key != curses.KEY_DOWN \
#                 or next_key == curses.KEY_DOWN and key != curses.KEY_UP:
#             key = next_key                                                                                              # 获取有效的运动方向键
#
#         temp = snake[0]                                                                                                 # 更新蛇头位置
#         if key == curses.KEY_UP:
#             snake.insert(0, [temp[0] - 1, temp[1]])
#         if key == curses.KEY_DOWN:
#             snake.insert(0, [temp[0] + 1, temp[1]])
#         if key == curses.KEY_RIGHT:
#             snake.insert(0, [temp[0], temp[1] + 1])
#         if key == curses.KEY_LEFT:
#             snake.insert(0, [temp[0], temp[1] - 1])
#
#         if snake[0] in snake[1:] or snake[0][0] in (0, H) or snake[0][1] in (0, W):                                     # 判断蛇是否死亡,是则恢复默认窗口退出
#             # recover_windows()
#             # print('Your Snake is death! \nScore:' + str(score))
#             return
#
#         eaten()
#         w.addch(snake[0][0], snake[0][1], 'X', curses.color_pair(1))
#
#
# def player_1():                                                                                                         # 玩家操控贪吃蛇
#     global key_1
#     while True:
#         next_key = w.getch()                                                                                            # 获取下一个方向键
#         if next_key == 27:                                                                                              # 按下Esc鍵或者發生error則恢復窗口後退出
#             recover_windows()
#             print('QUIT GAME! \nScore:' + str(score_1))
#             return
#
#         if next_key == 100 and key_1 != 97 \
#                 or next_key == 97 and key_1 != 100 \
#                 or next_key == 119 and key_1 != 115 \
#                 or next_key == 115 and key_1 != 119:
#             key_1 = next_key                                                                                            # 获取有效的运动方向键
#
#         temp = snake_1[0]                                                                                               # 更新蛇头位置
#         if key_1 == 119:
#             snake_1.insert(0, [temp[0] - 1, temp[1]])
#         if key_1 == 115:
#             snake_1.insert(0, [temp[0] + 1, temp[1]])
#         if key_1 == 100:
#             snake_1.insert(0, [temp[0], temp[1] + 1])
#         if key_1 == 97:
#             snake_1.insert(0, [temp[0], temp[1] - 1])
#
#         if snake_1[0] in snake_1[1:] or snake_1[0][0] in (0, H) or snake_1[0][1] in (0, W):                             # 判断蛇是否死亡,是则恢复默认窗口退出
#             # recover_windows()
#             # print('Your Snake is death! \nScore:' + str(score_1))
#             return
#
#         eaten(1)
#         w.addch(snake_1[0][0], snake_1[0][1], 'X', curses.color_pair(3))
#
#
# def eaten(num=0):                                                                                                       # 检查食物状态
#     global score, score_1
#     if num == 0:
#         if snake[0] == food[0]:                                                                                         # 判断是否吃掉食物
#             temp = food.pop()
#             w.addch(temp[0], temp[1], ' ')                                                                              # 把吃掉的食物打印為空
#             if len(snake) < (H - 1) * (W - 1) - len(snake_1):                                                           # 判断是否走完
#                 while temp in snake or temp in snake_1:                                                                 # 隨機產生一個食物
#                     temp = [random.randint(1, H - 1), random.randint(1, W - 1)]
#                 food.insert(0, temp)
#                 w.addch(temp[0], temp[1], '$', curses.color_pair(2))                                                    # 打印顯示新食物
#             score += 1                                                                                                  # 記錄分數
#         else:
#             tail = snake.pop()                                                                                          # 沒有吃到食物需要把尾巴去掉
#             w.addch(tail[0], tail[1], ' ')
#     elif num == 1:
#         if snake_1[0] == food[0]:                                                                                       # 判断是否吃掉食物
#             temp = food.pop()
#             w.addch(temp[0], temp[1], ' ')                                                                              # 把吃掉的食物打印為空
#             if len(snake_1) < (H - 1) * (W - 1) - len(snake):                                                           # 判断是否走完
#                 while temp in snake_1 or temp in snake:                                                                 # 隨機產生一個食物
#                     temp = [random.randint(1, H - 1), random.randint(1, W - 1)]
#                 food.insert(0, temp)
#                 w.addch(temp[0], temp[1], '$', curses.color_pair(2))                                                    # 打印顯示新食物
#             score_1 += 1                                                                                                # 記錄分數
#         else:
#             tail = snake_1.pop()                                                                                        # 沒有吃到食物需要把尾巴去掉
#             w.addch(tail[0], tail[1], ' ')


def played():
    global key, key_1
    next_key = None
    while True:
        if K:
            lock.acquire()
            next_key = K.pop(0)
            lock.release()
            if next_key == 27:
                recover_windows()
                print('QUIT GAME! \nPlayer1 Score: %d\nPlayer2 Score: %d' % (score, score_1))
                return

        if next_key == curses.KEY_RIGHT and key != curses.KEY_LEFT \
                or next_key == curses.KEY_LEFT and key != curses.KEY_RIGHT \
                or next_key == curses.KEY_UP and key != curses.KEY_DOWN \
                or next_key == curses.KEY_DOWN and key != curses.KEY_UP:
            key = next_key
        elif next_key == 100 and key_1 != 97 \
                or next_key == 97 and key_1 != 100 \
                or next_key == 119 and key_1 != 115 \
                or next_key == 115 and key_1 != 119:
            key_1 = next_key

        temp = snake[0]  # 更新蛇头位置
        if key == curses.KEY_UP:
            snake.insert(0, [temp[0] - 1, temp[1]])
        if key == curses.KEY_DOWN:
            snake.insert(0, [temp[0] + 1, temp[1]])
        if key == curses.KEY_RIGHT:
            snake.insert(0, [temp[0], temp[1] + 1])
        if key == curses.KEY_LEFT:
            snake.insert(0, [temp[0], temp[1] - 1])

        temp = snake_1[0]  # 更新蛇头位置
        if key_1 == 119:
            snake_1.insert(0, [temp[0] - 1, temp[1]])
        if key_1 == 115:
            snake_1.insert(0, [temp[0] + 1, temp[1]])
        if key_1 == 100:
            snake_1.insert(0, [temp[0], temp[1] + 1])
        if key_1 == 97:
            snake_1.insert(0, [temp[0], temp[1] - 1])

        if snake[0] in snake[1:] or snake[0][0] in (0, H) or snake[0][1] in (0, W) \
                or snake_1[0] in snake_1[1:] or snake_1[0][0] in (0, H) or snake_1[0][1] in (0, W):
            return

        eaten()
        w.addch(snake[0][0], snake[0][1], 'X', curses.color_pair(1))
        w.addch(snake_1[0][0], snake_1[0][1], 'X', curses.color_pair(3))
        w.getch()


def eaten():                                                                                                       # 检查食物状态
    global score, score_1
    if snake[0] == food[0]:                                                                                         # 判断是否吃掉食物
        temp = food.pop()
        w.addch(temp[0], temp[1], ' ')                                                                              # 把吃掉的食物打印為空
        if len(snake) < (H - 1) * (W - 1) - len(snake_1):                                                           # 判断是否走完
            while temp in snake or temp in snake_1:                                                                 # 隨機產生一個食物
                temp = [random.randint(1, H - 1), random.randint(1, W - 1)]
            food.insert(0, temp)
            w.addch(temp[0], temp[1], '$', curses.color_pair(2))                                                    # 打印顯示新食物
        score += 1                                                                                                  # 記錄分數
    else:
        tail = snake.pop()                                                                                          # 沒有吃到食物需要把尾巴去掉
        w.addch(tail[0], tail[1], ' ')

    if snake_1[0] == food[0]:                                                                                       # 判断是否吃掉食物
        temp = food.pop()
        w.addch(temp[0], temp[1], ' ')                                                                              # 把吃掉的食物打印為空
        if len(snake_1) < (H - 1) * (W - 1) - len(snake):                                                           # 判断是否走完
            while temp in snake_1 or temp in snake:                                                                 # 隨機產生一個食物
                temp = [random.randint(1, H - 1), random.randint(1, W - 1)]
            food.insert(0, temp)
            w.addch(temp[0], temp[1], '$', curses.color_pair(2))                                                    # 打印顯示新食物
        score_1 += 1                                                                                                # 記錄分數
    else:
        tail = snake_1.pop()                                                                                        # 沒有吃到食物需要把尾巴去掉
        w.addch(tail[0], tail[1], ' ')


def get_key():
    while True:
        getkey = w.getch()
        if getkey in (27, 97, 100, 115, 119, 258, 259, 260, 261):
            lock.acquire()
            K.append(getkey)
            lock.release()
        if getkey == 27:
            return


def main():
    try:                                                                                                                # 拦截程序内的错误
        initialize_windows()                                                                                            # 初始化窗口
        p = threading.Thread(target=played)
        lists.append(p)
        p = threading.Thread(target=get_key)
        lists.append(p)
        for i in lists:
            i.start()
        for i in lists:
            i.join()
        recover_windows()                                                                                               # 恢复默认窗口
        print(K)

    except Exception as E:
        recover_windows()
        print(E)
        print('Your Snake is death! \nScore:' + str(score))
        print('Your Snake_1 is death! \nScore:' + str(score_1))


if __name__ == '__main__':
    w, H, W, food, snake, snake_1, score, score_1, key, key_1, lists, K = object, 0, 0, [], [], [], 0, 0, 0, 0, [], []       # 定义全局变量和对象
    lock = threading.Lock
    main()
