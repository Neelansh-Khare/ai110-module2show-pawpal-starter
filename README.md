# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Smarter Scheduling

PawPal+ includes an algorithmic layer that makes scheduling easier:
- **Chronological Sorting:** Tasks are automatically ordered by time.
- **Conflict Detection:** The system warns you if multiple tasks are scheduled for the same time.
- **Recurrence Logic:** Mark a "Daily" or "Weekly" task as done, and PawPal+ automatically schedules the next instance for you.
- **Filtering:** Filter tasks by status (Pending/Completed) or by specific pet.

## Testing PawPal+

To ensure the system is reliable, a comprehensive test suite is included.
Run the tests with:
```bash
source .venv/bin/activate
python -m pytest tests/test_pawpal.py
```

**Confidence Level:** ⭐⭐⭐⭐⭐ (5/5) - The core logic is fully covered by automated tests.
