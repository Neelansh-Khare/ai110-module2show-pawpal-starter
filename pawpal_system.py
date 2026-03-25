from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime, timedelta

@dataclass
class Task:
    description: str
    time: str  # Format "HH:MM"
    duration: int  # minutes
    priority: str  # "Low", "Medium", "High"
    frequency: str  # "Daily", "Weekly", "Once"
    is_completed: bool = False
    pet_name: str = "" # Added to track which pet it belongs to when aggregated

    def mark_complete(self):
        """Marks the task as completed."""
        self.is_completed = True

@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Adds a task to the pet's list."""
        task.pet_name = self.name
        self.tasks.append(task)

@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Adds a pet to the owner's list."""
        self.pets.append(pet)

class Scheduler:
    def get_all_tasks(self, owner: Owner) -> List[Task]:
        """Retrieves all tasks for all of the owner's pets."""
        all_tasks = []
        for pet in owner.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sorts tasks by their scheduled time (HH:MM)."""
        return sorted(tasks, key=lambda x: x.time)

    def filter_tasks(self, tasks: List[Task], status: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filters tasks by completion status or pet name."""
        filtered = tasks
        if status is not None:
            filtered = [t for t in filtered if t.is_completed == status]
        if pet_name:
            filtered = [t for t in filtered if t.pet_name.lower() == pet_name.lower()]
        return filtered

    def check_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detects if multiple tasks are scheduled at the same time and returns warning messages."""
        warnings = []
        time_slots: Dict[str, List[Task]] = {}
        for task in tasks:
            if task.time not in time_slots:
                time_slots[task.time] = []
            time_slots[task.time].append(task)
        
        for time, task_list in time_slots.items():
            if len(task_list) > 1:
                pet_names = ", ".join([t.pet_name for t in task_list])
                warnings.append(f"Conflict at {time}: Multiple tasks for {pet_names}.")
        return warnings
