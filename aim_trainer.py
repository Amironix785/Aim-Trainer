
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


import random
import math
import json
import os
import wave
import struct


# =========================================================
# SETTINGS
# =========================================================

GAME_TITLE = "3D AIM CHALLENGE"
LEADERBOARD_FILE = "leaderboard.json"
SOUND_FOLDER = "aim_sounds"

WIDTH = 1536
HEIGHT = 864


# =========================================================
# APP
# =========================================================

app = Ursina()

window.title = GAME_TITLE
window.borderless = False
window.fullscreen = False
window.fps_counter.enabled = False
window.exit_button.visible = False

# Shader



# =========================================================
# DIFFICULTIES
# =========================================================

DIFFICULTIES = {
    "Easy": {
        "time": 60,
        "target_size": 1.4,
        "spawn_delay": 0.7,
        "speed": 0,
        "moving_chance": 0.10,
        "multiplier": 1.0
    },

    "Normal": {
        "time": 45,
        "target_size": 1.1,
        "spawn_delay": 0.55,
        "speed": 1.0,
        "moving_chance": 0.30,
        "multiplier": 1.5
    },

    "Hard": {
        "time": 30,
        "target_size": 0.8,
        "spawn_delay": 0.40,
        "speed": 1.8,
        "moving_chance": 0.55,
        "multiplier": 2.0
    },

    "Extreme": {
        "time": 20,
        "target_size": 0.55,
        "spawn_delay": 0.28,
        "speed": 2.7,
        "moving_chance": 0.80,
        "multiplier": 3.0
    }
}


# =========================================================
# GLOBAL VARIABLES
# =========================================================

player_name = "Player"
selected_difficulty = "Normal"

game_running = False
game_over = False

score = 0
hits = 0
misses = 0
combo = 0
best_combo = 0

time_left = 0
spawn_timer = 0
last_target_time = 0

targets = []
effects = []

leaderboard = []


# =========================================================
# LEADERBOARD
# =========================================================

def load_leaderboard():

    global leaderboard

    if not os.path.exists(LEADERBOARD_FILE):
        leaderboard = []
        return

    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
            leaderboard = json.load(file)

    except:
        leaderboard = []


def save_leaderboard():

    try:
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
            json.dump(leaderboard, file, indent=4, ensure_ascii=False)

    except Exception as e:
        print("Leaderboard save error:", e)


def add_score():

    global leaderboard

    leaderboard.append({
        "name": player_name,
        "score": score,
        "hits": hits,
        "accuracy": get_accuracy(),
        "difficulty": selected_difficulty
    })

    leaderboard.sort(
        key=lambda x: x.get("score", 0),
        reverse=True
    )

    leaderboard = leaderboard[:10]

    save_leaderboard()


def get_accuracy():

    total = hits + misses

    if total == 0:
        return 0

    return round((hits / total) * 100, 1)


# =========================================================
# SOUND
# =========================================================

def make_sound(filename, frequency, duration, volume=0.2):

    os.makedirs(SOUND_FOLDER, exist_ok=True)

    path = os.path.join(SOUND_FOLDER, filename)

    if os.path.exists(path):
        return path

    sample_rate = 44100
    samples = int(sample_rate * duration)

    with wave.open(path, "w") as wav:

        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        data = bytearray()

        for i in range(samples):

            t = i / sample_rate

            value = int(
                32767
                * volume
                * math.sin(2 * math.pi * frequency * t)
            )

            data += struct.pack("<h", value)

        wav.writeframes(data)

    return path


shoot_sound = make_sound(
    "shoot.wav",
    180,
    0.045,
    0.12
)

hit_sound = make_sound(
    "hit.wav",
    700,
    0.08,
    0.18
)

miss_sound = make_sound(
    "miss.wav",
    120,
    0.08,
    0.12
)

combo_sound = make_sound(
    "combo.wav",
    1000,
    0.12,
    0.15
)

gameover_sound = make_sound(
    "gameover.wav",
    70,
    0.35,
    0.18
)


def play_sound(path):

    try:
        Audio(
            path,
            autoplay=True,
            volume=0.5
        )
    except:
        pass


# =========================================================
# WORLD
# =========================================================

world = Entity()


# Floor
floor = Entity(
    parent=world,
    model="plane",
    scale=80,
    texture="white_cube",
    texture_scale=(80, 80),
    color=color.rgb(20, 23, 30),
    collider="box"
)


# Ceiling
ceiling = Entity(
    parent=world,
    model="plane",
    scale=80,
    rotation_x=180,
    y=15,
    color=color.rgb(15, 17, 23)
)


# Walls
wall_left = Entity(
    parent=world,
    model="cube",
    scale=(1, 15, 80),
    x=-40,
    y=7.5,
    color=color.rgb(30, 34, 45),
    collider="box"
)

wall_right = Entity(
    parent=world,
    model="cube",
    scale=(1, 15, 80),
    x=40,
    y=7.5,
    color=color.rgb(30, 34, 45),
    collider="box"
)

wall_back = Entity(
    parent=world,
    model="cube",
    scale=(80, 15, 1),
    z=40,
    y=7.5,
    color=color.rgb(30, 34, 45),
    collider="box"
)

wall_front = Entity(
    parent=world,
    model="cube",
    scale=(80, 15, 1),
    z=-40,
    y=7.5,
    color=color.rgb(30, 34, 45),
    collider="box"
)


# =========================================================
# DECORATION
# =========================================================

for x in range(-35, 36, 10):

    Entity(
        parent=world,
        model="cube",
        scale=(0.25, 10, 0.25),
        position=(x, 5, 35),
        color=color.azure
    )


for z in range(-30, 31, 10):

    Entity(
        parent=world,
        model="cube",
        scale=(0.15, 0.08, 80),
        position=(0, 0.03, z),
        color=color.rgb(40, 50, 65)
    )


# Pillars
for x in (-32, 32):

    for z in (-25, 0, 25):

        Entity(
            parent=world,
            model="cube",
            scale=(2, 12, 2),
            position=(x, 6, z),
            color=color.rgb(35, 40, 52)
        )


# =========================================================
# LIGHT
# =========================================================

try:

    sun = DirectionalLight(
        parent=world,
        y=20,
        rotation=(45, -45, 45)
    )

    sun.look_at(Vec3(0, 0, 0))

except:

    sun = None


# Sky
sky = Entity(
    parent=scene,
    model='sphere',
    scale=200,
    double_sided=True,
    color=color.rgb(35, 45, 70)
)


# =========================================================
# PLAYER
# =========================================================

player = FirstPersonController(
    position=(0, 2, -25)
)

player.speed = 7
player.gravity = 0.8
player.cursor.color = color.white


# =========================================================
# UI
# =========================================================

hud = Entity(
    parent=camera.ui,
    enabled=False
)

score_text = Text(
    parent=hud,
    text="SCORE: 0",
    x=-0.85,
    y=0.45,
    scale=1.4
)

time_text = Text(
    parent=hud,
    text="TIME: 0",
    x=-0.85,
    y=0.40,
    scale=1.4
)

combo_text = Text(
    parent=hud,
    text="COMBO: 0",
    x=0.55,
    y=0.45,
    scale=1.4
)

accuracy_text = Text(
    parent=hud,
    text="ACC: 100%",
    x=0.55,
    y=0.40,
    scale=1.2
)


# Crosshair
crosshair = Text(
    parent=camera.ui,
    text="+",
    origin=(0, 0),
    scale=1.5,
    color=color.white
)


# =========================================================
# MENU
# =========================================================

menu = Entity(
    parent=camera.ui
)

menu_background = Panel(
    parent=menu,
    scale=(0.75, 0.85),
    color=color.rgba(5, 8, 15, 240)
)


title = Text(
    parent=menu,
    text="3D AIM CHALLENGE",
    y=0.32,
    origin=(0, 0),
    scale=2
)


subtitle = Text(
    parent=menu,
    text="Test your reaction speed",
    y=0.24,
    origin=(0, 0),
    scale=1
)


name_label = Text(
    parent=menu,
    text="PLAYER NAME",
    y=0.12,
    origin=(0, 0),
    scale=1.1
)


name_input = InputField(
    parent=menu,
    default_value="Player",
    y=0.04,
    scale=(0.45, 0.07),
    origin=(0, 0)
)


difficulty_label = Text(
    parent=menu,
    text="DIFFICULTY",
    y=-0.07,
    origin=(0, 0),
    scale=1.1
)


# =========================================================
# DIFFICULTY BUTTONS
# =========================================================

difficulty_buttons = []

difficulty_names = [
    "Easy",
    "Normal",
    "Hard",
    "Extreme"
]

difficulty_x = [-0.27, -0.09, 0.09, 0.27]

for name, x in zip(difficulty_names, difficulty_x):

    button = Button(
        parent=menu,
        text=name,
        position=(x, -0.16),
        scale=(0.16, 0.07)
    )

    difficulty_buttons.append(button)


def update_difficulty_buttons():

    for i, button in enumerate(difficulty_buttons):

        if difficulty_names[i] == selected_difficulty:
            button.color = color.azure
        else:
            button.color = color.gray


update_difficulty_buttons()


# Start button
start_button = Button(
    parent=menu,
    text="START GAME",
    y=-0.29,
    scale=(0.35, 0.09),
    color=color.azure
)


leaderboard_button = Button(
    parent=menu,
    text="LEADERBOARD",
    y=-0.40,
    scale=(0.35, 0.07)
)


exit_button = Button(
    parent=menu,
    text="EXIT",
    y=-0.49,
    scale=(0.35, 0.07)
)


# =========================================================
# LEADERBOARD UI
# =========================================================

leaderboard_panel = Entity(
    parent=camera.ui,
    enabled=False
)


leaderboard_bg = Panel(
    parent=leaderboard_panel,
    scale=(0.75, 0.85),
    color=color.rgba(5, 8, 15, 245)
)


leaderboard_title = Text(
    parent=leaderboard_panel,
    text="LEADERBOARD",
    y=0.35,
    origin=(0, 0),
    scale=2
)


leaderboard_text = Text(
    parent=leaderboard_panel,
    text="",
    y=0.20,
    origin=(0, 0),
    scale=1.1
)


back_button = Button(
    parent=leaderboard_panel,
    text="BACK",
    y=-0.38,
    scale=(0.3, 0.08)
)


# =========================================================
# RESULT SCREEN
# =========================================================

result_panel = Entity(
    parent=camera.ui,
    enabled=False
)


result_bg = Panel(
    parent=result_panel,
    scale=(0.72, 0.78),
    color=color.rgba(5, 8, 15, 245)
)


result_title = Text(
    parent=result_panel,
    text="GAME OVER",
    y=0.28,
    origin=(0, 0),
    scale=2
)


result_text = Text(
    parent=result_panel,
    text="",
    y=0.05,
    origin=(0, 0),
    scale=1.15
)


replay_button = Button(
    parent=result_panel,
    text="PLAY AGAIN",
    y=-0.25,
    scale=(0.32, 0.08),
    color=color.azure
)


result_menu_button = Button(
    parent=result_panel,
    text="MAIN MENU",
    y=-0.36,
    scale=(0.32, 0.08)
)


# =========================================================
# EFFECTS
# =========================================================

def create_hit_effect(position):

    effect = Entity(
        model="sphere",
        position=position,
        scale=0.2,
        color=color.azure
    )

    effects.append({
        "entity": effect,
        "life": 0.25
    })


def update_effects(dt):

    for effect in effects[:]:

        entity = effect["entity"]

        effect["life"] -= dt

        entity.scale += Vec3(
            dt * 7,
            dt * 7,
            dt * 7
        )

        entity.alpha = max(
            0,
            effect["life"] / 0.25
        )

        if effect["life"] <= 0:

            destroy(entity)
            effects.remove(effect)


# =========================================================
# TARGET
# =========================================================

class AimTarget(Entity):

    def __init__(self):

        difficulty = DIFFICULTIES[selected_difficulty]

        size = difficulty["target_size"]

        x = random.uniform(-25, 25)
        y = random.uniform(2.5, 11)
        z = random.uniform(-5, 32)

        super().__init__(
            parent=world,
            model="sphere",
            position=(x, y, z),
            scale=size,
            color=color.red,
            collider="sphere"
        )

        self.spawn_time = time.time()

        self.moving = (
            random.random()
            < difficulty["moving_chance"]
        )

        self.direction = random.choice([
            -1,
            1
        ])

        self.move_speed = difficulty["speed"] * random.uniform(
            1.0,
            2.0
        )

        # Outer ring without torus
        self.ring = Entity(
            parent=self,
            model="sphere",
            scale=1.12,
            color=color.rgba(
                255,
                255,
                255,
                80
            )
        )

        self.ring.z = 0.02

        # Hide ring's collider
        self.ring.collider = None

    def update_target(self, dt):

        if not self.moving:
            return

        self.x += (
            self.direction
            * self.move_speed
            * dt
        )

        if self.x > 28:
            self.direction = -1

        if self.x < -28:
            self.direction = 1


# =========================================================
# SPAWN TARGET
# =========================================================

def spawn_target():

    target = AimTarget()

    targets.append(target)

    global last_target_time

    last_target_time = time.time()


# =========================================================
# DESTROY ALL TARGETS
# =========================================================

def clear_targets():

    for target in targets[:]:

        destroy(target)

    targets.clear()


# =========================================================
# SCORE
# =========================================================

def calculate_score(reaction_time):

    difficulty = DIFFICULTIES[selected_difficulty]

    base_score = 100

    reaction_bonus = max(
        0,
        int(300 - reaction_time * 100)
    )

    combo_bonus = combo * 10

    total = (
        base_score
        + reaction_bonus
        + combo_bonus
    )

    total *= difficulty["multiplier"]

    return int(total)


# =========================================================
# SHOOT
# =========================================================

def shoot():

    global score
    global hits
    global misses
    global combo
    global best_combo

    if not game_running:
        return

    play_sound(shoot_sound)

    hit_entity = mouse.hovered_entity

    target = None

    if hit_entity:

        if isinstance(hit_entity, AimTarget):
            target = hit_entity

        elif hit_entity.parent:

            if isinstance(
                hit_entity.parent,
                AimTarget
            ):
                target = hit_entity.parent

    if target and target in targets:

        reaction_time = time.time() - target.spawn_time

        points = calculate_score(
            reaction_time
        )

        score += points

        hits += 1

        combo += 1

        best_combo = max(
            best_combo,
            combo
        )

        play_sound(hit_sound)

        if combo >= 3:
            play_sound(combo_sound)

        create_hit_effect(
            target.position
        )

        destroy(target)

        targets.remove(target)

        spawn_timer = 0

    else:

        misses += 1
        combo = 0

        play_sound(miss_sound)


# =========================================================
# GAME START
# =========================================================

def start_game():

    global player_name
    global score
    global hits
    global misses
    global combo
    global best_combo
    global time_left
    global spawn_timer
    global game_running
    global game_over

    name = name_input.text.strip()

    if name == "":
        name = "Player"

    player_name = name[:16]

    score = 0
    hits = 0
    misses = 0
    combo = 0
    best_combo = 0

    time_left = DIFFICULTIES[selected_difficulty]["time"]

    spawn_timer = 0

    game_running = True
    game_over = False

    clear_targets()

    menu.enabled = False
    leaderboard_panel.enabled = False
    result_panel.enabled = False

    hud.enabled = True
    crosshair.enabled = True

    player.enabled = True

    player.position = (
        0,
        2,
        -25
    )

    mouse.locked = True

    spawn_target()
    spawn_target()


# =========================================================
# END GAME
# =========================================================

def end_game():

    global game_running
    global game_over

    game_running = False
    game_over = True

    clear_targets()

    play_sound(gameover_sound)

    add_score()

    hud.enabled = False

    result_panel.enabled = True

    mouse.locked = False

    player.enabled = False

    result_text.text = (
        f"PLAYER: {player_name}\n\n"
        f"SCORE: {score}\n"
        f"HITS: {hits}\n"
        f"MISSES: {misses}\n"
        f"ACCURACY: {get_accuracy()}%\n"
        f"BEST COMBO: {best_combo}\n\n"
        f"DIFFICULTY: {selected_difficulty}"
    )


# =========================================================
# LEADERBOARD
# =========================================================

def show_leaderboard():

    menu.enabled = False
    leaderboard_panel.enabled = True

    lines = []

    if not leaderboard:

        lines.append(
            "No scores yet!"
        )

    else:

        for i, entry in enumerate(
            leaderboard[:10],
            start=1
        ):

            name = entry.get(
                "name",
                "Player"
            )

            player_score = entry.get(
                "score",
                0
            )

            difficulty = entry.get(
                "difficulty",
                "Normal"
            )

            accuracy = entry.get(
                "accuracy",
                0
            )

            lines.append(
                f"{i}. {name:<16} "
                f"{player_score:>6}   "
                f"{difficulty:<8}   "
                f"{accuracy}%"
            )

    leaderboard_text.text = "\n".join(lines)


def hide_leaderboard():

    leaderboard_panel.enabled = False
    menu.enabled = True


# =========================================================
# RETURN TO MENU
# =========================================================

def main_menu():

    global game_running
    global game_over

    game_running = False
    game_over = False

    clear_targets()

    result_panel.enabled = False
    leaderboard_panel.enabled = False
    hud.enabled = False

    menu.enabled = True

    player.enabled = False

    mouse.locked = False


# =========================================================
# INPUT
# =========================================================

def input(key):

    global selected_difficulty
    global game_running

    if key == "left mouse down":

        if game_running:
            shoot()

    if key == "escape":

        if game_running:

            game_running = False
            mouse.locked = False

            hud.enabled = False
            player.enabled = False

            menu.enabled = True

            clear_targets()

    if key == "f11":

        window.fullscreen = not window.fullscreen
        return

    # Difficulty
    for i, button in enumerate(difficulty_buttons):

        if key == "left mouse down" and mouse.hovered_entity == button:

            selected_difficulty = difficulty_names[i]

            update_difficulty_buttons()

    # Difficulty
    for i, button in enumerate(difficulty_buttons):

        if key == "left mouse down" and mouse.hovered_entity == button:

            selected_difficulty = difficulty_names[i]

            update_difficulty_buttons()


# =========================================================
# BUTTON EVENTS
# =========================================================

start_button.on_click = start_game

leaderboard_button.on_click = show_leaderboard

back_button.on_click = hide_leaderboard

replay_button.on_click = start_game

result_menu_button.on_click = main_menu

exit_button.on_click = application.quit


# =========================================================
# UPDATE
# =========================================================

def update():

    global time_left
    global spawn_timer

    dt = time.dt

    update_effects(dt)

    if not game_running:
        return

    # Timer
    time_left -= dt

    if time_left <= 0:

        time_left = 0
        end_game()
        return

    # Spawn
    difficulty = DIFFICULTIES[selected_difficulty]

    spawn_timer += dt

    if spawn_timer >= difficulty["spawn_delay"]:

        spawn_timer = 0

        if len(targets) < 5:

            spawn_target()

    # Move targets
    for target in targets[:]:

        if target in targets:

            target.update_target(dt)

    # HUD
    score_text.text = f"SCORE: {score}"

    time_text.text = (
        f"TIME: {max(0, int(time_left))}"
    )

    combo_text.text = (
        f"COMBO: {combo}"
    )

    accuracy_text.text = (
        f"ACC: {get_accuracy()}%"
    )


# =========================================================
# INITIAL STATE
# =========================================================

load_leaderboard()

hud.enabled = False
crosshair.enabled = False
player.enabled = False

menu.enabled = True

mouse.locked = False


# =========================================================
# RUN
# =========================================================

app.run()