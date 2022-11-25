import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

FONT_STYLE = 'freesansbold.ttf'

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.score = 0
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.font = pygame.font.Font(FONT_STYLE, 22)
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit            

    def run(self):#Reinicia a partida
        #Executa o jogo
        #Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        #Toda vez que o jogo é reiniciado o score é reiniciado 
        self.score = 0
        #Toda vez que o jogo é reiniciado o game_speed volta para o valor inicial
        self.game_speed = 20
        while self.playing:
            self.events()
            self.update()
            self.draw()

       #Eventos do usuarios - quebra do loop
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

        #Atualização acontecendo constantemente
    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self.score, self.game_speed, self.player)
         
    def update_score(self):
        self.score += 1 
        if self.score % 100 == 0:
            self.game_speed += 5

        # Preenche a tela
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()
        
    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        #Move a imagem na velocidade do jogo 
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        text = self.font.render("Score: "  + str(self.score), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (1000, 50)
        self.screen.blit(text, text_rect)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            half_screen_height = SCREEN_HEIGHT // 2
            half_screen_width = SCREEN_WIDTH // 2
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
             text_exit = self.font.render(f"{self.player.type.capitalize()} enable for seconds", True, (0,0,255))
             text_rect_exit = text_exit.get_rect()
             text_rect_exit.center = (half_screen_width, half_screen_height + 160)
             self.screen.blit(text_exit, text_rect_exit)
            else:
               self.player.has_power_up = False
               self.player.type = DEFAULT_TYPE
                    

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            #Fecha jogo     
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
            #Reinicia o jogo           
            elif event.type == pygame.KEYDOWN: #Qualquer tecla
                self.run()        

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            text = self.font.render("Press any key to start", True, (0,0,0))
            text_rect = text.get_rect()
            text_rect.center = (half_screen_width, half_screen_height)
            self.screen.blit(text, text_rect)
        else:
            ##Mensagem do Score
            text = self.font.render("Your Score: " + str(self.score) , True, (0,0,0))
            text_rect = text.get_rect()
            text_rect.center = (half_screen_width, half_screen_height)
            self.screen.blit(text, text_rect)
            self.screen.blit(ICON, (half_screen_width - 40, half_screen_height - 120))
            ##Opção para continuar no jogo
            text_play = self.font.render("Click any key to play again!", True, (255,0,0))
            text_rect_play = text_play.get_rect()
            text_rect_play.center = (half_screen_width, half_screen_height + 40)
            self.screen.blit(text_play, text_rect_play)
            ##Opção para sair do jogo
            text_exit = self.font.render("Or click the mouse button to exit the game!", True, (0,0,255))
            text_rect_exit = text_exit.get_rect()
            text_rect_exit.center = (half_screen_width, half_screen_height + 80)
            self.screen.blit(text_exit, text_rect_exit)
             #"Press any key to restart"
             ## Mostrar score atingido e death_count
             # Quando reiniciar, resetar game_speed e score
             # método reutilizável para desenhar os textos   
            text_death_count = self.font.render("Death count " + str(self.death_count), True, (0,128,128))
            text_rect_death_count = text_death_count.get_rect()
            text_rect_death_count.center = (half_screen_width, half_screen_height + 120)
            self.screen.blit(text_death_count, text_rect_death_count)

        pygame.display.update()
        self.handle_events_on_menu()

        def drawText(self, sentence, width, height, text_color):
            text = self.font.render(sentence, True, text_color)
            text_rect = text.get_rect()
            text_rect.center = (half_screen_width + width, half_screen_height + height)
            self.screen.blit(text, text_rect)
