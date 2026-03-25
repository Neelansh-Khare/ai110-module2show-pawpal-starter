import pytest
from pawpal_system import Task, Pet, Owner, Scheduler

def test_task_completion():
    task = Task(description="Walk Buddy", time="08:00", duration=30, priority="High", frequency="Daily")
    assert not task.is_completed
    task.mark_complete()
    assert task.is_completed

def test_task_addition():
    pet = Pet(name="Buddy", species="Dog")
    task = Task(description="Walk Buddy", time="08:00", duration=30, priority="High", frequency="Daily")
    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1
    assert pet.tasks[0].description == "Walk Buddy"
    assert pet.tasks[0].pet_name == "Buddy"

def test_scheduler_get_all_tasks():
    owner = Owner(name="John")
    pet1 = Pet(name="Buddy", species="Dog")
    pet2 = Pet(name="Luna", species="Cat")
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    
    pet1.add_task(Task(description="Walk Buddy", time="08:00", duration=30, priority="High", frequency="Daily"))
    pet2.add_task(Task(description="Feed Luna", time="08:00", duration=10, priority="High", frequency="Daily"))
    
    scheduler = Scheduler()
    all_tasks = scheduler.get_all_tasks(owner)
    assert len(all_tasks) == 2

def test_scheduler_sorting():
    scheduler = Scheduler()
    tasks = [
        Task(description="Late Task", time="18:00", duration=10, priority="Low", frequency="Once"),
        Task(description="Early Task", time="07:00", duration=10, priority="High", frequency="Daily"),
        Task(description="Mid Task", time="12:00", duration=10, priority="Medium", frequency="Once")
    ]
    sorted_tasks = scheduler.sort_by_time(tasks)
    assert sorted_tasks[0].time == "07:00"
    assert sorted_tasks[1].time == "12:00"
    assert sorted_tasks[2].time == "18:00"

def test_scheduler_conflicts():
    scheduler = Scheduler()
    tasks = [
        Task(description="Task 1", time="08:00", duration=10, priority="High", frequency="Daily", pet_name="Buddy"),
        Task(description="Task 2", time="08:00", duration=10, priority="High", frequency="Daily", pet_name="Luna")
    ]
    warnings = scheduler.check_conflicts(tasks)
    assert len(warnings) == 1
    assert "Conflict at 08:00" in warnings[0]
