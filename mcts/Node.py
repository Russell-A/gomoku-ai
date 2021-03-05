from Threat import Threat
min_or_max = ["max", "min"]
import util as ut
import pisqpipe as pp
KillDict = {}
StateDict = {}
def boardtolist(board):
    change = []
    for a in range(pp.width):
        for b in range(pp.height):
            if board[a][b] > 0:
                change.append((a,b,board[a][b]))
    return tuple(change)
import Data as dt
import hash
hashtable = hash.hash(20,20)

COE_NORMAL = {1:2, 2:2, 3:2, 4:2, 5:20}
COE_DEFEND = {1:8, 2:10, 3:8, 4:8, 5:40}

score = [0, 100, -100]
enddict = {0:0, 1:2, 2:1}
N_kill = 10 # 计算杀棋的层数


class Node:
    def __init__(self, next_cd = (0,0), who = 2, boardNow = [], hashboard = 0):
        self.next_cd = next_cd  #who这步棋的坐标（产生候选的之后的操作就是更新棋盘）
        self.value = 0
        self.who = who
        self.board = boardNow  #当前棋盘
        self.hasboard = hashboard
        if next_cd == (-1,-1): #root节点
            self.threat = Threat(self.board)
        else:
            self.board[next_cd[0]][next_cd[1]] = who
            self.threat = Threat(self.board)
            self.board[next_cd[0]][next_cd[1]] = 0


    def get_successors(self): #产生下一步的候选，这是3-who要下的棋的集合
        states = self.threat.get_successor(3-self.who)
        if len(states) > 0:
            result = []
            for s in states:
                result.append(Node(next_cd=s, who=3 - self.who, boardNow=self.board))
            return result

        states = ut.get_successor(self, unsorted=False)   #每层排序
        # for s in states:
        #     result.append(Node(next_cd=s, who=3-self.who, boardNow=self.board))
        cd_set = set([i.next_cd for i in states])
        attack_states = ut.get_attack(self, unsorted=False)
        for s in attack_states:
            if s.next_cd not in cd_set:
                states.append(s)

        return states

    def kill_chess_get_successors(self, whokill = 1):

        states = self.threat.get_successor(3-self.who)  ## 对于我方来说，在冲3过程中要防对面的冲4，对敌方来说要防我方的活3或自己冲4
        result = []
        if len(states) > 0:
            for s in states:
                result.append(Node(next_cd=s, who=3 - self.who, boardNow=self.board))
            return result
        else:   ## 对于我方来说，要形成活3，如果敌方进入了这一步，则我方杀棋失败
            if (3-self.who) == 3-whokill:
                return []
            else:
                # states = self.threat.get_attack(3-self.who)
                # for s in states:
                #     result.append(Node(next_cd=s, who=3 - self.who, boardNow=self.board))
                result = ut.get_attack(self, unsorted=False, branch_attack=128)

            return result

    def check_kill_chess(self, whokill, N = N_kill):   ## 寻找杀棋，whokill是在当前棋盘下假设下一步是whokill下，是否存在whokill的杀棋
        alpha = float('-inf')
        beta = float('inf')

        temp_who = self.who
        temp_board = self.board[self.next_cd[0]][self.next_cd[1]]

        self.board[self.next_cd[0]][self.next_cd[1]] = self.who
        self.who = 3-whokill

        global KillDict
        KillDict = {}
        rt_node = get_value(self, alpha, beta, 0, whokill, N)

        dt.set_glo('KillDict', KillDict)


        self.who = temp_who
        self.board[self.next_cd[0]][self.next_cd[1]] = temp_board

        return rt_node


    # 有三种评价方式，mode = 0为正常模式，敌我进攻权重相同，mode = 1为防守模式，敌方进攻棋权重大，mode = 2为进攻模式，我方进攻棋权重大
    # mode = -1 则选择自动评估
    def evaluate(self, mode = 0):
        attack = [self.threat.my_attack, self.threat.op_attack]
        threat = [self.threat.my_threat, self.threat.op_threat]
        myattack = attack[self.who - 1]
        opattack = attack[2-self.who]
        mythreat = threat[self.who - 1]
        opthreat = threat[2-self.who]
        coemy = {}
        coeop = {}
        if mode == 0:
            coemy = COE_NORMAL
            coeop = COE_NORMAL
        if mode == 1:
            coemy = COE_NORMAL
            coeop = COE_DEFEND
        if mode == 2:
            coemy = COE_DEFEND
            coeop = COE_NORMAL
        va = 0
        for i in myattack:
            va += coemy[i[0]]
        for i in mythreat:
            va += coemy[i[0]]
        for i in opattack:
            va -= coeop[i[0]]
        for i in opthreat:
            va -= coeop[i[0]]
        va += max(len(mythreat)-1, 0)*20
        va -= len(opthreat)*10
        va += len(mythreat)*(len(myattack)-len(opattack)+1)*2
        # a = self.check_kill_chess(self.who, 2)
        # if (a.value == 100):
        #     va += 5

        self.value = va
        if self.who == 2:
            self.value = -self.value



    def updateboard(self, who = -1):
        if who == -1:
            who = self.who
        self.board[self.next_cd[0]][self.next_cd[1]] = who
        self.hasboard = self.hasboard^hashtable.table()[who-1][self.next_cd[0]][self.next_cd[1]]


    def restoreboard(self, who = -1):
        if who == -1:
            who = self.who
        self.board[self.next_cd[0]][self.next_cd[1]] = 0
        self.hasboard = self.hasboard^hashtable.table()[who-1][self.next_cd[0]][self.next_cd[1]]




# score = [0, 100, -100]
# enddict = {0:0, 1:2, 2:1}
# N_kill = 8 # 计算杀棋的层数
def get_value(node, alpha, beta, iteration, whokill = 1, N = N_kill):

    # t = boardtolist(node.board)
    # if t in StateDict:
    #     node.value = StateDict[t]
    #     # print("have explored")
    #     return node

    # end = ut.check_success(node.board, node.next_cd[0], node.next_cd[1], who=node.who)
    end = ut.ck_success(node)
    if (end)>=0:
        if whokill == 2:
            end = enddict[end]
        node.value = score[end]
        return node

    if (iteration > N):  # 杀棋层数太高，放弃
        node.value = 0
        return node


    if (iteration % 2 == 0):
        return max_value(node, alpha, beta, iteration, whokill = whokill, N = N)

    else:
        return min_value(node, alpha, beta, iteration, whokill = whokill, N = N)

def max_value(node, alpha, beta, iteration, whokill = 1, N = N_kill):

    if node.hasboard in KillDict:
        retnode = Node(KillDict[node.hasboard][1], who=3-whokill, boardNow=node.board, hashboard = node.hasboard)
        retnode.value = KillDict[node.hasboard][0]
        return retnode

    value = float('-inf')
    successors = node.kill_chess_get_successors(whokill = whokill) # 当前已是最新棋盘，据此来产生候选
    maxnode = node
    for i in successors:
        if whokill == 1:
            if (len(i.threat.my_threat)) > 1 and len(i.threat.op_threat) == 0 and (len(i.threat.op_attack)==0 or max([a[0] for a in i.threat.op_attack]) < 2):
                i.value = 100

                KillDict[i.hasboard] = (100, i.next_cd)

                return i

            # 我方产生活4且对面没有4颗时已经胜利
            if (len(i.threat.my_threat) > 0 and max([a[0] for a in i.threat.my_threat]) == 5):
                if (len(i.threat.op_threat) == 0 or max([a[0] for a in i.threat.op_threat]) < 4):
                    i.value = 100

                    KillDict[i.hasboard] = (100, i.next_cd)

                    return i
        if whokill == 2:
            if (len(i.threat.op_threat)) > 1 and len(i.threat.my_threat) == 0 and (len(i.threat.my_attack)==0 or max([a[0] for a in i.threat.my_attack]) < 2):
                i.value = 100

                KillDict[i.hasboard] = (100, i.next_cd)

                return i

            if (len(i.threat.op_threat) > 0 and max([a[0] for a in i.threat.op_threat]) == 5):
                if (len(i.threat.my_threat) == 0 or max([a[0] for a in i.threat.my_threat]) < 4):
                    i.value = 100

                    KillDict[i.hasboard] = (100, i.next_cd)

                    return i

        # i.board[i.next_cd[0]][i.next_cd[1]] = whokill   #更新棋盘

        i.updateboard(whokill)
        getnode = get_value(i, alpha, beta, iteration+1, whokill = whokill, N = N)
        # StateDict[boardtolist(getnode.board)] = getnode.value
        i.restoreboard(whokill)  #复原棋盘

        if (getnode.value == 100):  # 对于max来说，只要有一个是赢的说明有杀棋, 并将这个棋谱保存到KillDict中
            i.value = 100

            KillDict[i.hasboard] = (100, i.next_cd)

            return i

        if getnode.value > value:
            value = getnode.value
            i.value = value
            maxnode = i

        if value > alpha:
            alpha = value
        if value >= beta:
            KillDict[maxnode.hasboard] = (maxnode.value, maxnode.next_cd)
            return maxnode

    KillDict[maxnode.hasboard] = (maxnode.value, maxnode.next_cd)
    return maxnode

def min_value(node, alpha, beta, iteration, whokill = 1, N = N_kill):

    if node.hasboard in KillDict:
        retnode = Node(KillDict[node.hasboard][1], who=3-whokill, boardNow=node.board, hashboard = node.hasboard)
        retnode.value = KillDict[node.hasboard][0]
        return retnode

    value = float('inf')
    minnode = node
    successors = node.kill_chess_get_successors(whokill = whokill)
    for i in successors:
        # i.board[i.next_cd[0]][i.next_cd[1]] = 3-whokill


        i.updateboard(3-whokill)
        getnode = get_value(i, alpha, beta, iteration+1, whokill=whokill, N = N)
        # StateDict[boardtolist(getnode.board)] = getnode.value
        i.restoreboard(3-whokill)

        if getnode.value == 0:

            KillDict[i.hasboard] = (0, i.next_cd)

            return i


        if getnode.value < value:
            value = getnode.value
            i.value = value
            minnode = i

        if value < beta:
            beta = value
        if (value <= alpha):
            KillDict[node.hasboard] = (minnode.value, minnode.next_cd)
            return minnode

    KillDict[node.hasboard] = (minnode.value, minnode.next_cd)

    return minnode
