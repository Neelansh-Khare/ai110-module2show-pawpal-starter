import json
from dataclasses import dataclass, field, asdict
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
    pet_name: str = ""

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

    def save_to_json(self, filename: str):
        """Saves the owner and pets data to a JSON file."""
        data = {
            "name": self.name,
            "pets": []
        }
        for pet in self.pets:
            pet_data = {
                "name": pet.name,
                "species": pet.species,
                "tasks": [asdict(task) for task in pet.tasks]
            }
            data["pets"].append(pet_data)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load_from_json(cls, filename: str) -> 'Owner':
        """Loads the owner and pets data from a JSON file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            owner = cls(name=data["name"])
            for pet_data in data["pets"]:
                pet = Pet(name=pet_data["name"], species=pet_data["species"])
                for task_data in pet_data["tasks"]:
                    task = Task(**task_data)
                    pet.add_task(task)
                owner.add_pet(pet)
            return owner
        except (FileNotFoundError, json.JSONDecodeError):
            return cls(name="Default Owner")

class Scheduler:
    def get_all_tasks(self, owner: Owner) -> List[Task]:
        """Retrieves all tasks for all of the owner's pets."""
        all_tasks = []
        for pet in owner.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def sort_by_time_and_priority(self, tasks: List[Task]) -> List[Task]:
        """Sorts tasks by priority (High > Medium > Low) then by time."""
        priority_map = {"High": 0, "Medium": 1, "Low": 2}
        return sorted(tasks, key=lambda x: (priority_map.get(x.priority, 3), x.time))

    def filter_tasks(self, tasks: List[Task], status: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filters tasks by completion status or pet name."""
        filtered = tasks
        if status is not None:
            filtered = [t for t in filtered if t.is_completed == status]
        if pet_name:
            filtered = [t for t in filtered if t.pet_name.lower() == pet_name.lower()]
        return filtered

    def check_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detects if multiple tasks are scheduled at the same time."""
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

    def handle_recurrence(self, pet: Pet, task: Task):
        """Creates the next instance of a recurring task."""
        if not task.is_completed:
            return

        if task.frequency in ["Daily", "Weekly"]:
            new_task = Task(
                description=task.description,
                time=task.time,
                duration=task.duration,
                priority=task.priority,
                frequency=task.frequency
            )
            pet.add_task(new_task)
