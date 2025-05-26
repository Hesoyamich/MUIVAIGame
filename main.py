import pygame
from scripts.TaxiDriver import TaxiDriver
# from dqnagent import DQNAgent
from main_meny import MainMenu
from train_menu import TrainMenu

class Game:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.f1 = pygame.font.Font(None, 36)
        SCREEN_HEIGHT, SCREEN_WIDTH = 1000, 1000

        self.is_running = True
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.games = {"Taxi Driver": {"desc": "Нейронной сети требуется забрать попутчика и отвезти его в точку прибытия.", "game_class": TaxiDriver}}
        # self.agent = DQNAgent(21, 4)
        # self.episode = 0
        # self.max_episodes = 1000
        # self.total_time = 0
        # self.total_reward = 0
        # self.done = False
        self.menu = MainMenu(self.f1)
        self.train_menu = None
        self.game_state = None
        

    def run(self):
        while self.is_running:
            mouse_press = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_press = True
                # elif event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_w:
                #         self.state, reward, done = self.taxi_driver.step(0)
                #     if event.key == pygame.K_s:
                #         self.state, reward, done = self.taxi_driver.step(1)
                #     if event.key == pygame.K_a:
                #         self.state, reward, done = self.taxi_driver.step(2)
                #     if event.key == pygame.K_d:
                #         self.state, reward, done = self.taxi_driver.step(3)
            
            mouse_pos = pygame.mouse.get_pos()

            if self.game_state == None:
                menu_event = self.menu.update(mouse_pos, mouse_press, None)
            else:
                menu_event = self.game_state.update(mouse_pos, mouse_press, None)
            if menu_event == "quit":
                self.is_running = False
            if menu_event == "start_nn":
                self.in_game = True
            if menu_event == "train_nn":
                if self.train_menu == None:
                    self.train_menu = TrainMenu(self)
                    self.game_state = self.train_menu
            if menu_event == "train_next":
                self.game_state.step = min(self.game_state.step + 1, 3)
            if menu_event == "train_back":
                self.game_state.step -= 1
                if self.game_state.step < 0:
                    self.train_menu = None
                    self.game_state = None
                

            # action = self.agent.take_action(self.state)
            # next_state, reward, self.done = self.taxi_driver.step(action)
            # self.agent.remember(self.state, action, reward, next_state, self.done)
            # self.state = next_state
            # self.total_reward += reward
            
            # # Обучение
            # self.agent.train()
            
            # # Обновлять целевую модель переодически
            # if self.total_time % self.agent.update_target_every == 0:
            #     self.agent.update_target_network()

            # if self.done:
            #     print(f"Episode: {self.episode+1}/{self.max_episodes}, Total Reward: {self.total_reward}, Epsilon: {self.agent.epsilon:.2f}")
            #     self.total_reward = 0
            #     self.episode += 1
            #     self.state = self.taxi_driver.reset()
            #     self.done = False

            

            self.display.fill((40, 40, 40))

            if self.game_state == None:
                self.menu.render(self.display)

            else:
                self.game_state.render(self.display)


            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    g = Game()
    g.run()