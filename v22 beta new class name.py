import pygame as py
import matplotlib.pyplot as plt
import math
import numpy as np
import io
from PIL import Image
import os
import sys
import time
#set up colour constant,display window and axis in the window
py.display.set_caption("Prejoctile Practice NEA")
LIGHT_BLACK=(59,68,75)
GREEN=(152,251,152)
BLUE=(135,206,250)
BLACK=(0,0,0)
WHITE=(255,255,255)
GREY=(175,161,157)
DARK_GREY=(89,89,89)
DARK_BLUE=(0,0,139)
RED=(255,99,71)
DARK_RED=(139,0,0)
BROWN=(88,57,39)
DARK_BROWN=(38,37,16)
YELLOW=(255,255,0)
curve_cursor_colour=(3, 32, 252)#darker Blue
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as py
color_inactive_button = py.Color('lightskyblue3')
color_active_button = py.Color('dodgerblue2')
window = py.display.set_mode((1500,700))
window.fill(GREY)
py.draw.rect(window,DARK_GREY,py.Rect(1100,0,400,700))
py.draw.rect(window,BLACK,py.Rect(100,10,5,650))
py.draw.rect(window,BLACK,py.Rect(100,655,950,5))
py.font.init()
clock=py.time.Clock()
#set up texts font
font = py.font.SysFont(None, 43)
width_of_curve=3

#use calss to store the Projectile and the data, there are two type of projeectile ,seperate by frictionless and frictional 
class Projectile:
    @classmethod
    def find_displacement(cls,height,data,t_pass):
        x=data.velocity*math.cos(data.angle)*t_pass
        y=height+data.velocity*math.sin(data.angle)*t_pass-(0.5*data.g*(t_pass**2))
        return x,y

    #define the attributes of the Projectile
    def __init__(self,height,velocity,angle,option=False,drag=0.47,mass=5,diameter=0.35,air_density=1.225):
        if option==False:
            self.drag_coff=0
            self.mass=0
            self.resistance=0
            self.air_density=0
            self.k=0
            angle=math.radians(angle)
            self.g=9.81
            self.velocity=velocity
            self.angle=angle
            self.v_x=velocity*math.cos(angle)
            self.v_y=velocity*math.sin(angle)
            self.t=2*velocity*math.sin(angle)/self.g
            self.acceleration_overtime_x=[]
            self.acceleration_overtime_y=[]
            x=[]
            y=[]
            self.all_time_step=[]
            self.velocity_overtime_x=[]
            self.velocity_overtime_y=[]
            for t_pass in np.arange(0,1000,0.01):
                x_at_time,y_at_time=Projectile.find_displacement(height,self,t_pass)
                if y_at_time<0:
                    self.total_time=t_pass
                    break
                self.acceleration_overtime_x.append(0)
                self.acceleration_overtime_y.append(-self.g)
                self.velocity_overtime_x.append(self.v_x)
                self.velocity_overtime_y.append(self.v_y-self.g*t_pass)
                self.all_time_step.append(t_pass)
                x.append(x_at_time) 
                y.append(y_at_time)
            
            self.displacement_x,self.displacement_y=x,y


        else:
            angle=math.radians(angle)
            self.drag_coff=drag
            self.mass=mass
            self.resistance=drag/mass
            self.air_density=air_density
            self.k=(air_density*drag*math.pi*(diameter/2)**2)/(2*mass)
            self.g=9.81
            self.velocity=velocity
            self.angle=angle
            self.v_x=velocity*math.cos(angle)
            self.v_y=velocity*math.sin(angle)
            self.a_x=-self.k*self.v_x*velocity
            self.a_y=-self.g-(self.k*self.v_y*velocity)
            self.t=(2*velocity*math.sin(angle)/self.g)-((air_density*drag*math.pi*((diameter/2)**2)*(velocity**2)*math.sin(angle))/(3*mass*self.g**2))
            x=[]
            y=[]
            self.velocity_overtime_x=[]
            self.velocity_overtime_y=[]
            self.acceleration_overtime_x=[]
            self.acceleration_overtime_y=[]
            initial_x=0
            initial_y=height
            v_x=self.v_x
            v_y=self.v_y
            self.total_time=0
            self.all_time_step=[]
            t_pass=0.01
            while initial_y>=0:
                a_x=-self.k*math.sqrt(v_x**2+v_y**2)*v_x
                a_y=-self.g-self.k*math.sqrt(v_x**2+v_y**2)*v_y


                initial_x=initial_x+v_x*t_pass
                initial_y=initial_y+v_y*t_pass

                v_x+=a_x*t_pass
                v_y+=a_y*t_pass
                self.velocity_overtime_x.append(v_x)
                self.velocity_overtime_y.append(v_y)
                self.acceleration_overtime_x.append(a_x)
                self.acceleration_overtime_y.append(a_y)
                x.append(initial_x)
                y.append(initial_y)
                self.total_time+=t_pass
                self.all_time_step.append(self.total_time)

            self.displacement_x,self.displacement_y=x,y   

#key function that draw the path of the Projectile, subfunction is create for drawing vectors
def draw_projectile(mass,diameter,no_repeated_curve_check,height,acceleration_vector,velocity_vector,shifting,animate,multi_launch_data,scale_factor_x,scale_factor_y,velocity,angle,air_res_switch=False,drag=0):

        
    def draw_velocity_x(air_res_switch,projectile_data,scale_velocity_x=0):
        
        width_of_velocity_vector=projectile_data.velocity_overtime_x[i]*scale_velocity_x
        #prevent the x vleocity cross into the dark grey area
        if air_res_switch:
            if projectile_data.displacement_x[i]*scale_factor_x+shifting+width_of_velocity_vector>1095:
                py.draw.rect(window,YELLOW,py.Rect(4+projectile_data.displacement_x[i]*scale_factor_x+shifting ,655-projectile_data.displacement_y[i]*scale_factor_y,1050-(projectile_data.displacement_x[i]*scale_factor_x+shifting),5))
            else:
                py.draw.rect(window,YELLOW,py.Rect(4+projectile_data.displacement_x[i]*scale_factor_x+shifting ,655-projectile_data.displacement_y[i]*scale_factor_y,  width_of_velocity_vector,5))

    def draw_velocity_y(air_res_switch,projectile_data,scale_velocity_y):    
        height_of_velocity_vector=projectile_data.velocity_overtime_y[i]*scale_velocity_y
        if height_of_velocity_vector<0:
            py.draw.rect(window,YELLOW,py.Rect(2+projectile_data.displacement_x[i]*scale_factor_x+shifting ,655-projectile_data.displacement_y[i]*scale_factor_y,5,-height_of_velocity_vector))
        else:
            py.draw.rect(window,YELLOW,py.Rect(2+projectile_data.displacement_x[i]*scale_factor_x+shifting ,-height_of_velocity_vector+(655-projectile_data.displacement_y[i]*scale_factor_y),5,height_of_velocity_vector))

    def draw_accelaltion_x(air_res_switch,projectile_data,scale_acceleration_x=0):
        width_of_acceleration_vector=projectile_data.acceleration_overtime_x[i]*scale_acceleration_x
        #prevent the x vector cross into the dark grey area
        if air_res_switch:
            if projectile_data.displacement_x[i]*scale_factor_x+shifting+width_of_acceleration_vector>1095:
                py.draw.rect(window,DARK_RED,py.Rect(4+projectile_data.displacement_x[i]*scale_factor_x+shifting ,655-projectile_data.displacement_y[i]*scale_factor_y,1050-(projectile_data.displacement_x[i]*scale_factor_x+shifting),5))
            else:
                py.draw.rect(window,DARK_RED,py.Rect(4+projectile_data.displacement_x[i]*scale_factor_x+shifting+width_of_acceleration_vector ,655-projectile_data.displacement_y[i]*scale_factor_y,  -width_of_acceleration_vector,5))
    def draw_accelaltion_y(air_res_switch,projectile_data,scale_acceleration_y):    
        height_of_acceleration_vector=projectile_data.acceleration_overtime_y[i]*scale_acceleration_y
        if height_of_acceleration_vector<0:
            py.draw.rect(window,DARK_RED,py.Rect(2+projectile_data.displacement_x[i]*scale_factor_x+shifting ,655-projectile_data.displacement_y[i]*scale_factor_y,5,-height_of_acceleration_vector))
        else:
            py.draw.rect(window,DARK_RED,py.Rect(2+projectile_data.displacement_x[i]*scale_factor_x+shifting ,-height_of_acceleration_vector+(655-projectile_data.displacement_y[i]*scale_factor_y),5,height_of_acceleration_vector))
#a function for undating the axis so the curve doesn't cross the axis adn the area outside of it
    def update_axis():
        py.draw.rect(window,BLACK,py.Rect(100,10,5,650))
        py.draw.rect(window,BLACK,py.Rect(100,655,950,5))
        py.draw.rect(window,GREY,py.Rect(0,0,95,700))
        #py.display.flip()
    if air_res_switch==True:
        projectile_data=Projectile(height,velocity,angle,air_res_switch,drag,mass,diameter)
    else:
        projectile_data=Projectile(height,velocity,angle,air_res_switch,0,mass,diameter)

    #check if there are repeated curve with same variables, only store the curve if there are no repeated
    if (height,velocity,angle,air_res_switch,drag,mass,diameter) not in no_repeated_curve_check:
        no_repeated_curve_check.append((height,velocity,angle,air_res_switch,drag,mass,diameter))

        multi_launch_data[len(multi_launch_data)]=(projectile_data.displacement_x,projectile_data.displacement_y,projectile_data.all_time_step,scale_factor_x,scale_factor_y,shifting,projectile_data.velocity_overtime_x,projectile_data.velocity_overtime_y)


        #create scale factor for the first curve so it fits in the axis
        if scale_factor_x==0 and max(multi_launch_data[0][1])!=0 and max(multi_launch_data[0][0])!=0:
        
            scale_factor_x=950/max(multi_launch_data[0][0])
            scale_factor_y=650/max(multi_launch_data[0][1])
        elif max(multi_launch_data[0][0])==0:
            scale_factor_x=10
            scale_factor_y=10

        #create suitable scale factor for the vectors
        for i in range(len(projectile_data.displacement_x)-1):
            if air_res_switch==True:
                scale_acceleration_x=100
                scale_acceleration_y=10

            if air_res_switch==True:
                scale_velocity_x=4
                scale_velocity_y=4
            else:
                scale_velocity_x=0
                scale_velocity_y=4
                scale_acceleration_x=0
                scale_acceleration_y=10
            Draw=True
            #check if user wants animation or not
            if animate:
                #only draw the point if the y displacement  is larger than 0
                if projectile_data.displacement_y[i]>0:
                    #condition to check if the curve is inside the axis, if not the drawing will stop
                    if (projectile_data.displacement_x[i]*scale_factor_x+shifting>1050) or (projectile_data.displacement_x[i]*scale_factor_x+shifting>1050 and 660-projectile_data.displacement_y[i]*scale_factor_y<10):
                        Draw=False
                        #pass
                    elif projectile_data.displacement_x[i]*scale_factor_x+shifting<105 or 660-projectile_data.displacement_y[i]*scale_factor_y>655:
                        Draw=False
                        #pass
                    if Draw==True:
                        py.draw.rect(window,GREY,py.Rect(95,660,1000,100))
                        py.draw.rect(window,GREY,py.Rect(1055,0,45,655))
                        #check if velocity vector is on
                        if velocity_vector==True or acceleration_vector==True:
                            if air_res_switch==True:
                                py.draw.rect(window,GREY,py.Rect(0,0,1100,700))
                                update_axis()
                                if len(multi_launch_data)!=1 and len(multi_launch_data)!=0:
                                    for draw_each_curve in range(len(multi_launch_data)-1):
                                        for curve_datil in range(len(multi_launch_data[draw_each_curve][1])-1):
                                            Draw=True
                                            if multi_launch_data[draw_each_curve][1][curve_datil]>0:
                                                if (multi_launch_data[draw_each_curve][0][curve_datil]*scale_factor_x+shifting>1050) or (multi_launch_data[draw_each_curve][0][curve_datil]*scale_factor_x+shifting>1050 and 660-multi_launch_data[draw_each_curve][1][curve_datil]*scale_factor_y>660) or 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_factor_y>660:
                                                    Draw=False
                                                    pass
                                                elif multi_launch_data[draw_each_curve][0][curve_datil]*scale_factor_x+shifting<105 or 660-multi_launch_data[draw_each_curve][1][curve_datil]*scale_factor_y>655:
                                                    Draw=False
                                                    pass
                                                elif Draw==True:
                                                    py.draw.line(window, BLACK, (multi_launch_data[draw_each_curve][0][curve_datil]*scale_factor_x+shifting,660-multi_launch_data[draw_each_curve][1][curve_datil]*scale_factor_y),  (multi_launch_data[draw_each_curve][0][curve_datil+1]*scale_factor_x+shifting,660-multi_launch_data[draw_each_curve][1][curve_datil+1]*scale_factor_y), width=width_of_curve)
                                        py.draw.rect(window,GREY,py.Rect(95,660,1000,100))
                                        py.draw.rect(window,GREY,py.Rect(1055,0,45,700))
                                #draw the previous line of the curve so it doesn't get covered by the vector
                                for a in range(i-1):
                                    py.draw.line(window, BLACK, (projectile_data.displacement_x[a]*scale_factor_x+shifting,660-projectile_data.displacement_y[a]*scale_factor_y),  (projectile_data.displacement_x[a+1]*scale_factor_x+shifting,660-projectile_data.displacement_y[a+1]*scale_factor_y),width=width_of_curve)  
                                if velocity_vector==True:
                                    draw_velocity_x(air_res_switch,projectile_data,scale_velocity_x)
                                    draw_velocity_y(air_res_switch,projectile_data,scale_velocity_y)
                                if acceleration_vector==True:
                                    draw_accelaltion_x(air_res_switch,projectile_data,scale_acceleration_x)
                                    draw_accelaltion_y(air_res_switch,projectile_data,scale_acceleration_y)
                                py.draw.line(window, BLACK, (projectile_data.displacement_x[i]*scale_factor_x+shifting,660-projectile_data.displacement_y[i]*scale_factor_y),  (projectile_data.displacement_x[i+1]*scale_factor_x+shifting,660-projectile_data.displacement_y[i+1]*scale_factor_y),width=width_of_curve)                  
                                py.draw.rect(window,GREY,py.Rect(95,660,1000,100))
                                py.draw.rect(window,GREY,py.Rect(1055,0,10,655))
                                py.draw.rect(window,GREY,py.Rect(0,0,100,700))
                                py.display.flip()


                            else:
                                py.draw.rect(window,GREY,py.Rect(0,0,1100,700))
                                update_axis()
                                if len(multi_launch_data)!=1 and len(multi_launch_data)!=0:
                                    for draw_each_curve in range(len(multi_launch_data)-1):
                                        for curve_datil in range(len(multi_launch_data[draw_each_curve][1])-1):
                                            Draw=True
                                            if multi_launch_data[draw_each_curve][1][curve_datil]>0:
                                                #pygame.draw.circle(screen,(self.__colour),(self.__points_list[i]),5)
                                                if (multi_launch_data[draw_each_curve][0][curve_datil]*scale_factor_x+shifting>1050) or (multi_launch_data[draw_each_curve][0][curve_datil]*scale_factor_x+shifting>1050 and 660-multi_launch_data[draw_each_curve][1][curve_datil]*scale_factor_y>660) or 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_factor_y>660:
                                                    Draw=False
                                                    pass
                                                elif multi_launch_data[draw_each_curve][0][curve_datil]*scale_factor_x+shifting<105 or 660-multi_launch_data[draw_each_curve][1][curve_datil]*scale_factor_y>655:
                                                    Draw=False
                                                    pass
                                                elif Draw==True:
                                                    py.draw.line(window, BLACK, (multi_launch_data[draw_each_curve][0][curve_datil]*scale_factor_x+shifting,660-multi_launch_data[draw_each_curve][1][curve_datil]*scale_factor_y),  (multi_launch_data[draw_each_curve][0][curve_datil+1]*scale_factor_x+shifting,660-multi_launch_data[draw_each_curve][1][curve_datil+1]*scale_factor_y),width=width_of_curve)
                                        py.draw.rect(window,GREY,py.Rect(95,660,1000,100))
                                        py.draw.rect(window,GREY,py.Rect(1055,0,45,700))

                                #py.display.flip()
                                for a in range(i-1):
                                    py.draw.line(window, BLACK, (projectile_data.displacement_x[a]*scale_factor_x+shifting,660-projectile_data.displacement_y[a]*scale_factor_y),  (projectile_data.displacement_x[a+1]*scale_factor_x+shifting,660-projectile_data.displacement_y[a+1]*scale_factor_y),width=width_of_curve)  
                                if velocity_vector==True:
                                    draw_velocity_x(air_res_switch,projectile_data,scale_velocity_x)
                                    draw_velocity_y(air_res_switch,projectile_data,scale_velocity_y)
                                if acceleration_vector==True:
                                    draw_accelaltion_y(air_res_switch,projectile_data,scale_acceleration_y)
                                py.draw.line(window, BLACK, (projectile_data.displacement_x[i]*scale_factor_x+shifting,660-projectile_data.displacement_y[i]*scale_factor_y),  (projectile_data.displacement_x[i+1]*scale_factor_x+shifting,660-projectile_data.displacement_y[i+1]*scale_factor_y),width=width_of_curve)                  
                                #time.sleep(projectile_data.total_time/len(projectile_data.displacement_y))
                                py.draw.rect(window,GREY,py.Rect(95,660,1000,100))
                                py.draw.rect(window,GREY,py.Rect(1055,0,10,655))
                                py.display.flip()
                        #condition true if neither vectors are on, draw normal curve
                        else:
                            #make sure the grey area outside the axis is complete and no curve has cross the axis 
                            py.draw.rect(window,GREY,py.Rect(95,660,1000,100))
                            py.draw.rect(window,GREY,py.Rect(1055,0,45,655))
                            py.draw.rect(window,GREY,py.Rect(0,0,1100,700))
                            update_axis()
                            #draw all the previous curves so not only the latest curve is being drawn
                            if len(multi_launch_data)!=1 and len(multi_launch_data)!=0:
                                for draw_each_curve in range(len(multi_launch_data)-1):
                                    for curve_datil in range(len(multi_launch_data[draw_each_curve][1])-1):
                                        Draw=True
                                        if multi_launch_data[draw_each_curve][1][curve_datil]>0:
                                            if (multi_launch_data[draw_each_curve][0][curve_datil]*scale_factor_x+shifting>1050) or (multi_launch_data[draw_each_curve][0][curve_datil]*scale_factor_x+shifting>1050 and 660-multi_launch_data[draw_each_curve][1][curve_datil]*scale_factor_y>660) or 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_factor_y>660:
                                                Draw=False
                                                pass
                                            elif multi_launch_data[draw_each_curve][0][curve_datil]*scale_factor_x+shifting<105 or 660-multi_launch_data[draw_each_curve][1][curve_datil]*scale_factor_y>655:
                                                Draw=False
                                                pass
                                            elif Draw==True:
                                                py.draw.line(window, BLACK, (multi_launch_data[draw_each_curve][0][curve_datil]*scale_factor_x+shifting,660-multi_launch_data[draw_each_curve][1][curve_datil]*scale_factor_y),  (multi_launch_data[draw_each_curve][0][curve_datil+1]*scale_factor_x+shifting,660-multi_launch_data[draw_each_curve][1][curve_datil+1]*scale_factor_y), width=width_of_curve)
                                    py.draw.rect(window,GREY,py.Rect(95,660,1000,100))
                                    py.draw.rect(window,GREY,py.Rect(1055,0,45,700))
                            #draw all the previous part of the curve, make sure the entire curve is complete
                            for a in range(i-1):
                                py.draw.line(window, BLACK, (projectile_data.displacement_x[a]*scale_factor_x+shifting,660-projectile_data.displacement_y[a]*scale_factor_y),  (projectile_data.displacement_x[a+1]*scale_factor_x+shifting,660-projectile_data.displacement_y[a+1]*scale_factor_y),width=width_of_curve)  
                            py.draw.line(window, BLACK, (projectile_data.displacement_x[i]*scale_factor_x+shifting,660-projectile_data.displacement_y[i]*scale_factor_y),  (projectile_data.displacement_x[i+1]*scale_factor_x+shifting,660-projectile_data.displacement_y[i+1]*scale_factor_y),width=width_of_curve)                  
                            py.draw.rect(window,GREY,py.Rect(95,660,1000,100))
                            py.draw.rect(window,GREY,py.Rect(1055,0,10,655))
                            py.draw.rect(window,GREY,py.Rect(0,0,100,700))
                            py.display.flip()

            #if animation is off then only update the window after drawing the entire curve
            else:
                if projectile_data.displacement_y[i]>0:

                    if (projectile_data.displacement_x[i]*scale_factor_x+shifting>1050) or (projectile_data.displacement_x[i]*scale_factor_x+shifting>1050 and 660-projectile_data.displacement_y[i]*scale_factor_y<10):
                        Draw=False
                        pass
                    elif projectile_data.displacement_x[i]*scale_factor_x+shifting<105 or 660-projectile_data.displacement_y[i]*scale_factor_y>655:
                        Draw=False
                        pass
                    elif Draw==True:
                        py.draw.line(window, BLACK, (projectile_data.displacement_x[i]*scale_factor_x+shifting,660-projectile_data.displacement_y[i]*scale_factor_y),  (projectile_data.displacement_x[i+1]*scale_factor_x+shifting,660-projectile_data.displacement_y[i+1]*scale_factor_y),width=width_of_curve)
        py.draw.rect(window,GREY,py.Rect(0,0,1100,700))
        #draw the previous curve 
        for draw_each_curve in range(len(multi_launch_data)):
            for curve_datil in range(len(multi_launch_data[draw_each_curve][1])-1):
                Draw=True
                if multi_launch_data[draw_each_curve][1][curve_datil]>0:
                    if (multi_launch_data[draw_each_curve][0][curve_datil]*scale_factor_x+shifting>1050) or (multi_launch_data[draw_each_curve][0][curve_datil]*scale_factor_x+shifting>1050 and 660-multi_launch_data[draw_each_curve][1][curve_datil]*scale_factor_y>660) or 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_factor_y>660:
                        Draw=False
                        pass
                    elif multi_launch_data[draw_each_curve][0][curve_datil]*scale_factor_x+shifting<105 or 660-multi_launch_data[draw_each_curve][1][curve_datil]*scale_factor_y>655:
                        Draw=False
                        pass
                    elif Draw==True:
                        py.draw.line(window, BLACK, (multi_launch_data[draw_each_curve][0][curve_datil]*scale_factor_x+shifting,660-multi_launch_data[draw_each_curve][1][curve_datil]*scale_factor_y),  (multi_launch_data[draw_each_curve][0][curve_datil+1]*scale_factor_x+shifting,660-multi_launch_data[draw_each_curve][1][curve_datil+1]*scale_factor_y),width=width_of_curve)

        py.display.flip()
        #draw grey box to cover up the curve that is out of the axis
        py.draw.rect(window,GREY,py.Rect(95,660,1000,100))
        py.draw.rect(window,GREY,py.Rect(1055,0,10,655))
        py.draw.rect(window,BLACK,py.Rect(100,10,5,650))
        py.draw.rect(window,BLACK,py.Rect(100,655,950,5))
        py.display.flip()

    return no_repeated_curve_check,multi_launch_data,scale_factor_x,scale_factor_y



#use class to create a button that input text and output value
class Text_input_button:
    #create attributes to store the top left coordinates,width,height and input values
    def __init__(self,x_coor,y_coor,width,height,length_of_text=200):
        self.x_coor=x_coor
        self.y_coor=y_coor
        self.button=py.Rect(x_coor,y_coor,width,height)
        self.button_switch=False
        self.input_value=""
        self.width=width
        self.height=height
        self.length_of_text=length_of_text
    #draw the button 
    def draw_button(self,text=""):
        output=font.render(self.input_value,True,BLACK)
        text_before_box=font.render(text,True,BLACK)
        py.draw.rect(window,BLACK,py.Rect(self.x_coor-2,self.y_coor-2,self.width+4,self.height+4))
        py.draw.rect(window,BLACK,py.Rect(self.x_coor+5,self.y_coor+5,self.width,self.height))
        py.draw.rect(window,WHITE,self.button)
        window.blit(output, (self.x_coor+5,self.y_coor+5))
        window.blit(text_before_box, (self.x_coor-self.length_of_text,self.y_coor+5))
        py.display.update()
    #check if mouse position collidie the button rectangle
    def collide_self(self,event):
        if self.button.collidepoint(event.pos):
            self.button_switch=True
        else:
            self.button_switch=False
    #check input from the keyboard and return the final input value
    def button_input(self,event):
        if event.key == py.K_RETURN:
            return self.input_value
        elif event.key == py.K_BACKSPACE:
            self.input_value = self.input_value[:-1]
        else:
            self.input_value += event.unicode
        return self.input_value
    #draw the input value and update 
    def update_text(self,event):

        if event.type == py.KEYDOWN and self.button_switch==True and len(self.input_value)<4:
            self.input_value=self.button_input(event)
            self.check_input_length()
            self.draw_button()
    #check the input value is integer, if not the value is set to 0
    def check_input_length(self):
        if len(self.input_value)==3:
            self.input_value=self.input_value[:2]
        if not self.input_value.isdecimal():
            self.input_value=""
    #limit the length of the value
    def limit_input(self,limit_value):
        try:
            if int(self.input_value)>limit_value:
                self.input_value="0"
        except:
            pass
    #if no value has been put in, initial value become 0
    def check_empty(self,input_value):
        if input_value=="":
            return "0"
        return input_value

#use class to create button that can turn on and off
class Click_button:
    #store button's top left coordinates, width, height and the button rectangle as as attributes
    def __init__(self,x_coor,y_coor,width,height,length_of_text=110):
        self.x_coor=x_coor
        self.y_coor=y_coor
        self.button=py.Rect(x_coor,y_coor,width,height)
        self.width=width
        self.height=height
        self.length_of_text=length_of_text
    #serval methods of drawing for different types of buttons
    def draw_self_button(self,text=""):
        text_before_box=font.render(text,True,BLACK)
        py.draw.rect(window,DARK_RED,py.Rect(self.x_coor+5,self.y_coor+5,self.width,self.height))
        py.draw.rect(window,RED,self.button)
        window.blit(text_before_box, (self.x_coor-self.length_of_text,self.y_coor+5))
        py.display.update()

    @classmethod
    def draw_button_method2_in_class(cls,data,colour_base,colour,text=""):
        text_before_box=font.render(text,True,BLACK)
        window.blit(text_before_box, (data.x_coor-130,data.y_coor+5))
        py.draw.rect(window,colour_base,py.Rect(data.x_coor+5,data.y_coor+5,data.width,data.height))
        py.draw.rect(window,colour,py.Rect(data.x_coor,data.y_coor,data.width,data.height))
        py.display.update()
    
    def draw_button_method2(self,colour_base,colour,text=" "):
        py.draw.rect(window,colour_base,py.Rect(self.x_coor+5,self.y_coor+5,self.width,self.height))
        py.draw.rect(window,colour,py.Rect(self.x_coor,self.y_coor,self.width,self.height))
        text_before_box=font.render(text,True,BLACK)
        window.blit(text_before_box, (self.x_coor-self.length_of_text,self.y_coor+5))
        py.display.update()
        
    def draw_button_method3(self,colour_base,colour,text="",text_colour=False):
        if text_colour==False:
            font = py.font.SysFont(None, 23)
        else:
            font = py.font.SysFont(None, 43)

        py.draw.rect(window,colour_base,py.Rect(self.x_coor+5,self.y_coor+5,self.width,self.height))
        py.draw.rect(window,colour,py.Rect(self.x_coor,self.y_coor,self.width,self.height))
        if text_colour!=False:
            text_before_box=font.render(text,True,text_colour)
        else:
            text_before_box=font.render(text,True,BLACK)
            
        text_rect = text_before_box.get_rect(center=((self.x_coor+self.width/2),(self.y_coor+self.height/2)-1))
        window.blit(text_before_box, text_rect)
        py.display.update()
    
    #method for increasing the scale factor so the user can "zoom in" the curve
    def scale_up(self,shifting,multi_launch_data,scale_x,scale_y):
        scale_x+=0.5
        scale_y+=0.5
        py.draw.rect(window,GREY,py.Rect(105,0,950,655))
        for draw_each_curve in range(len(multi_launch_data)):
            for curve_datil in range(len(multi_launch_data[draw_each_curve][1])-1):
                Draw=True
                if multi_launch_data[draw_each_curve][1][curve_datil]>0:
                    #pygame.draw.circle(screen,(self.__colour),(self.__points_list[i]),5)
                    if (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting>1050) or (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting>1050 and 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y>660) or 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y>660:
                        Draw=False
                        pass
                    elif multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting<105 or 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y>655:
                        Draw=False
                        pass
                    elif Draw==True:
                        py.draw.line(window, BLACK, (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting,655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y),  (multi_launch_data[draw_each_curve][0][curve_datil+1]*scale_x+shifting,655-multi_launch_data[draw_each_curve][1][curve_datil+1]*scale_y),width=width_of_curve)
        py.draw.rect(window,GREY,py.Rect(95,660,1000,100))
        py.draw.rect(window,GREY,py.Rect(1055,0,45,700))

        py.display.update()
        return scale_x,scale_y
    
    #method for decreasing the scale factor so the user can "zoom out" the curve
    def scale_down(self,shifting,multi_launch_data,scale_x,scale_y):
        if scale_x-1>0:
            scale_x-=0.5
            scale_y-=0.5
        
        if scale_x>0:
            py.draw.rect(window,GREY,py.Rect(105,0,950,655))
            for draw_each_curve in range(len(multi_launch_data)):
                for curve_datil in range(len(multi_launch_data[draw_each_curve][1])-1):
                    Draw=True
                    if multi_launch_data[draw_each_curve][1][curve_datil]>0:
                        #pygame.draw.circle(screen,(self.__colour),(self.__points_list[i]),5) #+100
                        if (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting-5>1050) or (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting-5>1050 and 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y<10):
                            Draw=False
                            pass
                        elif multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting<105 or 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y>655:
                            Draw=False
                            pass
                        elif  multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting< multi_launch_data[draw_each_curve][0][0]*scale_x+shifting<10:
                            Draw=False
                            pass
                        elif Draw==True:
                            py.draw.line(window, BLACK, (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting,655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y),  (multi_launch_data[draw_each_curve][0][curve_datil+1]*scale_x+shifting,655-multi_launch_data[draw_each_curve][1][curve_datil+1]*scale_y),width=width_of_curve)
            py.draw.rect(window,GREY,py.Rect(95,660,1000,100))#clean edge curve
            py.draw.rect(window,GREY,py.Rect(1055,0,45,655))
            py.display.update()
        
        return scale_x,scale_y
    
    #method that decrease the variable "shift" so user can move the curve to the left
    def shift_left(self,shifting,multi_launch_data,scale_x,scale_y):
        shifting-=5
        
        py.draw.rect(window,GREY,py.Rect(105,0,950,655))
        for draw_each_curve in range(len(multi_launch_data)):
            for curve_datil in range(len(multi_launch_data[draw_each_curve][1])-1):
                if multi_launch_data[draw_each_curve][1][curve_datil]>0:
                    Draw=True
                    #pygame.draw.circle(screen,(self.__colour),(self.__points_list[i]),5)
                    if (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting-5>1050) or (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting-5>1050 and 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y<10):
                        Draw=False
                        pass
                    elif multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting<105 or 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y>655:
                        Draw=False
                        pass
                    elif  multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting< multi_launch_data[draw_each_curve][0][0]*scale_x+shifting<10:
                        Draw=False
                        pass
                    elif Draw==True:
                        py.draw.line(window, BLACK, (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting,655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y),  (multi_launch_data[draw_each_curve][0][curve_datil+1]*scale_x+shifting,655-multi_launch_data[draw_each_curve][1][curve_datil+1]*scale_y),width=width_of_curve)
            py.draw.rect(window,GREY,py.Rect(95,660,1000,100))#clean edge curve
            py.draw.rect(window,GREY,py.Rect(1055,0,10,655))
        py.display.flip()
        return shifting
    
    #method that increase the variable "shift" so user can move the curve to the right
    def shift_right(self,shifting,multi_launch_data,scale_x,scale_y):
        shifting+=5
        py.draw.rect(window,GREY,py.Rect(105,0,950,655))
        for draw_each_curve in range(len(multi_launch_data)):
            for curve_datil in range(len(multi_launch_data[draw_each_curve][1])-1):
                Draw=True
                if multi_launch_data[draw_each_curve][1][curve_datil]>0:
                    #pygame.draw.circle(screen,(self.__colour),(self.__points_list[i]),5)
                    if (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting-5>1050) or (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting-5>1050 and 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y<10):
                        Draw=False
                        pass
                    elif multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting<105 or 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y>655:
                        Draw=False
                        pass
                    elif  multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting< multi_launch_data[draw_each_curve][0][0]*scale_x+shifting<10:
                        Draw=False
                        pass
                    elif Draw==True:
                        py.draw.line(window, BLACK, (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting,655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y),  (multi_launch_data[draw_each_curve][0][curve_datil+1]*scale_x+shifting,655-multi_launch_data[draw_each_curve][1][curve_datil+1]*scale_y),width=width_of_curve)
        py.draw.rect(window,GREY,py.Rect(95,660,1000,100))#clean edge curve
        py.draw.rect(window,GREY,py.Rect(1055,0,10,655))
        py.display.flip()
        return shifting
        
    #method that refresh the axis and the curve and the dictionary "multi_launch_data", which means all the previous curve would disappear    
    def refresh_page(self):
        py.draw.rect(window,GREY,py.Rect(0,0,1100,700))
        py.draw.rect(window,BLACK,py.Rect(100,10,5,650))
        py.draw.rect(window,BLACK,py.Rect(100,655,950,5))
        py.display.update()

    #method that change the colour of the button that indicates the on and off of the button
    def change_colour(self,colour1,colour2,colour3,colour4,switch):
        if switch:
            Click_button.draw_button_method2_in_class(self,colour1,colour2)
            switch=False
        elif switch==False:
            Click_button.draw_button_method2_in_class(self,colour3,colour4)
            switch=True
        return switch
    
    #method for the "next page" button that allows user to go to the next page 
    def next_page(self,page):
        py.draw.rect(window,DARK_GREY,py.Rect(1100,0,400,700))
        return page+1

    #method for the "last page" button that allows user to go to the last page 
    def last_page(self,page):
        py.draw.rect(window,DARK_GREY,py.Rect(1100,0,400,700))
        return page-1
    
    #method for the button "choose curve" to indicate user which curve are currently being represented
    def cursor_at_curve(self,current_pointer,multi_launch_data,scale_x,scale_y,shifting):

        py.draw.rect(window,GREY,py.Rect(0,0,1100,700))
        py.draw.rect(window,BLACK,py.Rect(100,10,5,650))
        py.draw.rect(window,BLACK,py.Rect(100,655,950,5))
        py.display.flip()
        for draw_each_curve in range(len(multi_launch_data)):

            for curve_datil in range(len(multi_launch_data[draw_each_curve][1])-1):
                if multi_launch_data[draw_each_curve][1][curve_datil]>0:
                    Draw=True
                    if (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting-5>1050) or (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting-5>1050 and 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y<10):
                        Draw=False
                        pass
                    elif multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting<105 or 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y>655:
                        Draw=False
                        pass
                    elif  multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting< multi_launch_data[draw_each_curve][0][0]*scale_x+shifting<10:
                        Draw=False
                        pass
                    elif Draw==True:
                        if draw_each_curve==current_pointer:

                            py.draw.line(window, curve_cursor_colour, (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting,660-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y),  (multi_launch_data[draw_each_curve][0][curve_datil+1]*scale_x+shifting,660-multi_launch_data[draw_each_curve][1][curve_datil+1]*scale_y),width=width_of_curve)
                        else:
                            py.draw.line(window, BLACK, (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting,660-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y),  (multi_launch_data[draw_each_curve][0][curve_datil+1]*scale_x+shifting,660-multi_launch_data[draw_each_curve][1][curve_datil+1]*scale_y),width=width_of_curve)

        py.draw.rect(window,GREY,py.Rect(95,660,1000,100))#clean edge curve
        py.draw.rect(window,GREY,py.Rect(1055,0,10,655))
        py.display.flip()
    #method that increase the pointer if the button is being clicked, if the pointer exceed the maximum number of curve it would be set to 0
    def increase_pointer(self,multa_launch_data,current_pointer):
        if current_pointer+1>len(multa_launch_data)-1:
            return 0
        else:
            return current_pointer+1
        
#create a Slider for representing curve detail
class Slider:
    #class method that is being use to converge a large data set into either 100 points list or 1000 points list depending on the size of the input
    @classmethod
    def pack_up_curve_into_pencatage(cls,curve):
        if len(curve[0])>1000:
            step=len(curve[0])/1000
            final_x=[]
            final_y=[]
            final_t=[]

            for i in range(0,1000):
                index=int(i*step)
                final_x.append(curve[0][index])
                final_y.append(curve[1][index])
                final_t.append(curve[2][index])
        elif len(curve[0])<1000:
            step=len(curve[0])/100
            final_x=[]
            final_y=[]
            final_t=[]

            for i in range(0,100):
                index=int(i*step)
                final_x.append(curve[0][index])
                final_y.append(curve[1][index])
                final_t.append(curve[2][index])
        return final_x,final_y,final_t
    
    #similar class method for converging velocity data points into smaller list 
    @classmethod
    def pack_up_velocity_into_pencatage(cls,velocity_x,velocity_y):
        velocity=[math.sqrt(velocity_x[i]**2+velocity_y[i]**2) for i in range(len(velocity_x))]
        if len(velocity)>1000:
            step=len(velocity)/1000
            final_velocity=[]
            for i in range(0,1000):
                index=int(i*step)
                final_velocity.append(velocity[index])

        elif len(velocity)<1000:
            step=len(velocity)/100

            final_velocity=[]
            for i in range(0,100):
                index=int(i*step)
                final_velocity.append(velocity[index])

        return final_velocity

    #store the top left coordinate,width adn length as the attributes 
    def __init__(self,top_left_x,top_left_y,length,width):
        self.top_left_x=top_left_x
        self.top_left_y=top_left_y
        self.length=length
        self.width=width
    

    #method that draw the initial line and the circle in the Slider
    def draw_line(self):
        py.draw.rect(window,BLACK,py.Rect(self.top_left_x-2,self.top_left_y-2,self.length+4,self.width+4))
        py.draw.rect(window,GREY,py.Rect(self.top_left_x,self.top_left_y,self.length,self.width))
        py.draw.circle(window,BLACK,(self.top_left_x+self.length/2,self.top_left_y+self.width/2),19)
        py.draw.circle(window,DARK_GREY,(self.top_left_x+self.length/2,self.top_left_y+self.width/2),17)
        py.display.flip()

    #method that allow user to move the circle in the Slider and update the line that is indicating at the current curve
    def move_circle(self,curve,multi_launch_data,scale_x,scale_y,shifting,pointer):
        data_x,data_y,data_t,data_velocity=0,0,0,0
        # try:
        if py.mouse.get_pressed()[0] != 0 :
            mouse_x=py.mouse.get_pos()[0]
            mouse_y=py.mouse.get_pos()[1]
            data_x,data_y,data_t=Slider.pack_up_curve_into_pencatage(curve)
            data_velocity=Slider.pack_up_velocity_into_pencatage(curve[6],curve[7])
            
            if mouse_x>self.top_left_x and mouse_x<self.top_left_x+self.length and mouse_y>self.top_left_y and mouse_y<self.top_left_y+self.width:
                current_pixel=mouse_x-(self.top_left_x)
                max_x=int(max(curve[0])*scale_x+shifting)-100
                percentage_of_current_pixel=round(current_pixel/250*100,1)
                py.draw.rect(window,GREY,py.Rect(0,0,1100,700))
                py.draw.rect(window,BLACK,py.Rect(100,10,5,650))
                py.draw.rect(window,BLACK,py.Rect(100,655,950,5))
                py.draw.rect(window,BLACK,py.Rect(self.top_left_x-2,self.top_left_y-2,self.length+4,self.width+4))
                py.draw.rect(window,GREY,py.Rect(self.top_left_x,self.top_left_y,self.length,self.width))
                py.draw.rect(window,GREY,py.Rect(self.top_left_x,self.top_left_y,self.length,self.width))
                py.draw.circle(window,BLACK,(mouse_x,self.top_left_y+self.width/2),19)
                py.draw.circle(window,DARK_GREY,(mouse_x,self.top_left_y+self.width/2),17)  
                py.draw.rect(window,DARK_GREY,py.Rect(self.top_left_x-20,self.top_left_y,18,self.width))
                py.draw.rect(window,DARK_GREY,py.Rect(self.top_left_x+self.length+2,self.top_left_y,20,self.width))
                if 100+int(max_x*percentage_of_current_pixel/100)<1050:
                    py.draw.line(window,BLACK,(100+int(max_x*percentage_of_current_pixel/100),10),(100+int(max_x*percentage_of_current_pixel/100),660),width=2)
                for draw_each_curve in range(len(multi_launch_data)):
                    for curve_datil in range(len(multi_launch_data[draw_each_curve][1])-1):
                        if multi_launch_data[draw_each_curve][1][curve_datil]>0:
                            Draw=True
                            if (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting-5>1050) or (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting-5>1050 and 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y<10):
                                Draw=False
                                pass
                            elif multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting<105 or 655-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y>655:
                                Draw=False
                                pass
                            elif  multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting< multi_launch_data[draw_each_curve][0][0]*scale_x+shifting<10:
                                Draw=False
                                pass
                            elif Draw==True:
                                if draw_each_curve==pointer:
                                    py.draw.line(window, curve_cursor_colour, (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting,660-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y),  (multi_launch_data[draw_each_curve][0][curve_datil+1]*scale_x+shifting,660-multi_launch_data[draw_each_curve][1][curve_datil+1]*scale_y),width=width_of_curve)
                                else:
                                    py.draw.line(window, BLACK, (multi_launch_data[draw_each_curve][0][curve_datil]*scale_x+shifting,660-multi_launch_data[draw_each_curve][1][curve_datil]*scale_y),  (multi_launch_data[draw_each_curve][0][curve_datil+1]*scale_x+shifting,660-multi_launch_data[draw_each_curve][1][curve_datil+1]*scale_y),width=width_of_curve)
                py.draw.rect(window,GREY,py.Rect(95,660,1000,100))
                py.draw.rect(window,GREY,py.Rect(1055,0,10,655))
                py.display.flip()
                
                if len(curve[0])>1000:
                    return round(data_x[int(percentage_of_current_pixel*10)],2),round(data_y[int(percentage_of_current_pixel*10)],2),round(data_t[int(percentage_of_current_pixel*10)],2),round(data_velocity[int(percentage_of_current_pixel*10)],2)
                else:
                    return round(data_x[int(percentage_of_current_pixel)],2),round(data_y[int(percentage_of_current_pixel)],2),round(data_t[int(percentage_of_current_pixel)],2),round(data_velocity[int(percentage_of_current_pixel)],2)

    #method that update the textbox and the values for showing the data of the curve    
    def show_data_text_box(self,data,x_coor,y_coor,width,length,text_before_value):
        
        values=font.render(data,True,BLACK)
        text_box=font.render(text_before_value,True,BLACK)
        window.blit(text_box,(x_coor-200,y_coor))
        window.blit(values,(x_coor,y_coor))
        
#main function for the program
def main_game():
    py.draw.rect(window,GREY,py.Rect(95,660,1000,100))
    py.draw.rect(window,GREY,py.Rect(1050,0,10,700))
    clock.tick(60)
    no_repeated_curve_check=[]
    multi_launch_data=dict()
    #create button as instance
    air_res_button=Text_input_button(1400,80,40,40)
    velocity_button=Text_input_button(1400,140,40,40,200)
    angle_button=Text_input_button(1400,200,40,40,217)
    height_button=Text_input_button(1400,260,40,40,195)
    mass_button=Text_input_button(1400,320,40,40,205)
    diameter_button=Text_input_button(1400,380,40,40,220)

    refresh_button=Click_button(1400,440,40,40,300)
    animate_button=Click_button(1400,500,40,40,300)
    launch_button=Click_button(1400,560,40,40,120)
    next_page_button=Click_button(1400,620,40,40)
    last_page_button=Click_button(1200,620,40,40)
    velocity__vector_button=Click_button(1400,20,40,40,305)
    acceleration_vector_button=Click_button(1400,80,40,40,310)
    choose_curve_button=Click_button(1400,140,40,40,300)
    scale_up_button=Click_button(1200,10,20,20)
    scale_down_button=Click_button(1450,10,20,20)
    shift_left=Click_button(1200,40,20,20)
    shift_right=Click_button(1450,40,20,20)

    curve_detail_slider=Slider(1200,200,250,40)

    pointer=0
    draw_all_buttons=True
    draw_all_buttons_page_2=True
    velocity_vector=False
    acceleration_vector=False
    page_numebr=1
    animate=True


    shifting=105
    run=True
    scale_factor_x=0
    scale_factor_y=0
    #an activation has to be made otherwise the program cannot detect the input texts
    while run:
        for event in py.event.get():
                if page_numebr==1 :
                    if draw_all_buttons==True:
                        animate_button.draw_button_method2(DARK_BLUE,BLUE,"                    Animate")
                        next_page_button.draw_button_method3(BLACK,LIGHT_BLACK,"2",WHITE)
                        height_button.draw_button("     Height(m)")
                        launch_button.draw_self_button("Launch")
                        refresh_button.draw_button_method2(DARK_BROWN,BROWN,"                     Refresh")
                        scale_up_button.draw_button_method3(BLACK,GREY,"+")
                        scale_down_button.draw_button_method3(BLACK,GREY,"-")
                        shift_left.draw_button_method3(BLACK,GREY,"<")
                        shift_right.draw_button_method3(BLACK,GREY,">")
                        air_res_button.draw_button("          Drag: 0.")
                        velocity_button.draw_button("Velocity(m/s)")
                        angle_button.draw_button("Angle(degree)")
                        mass_button.draw_button("        Mass(kg)")
                        diameter_button.draw_button("Diameter(m):0.")
                        draw_all_buttons=False
                        draw_all_buttons_page_2=True

                    #Check the position of the mouse when a click is detect
                    if event.type == py.MOUSEBUTTONDOWN :
                        if air_res_button.input_value=="":
                            if launch_button.button.collidepoint(event.pos):
                                #check the input value for the parameter for the Projectile is not 0
                                try:
                                    air_res_button.input_value=air_res_button.check_empty(air_res_button.input_value)
                                    velocity_button.input_value=velocity_button.check_empty(velocity_button.input_value)
                                    angle_button.input_value=angle_button.check_empty(angle_button.input_value)
                                    height_button.input_value=height_button.check_empty(height_button.input_value)
                                    mass_button.input_value=mass_button.check_empty(mass_button.input_value)
                                    diameter_button.input_value=diameter_button.check_empty(diameter_button.input_value)
                                    no_repeated_curve_check,multi_launch_data,scale_factor_x,scale_factor_y=draw_projectile(int(mass_button.input_value),int(diameter_button.input_value),no_repeated_curve_check,int(height_button.input_value),acceleration_vector,velocity_vector,shifting,animate,multi_launch_data,scale_factor_x,scale_factor_y,int(velocity_button.input_value),int(angle_button.input_value),False)
                                except Exception :
                                    pass 
                        else:
                            if launch_button.button.collidepoint(event.pos) and int(air_res_button.input_value)!=0:
                                try:
                                    air_res_button.input_value=air_res_button.check_empty(air_res_button.input_value)
                                    velocity_button.input_value=velocity_button.check_empty(velocity_button.input_value)
                                    angle_button.input_value=angle_button.check_empty(angle_button.input_value)
                                    height_button.input_value=height_button.check_empty(height_button.input_value)
                                    mass_button.input_value=mass_button.check_empty(mass_button.input_value)
                                    diameter_button.input_value=diameter_button.check_empty(diameter_button.input_value)
                                    no_repeated_curve_check,multi_launch_data,scale_factor_x,scale_factor_y=draw_projectile(int(mass_button.input_value),float(f"0.{diameter_button.input_value}"),no_repeated_curve_check,int(height_button.input_value),acceleration_vector,velocity_vector,shifting,animate,multi_launch_data,scale_factor_x,scale_factor_y,int(velocity_button.input_value),int(angle_button.input_value),True,float(f"0.{int(air_res_button.input_value)}"))
                                except Exception :
                                    pass 
                            
                            elif launch_button.button.collidepoint(event.pos) and int(air_res_button.input_value)==0:
                                try:
                                    air_res_button.input_value=air_res_button.check_empty(air_res_button.input_value)
                                    velocity_button.input_value=velocity_button.check_empty(velocity_button.input_value)
                                    angle_button.input_value=angle_button.check_empty(angle_button.input_value)
                                    height_button.input_value=height_button.check_empty(height_button.input_value)
                                    mass_button.input_value=mass_button.check_empty(mass_button.input_value)
                                    diameter_button.input_value=diameter_button.check_empty(diameter_button.input_value)
                                    no_repeated_curve_check,multi_launch_data,scale_factor_x,scale_factor_y=draw_projectile(int(mass_button.input_value),float(f"0.{diameter_button.input_value}"),no_repeated_curve_check,int(height_button.input_value),acceleration_vector,velocity_vector,shifting,animate,multi_launch_data,scale_factor_x,scale_factor_y,int(velocity_button.input_value),int(angle_button.input_value),False)
                                except Exception :
                                    pass 
                        #if button is being click and the position of the mouse is on a certain button, one or more methods for that button are called
                        if scale_up_button.button.collidepoint(event.pos):
                            scale_factor_x,scale_factor_y=scale_up_button.scale_up(shifting,multi_launch_data,scale_factor_x,scale_factor_y)
                        
                        elif scale_down_button.button.collidepoint(event.pos):
                            scale_factor_x,scale_factor_y=scale_up_button.scale_down(shifting,multi_launch_data,scale_factor_x,scale_factor_y)
                        
                        elif shift_left.button.collidepoint(event.pos):
                            shifting=scale_up_button.shift_left(shifting,multi_launch_data,scale_factor_x,scale_factor_y)
                        
                        elif shift_right.button.collidepoint(event.pos):
                            shifting=scale_up_button.shift_right(shifting,multi_launch_data,scale_factor_x,scale_factor_y)
                        
                        elif refresh_button.button.collidepoint(event.pos):
                            refresh_button.refresh_page()
                            multi_launch_data=dict()
                            no_repeated_curve_check=[]
                        
                        elif animate_button.button.collidepoint(event.pos):
                            animate=animate_button.change_colour(DARK_RED,RED,DARK_BLUE,BLUE,animate)
                        
                        elif next_page_button.button.collidepoint(event.pos):
                            page_numebr=next_page_button.next_page(page_numebr)
                        #check if the diameter 
                        air_res_button.collide_self(event)
                        velocity_button.collide_self(event)
                        angle_button.collide_self(event)
                        height_button.collide_self(event)
                        mass_button.collide_self(event)
                        diameter_button.collide_self(event)
                    
                    #update the text of the input button
                    height_button.update_text(event)
                    air_res_button.update_text(event)
                    velocity_button.update_text(event)
                    angle_button.limit_input(90)
                    angle_button.update_text(event)    
                    mass_button.update_text(event)    
                    diameter_button.update_text(event)    

                #draw page 2's buttons
                if page_numebr==2:
                    if draw_all_buttons_page_2:
                        #button needs to redraw if page is refresh 
                        last_page_button.draw_button_method3(BLACK,LIGHT_BLACK,"1",WHITE)
                        if velocity_vector==False:
                            velocity__vector_button.draw_button_method2(DARK_BLUE,BLUE,"         Velocity vector")
                        elif velocity_vector==True:
                            velocity__vector_button.draw_button_method2(DARK_RED,RED,"         Velocity vector")
                        if acceleration_vector==False:
                            acceleration_vector_button.draw_button_method2(DARK_BLUE,BLUE,"     Accelation vector")
                        elif acceleration_vector==True:
                            acceleration_vector_button.draw_button_method2(DARK_RED,RED,"     Accelation vector")
                        draw_all_buttons_page_2=False
                        choose_curve_button.draw_button_method2(DARK_BROWN,BROWN,"          Choose Curve")
                        curve_detail_slider.draw_line()
                    if event.type == py.MOUSEBUTTONDOWN :
                        if last_page_button.button.collidepoint(event.pos):
                            page_numebr=last_page_button.last_page(page_numebr)
                            draw_all_buttons=True
                        elif velocity__vector_button.button.collidepoint(event.pos):
                            velocity_vector=velocity__vector_button.change_colour(DARK_BLUE,BLUE,DARK_RED,RED,velocity_vector)
                        elif acceleration_vector_button.button.collidepoint(event.pos):
                            acceleration_vector=acceleration_vector_button.change_colour(DARK_BLUE,BLUE,DARK_RED,RED,acceleration_vector)
                        elif choose_curve_button.button.collidepoint(event.pos):
                            pointer=choose_curve_button.increase_pointer(multi_launch_data,pointer)
                            choose_curve_button.cursor_at_curve(pointer,multi_launch_data,scale_factor_x,scale_factor_y,shifting)

                    #use the Slider to show the data of the current Projectile
                    try:
                        data_x,data_y,data_t,data_velocity=curve_detail_slider.move_circle(multi_launch_data[pointer],multi_launch_data,scale_factor_x,scale_factor_y,shifting,pointer)
                        py.draw.rect(window,DARK_GREY,py.Rect(1100,250,450,300))
                        curve_detail_slider.show_data_text_box(str(data_x),1400,260,100,40,"Distance x")
                        curve_detail_slider.show_data_text_box(str(data_y),1400,320,100,40,"Distance y")
                        curve_detail_slider.show_data_text_box(str(data_t),1400,380,100,40,"time")
                        curve_detail_slider.show_data_text_box(str(data_velocity),1400,440,100,40,"velocity")
                        py.display.update(py.Rect(1100,250,450,300))
                    except Exception as e:
                        pass
                
                #check if the user wants to close the program
                if event.type == py.QUIT:
                    run=False
                    sys.exit()
                    break

        py.display.update()

#call the main function of the game
main_game()

