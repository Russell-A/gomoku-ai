# gomoku-ai

For the final project, our group has designed two sorts of gomoku AI by using minimax together with situation evaluation and monte-carlo tree search. You can find the source code and executable AI in folders, and one corresponds for a different AI. The report will briefly explain the techniques we have used in our AI.
  
Remember to use Piskvork if you want to play against AI or if you want to launch the tournament of Artificial Intelligences.

## Minimax with situation evaluation:

This AI is improved from our midterm one, using the tradition way of minimax with alpha-beta pruning and situation evaluation. Given a gameboard with me being the next move, we can form a minimax search tree, where the max node and the min node take turns to appear. The max node gets the highest value of its children while the min node gets the lowest one. 

Ideally, the minimax search tree should take all its children into consideration, but it will cost a lot of times and computation resources in this way. Therefore, we evaluate the status of each child for each node and prune worse ones during expanding a minimax tree. In such a way, it may cause little bias in exchange of computation time, and we hold the belief that through our evaluation function, the bias can be reduced, even to zero. The AI submitted is set with maximum 3 children for a node and depth 5 for the search tree.

Alpha-beta pruning means that for every min node, if the parent node has already gotten a value larger than or equal to its current value, then we can prune the node from the graph. The reason is simple. The min node can never return a value larger the parent node has, so it is useless. For the max node, it’s similar except that it is pruned if its value is larger than or equal to its parent’s current value. 
When programming, we can use two variables, named after alpha and beta, to keep in track the largest value a max node can get and the smallest value a min node can acquire now. We renew alpha in a max node and beta in a min node. Every node gets alpha and beta from its parent. For every min node, if the current value is smaller than alpha, then it be pruned. For every max node, if the current value is bigger than beta, it can also be pruned.
	
We made a global variable, called threat, to record the threatening chess both my me and the opponent in the increasing order of threating level, i.e. active two, sleep three, active three, sleep four, active four, five-in-a-row. The latter four is called threating patterns or decisive patterns. When the decisive patterns appear, the next player have no choice but to block the pattern or making a more threating pattern. The global variable is updated together with the game board. Threat is used both for the evaluation function and for checking kill move.

Also, we take advantage of the translation table to speed up the searching process. By setting two tables with random 64-digit integers of the board’s size to represent the white piece and black piece respectively, we can easily represent the board by a 64-digit integer with the exclusive or operation, saving a lot of time of comparing the board. By using an exclusive or operation, in fact the board is hashed into a random integer. Therefore, when we are searching, whether for a killing move or for the current best move, we can use the translation table to record the values associated with the board, and use them later.

The evaluation function is accomplished by checking the pattern of pieces recorded in threat. If the opponent has decisive patterns like an active four or a sleep four, which means that we are about to lose the game, the value will be extremely low. On the other hand, if we have some decisive pattern, the value will be considerably high. If there is no threatening pattern, and we have opportunity to choose whether to attack or to defend, then we take all the patterns out, making each one a value and sum them up to evaluate the board. What’s important is that to make a minimax tree, we make the value of us positive and the opponent negative when evaluating. 

Checking for the killing move is also a searching problem. The two players act as a attacking role and a defending role separately, and the attacking player makes the move first. Different from alpha-beta pruning, for the attacking player, when searching for the possible next move, if the defensive one has no available active four, return the points forming a active three or a sleep four and the point to block the active four if the defensive one have any active four. For the defensive one, because the attractive one has already formed an active three or sleep four, he can only block the threating patterns or making a four-in-a-row when the attacking one has a active three. When the attacking one can no longer form a possible threating pattern or the defensive one no longer needs to defend or the searching goes beyond the limit, we cannot make a killing move.
When searching for the killing move, we record the board and the best move by transposition tables. When we get a killing move, we can record all the situation leading the final killing move. Therefore, we can rapidly lead to the final move after opponent’s defend.
Because searching for a rigidly true killing move needs a high searching depth, for example the opponent has many possible sleep fours. So, we can use the following two approximate method to determine kill or not. The first one is Victory of Continuous Four, which means the attacking one only form the sleep four. In such a way the defending one has no choice but to defend. The second one is naïvely checking for killing move. In such a way the defensive one only defends the threating pattern.
Therefore, there are three steps when searching for the killing move. First, check Victory of Continuous Four for me, and possibly we can find a killing move. Second, checking Victory of Continuous Four for the opponent. If there is a Victory of Continuous Four for the opponent, it means we cannot have a killing move. If the last two steps fail, then we naïvely checking for killing move for ourselves. These three steps are faster because it generates fewer children when searching.

As we expected, this Ai practices well and make scores over 1300

## MCTS

MCTS is the abbreviation of Monte Carlo Tree Search. MCTS requires a large number of simulation and builds up a large search tree according to the results. An important feature of MCTS is its estimated value will become more and more accurate with the increase of the simulation times and nodes accessed. The basic process of MCTS is shown in Fig. 1. It consists of four main stages: Selection, Expansion, Simulation, and Backpropagation.

The basic process of MCTS starts from the first stage called Selection. At this stage, it begins from the root node, and recursively applies the child selection policy (also known as Tree Policy) to descend through the tree until it reaches the most urgent expandable node. Then at Expansion stage, it can add one or more child nodes to expand the tree according to the available actions. At the third stage called Simulation, it can run a simulation from the leaf node based on the settled policy (or called Default Policy) to produce an outcome. Finally, at Backpropagation stage, it can back propagate the simulation result through the selected nodes to update their state values.
In our AI, we use UCT algorithm, which is embranchment of MCTS algorithm, based on Upper Confidence Bounds. UCB is known as capable to solve the multi-armed bandit problem. The most obvious virtue of UCB is that it helps to balance the conflict between exploration and exploitation and find out the result earlier. Its simplest form is:. Here  is the average reward from jth simulation,  is the number of times that node j is visited, and n is the overall number of plays so far. The reward  encourages the exploitation of higher reward selection, but the right-hand term  encourages the exploration of less visited choices.
In our project, the tree policy is to randomly choose an unexpanded node if one exists, otherwise we choose the best child and expand his child. The best child is selected by the largest UCB value. And the default policy is to randomly pick a move in the whole board. It may be inaccurate for the simulation because the player will never make moves like this, and the result is highly unpredictable with such a method. But in pursue of a higher speed, we cannot make a slower policy. 
In our project, we set the total round of expand and simulation to three thousand in consideration of speed and the computation resources. In fact, in some time the round is far fewer than it needs to converge. Therefore, the MCTS AI doesn’t preform well and acquire the points less than 1000.
