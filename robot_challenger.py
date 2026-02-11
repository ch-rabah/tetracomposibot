# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Rabah CHELALI 21315151
#  Prénom Nom No_étudiant/e : Anis SAFAR 21304587
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 
import math

nb_robots = 0

class Robot_player(Robot):

    team_name = "Challenger_Rabah/_Anis"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)


    def strategy3(self, sensors, sensor_view, sensor_robot, sensor_team):
        # strategie qui permet de suivre le mur pour faire le tour de l'arène
        tran = 0.6 * sensors[sensor_front] + 0.2
        rot  = (sensors[sensor_left] + sensors[sensor_front_left]) - (sensors[sensor_right] + sensors[sensor_front_right])
        return tran, rot
    
    def strategy2(self, sensors, sensor_view, sensor_robot, sensor_team):
        # strategie qui permet d'eviter un obstacle
        #tran =  sensors[sensor_front] + 0.2
        #rot = 1 - sensors[sensor_front] + sensors[sensor_left] + sensors[sensor_front_left] - sensors[sensor_right] - sensors[sensor_front_right]
        translation = sensors[sensor_front]*0.1+0.2
        rotation = 0.2 * sensors[sensor_left] + 0.2 * sensors[sensor_front_left] - 0.2 * sensors[sensor_right] - 0.2 * sensors[sensor_front_right] + (random.random()-0.5)*1. #+ sensors[sensor_front] * 0.1
        
        return tran, rot

    def strategy1(self, sensors, sensor_view, sensor_robot, sensor_team):

        self.param=[-3, 5, 9, 8, 4, 10, -5, -8]#[1, 8, -8, 5, 3, 5, 2, -10]
        tran = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rot = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )
        return tran, rot

    def strategy4(self, sensors, sensor_view, sensor_robot, sensor_team):
        l=[[7,-8,-6.5,-8,0,8.5,8,8.5],[-3, 5, 9, 8, 4, 10, -5, -8],[1, 8, -8, 5, 3, 5, 2, -10]]
        n=random.randint(0,2)
        param=l[n]
        tran = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rot = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )
        return tran, rot


   


    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        
        sensor_to_wall = [] #liste des sensors en ne prennant en compte que les murs
        sensor_to_robot = [] #liste des sensors en ne prennant en compte que les robots
        sensor_to_advrobot= [] #liste des sensors en ne prennant en compte que les robots adverses
        
        for i in range (0,8): #remplissage des listes 
            if  sensor_view[i] == 1:
                sensor_to_wall.append(sensors[i])
                sensor_to_robot.append(1.0)
                sensor_to_advrobot.append(1.0) 
            elif sensor_view[i] ==2:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(sensors[i])
                if sensor_team[i]!=self.team_name:
                    sensor_to_advrobot.append(sensors[i])
                else:
                    sensor_to_advrobot.append(1.0) 
                                    
            else:
                sensor_to_wall.append(1.0)  
                sensor_to_robot.append(1.0)
                sensor_to_advrobot.append(1.0)

        def is_near():
            return sensors[sensor_front] <= 0.15 or sensors[sensor_front_left] <= 0.15 or sensors[sensor_front_right] <= 0.15
        def is_wall_far():
            return sensor_to_wall[sensor_right] >= 0.8 and sensor_to_wall[sensor_rear_right] >= 0.8
        def is_adv_near():
            return len([1 for i in sensor_to_advrobot if i != 1.0 ]) >=1
        
        def not_adv_near():
            for i in range(8):
                if sensors[i] <= 0.2 and sensor_to_advrobot[i] == 1.0 :
                    return True
            return False
        
        def is_ally_near() :
            for i in range(8):
                if sensor_to_robot[i] <= 0.2 and sensor_team[i] == self.team_name:
                    return True
            return False

        def danger_list(sensor_list):
            w =  [7, -8, -6, -8, 0, 8, 6, 8]
            rotation = 0
            for i in range(8):
                rotation += ((1 - sensor_list[i]) * w[i])*(random.random()*0.2)
            return rotation 

        def follow_wall(sensor_list):
            w = [6.2,-8,5,0,0,0,-6.8,9.2]
            rotation = 0
            for i in range(8):
                rotation += (1-sensor_list[i])*w[i]
            return rotation
        
        def follow_list(sensor_list):
            w = [7.0, -8, -6.5, -8, 0, 8.5, 8, 8.5]
            rotation = 0
            for i in range(8):
                rotation += (1-sensor_list[i])*w[i]
            return rotation

        if self.memory == 0:
            if self.robot_id==0:
                self.memory = 1
            else :
                self.memory = 0

        
        translation = sensors[sensor_front] + sensors[sensor_front_left] + sensors[sensor_front_right]
        if self.memory ==1:#mode passifique suivi de mur
            if is_near():
                rotation = danger_list(sensor_to_wall)
                translation = sensors[sensor_front]*0.5+0.2
            elif is_wall_far():
                rotation = 0.3*follow_list(sensor_to_wall)
                translation = sensors[sensor_front]*0.5+0.2
            else:
                rotation = 0.5 * follow_wall(sensor_to_wall)
                translation = sensors[sensor_front]*0.9+0.3
            
            if random.random() < 0.02:   
                self.memory = 2

        else:#mode aggressif 
            if not_adv_near():
                rotation = danger_list(sensors)
            else:
                if is_adv_near():
                    if is_ally_near():
                        #evite que deux robots en bloque qu'un seul
                        rotation = danger_list(sensors)
                    else:
                        rotation = follow_list(sensor_to_advrobot)
                else:
                    rotation = danger_list(sensors)
        
            if is_ally_near():
                #evite que deux robots en bloque qu'un seul
                rotation = danger_list(sensors)

            if random.random() < 0.02:   
                self.memory = 1

        
        return translation, rotation, False


