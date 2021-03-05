import pisqpipe as pp

# class test:
#     def __init__(self):
#         self.width = 10
#         self.height = 10
# pp = test()

def Free(x, y, board):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0

def takefirst(x):
    return x[0]
def take2(x):
    return x[1]
def take3(x):
    return x[2]

branch = 3
from Node import Node

branch_attack = 2
def get_attack(node, unsorted=True, branch_attack = branch_attack):   # 选取进攻的点位
    successor = node.threat.get_attack(3-node.who)
    if unsorted is True:
        return successor
    else:
        mark = []
        orgwho = node.who
        nextwho = 3-node.who
        for state in successor:
            # newnode = Node(next_cd=state, who=nextwho, boardNow=node.board, hashboard=node.hasboard)
            newnode = Node.copy_next(node, state)
            newnode.evaluate()
            a = newnode.value
            mark.append((a,newnode))
        if nextwho == 2:
            mark.sort(key=takefirst, reverse=False)
        else:
            mark.sort(key=takefirst, reverse=True)
        successorsort = []
        t = min(len(mark), branch_attack)
        for i in range(t):
            successorsort.append(mark[i][1])
        return successorsort


def get_successor(node, unsorted=True):
    board = node.board
    successor = []
    t = 0
    for i in range(pp.width):
        for j in range(pp.height):
            if board[i][j] != 0:
                t = 1
                for delta_i in range(-2, 3):
                    for delta_j in range(-2, 3):
                        if 0 <= i + delta_i < pp.width and 0 <= j + delta_j < pp.height and board[i + delta_i][
                            j + delta_j] == 0 and (i + delta_i, j + delta_j) not in successor:
                            if delta_i ^ 2 + delta_j ^ 2 > 2:
                                successor.append((i + delta_i, j + delta_j))
                            else:
                                successor.insert(0, (i + delta_i, j + delta_j))
                        # if 0 <= i + delta_i < pp.width and 0 <= j + delta_j < pp.height and board[i + delta_i][
                        #     j + delta_j] == 0 and (i + delta_i, j + delta_j) not in successor :
                        #     successor.append((i + delta_i, j + delta_j))
    if t == 0:
        successor.append((pp.width // 2, pp.height // 2))
    if unsorted is True:
        succ_node = []
        for s in successor:
            # succ_node.append(Node(next_cd=s, who=3 - node.who, boardNow=node.board, hashboard=node.hasboard))
            succ_node.append(Node.copy_next(node, s))

        return succ_node
    else:
        mark = []
        orgwho = node.who
        nextwho = 3-node.who
        for state in successor:
            # newnode = Node(next_cd=state, who=nextwho, boardNow=node.board, hashboard=node.hasboard)
            newnode = Node.copy_next(node = node, next_cd=state)
            newnode.evaluate(0)
            a = newnode.value

            # newnode.evaluate(1)
            # b = newnode.value
            #
            # newnode.evaluate(2)
            # c = newnode.value

            mark.append((a,newnode))

        successorsort = []
        cd_set = set()

        if nextwho == 2:
            mark.sort(key=takefirst, reverse=False)
        else:
            mark.sort(key=takefirst, reverse=True)
        t = min(len(mark), int(branch))
        for i in range(t):
            if mark[i][1].next_cd not in cd_set:
                cd_set.add(mark[i][1].next_cd)
                successorsort.append(mark[i][1])

        # if nextwho == 2:
        #     mark.sort(key=take2, reverse=False)
        # else:
        #     mark.sort(key=take2, reverse=True)
        # t = min(len(mark), int(branch/2))
        # for i in range(t):
        #     if mark[i][3].next_cd not in cd_set:
        #         cd_set.add(mark[i][3].next_cd)
        #         successorsort.append(mark[i][3])
        #
        # if nextwho == 2:
        #     mark.sort(key=take3, reverse=False)
        # else:
        #     mark.sort(key=take3, reverse=True)
        # t = min(len(mark), int(branch/2))
        # for i in range(t):
        #     if mark[i][3].next_cd not in cd_set:
        #         cd_set.add(mark[i][3].next_cd)
        #         successorsort.append(mark[i][3])
        # print(len(successorsort))

        return successorsort
    # mark = []
    # result = [0, 100, -100, 0]
    # if min_or_max == 'MIN':
    #     for state in successor:
    #         board[state[0]][state[1]] = 2
    #         ''' 2020/12/03 9:48'''
    #         threatboard = threat(board)
    #         if len(threatboard.opponent) >= 2:
    #             return [state]
    #         ''' 2020/12/03 9:48'''
    #         a = two_connnect(board, state[0], state[1])
    #         a += result[check_success(board, state[0], state[1])]
    #         mark.append((a, state))
    #         board[state[0]][state[1]] = 0
    #     mark.sort(key=takefirst, reverse=False)
    # else:
    #     for state in successor:
    #         board[state[0]][state[1]] = 1
    #         ''' 2020/12/03 9:48'''
    #         threatboard = threat(board)
    #         if len(threatboard.mine) >= 2:
    #             return [state]
    #         ''' 2020/12/03 9:48'''
    #         a = two_connnect(board)
    #         a += result[check_success(board, state[0], state[1])]
    #         mark.append((a, state))
    #         board[state[0]][state[1]] = 0
    #     mark.sort(key=takefirst, reverse=True)
    # successorsort = []
    # t = min(len(mark), branch)
    # for i in range(t):
    #     successorsort.append(mark[i][1])
    # return successorsort

def get_successors_mcts(board,who,  max_successors, unsorted=True):
    successor = []
    t = 0
    pp.width=pp.height=20
    for i in range(pp.width):
        for j in range(pp.height):
            if board[i][j] != 0:
                t = 1
                for delta_i in range(-2, 3):
                    for delta_j in range(-2, 3):
                        if 0 <= i + delta_i < pp.width and 0 <= j + delta_j < pp.height and board[i + delta_i][
                            j + delta_j] == 0 and (i + delta_i, j + delta_j) not in successor:
                            if delta_i ^ 2 + delta_j ^ 2 > 2:
                                successor.append((i + delta_i, j + delta_j))
                            else:
                                successor.insert(0, (i + delta_i, j + delta_j))
                        # if 0 <= i + delta_i < pp.width and 0 <= j + delta_j < pp.height and board[i + delta_i][
                        #     j + delta_j] == 0 and (i + delta_i, j + delta_j) not in successor :
                        #     successor.append((i + delta_i, j + delta_j))
    if t == 0:
        successor.append((pp.width // 2, pp.height // 2))
    if unsorted is True:
        # succ_node = []
        # for s in successor:
        #     succ_node.append(Node(next_cd=s, who=3 - who, boardNow=board))

        return successor
    else:
        mark = []
        orgwho = who
        nextwho = 3 - who
        for state in successor:
            newnode = Node(next_cd=state, who=nextwho, boardNow=board)
            newnode.evaluate()
            a = newnode.value

            newnode.evaluate(1)
            b = newnode.value

            newnode.evaluate(2)
            c = newnode.value

            mark.append((a, b, c, newnode))

        successorsort = []
        cd_set = set()

        if nextwho == 2:
            mark.sort(key=takefirst, reverse=False)
        else:
            mark.sort(key=takefirst, reverse=True)
        t = min(len(mark), int(max_successors))
        for i in range(t):
            if mark[i][3].next_cd not in cd_set:
                cd_set.add(mark[i][3].next_cd)
                successorsort.append(mark[i][3].next_cd)
        return successorsort



def ck_success(node):
    return node.threat.end


def check_success(board, x, y, who = 1):
    if (x == -1):
        return -1
    changed = 0
    if board[x][y] == 0:
        board[x][y] = who
        changed = 1
    # if changed == 1:
    #     board[x][y] = 0
    for i in range(x - 4, x + 5):  # 横向有没有出现5连（在边缘依次逐一遍历，是否五个棋子的类型一样）
        if i >= 0 and i + 4 < pp.width:
            if board[i][y] != 0 and \
                    board[i + 1][y] == board[i][y] and \
                    board[i + 2][y] == board[i][y] and \
                    board[i + 3][y] == board[i][y] and \
                    board[i + 4][y] == board[i][y]:
                if changed == 1:
                    board[x][y] = 0
                return board[i][y]

    for j in range(y - 4, y + 5):  # 纵向有没有出现5连（在边缘依次逐一遍历，是否五个棋子的类型一样）
        if j >= 0 and j + 4 < pp.height:
            if board[x][j] != 0 and \
                    board[x][j + 1] == board[x][j] and \
                    board[x][j + 2] == board[x][j] and \
                    board[x][j + 3] == board[x][j] and \
                    board[x][j + 4] == board[x][j]:
                if changed == 1:
                    board[x][y] = 0
                return board[x][j]

    # 先判断东北方向的对角下输赢 x 列轴， y是行轴 ， i 是行 j 是列（右斜向）（在边缘依次逐一遍历，是否五个棋子的类型一样）
    for j, i in zip(range(x + 4, x - 5, -1), range(y - 4, y + 5)):
        if j - 4 >= 0 and j < pp.width and i >= 0 and i + 4 < pp.height:
            if board[j][i] != 0 and \
                    board[j - 1][i + 1] == board[j][i] and \
                    board[j - 2][i + 2] == board[j][i] and \
                    board[j - 3][i + 3] == board[j][i] and \
                    board[j - 4][i + 4] == board[j][i]:
                if changed == 1:
                    board[x][y] = 0
                return board[j][i]

    # 2、判断西北方向的对角下输赢 x 列轴， y是行轴 ， i 是行 j 是列（左斜向）（在边缘依次逐一遍历，是否五个棋子的类型一样）
    for j, i in zip(range(x - 4, x + 5), range(y - 4, y + 5)):
        if j >= 0 and j + 4 < pp.width and i >= 0 and i + 4 < pp.height:
            if board[j][i] != 0 and \
                    board[j + 1][i + 1] == board[j][i] and \
                    board[j + 2][i + 2] == board[j][i] and \
                    board[j + 3][i + 3] == board[j][i] and \
                    board[j + 4][i + 4] == board[j][i]:
                if changed == 1:
                    board[x][y] = 0
                return board[j][i]
    # 检查是否未结束
    for i in range(pp.width):
        for j in range(pp.height):
            if board[i][j] == 0:
                if changed == 1:
                    board[x][y] = 0
                return -1
    if changed == 1:
        board[x][y] = 0
    return 0


def two_connnect(board):
    over = [0, 100, -100, 0]
    two = [0, 0]
    jump = [0, 0]
    twojump = [0, 0]
    for i in range(1, pp.height - 2):
        for j in range(1, pp.width - 2):
            me = board[i][j]
            if me == 0:
                continue
            op = 3 - me
            if i + 2 < pp.width and i - 1 >= 0 and board[i + 1][j] == me and board[i + 2][j] != op and board[i - 1][
                j] != op:
                two[me - 1] += 1
            if i + 3 < pp.width and i - 1 >= 0 and board[i + 2][j] == me and board[i + 1][j] != op and board[i + 3][
                j] != op and board[i - 1][j] != op:
                jump[me - 1] += 1
            if j + 2 < pp.height and j - 1 >= 0 and board[i][j + 1] == me and board[i][j + 2] != op and board[i][
                j - 1] != op:
                two[me - 1] += 1
            if j + 3 < pp.height and j - 1 >= 0 and board[i][j + 2] == me and board[i][j + 1] != op and board[i][
                j + 3] != op and board[i][j - 1] != op:
                jump[me - 1] += 1
            if j + 2 < pp.height and j - 1 >= 0 and i + 2 < pp.width and i - 1 >= 0 and board[i + 1][j + 1] == me and \
                    board[i + 2][j + 2] != op and board[i - 1][j - 1] != op:
                two[me - 1] += 1
            if j + 1 < pp.height and j - 2 >= 0 and i + 2 < pp.width and i - 1 >= 0 and board[i + 1][j - 1] == me and \
                    board[i + 2][j - 2] != op and board[i - 1][j + 1] != op:
                two[me - 1] += 1
            if j + 3 < pp.height and j - 1 >= 0 and i + 3 < pp.width and i - 1 >= 0 and board[i + 2][j + 2] == me and \
                    board[i + 1][j + 1] != op and board[i + 3][j + 3] != op and board[i - 1][j - 1] != op:
                jump[me - 1] += 1
            if j + 1 < pp.height and j - 3 >= 0 and i + 3 < pp.width and i - 1 >= 0 and board[i + 2][j - 2] == me and \
                    board[i + 1][j - 1] != op and board[i + 3][j - 3] != op and board[i - 1][j + 1] != op:
                jump[me - 1] += 1
    result = (two[0] - two[1]) * 2 + (jump[0] - jump[1]) * 1.5
    return result


    # def evaluate(self):
    #     mylive2 = 0
    #     mysleep3 = 0
    #     mylive3 = 0
    #     mysleep4 = 0
    #     mylive4 = 0
    #     oplive2 = 0
    #     opsleep3 = 0
    #     oplive3 = 0
    #     opsleep4 = 0
    #     oplive4 = 0
    #
    #     mylevel = 0
    #     oplevel = 0
    #
    #     if self.who == 1:
    #         if len(self.threat.my_threat) > 0:
    #             mylevel = max([a[0] for a in self.threat.my_threat])
    #         if len(self.threat.op_threat) > 0:
    #             oplevel = max([a[0] for a in self.threat.op_threat])
    #
    #         for i in self.threat.my_attack:
    #             if i[0] == 1:
    #                 mylive2 += 1
    #             if i[0] == 2:
    #                 mysleep3 += 1
    #         for i in self.threat.my_threat:
    #             if i[0] == 3:
    #                 mylive3 += 1
    #             if i[0] == 4:
    #                 mysleep4 += 1
    #             if i[0] == 5:
    #                 mylive4 += 1
    #
    #         for i in self.threat.op_attack:
    #             if i[0] == 1:
    #                 oplive2 += 1
    #             if i[0] == 2:
    #                 opsleep3 += 1
    #         for i in self.threat.op_threat:
    #             if i[0] == 3:
    #                 oplive3 += 1
    #             if i[0] == 4:
    #                 opsleep4 += 1
    #             if i[0] == 5:
    #                 oplive4 += 1
    #     else:
    #         if len(self.threat.my_threat) > 0:
    #             oplevel = max([a[0] for a in self.threat.my_threat])
    #         if len(self.threat.op_threat) > 0:
    #             mylevel = max([a[0] for a in self.threat.op_threat])
    #         for i in self.threat.op_attack:
    #             if i[0] == 1:
    #                 mylive2 += 1
    #             if i[0] == 2:
    #                 mysleep3 += 1
    #         for i in self.threat.op_threat:
    #             if i[0] == 3:
    #                 mylive3 += 1
    #             if i[0] == 4:
    #                 mysleep4 += 1
    #             if i[0] == 5:
    #                 mylive4 += 1
    #
    #         for i in self.threat.my_attack:
    #             if i[0] == 1:
    #                 oplive2 += 1
    #             if i[0] == 2:
    #                 opsleep3 += 1
    #         for i in self.threat.my_threat:
    #             if i[0] == 3:
    #                 oplive3 += 1
    #             if i[0] == 4:
    #                 opsleep4 += 1
    #             if i[0] == 5:
    #                 oplive4 += 1
    #     punish = 0
    #     if (mylevel <= oplevel and oplevel > 0) or oplevel >= 4:
    #         punish = 1
    #
    #     self.value = (mylive2 - 1.5*oplive2) * 2 + (mysleep3 - 1.5*opsleep3) * 3 - punish*50 + max(mylive4+mylive3+mysleep4-1, 0)*20 + mylive4*40 \
    #                  + 2*(mylive3+mysleep4)*max(mysleep3+mylive2,0)
    #
    #     # self.value = (mylive2 - oplive2) * 2 + (mylive4 - 2*oplive4) * 30 - mylive3 * 1 + max(mylive3 - 1,0) * 20 - 20 * oplive3 - oplive2*2 + (mysleep3-opsleep3)
    #     # self.value = (mylive2 - oplive2) * 2+(mysleep3-opsleep3) - oplive2-opsleep3
    #     if self.who == 2:
    #         self.value = -self.value
    #     # self.value = (mylive2+mysleep3)*2 - (oplive2+opsleep3)*8
    #     # self.value = (mylive2 - oplive2) * 2