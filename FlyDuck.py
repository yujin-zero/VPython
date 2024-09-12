from vpython import *
import random

def on_keydown(event):
    global duck
    global duckDirection
    global lifeNum
    if event.key == "left" : 
        duck.v.x -= 1
        if duckDirection == "R" :    
            duck.rotate(angle=radians(180), axis=vec(0, 1, 0))
            duck.v.x -= 3
            duckDirection = "L"
        
    elif event.key == "right":
        duck.v.x += 1
        if duckDirection == "L" :
            duck.rotate(angle=radians(180), axis=vec(0, 1, 0))
            duck.v.x += 3
            duckDirection = "R"
        
    elif event.key == "up":
        if lifeNum>0 :        
            Jump()
    elif event.key == "down" :
        Fall()
        
def Jump() :
    global lifeNum
    duck.v.y = 10
    lifeNum -= 1
    if lifeNum==2 :
        life[2].color = color.black
    elif lifeNum == 1 :
        life[1].color = color.black
    elif lifeNum == 0 :
        life[0].color = color.black
    
def Fall() :
    duck.v.y = -10
    
def calc_im(pBox, pbox, kv) :
    r1 = pbox.pos.y + 0.5*pbox.size.y
    r2 = pBox.pos.y + 0.5*pBox.size.y
    floatcheck = r1 - r2
    if floatcheck > 0 :
        pbox.volume_im = pbox.volume - floatcheck*pbox.size.x*pbox.size.z
    else :
        pbox.volume_im = pbox.volume
    if pbox.volume_im < 0 :
        pbox.volume_im = 0
    
    kv_im = pbox.volume_im/pbox.volume*kv
    return pbox.volume_im, kv_im
    

scene.title = "오리날다"
scene.range = 30
scene.background = vec(0.529, 0.808, 1.0)
scene.bind("keydown",on_keydown)

iceBlock=[]
for i in range(9) :
    iceBlock[i] = box(size=vec(6,1,4),pos=vec(16*i+8,i*3,0))
    
wind=[]
for i in range(4):
    newV = vec(random.randint(40,80),0,0)
    wind[i] = arrow(pos=vec(160-20*i,random.randint(10,30),0),color=color.red,axis=vec(-1,0,0),v=-1*newV , size=newV/8)


#초기오리
duckHead = sphere(pos=vec(0,0,0),color=color.yellow,radius=0.8)
duckMouth = cone(pos=vec(0,0,0), color=color.orange, axis=vec(1.5,0,0),radius=0.5)
duckBody = ellipsoid(pos=vec(-1,-1.2,0),color=color.yellow,length=2.5,width=2,height=1.5)
duckEye1 = sphere(pos=vec(0.4,0.2,0.8),color=color.black,radius=0.1)
duckEye2 = sphere(pos=vec(0.4,0.2,-0.8),color=color.black,radius=0.1)
duckLeg1 = cylinder(pos=vec(-1,-2,0.8),color=color.orange,radius=0.1,axis=vec(0,1,0))
duckLeg2 = cylinder(pos=vec(-1,-2,-0.8),color=color.orange,radius=0.1,axis=vec(0,1,0))
duck = compound([duckHead,duckMouth,duckBody,duckEye1,duckEye2,duckLeg1,duckLeg2])
duckDirection = "R"
duckBody_radius = duckBody.length / 2  
duck_area = pi * duckBody_radius**2 + pi*duckHead.radius**2

ground = box(pos=vec(-40,-20,0),size=vec(80,30,10))
ground_arrival = box(pos=vec(200,-20,0), size=vec(80,30,10))

# 깃발 생성
flag_pole = cylinder(pos=vec(ground_arrival.pos.x-30, ground_arrival.pos.y+15, 0),
                     axis=vec(0, 10, 0),
                     radius=0.2, color=color.gray(0.7))
flag = box(pos=vec(flag_pole.pos.x+2,flag_pole.pos.y+8,0),
           size=vec(4,2,0.2),
           color=color.red)
wall = box(pos=vec(160.5,10,0),texture=textures.wood,size=vec(1,30,10))
wall2 = box(pos=vec(-80,10,0),size=vec(1,30,10),texture=textures.wood)

water = box(pos=vec(80, -25, 0), size=vec(160, 30, 10),color=color.blue,opacity=0.3)
#duck.pos = vec(-20,10,0)
duck.pos = vec(-20,10,0)
duck.v = vec(0,0,0)
scene.center = duck.pos
time = label(text="시간",pos=scene.center+vec(38,25,0),box=False)
start = label(text="Starting Point",pos=vec(-10,-10,10))
duckVel = label(text="오리속도:"+str(duck.v.x),pos=scene.center+vec(38,22,0),box=False)
duck.rho = 300
water.rho = 1000
duck.volume = duck.size.x * duck.size.y * duck.size.z
duck.m = duck.rho*duck.volume
kv = 1000
kv_im = kv
Cd = 0.5

life = []
life[0] = box(color=color.green,pos=scene.center+vec(-45,25,0),size=vec(2,2,0.1))
life[1] = box(color=color.green,pos=scene.center+vec(-40,25,0),size=vec(2,2,0.1))
life[2] = box(color=color.green,pos=scene.center+vec(-35,25,0),size=vec(2,2,0.1))
lifeNum = 3

g=vec(0,-9.8,0)

t=0
dt=0.03
thold = 0.001

while True:
    rate(2/dt)    
    duck.f = duck.m * g
    if (duck.pos.x > 0 ) and (duck.pos.x < 160) and (duck.pos.y < -10) :
        duck.volume_im, kv_im = calc_im(water,duck,kv)
        duck.f -= kv_im*mag(duck.v)**2*norm(duck.v)
        duck.f -= water.rho*duck.volume_im*g
        
    for nowWind in wind :
        nowWind.pos += nowWind.v/3*dt
        if (abs(duck.pos.y - nowWind.pos.y) < 2) and (duck.pos.x >= (nowWind.pos.x-nowWind.size.x/2)) and (duck.pos.x <= (nowWind.pos.x+nowWind.size.x/2)) and nowWind.color != color.yellow :
            nowWind.color = color.yellow
            duck.v_w = duck.v - nowWind.v
            drag = -0.5*duck.rho*Cd*duck_area*mag(duck.v_w)**2*norm(duck.v_w)
            duck.f += drag
        if nowWind.pos.x <= 0 :
            nowWind.v = -1*vec(random.randint(40,80),0,0)
            nowWind.size = -1*nowWind.v/8
            nowWind.pos = vec(160,random.randint(10,30),0)
            nowWind.color=color.red
    
    
    duck.v += duck.f/duck.m*dt
    duck.pos += duck.v * dt
    
    for block in iceBlock:
        if duck.pos.y > block.pos.y-0.5  and duck.pos.x > block.pos.x - 3 and duck.pos.x < block.pos.x + 3 and duck.pos.y <= block.pos.y +2:
            duck.pos.y = block.pos.y + 2
            lifeNum = 3
            for i in range(3):
                life[i].color = color.green
    
    
    
    
    if(duck.pos.y <= -3) and ((duck.pos.x <=0) or (duck.pos.x >=160)):
        duck.pos.y = -3
        lifeNum = 3
        for i in range(3):
            life[i].color = color.green
    
    if mag(duck.pos-flag_pole.pos) <3 :
        flag.color = color.green
        break

    if duck.pos.x >= 159 and duck.pos.x <= 161 and duck.pos.y <= 25 :
        duck.pos.x = 159
    if duck.pos.x <=-79 :
        duck.pos.x = -79
    
    
    time.text="시간:"+str(round(t))  
    scene.center = vec(duck.pos.x,10,0)
    time.pos=scene.center + vec(38,25,0)
    duckVel.text="오리속도:"+str(round(duck.v.x,1))
    duckVel.pos = scene.center + vec(38,22,0)
    life[0].pos = scene.center + vec(-45,25,0)
    life[1].pos = scene.center + vec(-40,25,0)
    life[2].pos = scene.center + vec(-35,25,0)
    
    
    

    
    t+=dt
   
label(pos=scene.center, text='Clear!',color=color.red, height=30,box=False)
print("걸린시간= ",t )


