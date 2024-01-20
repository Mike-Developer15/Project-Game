import pygame
import Functions


pygame.init()

screen = pygame.display.set_mode((1280,720))
#fullscreen mode if I want
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

clock = pygame.time.Clock()
server = False
connected = True
width = screen.get_width()
height = screen.get_height()
menu = True
while menu:
    # Process player inputs.\
    mouse = pygame.mouse.get_pos()
    button1_logic = width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button1_logic:
                connected = False
                menu = False


    screen.fill("black")  # Fill the display with a solid color
    keys = pygame. key.get_pressed()

    

    if button1_logic: 
        pygame.draw.rect(screen,"white",[width/2,height/2,140,40]) 
          
    else: 
        pygame.draw.rect(screen,"red",[width/2,height/2,140,40]) 

    #starts the server side
    if keys[pygame.K_s]:
        pygame.draw.rect(screen,"green",[width/2,height/2,140,40])
        server = True
        menu = False
    #starts the client side 
    if keys[pygame.K_c]:
        pygame.draw.rect(screen,"blue",[width/2,height/2,140,40])
        menu = False
    #starts single player
    if keys[pygame.K_q]:
        connected = False
        menu = False
    # Render the graphics here.
    # ...
        


    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)

#declaring player varaibles
playerpos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
onlineplayerpos = pygame.Vector2(0,100)
bullet = pygame.Vector2(-10, -10)
onlineBullet = pygame.Vector2(-10,-10)
lives = 3
flying = False
jumpCount = 50

#ground
mainPlat = pygame.Rect(screen.get_width()/2 - 400, screen.get_height() - 100, 800, 10)
lSidePlat = pygame.Rect(screen.get_width()/4 - 200, screen.get_height() - 400, 200, 10)


#online player
online = Functions.ConnectionHelper(server);


#Connects to the other player is appliciable


while True:
    ground = False
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #close()  # close the connection
            pygame.quit()
            raise SystemExit


    #local network data tranfer shit
    message = str(playerpos.x) + " " + str(playerpos.y) + " " + str(bullet.x) + " " + str(bullet.y) #todo code in bullet data tranfer
    
    if connected:
        online.ConnectionProtocol(message)
        onlineplayerpos.x, onlineplayerpos.y, onlineBullet.x, onlineBullet.y = online.ParseData();


    #ground logic
    if playerpos.y > screen.get_height():
        #playerpos.y = screen.get_height() - 20
        ground = True
        lives-=1
        playerpos.x = screen.get_width() / 2
        playerpos.y = screen.get_height() / 2
        
    if pygame.Rect(playerpos.x, playerpos.y, 20, 20).colliderect(mainPlat):
        ground = True;
    if pygame.Rect(playerpos.x, playerpos.y, 20, 20).colliderect(lSidePlat):
        ground = True;
    

    #get what keys are pressed
    keys = pygame. key.get_pressed()
    if keys[pygame.K_a]:
        playerpos.x -= 10;
    if keys[pygame.K_d]:
        playerpos.x += 10;
    if keys[pygame.K_s] and not ground:
        playerpos.y += 5;
    

    #jumping mechanics
    if keys[pygame.K_SPACE] and jumpCount > 0:
       flying = True
    else:
        flying = False
    if not ground and not flying:
       playerpos.y+= 5
    if flying:
        jumpCount-=1;
        playerpos.y -=10
    if ground: # This will execute if our jump is finished
        jumpCount = 50
        flying = False
            

    screen.fill("black")  # Fill the display with a solid color

    # Render the graphics here.
    # ...
    #displays players on the screen
    pygame.draw.rect(screen, "red", pygame.Rect(playerpos.x, playerpos.y, 20, 20))
    pygame.draw.rect(screen, "blue", pygame.Rect(onlineplayerpos.x, onlineplayerpos.y, 20, 20))
    pygame.draw.rect(screen, "green", mainPlat)
    pygame.draw.rect(screen, "green", lSidePlat)

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)
