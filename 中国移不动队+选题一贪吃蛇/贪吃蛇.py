#coding=UTF-8
from Tkinter import *
from random import randint
import tkMessageBox
class Grid(object):
  #构造函数（为数据成员设置初值或进其他必要的初始化）
  def __init__(self, master=None,height=16, width=24, offset=10, grid_width=50, bg="#808080"):
    self.height = height#定义实例属性
    self.width = width
    self.offset = offset
    self.grid_width = grid_width
    self.bg = bg
    self.canvas = Canvas(master, width=self.width*self.grid_width+2*self.offset, height=self.height*self.grid_width+
                                              2*self.offset, bg=self.bg)
    self.canvas.pack(side=RIGHT, fill=Y)
  def draw(self, pos, color, ):
    x = pos[0] * self.grid_width + self.offset
    y = pos[1] * self.grid_width + self.offset
    #outline属性要与网格的背景色（self.bg）相同，要不然会很丑
    self.canvas.create_rectangle(x, y, x + self.grid_width, y + self.grid_width, fill=color, outline=self.bg)
class Food(object):
  def __init__(self, grid, color = "#23D978"):
    self.grid = grid
    self.color = color
    self.set_pos()
    self.type = 1
  def set_pos(self):
    x = randint(0, self.grid.width - 1)
    y = randint(0, self.grid.height - 1)
    self.pos = (x, y)
  def display(self):
    self.grid.draw(self.pos, self.color)
class Snake(object):
  def __init__(self, grid, color = "#000000"):
    self.grid = grid
    self.color = color
    self.body = [(8, 11), (8, 12), (8, 13)]
    self.direction = "Up"
    for i in self.body:
      self.grid.draw(i, self.color)
  #这个方法用于游戏重新开始时初始化贪吃蛇的位置
  def initial(self):
    while not len(self.body) == 0:
      pop = self.body.pop()
      self.grid.draw(pop, self.grid.bg)
    self.body = [(8, 11), (8, 12), (8, 13)]
    self.direction = "Up"
    self.color = "#000000"
    for i in self.body:
      self.grid.draw(i, self.color)
  #蛇像一个指定点移动
  def move(self, new):
    self.body.insert(0, new)
    pop = self.body.pop()
    self.grid.draw(pop, self.grid.bg)
    self.grid.draw(new, self.color)
  #蛇像一个指定点移动，并增加长度
  def add(self ,new):
    self.body.insert(0, new)
    self.grid.draw(new, self.color)
  #蛇吃到了特殊食物1，剪短自身的长度
  def cut_down(self,new):
    self.body.insert(0, new)
    self.grid.draw(new, self.color)
    for i in range(0,3):
      pop = self.body.pop()
      self.grid.draw(pop, self.grid.bg)
  #蛇吃到了特殊食物2，回到最初长度
  def init(self, new):
    self.body.insert(0, new)
    self.grid.draw(new, self.color)
    while len(self.body) > 3:
      pop = self.body.pop()
      self.grid.draw(pop, self.grid.bg)
   #蛇吃到了特殊食物3，改变了自身的颜色,纯属好玩
  def change(self, new, color):
    self.color = color
    self.body.insert(0, new)
    for item in self.body:
      self.grid.draw(item, self.color)
class SnakeGame(Frame):
  def __init__(self, master):
    Frame.__init__(self, master)
    self.grid = Grid(master)
    self.snake = Snake(self.grid)
    self.food = Food(self.grid)
    self.gameover = False
    self.score = 0
    self.status = ['run', 'stop']
    self.speed = 300
    self.grid.canvas.bind_all("<KeyRelease>", self.key_release)
    self.display_food()
    #用于设置变色食物 #差不多从这以下是314的
    self.color_c = ("#FFB6C1","#6A5ACD","#0000FF","#F0FFF0","#FFFFE0","#F0F8FF","#EE82EE","#000000","#5FA8D9","#32CD32")#变色可选颜色
    self.i = 0
    #界面左侧显示分数
    self.m = StringVar()#随分数的变化更新分数的显示
    self.ft1 = ('Fixdsys', 40, "bold")
    self.m1 = Message(master, textvariable=self.m, aspect=5000, font=self.ft1, bg="#696969")#设置显示内容及背景颜色
    self.m1.pack(side=LEFT, fill=Y)
    self.m.set("Score:"+str(self.score))#分数显示
  #这个方法用于游戏重新开始时初始化游戏
  def initial(self):
    self.gameover = False#游戏结束
    self.score = 0#初始化分数
    self.m.set("Score:"+str(self.score))
    self.snake.initial()#初始化蛇的位置和长度
  #type1:普通食物 type2:减少2 type3:大乐透，回到最初状态 type4:吃了会变色
  def display_food(self): #显示食物
    self.food.color = "#23D978" #普通食物的颜色
    self.food.type = 1 #普通食物的序号
    if randint(0, 40) == 5:#生成随机数
      self.food.color = "#FFD700"#大乐透食物的颜色
      self.food.type = 3#生成大乐透食物
      while (self.food.pos in self.snake.body):#如果食物的位置与蛇的身体有重合
        self.food.set_pos()#重新设定食物的位置
      self.food.display()#显示新的食物
    elif randint(0, 4) == 2:
      self.food.color = "#EE82EE"#导致变色食物的颜色
      self.food.type = 4
      while (self.food.pos in self.snake.body):#如果食物的位置与蛇的身体有重合
        self.food.set_pos()#重新设定食物的位置
      self.food.display()#重新显示食物
    elif len(self.snake.body) > 10 and randint(0, 16) == 5:#如果蛇的全长超过10且随机数为5
      self.food.color = "#BC8F8F"#生成吃了会变短的食物的颜色
      self.food.type = 2
      while (self.food.pos in self.snake.body):#如果食物的位置与蛇的身体有重合
        self.food.set_pos()#重新设定食物的位置
      self.food.display()#显示新的食物
    else:
      while (self.food.pos in self.snake.body):#如果食物的位置与蛇的身体有重合
        self.food.set_pos()#重新设定食物的位置
      self.food.display()#重新显示食物
  def key_release(self, event):
    key = event.keysym
    key_dict = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}#字典存储表示方向的词
    #蛇不可以像自己的反方向走
    if key_dict.has_key(key) and not key == key_dict[self.snake.direction]:#如果键入的方向不为蛇运动的反方向
      self.snake.direction = key#则键入的方向为改变的蛇运动的方向
      self.move()#蛇继续运动
    elif key == 'p':#如果用户键入p
      self.status.reverse()#则暂停游戏
  def run(self):
    #首先判断游戏是否暂停
    if not self.status[0] == 'stop':#如果游戏没有暂停
      #判断游戏是否结束
      if self.gameover == True:#如果游戏结束
        message = tkMessageBox.showinfo("Game Over", "your score: %d" % self.score)#显示游戏的结束信息
        if message == 'ok':#如果用户确认
          self.initial()#游戏初始化
      if self.food.type == 4:#如果食物为变色食物
        color = self.color_c[self.i]#贪吃蛇的颜色
        self.i = (self.i+1)%10#贪吃蛇吃了后变长
        self.food.color = color#食物的颜色
        self.food.display()#食物的颜色显色
        self.move(color)#贪吃蛇移动
      else:
        self.move()#蛇继续运动
    self.after(self.speed, self.run)
  def move(self, color="#EE82EE"):
    # 计算蛇下一次移动的点
    head = self.snake.body[0]
    if self.snake.direction == 'Up':#如果蛇向上移动
      if head[1] - 1 < 0:
        new = (head[0], 16)
      else:
        new = (head[0], head[1] - 1)
    elif self.snake.direction == 'Down':#如果蛇向下移动
      new = (head[0], (head[1] + 1) % 16)
    elif self.snake.direction == 'Left':#如果蛇向左移动
      if head[0] - 1 < 0:
        new = (24, head[1])
      else:
        new = (head[0] - 1, head[1])
    else:
      new = ((head[0] + 1) % 24, head[1])
      #撞到自己，设置游戏结束的标志位，等待下一循环
    if new in self.snake.body:
      self.gameover=True
    #吃到食物
    elif new == self.food.pos:#初始化食物的位置
      if self.food.type == 1:#如果吃了特殊食物1
        self.snake.add(new)#吃了增加体型
      elif self.food.type == 2:#如果吃了特殊食物2
        self.snake.cut_down(new)#吃了减少体型
      elif self.food.type == 4:#如果吃了特殊食物4
        self.snake.change(new, color)#吃了会根据食物的颜色变色
      else:
        self.snake.init(new)
      self.display_food()#显示食物的位置
      self.score = self.score+1#分数加1
      self.m.set("Score:" + str(self.score))
    #什么都没撞到，继续前进
    else:
      self.snake.move(new)#游戏重新开始
if __name__ == '__main__':#模块是对象，并且所有的模块都有一个内置属性 __name__。在cmd 中直接运行.py文件,则__name__的值是'__main__';此句判断是否直接运行.py文件
  root = Tk()#调用python的软件编程窗口
  snakegame = SnakeGame(root)#调用SnakeGame
  snakegame.run()#贪吃蛇游戏开始运行
  snakegame.mainloop()#一旦检测到事件，就刷新组件。贪吃蛇的方块立即在光标那个位置显示出来

