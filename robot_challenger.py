# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Rabah CHELALI 21315151
#  Prénom Nom No_étudiant/e : _________
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 

nb_robots = 0

class Robot_player(Robot):

    team_name = "Challenger_Rabah"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    
    def strategy1(self, sensors, sensor_view, sensor_robot, sensor_team):
        # strategie qui permet de suivre le mur pour faire le tour de l'arène

        

        tran = 0.2 +  sensors[sensor_front]   # avance toujours, plus si c'est libre devant
        rot  = 1 - sensors[sensor_front] + sensors[sensor_left] - sensors[sensor_right] #+ (random.random()-0.5)*1
        return tran, rot
    
    def strategy2(self, sensors, sensor_view, sensor_robot, sensor_team):
        # strategie qui permet d'eviter un obstacle
        tran =  sensors[sensor_front] + 0.2
        rot = 1 - sensors[sensor_front] + sensors[sensor_left] + sensors[sensor_front_left] - sensors[sensor_right] - sensors[sensor_front_right]

        return tran, rot

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        k = self.robot_id % 2

        sensor_to_wall = []
        sensor_to_robot = []
        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i] )
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        if k == 0:
            translation, rotation = self.strategy1(sensors, sensor_view, sensor_robot, sensor_team)
        elif k == 1:
            translation, rotation = self.strategy2(sensors, sensor_view, sensor_robot, sensor_team)
        elif k == 2:
            translation, rotation = self.strategy3(sensors, sensor_view, sensor_robot, sensor_team)
        else:
            translation, rotation = self.strategy4(sensors, sensor_view, sensor_robot, sensor_team)

        return translation, rotation, False

    

