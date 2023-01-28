from pygame import *
from random import randint
from time import time as timer #импортируем вункции для засекания времени

#подгружаем отдельно функции для работы со шрифтами
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render("YOU WIN!", True, (255, 255, 255))
lose = font1.render("YOU LOSE!", True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)

#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#нам нужны такие картинки:
img_back = "galaxy.jpg" #фон игры
img_bullet = "bullet.png" #пуля
img_hero = "rocket.png" #герой
img_enemy = "ufo.png" #враг
img_ast = "asteroid.png" #астероид

score = 0 #сбито кораблей
goal = 10 #столько кораблей нужно сбить для победы
lost = 0 #пропущено кораблей
max_lost = 3 #максимальное количество пропущенных кораблей
life = 3 #очки жизни

#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#класс главного игрока
class Player(GameSprite):
    #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_width - 80:
            self.rect.y += self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    #метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

#класс спрайта-врага   
class Enemy(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

#класс спрайта-пули 
class Asteroid(GameSprite): 
    life_ast = 0

    #движение врага 
    def update(self): 
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
        bullet = sprite.spritecollideany(self, bullets)
        if bullet is not None:
            self.life_ast += 1
            bullet.kill()
            if self.life_ast >= life:
                sprite.groupcollide(asteroids, bullets, True, True)
                global score
                #этот цикл повторяется столько раз, сколько монстров подбито
                score = score + 2
                asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
                asteroids.add(asteroid)
                self.life_ast = 0
                self.kill()

#класс спрайта-пули 
class Bullet(GameSprite): 
    #движение врага 
    def update(self): 
        self.rect.y += self.speed 
        #исчезает, если дойдет до края экрана 
        if self.rect.y < 0:
            self.kill()

class Button:
    def __init__(self, position, size, text, color1, color2):
        self.img = Surface(size)
        self.img.fill(color1)
        self.rect = self.img.get_rect(center = position)
        self.img.blit(text, text.get_rect(centerx = self.img.get_width()/2, centery = self.img.get_height()/2))

    def reset(self):
        window.blit(self.img, self.rect)


#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

#создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

#создание группы спрайтов-врагов
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

#создание группы спрайтов-астероидов
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Asteroid(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

#создание группы спрайтов-пуль
bullets = sprite.Group()

#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = False #флаг сбрасывается кнопкой закрытия окна

rel_time = False #флаг, отвечающий за перезарядку

num_fire = 0 #переменная для подсчёта выстрелов

# 
button_start = Button((350, 200), (100, 50), font2.render('Начать', True, (255, 255, 255)), (100, 100, 100), (100, 100, 100))

while not run:
    button_start.reset()
    time.delay(50)


while run:
    #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        #событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #проверяем, сколько выстрелов сделно и не происходит ли перезарядка
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                
                if num_fire >= 5 and rel_time == False: #если игрок сделал 5 выстрелов
                    last_time = timer() #засекаем время, когда это проищошло
                    rel_time = True #ставим флаг перезарядки

    #сама игра: действия спрайтов, проверка правил игры, перерисовка
    if not finish:
        #обновляем фон
        window.blit(background,(0,0))

        #производим движения спрайтов
        ship.update()
        asteroids.update()
        monsters.update()
        bullets.update()

        #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        asteroids.draw(window)
        bullets.draw(window)
        monsters.draw(window)

        #перезарядка
        if rel_time == True:
            now_time = timer() #считываем время

            if now_time - last_time < 3: #пока не прошло 3 секунды выводим информацию о перезарядке
                reload = font2.render("Перезарядка ...", 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            
            else:
                num_fire = 0 #обнуляем счётчик пуль
                rel_time = False #сбрасываем флаг перезарядки

        #проверка столкновение пули и монстров (и монстр, и пуля при касании исчезает)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #этот цикл повторяется столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        #проверка столкновение пули и астероида (и астероид, и пуля при касании исчезает

        #если спрайт коснулся врага, уменьшает жизнь
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1
            score -= 1

        #проигрыш
        if life == 0 or lost >= max_lost:
            finish = True #проиграли, ставим фон и больше не управляем спрайтами
            window.blit(lose,(200,200))

        #проверка выигрыша: сколько очков набрали?
        if score >= goal:
            finish = True 
            window.blit(win,(200,200))

        #пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()

    #бонус: автоматический перезапуск игры
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)

    time.delay(50)