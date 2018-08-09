#! usr/bin/env python
# coding = utf-8
# Author = 0Villian0
# Date = 7|4|2018
# Versions = 2.0

"""贪吃蛇AI逻辑思路参考文章：http://www.hawstein.com/posts/snake-ai.html（如何用python写一个AI贪吃蛇！）
    A* 寻路算法参考文章：https://www.aliyun.com/jiaocheng/510034.html
"""

import curses
import random
import time
import copy


def initialize_windows():
    global w, H, W, food, snake, score, key
    w = curses.initscr()                                                                                                # initialize the Windows
    curses.start_color()                                                                                                # 开启颜色显示
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)                                                           # 自定义颜色方案组
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.curs_set(0)                                                                                                  # 关闭光标显示
    curses.cbreak()                                                                                                     # 开启cbreak模式，键盘输入立即执行，而不是缓冲输入模式那样等待回车后才执行
    curses.noecho()                                                                                                     # 关闭键盘输入屏幕回显
    w.keypad(True)                                                                                                      # 开启特殊键位输入处理功能 如：上下左右键等
    w.timeout(1)                                                                                                        # 设置读取键盘输入等待时间 单位：毫秒
    H, W = w.getmaxyx()                                                                                                 # 获取w窗口的长宽
    H, W = 11, 11                                                                                                       # 把窗口设为固定值 调试用
    food = [[int(H / 2), int(W * 6 / 10)]]                                                                              # initialize the position of food
    w.addch(food[0][0], food[0][1], '$', curses.color_pair(2))                                                          # 在窗口中的坐标点使用颜色组2打印字符
    snake = [[int(H / 2), int(W * 2 / 10)], [int(H / 2), int(W * 2 / 10) - 1]]                                          # initialize the position of snake
    w.addch(snake[0][0], snake[0][1], 'X', curses.color_pair(1))
    w.addch(snake[1][0], snake[1][1], 'X', curses.color_pair(3))
    score = 0                                                                                                           # 分数值
    key = curses.KEY_RIGHT                                                                                              # 运动方向键值


def recover_windows():                                                                                                  # 恢复原始窗口设置，退出
    # global w                                                                                                          # 错误点：python中列表、字典、对象是明确的，不需要显式的声明global
    w.keypad(False)
    curses.echo()
    curses.nocbreak()
    curses.endwin()


def player():                                                                                                           # 玩家操控贪吃蛇
    global key
    while True:
        next_key = w.getch()                                                                                            # 获取下一个方向键
        if next_key == 27:                                                                                              # 按下Esc鍵或者發生error則恢復窗口後退出
            recover_windows()
            print('QUIT GAME! \nScore:' + str(score))
            return

        if next_key == curses.KEY_RIGHT and key != curses.KEY_LEFT \
                or next_key == curses.KEY_LEFT and key != curses.KEY_RIGHT \
                or next_key == curses.KEY_UP and key != curses.KEY_DOWN \
                or next_key == curses.KEY_DOWN and key != curses.KEY_UP:
            key = next_key                                                                                              # 获取有效的运动方向键

        temp = snake[0]                                                                                                 # 更新蛇头位置
        if key == curses.KEY_UP:
            snake.insert(0, [temp[0] - 1, temp[1]])
        if key == curses.KEY_DOWN:
            snake.insert(0, [temp[0] + 1, temp[1]])
        if key == curses.KEY_RIGHT:
            snake.insert(0, [temp[0], temp[1] + 1])
        if key == curses.KEY_LEFT:
            snake.insert(0, [temp[0], temp[1] - 1])

        if snake[0] in snake[1:] or snake[0][0] in (0, H) or snake[0][1] in (0, W):                                     # 判断蛇是否死亡,是则恢复默认窗口退出
            recover_windows()
            print('Your Snake is death! \nScore:' + str(score))
            return

        eaten()
        w.addch(snake[0][0], snake[0][1], 'X', curses.color_pair(1))


def eaten():                                                                                                            # 检查食物状态
    global score
    if snake[0] == food[0]:                                                                                             # 判断是否吃掉食物
        temp = food.pop()
        w.addch(temp[0], temp[1], ' ')                                                                                  # 把吃掉的食物打印為空
        if len(snake) < (H - 1) * (W - 1):                                                                              # 判断是否走完
            while temp in snake:                                                                                        # 隨機產生一個食物
                temp = [random.randint(1, H - 1), random.randint(1, W - 1)]
            food.insert(0, temp)
            w.addch(temp[0], temp[1], '$', curses.color_pair(2))                                                        # 打印顯示新食物
        score += 1                                                                                                      # 記錄分數
    else:
        tail = snake.pop()                                                                                              # 沒有吃到食物需要把尾巴去掉
        w.addch(tail[0], tail[1], ' ')


class Node(object):
    """节点类
            parent:当前节点的父节点
            r,c:当前节点的行,列坐标
            f: 当前点到起点,当前点到终点的总消耗(距离)
            g:当前点到起点的距离
            hn: 当前点到终点的距离
    """
    def __init__(self, parent, r, c, f, g, hn):
        self.parent = parent
        self.xrow = r
        self.ycol = c
        self.f = f
        self.g = g
        self.hn = hn


class AStar(object):
    """A星算法实现类
            sr,sc:起点的行,列
            er,ec:目标点得行列
            block_xrow,block_ycol:地图格子总的行和列
            open,close,path:寻路中的开启,关闭,路径列表
            snakes :贪吃蛇列表
    """
    def __init__(self, sc, sr, ec, er, block_xrow, block_ycol, snakes):
        self.starxrow = sr
        self.starycol = sc
        self.endxrow = er
        self.endycol = ec
        self.totalxrow = block_xrow
        self.totalycol = block_ycol
        self.open = []
        self.close = []
        self.path = []
        self.snake = snakes

    def find_path(self, length='short'):
        starnode = Node(None, self.starxrow, self.starycol, 0, 0, 0)                                                    # 生成开始节点，父节点为None
        self.close.append(starnode)
        while True:
            self.extend_node(starnode, length)                                                                          # 扩展当前节点的四周节点
            if not self.open:                                                                                           # 判断开放列表是否为空，是则没有找到路径退出
                return []
            self.open.sort(key=lambda x: x.f)                                                                           # 对开放列表按照F值进行排序
            if length == 'short':
                starnode = self.open[0]                                                                                 # 参数为short时获取最短路径即获取F值最小的节点
            elif length == 'long':                                                                                      # 参数为long时获取最长路径即获取F值最大的节点
                starnode = self.open[-1]
            if self.judge_to_target(starnode):                                                                          # 判断是否为终点
                self.get_path(starnode)                                                                                 # 抵达终点则根据父节点回溯路径
                return self.path
            self.close.append(starnode)                                                                                 # 将当前节点加入关闭列表后删除
            if length == 'short':                                                                                       # 求最短路径
                del self.open[0]
            elif length == 'long':                                                                                      # 求最长路径
                del self.open[-1]

    def extend_node(self, node, length):
        xs = (0, 1, -1, 0)
        ys = (1, 0, 0, -1)                                                                                              # 下右左上四个方向
        i = 0
        for row, col in zip(xs, ys):
            new_row = node.xrow + row
            new_col = node.ycol + col                                                                                   # 遍历四个方向扩展新节点坐标
            i += 1
            g = node.g + 1                                                                                              # 新节点到起点间的距离
            hn = self.get_cur_to_end(new_row, new_col)                                                                  # 新节点到终点间的距离
            f = g + hn                                                                                                  # 总消耗
            if not self.judge_usable(new_row, new_col):                                                                 # 判断新坐标点是否可用
                continue
            new_node = Node(node, new_row, new_col, f, g, hn)                                                           # 新坐标点可用则生成新节点
            if self.judge_node_in_close(new_node):                                                                      # 如果新节点在关闭列表中则忽略
                continue
            i = self.judge_node_in_open(new_node)
            if i == -1:                                                                                                 # 不在开放列表中则添加进去
                self.open.append(new_node)
            else:                                                                                                       # 已经在开放列表中如果新的G值更低,那就把相邻方格的父节点改为目前选中的方格,对应的H,G也跟着变化
                if length == 'short' and self.open[i].g > new_node.g:                                                   # 参数length为short，则求最短路径
                    self.open[i] = new_node
                elif length == 'long' and self.open[i].g < new_node.g:                                                  # 参数length为long，则求最长路径
                    self.open[i] = new_node
                else:
                    continue

    def get_cur_to_end(self, sr, sc):
        """曼哈顿方法求当前节点到终点的距离(消耗) 概率方法
           曼哈顿方法:它计算从当前格到目的格之间水平和垂直的方格的数量总和,忽略对角线方向。然后把结果乘以1
        """
        r = abs(self.endxrow - sr)
        c = abs(self.endycol - sc)
        return (r + c)*1

    def judge_usable(self, nr, nc):
        if self.totalxrow > nr > 0 and self.totalycol > nc > 0 and [nc, nr] not in self.snake:                          # 新坐标点不能超出边框和和蛇身重叠
            return True
        return False

    def judge_node_in_close(self, node):
        for n in self.close:
            if n.xrow == node.xrow and n.ycol == node.ycol:                                                             # 判断新节点是否在关闭列表中
                return True
        return False

    def judge_node_in_open(self, node):
        for i, n in enumerate(self.open):                                                                               # enumerate返回迭代器的元素下标与元素
            if n.xrow == node.xrow and n.ycol == node.ycol:                                                             # 如果新节点在开启列表中则返回此时的下标,不存在返回-1
                return i
        return -1

    def judge_to_target(self, node):
        return node.xrow == self.endxrow and node.ycol == self.endycol                                                  # 判断是否到达终点

    def get_path(self, node):
        while node:                                                                                                     # 从结束点开始回溯到开始节点,开始点的parent == None,获得正确的路径
            self.path.append([node.ycol, node.xrow])
            node = node.parent


def ai():
    while True:
        path = find_path()
        if not path:                                                                                                    # path为空则找不到路径，退出
            time.sleep(8)
            recover_windows()
            print('You can not find a viable path！')
            return False
        # for n in path:
        snake.insert(0, path[0])
        eaten()
        if len(snake) == (H - 1)*(W - 1):                                                                               # 贪吃蛇铺满地图，胜利，退出
            w.addch(snake[0][0], snake[0][1], 'X', curses.color_pair(1))
            w.addch(snake[1][0], snake[1][1], 'X', curses.color_pair(3))
            w.getch()
            return True
        w.addch(snake[0][0], snake[0][1], 'X', curses.color_pair(1))
        w.addch(snake[1][0], snake[1][1], 'X', curses.color_pair(3))
        w.addch(snake[-1][0], snake[-1][1], 'X', curses.color_pair(2))
        if w.getch() == 27:                                                                                             # 错误点：getch应该放在addch方法的后面  等待键盘输入，刷新屏幕打印输出
            return


def find_path():
    # global path
    a_star = AStar(snake[0][0], snake[0][1], food[0][0], food[0][1], W, H, snake)                                       # 生成A*算法类实例对象
    path = a_star.find_path()[-2::-1]                                                                                   # 使用算法实例方法寻找最短路径
    if path:                                                                                                            # 判断蛇和食物之间是否有路径
        if judge_virtual_snake_safe(path):                                                                              # 判断虚拟蛇吃完之后，蛇头和蛇尾之间是否有路径
            return path                                                                                                 # 如果是则返回最短路径，让真蛇去吃
        temp_path = follow_tail(snake, 'long')
        if temp_path:                                                                                                   # 判断真蛇是否可以追着蛇尾跑，可以则返回最长路径
            return temp_path
        else:
            return random_move()                                                                                        # 蛇和食物之间有路径，但是不安全而且真蛇也不能追蛇尾跑则返回随机一步
    temp_path = follow_tail(snake, 'long')
    if temp_path:                                                                                                       # 蛇和食物之间没有路径，则判断真蛇是否可以追着蛇尾跑，可以则返回最长路径
        return temp_path
    else:
        return random_move()                                                                                            # 如果蛇和食物丶蛇尾之间都没有路径则返回随机一步


def judge_virtual_snake_safe(p):
    v_snake = virtual_snake(p)                                                                                          # 派出虚拟蛇去吃食物
    if len(v_snake) == (H - 1)*(W - 1):                                                                                 # 如果虚拟蛇吃完后铺满整张地图则直接返回True让真蛇去吃
        return True
    if follow_tail(v_snake, 'long'):                                                                                    # 判断虚拟蛇吃掉食物后是否可以追着蛇尾
        if v_snake[0][0] + 1 == v_snake[-1][0] or v_snake[0][0] - 1 == v_snake[-1][0] \
                or v_snake[0][1] + 1 == v_snake[-1][1] or v_snake[0][1] - 1 == v_snake[-1][1]:                          # 如果蛇头和蛇尾紧挨着，则返回False即不能follow_tail，追着蛇尾运动了
            return False
        return True


def virtual_snake(p):
    v_snake = copy.deepcopy(snake)                                                                                      # 错误点：此处如果v_snake = snake 两个会指向同一个地址 而v_snake = snake[:]是浅拷贝
    for i in p:
        v_snake.insert(0, i)                                                                                            # 把路径path添加到虚拟蛇v_snake里
    v_snake = v_snake[:(len(snake) + 1)]                                                                                # 只有吃掉食物才增加一个蛇身
    return v_snake


def follow_tail(s, length='short'):
    temp_snake = copy.deepcopy(s)
    tail = temp_snake.pop()                                                                                             # 把贪吃蛇的尾巴作为食物
    temp_a_star = AStar(temp_snake[0][0], temp_snake[0][1], tail[0], tail[1], W, H, temp_snake)                         # 生成临时A*算法实例
    temp_path = temp_a_star.find_path(length)[-2::-1]                                                                   # 寻找蛇头蛇尾之间的最长路径
    return temp_path


def random_move():
    head = snake[0]
    temp = [[head[0] - 1, head[1]], [head[0] + 1, head[1]], [head[0], head[1] - 1], [head[0], head[1] + 1]]             # 蛇头的上下左右四点
    for i in temp:
        if H > i[0] > 0 and W > i[1] > 0 and i not in snake:                                                            # 把上下左右不符合的点移除
            pass
        else:
            temp.remove(i)
    if temp:                                                                                                            # 不为空则返回随机选择的一点
        return [random.choice(temp)]
    return temp                                                                                                         # 空则返回False


def main():
    try:                                                                                                                # 拦截程序内的错误
        initialize_windows()                                                                                            # 初始化窗口
        # player()                                                                                                      # 玩家模式
        ai()                                                                                                            # AI模式
        time.sleep(5)
        recover_windows()                                                                                               # 恢复默认窗口

    except Exception as E:
        recover_windows()
        print(E)

    finally:
        print(score)                                                                                                    # 输出分数丶贪吃蛇列表和食物列表
        print(snake)
        print(food)


if __name__ == '__main__':
    w, H, W, food, snake, score, key = object, 0, 0, [], [], 0, 0                                                       # 定义全局变量和对象
    main()
    # initialize_windows()
    # ai()
