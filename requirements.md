# 🕹️ Jumping Ball Game – Requirements Specification

## 🎯 Overview

A vertical-scrolling jumping game where the player controls a ball that jumps on platforms (bars) to reach the top of a map. The player must avoid hazards and can shoot objects for rewards. The game features multiple maps, each with unique settings and colors.

---

## 🎮 Core Gameplay

- The player controls a **ball** that:
  - Moves left and right.
  - Jumps automatically when landing on a platform.
  - Can perform a **manual high jump** by pressing the **Up** key (or assigned key).
  - Can **shoot** to hit floating objects.

- The camera scrolls **upward** with the player (similar to *Doodle Jump*).

- The goal of each map is to **reach the top height**.

- **Game Over** occurs when:
  - The player falls off the bottom of the screen.
  - The player lands on a **red bar**.
  - The player touches a **black hole**.

---

## ⚙️ Player Mechanics

- **Movement**: Left/Right with assigned keys.
- **Automatic Jumping**: Player bounces upon landing on platforms.
- **Manual Jump**: Triggered by pressing the UP key (or remapped control).
- **Shooting**:
  - Player can shoot **floating balls** with a visible hit counter.
  - Once a ball’s counter reaches 0, it grants a **reward**:
    - Extra score
    - Boosted jump

- **Gravity**: Realistic but customizable per map.

---

## 🪵 Platforms (Bars)

### Types of Platforms:
- **Stable Platforms**: Do not move.
- **Moving Platforms**: Move left/right continuously.
- **Disappearing Platforms**:
  - Can be jumped on a limited number of times (e.g., 2).
  - Have a **visible counter** showing remaining jumps.
- **Dangerous Platforms (Red Bars)**: Cause instant game over on contact.

---

## 🗺️ Maps

- **Total Maps**: 4
- Each map includes:
  - A unique **color theme** (same palette, different variations).
  - A fixed **target height** (top) to reach.
  - Custom **gravity** and **platform movement speed**.
  - Its own **Settings** button to adjust map-specific parameters.

---

## 🧭 Game Structure

### Main Menu:
- **Play** – Choose from the 4 available maps.
- **How to Play** – Instructions on gameplay mechanics, controls, and platform types.
- **Settings** – Global settings for audio and controls.

### In-Game HUD:
- **Score counter**
- **Floating object hit counters**
- **Jump counters on disappearing platforms**

---

## ⚙️ Settings

### Global Settings:
- **Sound**: On / Off
- **Music**: On / Off
- **Controls**: Remappable keys for:
  - Move Left
  - Move Right
  - Shoot
  - Manual Jump

### Per-Map Settings:
- **Gravity**
- **Platform speed**

---

## 🔊 Audio

- Simple sound effects:
  - Jump
  - Shoot
  - Land
  - Game over
  - Reward received

- Background music (toggleable)

---

## 🧱 Art & Assets

- **Style**: Simple 2D shapes (circles, rectangles)
- Use of color variation to theme maps
- Visual counters on objects and platforms

---

## 💾 Save & Progress

- No saving required at this stage.
- Optional future feature: save high scores or unlocked maps.

---

## ✅ Summary

The game will be a simple, engaging vertical-scroller built with Pygame, designed with clear progression, multiple maps, and easy customization. Players will enjoy skill-based jumping, object shooting, and customizable control.

