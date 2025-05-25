import pygame
from scripts.TaxiDriver import TaxiDriver
from dqnagent import DQNAgent

class Game:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.f1 = pygame.font.Font(None, 36)
        SCREEN_HEIGHT, SCREEN_WIDTH = 1000, 1000

        self.is_running = True
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.taxi_driver = TaxiDriver()
        self.hit_box_size = SCREEN_HEIGHT // self.taxi_driver.size
        self.state = self.taxi_driver.reset()
        self.agent = DQNAgent(21, 4)
        self.episode = 0
        self.max_episodes = 1000
        self.total_time = 0
        self.total_reward = 0
        self.done = False
        

    def run(self):
        while self.is_running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                # elif event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_w:
                #         self.state, reward, done = self.taxi_driver.step(0)
                #     if event.key == pygame.K_s:
                #         self.state, reward, done = self.taxi_driver.step(1)
                #     if event.key == pygame.K_a:
                #         self.state, reward, done = self.taxi_driver.step(2)
                #     if event.key == pygame.K_d:
                #         self.state, reward, done = self.taxi_driver.step(3)
            

            action = self.agent.take_action(self.state)
            next_state, reward, self.done = self.taxi_driver.step(action)
            self.agent.remember(self.state, action, reward, next_state, self.done)
            self.state = next_state
            self.total_reward += reward
            
            # Обучение
            self.agent.train()
            
            # Обновлять целевую модель переодически
            if self.total_time % self.agent.update_target_every == 0:
                self.agent.update_target_network()

            if self.done:
                print(f"Episode: {self.episode+1}/{self.max_episodes}, Total Reward: {self.total_reward}, Epsilon: {self.agent.epsilon:.2f}")
                self.total_reward = 0
                self.episode += 1
                self.state = self.taxi_driver.reset()
                self.done = False

            

            self.display.fill((10,50,255))

            pygame.draw.rect(self.display, (0, 255, 0), (self.taxi_driver.player_pos[0] * self.hit_box_size, self.taxi_driver.player_pos[1] * self.hit_box_size, self.hit_box_size, self.hit_box_size))
            pygame.draw.rect(self.display, (255, 0, 0), (self.taxi_driver.destination_pos[0] * self.hit_box_size, self.taxi_driver.destination_pos[1] * self.hit_box_size, self.hit_box_size, self.hit_box_size))

            if not self.taxi_driver.has_passenger:
                pygame.draw.rect(self.display, (0, 122, 122), (self.taxi_driver.passenger_pos[0] * self.hit_box_size, self.taxi_driver.passenger_pos[1] * self.hit_box_size, self.hit_box_size, self.hit_box_size))
            
            for i in range(len(self.taxi_driver.pits)):
                pygame.draw.rect(self.display, (128,0,128), (self.taxi_driver.pits[i][0] * self.hit_box_size, self.taxi_driver.pits[i][1] * self.hit_box_size, self.hit_box_size, self.hit_box_size))


            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    g = Game()
    g.run()