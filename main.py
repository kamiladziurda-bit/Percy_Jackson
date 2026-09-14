import pygame
import os
import math
import random


# ============================================================
# PYGAME
# ============================================================

os.environ["SDL_AUDIODRIVER"] = "dsp"

pygame.init()

SZEROKOSC = 800
WYSOKOSC = 600
FPS = 60

screen = pygame.display.set_mode(
    (SZEROKOSC, WYSOKOSC)
)

pygame.display.set_caption(
    "PERCY JACKSON - The Game"
)

clock = pygame.time.Clock()


# ============================================================
# COLORS
# ============================================================

RED = (220, 40, 40)
GREEN = (40, 210, 60)
BLUE = (40, 150, 255)
GOLD = (255, 210, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (10, 20, 55)
GRAY = (120, 120, 120)
ORANGE = (255, 130, 30)
PURPLE = (170, 60, 255)


# ============================================================
# FONTS
# ============================================================

font = pygame.font.SysFont(
    "serif",
    30,
    bold=True,
    italic=True
)

font_small = pygame.font.SysFont(
    "serif",
    24,
    bold=True,
    italic=True
)

font_character = pygame.font.SysFont(
    "serif",
    30,
    bold=True,
    italic=True
)

font_medium = pygame.font.SysFont(
    "serif",
    42,
    bold=True,
    italic=True
)

font_big = pygame.font.SysFont(
    "serif",
    72,
    bold=True,
    italic=True
)

font_title = pygame.font.SysFont(
    "serif",
    64,
    bold=True,
    italic=True
)


# ============================================================
# DIRECTIONS
# ============================================================

directions = [
    "south",
    "north",
    "west",
    "east",
    "north-east",
    "north-west",
    "south-east",
    "south-west"
]


# ============================================================
# SAFE IMAGE LOADING
# ============================================================

def load_image(path, size):

    try:

        image = pygame.image.load(
            path
        ).convert_alpha()

        image = pygame.transform.scale(
            image,
            size
        )

        return image

    except Exception as e:

        print(
            "Could not load:",
            path
        )

        print(e)

        image = pygame.Surface(
            size,
            pygame.SRCALPHA
        )

        image.fill(
            (255, 0, 255, 255)
        )

        return image


# ============================================================
# LOAD IDLE ANIMATION
# ============================================================

def load_idle(folder, size):

    animations = {}

    for direction in directions:

        path = os.path.join(
            folder,
            f"{direction}.png"
        )

        animations[direction] = load_image(
            path,
            size
        )

    return animations


# ============================================================
# LOAD WALKING ANIMATION
# ============================================================

def load_walk(folder, subfolder, size):

    animations = {}

    for direction in directions:

        animations[direction] = []

        for number in range(6):

            path = os.path.join(
                folder,
                subfolder,
                direction,
                f"frame_{number:03d}.png"
            )

            image = load_image(
                path,
                size
            )

            animations[direction].append(
                image
            )

    return animations


# ============================================================
# BACKGROUNDS
# ============================================================

level1_background = load_image(
    "1000014102.png",
    (SZEROKOSC, WYSOKOSC)
)

level2_background = load_image(
    "1000014107.png",
    (SZEROKOSC, WYSOKOSC)
)


# ============================================================
# COINS
# ============================================================

COIN_SIZE = (35, 35)

coin_image = load_image(
    "1000014106.png",
    COIN_SIZE
)

coins_on_map = []

MIN_COIN_TIME = 3500
MAX_COIN_TIME = 7000

next_coin = (
    pygame.time.get_ticks()
    +
    random.randint(
        MIN_COIN_TIME,
        MAX_COIN_TIME
    )
)


# ============================================================
# COINS
# IMPORTANT:
# Coins are NOT loaded from a file.
# They reset to 0 when the program starts.
# They remain during the current run.
# ============================================================

coins = 0


def save_coins():
    # Coins are intentionally not saved to disk.
    pass


# ============================================================
# ANNABETH
# IMPORTANT:
# Annabeth unlock resets when program starts.
# ============================================================

ANNABETH_COST = 5

annabeth_unlocked = False


def save_annabeth_status():
    # Annabeth is intentionally not saved to disk.
    pass


# ============================================================
# HERO
# ============================================================

HERO_SIZE = (80, 80)


# ============================================================
# PERCY
# ============================================================

idle_percy = load_idle(
    os.path.join(
        "Idle",
        "rotations"
    ),
    HERO_SIZE
)

walk_percy = load_walk(
    "",
    "Walk",
    HERO_SIZE
)


# ============================================================
# ANNABETH
# ============================================================

idle_annabeth = load_idle(
    "rotationsa",
    HERO_SIZE
)

walk_annabeth = load_walk(
    "animationsa",
    "Walk",
    HERO_SIZE
)


# ============================================================
# HERO VARIABLES
# ============================================================

hero_x = 400.0
hero_y = 500.0

hero_direction = "south"

selected_character = "Percy"

hero_image = idle_percy[
    hero_direction
]

hero_frame = 0

FRAME_TIME = 100

last_hero_frame_change = (
    pygame.time.get_ticks()
)


# ============================================================
# WATER ATTACK
# ============================================================

WATER_BALL_SIZE = (40, 40)
WATER_BALL_SPEED = 520.0
WATER_ATTACK_COOLDOWN = 300

water_ball_images = {}

for direction in directions:

    path = os.path.join(
        "water_ball_attack",
        "rotations",
        f"{direction}.png"
    )

    water_ball_images[direction] = load_image(
        path,
        WATER_BALL_SIZE
    )

water_balls = []

last_water_attack = 0


# ============================================================
# TSUNAMI
# ============================================================

TSUNAMI_SIZE = (140, 140)

tsunami_images = {}

for direction in directions:

    path = os.path.join(
        "tsunami_attack",
        "rotations",
        f"{direction}.png"
    )

    tsunami_images[direction] = load_image(
        path,
        TSUNAMI_SIZE
    )

tsunamis = []

MAX_TSUNAMI_CHARGE = 3

tsunami_charge = 0


# ============================================================
# MINOTAUR
# ============================================================

MINOTAUR_SIZE = (120, 120)

idle_minotaur = {}

for direction in directions:

    path = f"{direction}m.png"

    idle_minotaur[direction] = load_image(
        path,
        MINOTAUR_SIZE
    )


walk_minotaur = load_walk(
    "",
    "Running",
    MINOTAUR_SIZE
)


# ============================================================
# LEVEL 2 BOSS
# ============================================================

idle_level2_boss = load_idle(
    "rotationsc",
    MINOTAUR_SIZE
)

walk_level2_boss = load_walk(
    "animationsc",
    "Running",
    MINOTAUR_SIZE
)


# ============================================================
# DIFFICULTY
# ============================================================

difficulties = {

    "EASY": {

        "hero_hp": 130,
        "boss_hp": 180,
        "hero_speed": 300,
        "boss_speed": 40,
        "boss_damage": 8,
        "boss_cooldown": 1300,
        "water_damage": 12,
        "tsunami_damage": 35,
        "special_damage": 18
    },

    "MEDIUM": {

        "hero_hp": 100,
        "boss_hp": 250,
        "hero_speed": 300,
        "boss_speed": 55,
        "boss_damage": 12,
        "boss_cooldown": 1000,
        "water_damage": 10,
        "tsunami_damage": 30,
        "special_damage": 25
    },

    "HARD": {

        "hero_hp": 90,
        "boss_hp": 350,
        "hero_speed": 320,
        "boss_speed": 75,
        "boss_damage": 18,
        "boss_cooldown": 750,
        "water_damage": 9,
        "tsunami_damage": 28,
        "special_damage": 35
    }
}


selected_difficulty = "MEDIUM"


# ============================================================
# CURRENT STATS
# ============================================================

MAX_HERO_HP = 100
hero_hp = MAX_HERO_HP

MAX_BOSS_HP = 250
boss_hp = MAX_BOSS_HP

HERO_SPEED = 300
BOSS_SPEED = 55

BOSS_DAMAGE = 12
BOSS_COOLDOWN = 1000

WATER_DAMAGE = 10
TSUNAMI_DAMAGE = 30
SPECIAL_DAMAGE = 25


# ============================================================
# KNOCKBACK
# ============================================================

NORMAL_KNOCKBACK = 180
TSUNAMI_KNOCKBACK = 300
BOSS_KNOCKBACK = 240

hero_knockback_x = 0.0
hero_knockback_y = 0.0

boss_knockback_x = 0.0
boss_knockback_y = 0.0


# ============================================================
# BOSS VARIABLES
# ============================================================

boss_x = 100.0
boss_y = 100.0

boss_direction = "south"

boss_image = idle_minotaur[
    boss_direction
]

boss_frame = 0

BOSS_FRAME_TIME = 100

last_boss_frame_change = (
    pygame.time.get_ticks()
)

last_boss_attack = 0


# ============================================================
# LEVEL 2 SPECIAL ATTACK
# ============================================================

special_attack_active = False

special_attack_start = 0

last_special_attack = 0

SPECIAL_ATTACK_COOLDOWN = 5500

SPECIAL_ATTACK_CHARGE_TIME = 900

SPECIAL_ATTACK_DURATION = 700

special_attack_done = False


# ============================================================
# PARTICLES
# ============================================================

particles = []


def create_particles(
    x,
    y,
    color,
    amount=12
):

    for i in range(amount):

        angle = random.uniform(
            0,
            math.pi * 2
        )

        speed = random.uniform(
            80,
            220
        )

        particles.append({

            "x": float(x),
            "y": float(y),
            "dx": math.cos(angle) * speed,
            "dy": math.sin(angle) * speed,
            "life": 0.5,
            "max_life": 0.5,
            "color": color
        })


def update_particles(dt):

    for particle in particles:

        particle["x"] += (
            particle["dx"] * dt
        )

        particle["y"] += (
            particle["dy"] * dt
        )

        particle["life"] -= dt

    particles[:] = [

        particle

        for particle in particles

        if particle["life"] > 0
    ]


def draw_particles():

    for particle in particles:

        size = max(
            2,
            int(
                7 *
                (
                    particle["life"] /
                    particle["max_life"]
                )
            )
        )

        pygame.draw.circle(
            screen,
            particle["color"],
            (
                int(particle["x"]),
                int(particle["y"])
            ),
            size
        )


# ============================================================
# DIRECTION
# ============================================================

def get_direction(dx, dy):

    if dy < 0 and dx > 0:
        return "north-east"

    if dy < 0 and dx < 0:
        return "north-west"

    if dy > 0 and dx > 0:
        return "south-east"

    if dy > 0 and dx < 0:
        return "south-west"

    if dy < 0:
        return "north"

    if dy > 0:
        return "south"

    if dx < 0:
        return "west"

    if dx > 0:
        return "east"

    return None


# ============================================================
# HEALTH BAR
# ============================================================

def draw_health_bar(
    x,
    y,
    width,
    height,
    hp,
    max_hp,
    color=GREEN
):

    pygame.draw.rect(
        screen,
        BLACK,
        (
            x - 2,
            y - 2,
            width + 4,
            height + 4
        )
    )

    percentage = max(
        0,
        min(
            1,
            hp / max_hp
        )
    )

    pygame.draw.rect(
        screen,
        color,
        (
            x,
            y,
            int(
                width * percentage
            ),
            height
        )
    )


# ============================================================
# TSUNAMI BAR
# ============================================================

def draw_tsunami_bar():

    x = 5
    y = 85

    width = 250
    height = 18

    pygame.draw.rect(
        screen,
        BLACK,
        (
            x - 2,
            y - 2,
            width + 4,
            height + 4
        )
    )

    percentage = (
        tsunami_charge /
        MAX_TSUNAMI_CHARGE
    )

    pygame.draw.rect(
        screen,
        BLUE,
        (
            x,
            y,
            int(
                width * percentage
            ),
            height
        )
    )

    text = font_small.render(
        f"TSUNAMI {tsunami_charge}/3",
        True,
        WHITE
    )

    screen.blit(
        text,
        (
            x,
            y + 20
        )
    )


# ============================================================
# COINS
# ============================================================

def create_coin():

    x = random.randint(
        40,
        SZEROKOSC - 75
    )

    y = random.randint(
        100,
        WYSOKOSC - 75
    )

    coins_on_map.append({

        "x": float(x),
        "y": float(y),
        "animation": random.uniform(
            0,
            math.pi * 2
        )
    })


def update_coins(dt):

    global next_coin

    now = pygame.time.get_ticks()

    if now >= next_coin:

        if len(coins_on_map) < 3:

            create_coin()

        next_coin = (
            now
            +
            random.randint(
                MIN_COIN_TIME,
                MAX_COIN_TIME
            )
        )

    for coin in coins_on_map:

        coin["animation"] += (
            dt * 4
        )


def draw_coins():

    for coin in coins_on_map:

        y_offset = (
            math.sin(
                coin["animation"]
            ) * 4
        )

        screen.blit(
            coin_image,
            (
                int(coin["x"]),
                int(
                    coin["y"] +
                    y_offset
                )
            )
        )


def check_coin_collection():

    global coins

    hero_rect = pygame.Rect(
        int(hero_x),
        int(hero_y),
        80,
        80
    )

    collected = []

    for coin in coins_on_map:

        coin_rect = pygame.Rect(
            int(coin["x"]),
            int(coin["y"]),
            35,
            35
        )

        if hero_rect.colliderect(
            coin_rect
        ):

            coins += 1

            create_particles(
                coin["x"] + 17,
                coin["y"] + 17,
                GOLD,
                18
            )

            collected.append(
                coin
            )

    for coin in collected:

        if coin in coins_on_map:

            coins_on_map.remove(
                coin
            )


# ============================================================
# HERO GRAPHICS
# ============================================================

def set_hero_graphic():

    global hero_image

    if selected_character == "Annabeth":

        hero_image = idle_annabeth[
            hero_direction
        ]

    else:

        hero_image = idle_percy[
            hero_direction
        ]


def get_hero_walk_animation():

    if selected_character == "Annabeth":

        return walk_annabeth

    return walk_percy


# ============================================================
# BOSS GRAPHICS
# ============================================================

def get_boss_idle():

    if level == 2:

        return idle_level2_boss[
            boss_direction
        ]

    return idle_minotaur[
        boss_direction
    ]


def get_boss_walk():

    if level == 2:

        return walk_level2_boss

    return walk_minotaur


# ============================================================
# WATER BALL
# ============================================================

def shoot_water_ball():

    global last_water_attack

    now = pygame.time.get_ticks()

    if (
        now -
        last_water_attack
        <
        WATER_ATTACK_COOLDOWN
    ):

        return

    last_water_attack = now

    dx = 0
    dy = 0

    if hero_direction == "north":
        dy = -1

    elif hero_direction == "south":
        dy = 1

    elif hero_direction == "west":
        dx = -1

    elif hero_direction == "east":
        dx = 1

    elif hero_direction == "north-east":
        dx = 1
        dy = -1

    elif hero_direction == "north-west":
        dx = -1
        dy = -1

    elif hero_direction == "south-east":
        dx = 1
        dy = 1

    elif hero_direction == "south-west":
        dx = -1
        dy = 1

    length = math.hypot(
        dx,
        dy
    )

    if length == 0:
        return

    dx /= length
    dy /= length

    water_balls.append({

        "x": hero_x + 20,
        "y": hero_y + 20,
        "dx": dx,
        "dy": dy,
        "direction": hero_direction
    })


# ============================================================
# TSUNAMI
# ============================================================

def shoot_tsunami():

    global tsunami_charge

    if (
        tsunami_charge
        <
        MAX_TSUNAMI_CHARGE
    ):

        return

    dx = 0
    dy = 0

    if hero_direction == "north":
        dy = -1

    elif hero_direction == "south":
        dy = 1

    elif hero_direction == "west":
        dx = -1

    elif hero_direction == "east":
        dx = 1

    elif hero_direction == "north-east":
        dx = 1
        dy = -1

    elif hero_direction == "north-west":
        dx = -1
        dy = -1

    elif hero_direction == "south-east":
        dx = 1
        dy = 1

    elif hero_direction == "south-west":
        dx = -1
        dy = 1

    length = math.hypot(
        dx,
        dy
    )

    if length == 0:
        return

    dx /= length
    dy /= length

    tsunamis.append({

        "x": hero_x - 30,
        "y": hero_y - 30,
        "dx": dx,
        "dy": dy,
        "direction": hero_direction,
        "hit": False
    })

    tsunami_charge = 0


# ============================================================
# DIFFICULTY STATS
# ============================================================

def set_difficulty_stats():

    global MAX_HERO_HP
    global MAX_BOSS_HP
    global HERO_SPEED
    global BOSS_SPEED
    global BOSS_DAMAGE
    global BOSS_COOLDOWN
    global WATER_DAMAGE
    global TSUNAMI_DAMAGE
    global SPECIAL_DAMAGE

    data = difficulties[
        selected_difficulty
    ]

    MAX_HERO_HP = data[
        "hero_hp"
    ]

    MAX_BOSS_HP = data[
        "boss_hp"
    ]

    HERO_SPEED = data[
        "hero_speed"
    ]

    BOSS_SPEED = data[
        "boss_speed"
    ]

    BOSS_DAMAGE = data[
        "boss_damage"
    ]

    BOSS_COOLDOWN = data[
        "boss_cooldown"
    ]

    WATER_DAMAGE = data[
        "water_damage"
    ]

    TSUNAMI_DAMAGE = data[
        "tsunami_damage"
    ]

    SPECIAL_DAMAGE = data[
        "special_damage"
    ]

    if level == 2:

        MAX_BOSS_HP = int(
            MAX_BOSS_HP * 1.65
        )

        BOSS_SPEED *= 1.35

        BOSS_DAMAGE = int(
            BOSS_DAMAGE * 1.45
        )

        BOSS_COOLDOWN = int(
            BOSS_COOLDOWN * 0.72
        )

        SPECIAL_DAMAGE = int(
            SPECIAL_DAMAGE * 1.5
        )


# ============================================================
# RESET CURRENT GAME
# ============================================================

def reset_game():

    global hero_x
    global hero_y

    global boss_x
    global boss_y

    global hero_hp
    global boss_hp

    global tsunami_charge

    global hero_direction
    global boss_direction

    global hero_image
    global boss_image

    global hero_frame
    global boss_frame

    global hero_knockback_x
    global hero_knockback_y

    global boss_knockback_x
    global boss_knockback_y

    global last_boss_attack
    global last_water_attack

    global special_attack_active
    global special_attack_start
    global last_special_attack
    global special_attack_done

    global next_coin

    global death_animation
    global death_time
    global death_victim

    set_difficulty_stats()

    hero_x = 400.0
    hero_y = 500.0

    # Boss starts inside screen
    boss_x = 100.0
    boss_y = 100.0

    hero_hp = MAX_HERO_HP
    boss_hp = MAX_BOSS_HP

    tsunami_charge = 0

    water_balls.clear()
    tsunamis.clear()
    coins_on_map.clear()
    particles.clear()

    hero_knockback_x = 0
    hero_knockback_y = 0

    boss_knockback_x = 0
    boss_knockback_y = 0

    hero_direction = "south"
    boss_direction = "south"

    hero_frame = 0
    boss_frame = 0

    set_hero_graphic()

    boss_image = get_boss_idle()

    last_boss_attack = 0
    last_water_attack = 0

    special_attack_active = False
    special_attack_start = 0

    last_special_attack = (
        pygame.time.get_ticks()
    )

    special_attack_done = False

    next_coin = (
        pygame.time.get_ticks()
        +
        random.randint(
            2000,
            5000
        )
    )

    death_animation = False
    death_time = 0
    death_victim = None


# ============================================================
# DEATH ANIMATION
# ============================================================

death_animation = False

death_time = 0

death_victim = None

death_image = None

death_x = 0

death_y = 0

game_over = False

winner = None


def start_death(victim):

    global death_animation
    global death_time
    global death_victim
    global death_image
    global death_x
    global death_y
    global winner

    if death_animation:
        return

    death_animation = True

    death_time = pygame.time.get_ticks()

    death_victim = victim

    if victim == "HERO":

        death_image = hero_image

        death_x = hero_x

        death_y = hero_y

        winner = "BOSS"

    else:

        death_image = boss_image

        death_x = boss_x

        death_y = boss_y

        winner = "HERO"


def update_death():

    global death_animation
    global game_over
    global character_selection_screen
    global winner

    if not death_animation:
        return

    now = pygame.time.get_ticks()

    elapsed = now - death_time

    if elapsed >= 1300:

        death_animation = False

        if death_victim == "HERO":

            game_over = True

        else:

            if level == 1:

                character_selection_screen = True

                game_over = False

            else:

                game_over = True

                winner = "HERO"


def draw_death():

    if not death_animation:
        return

    now = pygame.time.get_ticks()

    elapsed = now - death_time

    if elapsed < 300:

        if (elapsed // 70) % 2 == 0:
            alpha = 255
        else:
            alpha = 70

        angle = 0
        offset_y = 0

    elif elapsed < 850:

        alpha = 255

        progress = (
            elapsed - 300
        ) / 550

        angle = 90 * progress

        offset_y = (
            25 * progress
        )

    else:

        progress = (
            elapsed - 850
        ) / 450

        alpha = int(
            255 *
            (1 - progress)
        )

        angle = 90

        offset_y = 25

    image = death_image.copy()

    image.set_alpha(
        max(
            0,
            min(
                255,
                alpha
            )
        )
    )

    image = pygame.transform.rotate(
        image,
        angle
    )

    rect = image.get_rect(
        center=(
            int(death_x + 40),
            int(
                death_y +
                40 +
                offset_y
            )
        )
    )

    screen.blit(
        image,
        rect
    )


# ============================================================
# LEVEL 2 SPECIAL ATTACK
# ============================================================

def update_special_attack():

    global special_attack_active
    global special_attack_start
    global last_special_attack
    global special_attack_done
    global hero_hp
    global hero_knockback_x
    global hero_knockback_y

    if level != 2:
        return

    now = pygame.time.get_ticks()

    if (
        not special_attack_active
        and
        now -
        last_special_attack
        >=
        SPECIAL_ATTACK_COOLDOWN
    ):

        special_attack_active = True

        special_attack_start = now

        special_attack_done = False

    if not special_attack_active:
        return

    elapsed = (
        now -
        special_attack_start
    )

    if (
        elapsed >=
        SPECIAL_ATTACK_CHARGE_TIME
        and
        not special_attack_done
    ):

        special_attack_done = True

        distance = math.hypot(
            hero_x - boss_x,
            hero_y - boss_y
        )

        if distance <= 190:

            hero_hp -= SPECIAL_DAMAGE

            dx = hero_x - boss_x
            dy = hero_y - boss_y

            length = math.hypot(
                dx,
                dy
            )

            if length != 0:

                dx /= length
                dy /= length

            hero_knockback_x = dx * 400
            hero_knockback_y = dy * 400

            create_particles(
                hero_x + 40,
                hero_y + 40,
                PURPLE,
                30
            )

            if hero_hp <= 0:

                hero_hp = 0

                start_death(
                    "HERO"
                )

    if elapsed >= (
        SPECIAL_ATTACK_CHARGE_TIME
        +
        SPECIAL_ATTACK_DURATION
    ):

        special_attack_active = False

        special_attack_done = False

        last_special_attack = now


def draw_special_attack():

    if (
        level != 2
        or
        not special_attack_active
    ):
        return

    now = pygame.time.get_ticks()

    elapsed = (
        now -
        special_attack_start
    )

    if elapsed < SPECIAL_ATTACK_CHARGE_TIME:

        progress = (
            elapsed /
            SPECIAL_ATTACK_CHARGE_TIME
        )

        radius = (
            50 +
            60 * progress
        )

        pygame.draw.circle(
            screen,
            PURPLE,
            (
                int(boss_x + 60),
                int(boss_y + 60)
            ),
            int(radius),
            5
        )

    else:

        progress = (
            elapsed -
            SPECIAL_ATTACK_CHARGE_TIME
        ) / SPECIAL_ATTACK_DURATION

        radius = (
            110 +
            90 * progress
        )

        pygame.draw.circle(
            screen,
            PURPLE,
            (
                int(boss_x + 60),
                int(boss_y + 60)
            ),
            int(radius),
            8
        )


# ============================================================
# ANNABETH PURCHASE
# ============================================================

def buy_annabeth():

    global coins
    global annabeth_unlocked

    if annabeth_unlocked:

        return True

    if coins >= ANNABETH_COST:

        coins -= ANNABETH_COST

        annabeth_unlocked = True

        return True

    return False


# ============================================================
# GAME STATES
# ============================================================

running = True

start_screen = True

difficulty_screen = False

character_selection_screen = False

game_over = False

winner = None

level = 1

shop_message = ""


# ============================================================
# INITIAL GAME SETUP
# ============================================================

set_difficulty_stats()
reset_game()


# ============================================================
# MAIN LOOP
# ============================================================

while running:

    dt = clock.tick(FPS) / 1000.0

    dt = min(
        dt,
        0.05
    )


    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN:

            # =================================================
            # START SCREEN
            # =================================================

            if start_screen:

                if event.key == pygame.K_r:

                    start_screen = False

                    difficulty_screen = True


            # =================================================
            # DIFFICULTY
            # =================================================

            elif difficulty_screen:

                if event.key == pygame.K_1:

                    selected_difficulty = "EASY"

                    difficulty_screen = False

                    level = 1

                    selected_character = "Percy"

                    reset_game()

                elif event.key == pygame.K_2:

                    selected_difficulty = "MEDIUM"

                    difficulty_screen = False

                    level = 1

                    selected_character = "Percy"

                    reset_game()

                elif event.key == pygame.K_3:

                    selected_difficulty = "HARD"

                    difficulty_screen = False

                    level = 1

                    selected_character = "Percy"

                    reset_game()


            # =================================================
            # CHARACTER SELECTION AFTER LEVEL 1
            # =================================================

            elif character_selection_screen:

                if event.key == pygame.K_1:

                    selected_character = "Percy"

                    level = 2

                    character_selection_screen = False

                    shop_message = ""

                    reset_game()

                elif event.key == pygame.K_2:

                    if not annabeth_unlocked:

                        if buy_annabeth():

                            selected_character = "Annabeth"

                            level = 2

                            character_selection_screen = False

                            shop_message = ""

                            reset_game()

                        else:

                            shop_message = (
                                "You need 5 coins!"
                            )

                    else:

                        selected_character = "Annabeth"

                        level = 2

                        character_selection_screen = False

                        shop_message = ""

                        reset_game()


            # =================================================
            # GAMEPLAY
            # =================================================

            elif (
                not game_over
                and
                not death_animation
            ):

                if event.key == pygame.K_SPACE:

                    shoot_water_ball()

                if event.key == pygame.K_e:

                    shoot_tsunami()


            # =================================================
            # GAME OVER / WIN
            # =================================================

            elif game_over:

                if event.key == pygame.K_r:

                    # IMPORTANT:
                    # Coins remain after death.
                    # But Annabeth resets when starting
                    # a completely new run.

                    level = 1

                    selected_character = "Percy"

                    winner = None

                    game_over = False

                    start_screen = False

                    difficulty_screen = True

                    character_selection_screen = False

                    shop_message = ""

                    annabeth_unlocked = False

                    reset_game()


    # ========================================================
    # DEATH UPDATE
    # ========================================================

    if death_animation:

        update_death()


    # ========================================================
    # GAME UPDATE
    # ========================================================

    if (
        not start_screen
        and
        not difficulty_screen
        and
        not character_selection_screen
        and
        not game_over
        and
        not death_animation
    ):

        keys = pygame.key.get_pressed()

        hero_dx = 0
        hero_dy = 0


        # ====================================================
        # HERO MOVEMENT
        # ====================================================

        if keys[pygame.K_w]:
            hero_dy -= 1

        if keys[pygame.K_s]:
            hero_dy += 1

        if keys[pygame.K_a]:
            hero_dx -= 1

        if keys[pygame.K_d]:
            hero_dx += 1

        if keys[pygame.K_UP]:
            hero_dy -= 1

        if keys[pygame.K_DOWN]:
            hero_dy += 1

        if keys[pygame.K_LEFT]:
            hero_dx -= 1

        if keys[pygame.K_RIGHT]:
            hero_dx += 1


        moving = (
            hero_dx != 0
            or
            hero_dy != 0
        )


        if moving:

            length = math.hypot(
                hero_dx,
                hero_dy
            )

            hero_dx /= length
            hero_dy /= length

            hero_direction = get_direction(
                hero_dx,
                hero_dy
            )


        hero_x += (
            hero_dx
            *
            HERO_SPEED
            *
            dt
        )

        hero_y += (
            hero_dy
            *
            HERO_SPEED
            *
            dt
        )


        # ====================================================
        # HERO KNOCKBACK
        # ====================================================

        hero_x += (
            hero_knockback_x
            *
            dt
        )

        hero_y += (
            hero_knockback_y
            *
            dt
        )

        hero_knockback_x *= (
            0.04 ** dt
        )

        hero_knockback_y *= (
            0.04 ** dt
        )


        # ====================================================
        # HERO BOUNDARIES
        # ====================================================

        hero_x = max(
            0,
            min(
                SZEROKOSC - 80,
                hero_x
            )
        )

        hero_y = max(
            0,
            min(
                WYSOKOSC - 80,
                hero_y
            )
        )


        # ====================================================
        # HERO ANIMATION
        # ====================================================

        if moving:

            now = pygame.time.get_ticks()

            if (
                now -
                last_hero_frame_change
                >=
                FRAME_TIME
            ):

                hero_frame += 1

                if hero_frame >= 6:

                    hero_frame = 0

                last_hero_frame_change = now

            hero_animations = (
                get_hero_walk_animation()
            )

            hero_image = (
                hero_animations[
                    hero_direction
                ][
                    hero_frame
                ]
            )

        else:

            hero_frame = 0

            set_hero_graphic()


        # ====================================================
        # BOSS DISTANCE
        # ====================================================

        dx = (
            hero_x -
            boss_x
        )

        dy = (
            hero_y -
            boss_y
        )

        distance = math.hypot(
            dx,
            dy
        )


        # ====================================================
        # BOSS MOVEMENT
        # ====================================================

        if distance > 70:

            move_x = dx / distance

            move_y = dy / distance

            boss_x += (
                move_x
                *
                BOSS_SPEED
                *
                dt
            )

            boss_y += (
                move_y
                *
                BOSS_SPEED
                *
                dt
            )

            boss_x += (
                boss_knockback_x
                *
                dt
            )

            boss_y += (
                boss_knockback_y
                *
                dt
            )

            boss_knockback_x *= (
                0.02 ** dt
            )

            boss_knockback_y *= (
                0.02 ** dt
            )

            # =================================================
            # BOSS BOUNDARIES
            # =================================================

            boss_x = max(
                0,
                min(
                    SZEROKOSC - MINOTAUR_SIZE[0],
                    boss_x
                )
            )

            boss_y = max(
                0,
                min(
                    WYSOKOSC - MINOTAUR_SIZE[1],
                    boss_y
                )
            )

            new_direction = get_direction(
                move_x,
                move_y
            )

            if new_direction is not None:

                if (
                    new_direction
                    !=
                    boss_direction
                ):

                    boss_direction = (
                        new_direction
                    )

                    boss_frame = 0

                now = pygame.time.get_ticks()

                if (
                    now -
                    last_boss_frame_change
                    >=
                    BOSS_FRAME_TIME
                ):

                    boss_frame += 1

                    if boss_frame >= 6:

                        boss_frame = 0

                    last_boss_frame_change = now

                boss_animations = (
                    get_boss_walk()
                )

                boss_image = (
                    boss_animations[
                        boss_direction
                    ][
                        boss_frame
                    ]
                )

        else:

            boss_frame = 0

            boss_image = get_boss_idle()

            # Also keep boss inside screen
            boss_x = max(
                0,
                min(
                    SZEROKOSC - MINOTAUR_SIZE[0],
                    boss_x
                )
            )

            boss_y = max(
                0,
                min(
                    WYSOKOSC - MINOTAUR_SIZE[1],
                    boss_y
                )
            )


        # ====================================================
        # BOSS MELEE ATTACK
        # ====================================================

        now = pygame.time.get_ticks()

        if distance <= 80:

            if (
                now -
                last_boss_attack
                >=
                BOSS_COOLDOWN
            ):

                hero_hp -= BOSS_DAMAGE

                last_boss_attack = now

                hit_dx = (
                    hero_x -
                    boss_x
                )

                hit_dy = (
                    hero_y -
                    boss_y
                )

                hit_length = math.hypot(
                    hit_dx,
                    hit_dy
                )

                if hit_length != 0:

                    hit_dx /= hit_length

                    hit_dy /= hit_length

                hero_knockback_x = (
                    hit_dx
                    *
                    BOSS_KNOCKBACK
                )

                hero_knockback_y = (
                    hit_dy
                    *
                    BOSS_KNOCKBACK
                )

                create_particles(
                    hero_x + 40,
                    hero_y + 40,
                    RED,
                    16
                )

                if hero_hp <= 0:

                    hero_hp = 0

                    start_death(
                        "HERO"
                    )


        # ====================================================
        # LEVEL 2 SPECIAL ATTACK
        # ====================================================

        update_special_attack()


        # ====================================================
        # WATER BALL MOVEMENT
        # ====================================================

        for ball in water_balls:

            ball["x"] += (
                ball["dx"]
                *
                WATER_BALL_SPEED
                *
                dt
            )

            ball["y"] += (
                ball["dy"]
                *
                WATER_BALL_SPEED
                *
                dt
            )


        # ====================================================
        # WATER BALL COLLISION
        # ====================================================

        boss_rect = pygame.Rect(
            int(boss_x),
            int(boss_y),
            120,
            120
        )

        balls_to_remove = []

        for ball in water_balls:

            ball_rect = pygame.Rect(
                int(ball["x"]),
                int(ball["y"]),
                40,
                40
            )

            if ball_rect.colliderect(
                boss_rect
            ):

                boss_hp -= WATER_DAMAGE

                tsunami_charge += 1

                if (
                    tsunami_charge
                    >
                    MAX_TSUNAMI_CHARGE
                ):

                    tsunami_charge = (
                        MAX_TSUNAMI_CHARGE
                    )

                balls_to_remove.append(
                    ball
                )

                boss_knockback_x = (
                    ball["dx"]
                    *
                    NORMAL_KNOCKBACK
                )

                boss_knockback_y = (
                    ball["dy"]
                    *
                    NORMAL_KNOCKBACK
                )

                create_particles(
                    ball["x"] + 20,
                    ball["y"] + 20,
                    BLUE,
                    12
                )

                if boss_hp <= 0:

                    boss_hp = 0

                    start_death(
                        "BOSS"
                    )

                    break


        for ball in balls_to_remove:

            if ball in water_balls:

                water_balls.remove(
                    ball
                )


        # ====================================================
        # TSUNAMI MOVEMENT
        # ====================================================

        for wave in tsunamis:

            wave["x"] += (
                wave["dx"]
                *
                360
                *
                dt
            )

            wave["y"] += (
                wave["dy"]
                *
                360
                *
                dt
            )


        # ====================================================
        # TSUNAMI COLLISION
        # ====================================================

        waves_to_remove = []

        boss_rect = pygame.Rect(
            int(boss_x),
            int(boss_y),
            120,
            120
        )

        for wave in tsunamis:

            wave_rect = pygame.Rect(
                int(wave["x"]),
                int(wave["y"]),
                140,
                140
            )

            if wave_rect.colliderect(
                boss_rect
            ):

                if not wave["hit"]:

                    wave["hit"] = True

                    boss_hp -= TSUNAMI_DAMAGE

                    boss_knockback_x = (
                        wave["dx"]
                        *
                        TSUNAMI_KNOCKBACK
                    )

                    boss_knockback_y = (
                        wave["dy"]
                        *
                        TSUNAMI_KNOCKBACK
                    )

                    create_particles(
                        boss_x + 60,
                        boss_y + 60,
                        BLUE,
                        25
                    )

                    waves_to_remove.append(
                        wave
                    )

                    if boss_hp <= 0:

                        boss_hp = 0

                        start_death(
                            "BOSS"
                        )

                        break


        for wave in waves_to_remove:

            if wave in tsunamis:

                tsunamis.remove(
                    wave
                )


        # ====================================================
        # COINS
        # ====================================================

        update_coins(dt)

        check_coin_collection()


        # ====================================================
        # REMOVE PROJECTILES
        # ====================================================

        water_balls = [

            ball

            for ball in water_balls

            if (
                -100 < ball["x"]
                <
                SZEROKOSC + 100
                and
                -100 < ball["y"]
                <
                WYSOKOSC + 100
            )
        ]

        tsunamis = [

            wave

            for wave in tsunamis

            if (
                -200 < wave["x"]
                <
                SZEROKOSC + 200
                and
                -200 < wave["y"]
                <
                WYSOKOSC + 200
            )
        ]


        # ====================================================
        # PARTICLES
        # ====================================================

        update_particles(dt)


    # ========================================================
    # START SCREEN
    # ========================================================

    if start_screen:

        screen.fill(
            DARK_BLUE
        )

        title = font_title.render(
            "PERCY JACKSON",
            True,
            WHITE
        )

        screen.blit(
            title,
            title.get_rect(
                center=(
                    SZEROKOSC // 2,
                    100
                )
            )
        )

        subtitle = font_medium.render(
            "THE GAME",
            True,
            BLUE
        )

        screen.blit(
            subtitle,
            subtitle.get_rect(
                center=(
                    SZEROKOSC // 2,
                    165
                )
            )
        )

        text = font.render(
            "WASD / ARROWS - Move",
            True,
            WHITE
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    SZEROKOSC // 2,
                    235
                )
            )
        )

        text = font.render(
            "SPACE - Water Attack",
            True,
            BLUE
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    SZEROKOSC // 2,
                    280
                )
            )
        )

        text = font.render(
            "E - Tsunami",
            True,
            BLUE
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    SZEROKOSC // 2,
                    325
                )
            )
        )

        text = font_small.render(
            "UNLOCK ANNABETH FOR 5 COINS!",
            True,
            GOLD
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    SZEROKOSC // 2,
                    385
                )
            )
        )

        text = font_medium.render(
            "PRESS R TO START",
            True,
            GOLD
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    SZEROKOSC // 2,
                    480
                )
            )
        )


    # ========================================================
    # DIFFICULTY SCREEN
    # ========================================================

    elif difficulty_screen:

        screen.fill(
            DARK_BLUE
        )

        text = font_title.render(
            "DIFFICULTY",
            True,
            WHITE
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    SZEROKOSC // 2,
                    100
                )
            )
        )

        text = font_medium.render(
            "1 - EASY",
            True,
            GREEN
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    SZEROKOSC // 2,
                    230
                )
            )
        )

        text = font_medium.render(
            "2 - MEDIUM",
            True,
            GOLD
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    SZEROKOSC // 2,
                    310
                )
            )
        )

        text = font_medium.render(
            "3 - HARD",
            True,
            RED
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    SZEROKOSC // 2,
                    390
                )
            )
        )

        text = font.render(
            f"Coins: {coins}",
            True,
            GOLD
        )

        screen.blit(
            text,
            (
                20,
                20
            )
        )


    # ========================================================
    # CHARACTER SELECTION
    # ========================================================

    elif character_selection_screen:

        screen.fill(
            DARK_BLUE
        )

        text = font_medium.render(
            "CHOOSE YOUR CHARACTER",
            True,
            WHITE
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    SZEROKOSC // 2,
                    100
                )
            )
        )

        text = font_character.render(
            "1 - PLAY AS PERCY",
            True,
            BLUE
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    SZEROKOSC // 2,
                    230
                )
            )
        )

        if annabeth_unlocked:

            text = font_character.render(
                "2 - PLAY AS ANNABETH",
                True,
                GOLD
            )

        else:

            text = font_character.render(
                "2 - ANNABETH - 5 COINS",
                True,
                GOLD
            )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    SZEROKOSC // 2,
                    320
                )
            )
        )

        text = font.render(
            f"Coins: {coins}",
            True,
            GOLD
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    SZEROKOSC // 2,
                    420
                )
            )
        )

        text = font_small.render(
            "LEVEL 2 UNLOCKED",
            True,
            GREEN
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    SZEROKOSC // 2,
                    475
                )
            )
        )

        if shop_message != "":

            text = font_small.render(
                shop_message,
                True,
                RED
            )

            screen.blit(
                text,
                text.get_rect(
                    center=(
                        SZEROKOSC // 2,
                        535
                    )
                )
            )


    # ========================================================
    # GAME
    # ========================================================

    elif not game_over:

        if level == 1:

            screen.blit(
                level1_background,
                (0, 0)
            )

        else:

            screen.blit(
                level2_background,
                (0, 0)
            )


        # ====================================================
        # HERO
        # ====================================================

        if (
            not death_animation
            or
            death_victim != "HERO"
        ):

            screen.blit(
                hero_image,
                (
                    int(hero_x),
                    int(hero_y)
                )
            )


        # ====================================================
        # BOSS
        # ====================================================

        if (
            not death_animation
            or
            death_victim != "BOSS"
        ):

            screen.blit(
                boss_image,
                (
                    int(boss_x),
                    int(boss_y)
                )
            )


        # ====================================================
        # COINS
        # ====================================================

        draw_coins()


        # ====================================================
        # WATER BALLS
        # ====================================================

        for ball in water_balls:

            image = water_ball_images[
                ball["direction"]
            ]

            screen.blit(
                image,
                (
                    int(ball["x"]),
                    int(ball["y"])
                )
            )


        # ====================================================
        # TSUNAMIS
        # ====================================================

        for wave in tsunamis:

            image = tsunami_images[
                wave["direction"]
            ]

            screen.blit(
                image,
                (
                    int(wave["x"]),
                    int(wave["y"])
                )
            )


        # ====================================================
        # LEVEL 2 ATTACK VISUAL
        # ====================================================

        draw_special_attack()


        # ====================================================
        # DEATH ANIMATION
        # ====================================================

        if death_animation:

            draw_death()


        # ====================================================
        # PARTICLES
        # ====================================================

        draw_particles()


        # ====================================================
        # HERO HP
        # ====================================================

        draw_health_bar(
            5,
            20,
            250,
            25,
            hero_hp,
            MAX_HERO_HP
        )

        text = font_small.render(
            f"{selected_character}: "
            f"{hero_hp}/"
            f"{MAX_HERO_HP}",
            True,
            WHITE
        )

        screen.blit(
            text,
            (
                37,
                50
            )
        )


        # ====================================================
        # TSUNAMI
        # ====================================================

        draw_tsunami_bar()


        # ====================================================
        # BOSS HP
        # ====================================================

        draw_health_bar(
            SZEROKOSC - 255,
            20,
            250,
            25,
            boss_hp,
            MAX_BOSS_HP,
            RED
        )

        if level == 1:

            boss_name = "Minotaur"

        else:

            boss_name = "Level 2 Boss"

        text = font_small.render(
            f"{boss_name}: "
            f"{boss_hp}/"
            f"{MAX_BOSS_HP}",
            True,
            WHITE
        )

        screen.blit(
            text,
            (
                SZEROKOSC - 255,
                50
            )
        )


        # ====================================================
        # COINS
        # ====================================================

        text = font_small.render(
            f"Coins: {coins}",
            True,
            GOLD
        )

        screen.blit(
            text,
            (
                SZEROKOSC // 2 - 65,
                20
            )
        )


        # ====================================================
        # LEVEL
        # ====================================================

        text = font_small.render(
            f"LEVEL {level} - {selected_difficulty}",
            True,
            WHITE
        )

        screen.blit(
            text,
            (
                SZEROKOSC // 2 - 100,
                50
            )
        )


    # ========================================================
    # GAME OVER / YOU WIN
    # ========================================================

    else:

        if level == 1:

            screen.blit(
                level1_background,
                (0, 0)
            )

        else:

            screen.blit(
                level2_background,
                (0, 0)
            )

        dark_overlay = pygame.Surface(
            (
                SZEROKOSC,
                WYSOKOSC
            )
        )

        dark_overlay.set_alpha(
            190
        )

        dark_overlay.fill(
            BLACK
        )

        screen.blit(
            dark_overlay,
            (0, 0)
        )


        # ====================================================
        # FINAL WIN
        # ====================================================

        if (
            winner == "HERO"
            and
            level == 2
        ):

            text = font_big.render(
                "YOU WIN!",
                True,
                BLUE
            )

            screen.blit(
                text,
                text.get_rect(
                    center=(
                        SZEROKOSC // 2,
                        190
                    )
                )
            )

            text = font_medium.render(
                "LEVEL 2 COMPLETE",
                True,
                GREEN
            )

            screen.blit(
                text,
                text.get_rect(
                    center=(
                        SZEROKOSC // 2,
                        290
                    )
                )
            )

            text = font_small.render(
                f"Coins: {coins}",
                True,
                GOLD
            )

            screen.blit(
                text,
                text.get_rect(
                    center=(
                        SZEROKOSC // 2,
                        370
                    )
                )
            )

            text = font_medium.render(
                "PRESS R TO PLAY AGAIN",
                True,
                WHITE
            )

            screen.blit(
                text,
                text.get_rect(
                    center=(
                        SZEROKOSC // 2,
                        470
                    )
                )
            )


        # ====================================================
        # GAME OVER
        # ====================================================

        else:

            text = font_big.render(
                "GAME OVER!",
                True,
                RED
            )

            screen.blit(
                text,
                text.get_rect(
                    center=(
                        SZEROKOSC // 2,
                        190
                    )
                )
            )

            text = font_medium.render(
                f"Coins: {coins}",
                True,
                GOLD
            )

            screen.blit(
                text,
                text.get_rect(
                    center=(
                        SZEROKOSC // 2,
                        300
                    )
                )
            )

            text = font_medium.render(
                "PRESS R TO PLAY AGAIN",
                True,
                WHITE
            )

            screen.blit(
                text,
                text.get_rect(
                    center=(
                        SZEROKOSC // 2,
                        430
                    )
                )
            )


    # ========================================================
    # DISPLAY
    # ========================================================

    pygame.display.flip()


# ============================================================
# END
# ============================================================

pygame.quit()