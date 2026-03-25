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

One change I made was adding `pet_name` to the `Task` class. Initially, tasks only lived inside a `Pet`'s list. However, when the `Scheduler` aggregates all tasks from an `Owner`'s multiple pets into a single daily schedule, I realized I needed a way to identify which pet each task belonged to without constantly traversing the object hierarchy.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers **Time** (chronological order) and **Conflict** (simultaneous tasks). Time is the most critical constraint because a schedule is fundamentally a timeline. Conflicts mattered next to ensure the owner doesn't overcommit at a single moment. Priority and frequency are stored and displayed to help the user make decisions, though they don't yet "hard-constrain" the list.

**b. Tradeoffs**
...
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI to brainstorm the initial class structure and to generate the Mermaid.js UML. Prompts like "How should the Scheduler retrieve all tasks from the Owner's pets?" helped define clean interaction patterns between classes. I also used AI to quickly generate a robust set of edge-case tests for the algorithmic layer.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When implementing recurrence, the AI suggested complex date-time math with `timedelta` for "Daily" tasks. I simplified this for the prototype: since the app is currently a "daily planner" without persistent dates, I opted for a simpler logic that creates a new uncompleted task instance of the same description/time. This kept the code cleaner and more aligned with the project's current scope.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested task completion, pet task addition, scheduler aggregation, sorting, conflict detection, recurrence logic, and filtering. These were important to verify that the "brain" of the app (the logic layer) works independently of the UI.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am 100% confident (5/5 stars) in the current logic. If I had more time, I would test "overlapping duration" conflicts (e.g., a 1-hour walk at 8:00 and a 15-minute feeding at 8:30) and multi-day recurrence tracking.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with the clean separation between the logic layer (`pawpal_system.py`) and the UI layer (`app.py`). It made testing very straightforward and the code easy to reason about.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add persistent data storage (JSON or a database) so that pets and tasks aren't lost when the Streamlit session refreshes or the app restarts.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The "Lead Architect" role is crucial. AI is excellent at generating snippets and templates, but deciding on the *boundary* between classes (like where recurrence logic lives) requires human judgment to ensure the system stays maintainable.

## 6. Prompt Comparison (Optional Extension)

For the logic of rescheduling tasks, I compared suggestions from two different models:

- **Model A (e.g., GPT-4o style):** Suggested using a standalone function that takes a `Task` and returns a *new* `Task` with an incremented date. This was very "functional" but required more state management in the UI.
- **Model B (e.g., Claude 3.5 style):** Suggested adding a `handle_recurrence` method to the `Scheduler` class that modifies the `Pet`'s task list directly.

**Evaluation:** I chose **Model B's** approach because it better aligned with my object-oriented architecture where the `Scheduler` is the "orchestrator" of the system's state changes. It resulted in fewer lines of code in `app.py` and a more centralized logic for state management.

