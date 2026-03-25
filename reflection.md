# PawPal+ Project Reflection

## 1. System Design

**Core Actions:**
1. **Add and Manage Pets:** Users can create profiles for multiple pets, storing their names and species.
2. **Schedule and Track Tasks:** Users can add specific care tasks (like walks or feeding) with set times, priorities, and frequencies, and mark them as complete.
3. **Generate Daily Schedule:** The system can compile all tasks across all pets into a sorted, chronological daily plan with conflict detection.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I designed a system with four main classes: `Owner`, `Pet`, `Task`, and `Scheduler`. 
- **Owner**: Manages a collection of pets.
- **Pet**: Holds name, species, and its specific list of tasks.
- **Task**: Represents a single care action with attributes like description, time, duration, priority, frequency, and status.
- **Scheduler**: Acts as the logic layer to aggregate tasks from an owner's pets, sort them chronologically, filter by attributes, and identify conflicts.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
