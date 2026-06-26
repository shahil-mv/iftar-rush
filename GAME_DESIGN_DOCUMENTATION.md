# Iftar Rush: Office Edition

## Phase 1 Game Design Documentation

## 1. Game Overview

**Title:** Iftar Rush: Office Edition

**Genre:** Arcade / Reflex / Time-management

**Platform:** Desktop

**Current Prototype Stack:** Python + Pygame

**Core Pitch:**  
The player is an office worker trying to survive the final stretch of fasting while food keeps flying across the office. During fasting hours, touching food is a penalty. Once iftar begins, the same food becomes the source of points. The game creates tension by forcing the player to constantly switch between avoidance and collection.

## 2. High-Concept Summary

The game turns a familiar cultural moment into a fast-paced arcade challenge. Instead of a standard "catch falling items" loop, the same objects alternate between danger and reward depending on time of day. This makes the player unlearn and relearn the same behavior every few seconds.

That phase-switching rule is the main design differentiator.

## 3. Story and Narrative

### Who is the player?
The player is an office employee trying to finish the day while waiting for iftar. They are surrounded by colleagues, cravings, distractions, and the pressure of timing.

### What is the mission?
Survive the office rush, maintain control during fasting, and maximize food collection the moment iftar begins.

### What is the core conflict?
The player wants food, but can only safely collect it during the correct phase. The same impulse that causes failure during the day becomes the winning strategy at night.

### What choices matter?
- Move toward food or away from it based on current phase.
- Position early for likely item trajectories.
- Decide whether to chase low-value safe catches or wait for high-value items.
- Use the boost window aggressively or play safely.

### How does it end?
The round ends when the timer runs out or when the score drops below the failure threshold. The ending reflects how well the player balanced patience and reward timing.

## 4. Core Emotional Experience

The intended player experience is:
- Tension during fasting phase
- Relief when iftar starts
- Urgency during the short scoring window
- Humor from the office theme and recognizable food items
- Satisfaction from learning timing and movement patterns

## 5. Core Mechanics

## Main Gameplay Loop

1. Food items are thrown into the play area by office colleagues.
2. The player reads the current phase: **Fasting** or **Iftar**.
3. During **Fasting**, touching food reduces score.
4. During **Iftar**, touching food increases score.
5. The phase flips every fixed interval, forcing instant strategy change.
6. Difficulty increases over time through higher pressure and more item chaos.

## What Makes It Different?

- The same item is beneficial or harmful depending on phase.
- The player is not just reacting to objects, but also to a changing rule system.
- Cultural context gives the loop a strong identity instead of generic arcade logic.
- Office colleagues act as visible sources of gameplay pressure, which adds character.

## Current Implemented Mechanics

- Left/right movement using keyboard or mouse
- Timed phase switching between **DAY/FASTING** and **NIGHT/IFTAR**
- Multiple food items with different point values and spawn weights
- Item arcs with gravity and wall bounce
- Score gain/loss based on phase
- Temporary boost from protein powder during iftar
- Timer-based game over
- High-score tracking

## 6. System Breakdown

## Player System

- Horizontal movement only
- Strong emphasis on positioning and anticipation
- No attack or inventory system
- Readability is prioritized over complexity

## Item System

Each item has:
- A point value
- A spawn probability
- A unique visual identity
- A throw source (specific colleague)

### Current item values
- Mandhi: 500
- Biriyani: 400
- Shawaya: 300
- Kanji: 150
- Mess Meals: 100
- Protein Powder: 50 plus boost effect

## Phase System

- **Fasting/Day:** food is a penalty
- **Iftar/Night:** food is a reward
- Phase changes every 15 seconds in the prototype
- The adhan sound marks the transition into scoring mode

## Boost System

Protein powder activates a temporary score/speed advantage during iftar.  
Design-wise, this adds a short risk-reward spike and creates moments where the player shifts from careful play to aggressive collection.

## 7. Difficulty Design

## How Difficulty Evolves

Difficulty scales through:
- Longer survival expectations over the full match
- More frequent item spawns over time
- Higher mental load from rapid phase switching
- More crowded trajectories from multiple throw sources

The challenge is not only reaction speed. It is rule-switch adaptation.

## Why It Avoids Repetition

- Phase inversion changes the meaning of every item
- Spawn randomness alters each run
- Different point values create target prioritization
- Boost windows temporarily change optimal strategy

Even with a simple movement set, the player is making different decisions every few seconds.

## 8. Proposed Level Design for Presentation

The current prototype is one endless timed round. For presentation, it is stronger to describe it as a structured 5-level progression.

### Level 1: Settling In
- Introduces movement and phase switching
- Only 2 colleagues throw food
- Goal: understand that food is bad during fasting and good during iftar

### Level 2: Temptation
- Adds more food types with different values
- Introduces trajectory reading and positioning
- Goal: teach target prioritization

### Level 3: Office Chaos
- More colleagues become active
- Throw angles overlap more often
- Goal: train the player to plan movement instead of chasing every item

### Level 4: Power Window
- Introduces protein boost as a central strategy layer
- Player must decide when to commit hard to collection
- Goal: create short burst decision-making

### Level 5: Final Iftar Rush
- Fastest spawn pressure
- Shorter safe windows
- Highest point opportunity
- Goal: combine timing, restraint, and aggressive scoring into one final test

## 9. Design Balance

## Reward Structure

- High-value items create excitement
- Lower-value items fill dead space and maintain rhythm
- Boost introduces comeback potential

## Risk Structure

- Touching any item during fasting becomes a mistake
- Greedy movement can lead to chains of penalties
- Overcommitting to one high-value item can cause positional disadvantage

## Player Skill Expression

This game rewards:
- Timing awareness
- Pattern recognition
- Positioning
- Impulse control
- Fast adaptation after phase changes

## 10. Edge Cases and Failure Handling

### Player quits mid-game
- Current approach: game closes immediately
- Suggested presentation answer: score is discarded unless a save/profile system is added

### Score underflow
- Current implementation ends the run at `-2000`
- This prevents endless negative scoring spirals

### Score overflow
- Current score values are small enough for normal play
- If extended, score should be clamped or stored safely as an integer without UI overflow

### Spam clicks
- Not applicable in the current prototype because clicking is not a gameplay input
- If mouse-click interactions are added later, actions should be rate-limited

### Infinite loop exploit
- Core loop is timer-bounded at 120 seconds
- This prevents endless farming in a single match

### AI stuck state
- No AI navigation exists yet
- Colleagues are animation/throw sources rather than autonomous agents

### Item soft-locks
- Items are destroyed when they leave the screen
- Wall bounce reduces the chance of strange horizontal trapping

### Boost abuse
- Boost has a fixed duration
- Boost only activates from a specific item and only during iftar

## 11. Technical Architecture

## Current Architecture

### Main systems
- `Game` manages state, score, timing, spawning, rendering, and rules
- `Player` handles movement and bounds
- `Item` handles physics, rotation, and cleanup
- `Colleague` handles throw animations
- `ScorePopup` handles feedback on score change

### State flow
- `START`
- `PLAYING`
- `GAMEOVER`

### Important rule variables
- Total round time
- Phase duration
- Minimum score threshold
- Item weights and values
- Boost duration

## Why This Architecture Works for a Prototype

- Small and readable
- Easy to tune values quickly
- Good for demoing core loop fast
- Supports future additions like levels, UI polish, combos, or boss phases

## 12. Strengths of the Current Game

- Clear and understandable loop
- Strong cultural identity
- Good prototype scope for a student/demo project
- Fast feedback through score popups and phase transitions
- A simple mechanic with enough room for design expansion

## 13. Gaps and Improvement Opportunities

For Phase 1 presentation, mention these as planned next steps:

- Add explicit level progression instead of one endless round
- Introduce unique behavior per colleague
- Add combo scoring during iftar streaks
- Add mistakes counter or patience meter during fasting
- Add narrative framing before and after the round
- Add visual telegraphs for rare/high-value food
- Improve balancing of boost and spawn rates

## 14. Presentation Version You Can Say Out Loud

**Iftar Rush: Office Edition** is an arcade game set in an office during Ramadan. The player is trying to survive the final stretch before iftar while colleagues keep throwing food across the room. The twist is that the same food changes meaning depending on the phase. During fasting, touching food is a penalty. Once iftar starts, touching food gives points. That phase inversion is the core mechanic and the main reason the game feels different.

From a design perspective, the game is about timing, self-control, and fast rule adaptation. The player must constantly switch between avoidance and collection, which creates both tension and humor. The prototype already includes phase changes, scoring, item weights, boost mechanics, and increasing pressure. For progression, I would present it as a five-level experience where each level introduces new complexity, from basic phase understanding to full office chaos and optimized scoring.

## 15. Suggested Slide Structure

1. Title and one-line pitch
2. Story: player, mission, conflict
3. Core mechanic: fasting vs iftar phase inversion
4. Gameplay loop
5. Items and scoring system
6. Level progression across 5 levels
7. Edge cases and balancing
8. Technical architecture
9. What is already implemented
10. Next-step roadmap

## 16. Conclusion

Iftar Rush: Office Edition is a strong Phase 1 concept because it already has:
- A clear identity
- A simple but novel rule twist
- Scope that is realistic for implementation
- Enough depth to discuss mechanics, balance, progression, and architecture

For this week, the best presentation angle is not "we built a full game."  
It is "we designed a game with a clear core rule, meaningful progression, and a prototype that proves the idea works."
