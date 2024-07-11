# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def getGoalState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getForwardSuccessors(self, state):
        """
        This function is for Forward Successors of a Bi-directional search
        """
        util.raiseNotDefined()

    def getBackwardSuccessors(self, state):
        """
        This function is for Backward Successors of a Bi-directional search
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def graphTreeSearch(problem, fringe, search_type, heuristic):
    startingNode = problem.getStartState()
    if problem.isGoalState(startingNode):
        return []
    
    if search_type in ['dfs', 'bfs']:
        fringe.push((startingNode, []))
    elif search_type in ['ucs', 'a*s']:
        fringe.push((startingNode, [], 0), problem.getCostOfActions([]))
    else:
        return []

    visitedNodes = list()

    while not fringe.isEmpty():

        if search_type in ['dfs', 'bfs']:
            currentNode, actions = fringe.pop()
        elif search_type in ['ucs', 'a*s']:
            currentNode, actions, prevCost = fringe.pop()
        else:
            return []
    
        if currentNode not in visitedNodes:
            visitedNodes.append(currentNode)

            if problem.isGoalState(currentNode):
                return actions
            
            childNodes = problem.getSuccessors(currentNode)
            for nextNode, action, cost in childNodes:
                newAction = actions + [action]
                
                if search_type in ['a*s', 'ucs']:
                    newCostToNode = prevCost + cost
                    if search_type == 'a*s':
                        priority = newCostToNode + heuristic(nextNode, problem)
                    else:           # search_type == 'ucs'
                        priority = newCostToNode
                    fringe.push((nextNode, newAction, newCostToNode), priority)
                else:   # search_type == 'dfs' and 'bfs'
                    fringe.push((nextNode, newAction))

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    return graphTreeSearch(problem, stack, 'dfs', None)
    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    return graphTreeSearch(problem, queue, 'bfs', None)
    # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    priority_queue = util.PriorityQueue()
    return graphTreeSearch(problem, priority_queue, 'ucs', None)
    # util.raiseNotDefined()

def nullHeuristic(state, problem=None, info={}):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    priority_queue = util.PriorityQueue()
    return graphTreeSearch(problem, priority_queue, 'a*s', heuristic)
    # util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

#################################################################
'''
Here is the implementation done for the team project part. 

Project topic 1. Bi-directional search
Reference Paper: Bidirectional Search That Is Guaranteed to Meet in the Middle
'''
#################################################################

def flipActionPath(actions):
    directionsReverse = {'East': 'West', 'West': 'East', 'North': 'South', 'South': 'North'}
    return [directionsReverse[action] for action in list(reversed(actions))]

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal if 'flip' not in info or info['flip'] is False else problem.startState
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal if 'flip' not in info or info['flip'] is False else problem.startState
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5

def graphTreeBiSearch(problem, fringe_forward, fringe_backward, search_type, heuristic):
    startingNodeF = endingNodeB = problem.getStartState()
    endingNodeF = startingNodeB = problem.getGoalState()

    # print('StartF:', startingNodeF)
    # print('StartB:', startingNodeB)
    
    if search_type == 'MM_E':
        heuristic = euclideanHeuristic
    elif search_type == 'MM_M':
        heuristic = manhattanHeuristic
    else:                                   # if search_type == 'MM0':
        heuristic = nullHeuristic

    if ((startingNodeF == startingNodeB) or (endingNodeF == endingNodeB)):
        return []
    
    opensetForwards = dict()            #Open set of unvisited nodes for forward search
    closedsetForwards = dict()          #Closed set of visited nodes for forward search

    opensetBackwards = dict()           #Open set of unvisited nodes for forward search
    closedsetBackwards = dict()         #Closed set of visited nodes for backward search

    tempsetForwards = dict()
    tempsetBackwards = dict()

    # '''
    # A* works using the following formula, f(n) = g(n) + h(n) where,
    # f(n) is the total cost estimate of the optimal path.
    # g(n) is the actual cost function of the path to node 'n' which in terms of code is given by problem.getCostOfActions() function
    # h(n) is the heuristic function of the path to node 'n' which in terms of code is written as heuristic(state, problem)
    #
    # So, for a bidirectional search node should have following properties:
    #   {Node Value(n), Node Path(actions), Cost value(g(n)), Heuristic Value(h(n)), Priority Value} within a priority queue.
    # '''
    flipHeuristic = {}

    # For forward search
    flipHeuristic['flip'] = False

    opensetForwards[startingNodeF] = {
        'state': startingNodeF,
        'actions': [],
        'costValue': problem.getCostOfActions([]),
        'heuristicValue': heuristic(startingNodeF, problem, flipHeuristic),
        'totalCostValue': 0,
        'priority': 0
    }
    
    # print('Open F:', opensetForwards)

    fringe_forward.push(opensetForwards[startingNodeF], opensetForwards[startingNodeF]['priority'])

    # For backward search
    flipHeuristic['flip'] = True

    opensetBackwards[startingNodeB] = {
        'state': startingNodeB,
        'actions': [],
        'costValue': problem.getCostOfActions([]),
        'heuristicValue': heuristic(startingNodeB, problem, flipHeuristic),
        'totalCostValue': 0,
        'priority': 0
    }

    # print('Open B:', opensetBackwards)

    fringe_backward.push(opensetBackwards[startingNodeB], opensetBackwards[startingNodeB]['priority'])

    '''
    U is the cost of the cheapest solution found so far in the state space.
    Initially, the value of U is considered as infinity as there is no cost found until there is a traversal in the state space.
    '''
    U = float('inf')

    '''
    Variable 'eps' is the cost of the cheapest edge in the state space. 
    Here in the pacman domain, the edge costs are unit. So, the value of eps is considered as 1.
    '''
    eps = 1 

    '''
    For tracing the resultant path, we have considered a list named actionPath.
    '''
    actionPath = list()

    recentNodeB = None
    recentNodeF = None

    while(not fringe_forward.isEmpty()) and (not fringe_backward.isEmpty()):
        
        # This is for the forward search
        curMinNodeF = fringe_forward.peek()
        
        # print('Min Node F:', curMinNodeF)
        # For calculating custom priority of the node using the function priority(n) = max(f(n), 2*g(n)) according to the reference algorithm.
        curMinNodeF['totalCostValue'] = curMinNodeF['costValue'] + curMinNodeF['heuristicValue']
        fVal_Forwards = curMinNodeF['totalCostValue']
        gVal_Forwards = curMinNodeF['costValue']
        priorityMinForwards = max(fVal_Forwards, 2*gVal_Forwards)

        # print('priorityMinForwards:', priorityMinForwards)

        # This is for the backward search
        curMinNodeB = fringe_backward.peek()

        # print('Min Node B:', curMinNodeB)
        # For calculating custom priority of the node using the function priority(n) = max(f(n), 2*g(n)) according to the reference algorithm.
        curMinNodeB['totalCostValue'] = curMinNodeB['costValue'] + curMinNodeB['heuristicValue'] 
        fVal_Backwards = curMinNodeB['totalCostValue']
        gVal_Backwards = curMinNodeB['costValue']
        priorityMinBackwards = max(fVal_Backwards, 2*gVal_Backwards)

        # print('priorityMinBackwards:', priorityMinBackwards)
        '''
        C is the cost of an optimal solution and it is given as C = min(priorityMinForwards, priorityMinBackwards)
        '''
        C = min(priorityMinForwards, priorityMinBackwards)
        # print('C:', C)
        '''
        U is the cost of the cheapest solution found so far. So, it is updated everytime when it satisfies the following condition.
        if U <= max(C, fminF, fminB, gminF +gminB + eps) or if U <= C
        then
            return U        --> This means the resultant cost found after the bidirectional search.
        
        In this program, we would like to find the resultant path as the pacman needs the path for traversal.

        Here, max(C, fminF, fminB, gminF +gminB + eps) is lower cost bound and 'eps' is the cost of the cheapest edge in the state space.
        '''
        lowerCostBound = max(C, fVal_Forwards, fVal_Backwards, gVal_Forwards + gVal_Backwards + eps)
        if (U <= lowerCostBound) or (U <= C):
            return actionPath
        
        if (C == priorityMinForwards):
            recentNodeF = curNodeF = fringe_forward.pop()

            if curNodeF['state'] in opensetForwards:            
                opensetForwards.pop(curNodeF['state'])
            # print('Open F1:', opensetForwards)

            closedsetForwards[curNodeF['state']] = curNodeF
            # print('Closed F1:', closedsetBackwards)

            childNodesF = problem.getForwardSuccessors(curNodeF['state'])
            # print('ChildNodes F:', childNodesF)

            for nextChildNodeF, actionChildNodeF, costChildNodeF in childNodesF:      
                # print('Child Prop F', nextChildNodeF, actionChildNodeF, costChildNodeF)

                if (nextChildNodeF in opensetForwards):
                    # print('New Node F loop1:', opensetForwards[nextChildNodeF])
                    nextNodeF = opensetForwards[nextChildNodeF]

                elif (nextChildNodeF in closedsetForwards):
                    # print('New Node F loop2:', closedsetForwards[nextChildNodeF])
                    nextNodeF = closedsetForwards[nextChildNodeF]

                else:
                    nextNodeF = None

                if nextNodeF is not None:
                    # print('LIKHITH:', nextNodeF)

                    if (nextNodeF['costValue'] <= curNodeF['costValue'] + costChildNodeF):
                        continue
                    
                    fringe_forward.remove(nextNodeF)

                    if (nextChildNodeF in opensetBackwards):
                        opensetForwards.pop(nextChildNodeF)

                    if (nextChildNodeF in closedsetBackwards):
                        closedsetForwards.pop(nextChildNodeF)

                    flipHeuristic['flip'] = False

                    nextNodeF['costValue'] = curNodeF['costValue'] + costChildNodeF
                    nextNodeF['heuristicValue'] = heuristic(nextNodeF['state'], problem, flipHeuristic)
                    nextNodeF['totalCostValue'] = nextNodeF['costValue'] + nextNodeF['heuristicValue']
                    nextNodeF['actions'] = list(curNodeF['actions']) + [actionChildNodeF]
                    # nextNodeF['priority'] = max( nextNodeF['totalCostValue'], 2 * nextNodeF['costValue'])
                    
                else:
                    flipHeuristic['flip'] = False

                    tempsetForwards[nextChildNodeF] = {
                            'state': nextChildNodeF,
                            'actions': list(curNodeF['actions']) + [actionChildNodeF],
                            'costValue':  curNodeF['costValue'] + costChildNodeF,
                            'heuristicValue': heuristic(nextChildNodeF, problem, flipHeuristic),
                            'totalCostValue': 0,
                            'priority': 0
                    }
                    
                    tempsetForwards[nextChildNodeF]['totalCostValue'] = tempsetForwards[nextChildNodeF]['costValue'] + tempsetForwards[nextChildNodeF]['heuristicValue']
                    tempsetForwards[nextChildNodeF]['priority'] = tempsetForwards[nextChildNodeF]['costValue'] + max(tempsetForwards[nextChildNodeF]['totalCostValue'], 2 * tempsetForwards[nextChildNodeF]['costValue'])
                    
                    nextNodeF = tempsetForwards[nextChildNodeF]

                    # print('Tempset A:', tempsetForwards)

                fringe_forward.push(nextNodeF, nextNodeF['priority'])
                opensetForwards[nextChildNodeF] = nextNodeF
                # print('Open F2:', opensetForwards)

                if (nextNodeF['state'] in opensetBackwards):
                    nextNodeBBar = opensetBackwards[nextNodeF['state']]                
                    U = min(U, nextNodeF['costValue'] + nextNodeBBar['costValue'])
                    actionPath = list(nextNodeF['actions']) + flipActionPath(nextNodeBBar['actions'])

        else:
            recentNodeB = curNodeB = fringe_backward.pop()
            # print('CurrentNode B:', curNodeB)

            if curNodeB['state'] in opensetBackwards:            
                opensetBackwards.pop(curNodeB['state'])
            # print('Open B1:', opensetBackwards)

            closedsetBackwards[curNodeB['state']] = curNodeB
            # print('Closed B1:', closedsetBackwards)

            childNodesB = problem.getBackwardSuccessors(curNodeB['state'])
            # print('ChildNodes:', childNodesB)

            for nextChildNodeB, actionChildNodeB, costChildNodeB in childNodesB: 
                # print('Child Prop', nextChildNodeB, actionChildNodeB, costChildNodeB)

                if (nextChildNodeB in opensetBackwards):
                    # print('New Node B loop1:', opensetBackwards[nextChildNodeB])
                    nextNodeB = opensetBackwards[nextChildNodeB]
                    
                elif (nextChildNodeB in closedsetBackwards):
                    # print('New Node B loop2:',closedsetBackwards[nextChildNodeB])
                    nextNodeB = closedsetBackwards[nextChildNodeB]

                else:
                    nextNodeB = None

                # print('NextNode:', nextNodeB)

                if nextNodeB is not None:
                    # print('LIKHITH:', nextNodeB)

                    if (nextNodeB['costValue'] <= curNodeB['costValue'] + costChildNodeB):
                        continue
                    
                    fringe_backward.remove(nextNodeB)

                    if (nextChildNodeB in opensetBackwards):
                        opensetBackwards.pop(nextChildNodeB)

                    if (nextChildNodeB in closedsetBackwards):
                        closedsetBackwards.pop(nextChildNodeB)

                    flipHeuristic['flip'] = True

                    nextNodeB['costValue'] = curNodeB['costValue'] + costChildNodeB
                    nextNodeB['heuristicValue'] = heuristic(nextNodeB['state'], problem, flipHeuristic)
                    nextNodeB['totalCostValue'] = nextNodeB['costValue'] + nextNodeB['heuristicValue']
                    nextNodeB['actions'] = list(curNodeB['actions']) + [actionChildNodeB]
                    # nextNodeB['priority'] = nextNodeB['costValue'] + max( nextNodeB['totalCostValue'], 2 * nextNodeB['costValue'])
                    
                else:

                    flipHeuristic['flip'] = True
                    tempsetBackwards[nextChildNodeB] = {
                            'state': nextChildNodeB,
                            'actions': list(curNodeB['actions']) + [actionChildNodeB],
                            'costValue':  curNodeB['costValue'] + costChildNodeB,
                            'heuristicValue': heuristic(nextChildNodeB, problem, flipHeuristic),
                            'totalCostValue': 0,
                            'priority': 0
                    }
                    
                    tempsetBackwards[nextChildNodeB]['totalCostValue'] = tempsetBackwards[nextChildNodeB]['costValue'] + tempsetBackwards[nextChildNodeB]['heuristicValue']
                    tempsetBackwards[nextChildNodeB]['priority'] = tempsetBackwards[nextChildNodeB]['costValue'] + max(tempsetBackwards[nextChildNodeB]['totalCostValue'], 2 * tempsetBackwards[nextChildNodeB]['costValue'])
                    
                    nextNodeB = tempsetBackwards[nextChildNodeB]

                    # print('Tempset B:', tempsetBackwards)
                
                fringe_backward.push(nextNodeB, nextNodeB['priority'])
                opensetBackwards[nextChildNodeB] = nextNodeB
                # print('Open B2:', opensetBackwards)
                
                if (nextNodeB['state'] in opensetForwards):
                    nextNodeFBar = opensetForwards[nextNodeB['state']]                
                    U = min(U, nextNodeB['costValue'] + nextNodeFBar['costValue'])
                    actionPath = list(nextNodeFBar['actions']) + flipActionPath(nextNodeB['actions'])

    # print('Recent F:', recentNodeF)
    # print('Recent B:', recentNodeB)

    return recentNodeF['actions'] + flipActionPath(recentNodeB['actions']) if ((recentNodeB is not None) and (recentNodeF is not None)) else []
    

def biDirectionalAStarManhattanHeuristicSearch(problem, heuristic):
    priority_queue_fwd = util.PriorityQueue()
    priority_queue_bwd = util.PriorityQueue()
    return graphTreeBiSearch(problem, priority_queue_fwd, priority_queue_bwd, 'MM_M', heuristic)

def biDirectionalAStarEuclideanHeuristicSearch(problem, heuristic):
    priority_queue_fwd = util.PriorityQueue()
    priority_queue_bwd = util.PriorityQueue()
    return graphTreeBiSearch(problem, priority_queue_fwd, priority_queue_bwd, 'MM_E', heuristic)

def biDirectionalAStarSearchBruteForce(problem, heuristic):
    # biDirectionalAStarSearchBruteForce is biDirectionalAStarSearch with null heuristic.
    priority_queue_fwd = util.PriorityQueue()
    priority_queue_bwd = util.PriorityQueue()
    return graphTreeBiSearch(problem, priority_queue_fwd, priority_queue_bwd, 'MM0', heuristic)


# Abbreviations
bds_mm0 = biDirectionalAStarSearchBruteForce
bds_mmMan = biDirectionalAStarManhattanHeuristicSearch
bds_mmEuc = biDirectionalAStarEuclideanHeuristicSearch