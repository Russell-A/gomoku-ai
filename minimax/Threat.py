## 棋形
## 活2
chessdic = {}
## 眠二
# xoo...? | ?xo.o.. | ?xo..o. | ..oox?? | ..o.ox? | ..o..ox
# chessdic[(2,1,1,0,0,0,3)] = (0, (3,4))
# chessdic[(3,2,1,0,1,0,0)] = (0, (3,5))
# chessdic[(3,2,1,0,0,1,0)] = (0, (3,4))
# chessdic[(0,0,1,1,2,3,3)] = (0, (0,1))
# chessdic[(0,0,1,0,1,2,3)] = (0, (1,3))
# chessdic[(0,0,1,0,0,1,2)] = (0, (3,4))


# 从一个下过的子开始,取它的前两格和后四格
# x.oo... | ..oo..x | ..oo... | ..o.o.. | x.o.o.. | ..o.o.x 这里和眠三会有冲突 | ?.o..o. | ..oo.x?
chessdic[(2,0,1,1,0,0,0)] = (1, (4,5))
chessdic[(0,0,1,1,0,0,2)] = (1, (0,1,4))
chessdic[(0,0,1,1,0,0,0)] = (1, (0,1,4,5))
chessdic[(0,0,1,0,1,0,0)] = (1, (1,3,5))
chessdic[(2,0,1,0,1,0,0)] = (1, (3,5))
chessdic[(0,0,1,0,1,0,2)] = (1, (1,3))
chessdic[(3,0,1,0,0,1,0)] = (1, (3,4), (1,6))  ## 优先级，进攻点，防守点
chessdic[(0,0,1,1,0,2,3)] = (1, (0,1))

## 眠3
# x.ooo.x | ?xooo.. | ..ooox? | ?xoo.o. | ??o.o.o | ?xo.oo. | ..ooox? | ?.o.oox | ?.oo.ox | ??oo..o | ??o..oo
chessdic[(2,0,1,1,1,0,2)] = (2, (1,5))
chessdic[(3,2,1,1,1,0,0)] = (2, (5,6))
chessdic[(0,0,1,1,1,2,3)] = (2, (0,1))
chessdic[(3,2,1,1,0,1,0)] = (2, (4,6))
chessdic[(3,3,1,0,1,0,1)] = (2, (3,5)) # 这里可能会超出棋盘，要检测  ', (1,7)'
chessdic[(3,2,1,0,1,1,0)] = (2, (3,6)) #优先级，冲4点，冲3点  ', (7,)'
chessdic[(0,0,1,1,1,2,3)] = (2, (0,1))
chessdic[(3,0,1,0,1,1,2)] = (2, (1,3))
chessdic[(3,0,1,1,0,1,2)] = (2, (1,4)) #    ', (0,)'
chessdic[(3,3,1,1,0,0,1)] = (2, (4,5))
chessdic[(3,3,1,0,0,1,1)] = (2, (3,4))
## 活3
# x.ooo.. | ..ooo.. | ..ooo.x | ?.oo.o. | ?.o.oo. |
chessdic[(2, 0, 1, 1, 1, 0, 0)] = (3, (5,), (1, 6))  ## 优先级，进攻点，防守点
chessdic[(0, 0, 1, 1, 1, 0, 0)] = (3, (1, 5))
chessdic[(0, 0, 1, 1, 1, 0, 2)] = (3, (1,), (0, 5))
chessdic[(3, 0, 1, 1, 0, 1, 0)] = (3, (4,), (1, 6))
chessdic[(3, 0, 1, 0, 1, 1, 0)] = (3, (3,), (1, 6))
## 眠4
# ?xoooo. | ??ooo.o | ?.oooox | ??oo.oo | ??o.ooo |
chessdic[(3,2,1,1,1,1,0)] = (4, (6,))
chessdic[(3,3,1,1,1,0,1)] = (4, (5,))
chessdic[(3,0,1,1,1,1,2)] = (4, (1,))
chessdic[(3,3,1,1,0,1,1)] = (4, (4,))
chessdic[(3,3,1,0,1,1,1)] = (4, (3,))
## 活4
# ?.oooo.
chessdic[(3,0,1,1,1,1,0)] = (5, (1,))
# ??ooooo
chessdic[(3,3,1,1,1,1,1)] = (6, (0,))

index = [0,1,2]
## 预处理chessdic， 将3替换成0，1，2
for i in range(2):
    for a in list(chessdic.keys()):
        de = 0
        for i in range(len(a)):
            if a[i] == 3:
                de = 1
                t = list(a)
                for k in index:
                    t[i] = k
                    chessdic[tuple(t)] = chessdic[a]
        if de == 1:
            chessdic.pop(a)

vector = [(1, 1), (1, 0), (0, 1), (1, -1)]
## 向量加法
def vecadd(cd, vec, t):
    return (cd[0]+vec[0]*t, cd[1]+vec[1]*t)

def inboard(cd, board):
    if 0 <= cd[0] and cd[0] < len(board) and 0 <= cd[1] and cd[1] < len(board):
        return 1
    else:
        return 0

def isfree(cd, board):
    if inboard(cd, board) and board[cd[0]][cd[1]] == 0:
        return 1
    else:
        return 0

## 根据vec方向取一个点的前两格和后四格，
def seek7(x,y,who,vec,board):
    lenxy = len(board)
    res = []
    cdres = []
    for i in range(-2,5):
        cd = vecadd((x,y), vec, i)
        cdres.append(cd)
        if inboard(cd, board) == 1:
            if board[cd[0]][cd[1]] == who:
                value = 1
            elif board[cd[0]][cd[1]] == 3-who:
                value = 2
            else:
                value = 0
        else:
            value = 2
        res.append(value)
    return tuple(res), cdres


class Threat:
    def __init__(self, board):
        self.my_threat = set()
        self.op_threat = set()
        self.my_attack = set()
        self.op_attack = set()
        self.end = -1
        my, op = self.findall(board)
        for i in my:
            if (i[0] < 3):
                self.my_attack.add(i)
            elif (i[0] < 6):
                self.my_threat.add(i)
            else:
                self.end = 1
        for i in op:
            if (i[0] < 3):
                self.op_attack.add(i)
            elif (i[0] < 6):
                self.op_threat.add(i)
            else:
                self.end = 2
        my_threat = set()
        for i in self.my_threat:
            if i[0] != 4:
                my_threat.add(i)
            else:
                add = True
                for j in my_threat:
                    if j[0] == 4 and j[2] == i[2]:
                        add = False
                        break
                if add == True:
                    my_threat.add(i)
        op_threat = set()
        for i in self.op_threat:
            if i[0] != 4:
                op_threat.add(i)
            else:
                add = True
                for j in op_threat:
                    if j[0] == 4 and j[2] == i[2]:
                        add = False
                        break
                if add == True:
                    op_threat.add(i)
        self.my_threat = my_threat
        self.op_threat = op_threat



    def findall(self, board):  ## 找到所有棋形
        mychesstype = []
        opchesstype = []
        for vec in vector:
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == 1:
                        type, cdli = seek7(i, j, 1, vec, board)
                        if type in chessdic:
                            t = chessdic[type]
                            ##
                            if len(t) == 2:
                                mychesstype.append((t[0],(i,j),tuple(cdli[k] for k in t[1])))
                            else:
                                mychesstype.append((t[0], (i, j), tuple(cdli[k] for k in t[1]), tuple(cdli[k] for k in t[2])))
                    if board[i][j] == 2:
                        type, cdli = seek7(i, j, 2, vec, board)
                        if type in chessdic:
                            t = chessdic[type]
                            if (len(t) == 2):
                                opchesstype.append((t[0],(i,j),tuple(cdli[k] for k in t[1])))
                            else:
                                opchesstype.append((t[0], (i, j), tuple(cdli[k] for k in t[1]), tuple(cdli[k] for k in t[2])))
        return mychesstype, opchesstype

    def get_successor(self, who):
        index = who-1
        threatinfo = [self.my_threat, self.op_threat]
        attackinfo = [self.my_attack, self.op_attack]
        threatmine = threatinfo[index]
        threatoppo = threatinfo[1-index]
        attackmine = attackinfo[index]
        attackoppo = attackinfo[1-index]

        levelme = 0
        if len(threatmine) > 0:
            levelme = max([a[0] for a in threatmine])
        levelop = 0
        if len(threatoppo) > 0:
            levelop = max([a[0] for a in threatoppo])
        if max(levelop, levelme) == 0:
            return []

        if levelme >= levelop or levelme == 4:  ## 返回进攻的棋子
            succ = []
            for a in threatmine:
                if a[0] == levelme:
                    for t in a[2]:
                        succ.append(t)
            succ = list(set(succ))
            return succ

        if levelme < levelop:  ## 返回防守的棋子
            succ = []
            for a in threatoppo:
                if a[0] == levelop:
                    for t in a[2]:
                        succ.append(t)
                    if (len(a) > 3):
                        for t in a[3]:
                            succ.append(t)
            if levelop > 3:
                succ = list(set(succ))
                return succ

            for a in attackmine:  ## 增加冲4的棋子
                if a[0] == 2:
                    for t in a[2]:
                        succ.append(t)
            succ = list(set(succ))
            return succ

    def get_attack(self, who):
        index = who-1
        attackinfo = [self.my_attack, self.op_attack]
        attackmine = attackinfo[index]

        if len(attackmine) == 0:
            return []

        result = []
        for a in attackmine:
            for t in a[2]:
                result.append(t)
        result = list(set(result))
        return result

    def update(self, next_cd, board, who):
        board[next_cd[0]][next_cd[1]] = who
        for vec in vector:
            effect = [next_cd]  ## 可能受影响的点的集合
            for i in range(-2,5):
                if inboard(vecadd(cd=next_cd, vec=vec, t=-i), board):
                    effect.append(vecadd(cd = next_cd, vec = vec, t = -i))
            a = set()
            for item in self.my_threat:
                if item[1] not in effect:
                    a.add(item)
                else:
                    cd1x, cd1y = item[1]
                    cd2x, cd2y = item[2][0]
                    cd3x, cd3y = vec
                    if not abs((cd2y-cd1y)*(cd3x)-(cd3y)*(cd2x-cd1x)) <= 1e-6:
                        a.add(item)
                    self.my_threat = a
            a = set()
            for item in self.my_attack:
                if item[1] not in effect:
                    a.add(item)
                else:
                    cd1x, cd1y = item[1]
                    cd2x, cd2y = item[2][0]
                    cd3x, cd3y = vec
                    if not abs((cd2y-cd1y)*(cd3x)-(cd3y)*(cd2x-cd1x)) <= 1e-6:
                        a.add(item)
                    self.my_attack = a
            a = set()
            for item in self.op_threat:
                if item[1] not in effect:
                    a.add(item)
                else:
                    cd1x, cd1y = item[1]
                    cd2x, cd2y = item[2][0]
                    cd3x, cd3y = vec
                    if not abs((cd2y-cd1y)*(cd3x)-(cd3y)*(cd2x-cd1x)) <= 1e-6:
                        a.add(item)
                    self.op_threat = a
            a = set()
            for item in self.op_attack:
                if item[1] not in effect:
                    a.add(item)
                else:
                    cd1x, cd1y = item[1]
                    cd2x, cd2y = item[2][0]
                    cd3x, cd3y = vec
                    if not abs((cd2y-cd1y)*(cd3x)-(cd3y)*(cd2x-cd1x)) <= 1e-6:
                        a.add(item)
                    self.op_attack = a
            for cd in effect:
                my, op = self.find(cd , board, who, vec)
                for i in my:
                    if (i[0] < 3):
                        self.my_attack.add(i)
                    elif (i[0] < 6):
                        self.my_threat.add(i)
                    else:
                        self.end = 1
                for i in op:
                    if (i[0] < 3):
                        self.op_attack.add(i)
                    elif (i[0] < 6):
                        self.op_threat.add(i)
                    else:
                        self.end = 2
        my_threat = set()
        for i in self.my_threat:
            if i[0] != 4:
                my_threat.add(i)
            else:
                add = True
                for j in my_threat:
                    if j[0] == 4 and j[2] == i[2]:
                        add = False
                        break
                if add == True:
                    my_threat.add(i)
        op_threat = set()
        for i in self.op_threat:
            if i[0] != 4:
                op_threat.add(i)
            else:
                add = True
                for j in op_threat:
                    if j[0] == 4 and j[2] == i[2]:
                        add = False
                        break
                if add == True:
                    op_threat.add(i)
        self.my_threat = my_threat
        self.op_threat = op_threat

        board[next_cd[0]][next_cd[1]] = 0

    def find(self, cd:tuple, board, who, vec):
        mychesstype = []
        opchesstype = []
        i = cd[0]
        j = cd[1]
        if board[i][j] == 1:
            type, cdli = seek7(i, j, 1, vec, board)
            if type in chessdic:
                t = chessdic[type]
                ##
                if len(t) == 2:
                    mychesstype.append((t[0],(i,j),tuple(cdli[k] for k in t[1])))
                else:
                    mychesstype.append((t[0], (i, j), tuple(cdli[k] for k in t[1]), tuple(cdli[k] for k in t[2])))
        if board[i][j] == 2:
            type, cdli = seek7(i, j, 2, vec, board)
            if type in chessdic:
                t = chessdic[type]
                if (len(t) == 2):
                    opchesstype.append((t[0],(i,j),tuple(cdli[k] for k in t[1])))
                else:
                    opchesstype.append((t[0], (i, j), tuple(cdli[k] for k in t[1]), tuple(cdli[k] for k in t[2])))
        return mychesstype, opchesstype







# board = [[0 for i in range(20)] for j in range(20)]
# j = 1
# for i in lis:
#     j += 1
#     if j % 2 == 0:
#         board[i[0]][i[1]] = 1
#     else:
#         board[i[0]][i[1]] = 2
# board[10][10] = 2
# board[10][9]=2
# board[3][7]=2
# board[3][5]=1
# board[3][4]=1
# board[1][3]=1
# board[1][4]=2
# board[2][3]=1
# board[4][1]=1
# board[4][2]=2
# board[5][1]=1
# board[5][2]=2
# a = Threat(board)
# a.update((3,4), board, 2)
# board[3][4]=2
#
# a.update((3,6), board, 1)
# board[3][6]=1
#
# a.update((1,3), board, 2)
# board[1][3]=2
#
# a.update((1,4), board, 1)
# board[1][4]=1
#
# a.update((2,3), board, 2)
# board[2][3]=2
#
# a.update((4,1), board, 2)
# board[4][1]=2
#
# a.update((4,2), board, 1)
# board[4][2]=1
#
# a.update((5,1), board, 2)
# board[5][1]=2
#
# a.update((5,2), board, 1)
# board[5][2]=1
#
# a.update((3,5), board, 2)
# board[3][5]=2
#
# a.update((1,2), board, 1)
# board[1][2]=1
#
# a.update((1,6), board, 2)
# board[1][6]=2
#
#
# board = [[0 for i in range(20)] for j in range(20)]
# a = Threat(board)
# a.update((0,8), board, 1)
# board[0][8] = 1
# a.update((0,9), board, 1)
# board[0][9] = 1
# a.update((0,10), board, 2)
# board[0][10] = 2
# a.update((0,10), board, 2)
# board[0][10] = 2
# a = Threat(board)
# #
# #
# print(a.my_threat, a.my_attack)
# print(a.op_threat, a.op_attack)
#
# test = Threat(board)
# print(test.my_threat, test.my_attack)
# print(test.op_threat, test.op_attack)
# print(test.get_attack(1))
# from Data import gl_find_KillDict
# from Data import global_hashtable
# import Data as dt
# find_KillDict = gl_find_KillDict
# find_KillDict[1] = 0
# dt.set_kill_dict()
# print(dt.gl_KillDict)