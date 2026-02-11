
from robot import * 
import math
import random


nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "Optimizer"
    robot_id = -1
    iteration = 0

    param = []
    bestParam = [0,0,0,0,0,0,0,0]
    it_per_evaluation = 400
    trial = 0

    x_0 = 0
    y_0 = 0
    theta_0 = 0 # in [0,360]
    score_best=0
    cell_size = 4

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=0,it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.param = [random.randint(-1, 1) for i in range(8)]
        self.it_per_evaluation = it_per_evaluation
        self.visited=set()
        super().__init__(x_0, y_0, theta_0, name=name, team=team)
        
    def reset(self):
        super().reset()
    
    def get_cell(self, x, y):
        x = max(0, min(99, x))
        y = max(0, min(99, y))
        return (int(x // self.cell_size), int(y // self.cell_size))


    def score(self):
        return len(self.visited)

    nb_essai=0

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # cet exemple montre comment générer au hasard, et évaluer, des stratégies comportementales
        # Remarques:
        # - la liste "param", définie ci-dessus, permet de stocker les paramètres de la fonction de contrôle
        # - la fonction de controle est une combinaison linéaire des senseurs, pondérés par les paramètres (c'est un "Perceptron")

        # toutes les X itérations: le robot est remis à sa position initiale de l'arène avec une orientation aléatoire
        self.visited.add(self.get_cell(self.x, self.y))

        if self.iteration % self.it_per_evaluation == 0:

                if self.iteration > 0:
                    print ("\tbest param      =", self.bestParam)
                    print ("\tscore           =",self.score())
                    print ("\tparameters           =",self.param)
                    print ("\ttranslations         =",self.log_sum_of_translation,"; rotations =",self.log_sum_of_rotation) # *effective* translation/rotation (ie. measured from displacement)
                    print ("\tdistance from origin =",math.sqrt((self.x-self.x_0)**2+(self.y-self.y_0)**2))
                s= self.score()
                if self.score_best < s:
                    self.score_best = s
                    self.bestParam=self.param
                self.visited.clear()
                if self.nb_essai ==2 :
                    self.param = [random.randint(-10, 10) for i in range(8)]
                    self.trial = self.trial + 1
                    print ("Trying strategy no.",self.trial)
                    self.iteration = self.iteration + 1
                    self.nb_essai=0
                    return 0, 0, True # ask for reset
                else :
                    self.theta = random.randint(0,360)
                    self.nb_essai=self.nb_essai+1
                    self.trial = self.trial + 1

                    

        # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
        translation = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rotation = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )
        
        
        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)

        self.iteration = self.iteration + 1        

        return translation, rotation, False
