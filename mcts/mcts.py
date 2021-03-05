#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import random
import util as ut
import hash
import Threat
import Node as n

# AVAILABLE_CHOICES = [1, -1, 2, -2]
# AVAILABLE_CHOICE_NUMBER = len(AVAILABLE_CHOICES)
MAX_ROUND_NUMBER = 200
HASH = hash.hash(20,20)
# import Data as dt
# dt.set_glo('glo_has', HASH)

def isEmpty(board, x, y):
    return 0<=x<=19 and 0<=y<=19 and board[x][y]== 0

def isnotEmpty(board, x, y):
    return 0<=x<=19 and 0<=y<=19 and board[x][y]!= 0

class State(object):
    """
  蒙特卡罗树搜索的游戏状态，记录在某一个Node节点下的状态数据，包含当前的游戏得分、当前的游戏round数、从开始到当前的执行记录。

  需要实现判断当前状态是否达到游戏结束状态，支持从Action集合中随机取出操作。
  """

    def __init__(self, board, who):
        self.board = board
        self.hashtable = 0
        self.current_value = 0.0
        # For the first root node, the index is 0 and the game should start from 1
        self.current_round_index = 0
        self.cumulative_choices = []
        self.successors = []
        self.who = who
        self.sorted = False
        self.depth = 1
        self.threat = None

    def get_current_value(self):
        return self.current_value

    def set_current_value(self, value):
        self.current_value = value

    def get_current_round_index(self):
        return self.current_round_index

    def set_current_round_index(self, turn):
        self.current_round_index = turn

    def get_cumulative_choices(self):
        return self.cumulative_choices

    def set_cumulative_choices(self, choices):
        self.cumulative_choices = choices

    def set_depth(self,depth):
        self.depth = depth

    def get_depth(self):
        return self.depth

    def is_terminal(self):
        if self.cumulative_choices:
            if ut.check_success(self.board, x=self.cumulative_choices[-1][0], y=self.cumulative_choices[-1][1],
                            who=1) != -1:
                return True
        # The round index starts from 1 to max round number
        return self.current_round_index == MAX_ROUND_NUMBER

    def compute_reward(self):
        return self.current_value

    def set_successors(self, maxsuccessors, unsorted):
        s = Threat.Threat(self.board).get_successor(who = self.who)
        if s:
            self.successors =s
        else:
            self.successors = ut.get_successors_mcts(board = self.board,who = self.who,  max_successors=maxsuccessors, unsorted=unsorted , threat = self.threat)

    def set_hashtable(self, hashtable):
        self.hashtable = hashtable

    def get_hashtable(self):
        return self.hashtable

    def get_next_state_with_random_choice(self):
        if not self.successors:
            self.set_successors(maxsuccessors=10, unsorted=False)
        random_choice = random.choice(self.successors)
        self.board[random_choice[0]][random_choice[1]] = self.who
        next_state = State(board = self.board, who = 3-self.who)
        new_hashtable = self.hashtable ^ HASH.table()[self.who-1][random_choice[0]][random_choice[1]]
        next_state.set_hashtable(hashtable=new_hashtable)
        import copy
        next_state.threat = copy.copy(self.threat)
        next_state.threat.update(random_choice, self.board ,self.who)

        success = ut.check_success(self.board, random_choice[0], random_choice[1], who=self.who)
        if success == 1:
            #print('win')
            next_state.set_current_value(self.current_value + 1)
        elif success == 2:
            next_state.set_current_value(self.current_value + 0)
            #print('lose')
        elif success == 0:
            next_state.set_current_value(self.current_value + 0.5 )
        next_state.set_depth(self.depth+1)
        next_state.set_current_round_index(self.current_round_index + 1)
        next_state.set_cumulative_choices(self.cumulative_choices +
                                          [random_choice])
        return next_state

    def get_next_state_with_random_choice_for_simulation(self):
        x = random.randint(0,19)
        y = random.randint(0,19)
        board = self.board
        while isnotEmpty(board, x, y):
            x = random.randint(0, 19)
            y = random.randint(0, 19)
        random_choice = (x,y)
        self.board[random_choice[0]][random_choice[1]] = self.who
        next_state = State(board = self.board, who = 3-self.who)

        success = ut.check_success(self.board, random_choice[0], random_choice[1], who=self.who)
        if success == 1:
            #print('win')
            next_state.set_current_value(self.current_value + 1)
        elif success == 2:
            next_state.set_current_value(self.current_value + 0)
            #print('lose')
        elif success == 0:
            next_state.set_current_value(self.current_value + 0.5 )
        next_state.set_current_round_index(self.current_round_index + 1)
        next_state.set_cumulative_choices(self.cumulative_choices +
                                          [random_choice])
        return next_state

    # def __repr__(self):
    #   return "State: {}, value: {}, round: {}, choices: {}".format(
    #       hash(self), self.current_value, self.current_round_index,
    #       self.cumulative_choices)


class Node(object):
    """
  蒙特卡罗树搜索的树结构的Node，包含了父节点和直接点等信息，还有用于计算UCB的遍历次数和quality值，还有游戏选择这个Node的State。
  """

    def __init__(self):
        self.parent = None
        self.children = []

        self.visit_times = 0
        self.quality_value = 0.0

        self.state = None
        self.threat = None

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state
    
    def get_state_hash(self):
        return self.state.hashtable

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_children(self):
        return self.children

    def get_visit_times(self):
        return self.visit_times

    def set_visit_times(self, times):
        self.visit_times = times

    def visit_times_add_one(self):
        self.visit_times += 1

    def get_quality_value(self):
        return self.quality_value

    def set_quality_value(self, value):
        self.quality_value = value

    def quality_value_add_n(self, n):
        self.quality_value += n

    def is_all_expand(self):
        self.state.set_successors(maxsuccessors=1000, unsorted=True)
        return len(self.children) == len(self.state.successors)

    def add_child(self, sub_node):
        sub_node.set_parent(self)
        self.children.append(sub_node)

    # def __repr__(self):
    #     return "Node: {}, Q/N: {}/{}, state: {}".format(
    #         hash(self), self.quality_value, self.visit_times, self.state)


def tree_policy(node):
    """
  蒙特卡罗树搜索的Selection和Expansion阶段，传入当前需要开始搜索的节点（例如根节点），根据exploration/exploitation算法返回最好的需要expend的节点，注意如果节点是叶子结点直接返回。

  基本策略是先找当前未选择过的子节点，如果有多个则随机选。如果都选择过就找权衡过exploration/exploitation的UCB值最大的，如果UCB值相等则随机选。
  """

    # Check if the current node is the leaf node
    while not node.get_state().is_terminal():

        if node.is_all_expand():
            node = best_child(node, True)
        else:
            sub_node = expand(node)
            # Return the new sub node
            # if node.get_state().get_depth() < 3:
            #     sub_node = expand(node)
            # else:
            #     sub_node = best_child(node, False)
            return sub_node

    # Return the leaf node
    return node


def default_policy(node):
    """
  蒙特卡罗树搜索的Simulation阶段，输入一个需要expand的节点，随机操作后创建新的节点，返回新增节点的reward。注意输入的节点应该不是子节点，而且是有未执行的Action可以expend的。

  基本策略是随机选择Action。
  """

    # Get the state of the game
    import copy
    current_state = copy.deepcopy(node.get_state())
    #print(node.get_state().board)
    # Run until the game over
    while current_state.is_terminal() == False:
        # Pick one random action to play and get next state
        current_state = current_state.get_next_state_with_random_choice_for_simulation()

    final_state_reward = current_state.compute_reward()
    #print('final_state_reward:%d'%final_state_reward)
    #print(node.get_state().board)
    return final_state_reward


def expand(node):
    """
  输入一个节点，在该节点上拓展一个新的节点，使用random方法执行Action，返回新增的节点。注意，需要保证新增的节点与其他节点Action不同。
  """

    tried_sub_node_states = [
        sub_node.get_state_hash() for sub_node in node.get_children()
    ]

    new_state = node.get_state().get_next_state_with_random_choice()

    # Check until get the new state which has the different action from others
    while new_state.hashtable in tried_sub_node_states:
        new_state.board[new_state.cumulative_choices[-1][0]][new_state.cumulative_choices[-1][1]] = 0
        new_state = node.get_state().get_next_state_with_random_choice()

    sub_node = Node()
    sub_node.set_state(new_state)
    node.add_child(sub_node)
    #print('subnode',sub_node)
    return sub_node


def best_child(node, is_exploration):
    """
  使用UCB算法，权衡exploration和exploitation后选择得分最高的子节点，注意如果是预测阶段直接选择当前Q值得分最高的。
  """

    # TODO: Use the min float value
    best_score = -sys.maxsize
    best_sub_node = None

    # Travel all sub nodes to find the best one
    for sub_node in node.get_children():

        # Ignore exploration for inference
        if is_exploration:
            C = 1 / math.sqrt(2.0)
        else:
            C = 0.0

        # UCB = quality / times + C * sqrt(2 * ln(total_times) / times)
        left = sub_node.get_quality_value() / sub_node.get_visit_times()
        right = 2.0 * math.log(node.get_visit_times()) / sub_node.get_visit_times()
        score = left + C * math.sqrt(right)

        if score > best_score:
            best_sub_node = sub_node
            best_score = score
    #print('best_score:%d'%best_score)
    choice = best_sub_node.state.cumulative_choices[-1]
    best_sub_node.state.board[choice[0]][choice[1]] = node.state.who
    return best_sub_node


def backup(node, reward):
    """
  蒙特卡洛树搜索的Backpropagation阶段，输入前面获取需要expend的节点和新执行Action的reward，反馈给expend节点和上游所有节点并更新对应数据。
  """

    # Update util the root node
    while node != None:
        # 删去最后一次下的子
        if len(node.get_state().cumulative_choices) != 0:
            #print(node.get_state().cumulative_choices)
            node.get_state().board[node.get_state().cumulative_choices[-1][0]][node.get_state().cumulative_choices[-1][1]] = 0

        # Update the visit times
        node.visit_times_add_one()

        # Update the quality value
        node.quality_value_add_n(reward)

        # Change the node to the parent node
        node = node.parent


def monte_carlo_tree_search(node):
    """
  实现蒙特卡洛树搜索算法，传入一个根节点，在有限的时间内根据之前已经探索过的树结构expand新节点和更新数据，然后返回只要exploitation最高的子节点。

  蒙特卡洛树搜索包含四个步骤，Selection、Expansion、Simulation、Backpropagation。
  前两步使用tree policy找到值得探索的节点。
  第三步使用default policy也就是在选中的节点上随机算法选一个子节点并计算reward。
  最后一步使用backup也就是把reward更新到所有经过的选中节点的节点上。

  进行预测时，只需要根据Q值选择exploitation最大的节点即可，找到下一个最优的节点。
  """
    computation_budget = 3000

    # Run as much as possible under the computation budget
    for i in range(computation_budget):
        # print('computation_budget :%d' % i)
        if i == 1433:
            i = 1433
        # 1. Find the best node to expand
        expand_node = tree_policy(node)

        # 2. Random run to add node and get reward
        reward = default_policy(expand_node)

        # 3. Update all passing nodes with reward
        backup(expand_node, reward)
        # print(node.get_state().board)

    # N. Get the best next node
    best_next_node = best_child(node, False)

    return best_next_node


def MCTS(board):
    import copy

    board = copy.deepcopy(board)
    # node = n.Node(next_cd=(-1, -1), who=2, boardNow= board, hashboard= 0)
    # node_new = node.check_kill_chess(whokill=1,N=4)
    # if node_new.value == 100:
    #     return node_new.next_cd
    init_state = State(board, who = 1)
    init_state.threat = Threat.Threat(board)
    init_node = Node()
    init_node.set_state(init_state)
    current_node = init_node
    current_node = monte_carlo_tree_search(current_node)
    return current_node.state.cumulative_choices[0]

def main():
    # Create the initialized state and initialized node
    board = [[0 for i in range(20)] for j in range(20)]

    init_state = State(board, who = 1)
    init_state.threat = Threat.Threat(board)
    init_node = Node()
    init_node.set_state(init_state)
    current_node = init_node
    current_node = monte_carlo_tree_search(current_node)
    print(current_node.state.cumulative_choices[0])
    # Set the rounds to play
    # for i in range(10):
    #     #print("Play round: {}".format(i + 1))
    #     current_node = monte_carlo_tree_search(current_node)
    #     #print("Choose node: {}".format(current_node))


if __name__ == "__main__":
    main()
