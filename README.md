# 🎯 3D Aim Challenge

A simple **3D Aim Training Game** made with **Python and Ursina Engine**.

The goal is simple: **shoot the targets as quickly and accurately as possible before the timer runs out!**

The game includes different difficulty levels, moving targets, combos, accuracy tracking, generated sound effects, and a local leaderboard.

---

## 🎮 Features

* 🧊 3D first-person environment
* 🎯 Aim and shoot targets
* ⚡ Reaction-time based scoring
* 🔥 Combo system
* 📊 Accuracy tracking
* 🏆 Local leaderboard
* 👤 Player name system
* 🔊 Automatically generated sound effects
* 🚶 Moving targets
* ⏱️ Different time limits
* 📈 Different difficulty levels
* 💾 Scores saved in a JSON file
* ✨ Hit effects
* 🖥️ Fullscreen support
* 🎮 First-person controller

---

## 🎚️ Difficulty Levels

The game has four difficulty levels:

| Difficulty | Time | Target Size | Target Speed | Moving Chance | Score Multiplier |
| ---------- | ---- | ----------- | ------------ | ------------- | ---------------- |
| Easy       | 60s  | Large       | Very Slow    | 10%           | 1.0x             |
| Normal     | 45s  | Medium      | Slow         | 30%           | 1.5x             |
| Hard       | 30s  | Small       | Fast         | 55%           | 2.0x             |
| Extreme    | 20s  | Very Small  | Very Fast    | 80%           | 3.0x             |

Higher difficulties give you less time and smaller/faster targets, but they also provide a higher score multiplier.

---

## 🎯 Scoring System

Your score depends on several things:

* Base score
* Reaction time
* Current combo
* Difficulty multiplier

### Reaction Bonus

The faster you hit a target, the more bonus points you receive.

### Combo

Every successful hit increases your combo.

Missing a target resets your combo to `0`.

A higher combo also gives additional points.

---

## 📊 Accuracy

Accuracy is calculated using:

```text
Accuracy = Hits / (Hits + Misses) × 100
```

For example:

```text
Hits: 40
Misses: 10

Accuracy: 80%
```

---

## 🏆 Leaderboard

The game stores the top **10 scores** in:

```text
leaderboard.json
```

Each leaderboard entry contains:

```json
{
    "name": "Player",
    "score": 1250,
    "hits": 25,
    "accuracy": 83.3,
    "difficulty": "Hard"
}
```

The leaderboard is automatically sorted by score.

---

## 🔊 Sound System

The game automatically generates simple `.wav` sound effects when they do not already exist.

The sounds are stored inside:

```text
aim_sounds/
```

Generated sounds include:

```text
shoot.wav
hit.wav
miss.wav
combo.wav
gameover.wav
```

The sounds are generated using Python's built-in:

* `wave`
* `struct`
* `math`

So you don't need to download external sound files.

---

## 🕹️ Controls

| Key          | Action            |
| ------------ | ----------------- |
| `W A S D`    | Move              |
| `Mouse`      | Look around       |
| `Left Mouse` | Shoot             |
| `ESC`        | Return to menu    |
| `F11`        | Toggle fullscreen |

---

## 🖥️ Main Menu

The main menu allows you to:

* Enter your player name
* Select difficulty
* Start the game
* View the leaderboard
* Exit the game

---

## 🎯 Targets

Targets are randomly spawned around the arena.

Each target can:

* Have a different size depending on difficulty
* Move horizontally
* Have a different movement speed
* Give different amounts of score depending on reaction time

Some targets also have a visual outer ring.

---

## ✨ Hit Effects

When you successfully hit a target, a small visual effect is created at the target's position.

The effect:

1. Starts as a small sphere
2. Expands
3. Becomes transparent
4. Disappears

---

## 🌎 3D Environment

The game contains a custom 3D arena with:

* Floor
* Ceiling
* Four walls
* Pillars
* Grid-like decoration
* Lighting
* Sky
* First-person camera

The player starts at the back of the arena and aims toward the targets.

---

## 📁 Project Structure

```text
3D-Aim-Challenge/
│
├── main.py
│
├── leaderboard.json
│
├── aim_sounds/
│   ├── shoot.wav
│   ├── hit.wav
│   ├── miss.wav
│   ├── combo.wav
│   └── gameover.wav
│
└── README.md
```

> `leaderboard.json` and the `aim_sounds` folder can be created automatically by the game.

---

## 🛠️ Requirements

You need:

* Python 3.x
* Ursina Engine

Install Ursina with:

```bash
pip install ursina
```

---

## ▶️ Run the Game

Clone or download the project, then run:

```bash
python main.py
```

The game should open automatically.

---

## 📚 Python Concepts Used

This project uses several Python concepts:

* Functions
* Classes
* Inheritance
* Dictionaries
* Lists
* Loops
* `if / elif / else`
* Global variables
* Random numbers
* File handling
* JSON
* Exception handling
* Object-oriented programming
* Mathematical calculations
* Time calculations
* Audio generation
* 3D game development

---

## 🧠 What I Learned

While making this project, I practiced:

* Creating a 3D game with Python
* Working with the Ursina Engine
* Creating first-person controls
* Detecting mouse hits
* Creating interactive targets
* Building a scoring system
* Creating combos
* Calculating accuracy
* Saving data with JSON
* Creating sound effects with Python
* Creating game menus and UI
* Managing game states
* Working with classes and objects

---

## 🚀 Possible Future Improvements

Some ideas for future versions:

* 🎯 Different target types
* 🔴 Critical hit zones
* 🏹 More advanced weapons
* 📈 Statistics screen
* 🌐 Online leaderboard
* 👥 Multiplayer aim training
* 🎨 Better graphics
* 🔊 More advanced sound effects
* 💥 More visual effects
* 🥇 Personal best tracking
* 📅 Daily challenges
* 🗺️ Multiple maps
* 🎮 Custom crosshairs
* ⚙️ Settings menu

---

## 📌 Project Information

**Project:** 3D Aim Challenge
**Language:** Python 🐍
**Engine:** Ursina
**Type:** 3D Aim Trainer
**Difficulty:** Easy → Extreme

---

## ⭐ About

This project was created as a Python game development project to practice **3D programming, game logic, UI, file handling, scoring systems, and object-oriented programming**.

> 🎯 **Aim faster. Hit more. Build your combo.**
