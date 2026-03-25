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
        Task(description="Late Task", time="18:00", duration=10, priority="High", frequency="Once"),
        Task(description="Early Task", time="07:00", duration=10, priority="High", frequency="Daily"),
        Task(description="Mid Task", time="12:00", duration=10, priority="High", frequency="Once")
    ]
    sorted_tasks = scheduler.sort_by_time_and_priority(tasks)
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

def test_recurrence_logic():
    scheduler = Scheduler()
    pet = Pet(name="Buddy", species="Dog")
    task = Task(description="Daily Walk", time="09:00", duration=30, priority="High", frequency="Daily")
    pet.add_task(task)
    
    # Task 0 is the original
    assert len(pet.tasks) == 1
    pet.tasks[0].mark_complete()
    scheduler.handle_recurrence(pet, pet.tasks[0])
    
    # After handling, there should be a new one
    assert len(pet.tasks) == 2
    assert pet.tasks[1].description == "Daily Walk"
    assert not pet.tasks[1].is_completed
    assert pet.tasks[1].frequency == "Daily"

def test_filter_by_status():
    scheduler = Scheduler()
    tasks = [
        Task(description="T1", time="08:00", duration=10, priority="High", frequency="Once", is_completed=True),
        Task(description="T2", time="09:00", duration=10, priority="High", frequency="Once", is_completed=False)
    ]
    completed = scheduler.filter_tasks(tasks, status=True)
    assert len(completed) == 1
    assert completed[0].description == "T1"
    
    pending = scheduler.filter_tasks(tasks, status=False)
    assert len(pending) == 1
    assert pending[0].description == "T2"

def test_filter_by_pet():
    scheduler = Scheduler()
    tasks = [
        Task(description="T1", time="08:00", duration=10, priority="High", frequency="Once", pet_name="Buddy"),
        Task(description="T2", time="09:00", duration=10, priority="High", frequency="Once", pet_name="Luna")
    ]
    buddy_tasks = scheduler.filter_tasks(tasks, pet_name="Buddy")
    assert len(buddy_tasks) == 1
    assert buddy_tasks[0].description == "T1"

def test_priority_sorting():
    scheduler = Scheduler()
    tasks = [
        Task(description="Low-08:00", time="08:00", duration=10, priority="Low", frequency="Once"),
        Task(description="High-10:00", time="10:00", duration=10, priority="High", frequency="Once"),
        Task(description="Medium-09:00", time="09:00", duration=10, priority="Medium", frequency="Once"),
        Task(description="High-08:00", time="08:00", duration=10, priority="High", frequency="Once")
    ]
    sorted_tasks = scheduler.sort_by_time_and_priority(tasks)
    # Expected: High-08:00, High-10:00, Medium-09:00, Low-08:00
    assert sorted_tasks[0].description == "High-08:00"
    assert sorted_tasks[1].description == "High-10:00"
    assert sorted_tasks[2].description == "Medium-09:00"
    assert sorted_tasks[3].description == "Low-08:00"

def test_json_persistence(tmp_path):
    file_path = tmp_path / "test_data.json"
    owner = Owner(name="Test Owner")
    pet = Pet(name="Test Pet", species="Dog")
    task = Task(description="Test Task", time="08:00", duration=30, priority="High", frequency="Once")
    pet.add_task(task)
    owner.add_pet(pet)
    
    # Save
    owner.save_to_json(str(file_path))
    
    # Load
    new_owner = Owner.load_from_json(str(file_path))
    assert new_owner.name == "Test Owner"
    assert len(new_owner.pets) == 1
    assert new_owner.pets[0].name == "Test Pet"
    assert len(new_owner.pets[0].tasks) == 1
    assert new_owner.pets[0].tasks[0].description == "Test Task"

