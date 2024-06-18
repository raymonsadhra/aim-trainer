#imports needed to run the aim trainer 
import math
import random
import time
import pygame

#initializing pygame and pygame mixer
pygame.init()   
pygame.mixer.init()
background_music = "sidehustle.mp3"
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)
hit = pygame.mixer.Sound("ding.mp3")



#x,y for window
WIDTH, HEIGHT  = 800, 600
#window display 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#caption for window
pygame.display.set_caption("Aim Trainer")

#rate at which targets appear
TARGET_INCREMENT = 750

COLOR = ""
SECOND_COLOR = ""
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
BG_VALUE = (0,25,40)
LIVES = 5
TOP_BAR_HEIGHT = 50
LABEL_FONT = pygame.font.SysFont("comicsans", 24)

class Button:
     def __init__(self, text, x, y, width, height, color, hover_color, font):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = font

     def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

     def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
def draw_start_screen(win, buttons):
    win.fill(BG_VALUE)
    for button in buttons:
        button.draw(win)
    pygame.display.update()
     
def start_screen():
          font = pygame.font.SysFont("comicsans", 30)
          buttons = [
              Button("Easy", WIDTH//2 - 75, HEIGHT//2 - 100, 150, 50, (0, 255, 0), (0, 200, 0), font),
              Button("Medium", WIDTH//2 - 75, HEIGHT//2 - 25, 150, 50, (255, 255, 0), (200, 200, 0), font),
              Button("Hard", WIDTH//2 - 75, HEIGHT//2 + 50, 150, 50, (255, 0, 0), (200, 0, 0), font),
            ]
          run = True
          while run:
              draw_start_screen(WIN, buttons)
              for event in pygame.event.get():
                  #if event.type==pygame.QUIT():
                   #   pygame.quit()
                    #  quit()
                  for button in buttons:
                      if button.is_clicked(event):
                          return button.text
              


class Target:
    MAX_SIZE = 30
    GROWTH = 0.2
    #COLOR = "green"
    #SECOND_COLOR = "white"
    

    def __init__(self,x,y, COLOR, SECOND_COLOR):
        self.x=x
        self.y=y
        self.size = 0 
        self.grow = True
        self.COLOR = COLOR
        self.SECOND_COLOR = SECOND_COLOR
    def update(self):
        if self.size + self.GROWTH >= self.MAX_SIZE:
            self.grow=False
        if self.grow:
            self.size += self.GROWTH
        else:
            self.size-=self.GROWTH
    
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x,self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x,self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x,self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x,self.y), self.size * 0.4)

    def collide(self,x,y):
        dis = math.sqrt((x-self.x)**2 + (y-self.y)**2)
        return dis<=self.size


def draw(win, targets):
    win.fill(BG_VALUE)
    for target in targets:
        target.draw(win)
    
    

def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs//60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"



def draw_top_bar(win, elapsed_time, target_pressed, misses):
    pygame.draw.rect(win, "grey", (0,0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}",1,"yellow")
    
    speed = round(target_pressed/elapsed_time,1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black") 

    hits_label = LABEL_FONT.render(f"Hits: {target_pressed}", 1, "black")
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")     

    win.blit(time_label, (5,5))
    win.blit(speed_label, (200,5))
    win.blit(hits_label, (400,5))
    win.blit(lives_label, (600,5))

def endscreen(win, elapsed_time, target_pressed, clicks):
    win.fill(BG_VALUE)

    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}",1,"yellow")
    
    speed = round(target_pressed/elapsed_time,1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "yellow") 

    hits_label = LABEL_FONT.render(f"Hits: {target_pressed}", 1, "yellow")

    accuracy = round(target_pressed/clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "yellow")

    win.blit(time_label, (get_middle(time_label),200))
    win.blit(speed_label, (get_middle(speed_label),250))
    win.blit(hits_label, (get_middle(hits_label),300))
    win.blit(accuracy_label, (get_middle(accuracy_label),350))

    pygame.display.update()
    run = True  
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

def get_middle(surface):
    return WIDTH/2 - surface.get_width()/2

def play_sound():
    hit.play()


def main():
    difficulty = start_screen()
    global SECOND_COLOR
    global COLOR
    SECOND_COLOR = "white"
    global TARGET_INCREMENT
    if difficulty == "Easy":
         TARGET_INCREMENT = 1000
         COLOR = "green"
    elif difficulty == "Medium":
         TARGET_INCREMENT = 750
         COLOR = "yellow"
    elif difficulty == "Hard":
         TARGET_INCREMENT = 500
         COLOR = "red"



    run = True
    targets = []
    clock = pygame.time.Clock()
    target_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

 

    while run:
        
        
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING , WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x,y, COLOR, SECOND_COLOR)
                targets.append(target)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks+=1


        for target in targets:
            target.update()
            if target.size <=0:
                targets.remove(target)
                misses+=1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                target_pressed+=1
                play_sound()
        if misses>= LIVES:
            endscreen(WIN, elapsed_time, target_pressed, misses)
            
        
        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, target_pressed, misses)
        pygame.display.update()
    
    pygame.quit()
if __name__ == '__main__':
    main()
