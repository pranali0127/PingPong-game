# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

class PongPaddle(Widget):
    score = NumericProperty(0)
    def bounce_ball(self,ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -0.9
    

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x,velocity_y)
    
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        
#on_touch_down() - when fingers/mouse touches screen
#on_touch_up() - when we lift finger after touching screen
#on_touch_move() - when we drg our finger on the screen

    
class PongGame(Widget):
    
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    
    def serve_ball(self):
        self.ball.velocity = Vector(4,0).rotate(randint(0,360))
    
    def reset_ball(self):
        self.ball.pos = self.parent.center
        self.serve_ball()


    def update(self,dt):
        self.ball.move()
        
        #bounce off top and bottom
        if(self.ball.y < 0 or self.ball.y > self.height -50):
            self.ball.velocity_y *=-1
        
        #bounce off left 
        if(self.ball.x < 0):
            self.ball.velocity_x *=-1
            self.player1.score += 1
            self.reset_ball()
        #bounce off right
        if (self.ball.x > self.width - 50):
            self.ball.velocity_x *=-1
            self.player2.score +=1
            self.reset_ball()
            
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
    
    def on_touch_move(self,touch):
        if touch.x < self.width / 1/4:
            self.player1.center_y = touch.y
        if touch.x  >self.width * 3/4:
            self.player2.center_y = touch.y
        
class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game
PongApp().run() 