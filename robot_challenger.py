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
import random

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


    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        
        sensor_to_wall = [] #liste des sensors des murs uniquement
        sensor_to_robot = [] #liste des sensors des robots (adv/team)
        sensor_to_advrobot= [] #liste des sensors des robots adv
        
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
            """retourne vrai si un mur/robot est proche"""
            return sensors[sensor_front] <= 0.15 or sensors[sensor_front_left] <= 0.15 or sensors[sensor_front_right] <= 0.15

        def is_wall_far():
            """retourne vrai si un mur est un peu loin"""
            return sensor_to_wall[sensor_right] >= 0.7 and sensor_to_wall[sensor_rear_left] >= 0.7
        
        def is_adv_near():
            """retourne vrai si un robot adversaire est proche"""
            return len([1 for i in sensor_to_advrobot if i != 1.0 ]) >=1
        
        def not_adv_near():
            """retourne vrai si y a un mur ou un robot de meme equipe est proche mais pas un robot adversaire"""
            for i in range(8):
                if sensors[i] <= 0.2 and sensor_to_advrobot[i] == 1.0 :
                    return True
            return False
        
        def is_teammate_near() :
            """retourne vrai si un robot de meme equipe est proche""" 
            for i in range(8):
                if sensor_to_robot[i] <= 0.2 and sensor_team[i] == self.team_name:
                    return True
            return False

        def danger_list(sensor_list):
            """permet d'eviter un objet dont le sensor est donné en parametre"""
            w =  [7, -8, -6, -8, 0, 8, 6, 8]
            rotation = 0
            for i in range(8):
                rotation += ((1 - sensor_list[i]) * w[i])*(random.random()*0.2)
            return rotation 

        
        


        def follow_wall(sensor_list):
            """permet de suivre un mur"""
            w = [6.2,-8,5,0,0,0,-6.8,9.2]
            rotation = 0
            for i in range(8):
                rotation += (1-sensor_list[i])*w[i]
            return rotation
        
        def follow_list(sensor_list):
            """permet de suivre un objet dont le sensor est donné en parametre"""
            w = [7.0, -8, -6.5, -8, 0, 8.5, 8, 8.5]
            rotation = 0
            for i in range(8):
                rotation += (1-sensor_list[i])*w[i]
            return rotation

        def is_blocked() :
            """retourne vrai si le robot est bloque"""
            return (sensors[sensor_front] <= 0.08 and sensors[sensor_front_left] <= 0.12 and sensors[sensor_front_right] <= 0.12)

        if self.memory == 0:
            if self.robot_id==0:
                self.memory = 1 # un robot qui suit le mur 
            else :
                self.memory = 2 # mode attaque

        translation = sensors[sensor_front] + sensors[sensor_front_left] + sensors[sensor_front_right]
        
        if self.memory != 3 and is_blocked():
            self.memory = 3 #mode anti-bloquage
        
        
        

        
        if self.memory == 3:#mode anti-bloquage
            translation = -0.2 #recule
            rotation = danger_list(sensor_to_wall)* (0.8 + random.random()*0.4)

            # sortir de mode anti-bloquage
            if sensors[sensor_front] > 0.25 and sensors[sensor_front_left] > 0.25 and sensors[sensor_front_right] > 0.25  :
                self.memory = 1 if self.robot_id == 0 else 2

        
        elif self.memory ==1:#mode suivi de mur
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

        else:#mode attaque
            if not_adv_near():
                rotation = danger_list(sensors)
            else:
                if is_adv_near():
                    if is_teammate_near():
                        #evite que deux robots en bloque qu'un seul
                        rotation = danger_list(sensors)
                    else:
                        rotation = follow_list(sensor_to_advrobot)
                else:
                    rotation = danger_list(sensors)
        
            if is_teammate_near():
                #evite que deux robots en bloque qu'un seul
                rotation = danger_list(sensors)

            if random.random() < 0.08:   
                self.memory = 1

        
        return translation, rotation, False


