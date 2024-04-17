
from queue import PriorityQueue
import math
import pygame


pygame.init()

q = PriorityQueue()

N = 50
SCALE = 700/N

WIDTH, HEIGHT = 700,700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0,0,0)
WHITE=(255, 255, 255)
BLUE = (0,255,255)
RED = (255, 0, 0)
GREEN = (0,255,0)

FPS = 40

#convert by scale
START = (int(N/10),int(N/10))
END =(int(N-(N/10)),int(N-(N/10)))

pygame.display.set_caption("A* Algorithm")

world = {}  
dist = {}   
vis = {}  
par = {}   
'''
1 if obstacle
2 if processing
3 if processed
4 if path
'''

for i in range(N):
    world[i]=[]
    dist[i]=[]
    vis[i]=[]
    par[i]=[]
    for j in range(N):
        world[i].append(0)
        dist[i].append(-1)
        vis[i].append(0)
        par[i].append((-1,-1))

def centers(x, y):
    return (SCALE*x+(SCALE-1)/2, SCALE*y+(SCALE-1)/2)

def show():
    global world
    for i in range(N):
        for j in range(N):
            if(world[i][j]==1):
                pygame.draw.rect(WIN, BLACK, (SCALE*i, SCALE*j, SCALE-1, SCALE-1))
            if(world[i][j]==2):
                pygame.draw.rect(WIN, GREEN, (SCALE*i, SCALE*j, SCALE-1, SCALE-1))
            if(world[i][j]==3):
                pygame.draw.rect(WIN, BLUE, (SCALE*i, SCALE*j, SCALE-1, SCALE-1))   
            if(world[i][j]==0):
                pygame.draw.rect(WIN, WHITE, (SCALE*i,SCALE*j, SCALE-1, SCALE-1))
            if((i,j) == START or (i,j) == END):
                pygame.draw.rect(WIN, RED, (SCALE*i,SCALE*j, SCALE-1, SCALE-1))
                continue
            if(world[i][j]==4):
                pygame.draw.rect(WIN, BLUE, (SCALE*i,SCALE*j, SCALE-1, SCALE-1))
                p1,p2 = par[i][j]
                pygame.draw.line(WIN, RED, (centers(i,j)), (centers(p1, p2)), 4)
            


#functions:

def coord(x,y):
    a=int(x/SCALE)
    b=int(y/SCALE)
    global world
    world[a][b]=1


def heuristic(x,y):
    (a,b)=END
    i = (x-a)*(x-a)
    j = (y-b)*(y-b)
    ret = math.sqrt(i+j)
    return int(ret)*10




run = True
execute = False
done = False
isPressed = False

while run:

    #time delay
    pygame.time.delay(FPS)

    for event in pygame.event.get():
        if(execute == False):
            if event.type == pygame.MOUSEBUTTONDOWN:
                isPressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                isPressed = False
            elif event.type == pygame.MOUSEMOTION and isPressed == True:  
                pos = pygame.mouse.get_pos()
                coord(*pos)

        if (event.type==pygame.QUIT): run = False
    

    keys = pygame.key.get_pressed()

    #A star

    if(execute==True and done == False):
        done = True

       

        (aa,bb)=START
        dist[aa][bb]=0

        q.put((heuristic(aa,bb), (aa, bb)))

        while q.qsize() > 0:

            
            wt, pos= q.get()
           
            x, y = pos

            if(pos == END):
                break

            #print('*')
            #print(wt, x, y)



            if(vis[x][y] == 1):
                continue
            vis[x][y] = 1

            if((x,y)!=START and (x,y)!=END):world[x][y]=3

            dx=[1,-1,0,0]
            dy=[0,0,1,-1]

            for i in range(4):
                X = dx[i]+x
                Y = dy[i]+y
                if X<0 or Y<0 or X>=N or Y>=N:
                    continue
                if world[X][Y]==1: continue
                val = 10+dist[x][y]
                if(val<dist[X][Y] or dist[X][Y]==-1):
                    dist[X][Y]=val
                    q.put((dist[X][Y]+heuristic(X,Y),(X,Y)))
                    par[X][Y]=(x,y)
                    world[X][Y]=2
            
            dx=[1,-1,1,-1]
            dy=[1,1,-1,-1]

            for i in range(4):
                X = dx[i]+x
                Y = dy[i]+y
                if X<0 or Y<0 or X>=N or Y>=N:
                    continue
                if world[X][Y]==1: continue
                val = 14+dist[x][y]
                if(val<dist[X][Y] or dist[X][Y]==-1):
                    dist[X][Y]=val
                    q.put((dist[X][Y]+heuristic(X,Y),(X,Y)))
                    par[X][Y]=(x,y)
                    world[X][Y]=2


            WIN.fill((0,0,0))
            show()
            pygame.time.delay(FPS)
            pygame.display.update()
           # node = q.get()
        
        (X,Y)=END
        while (X,Y)!=(-1,-1):
            world[X][Y]=4
            (X,Y)=par[X][Y]



    if keys[pygame.K_SPACE]:
        execute = True
    

    WIN.fill((0,0,0))
    show()
    pygame.display.update()

 
pygame.quit()

