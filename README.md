<p align="center">
<img width="20%" src="assets/images/icon.ico" alt="Floppy Sticks Logo">
<br/>
<br/>
< <a href="#1-description">Description</a> | <a href="#2-requirements">Requirements</a> | <a href="#3-installation">Installation</a> >
<br/>
< <a href="#4-features">Features</a> | <a href="#5-how-to-play">How to Play</a> | <a href="#6-extra">Extra</a> >
</p>

# **Floppy Sticks**

## 1. Description

Floppy Sticks is a 2D puzzler inspired by a numerical method used to integrate Newton's equations of motion.\
Despite the ***silly*** name....\
Floppy Sticks emits a rather relaxing and statisfying atmosphere as you solve each puzzle.

## 2. Requirements

* Python >= 3.10
* Pygame >= 2.0

## 3. Installation

* ```
  git clone https://github.com/Parallaxi/FloppySticks.git
  ```
* [**Itch.io** (*Coming Soon*)](https://parallaxi.itch.io "Itch.io")

## 4. Features

* Start Menu :arrow_forward:
* Tutorial :dart:
* Visual Effects :sparkles:
* Dynamic Background :cyclone:
* Notifications :bell:
* Music & Sound :musical_note:

## 5. How to play

The goal of the game is to convert all the given points into dynamic points.
There exist 3 types of points (*clickable*, *dynamic*, *static*) in the game, which are represented by differently coloured circles.

1. <img src="assets/images/points/clickable.png" alt="Clickable"> ***Clickable***
   * Initially they are static and don't move. However when clicked they turn into dynamic points.
2. <img src="assets/images/points/dynamic.png" alt="Dynamic"> ***Dynamic***
   * On conversion, they become affected by forces such as gravity and springs.
3. <img src="assets/images/points/static.png" alt="Static"> ***Static***
   * Spends most its life locked in place, the only way to convert it into a dynamic point is to knock it with a dynamic point.

## 6. Extra

If you come from a *Game Developement* background, you've probably heard of [**Euler Integration**](https://en.wikipedia.org/wiki/Euler_method "Wikipedia"). This is a numerical method often used in games. This method is by far the simplest and easiest to implement. However as time grows this method begins to become unstable resulting in the system exploding.\
This is why **Floppy Sticks** makes use of [**Verlet Integration**](https://en.wikipedia.org/wiki/Verlet_integration "Wikipedia").\
Verlet allows for less error and can be used to simulate more complex/realistic systems.

Here is a basic implementation of both integrations with no respect to delta time.

```python
# Euler Integration
def euler_integration(position, velocity, dt):
    new_velocity = velocity + acceleration * dt
    new_position = position + new_velocity * dt

    return new_position, new_velocity
```

```python
# Verlet Integration
def verlet_integration(current_position, previous_position, acceleration, dt):
    new_current_position = 2 * current_position - previous_position + acceleration * dt * dt
    new_previous_position = current_position

    return new_current_position, new_previous_position
```

This can be used to simulate surprisingly realistic behaviour.

## 7. Credits

* MUSIC CREATOR - [Context Sensitive](https://www.youtube.com/c/ContextSensitive "YouTube Channel")
* ORIGINAL IDEA - [Supernapie](https://supernapie.com "Website")

## 8. License

**Floppy Sticks** is licenced under an MIT licence.
