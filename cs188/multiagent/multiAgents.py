# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        currentFoodList = currentGameState.getFood().asList()
        newFoodList = newFood.asList()
        ghostPositions = successorGameState.getGhostPositions()
        distance = float("inf")
        scared = newScaredTimes[0] > 0
        for ghost in ghostPositions:
            d = manhattanDistance(ghost, newPos)
            distance = min(d, distance)
        distance2 = float("inf")        
        for food in newFoodList:
            d = manhattanDistance(food, newPos)
            distance2 = min(d, distance2)
        count = len(newFoodList)
        cond = len(newFoodList) < len(currentFoodList)
        if cond:
            count = 10000
        if distance < 2:
            distance = -100000
        else:
            distance = 0
        if count == 0:
            count = -1000
        if scared:
            distance = 0
        return distance + 1.0/distance2 + count - successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimax(agentIndex, gameState, depth, evalFunc):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return evalFunc(gameState)
            actions = gameState.getLegalActions(agentIndex)
            if agentIndex == 0:
                x = float("-inf")
            else:
                x = float("inf")
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == 0:
                    x = max(x, minimax(agentIndex + 1, successor, depth, evalFunc))
                elif agentIndex < gameState.getNumAgents() - 1:
                    x = min(x, minimax(agentIndex + 1, successor, depth, evalFunc))
                else:
                    x = min(x, minimax(0, successor, depth - 1, evalFunc))
            return x

        maximum = float("-inf")
        actions = gameState.getLegalActions(0)
        solution = actions[0]
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            temp = minimax(1, successor, self.depth, self.evaluationFunction)
            if temp > maximum:
                maximum = temp
                solution = action
        return solution

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def minimaxPrune(agentIndex, gameState, depth, evalFunc, alpha, beta):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return evalFunc(gameState)   
            if agentIndex == 0:
                x = float("-inf")
            else:
                x = float("inf")
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:    
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == 0:      
                    x = max(x, minimaxPrune(agentIndex + 1, successor, depth, evalFunc, alpha, beta))
                    if x > beta:
                        return x
                    alpha = max(alpha, x)
                elif agentIndex < gameState.getNumAgents() - 1:     
                    x = min(x, minimaxPrune(agentIndex + 1, successor, depth, evalFunc, alpha, beta))
                    if x < alpha:
                        return x
                    beta = min(beta, x)
                else:
                    x = min(x, minimaxPrune(0, successor, depth - 1, evalFunc, alpha, beta))
                    if x < alpha:
                        return x
                    beta = min(beta, x)
            return x

        maximum = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        actions = gameState.getLegalActions(0)
        solution = actions[0]
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            temp = minimaxPrune(1, successor, self.depth, self.evaluationFunction, alpha, beta)            
            if temp > maximum:
                maximum = temp
                solution = action
            if maximum > beta:
                return solution
            alpha = max(alpha, maximum)
        return solution

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def minimax(agentIndex, gameState, depth, evalFunc):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return evalFunc(gameState)
            actions = gameState.getLegalActions(agentIndex)
            if agentIndex == 0:
                x = float("-inf")
            else:
                x = float(0)
            count = 0
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == 0:
                    x = max(x, minimax(agentIndex + 1, successor, depth, evalFunc))
                elif agentIndex < gameState.getNumAgents() - 1:
                    x = x + minimax(agentIndex + 1, successor, depth, evalFunc)
                    count += 1
                else:
                    x = x + minimax(0, successor, depth - 1, evalFunc)
                    count += 1
            if agentIndex != 0:
                x = x / count
            return x

        maximum = float("-inf")
        actions = gameState.getLegalActions(0)
        solution = actions[0]
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            temp = minimax(1, successor, self.depth, self.evaluationFunction)
            if temp > maximum:
                maximum = temp
                solution = action
        return solution
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    food = currentGameState.getFood()
    foodList = food.asList()
    pos = currentGameState.getPacmanPosition()        
    ghostStates = currentGameState.getGhostStates()
    foodList = food.asList()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPositions = currentGameState.getGhostPositions()
    distance = float("inf")
    scared = 0
    times = 1
    for time in scaredTimes:
        times += time
        if time > 2:
            scared += 1
    avgDist = 1
    ghostCount = 0
    for ghost in ghostPositions:
        d = manhattanDistance(ghost, pos)
        avgDist += d
        if d <= 15:
            ghostCount+=1
        distance = min(d, distance)
    avgDist = float(avgDist)/len(ghostPositions)
    distance2 = float("inf")  
    for food in foodList:
        d = manhattanDistance(food, pos)
        distance2 = min(d, distance2)  
    distance2 += 1
    count = len(foodList) + 1
    legalMoves = len(currentGameState.getLegalActions(0)) +1        
    if distance < 2:
        distance = -100000
    else:
        distance = 0
    score = currentGameState.getScore() + 1
    return distance + 1.0/distance2 + 10000.0/count - 50000*ghostCount + 50000*scared - 1000/times + 1.0/avgDist + 1000.0*score
# Abbreviation
better = betterEvaluationFunction

