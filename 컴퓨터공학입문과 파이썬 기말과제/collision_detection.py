import turtle
import math
import random

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Collision Detection by @TokyoEdtech")
wn.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

shapes = ["wizard.gif", "goblin.gif", "pacman.gif", "cherry.gif", "bar.gif", "ball.gif", "x.gif"]

for shape in shapes:
    wn.register_shape(shape)
    
class Sprite():
    
    ## 생성자: 스프라이트의 위치, 가로/세로 크기, 이미지 지정

    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    ## 스프라이트 메서드

    # 지정된 위치로 스프라이트 이동 후 도장 찍기
    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.image)
        pen.stamp()

    # 충돌 감지 방법 1: 두 스프라이트의 중심이 일치할 때 충돌 발생
    def is_overlapping_collision(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    # 충돌 감지 방법 2: 두 스프라이트 사이의 거리가 두 객체의 너비의 평균값 보다 작을 때 충돌 발생
    def is_distance_collision(self, other):
        distance = (((self.x-other.x) ** 2) + ((self.y-other.y) ** 2)) ** 0.5
        if distance < (self.width + other.width)/2.0:
            return True
        else:
            return False

    # 충돌 감지 방법 3: 각각의 스프라이트를 둘러썬 경계상자가 겹칠 때 충돌 발생
    # aabb: Axis Aligned Bounding Box
    def is_aabb_collision(self, other):
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return (x_collision and y_collision)


class Charater(Sprite):
    def __init__(self, x, y, width, height, image, jump=False):
        super().__init__(x, y, width, height, image)
        self.jump = jump
        # 새로 추가
        self.jump_distance = 0
        self.diagonal_distance = 0

    def hop(self, distance):
        if self.jump == True:
            self.jump_distance = distance
    
    # 만약 self.jump_dictance 가 0보다 클 경우 x 값이 증가하고 y의 값은 이에 따라 변화
    def hop_update_position(self):
        if self.jump_distance > 0:
            self.x += 1
            self.y += 2*math.cos((self.x + 128)*math.pi/180)
            self.jump_distance -= 1

    def diagonal(self, diagonal_distance):
        if self.jump == True:
            self.diagonal_distance = diagonal_distance

    # self.diagonal_distance 가 0 보다 클 경우 x,y 값이 각각 1씩 증가
    def diagonal_update_position(self):
        if self.diagonal_distance > 0:
            self.x += 1
            self.y += 1
            self.diagonal_distance -= 1


# 참고 출처: https://www.youtube.com/watch?v=Pbs6jQZrZA4&t=1021s
class battle:
    def __init__(self, moves):
        self.moves = moves
        self.chance = 3
        self.goblin_chance = 3
    
    def fight(self):
        # self.chance와 self.goblin_chance 가 0을 초과하고 있을 동안 반복
        while self.chance > 0 and self.goblin_chance > 0:
            print("pacman VS goblin")
            
            # 선택지와 남은 기회를 출력
            print("\n1. 가위 \n2. 바위\n3. 보자기")
            print(f"\n남은 기회: {self.chance}")

            choice = int(input("pacman은 무엇을 할까?: "))
            # goblin 은 1 ~ 3 사이의 값을 랜덤으로 선택
            goblin_choice = random.randint(1,3)
            
            # 만약 사용자가 선택지외의 숫자를 선택했을 때 처음부터 다시 시작
            if not 1 <= choice <= 3:
                print("다른 모양은 낼수 없다!")
                continue
            
            # pacman과 goblin의 선택을 출력
            print(f"\npacman은 [{self.moves[choice -1]}]를 냈다")
            print(f"goblin은 [{self.moves[goblin_choice - 1]}]를 냈다")
            
            # 가위바위보의 승패에 따라 pacman의 기회 혹은 goblin의 기회 횟수 차감
            if choice == goblin_choice:
                print("무승부!")
            elif goblin_choice == choice + 1:
                print("goblin의 승리!")
                self.chance -= 1
            elif choice == goblin_choice + 1:
                print("pacman의 승리!")
                self.goblin_chance -= 1
            elif choice + 2 == goblin_choice:
                print("pacman의 승리!")
                self.goblin_chance -= 1
            else:
                print("goblin의 승리!")
                self.chance -= 1
            
            # 기회 횟수가 0 이 되었을 때 승패를 결정하고 실행 종료
            if self.chance == 0:
                print("\n패배...")
                break
            elif self.goblin_chance == 0:
                print("\n승리!!")
                break         

wizard = Charater(-128, 200, 128, 128, "wizard.gif")
goblin = Sprite(128, 200, 108, 128, "goblin.gif")

pacman = Charater(-128, 0, 128, 128, "pacman.gif", jump=True)
cherry = Sprite(128, 0, 128, 128, "cherry.gif")

bar = Sprite(0, -400, 128, 24, "bar.gif")
ball = Sprite(0,-200, 32, 32, "ball.gif")

# 스프라이트 모음 리스트
sprites = [wizard, goblin, pacman, cherry, bar, ball]

# 고블린 이동
def move_goblin():
    goblin.x -= 64

# 팩맨 이동
def move_pacman():
    pacman.x += 30

def jump_pacman(distance=180):
    pacman.hop(distance)

def diagonal_pacman(diagonal_distance=200):
    pacman.diagonal(diagonal_distance)
    
# 야구공 이동
def move_ball():
    ball.y -= 24

# 이벤트 처리
wn.listen()
wn.onkeypress(move_goblin, "Left")  # 왼쪽 방향 화살표 입력
wn.onkeypress(move_pacman, "Right") # 오른쪽 방향 화살표 입력
wn.onkeypress(move_ball, "Down")    # 아래방향 화살표 입력
wn.onkeypress(jump_pacman, "space") # Space바 입력
wn.onkeypress(diagonal_pacman, "Up") # 위쪽방향 화살표 입력

while True:
    
    # 각 스프라이트 위치 이동 및 도장 찍기
    for sprite in sprites:
        sprite.render(pen)
        '''
        만약 sprite가 Charater의 객체라면 hop_update_position()과 diagonal_update_position()을 
        distance값과 diagonal_diatnace값 만큼 각각 반복 시행
        '''
        if isinstance(sprite, Charater):
            sprite.hop_update_position()
            sprite.diagonal_update_position()
        
    # 충돌 여부 확인
    if wizard.is_overlapping_collision(goblin):
        wizard.image = "x.gif"
        
    if pacman.is_distance_collision(cherry):
        cherry.image = "x.gif"

    # 만약 pacman과 goblin이 충돌했다면 battle_pacman을 정의하고 battle클래스의 fight 함수 실행
    if pacman.is_distance_collision(goblin):
        battle_pacman = battle(['가위','바위','보자기'])
        battle_pacman.fight()

        #만약 pacman의 기회, 또는 goblin의 기회가 0이 된다면 게임 실행 종료
        if battle_pacman.chance == 0:
            break
        if battle_pacman.goblin_chance == 0:
            break

    if bar.is_aabb_collision(ball):
        ball.image = "x.gif"
        
    wn.update() # 화면 업데이트
    pen.clear() # 스프라이트 이동흔적 삭제'''

