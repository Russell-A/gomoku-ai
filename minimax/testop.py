import copy
import random
class test:
    def __init__(self):
        self.width = 20
        self.height = 20
pp = test()
MAX_BOARD = 20
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
# board[10][10] = 2
# board[10][9]=2
# board[3][5]=2
# board[3][4]=2
# board[3][2]=2
# board[1][3]=2
# board[1][4]=1
# board[2][3]=2
# board[4][1]=2
# board[4][2]=1
# board[5][1]=2
# board[5][2]=1
# board[3][5]=1
import copy
N = 2
score = [0, 100, -100]
import util as ut
ut.pp.width = pp.width
ut.pp.height = pp.height
min_or_max = ["max", "min"]
from Node import Node
StateDict = {}
IsExistKill = 0


def boardtolist(board):
    change = []
    for a in range(pp.width):
        for b in range(pp.height):
            if board[a][b] > 0:
                change.append((a, b, board[a][b]))
    return tuple(change)


def brain_turn():
    # if pp.terminateAI:
    #     return
    global IsExistKill
    alpha = float('-inf')
    beta = float('inf')
    boardtemp = copy.deepcopy([a[0:pp.width] for a in board[0:pp.height]])

    root = Node(next_cd=(-1, -1), who=2, boardNow=boardtemp)  ## 正常下棋
    rtnode = get_value(root, alpha, beta, 0)
    return rtnode.next_cd


def get_value(node, alpha, beta, iteration):
    # t = boardtolist(node.board)
    # if t in StateDict:
    #     node.value = StateDict[t]
    #     # print("have explored")
    #     return node

    end = ut.check_success(node.board, node.next_cd[0], node.next_cd[1], who=node.who)
    if (end) >= 0:
        node.value = score[end]
        return node

    if (iteration > N):  # 对棋盘评估
        return evaluate(node)

    if (iteration % 2 == 0):
        return max_value(node, alpha, beta, iteration)

    else:
        return min_value(node, alpha, beta, iteration)


def max_value(node, alpha, beta, iteration):
    value = float('-inf')
    successors = node.get_successors()  # 当前已是最新棋盘，据此来产生候选

    maxnode = node
    for i in successors:

        i.updateboard()  # 更新棋盘
        getnode = get_value(i, alpha, beta, iteration + 1)
        # StateDict[boardtolist(getnode.board)] = getnode.value
        i.restoreboard()  # 复原棋盘

        if getnode.value > value:
            value = getnode.value
            i.value = value
            maxnode = i

        if value > alpha:
            alpha = value
        if value >= beta:
            return maxnode
    return maxnode


def min_value(node, alpha, beta, iteration):
    value = float('inf')
    minnode = node
    successors = node.get_successors()
    for i in successors:

        i.updateboard()
        getnode = get_value(i, alpha, beta, iteration + 1)
        # StateDict[boardtolist(getnode.board)] = getnode.value
        i.restoreboard()

        if getnode.value < value:
            value = getnode.value
            i.value = value
            minnode = i

        if value < beta:
            beta = value
        if (value <= alpha):
            return minnode
    return minnode


def evaluate(node):
    # if node.who == 1:
    #     mylive2 = len(node.threat.my_attack)
    #     mylive3 = len(node.threat.my_threat)
    #     mylive4 = 0
    #     for i in node.threat.my_threat:
    #         if i[0] == 5:
    #             mylive4 += 1
    #     oplive2 = len(node.threat.op_attack)
    #     oplive3 = len(node.threat.op_threat)
    #     oplive4 = 0
    #     for i in node.threat.op_threat:
    #         if i[0] == 5:
    #             oplive4 += 1
    # else:
    #     oplive2 = len(node.threat.my_attack)
    #     oplive3 = len(node.threat.my_threat)
    #     oplive4 = 0
    #     for i in node.threat.my_threat:
    #         if i[0] == 5:
    #             oplive4 += 1
    #     mylive2 = len(node.threat.op_attack)
    #     mylive3 = len(node.threat.op_threat)
    #     mylive4 = 0
    #     for i in node.threat.op_threat:
    #         if i[0] == 5:
    #             mylive4 += 1
    #
    #
    # t = N % 2
    # node.value = (mylive2 - oplive2) * 2 + (mylive4 - oplive4) * 50 + mylive3 * 2 + max(mylive3 - 1, 0) * 20 - 50 * oplive3
    node.value = ut.two_connnect(node.board)
    return node
