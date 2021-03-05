import random
import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG

pp.infotext = 'name="pbrain-pyrandom", author="Jan Stransky", version="1.0", country="Czech Republic", www="https://github.com/stranskyjan/pbrain-pyrandom"'

MAX_BOARD = 100
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]


score = [0, 1000, -1000]
def brain_init():
    if pp.width < 5 or pp.height < 5:
        pp.pipeOut("ERROR size of the board")
        return
    if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
        pp.pipeOut("ERROR Maximal board size is {}".format(MAX_BOARD))
        return
    pp.pipeOut("OK")


def brain_restart():
    global IsExistKill
    IsExistKill = 0
    global Kill_dict
    Kill_dict = {}
    global StateDict
    StateDict = {}
    for x in range(pp.width):
        for y in range(pp.height):
            board[x][y] = 0
    pp.pipeOut("OK")


def isFree(x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0


def brain_my(x, y):
    if isFree(x, y):
        board[x][y] = 1
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    if isFree(x, y):
        board[x][y] = 2
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))


def brain_block(x, y):
    if isFree(x, y):
        board[x][y] = 3
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))


def brain_takeback(x, y):
    if x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] != 0:
        board[x][y] = 0
        return 0
    return 2


IsExistKill = 0
Kill_dict = {}
import Data as dt
import hash
dt._init()
dt.set_glo('glo_hash', hash.hash(20,20))
import copy
import util as ut
ut.pp.width = pp.width
ut.pp.height = pp.height
min_or_max = ["max", "min"]
from Node import Node

StateDict = {}
N = 5

board_old = [[0 for _ in range(20)] for _ in range(20)]

def brain_turn():


    global IsExistKill
    global Kill_dict
    global StateDict
    StateDict = {}
    if pp.terminateAI:
        return
    i = 0
    while True:
        alpha = float('-inf')
        beta = float('inf')
        boardtemp = copy.deepcopy([a[0:pp.width] for a in board[0:pp.height]])
        hashboard = hash.create_hashboard(dt.get_glo('glo_hash'), boardtemp, pp.width, pp.height)
        if IsExistKill == 1:  # 若存在连续杀棋则从字典里找要下哪步，若该点不在字典里则说明对方没有堵
            li = hashboard
            if li in Kill_dict:
                # logDebug("find kill in dict")
                cd = Kill_dict[li][1]
                x = cd[0]
                y = cd[1]
            else:
                StateDict = {}
                root = Node(next_cd=(-1, -1), who=2, boardNow=boardtemp, hashboard=hashboard)
                rtnode = get_value(root, alpha, beta, 0)
                x = rtnode.next_cd[0]
                y = rtnode.next_cd[1]

        else:
            root = Node(next_cd=(-1, -1), who=2, boardNow=boardtemp, hashboard=hashboard)  ## 寻找杀棋
            rtnode,dic = root.check_kill_chess(1)
            if (rtnode.value) == 100:
                # logDebug("find kill")
                IsExistKill = 1
                Kill_dict = copy.deepcopy(dic)
                pass
            else:
                oproot = Node(next_cd=(-1, -1), who=1, boardNow=boardtemp, hashboard=hashboard) ## 如果对面有杀棋则堵
                if len(oproot.threat.get_successor(1))==0:
                    opnode, _ = oproot.check_kill_chess(2, 2)
                    if (opnode.value == 100):
                        rtnode = opnode
                # if (1 == 0):
                #     pass
                    else:
                        StateDict = {}
                        root = Node(next_cd=(-1, -1), who=2, boardNow=boardtemp, hashboard=hashboard)  ## 正常下棋
                        rtnode = get_value(root, alpha, beta, 0)
            x = rtnode.next_cd[0]
            y = rtnode.next_cd[1]

        # logDebug(str(x))
        i += 1
        if pp.terminateAI:
            return
        if isFree(x, y):
            break
    if i > 1:
        pp.pipeOut("DEBUG {} coordinates didn't hit an empty field".format(i))
    pp.do_mymove(int(x), int(y))


def get_value(node, alpha, beta, iteration):

    # end = ut.check_success(node.board, node.next_cd[0], node.next_cd[1], who=node.who)
    end = ut.ck_success(node)
    if (end)>=0:
        node.value = score[end]
        return node

    if (iteration > N):  # 对棋盘评估
        node.evaluate()
        return node

    if (iteration % 2 == 0):
        return max_value(node, alpha, beta, iteration)

    else:
        return min_value(node, alpha, beta, iteration)

def max_value(node, alpha, beta, iteration):

    value = float('-inf')
    successors = node.get_successors() # 当前已是最新棋盘，据此来产生候选
    maxnode = 0
    for i in successors:

        i.updateboard()   #更新棋盘
        if i.hasboard not in StateDict:
            getnode = get_value(i, alpha, beta, iteration + 1)
            # StateDict[boardtolist(getnode.board)] = getnode.value
            StateDict[i.hasboard] = getnode.value
        else:
            getnode = i
            getnode.value = StateDict[i.hasboard]
        i.restoreboard()  #复原棋盘

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
    minnode = 0
    successors = node.get_successors()
    for i in successors:

        i.updateboard()
        if i.hasboard not in StateDict:
            getnode = get_value(i, alpha, beta, iteration + 1)
            # StateDict[boardtolist(getnode.board)] = getnode.value
            StateDict[i.hasboard] = getnode.value
        else:
            getnode = i
            getnode.value = StateDict[i.hasboard]
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



def brain_end():
    pass


def brain_about():
    pp.pipeOut(pp.infotext)


if DEBUG_EVAL:
    import win32gui


    def brain_eval(x, y):
        # TODO check if it works as expected
        wnd = win32gui.GetForegroundWindow()
        dc = win32gui.GetDC(wnd)
        rc = win32gui.GetClientRect(wnd)
        c = str(board[x][y])
        win32gui.ExtTextOut(dc, rc[2] - 15, 3, 0, None, c, ())
        win32gui.ReleaseDC(wnd, dc)

######################################################################
# A possible way how to debug brains.
# To test it, just "uncomment" it (delete enclosing """)
######################################################################
"""
# define a file for logging ...
DEBUG_LOGFILE = "D:\pbrain-pyrandom.log"
# ...and clear it initially
with open(DEBUG_LOGFILE, "w") as f:
    pass


# define a function for writing messages to the file
def logDebug(msg):
    with open(DEBUG_LOGFILE, "a") as f:
        f.write(msg + "\n")
        f.flush()


# define a function to get exception traceback
def logTraceBack():
    import traceback
    with open(DEBUG_LOGFILE, "a") as f:
        traceback.print_exc(file=f)
        f.flush()
    raise


# use logDebug wherever
# use try-except (with logTraceBack in except branch) to get exception info
# an example of problematic function
# def brain_turn():
#     logDebug("some message 1")
#     try:
#         logDebug("some message 2")
#         1. / 0.  # some code raising an exception
#         logDebug("some message 3")  # not logged, as it is after error
#     except:
#         logTraceBack()


"""
######################################################################

# "overwrites" functions in pisqpipe module
pp.brain_init = brain_init
pp.brain_restart = brain_restart
pp.brain_my = brain_my
pp.brain_opponents = brain_opponents
pp.brain_block = brain_block
pp.brain_takeback = brain_takeback
pp.brain_turn = brain_turn
pp.brain_end = brain_end
pp.brain_about = brain_about
if DEBUG_EVAL:
    pp.brain_eval = brain_eval


def main():
    pp.main()


if __name__ == "__main__":
    main()
    brain_turn()