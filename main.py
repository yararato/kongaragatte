#python -m pygbag congara_web2

import pygame
import sys
import math
import random
import asyncio

fall_flag = False #落ちたことのフラグ

chk_0_A = True
chk_0_C = True
chk_0_T = True

chk_0 = True
 
chk_goal_A = False
chk_goal_C = False
chk_goal_T = False

chk_Lastgoal_C = False #False=ゴールしていない
chk_Lastgoal_T = False #False=ゴールしていない

chk_goal = False

index = 1
stage = 5
generated = []
life = 3

enshutsu = -200

en_ind = 1 #ページの進行
en_timer1 = 120

#音声関係
kansei = 0
messe = 0
bloomy = 0

tuto_ind = 1
con_ind = 3
SOUSA_MODE = 1


#=====SE======
se_jump = None
se_turn = None
se_fall = None

#=====col=====
RED = (255, 0, 0)
YELLOW = (255,255,128)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255, 255, 255)

PINK = (255,0,192)

#キャラの動き============================================
class Move_Amana(): #済
    def __init__(self):
        self.ground = 125
        self.x_amana = 0 #甘奈の位置
        self.h = 50
        self.y = self.ground - self.h #(甘奈の縦幅)
        
        
        self.speed = 1
        self.land = True
        self.fall_flag = False

        self.jump_timer = 30
        self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.turn = False
        self.turn_int = 1

        self.t_draw = 0

        self.t_turn = 0 #方向切り替えタイマー
        self.canTurn = True

        self.height = 40 #ジャンプ高さ

        self.canJump = True
        self.t_canjump = 0

        self.t_move = 0
        self.t_jump = 0

        self.radPerFrame = 2 * math.pi  / 60

        self.run_amana = [
                pygame.image.load("amana0.png"),
                pygame.image.load("amana1.png"),
                pygame.image.load("amana2.png"),
                pygame.image.load("amana3.png"),
                ]
        self.jump_amana= [
                None,
                pygame.image.load("amana_up.png"),
                pygame.image.load("amana_down.png"),
                ]

        self.run_han_amana = [
                pygame.image.load("hantai_amana0.png"),
                pygame.image.load("hantai_amana1.png"),
                pygame.image.load("hantai_amana2.png"),
                pygame.image.load("hantai_amana3.png"),
                ]

        self.jump_han_amana =[
                None,
                pygame.image.load("hantai_amana_up.png"),
                pygame.image.load("hantai_amana_down.png"),            
                ]

        self.stand_amana =[
                pygame.image.load("amana_stand_left.png"),
                pygame.image.load("hantai_amana_up.png"),
                pygame.image.load("hantai_amana_down.png"), 

                pygame.image.load("amana_stand_right.png"),            
                ]        

    def draw_chara(self, bg):
        global chk_goal_A, index
        if self.turn_int == -1:
            self.ANIMATION = [0]* 10 + [1] * 10 + [2] * 10 + [3] * 10

        if self.turn_int == 1:
            self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.ama_a = self.ANIMATION[self.x_amana % len(self.ANIMATION)]
    
        if index == 1 or index == 2:
            if chk_goal_A == False:
                if self.turn_int == -1 and self.land == True: #左への移動時
                    bg.blit(self.run_han_amana[self.ama_a], (self.x_amana, self.y))

                elif self.turn_int == 1 and self.land == True: #右への移動時
                    bg.blit(self.run_amana[self.ama_a], (self.x_amana, self.y))


                elif self.turn_int == -1 and self.land == False: #左へのジャンプ
                    bg.blit(self.jump_han_amana[self.i], (self.x_amana, self.y))

                elif self.turn_int == 1 and self.land == False: #右へのジャンプ
                    bg.blit(self.jump_amana[self.i], (self.x_amana, self.y))

            elif chk_goal_A == True:
                #i=1:上昇, i=2:下降
                bg.blit(self.stand_amana[self.i], (self.x_amana, self.y))

        elif index == 4:
            #if self.turn_int == 1 and self.land == True: #右への移動時
            bg.blit(self.run_amana[self.ama_a], (self.x_amana, self.y))

    def rect_x_update(self):
        global chk_0_A, chk_goal_A, index, life, chk_goal
        
        if chk_goal == False:
            self.speed = 1

        elif chk_goal == True:
            self.speed = 2

        if chk_goal_A == False:
            if chk_0_A == True: #床の上
                if self.turn_int == -1:
                    if self.canJump == False and self.land == False: #ジャンプ中
                        self.x_amana += -self.speed - 2

                    elif self.land == True: #左へ移動
                        self.x_amana -= self.speed * 2

                elif self.turn_int == 1:
                    
                    if self.canJump == False and self.land == False: #ジャンプ中
                        self.x_amana += self.speed + 2
            
                    elif self.land == True: #右へ移動
                        self.t_move = 0
                            
                        self.x_amana += self.speed


                if self.x_amana >= 480:
                    self.x_amana = 480
                if self.x_amana <= -100:
                    self.x_amana = -100

            if chk_0_A == False: #穴の上
                if self.turn_int == -1:
                    if self.land == False: #ジャンプ中
                        self.x_amana += -self.speed - 2

                    elif self.land == True: #左へ移動
                        self.x_amana -= 0

                elif self.turn_int == 1:
                    if self.land == False: #ジャンプ中
                        self.x_amana += self.speed + 2
                
                    elif self.land == True: #右へ移動
                        self.x_amana += 0

            if self.x_amana < -50: #画面外へ移動時ミス
                #Life = Life_Manage()
                life -= 1              
                index = 2

        #ゴール後の処理
        elif chk_goal_A == True: 

            #TODO 限度を設ける
            if self.x_amana <= 480 - 25 * 6: #「3」はゴールマスのマス数
                self.x_amana = 480 - 25 * 6

            self.x_amana -= 1

        if index == 4:
            self.x_amana += 3
            self.turn_int == 1

            if self.x_amana >= 480:
                self.x_amana = 480
   
    def rect_y_update(self):
        global chk_0_A, index, life, fall_flag

        #if (self.canJump== False or self.canJump == True) and self.land == True:
        if self.land == True:
            if chk_0_A == False:
                fall_flag = True
                self.y += 5
            if chk_0_A == True:
                self.y = self.ground - self.h 
        
        #elif (self.canJump== False or self.canJump == True) and self.land == False: #ジャンプ時に
        elif self.land == False: #ジャンプ時に
            if chk_0_A == True: #下が床なら
                self.t_jump += 1/60
                self.y = -self.height * (1.0 - (1.0 - math.sin(2*self.radPerFrame * self.t_jump))**10) + self.ground - self.h
            
                if self.y >= self.ground - self.h:
                    self.y = self.ground - self.h 
                    self.land = True #←←ここ着地

            if chk_0_A == False: #下が穴なら
                if self.y >= self.ground - self.h:
                    self.y = self.ground - self.h 
                    self.land = True #←←ここ着地
                       
        if self.y > 360:
            life -= 1
            index = 2

        if index == 4:
            self.y = self.ground - self.h 

    def jump(self): #ジャンプフラグ    
        if self.canJump:
            self.t_jump = 0
            self.canJump = False
            self.i = 1

    def jump_down(self): #下降時
        A = math.cos(self.radPerFrame * self.t_jump) - math.sin(2 * (self.radPerFrame * self.t_jump)) / 2

        if self.canJump == False and A < 0.3:
            self.i = 2

    def jump_flag(self):
        if self.land == True:
            self.t_canjump = 30            
            self.land = False

    def jump_reset(self):
        self.t_canjump = 0
        self.canJump = True

    def turn_chara(self):
        self.turn_int = -1 * self.turn_int

    def turn_flag(self):
        self.t_turn = 8
        self.canTurn = False
    
    def turn_reset(self):        
        self.t_turn = 0
        self.canTurn = True

#===============================================================================
class Move_Amana_tuto(): #済
    def __init__(self):
        self.ground = 125
        self.x_amana = 0 #甘奈の位置
        self.h = 50
        self.y = self.ground - self.h #(甘奈の縦幅)
        
        self.speed = 1
        self.land = True
        self.fall_flag = False

        self.jump_timer = 30
        self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.turn = False
        self.turn_int = 1

        self.t_draw = 0

        self.t_turn = 0 #方向切り替えタイマー
        self.canTurn = True

        self.height = 40 #ジャンプ高さ

        self.canJump = True
        self.t_canjump = 0

        self.t_move = 0
        self.t_jump = 0

        self.radPerFrame = 2 * math.pi  / 60
        self.run_amana = [
                pygame.image.load("amana0.png"),
                pygame.image.load("amana1.png"),
                pygame.image.load("amana2.png"),
                pygame.image.load("amana3.png"),
                ]
        self.jump_amana= [
                None,
                pygame.image.load("amana_up.png"),
                pygame.image.load("amana_down.png"),
                ]

        self.run_han_amana = [
                pygame.image.load("hantai_amana0.png"),
                pygame.image.load("hantai_amana1.png"),
                pygame.image.load("hantai_amana2.png"),
                pygame.image.load("hantai_amana3.png"),
                ]

        self.jump_han_amana =[
                None,
                pygame.image.load("hantai_amana_up.png"),
                pygame.image.load("hantai_amana_down.png"),            
                ]

        self.stand_amana =[
                pygame.image.load("amana_stand_left.png"),
                pygame.image.load("hantai_amana_up.png"),
                pygame.image.load("hantai_amana_down.png"), 

                pygame.image.load("amana_stand_right.png"),            
                ]
        self.ama_at = 0

    def draw_chara(self, bg):
        self.ama_a = self.ANIMATION[self.ama_at % len(self.ANIMATION)]

        if self.turn_int == -1 and self.land == True: #左への移動時
            bg.blit(self.run_han_amana[self.ama_a], (390, self.y))

        elif self.turn_int == 1 and self.land == True: #右への移動時
            bg.blit(self.run_amana[self.ama_a], (390, self.y))

        elif self.turn_int == -1 and self.land == False: #左へのジャンプ
            bg.blit(self.jump_han_amana[self.i], (390, self.y))

        elif self.turn_int == 1 and self.land == False: #右へのジャンプ
            bg.blit(self.jump_amana[self.i], (390, self.y))
            
    def rect_x_update(self):            
        self.x_amana += 0
        self.ama_at += self.speed
        

    def rect_y_update(self):
        if self.land == True:
            self.y = self.ground - self.h 

        elif self.land == False:
            
            self.t_jump += 1/60
            self.y = -self.height * (1.0 - (1.0 - math.sin(2*self.radPerFrame * self.t_jump))**10) + self.ground - self.h
            
            if self.y >= self.ground - self.h:
                self.y = self.ground - self.h 
                self.land = True #←←ここ着地
        

    def jump(self): #ジャンプフラグ    
        if self.canJump == True:
            self.t_jump = 0
            self.canJump = False

            self.i = 1

    def jump_down(self): #下降時
        A = math.cos(self.radPerFrame * self.t_jump) - math.sin(2 * (self.radPerFrame * self.t_jump)) / 2

        if self.land == False and A < 0.3:
            self.i = 2 

    def jump_flag(self):
        if self.land == True:
            self.t_canjump = 30            
            self.land = False

    def jump_reset(self):
        self.t_canjump = 0
        self.canJump = True

    def turn_chara(self):
        self.turn_int = -1 * self.turn_int

    def turn_flag(self):
        self.t_turn = 8
        self.canTurn = False

    def turn_reset(self):        
        self.t_turn = 0
        self.canTurn = True

#===============================================================================
class Move_Chikiyu(): #済
    def __init__(self):
        self.x_amana = 0
        self.speed = 1
        self.ground = 225
        self.h = 55
        self.y = self.ground - self.h #(甘奈の縦幅)

        self.land = True
        self.fall_flag = False

        self.jump_timer = 30
        self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.turn = False
        self.turn_int = 1

        self.t_draw = 0

        self.t_turn = 0 #方向切り替えタイマー
        self.canTurn = True

        self.height = 40 #ジャンプ高さ

        self.canJump = True
        self.t_canjump = 0

        self.t_move = 0
        self.t_jump = 0

        self.radPerFrame = 2 * math.pi  / 60

        self.run_amana = [
                pygame.image.load("chikiyu0.png"),
                pygame.image.load("chikiyu1.png"),
                pygame.image.load("chikiyu2.png"),
                pygame.image.load("chikiyu3.png"),
                ]
        self.jump_amana= [
                None,
                pygame.image.load("chikiyu_up.png"),
                pygame.image.load("chikiyu_down.png"),
                ]

        self.run_han_amana = [
                pygame.image.load("hantai_chikiyu0.png"),
                pygame.image.load("hantai_chikiyu1.png"),
                pygame.image.load("hantai_chikiyu2.png"),
                pygame.image.load("hantai_chikiyu3.png"),
                ]

        self.jump_han_amana =[
                None,
                pygame.image.load("hantai_chikiyu_up.png"),
                pygame.image.load("hantai_chikiyu_down.png"),            
                ]
        
        self.stand_amana =[
                pygame.image.load("chikiyu_stand_left.png"),
                pygame.image.load("hantai_chikiyu_up.png"),
                pygame.image.load("hantai_chikiyu_down.png"), 

                pygame.image.load("chikiyu_stand_right.png"),#stage6       
                pygame.image.load("chikiyu_stand_right_ce.png"),#end    
                ]
        
    def draw_chara(self, bg):
        global chk_goal_C, chk_Lastgoal_C, index

        if self.turn_int == -1:
            self.ANIMATION = [0]* 10 + [1] * 10 + [2] * 10 + [3] * 10

        if self.turn_int == 1:
            self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.ama_a = self.ANIMATION[self.x_amana % len(self.ANIMATION)]
        if chk_Lastgoal_C == False:
            if chk_goal_C == False:
                if self.turn_int == -1 and self.land == True: #左への移動時
                    bg.blit(self.run_han_amana[self.ama_a], (self.x_amana, self.y))

                elif self.turn_int == 1 and self.land == True: #右への移動時
                    bg.blit(self.run_amana[self.ama_a], (self.x_amana, self.y))


                elif self.turn_int == -1 and self.land == False: #左へのジャンプ
                    bg.blit(self.jump_han_amana[self.i], (self.x_amana, self.y))

                elif self.turn_int == 1 and self.land == False: #右へのジャンプ
                    bg.blit(self.jump_amana[self.i], (self.x_amana, self.y))

            elif index == 1 and chk_goal_C == True:
                #i=1:上昇, i=2:下降
                bg.blit(self.stand_amana[self.i], (self.x_amana, self.y))

            elif index == 4 and chk_goal_C == True:
                if self.turn_int == 1 and self.land == True: #右への移動時
                    bg.blit(self.run_amana[self.ama_a], (self.x_amana, self.y))

        elif chk_Lastgoal_C == True:
            bg.blit(self.stand_amana[3], (self.x_amana, self.y))

    def rect_x_update(self):
        global chk_0_C, chk_goal_C, chk_Lastgoal_C, index, life, chk_goal
        if chk_goal == False:
            self.speed = 1

        elif chk_goal == True:
            self.speed = 2

        if chk_Lastgoal_C == False:
            if chk_goal_C == False:
                if chk_0_C == True: #床の上
                    if self.turn_int == -1:
                        if self.canJump == False and self.land == False: #ジャンプ中
                            self.x_amana += -self.speed - 2

                        elif self.land == True: #左へ移動
                            self.x_amana -= self.speed * 2

                    elif self.turn_int == 1:
                    
                        if self.canJump == False and self.land == False: #ジャンプ中
                            self.x_amana += self.speed + 2
            
                        elif self.land == True: #右へ移動
                            self.t_move = 0
                            
                            self.x_amana += self.speed


                    if self.x_amana >= 480:
                        self.x_amana = 480
                    if self.x_amana <= -100:
                        self.x_amana = -100

                if chk_0_C == False: #穴の上
                    if self.turn_int == -1:
                        if self.land == False: #ジャンプ中
                            self.x_amana += -self.speed - 2

                    elif self.land == True: #左へ移動
                        self.x_amana -= 0
                        
                    elif self.turn_int == 1:
                        if self.land == False: #ジャンプ中
                            self.x_amana += self.speed + 2
                
                    elif self.land == True: #右へ移動
                        self.x_amana += 0

                if self.x_amana < -50: #画面外へ移動時ミス  
                    life -= 1   
                    index = 2
            #ゴール後の処理
            elif chk_goal_C == True: 

                #TODO 限度を設ける
                if self.x_amana <= 480 - 25 * 6: #「3」はゴールマスのマス数
                    self.x_amana = 480 - 25 * 6

                self.x_amana -= 1    

        elif chk_Lastgoal_C == True: #stage6の仕様
            if self.x_amana <= 480 - 25 * 10: #「3」はゴールマスのマス数
                self.x_amana = 480 - 25 * 10
            self.x_amana -= 1

        if index == 4:
            if stage == 6:
                self.x_amana += 0
            else:
                self.x_amana += 3
                self.turn_int == 1

            if self.x_amana >= 480:
                self.x_amana = 480

    def rect_y_update(self):
        global chk_0_C, index, life, fall_flag
        if self.land == True:
            if chk_0_C == False:
                fall_flag = True
                self.y += 5

            if chk_0_C == True:
                self.y = self.ground - self.h 

        elif self.land == False:
            if chk_0_C == True:
                self.t_jump += 1/60
                self.y = -self.height * (1.0 - (1.0 - math.sin(2*self.radPerFrame * self.t_jump))**10) + self.ground - self.h
            
                if self.y >= self.ground - self.h:
                    self.y = self.ground - self.h 
                    self.land = True #←←ここ着地
            if chk_0_C == False: #下が穴なら
                if self.y >= self.ground - self.h:
                    self.y = self.ground - self.h 
                    self.land = True #←←ここ着地 

        if self.y > 360:
            #Life = Life_Manage()
            life -= 1  
            index = 2

        if index == 4:
            self.y = self.ground - self.h

    def jump(self): #ジャンプフラグ    
        if self.canJump:
            self.t_jump = 0
            self.canJump = False
            self.i = 1

    def jump_down(self): #下降時
        A = math.cos(self.radPerFrame * self.t_jump) - math.sin(2 * (self.radPerFrame * self.t_jump)) / 2

        if self.canJump == False and A < 0.3:
            self.i = 2

    def jump_flag(self):
        if self.land == True:
            self.t_canjump = 30            
            self.land = False

    def jump_reset(self):
        self.t_canjump = 0
        self.canJump = True

    def turn_chara(self):
        self.turn_int = -1 * self.turn_int

    def turn_flag(self):
        self.t_turn = 8
        self.canTurn = False

    def turn_reset(self):        
        self.t_turn = 0
        self.canTurn = True
#===============================================================================
class Move_Chikiyu_tuto(): #済
    def __init__(self):
        self.x_amana = 0
        self.speed = 1
        self.ground = 225
        self.h = 55
        self.y = self.ground - self.h #(甘奈の縦幅)

        self.land = True
        self.fall_flag = False

        self.jump_timer = 30
        self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.turn = False
        self.turn_int = 1

        self.t_draw = 0

        self.t_turn = 0 #方向切り替えタイマー
        self.canTurn = True

        self.height = 40 #ジャンプ高さ

        self.canJump = True
        self.t_canjump = 0

        self.t_move = 0
        self.t_jump = 0

        self.radPerFrame = 2 * math.pi  / 60

        self.run_amana = [
                pygame.image.load("chikiyu0.png"),
                pygame.image.load("chikiyu1.png"),
                pygame.image.load("chikiyu2.png"),
                pygame.image.load("chikiyu3.png"),
                ]
        self.jump_amana= [
                None,
                pygame.image.load("chikiyu_up.png"),
                pygame.image.load("chikiyu_down.png"),
                ]

        self.run_han_amana = [
                pygame.image.load("hantai_chikiyu0.png"),
                pygame.image.load("hantai_chikiyu1.png"),
                pygame.image.load("hantai_chikiyu2.png"),
                pygame.image.load("hantai_chikiyu3.png"),
                ]

        self.jump_han_amana =[
                None,
                pygame.image.load("hantai_chikiyu_up.png"),
                pygame.image.load("hantai_chikiyu_down.png"),            
                ]
        
        self.stand_amana =[
                pygame.image.load("chikiyu_stand_left.png"),
                pygame.image.load("hantai_chikiyu_up.png"),
                pygame.image.load("hantai_chikiyu_down.png"), 

                pygame.image.load("chikiyu_stand_right.png"),#stage6       
                pygame.image.load("chikiyu_stand_right_ce.png"),#end    
                ]
        self.ama_at = 0

    def draw_chara(self, bg):
        self.ama_a = self.ANIMATION[self.ama_at % len(self.ANIMATION)]

        if self.turn_int == -1 and self.land == True: #左への移動時
            bg.blit(self.run_han_amana[self.ama_a], (390, self.y))

        elif self.turn_int == 1 and self.land == True: #右への移動時
            bg.blit(self.run_amana[self.ama_a], (390, self.y))

        elif self.turn_int == -1 and self.land == False: #左へのジャンプ
            bg.blit(self.jump_han_amana[self.i], (390, self.y))

        elif self.turn_int == 1 and self.land == False: #右へのジャンプ
            bg.blit(self.jump_amana[self.i], (390, self.y))
            
    def rect_x_update(self):            
        self.x_amana += 0
        self.ama_at += self.speed

    def rect_y_update(self):
        if self.land == True:
            self.y = self.ground - self.h 

        elif self.land == False:
            
            self.t_jump += 1/60
            self.y = -self.height * (1.0 - (1.0 - math.sin(2*self.radPerFrame * self.t_jump))**10) + self.ground - self.h
            
            if self.y >= self.ground - self.h:
                self.y = self.ground - self.h 
                self.land = True #←←ここ着地
        

    def jump(self): #ジャンプフラグ    
        if self.canJump == True:
            self.t_jump = 0
            self.canJump = False

            self.i = 1

    def jump_down(self): #下降時
        A = math.cos(self.radPerFrame * self.t_jump) - math.sin(2 * (self.radPerFrame * self.t_jump)) / 2

        if self.land == False and A < 0.3:
            self.i = 2 

    def jump_flag(self):
        if self.land == True:
            self.t_canjump = 30            
            self.land = False

    def jump_reset(self):
        self.t_canjump = 0
        self.canJump = True

    def turn_chara(self):
        self.turn_int = -1 * self.turn_int

    def turn_flag(self):
        self.t_turn = 8
        self.canTurn = False

    def turn_reset(self):        
        self.t_turn = 0
        self.canTurn = True
#===============================================================================
class Move_Chikiyu_Ending(): #済
    def __init__(self):
        self.ground = 200
        self.speed = 2
        self.h = 55

        self.h = 55
        self.y = self.ground - self.h #(甘奈の縦幅)
        self.x_amana = 0

        self.land = True
        self.fall_flag = False

        self.jump_timer = 30
        self.ANIMATION = [0]* 10 + [1] * 10 + [2] * 10 + [3] * 10

        self.turn = False
        self.turn_int = 1

        self.t_draw = 0

        self.t_turn = 0 #方向切り替えタイマー
        self.canTurn = True

        self.height = 40 #ジャンプ高さ

        self.canJump = True
        self.t_canjump = 0

        self.t_move = 0
        self.t_jump = 0

        self.radPerFrame = 2 * math.pi  / 60
        self.run_amana = [
                pygame.image.load("chikiyu0.png"),
                pygame.image.load("chikiyu1.png"),
                pygame.image.load("chikiyu2.png"),
                pygame.image.load("chikiyu3.png"),
                ]
        self.jump_amana= [
                None,
                pygame.image.load("chikiyu_up.png"),
                pygame.image.load("chikiyu_down.png"),
                ]

        self.run_han_amana = [
                pygame.image.load("hantai_chikiyu0.png"),
                pygame.image.load("hantai_chikiyu1.png"),
                pygame.image.load("hantai_chikiyu2.png"),
                pygame.image.load("hantai_chikiyu3.png"),
                ]

        self.jump_han_amana =[
                None,
                pygame.image.load("hantai_chikiyu_up.png"),
                pygame.image.load("hantai_chikiyu_down.png"),            
                ]
        
        self.stand_amana =[
                pygame.image.load("chikiyu_stand_left.png"),
                pygame.image.load("hantai_chikiyu_up.png"),
                pygame.image.load("hantai_chikiyu_down.png"), 

                pygame.image.load("chikiyu_stand_right.png"),#stage6       
                pygame.image.load("chikiyu_stand_right_ce.png"),#end    
                ]
    def draw_chara(self, bg):
        global en_ind7, stop_ce
        self.ama_a = self.ANIMATION[self.x_amana % len(self.ANIMATION)]

        if stop_ce == False:
            if en_ind7 == 1 or en_ind7 == 4:
                bg.blit(self.run_amana[self.ama_a], (self.x_amana, self.y))
        elif stop_ce == True:
            if en_ind7 == 2:
                bg.blit(self.stand_amana[0], (self.x_amana, self.y))

            elif en_ind7 == 3:
                bg.blit(self.stand_amana[4], (self.x_amana, self.y))

    def rect_x_update(self):
        global en_ind7, stop_ce

        self.t_move = 0
        if stop_ce == False:
            #if en_ind7 == 1 or en_ind7 == 4:                
                self.x_amana += self.speed
        
        elif stop_ce == True:
            #if en_ind7 == 2 or en_ind7 == 3:
                self.x_amana += 0

        if self.x_amana >= 480:
            self.x_amana = 480
        if self.x_amana <= -100:
            self.x_amana = -100

#==============================================================================
class Move_Tenka(): #済
    def __init__(self):
        self.speed = 1
        self.h = 50
        self.ground = 325
        self.y = self.ground - self.h #(甘奈の縦幅)
        self.x_amana = 0

        self.land = True
        self.fall_flag = False

        self.jump_timer = 30
        self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.turn = False
        self.turn_int = 1

        self.t_draw = 0

        self.t_turn = 0 #方向切り替えタイマー
        self.canTurn = True

        self.height = 40 #ジャンプ高さ

        self.canJump = True
        self.t_canjump = 0

        self.t_move = 0
        self.t_jump = 0

        self.radPerFrame = 2 * math.pi  / 60
        self.run_amana = [
                pygame.image.load("tenka0.png"),
                pygame.image.load("tenka1.png"),
                pygame.image.load("tenka2.png"),
                pygame.image.load("tenka3.png"),
                ]
        self.jump_amana= [
                None,
                pygame.image.load("tenka_up.png"),
                pygame.image.load("tenka_down.png"),
                ]

        self.run_han_amana = [
                pygame.image.load("hantai_tenka0.png"),
                pygame.image.load("hantai_tenka1.png"),
                pygame.image.load("hantai_tenka2.png"),
                pygame.image.load("hantai_tenka3.png"),
                ]

        self.jump_han_amana =[
                None,
                pygame.image.load("hantai_tenka_up.png"),
                pygame.image.load("hantai_tenka_down.png"),            
                ]
        
        self.stand_amana =[
                pygame.image.load("tenka_stand_left.png"),
                pygame.image.load("hantai_tenka_up.png"),
                pygame.image.load("hantai_tenka_down.png"), 

                pygame.image.load("tenka_stand_right.png"),            
                ]
        
    def draw_chara(self, bg):
        global chk_goal_T, chk_Lastgoal_T, index
        if self.turn_int == -1:
            self.ANIMATION = [0]* 10 + [1] * 10 + [2] * 10 + [3] * 10

        if self.turn_int == 1:
            self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.ama_a = self.ANIMATION[self.x_amana % len(self.ANIMATION)]
        if chk_Lastgoal_T == False:
            if chk_goal_T == False:
                if self.turn_int == -1 and self.land == True: #左への移動時
                    bg.blit(self.run_han_amana[self.ama_a], (self.x_amana, self.y))

                elif self.turn_int == 1 and self.land == True: #右への移動時
                    bg.blit(self.run_amana[self.ama_a], (self.x_amana, self.y))


                elif self.turn_int == -1 and self.land == False: #左へのジャンプ
                    bg.blit(self.jump_han_amana[self.i], (self.x_amana, self.y))

                elif self.turn_int == 1 and self.land == False: #右へのジャンプ
                    bg.blit(self.jump_amana[self.i], (self.x_amana, self.y))

            elif index == 1 and chk_goal_T == True:
                #i=1:上昇, i=2:下降
                bg.blit(self.stand_amana[self.i], (self.x_amana, self.y))

            elif index == 4 and chk_goal_T == True:
                if self.turn_int == 1 and self.land == True: #右への移動時
                    bg.blit(self.run_amana[self.ama_a], (self.x_amana, self.y))

        elif chk_Lastgoal_T == True:
            bg.blit(self.stand_amana[3], (self.x_amana, self.y))

    def rect_x_update(self):
        global chk_0_T, chk_goal_T, chk_Lastgoal_T, index, life, chk_goal
        if chk_goal == False:
            self.speed = 1

        elif chk_goal == True:
            self.speed = 2

        if chk_Lastgoal_T == False:
            if chk_goal_T == False:
                if chk_0_T == True: #床の上
                    if self.turn_int == -1:
                        if self.canJump == False and self.land == False: #ジャンプ中
                            self.x_amana += -self.speed - 2

                        elif self.land == True: #左へ移動
                            self.x_amana -= self.speed * 2

                    elif self.turn_int == 1:
                    
                        if self.canJump == False and self.land == False: #ジャンプ中
                            self.x_amana += self.speed + 2
            
                        elif self.land == True: #右へ移動
                            self.t_move = 0
                            
                            self.x_amana += self.speed


                    if self.x_amana >= 480:
                        self.x_amana = 480
                    if self.x_amana <= -100:
                        self.x_amana = -100

                if chk_0_T == False: #穴の上
                    if self.turn_int == -1:
                        if self.land == False: #ジャンプ中
                            self.x_amana += -self.speed - 2

                    elif self.land == True: #左へ移動
                        self.x_amana -= 0
                        
                    elif self.turn_int == 1:
                        if self.land == False: #ジャンプ中
                            self.x_amana += self.speed + 2
                
                    elif self.land == True: #右へ移動
                        self.x_amana += 0

                if self.x_amana < -50: #画面外へ移動時ミス  
                    life -= 1   
                    index = 2
            #ゴール後の処理
            elif chk_goal_T == True: 

                #TODO 限度を設ける
                if self.x_amana <= 480 - 25 * 6: #「3」はゴールマスのマス数
                    self.x_amana = 480 - 25 * 6

                self.x_amana -= 1    

        elif chk_Lastgoal_C == True: #stage6の仕様
            if self.x_amana <= 480 - 25 * 10: #「3」はゴールマスのマス数
                self.x_amana = 480 - 25 * 10
            self.x_amana -= 1

        if index == 4:
            if stage == 6:
                self.x_amana += 0
            else:
                self.x_amana += 3
                self.turn_int == 1

            if self.x_amana >= 480:
                self.x_amana = 480

    def rect_y_update(self):
        global chk_0_T, index, life, fall_flag
        if self.land == True:
            if chk_0_T == False:
                fall_flag = True
                self.y += 5
                
            if chk_0_T == True:
                self.y = self.ground - self.h 

        elif self.land == False:
            if chk_0_T == True:
                self.t_jump += 1/60
                self.y = -self.height * (1.0 - (1.0 - math.sin(2*self.radPerFrame * self.t_jump))**10) + self.ground - self.h
            
                if self.y >= self.ground - self.h:
                    self.y = self.ground - self.h 
                    self.land = True #←←ここ着地
            if chk_0_T == False: #下が穴なら
                if self.y >= self.ground - self.h:
                    self.y = self.ground - self.h 
                    self.land = True #←←ここ着地 

        if self.y > 360:
            #Life = Life_Manage()
            life -= 1  
            index = 2

        if index == 4:
            self.y = 225

    def jump(self): #ジャンプフラグ    
        if self.canJump == True:
            self.t_jump = 0
            self.canJump = False

            self.i = 1

    def jump_down(self): #下降時
        A = math.cos(self.radPerFrame * self.t_jump) - math.sin(2 * (self.radPerFrame * self.t_jump)) / 2

        if self.land == False and A < 0.3:
            self.i = 2 

    def jump_flag(self):
        if self.land == True:
            self.t_canjump = 30            
            self.land = False

    def jump_reset(self):
        self.t_canjump = 0
        self.canJump = True

    def turn_chara(self):
        self.turn_int = -1 * self.turn_int

    def turn_flag(self):
        self.t_turn = 8
        self.canTurn = False

    def turn_reset(self):        
        self.t_turn = 0
        self.canTurn = True
#==============================================================================
class Move_Tenka_tuto(): #済
    def __init__(self):
        self.ground = 325
        self.speed = 1
        self.h = 50
        self.y = self.ground - self.h #(甘奈の縦幅)
        self.x_amana = 0

        self.land = True
        self.fall_flag = False

        self.jump_timer = 30
        self.ANIMATION = [0]* 5 + [1] * 5 + [2] * 5 + [3] * 5

        self.turn = False
        self.turn_int = 1

        self.t_draw = 0

        self.t_turn = 0 #方向切り替えタイマー
        self.canTurn = True

        self.height = 40 #ジャンプ高さ

        self.canJump = True
        self.t_canjump = 0

        self.t_move = 0
        self.t_jump = 0

        self.radPerFrame = 2 * math.pi  / 60

        self.run_amana = [
                pygame.image.load("tenka0.png"),
                pygame.image.load("tenka1.png"),
                pygame.image.load("tenka2.png"),
                pygame.image.load("tenka3.png"),
                ]
        self.jump_amana= [
                None,
                pygame.image.load("tenka_up.png"),
                pygame.image.load("tenka_down.png"),
                ]

        self.run_han_amana = [
                pygame.image.load("hantai_tenka0.png"),
                pygame.image.load("hantai_tenka1.png"),
                pygame.image.load("hantai_tenka2.png"),
                pygame.image.load("hantai_tenka3.png"),
                ]

        self.jump_han_amana =[
                None,
                pygame.image.load("hantai_tenka_up.png"),
                pygame.image.load("hantai_tenka_down.png"),            
                ]
        
        self.stand_amana =[
                pygame.image.load("tenka_stand_left.png"),
                pygame.image.load("hantai_tenka_up.png"),
                pygame.image.load("hantai_tenka_down.png"), 

                pygame.image.load("tenka_stand_right.png"),            
                ]
        self.ama_at = 0

    def draw_chara(self, bg):
        self.ama_a = self.ANIMATION[self.ama_at % len(self.ANIMATION)]

        if self.turn_int == -1 and self.land == True: #左への移動時
            bg.blit(self.run_han_amana[self.ama_a], (390, self.y))

        elif self.turn_int == 1 and self.land == True: #右への移動時
            bg.blit(self.run_amana[self.ama_a], (390, self.y))

        elif self.turn_int == -1 and self.land == False: #左へのジャンプ
            bg.blit(self.jump_han_amana[self.i], (390, self.y))

        elif self.turn_int == 1 and self.land == False: #右へのジャンプ
            bg.blit(self.jump_amana[self.i], (390, self.y))
            
    def rect_x_update(self):            
        self.x_amana += 0
        self.ama_at += self.speed
        

    def rect_y_update(self):
        if self.land == True:
            self.y = self.ground - self.h 

        elif self.land == False:
            
            self.t_jump += 1/60
            self.y = -self.height * (1.0 - (1.0 - math.sin(2*self.radPerFrame * self.t_jump))**10) + self.ground - self.h
            
            if self.y >= self.ground - self.h:
                self.y = self.ground - self.h 
                self.land = True #←←ここ着地

        

    def jump(self): #ジャンプフラグ    
        if self.canJump == True:
            self.t_jump = 0
            self.canJump = False

            self.i = 1

    def jump_down(self): #下降時
        A = math.cos(self.radPerFrame * self.t_jump) - math.sin(2 * (self.radPerFrame * self.t_jump)) / 2

        if self.land == False and A < 0.3:
            self.i = 2 

    def jump_flag(self):
        if self.land == True:
            self.t_canjump = 30            
            self.land = False

    def jump_reset(self):
        self.t_canjump = 0
        self.canJump = True

    def turn_chara(self):
        self.turn_int = -1 * self.turn_int

    def turn_flag(self):
        self.t_turn = 8
        self.canTurn = False

    def turn_reset(self):        
        self.t_turn = 0
        self.canTurn = True
#キャラの動き============================================

#ステージの動き============================================
class Stage_Create(): #済
    def __init__(self):
        super().__init__()
        self.chk_goal = False

        self.x_road = 0
        self.map_data = []

        self.BLUE = (128, 128, 255)
        self.BLACK = (0, 0, 64)
        self.PINK = (255,232,255)

        self.block = [
                pygame.image.load("block_kara.png"),
                pygame.image.load("block_pskyblue.png"),
                
                pygame.image.load("block_yellow.png"), #start
                pygame.image.load("block_yellow.png"), #goal

                pygame.image.load("block_chikiyu.png"),
                pygame.image.load("block_tenka.png"),
                pygame.image.load("block_tenka.png"), #stage6用
                pygame.image.load("block_yellow_2_2.png"), #ending用

                pygame.image.load("block_pskyblue.png"), #8
                pygame.image.load("block_chikiyu.png"), #9
                pygame.image.load("block_tenka.png"), #10
            ]

    def set_stage(self):
        global stage, generated, generated2
        if stage == 1:
            self.map_data = [
                [2,2,2,2,  1,1,1,1,1,1, 1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1, 3,3,3,3,3,3], #甘奈
                [2,2,2,2,  1,1,1,1,1,1, 1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1, 3,3,3,3,3,3], #ちきゆ
                [2,2,2,2,  1,1,1,1,1,1, 1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1, 3,3,3,3,3,3], #甜花
                ]
        
        if stage == 2:
            self.map_data = [
                [2,2,2,2,  1,1,1,1,  1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,  3,3,3,3,3,3], #甘奈
                [2,2,2,2,  1,1,1,1,  1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,  3,3,3,3,3,3], #ちきゆ
                [2,2,2,2,  1,1,1,1,  1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,  3,3,3,3,3,3], #甜花
                ]

        if stage == 3:
            self.map_data = [
                [2,2,2,2, 4,4,4,4,4,4,  4,4,4,4,0,0,4,4,4,4,0,0,4,4,4,4,4,4,4,4,4,4,0,0,4,4,4,4,4,4,4,4,4,4, 3,3,3,3,3,3], #甘奈
                [2,2,2,2, 4,4,4,4,4,4,  4,4,4,4,4,4,4,4,4,4,4,4,0,0,4,4,4,4,4,4,0,0,4,4,4,4,0,0,4,4,4,4,4,4, 3,3,3,3,3,3], #ちきゆ
                [2,2,2,2, 4,4,4,4,4,4,  4,4,4,4,4,4,0,0,4,4,4,4,0,0,4,4,4,4,4,4,4,4,0,0,4,4,4,4,4,4,4,4,4,4, 3,3,3,3,3,3], #甜花
                ]
            
        if stage == 4:
            #s_random = Stage_Create_RN()
            self.map_data = generated

        if stage == 5:
            self.map_data = [
                [2,2,2,2,  5,5,5,5,5,5, 5,5,5,5,5,5,5,5,5,5,5,5,0,0,5,5,5,5,0,0,5,5,5,5,5,5,5,5,5,5,5,5,0,0,5,5, 3,3,3,3,3,3], #甘奈
                [2,2,2,2,  5,5,5,5,5,5, 5,5,5,5,5,5,5,5,5,5,5,5,0,0,5,5,5,5,0,0,5,5,5,5,5,5,5,5,0,0,5,5,5,5,5,5, 3,3,3,3,3,3], #ちきゆ
                [2,2,2,2,  5,5,5,5,5,5, 5,5,5,5,5,5,5,5,5,5,5,5,0,0,5,5,5,5,0,0,5,5,5,5,5,5,5,5,5,5,0,0,5,5,5,5, 3,3,3,3,3,3], #甜花
                ]

        if stage == 6:
            #s_random = Stage_Create_RN()
            self.map_data = generated2

    def create_stage(self, bg):
        self.set_stage()
        stage_len = self.map_data[0]
    
        for i in range(len(stage_len)):

            #甘奈
            if self.map_data[0][i] == 0:
                bg.blit(self.block[0], (25 * i - self.x_road, 125))
                
            elif self.map_data[0][i] == 1:
                bg.blit(self.block[1], (25 * i - self.x_road, 125))

            elif self.map_data[0][i] == 2:
                bg.blit(self.block[2], (25 * i - self.x_road, 125))

            elif self.map_data[0][i] == 3:
                bg.blit(self.block[3], (25 * i - self.x_road, 125))     

            elif self.map_data[0][i] == 4:
                bg.blit(self.block[4], (25 * i - self.x_road, 125))

            elif self.map_data[0][i] == 5:
                bg.blit(self.block[5], (25 * i - self.x_road, 125))  

            #ちきゆ
            if self.map_data[1][i] == 0:
                bg.blit(self.block[0], (25 * i - self.x_road, 225))
                
            elif self.map_data[1][i] == 1:
                bg.blit(self.block[1], (25 * i - self.x_road, 225))

            elif self.map_data[1][i] == 2:
                bg.blit(self.block[2], (25 * i - self.x_road, 225))

            elif self.map_data[1][i] == 3:
                bg.blit(self.block[3], (25 * i - self.x_road, 225))

            elif self.map_data[1][i] == 4:
                bg.blit(self.block[4], (25 * i - self.x_road, 225))

            elif self.map_data[1][i] == 5:
                bg.blit(self.block[5], (25 * i - self.x_road, 225)) 

            elif self.map_data[1][i] == 6:
                bg.blit(self.block[5], (25 * i - self.x_road, 225))

            #甜花
            if self.map_data[2][i] == 0:
                bg.blit(self.block[0], (25 * i - self.x_road, 325))
                
            elif self.map_data[2][i] == 1:
                bg.blit(self.block[1], (25 * i - self.x_road, 325))

            elif self.map_data[2][i] == 2:
                bg.blit(self.block[2], (25 * i - self.x_road, 325))

            elif self.map_data[2][i] == 3:
                bg.blit(self.block[3], (25 * i - self.x_road, 325))

            elif self.map_data[2][i] == 4:
                bg.blit(self.block[4], (25 * i - self.x_road, 325))

            elif self.map_data[2][i] == 5:
                bg.blit(self.block[5], (25 * i - self.x_road, 325))  

            elif self.map_data[2][i] == 6:
                bg.blit(self.block[5], (25 * i - self.x_road, 325))

    def stage_scrool2(self):
        global fall_flag
        self.set_stage()
        if fall_flag == False:
            self.x_road += 1

        elif fall_flag == True:
            self.x_road += 0

        self.x_Limit()
        

    def x_Limit(self):
        global generated, generated2, chk_goal
        line = self.map_data[0]

        if self.x_road >= len(line)*25 - 480: #960:画面の横幅
            self.x_road = len(line)*25 - 480
            chk_goal = True
            
        if self.x_road <= -100:
            self.x_road = -100

class Stage_Create_RN():
    def __init__(self):
        self.x_road = 0
        self.map_data = []
        self.block = [
                pygame.image.load("block_kara.png"),
                pygame.image.load("block_pskyblue.png"),
                
                pygame.image.load("block_yellow.png"), #start
                pygame.image.load("block_yellow.png"), #goal

                pygame.image.load("block_chikiyu.png"),
                pygame.image.load("block_tenka.png"),
                ]
    def set_stage(self, tip_num,repeat):
        #TODO ランダム生成
        self.map_data = [[2] * 4, [2] * 4, [2] * 4]

        if tip_num == 4:
            map_tip = [[tip_num,tip_num,tip_num,tip_num,tip_num,tip_num,0,0,],
                       [tip_num,tip_num,tip_num,tip_num,0,0,tip_num,tip_num,],
                       [tip_num,tip_num,0,0,tip_num,tip_num,tip_num,tip_num,],
                       [tip_num,tip_num,tip_num,tip_num,tip_num,tip_num,tip_num,tip_num]]
        
        if tip_num == 5:
            map_tip = [[tip_num,tip_num,tip_num,tip_num,tip_num,tip_num,0,0,],
                       [tip_num,tip_num,tip_num,tip_num,0,0,tip_num,tip_num,],
                       [tip_num,tip_num,0,0,tip_num,tip_num,tip_num,tip_num,],
                       [tip_num,tip_num,tip_num,tip_num,0,0,tip_num,tip_num,]]
        
        map_line1 = []
        map_line2 = []
        map_line3 = []

        i = 1
        j = 1
        k = 1

        while i <= repeat:
            n = random.randint(0, 3)
            if n == 0:
                map_line1 += map_tip[0]
            elif n == 1:
                map_line1 += map_tip[1]
            elif n == 2:
                map_line1 += map_tip[2]
            elif n == 3:
                map_line1 += map_tip[3]
            i += 1
        map_line1 += [tip_num, tip_num]

        if tip_num == 5:
            map_line1 += [tip_num] * 4

        map_line1 += [3] * 6
        #print(len(map_line1))
        self.map_data[0] += map_line1

        while j <= repeat:
            n = random.randint(0, 3)
            if n == 0:
                map_line2 += map_tip[0]
            elif n == 1:
                map_line2 += map_tip[1]
            elif n == 2:
                map_line2 += map_tip[2]
            elif n == 3:
                map_line2 += map_tip[3]
            j += 1
        map_line2 += [tip_num, tip_num]

        if tip_num == 5:
            map_line2 += [6] * 4

        map_line2 += [3] * 6
        #print(len(map_line2))
        self.map_data[1] += map_line2

        while k <= repeat:
            n = random.randint(0, 3)
            if n == 0:
                map_line3 += map_tip[0]
            elif n == 1:
                map_line3 += map_tip[1]
            elif n == 2:
                map_line3 += map_tip[2]
            elif n == 3:
                map_line3 += map_tip[3]
            k += 1

        map_line3 += [tip_num, tip_num]

        if tip_num == 5:
            map_line3 += [6] * 4

        map_line3 += [3] * 6
        #print(len(map_line3))
        self.map_data[2] += map_line3

#ステージの動き============================================

#ライフ管理================================================
class Life_Manage(): #済
    def __init__(self):
        self.mark =pygame.image.load("mark2.png")

    def life_draw(self, bg):
        global index, life
        
        if life <= 3:
            for i in range(life):
                bg.blit(self.mark, (120 + 30 * i , 15))

        Txt = Text_Manage()

        if life >= 4:
            for i in range(3):
                bg.blit(self.mark, (120 + 30 * i , 15))

            Txt.text_draw("+" + str(life-3), WHITE, 25, 225, 30, bg)


#テキスト管理================================================
class Text_Manage():
    def __init__(self):
        self.message = "text"

    def text_draw(self, msg, col, size, x, y, bg):
        font = pygame.font.Font(("JF-Dot-Shinonome16.ttf"), size)

        sur3 = font.render(msg, True, (0,0,0))
        sur3_rect = sur3.get_rect(center=(x+1, y+1))
        bg.blit(sur3, sur3_rect)

        sur1 = font.render(msg, True, col)
        sur1_rect = sur1.get_rect(center=(x, y))
        bg.blit(sur1, sur1_rect)

        sur2 = font.render(msg, True, col)
        sur2_rect = sur2.get_rect(center=(x-1, y-1))
        bg.blit(sur2, sur2_rect)

#インターバル================================================
class Enshutsu():
    def __init__(self):
        self.i = -200
        self.amana1 = pygame.image.load("amn1.png")
        self.amana2 = pygame.image.load("amn2.png")

        self.tenka1 = pygame.image.load("tnk1.png")
        self.tenka2 = pygame.image.load("tnk2.png")

        self.chikiyu1 = pygame.image.load("cky1.png")
        self.chikiyu2 = pygame.image.load("cky2.png")            

        self.sP = pygame.image.load("P.png")

        self.last1 = pygame.image.load("last1.png")    
        self.last2 = pygame.image.load("last2.png")
        self.last3 = pygame.image.load("last3.png")

    def text_draw_left(self, msg, col, size, x, y, bg):
        font = pygame.font.Font(("JF-Dot-Shinonome16.ttf"), size)

        sur3 = font.render(msg, True, col)
        bg.blit(sur3, (x-1, y-1))

        sur1 = font.render(msg, True, col)
        bg.blit(sur1, (x, y))

    def text_draw_center(self, msg, col, size, x, y, bg):
        font = pygame.font.Font(("JF-Dot-Shinonome16.ttf"), size)
        
        sur_s = font.render(msg, True, (0,0,0))
        sur_rect_s = sur_s.get_rect(center=(x+2, y+2))
        bg.blit(sur_s, sur_rect_s)

        sur3 = font.render(msg, True, col)
        sur3_rect = sur3.get_rect(center=(x-1, y-1))
        bg.blit(sur3, sur3_rect)

        sur1 = font.render(msg, True, col)
        sur1_rect = sur1.get_rect(center=(x, y))
        bg.blit(sur1, sur1_rect)

        sur2 = font.render(msg, True, col)
        sur2_rect = sur2.get_rect(center=(x+1, y+1))
        bg.blit(sur2, sur2_rect)

    def text_draw_center56(self, msg, col, size, x, y, bg):
        font = pygame.font.Font(("JF-Dot-Shinonome16.ttf"), size)

        sur3 = font.render(msg, True, col)
        sur3_rect = sur3.get_rect(center=(x-1, y-1))
        bg.blit(sur3, sur3_rect)

        sur1 = font.render(msg, True, col)
        sur1_rect = sur1.get_rect(center=(x, y))
        bg.blit(sur1, sur1_rect)

        sur2 = font.render(msg, True, col)
        sur2_rect = sur2.get_rect(center=(x+1, y+1))
        bg.blit(sur2, sur2_rect)

    def tuto_rial(self, bg): #済
        global tuto_ind
        sousa = pygame.image.load("sousa.png")        
        #self.text_draw_left(("[←]      ") + str(tuto_ind) + ("/3      [→]"), (255,255,255), 25, 35,300, bg)
        bg.blit(sousa, (0,0))

        if tuto_ind == 1:
            sousa1 = pygame.image.load("sousa1.png")
            bg.blit(sousa1, (-1,0))

        if tuto_ind == 2:
            sousa2 = pygame.image.load("sousa2.png")
            bg.blit(sousa2, (0,0))

        if tuto_ind == 3:
            sousa3 = pygame.image.load("sousa3.png")
            bg.blit(sousa3, (0,0))

    def config(self, bg): #済
        global SOUSA_MODE, con_ind
        con = pygame.image.load("config.png")
        bg.blit(con, (0,0))

        if SOUSA_MODE == 1:
            con1 = pygame.image.load("config1.png")
            bg.blit(con1, (0,2))

        if SOUSA_MODE == 2:
            con2 = pygame.image.load("config2.png")
            bg.blit(con2, (0,0))

        #if SOUSA_MODE == 3:
        #    con3 = pygame.image.load("config3.png")
        #    bg.blit(con3, (0,2))

        #if SOUSA_MODE == 4:
        #    con4 = pygame.image.load("config4.png")
        #    bg.blit(con4, (0,0))

    def stage0(self, bg):
        global enshutsu
    
        WHITE = (255,255,255)

        img_s_a = pygame.transform.scale(self.amana1,[60, 60])
        img_s_c = pygame.transform.scale(self.chikiyu1,[60, 60])

        # -200 から100 -100から200 
        self.text_draw_center("STAGE 1",WHITE, 25, 240, 50 + enshutsu, bg)
        self.text_draw_center("「アプリコット」", WHITE, 25, 240, 100 + enshutsu, bg)

        self.text_draw_center("アルストロメリアは雑誌「アプリコット」の", WHITE, 15, 240, 140+ enshutsu, bg)
        self.text_draw_center("オーディションに向けて練習中で...", WHITE, 15, 240, 160+ enshutsu, bg)

        self.text_draw_left("「もっと厳しくお願いしたいのー！」", WHITE, 17, 125, 200, bg)
        self.text_draw_left("「反対ごっこなら──空っぽ", WHITE, 17, 50, 275, bg)
        self.text_draw_left("　ですね...何も感じません...！」", WHITE, 17, 50, 300, bg)

        bg.blit(img_s_a, (50, 175))
        #bg.blit(self.tenka1, (100, 250))
        bg.blit(img_s_c, (360, 275))

    def stage1(self, bg):
        global enshutsu
        WHITE = (255,255,255)

        img_s_a = pygame.transform.scale(self.amana1,[60, 60])
        img_s_c = pygame.transform.scale(self.chikiyu1,[60, 60])

        self.text_draw_center("STAGE 2",WHITE, 25, 240, 50 + enshutsu, bg)
        self.text_draw_center("「反対ごっこ」", WHITE, 25, 240, 100 + enshutsu, bg)
        self.text_draw_center("千雪さんは「アプリコット」に何か思い出があるようで...", WHITE, 15, 240, 140+ enshutsu, bg)

        self.text_draw_left("「これ『アプリコット』...！？", WHITE, 17, 125, 195, bg)
        self.text_draw_left("　千雪さん…持ってたの…！」", WHITE, 17, 125, 220, bg)
    
        self.text_draw_left("「...あっ…ううん...！", WHITE, 17, 50, 275, bg)
        self.text_draw_left("　たまたまなの...」", WHITE, 17, 50, 300, bg)

        bg.blit(img_s_a, (50, 175))
        bg.blit(img_s_c, (360, 275))

    def stage2(self, bg):
        global enshutsu
        WHITE = (255,255,255)

        img_s_a = pygame.transform.scale(self.amana1,[60, 60])
        img_s_t = pygame.transform.scale(self.tenka1,[60, 60])
        img_s_c = pygame.transform.scale(self.chikiyu1,[60, 60])
        img_s_p = pygame.transform.scale(self.sP,[60, 60])

        self.text_draw_center("STAGE 3",WHITE, 25, 240, 50 + enshutsu, bg)
        self.text_draw_center("「そして彼女はインターホンを鳴らす」", WHITE, 25, 240, 100 + enshutsu, bg)
        self.text_draw_center("甜花ちゃんが偶然聞いた話の内容とは...？", WHITE, 15, 240, 140+ enshutsu, bg)
        #self.text_draw_center("何か思い出があるようで…", WHITE, 30, 480, 320, bg)

        self.text_draw_left("「いや、だって…！グランプリがうちの", WHITE, 17, 125, 195, bg)
        self.text_draw_left("　大崎甘奈に内定してるっていうのは─」", WHITE, 17, 125, 220, bg)
    
        self.text_draw_left("「...えっ」", WHITE, 17, 180, 285, bg)

        bg.blit(img_s_p, (50, 175))
        bg.blit(img_s_t, (360, 275))

    def stage3(self, bg):
        global enshutsu
        WHITE = (255,255,255)

        img_s_a = pygame.transform.scale(self.amana1,[60, 60])
        img_s_t = pygame.transform.scale(self.tenka1,[60, 60])
        img_s_c = pygame.transform.scale(self.chikiyu1,[60, 60])
        img_s_p = pygame.transform.scale(self.sP,[60, 60])

        self.text_draw_center("STAGE 4",WHITE, 25, 240, 50 + enshutsu, bg)
        self.text_draw_center("「ふたつの夜」", WHITE, 25, 240, 100 + enshutsu, bg)
        self.text_draw_center("千雪さんは甘奈ちゃんと甜花ちゃんに大事な話があるようで…", WHITE, 15, 240, 140+ enshutsu, bg)

        self.text_draw_left("「...千雪さん...」", WHITE, 17, 125, 200, bg)
    
        self.text_draw_left("「───アプリコットのオーディション", WHITE, 17, 50, 275, bg)
        self.text_draw_left("　私も...受けたい」", WHITE, 17, 50, 300, bg)

        bg.blit(img_s_a, (50, 175))
        bg.blit(img_s_c, (360, 275))

    def stage4(self, bg):
        global enshutsu
        BLACK = (128,128,192)

        img_s_a = pygame.transform.scale(self.amana1,[60, 60])
        img_s_t = pygame.transform.scale(self.tenka1,[60, 60])
        img_s_c = pygame.transform.scale(self.chikiyu1,[60, 60])
        img_s_p = pygame.transform.scale(self.sP,[60, 60])

        self.text_draw_center56("STAGE 5",BLACK, 25, 240, 50 + enshutsu, bg)
        self.text_draw_center56("「こわい」", BLACK, 25, 240, 100 + enshutsu, bg)
        self.text_draw_center56("出来レースの話を聞いた甘奈ちゃんは", BLACK, 15, 240, 130+ enshutsu, bg)
        self.text_draw_center56("ユニットを思いオーディションの辞退を考えますが...", BLACK, 15, 240, 150+ enshutsu, bg)


        self.text_draw_left("「反対ごっこ...しよっか」", BLACK, 17, 125, 200, bg)
    
        self.text_draw_left("「アルストロメリア、なんか...", BLACK, 17, 50, 275, bg)
        self.text_draw_left("　一番...大事じゃない...！」", BLACK, 17, 50, 300, bg)

        bg.blit(img_s_c, (50, 175))
        bg.blit(img_s_t, (360, 275))

    def stage5(self, bg):
        global enshutsu
        BLACK = (128,128,192)

        img_s_a = pygame.transform.scale(self.amana2,[60, 60])
        img_s_t = pygame.transform.scale(self.tenka1,[60, 60])
        img_s_c = pygame.transform.scale(self.chikiyu1,[60, 60])
        img_s_p = pygame.transform.scale(self.sP,[60, 60])

        self.text_draw_center56("STAGE 6",BLACK, 25, 240, 50 + enshutsu, bg)
        self.text_draw_center56("「薄桃色にこんがらがって」", BLACK, 25, 240, 100 + enshutsu, bg)
        self.text_draw_center56("「声」を出したアルストロメリアは...", BLACK, 15, 240, 140+ enshutsu, bg)

        self.text_draw_left("「───甘奈と戦ってください、", BLACK, 17, 125, 195, bg)
        self.text_draw_left("　千雪さん」", BLACK, 17, 125, 220, bg)
    
        self.text_draw_left("「───はい」", BLACK, 17, 150, 285, bg)

        bg.blit(img_s_a, (50, 175))
        bg.blit(img_s_c, (360, 275))

    def ending(self, bg):
        global en_ind, en_timer1, kansei, messe, bloomy
        WHITE = (255,255,255)

        img_s_t = pygame.transform.scale(self.tenka1,[60, 60])
        img_s_t2 = pygame.transform.scale(self.tenka2,[60, 60])
        img_s_c = pygame.transform.scale(self.chikiyu1,[60, 60])
        img_s_c2 = pygame.transform.scale(self.chikiyu2,[60, 60])

        #se_kansei = pygame.mixer.Sound("fan_no_minasan.ogg")
        se_messe = pygame.mixer.Sound("messe.ogg")
            
        #if en_ind == 1 or en_ind == 2 or en_ind == 3:
            #kansei += 1
            #if kansei == 1:
            #    se_kansei.play()

        if en_ind == 1:
            bg.blit(self.last1, (0,0))
            self.text_draw_center("あーまーな☆ あーまーな☆",WHITE, 25, 240, 240, bg)

        if en_ind == 2:
            bg.blit(self.last1, (0,0))
            bg.blit(img_s_c2, (50,235))
            self.text_draw_left("「あーまーな☆」",WHITE, 25, 120, 240, bg)

        if en_ind == 3:
            bg.blit(self.last1, (0,0))
            bg.blit(img_s_t2, (50,235))
            self.text_draw_left("「あーまーな......☆」",WHITE, 25, 120, 240, bg)

        if en_ind == 4:
            bg.blit(self.last1, (0,0))
            bg.blit(img_s_t, (50,235))
            self.text_draw_left("「千雪さん...ありがと...」",WHITE, 25, 120, 240, bg)    

        if en_ind == 5:
            bg.blit(self.last1, (0,0))
            bg.blit(img_s_t, (50,235))
            self.text_draw_left("「千雪さん...大事なもの...",WHITE, 25, 120, 240, bg)
            self.text_draw_left("　諦めなかった...」",WHITE, 25, 120, 270, bg)

        if en_ind == 6:
            bg.blit(self.last1, (0,0))
            bg.blit(img_s_t, (50,235))
            self.text_draw_left("「だから甜花も、わかった...",WHITE, 25, 120, 240, bg)
            self.text_draw_left("　大事なもの...」",WHITE, 25, 120, 270, bg)

        if en_ind == 7:
            bg.blit(self.last1, (0,0))
            bg.blit(img_s_c, (50,235))
            self.text_draw_left("「─────",WHITE, 25, 120, 240, bg)
            self.text_draw_left("　甜花ちゃん......」",WHITE, 25, 120, 270, bg) 

        if en_ind == 8:
            bg.blit(self.last1, (0,0))
            bg.blit(img_s_c, (50,235))
            self.text_draw_left("「─────",WHITE, 25, 120, 240, bg) 
            self.text_draw_left("　悔しい......」",WHITE, 25, 120, 270, bg)

        if en_ind == 9:
            bg.blit(self.last2, (0,0))
            self.text_draw_center("「悔しいなぁ............っ」",WHITE, 25, 240, 240, bg)
            
            bloomy += 1
            if bloomy == 1:
                pygame.mixer.music.load("bloomy+.ogg")
                pygame.mixer.music.play(0)

        if en_ind == 10:
            bg.blit(self.last2, (0,0))
            self.text_draw_left("「ちょっとだけ...",WHITE, 25, 120, 240, bg)  
            self.text_draw_left("　肩、貸してね......」",WHITE, 25, 120, 270, bg) 

        if en_ind == 11:
            bg.blit(self.last2, (0,0))
            self.text_draw_center("「う、うん.........!」",WHITE, 25, 240, 240, bg)

        if en_ind == 12:
            bg.blit(self.last2, (0,0))
            self.text_draw_center("「甜花......",WHITE, 25, 240, 240, bg) 
            self.text_draw_center("　でも.........」",WHITE, 25, 240, 270, bg) 

        if en_ind == 13:
            bg.blit(self.last2, (0,0))
            self.text_draw_center("「だから...大事な",WHITE, 25, 240, 240, bg) 
            self.text_draw_center("　オーディションになった...」",WHITE, 25, 240, 270, bg) 

        if en_ind == 14:
            bg.blit(self.last2, (0,0))
            self.text_draw_center("「私も思ったの、声にしなきゃ",WHITE, 25, 240, 240, bg)  
            self.text_draw_center("　いけないことで──」",WHITE, 25, 240, 270, bg)

        if en_ind == 15:
            bg.blit(self.last2, (0,0))
            self.text_draw_center("「───してないこと、",WHITE, 25, 240, 240, bg) 
            self.text_draw_center("　あったなって」",WHITE, 25, 240, 270, bg)

        if en_ind == 16:
            bg.blit(self.last3, (0,0))
            bg.blit(img_s_c, (50,235))
            self.text_draw_left("『くやしい！、",WHITE, 25, 120, 240, bg)  
            self.text_draw_left("　負けたのくやしいよー！』",WHITE, 25, 120, 270, bg)
            messe += 1
            if messe == 1:
                se_messe.play()

        if en_ind == 17:
            bg.blit(self.last3, (0,0))
            bg.blit(img_s_t, (50,235))
            self.text_draw_left("「──わ......!",WHITE, 25, 120, 240, bg)  
            self.text_draw_left("　グループに......──」",WHITE, 25, 120, 270, bg)

        if en_ind == 18:
            bg.blit(self.last3, (0,0))
            bg.blit(img_s_c, (50,235))
            self.text_draw_left("「ふふっ",WHITE, 25, 120, 240, bg)  
            self.text_draw_left("　3人でアルストロメリア...」",WHITE, 25, 120, 270, bg)

        if en_ind == 19:
            bg.blit(self.last3, (0,0))
            bg.blit(img_s_c2, (50,235))
            self.text_draw_left("「遠慮はしないんだ、もう」",WHITE, 25, 120, 240, bg)   
#=================================================================================
async def main():
    global fall_flag, chk_0_A, chk_0_C, chk_0_T, index, stage, generated, generated2, life,enshutsu
    global chk_goal_A, chk_goal_C, chk_goal_T, chk_goal
    global chk_Lastgoal_C, chk_Lastgoal_T
    global rect1, rect2
    global en_ind, en_timer1, stop_ce, en_ind7, tuto_ind, t_key, mode_flag
    global SOUSA_MODE, con_ind

    pygame.init()
    pygame.display.set_caption("")

    screen = pygame.display.set_mode((480, 360))
    clock = pygame.time.Clock()

    #甘奈
    Moving_A = Move_Amana()
    Moving_AT = Move_Amana_tuto()
    #ちきゆ
    Moving_C = Move_Chikiyu()
    Moving_CT = Move_Chikiyu_tuto()
    Moving_CE = Move_Chikiyu_Ending()
    #甜花
    Moving_T = Move_Tenka()
    Moving_TT = Move_Tenka_tuto()

    #演出
    En = Enshutsu()

    #ステージ
    StCre = Stage_Create()
    #ライフ
    Life = Life_Manage()
    #テキスト
    Txt = Text_Manage()
    
    #甘奈
    chk_0_A = True
    chk_goal_A = False #False=ゴールしていない
    #ちきゆ
    chk_0_C = True
    chk_goal_C = False #False=ゴールしていない
    chk_Lastgoal_C = False #False=ゴールしていない
    #甜花
    chk_0_T = True
    chk_goal_T = False #False=ゴールしていない
    chk_Lastgoal_T = False #False=ゴールしていない


    chk_goal = False

    t_GO = 0

    index = 0
    tmr_music = 0
    life = 3
    stage = 1
    mode_flag = 1

    #アイキャッチ用
    from5to1 = 60
    from5toaccA = 480
    from5toaccB = 480
    can_SPACE = False

    #説明用
    tuto_ind = 1
    t_key = 0

    #エンディング用
    stop_ce = False
    en_ind7 = 1
    
    #ページの進行
    en_ind = 1
    en_timer1 = 120
    en_timer2 = 180
    en_timer3 = 600

    #キーコン
    con_ind = 1
    SOUSA_MODE = 1

    s_random = Stage_Create_RN()
    s_random.set_stage(5, 2)
    generated2 = s_random.map_data

    pygame.mixer.music.load("arusutoromeria.ogg")

    se_jump = pygame.mixer.Sound("jump.ogg")
    se_turn = pygame.mixer.Sound("turn.ogg")
    se_fall = pygame.mixer.Sound("fall.ogg")
    se_gameover = pygame.mixer.Sound("gameover.ogg")
    se_sairen = pygame.mixer.Sound("sairen.ogg")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if index == 0: #済
            pygame.mixer.music.stop()
            TITLE = pygame.image.load("title.png")
            screen.blit(TITLE, (0, 0)) 

            chk_goal = False

            Moving_A.__init__()
            chk_goal_A = False

            Moving_C.__init__()
            chk_goal_C = False

            Moving_T.__init__()
            chk_goal_T = False

            StCre.__init__()

            
            #index = 0
            tmr_music = 0

            life = 3
            t_GO = 0

            rect1 = 0
            rect2 = 0

            en_ind = 1
            en_timer1 = 120

            Txt.text_draw("START PRODUCE!", WHITE, 30, 240, 250, screen)
            Txt.text_draw("MANUAL", WHITE, 30, 240, 290, screen)
            Txt.text_draw("CONFIG", WHITE, 30, 240, 330, screen)

            #t_key -= 1

            if mode_flag == 1:
                pygame.draw.polygon(screen, (255,255,255), [[90,240],[90,260],[125,250]])
            elif mode_flag == 2:
                pygame.draw.polygon(screen, (255,255,255), [[90,275],[90,295],[125,285]])
            elif mode_flag == 3:
                pygame.draw.polygon(screen, (255,255,255), [[90,315],[90,335],[125,325]])

            key = pygame.key.get_pressed()

            if t_key <= 0:
                t_key = 0
            
                if key[pygame.K_UP] == True:
                    mode_flag -= 1
                    t_key = 10

                if key[pygame.K_DOWN] == True:
                    mode_flag += 1
                    t_key = 10

                if mode_flag < 1:
                    mode_flag = 3
                if mode_flag > 3:
                    mode_flag = 1
            
                if key[pygame.K_SPACE] == True:       
                    if mode_flag == 1:
                        stage = 1
                        fall_flag = False
                        t_key = 50
                        index = 5

                    elif mode_flag == 2:
                        t_key = 10
                        tuto_ind = 1
                        index = 8

                    elif mode_flag == 3:
                        t_key = 10
                        tuto_ind = 1
                        index = 9

        if index == 1: #済
            if tmr_music == 1:
                pygame.mixer.music.play(-1)

            if stage == 1 or stage == 2:
                screen.fill(StCre.BLUE)

            if stage == 3 or stage == 4:
                screen.fill(StCre.BLACK)

            if stage == 5 or stage == 6:
                screen.fill(StCre.PINK)
        #甘奈        
            Moving_A.t_move += 1
            Moving_A.t_jump += 1
            Moving_A.t_draw += 1
        #ちきゆ        
            Moving_C.t_move += 1
            Moving_C.t_jump += 1
            Moving_C.t_draw += 1
        #甜花        
            Moving_T.t_move += 1
            Moving_T.t_jump += 1
            Moving_T.t_draw += 1

            StCre.stage_scrool2()
            StCre.create_stage(screen)

#====================甘奈=======================================================

        # キャラの描画
            Moving_A.draw_chara(screen)
        
        #床の判定(なんか関数に出来ない)
            StA = StCre.map_data[0]
            #print(StA)　#チェック用

            if Moving_A.turn_int == -1: #左向き
                if chk_goal_A == False:                
                    B = int((Moving_A.x_amana + StCre.x_road)/25) #左向きの右寄り
                    #C = int((Moving_A.x_amana + StCre.x_road)/100 + 1) #左向きの左寄り

                if chk_goal_A == False:                
                    B = int((Moving_A.x_amana + StCre.x_road)/25)
                    #print(B)　チェック用
                    if StA[B] == 0 and StA[B+1] == 0:
                        chk_0_A = False

                    elif StA[B] == 6:
                        Moving_A.canJump = False

                    elif StA[B] == 3:
                        chk_goal_A = True

                    else:
                        chk_0_A = True

            if Moving_A.turn_int == 1: #右向き
                if chk_goal_A == False: 
                    A = int((Moving_A.x_amana + StCre.x_road )/25)
                #print(A)　チェック用
                    if StA[A] == 0:
                        chk_0_A = False
                    if StA[A] == 1 or StA[A] == 2 or StA[A] == 4 or StA[A] == 5:
                        chk_0_A = True
                
                    if StA[A] == 3:
                        chk_goal_A = True
                #print(chk_0_A)　チェック用
        #ここまで床

            key = pygame.key.get_pressed()

            if chk_goal_A == False:
        #ここからジャンプ
                if Moving_A.canJump == True and Moving_A.land == True:
                    if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                        if key[pygame.K_j] == True: #<===============================================
                            if Moving_A.y == Moving_A.ground - Moving_A.h: #150 甘奈上角のy座標 
                                se_jump.play()  
                                Moving_A.jump()
                                Moving_A.jump_flag()

                    if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                        if key[pygame.K_SEMICOLON] == True: #<===============================================
                            if Moving_A.y == Moving_A.ground - Moving_A.h: #150 甘奈上角のy座標 
                                se_jump.play()  
                                Moving_A.jump()
                                Moving_A.jump_flag()

                    #落下音
                    if Moving_A.y == Moving_A.ground - Moving_A.height + 5:
                        se_fall.play()

            Moving_A.t_canjump -= 1

            if Moving_A.t_canjump == 0:
                Moving_A.jump_reset()


        #ここまでジャンプ
        
        #反対ごっこ
            if SOUSA_MODE == 1 or SOUSA_MODE == 3:
                if key[pygame.K_d] == True and Moving_A.canTurn == True:  #<===============================================   
                    Moving_A.turn_chara() #反対ごっこ
                    Moving_A.turn_flag() #次の反対ごっこまでの猶予
                    se_turn.play()
            
            elif SOUSA_MODE == 2 or SOUSA_MODE == 4:
                if key[pygame.K_a] == True and Moving_A.canTurn == True:  #<===============================================   
                    Moving_A.turn_chara() #反対ごっこ
                    Moving_A.turn_flag() #次の反対ごっこまでの猶予
                    se_turn.play()
        
            if stage == 5:
                RN_A = random.randint(1, 1000)
                if RN_A == 1:
                    Moving_A.turn_chara() #反対ごっこ
                    Moving_A.turn_flag() #次の反対ごっこまでの猶予
                    se_turn.play()

            Moving_A.t_turn -= 1 #タイマーを起動

            if Moving_A.t_turn == 0: #タイマーが0で
                Moving_A.turn_reset() #ターン出来るようにする
        #ここまで反対ごっこ

            Moving_A.jump_down()

            #ゴール後ぴょんぴょん
            if chk_goal_A == True:
                Moving_A.i = 0
                if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                    if key[pygame.K_j] == True: #<===============================================
                        if Moving_A.y == 75: #150 甘奈上角のy座標 
                            se_jump.play() 
                            Moving_A.jump()
                            Moving_A.jump_flag()

                if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                    if key[pygame.K_SEMICOLON] == True: #<===============================================
                        if Moving_A.y == 75: #150 甘奈上角のy座標 
                            se_jump.play() 
                            Moving_A.jump()
                            Moving_A.jump_flag()

                if Moving_A.canJump == False and Moving_A.land == False:
                    Moving_A.i = 1

                Moving_A.jump_down()
            #ゴール後ぴょんぴょん

#====================ちきゆ=======================================================

        # キャラの描画
            Moving_C.draw_chara(screen)
        
        #床の判定(なんか関数に出来ない)
            StC = StCre.map_data[1]
            #print(StC) #チェック用

            if Moving_C.turn_int == -1:
                if chk_goal_C == False:                
                    B = int((Moving_C.x_amana + StCre.x_road)/25)
                    #print(B)　チェック用
                    if StC[B] == 0 and StC[B+1] == 0:
                        chk_0_C = False

                    elif StC[B] == 6:
                        Moving_C.canJump = False
                        chk_Lastgoal_C = True  

                    elif StC[B] == 3:
                        chk_goal_C = True
                    else:
                        chk_0_C = True

            if Moving_C.turn_int == 1:
                A = int((Moving_C.x_amana + StCre.x_road )/25)
            #print(A)　チェック用
                if StC[A] == 0:
                    chk_0_C = False
                if StC[A] == 1 or StC[A] == 2 or StC[A] == 4 or StC[A] == 5:
                    chk_0_C = True
                
                if StC[A] == 3:
                    chk_goal_C = True

                if StC[A] == 6:
                    Moving_C.canJump = False
                    chk_Lastgoal_C = True
            #print(chk_0_A)　チェック用
        #ここまで床

            key = pygame.key.get_pressed()

            if chk_goal_C == False:
        #ここからジャンプ
                if Moving_C.canJump == True and Moving_C.land == True:
                    if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                        if key[pygame.K_k] == True: #<===============================================
                            if Moving_C.y == Moving_C.ground - Moving_C.h: #150 甘奈上角のy座標 
                                se_jump.play()  
                                Moving_C.jump()
                                Moving_C.jump_flag()

                    if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                        if key[pygame.K_COLON] == True: #<===============================================
                            if Moving_C.y == Moving_C.ground - Moving_C.h: #150 甘奈上角のy座標 
                                se_jump.play()  
                                Moving_C.jump()
                                Moving_C.jump_flag()

            Moving_C.t_canjump -= 1

            if Moving_C.t_canjump == 0:
                Moving_C.jump_reset()

            if Moving_C.y == Moving_C.ground - Moving_C.height + 5:
                se_fall.play()


        #ここまでジャンプ

        #反対ごっこ
            if key[pygame.K_s] == True and Moving_C.canTurn == True: #<===============================================    
                Moving_C.turn_chara() #反対ごzcっこ
                Moving_C.turn_flag() #次の反対ごっこまでの猶予
                se_turn.play()

            if stage == 5:
                RN_A = random.randint(1, 1000)
                if RN_A == 1:
                    Moving_C.turn_chara() #反対ごっこ
                    Moving_C.turn_flag() #次の反対ごっこまでの猶予
                    se_turn.play()
            
            Moving_C.t_turn -= 1 #タイマーを起動

            if Moving_C.t_turn == 0: #タイマーが0で
                Moving_C.turn_reset() #ターン出来るようにする
        #ここまで反対ごっこ
            Moving_C.jump_down()
            #ゴール後ぴょんぴょん
            if chk_goal_C == True:
                Moving_C.i = 0
                if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                    if key[pygame.K_k] == True: #<===============================================
                        if Moving_C.y == Moving_C.ground - Moving_C.h: #150 甘奈上角のy座標 
                            se_jump.play()  
                            Moving_C.jump()
                            Moving_C.jump_flag()

                if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                    if key[pygame.K_COLON] == True: #<===============================================
                        if Moving_C.y == Moving_C.ground - Moving_C.h: #150 甘奈上角のy座標 
                            se_jump.play()  
                            Moving_C.jump()
                            Moving_C.jump_flag()

                if Moving_C.canJump == False and Moving_C.land == False:
                    Moving_C.i = 1

                    Moving_C.jump_down()
            #ゴール後ぴょんぴょん

#====================甜花=======================================================

        # キャラの描画
            Moving_T.draw_chara(screen)
            #print(Moving_T.y)
        
        #床の判定(なんか関数に出来ない)
            StT = StCre.map_data[2]
            #print(StT)　#チェック用
            
            if Moving_T.turn_int == -1:
                if chk_goal_T == False:                
                    B = int((Moving_T.x_amana + StCre.x_road)/25)
                    #print(B)　チェック用
                    if StT[B] == 0 and StT[B+1] == 0:
                        chk_0_T = False

                    elif StT[B] == 6:
                        Moving_T.canJump = False
                        chk_Lastgoal_T = True  

                    elif StT[B] == 3:
                        chk_goal_T = True

                    else:
                        chk_0_T = True

            if Moving_T.turn_int == 1:
                A = int((Moving_T.x_amana + StCre.x_road )/25)
            #print(A)　チェック用
                if StT[A] == 0:
                    chk_0_T = False
                if StT[A] == 1 or StT[A] == 2 or StT[A] == 4 or StT[A] == 5:
                    chk_0_T = True

                if StT[A] == 6:
                    Moving_T.canJump = False
                    chk_Lastgoal_T = True                

                if StT[A] == 3:
                    chk_goal_T = True
            #print(chk_0_A)　チェック用
        #ここまで床

            key = pygame.key.get_pressed()

            if chk_goal_T == False:
        #ここからジャンプ
                if Moving_T.canJump == True and Moving_T.land == True:
                    if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                        if key[pygame.K_l] == True: #<===============================================
                            if Moving_T.y == Moving_T.ground - Moving_T.h: #150 甘奈上角のy座標 
                                se_jump.play()  
                                Moving_T.jump()
                                Moving_T.jump_flag()

                    if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                        if key[pygame.K_RIGHTBRACKET] == True: #<===============================================
                            if Moving_T.y == Moving_T.ground - Moving_T.h: #150 甘奈上角のy座標 
                                se_jump.play()  
                                Moving_T.jump()
                                Moving_T.jump_flag()
                    
                    #落下音
                    if Moving_T.y == Moving_T.ground - Moving_T.height + 5:
                        se_fall.play()

                if Moving_T.canJump == False and Moving_T.land == False:
                    Moving_T.i = 1

                    Moving_T.jump_down()

            Moving_T.t_canjump -= 1

            if Moving_T.t_canjump == 0:
                Moving_T.jump_reset()
        #ここまでジャンプ

        #反対ごっこ
            if SOUSA_MODE == 1 or SOUSA_MODE == 3:
                if key[pygame.K_a] == True and Moving_T.canTurn == True: #<===============================================
                    Moving_T.turn_chara() #反対ごっこ
                    Moving_T.turn_flag() #次の反対ごっこまでの猶予
                    se_turn.play()
            
            if SOUSA_MODE == 2 or SOUSA_MODE == 4:
                if key[pygame.K_d] == True and Moving_T.canTurn == True: #<===============================================
                    Moving_T.turn_chara() #反対ごっこ
                    Moving_T.turn_flag() #次の反対ごっこまでの猶予
                    se_turn.play()

            if stage == 5:
                RN_A = random.randint(1, 1000)
                if RN_A == 1:
                    Moving_T.turn_chara() #反対ごっこ
                    Moving_T.turn_flag() #次の反対ごっこまでの猶予
                    se_turn.play()
        
            Moving_T.t_turn -= 1 #タイマーを起動

            if Moving_T.t_turn == 0: #タイマーが0で
                Moving_T.turn_reset() #ターン出来るようにする

                Moving_T.jump_down()
        #ここまで反対ごっこ

            #ゴール後ぴょんぴょん
            if chk_goal_T == True:
                Moving_T.i = 0
                if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                    if key[pygame.K_l] == True: #<===============================================
                        if Moving_T.y == Moving_T.ground - Moving_T.h: #150 甘奈上角のy座標 
                            se_jump.play()  
                            Moving_T.jump()
                            Moving_T.jump_flag()

                if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                    if key[pygame.K_RIGHTBRACKET] == True: #<===============================================
                        if Moving_T.y == Moving_T.ground - Moving_T.h: #150 甘奈上角のy座標 
                            se_jump.play()  
                            Moving_T.jump()
                            Moving_T.jump_flag()

                if Moving_T.canJump == False and Moving_T.land == False:
                    Moving_T.i = 1

                    Moving_T.jump_down()
            #ゴール後ぴょんぴょん

#===========================================================================

            #固定
            Life.life_draw(screen)
            Txt.text_draw("STAGE " + str(stage), WHITE, 25, 390, 30, screen)
            Txt.text_draw("MENTAL: ", WHITE, 25, 75, 30, screen)

            Moving_A.rect_x_update()
            Moving_A.rect_y_update()

            Moving_C.rect_x_update()
            Moving_C.rect_y_update()

            Moving_T.rect_x_update()
            Moving_T.rect_y_update()

            if stage == 6:
                if chk_goal == True and \
                    chk_goal_A == True and\
                    chk_Lastgoal_C == True and\
                    chk_Lastgoal_T == True:

                    if SOUSA_MODE == 1 or SOUSA_MODE == 3:
                        if key[pygame.K_d] == True:  #<===============================================
                            index = 4
                            tmr_music = 0
                    if SOUSA_MODE == 2 or SOUSA_MODE == 4:
                        if key[pygame.K_a] == True:  #<===============================================
                            index = 4
                            tmr_music = 0

            if chk_goal == True and \
                chk_goal_A == True and\
                chk_goal_C == True and\
                chk_goal_T == True:

                index = 4
                tmr_music = 0

            #固定

        if index == 2: #ミス、ゲームオーバー #済
            pygame.mixer.music.stop()

            if stage == 1 or stage == 2:
                screen.fill(StCre.BLUE)

            if stage == 3 or stage == 4:
                screen.fill(StCre.BLACK) 

            if stage == 5 or stage == 6:
                screen.fill(StCre.PINK) 

            #BACK = pygame.image.load("touka.png")
            #screen.blit(BACK, (0, 0)) 
            
            StCre.create_stage(screen)
            Moving_A.draw_chara(screen)
            Moving_C.draw_chara(screen)
            Moving_T.draw_chara(screen)

            Life.life_draw(screen)
            Txt.text_draw("STAGE " + str(stage), WHITE, 25, 390, 30, screen)
            Txt.text_draw("MENTAL: ", WHITE, 25, 75, 30, screen)

            StCre.x_road += 0
            if life > 0:
                Txt.text_draw("Miss", YELLOW, 54, 240, 180, screen)
                #Life.life_draw(screen)
                
                key = pygame.key.get_pressed()
                if key[pygame.K_SPACE] == True:    
                    Moving_A.__init__()
                    chk_goal_A = False

                    Moving_C.__init__()
                    chk_goal_C = False
                    chk_Lastgoal_C = False

                    Moving_T.__init__()
                    chk_goal_T = False
                    chk_Lastgoal_T = False

                    StCre.__init__()

                    chk_goal = False
                    fall_flag = False

                    index = 1
                    tmr_music = 0

                    #print(Life.life)

            if life <= 0:
                StCre.x_road += 0
                Txt.text_draw("GAME OVER", BLUE, 54, 240, 180, screen)    
                pygame.mixer.music.stop()
                
                t_GO += 1
                if t_GO == 1:
                    se_gameover.play()

                key = pygame.key.get_pressed()
                
                if key[pygame.K_SPACE] == True:
                    t_key = 30    
                    index = 0

        if index == 4: #ステージクリア #済
            if stage == 1 or stage == 2:
                screen.fill(StCre.BLUE)

            if stage == 3 or stage == 4:
                screen.fill(StCre.BLACK)

            if stage == 5 or stage == 6:
                screen.fill(StCre.PINK) 

            #BACK = pygame.image.load("touka.png")
            #screen.blit(BACK, (0, 0)) 

            Moving_A.t_jump += 1
            Moving_C.t_jump += 1
            Moving_T.t_jump += 1

            if tmr_music == 1:
                pygame.mixer.music.load("clear3.ogg")
                pygame.mixer.music.play(0)

            Moving_A.y = Moving_A.ground - Moving_A.h
            Moving_C.y = Moving_C.ground - Moving_C.h
            Moving_T.y = Moving_T.ground - Moving_T.h

            Moving_A.draw_chara(screen)
            Moving_C.draw_chara(screen)
            Moving_T.draw_chara(screen)
            Life.life_draw(screen)

            StCre.create_stage(screen)

            Moving_A.rect_x_update()
            Moving_C.rect_x_update()
            Moving_T.rect_x_update()

            Moving_A.rect_y_update()
            Moving_C.rect_y_update()
            Moving_T.rect_y_update()

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] == True:    
                Moving_A.__init__()
                chk_goal_A = False

                Moving_C.__init__()
                chk_goal_C = False

                Moving_T.__init__()
                chk_goal_T = False

                chk_goal = False

                StCre.__init__()

                if stage == 3:
                    s_random = Stage_Create_RN()
                    s_random.set_stage(4, 4)
                    generated = s_random.map_data

                if stage == 5:
                    s_random = Stage_Create_RN()
                    s_random.set_stage(5, 5)
                    generated2 = s_random.map_data

                if stage == 6:
                    index = 6
                    chk_Lastgoal_C = False
                    chk_Lastgoal_T = False

                if stage <= 5:
                    index = 5
                    life += 1 
                    stage += 1

            Txt.text_draw("STAGE " + str(stage), WHITE, 25, 390, 30, screen)
            Txt.text_draw("MENTAL: ", WHITE, 25, 75, 30, screen)
            if stage == 6:
                pass
            elif stage <= 5:
                Txt.text_draw("UMASTROMERIA!", PINK, 48, 240, 180, screen)

        if index == 5:#アイキャッチ
            scrool = False
            sc_rect1 = False
            sc_rect2 = False
            sc_acc = False

            if stage == 1 or stage == 2:
                screen.fill(StCre.BLUE)

            if stage == 3 or stage == 4:
                screen.fill(StCre.BLACK) 

            if stage == 5 or stage == 6:
                screen.fill(StCre.PINK) 

            if stage == 1:
                En.stage0(screen)
                pygame.draw.rect(screen, StCre.BLUE,(rect1,175,480,75))
                pygame.draw.rect(screen, StCre.BLUE,(rect2,270,480,75))

            elif stage == 2:
                En.stage1(screen)
                pygame.draw.rect(screen, StCre.BLUE,(rect1,175,480,75))
                pygame.draw.rect(screen, StCre.BLUE,(rect2,270,480,75))

            elif stage == 3:
                En.stage2(screen)
                pygame.draw.rect(screen, StCre.BLACK,(rect1,175,480,75))
                pygame.draw.rect(screen, StCre.BLACK,(rect2,270,480,75))

            elif stage == 4:
                En.stage3(screen)
                pygame.draw.rect(screen, StCre.BLACK,(rect1,175,480,75))
                pygame.draw.rect(screen, StCre.BLACK,(rect2,270,480,75))
            elif stage == 5:
                En.stage4(screen)
                pygame.draw.rect(screen, StCre.PINK,(rect1,175,480,75))
                pygame.draw.rect(screen, StCre.PINK,(rect2,270,480,75))

            elif stage == 6:
                En.stage5(screen)
                pygame.draw.rect(screen, StCre.PINK,(rect1,175,480,75))
                pygame.draw.rect(screen, StCre.PINK,(rect2,270,480,75))

            enshutsu += 6
            if enshutsu >= 0:
                enshutsu = 0
                scrool = True

            if scrool == True:
                rect1 += 10
                if rect1 >= 480:
                    rect1 = 480
                    sc_rect1 = True

            if sc_rect1 == True:
                rect2 += 10
                if rect2 >= 480:
                    rect2 == 480
                    sc_rect2 = True
                    

            if sc_rect2 == True:
                if stage == 1 or stage == 2 or stage == 3:
                    from5to1 -= 4
                elif stage == 4 or stage ==  5 or stage == 6:
                    se_sairen.play()
                    acc = pygame.image.load("acc.png")
                    
                    screen.blit(acc, (from5toaccA,0)) # 960 > 0 > -960
                    from5toaccA -= 40

                    if from5toaccA <= 0:
                        from5toaccA = 0
                        from5toaccB -= 15
                        if from5toaccB <= -720:
                            from5toaccB = -720
                            sc_acc = True

                        if stage == 4:
                            En.text_draw_left("Accident!:ステージランダム生成!", (255,255,255), 40, from5toaccB, 160, screen)
                        if stage == 5:
                            En.text_draw_left("Accident!:確率で自分から反対ごっこ!", (255,255,255), 40, from5toaccB, 160, screen)
                        if stage == 6:
                            En.text_draw_left("Accident!:ステージランダム生成!", (255,255,255), 40, from5toaccB, 160, screen)
                    if sc_acc == True:
                        from5to1 -= 4


            if from5to1 == 0:
                enshutsu = -200
                rect1 = 0
                rect2 = 0

                scrool = False
                sc_rect1 = False
                sc_rect2 = False
                sc_acc = False
                chk_goal = False

                from5to1 = 60
                from5toaccA = 480
                from5toaccB = 480

                tmr_music = 0
                if stage == 5 or stage == 6:
                    pygame.mixer.music.load("bloomy.ogg")
                else:
                    pygame.mixer.music.load("arusutoromeria.ogg")
                index = 1

        if index == 6: #ゲームクリア
            screen.fill((0,0,0))
            en_timer1 -= 1

            En.ending(screen)

            if en_timer1 == 0:
                en_timer1 = 64 #VSC上なら128
                en_ind += 1
            if en_ind == 20:
                index = 7
                #en_ind = 19
            
        if index == 7: #済
            #pygame.mixer.music.stop()
            screen.fill((0,0,0))
            en_timer2 -= 1
            en_timer3 -= 1

            screen.blit(StCre.block[7], (210, 200))
            En.text_draw_center("THANK YOU FOR PLAYING!", (255,255,255), 32, 240, 100, screen)

            Moving_CE.draw_chara(screen)

            if Moving_CE.x_amana == 210:
                en_ind7 = 2
                en_timer2 = 60
                Moving_CE.x_amana = 211
                stop_ce = True

            if en_timer2 == 0:
                en_ind7 += 1
                en_timer2 = 90

                if en_ind7 >= 4:
                    stop_ce = False
                    en_ind7 = 4

            if en_timer3 == 0:
                index = 0
                

            Moving_CE.rect_x_update()
        
        if index == 8: #マニュアル #済

            screen.fill(StCre.BLUE)

            for i in range(6):
                screen.blit(StCre.block[1], (330 + 25 * i, 125))

            for i in range(6):
                screen.blit(StCre.block[1], (330 + 25 * i, 225))

            for i in range(6):
                screen.blit(StCre.block[1], (330 + 25 * i, 325))
            
#=======甘奈=====================================================================
            Moving_AT.draw_chara(screen)

            key = pygame.key.get_pressed()

            Moving_AT.t_move += 1
            Moving_AT.t_jump += 1
            Moving_AT.t_draw += 1
        #ここからジャンプ
            if Moving_AT.canJump == True and Moving_AT.land == True:
                if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                    if key[pygame.K_j] == True: #<===============================================
                        if Moving_AT.y == Moving_AT.ground - Moving_AT.h: #150 甘奈上角のy座標 
                            se_jump.play()  
                            Moving_AT.jump()
                            Moving_AT.jump_flag()

                if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                    if key[pygame.K_SEMICOLON] == True: #<===============================================
                        if Moving_AT.y == Moving_AT.ground - Moving_AT.h: #150 甘奈上角のy座標 
                            se_jump.play()  
                            Moving_AT.jump()
                            Moving_AT.jump_flag()

            Moving_AT.t_canjump -= 1

            if Moving_AT.t_canjump == 0:
                Moving_AT.jump_reset()
            
        #ここまでジャンプ
        
        #反対ごっこ
            if SOUSA_MODE == 1 or SOUSA_MODE == 3:
                if key[pygame.K_d] == True and Moving_AT.canTurn == True:  #<===============================================   
                    Moving_AT.turn_chara() #反対ごっこ
                    Moving_AT.turn_flag() #次の反対ごっこまでの猶予
                    se_turn.play()
            
            if SOUSA_MODE == 2 or SOUSA_MODE == 4:
                if key[pygame.K_a] == True and Moving_AT.canTurn == True:  #<===============================================   
                    Moving_AT.turn_chara() #反対ごっこ
                    Moving_AT.turn_flag() #次の反対ごっこまでの猶予
                    se_turn.play()

            Moving_AT.t_turn -= 1 #タイマーを起動

            if Moving_AT.t_turn == 0: #タイマーが0で
                Moving_AT.turn_reset() #ターン出来るようにする
        #ここまで反対ごっこ
            Moving_AT.jump_down()

            Moving_AT.rect_x_update()
            Moving_AT.rect_y_update() 

#=======ちきゆ=====================================================================
            Moving_CT.draw_chara(screen)

            key = pygame.key.get_pressed()

            Moving_CT.t_move += 1
            Moving_CT.t_jump += 1
            Moving_CT.t_draw += 1
        #ここからジャンプ
            if Moving_CT.canJump == True and Moving_CT.land == True:
                if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                    if key[pygame.K_k] == True: #<===============================================
                        if Moving_CT.y == Moving_CT.ground - Moving_CT.h: #150 甘奈上角のy座標 
                            se_jump.play()  
                            Moving_CT.jump()
                            Moving_CT.jump_flag()

                if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                    if key[pygame.K_COLON] == True: #<===============================================
                        if Moving_CT.y == Moving_CT.ground - Moving_CT.h: #150 甘奈上角のy座標 
                            se_jump.play()  
                            Moving_CT.jump()
                            Moving_CT.jump_flag()

            Moving_CT.t_canjump -= 1

            if Moving_CT.t_canjump == 0:
                Moving_CT.jump_reset()
            
        #ここまでジャンプ
        
        #反対ごっこ
            if key[pygame.K_s] == True and Moving_CT.canTurn == True: #<===============================================    
                Moving_CT.turn_chara() #反対ごっこ
                Moving_CT.turn_flag() #次の反対ごっこまでの猶予
                se_turn.play()
            
            Moving_CT.t_turn -= 1 #タイマーを起動

            if Moving_CT.t_turn == 0: #タイマーが0で
                Moving_CT.turn_reset() #ターン出来るようにする
        #ここまで反対ごっこ
            Moving_CT.jump_down()

            Moving_CT.rect_x_update()
            Moving_CT.rect_y_update()

#=======甜花=====================================================================
            Moving_TT.draw_chara(screen)

            key = pygame.key.get_pressed()

            Moving_TT.t_move += 1
            Moving_TT.t_jump += 1
            Moving_TT.t_draw += 1
        #ここからジャンプ
            if Moving_TT.canJump == True and Moving_TT.land == True:
                if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                    if key[pygame.K_l] == True: #<===============================================
                        if Moving_TT.y == Moving_TT.ground - Moving_TT.h: #150 甘奈上角のy座標 
                            se_jump.play()  
                            Moving_TT.jump()
                            Moving_TT.jump_flag()

                if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                    if key[pygame.K_RIGHTBRACKET] == True: #<===============================================
                        if Moving_TT.y == Moving_TT.ground - Moving_TT.h: #150 甘奈上角のy座標 
                            se_jump.play()  
                            Moving_TT.jump()
                            Moving_TT.jump_flag()

            Moving_TT.t_canjump -= 1

            if Moving_TT.t_canjump == 0:
                Moving_TT.jump_reset()
            
        #ここまでジャンプ
        
        #反対ごっこ
            if SOUSA_MODE == 1 or SOUSA_MODE == 3:
                if key[pygame.K_a] == True and Moving_TT.canTurn == True: #<===============================================
                    Moving_TT.turn_chara() #反対ごっこ
                    Moving_TT.turn_flag() #次の反対ごっこまでの猶予
                    se_turn.play()
            
            if SOUSA_MODE == 2 or SOUSA_MODE == 4:
                if key[pygame.K_d] == True and Moving_TT.canTurn == True: #<===============================================
                    Moving_TT.turn_chara() #反対ごっこ
                    Moving_TT.turn_flag() #次の反対ごっこまでの猶予
                    se_turn.play()

            Moving_TT.t_turn -= 1 #タイマーを起動

            if Moving_TT.t_turn == 0: #タイマーが0で
                Moving_TT.turn_reset() #ターン出来るようにする
        #ここまで反対ごっこ
            Moving_TT.jump_down()

            Moving_TT.rect_x_update()
            Moving_TT.rect_y_update()
#============================================================================
            En.tuto_rial(screen)
            
            t_key -= 1
            
            if t_key <= 0:
                t_key = 0
                if key[pygame.K_LEFT] == True:
                    tuto_ind -= 1
                    t_key = 10
                if key[pygame.K_RIGHT] == True:
                    tuto_ind += 1
                    t_key = 10

                if key[pygame.K_SPACE] == True:
                    index = 0
                    t_key = 10

            if tuto_ind <= 1:
                tuto_ind = 1
            if tuto_ind >= 3:
                tuto_ind = 3

        if index == 9: #コンフィグ #済

            screen.fill(StCre.BLUE)

            for i in range(6):
                screen.blit(StCre.block[1], (330 + 25 * i, 125))

            for i in range(6):
                screen.blit(StCre.block[1], (330 + 25 * i, 225))

            for i in range(6):
                screen.blit(StCre.block[1], (330 + 25 * i, 325))
            

#=======甘奈=====================================================================
            Moving_AT.draw_chara(screen)

            key = pygame.key.get_pressed()

            Moving_AT.t_move += 1
            Moving_AT.t_jump += 1
            Moving_AT.t_draw += 1
        #ここからジャンプ
            if Moving_AT.canJump == True and Moving_AT.land == True:
                if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                    if key[pygame.K_j] == True: #<===============================================
                        if Moving_AT.y == Moving_AT.ground - Moving_AT.h: #150 甘奈上角のy座標 
                            se_jump.play()  
                            Moving_AT.jump()
                            Moving_AT.jump_flag()

                if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                    if key[pygame.K_SEMICOLON] == True: #<===============================================
                        if Moving_AT.y == Moving_AT.ground - Moving_AT.h: #150 甘奈上角のy座標 
                            se_jump.play()  
                            Moving_AT.jump()
                            Moving_AT.jump_flag()

            Moving_AT.t_canjump -= 1

            if Moving_AT.t_canjump == 0:
                Moving_AT.jump_reset()
            
        #ここまでジャンプ
        
        #反対ごっこ
            if SOUSA_MODE == 1 or SOUSA_MODE == 3:
                if key[pygame.K_d] == True and Moving_AT.canTurn == True:  #<===============================================   
                    Moving_AT.turn_chara() #反対ごっこ
                    Moving_AT.turn_flag() #次の反対ごっこまでの猶予
                    se_turn.play()
            
            if SOUSA_MODE == 2 or SOUSA_MODE == 4:
                if key[pygame.K_a] == True and Moving_AT.canTurn == True:  #<===============================================   
                    Moving_AT.turn_chara() #反対ごっこ
                    Moving_AT.turn_flag() #次の反対ごっこまでの猶予
                    se_turn.play()

            Moving_AT.t_turn -= 1 #タイマーを起動

            if Moving_AT.t_turn == 0: #タイマーが0で
                Moving_AT.turn_reset() #ターン出来るようにする
        #ここまで反対ごっこ
            Moving_AT.jump_down()

            Moving_AT.rect_x_update()
            Moving_AT.rect_y_update() 

#=======ちきゆ=====================================================================
            Moving_CT.draw_chara(screen)

            key = pygame.key.get_pressed()

            Moving_CT.t_move += 1
            Moving_CT.t_jump += 1
            Moving_CT.t_draw += 1
        #ここからジャンプ
            if Moving_CT.canJump == True and Moving_CT.land == True:
                if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                    if key[pygame.K_k] == True: #<===============================================
                        if Moving_CT.y == Moving_CT.ground - Moving_CT.h: #150 甘奈上角のy座標 
                            se_jump.play()  
                            Moving_CT.jump()
                            Moving_CT.jump_flag()

                if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                    if key[pygame.K_COLON] == True: #<===============================================
                        if Moving_CT.y == Moving_CT.ground - Moving_CT.h: #150 甘奈上角のy座標 
                            se_jump.play()  
                            Moving_CT.jump()
                            Moving_CT.jump_flag()

            Moving_CT.t_canjump -= 1

            if Moving_CT.t_canjump == 0:
                Moving_CT.jump_reset()
            
        #ここまでジャンプ
        
        #反対ごっこ
            if key[pygame.K_s] == True and Moving_CT.canTurn == True: #<===============================================    
                Moving_CT.turn_chara() #反対ごっこ
                Moving_CT.turn_flag() #次の反対ごっこまでの猶予
                se_turn.play()
            
            Moving_CT.t_turn -= 1 #タイマーを起動

            if Moving_CT.t_turn == 0: #タイマーが0で
                Moving_CT.turn_reset() #ターン出来るようにする
        #ここまで反対ごっこ
            Moving_CT.jump_down()

            Moving_CT.rect_x_update()
            Moving_CT.rect_y_update()

#=======甜花=====================================================================
            Moving_TT.draw_chara(screen)

            key = pygame.key.get_pressed()

            Moving_TT.t_move += 1
            Moving_TT.t_jump += 1
            Moving_TT.t_draw += 1
        #ここからジャンプ
            if Moving_TT.canJump == True and Moving_TT.land == True:
                if SOUSA_MODE == 1 or SOUSA_MODE == 2:
                    if key[pygame.K_l] == True: #<===============================================
                        if Moving_TT.y == Moving_TT.ground - Moving_TT.h: #150 甘奈上角のy座標 
                            se_jump.play()  
                            Moving_TT.jump()
                            Moving_TT.jump_flag()

                if SOUSA_MODE == 3 or SOUSA_MODE == 4:
                    if key[pygame.K_RIGHTBRACKET] == True: #<===============================================
                        if Moving_TT.y == Moving_TT.ground - Moving_TT.h: #150 甘奈上角のy座標 
                            se_jump.play()  
                            Moving_TT.jump()
                            Moving_TT.jump_flag()

            Moving_TT.t_canjump -= 1

            if Moving_TT.t_canjump == 0:
                Moving_TT.jump_reset()
            
        #ここまでジャンプ
        
        #反対ごっこ
            if SOUSA_MODE == 1 or SOUSA_MODE == 3:
                if key[pygame.K_a] == True and Moving_TT.canTurn == True: #<===============================================
                    Moving_TT.turn_chara() #反対ごっこ
                    Moving_TT.turn_flag() #次の反対ごっこまでの猶予
                    se_turn.play()
            
            if SOUSA_MODE == 2 or SOUSA_MODE == 4:
                if key[pygame.K_d] == True and Moving_TT.canTurn == True: #<===============================================
                    Moving_TT.turn_chara() #反対ごっこ
                    Moving_TT.turn_flag() #次の反対ごっこまでの猶予
                    se_turn.play()

            Moving_TT.t_turn -= 1 #タイマーを起動

            if Moving_TT.t_turn == 0: #タイマーが0で
                Moving_TT.turn_reset() #ターン出来るようにする
        #ここまで反対ごっこ
            Moving_TT.jump_down()

            Moving_TT.rect_x_update()
            Moving_TT.rect_y_update()
#============================================================================
            En.config(screen)

            if t_key <= 0:
                t_key = 0
                if key[pygame.K_LEFT] == True:
                    SOUSA_MODE -= 1
                    t_key = 10
                if key[pygame.K_RIGHT] == True:
                    SOUSA_MODE += 1
                    t_key = 10

                if key[pygame.K_SPACE] == True:
                    index = 0
                    t_key = 10

            if SOUSA_MODE < 1:
                SOUSA_MODE = 2
            if SOUSA_MODE > 2:
                SOUSA_MODE = 1

#======================================================
        tmr_music += 1
        t_key -= 1

        pygame.display.update()        
        clock.tick(30)
        await asyncio.sleep(0)

asyncio.run(main())
