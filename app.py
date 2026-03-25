import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

DATA_FILE = "data.json"

# --- Initialize Session State ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner.load_from_json(DATA_FILE)
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

owner = st.session_state.owner
scheduler = st.session_state.scheduler

def save_changes():
    owner.save_to_json(DATA_FILE)

st.title("🐾 PawPal+ Assistant")

# Sidebar for Owner/Pet Info
with st.sidebar:
    st.header("Owner Profile")
    new_owner_name = st.text_input("Owner Name", value=owner.name)
    if new_owner_name != owner.name:
        owner.name = new_owner_name
        save_changes()

    st.divider()
    st.header("Manage Pets")
    with st.form("add_pet_form"):
        p_name = st.text_input("Pet Name")
        p_species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
        if st.form_submit_button("Add Pet"):
            if p_name:
                owner.add_pet(Pet(name=p_name, species=p_species))
                save_changes()
                st.success(f"Added {p_name}")
                st.rerun()
    
    if owner.pets:
        st.write("My Pets:")
        for pet in owner.pets:
            st.write(f"- {pet.name} ({pet.species})")

if not owner.pets:
    st.info("👈 Start by adding a pet in the sidebar!")
    st.stop()

# Main UI
col_add, col_sched = st.columns([1, 2])

with col_add:
    st.header("➕ Schedule Task")
    selected_pet_name = st.selectbox("Pet", [p.name for p in owner.pets])
    selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)

    with st.form("add_task_form"):
        task_desc = st.text_input("Task")
        task_time = st.text_input("Time (HH:MM)", value="08:00")
        task_duration = st.number_input("Duration (min)", min_value=1, value=30)
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)
        task_freq = st.selectbox("Frequency", ["Once", "Daily", "Weekly"], index=1)
        
        if st.form_submit_button("Schedule Task"):
            if task_desc and task_time:
                try:
                    datetime.strptime(task_time, "%H:%M")
                    new_task = Task(
                        description=task_desc,
                        time=task_time,
                        duration=task_duration,
                        priority=task_priority,
                        frequency=task_freq
                    )
                    selected_pet.add_task(new_task)
                    save_changes()
                    st.success("Task Added!")
                    st.rerun()
                except ValueError:
                    st.error("Invalid time format.")
            else:
                st.error("Missing description or time.")

with col_sched:
    st.header("📅 Daily Schedule")
    
    # Sorting by Priority then Time
    all_tasks = scheduler.get_all_tasks(owner)
    sorted_tasks = scheduler.sort_by_time_and_priority(all_tasks)

    if not sorted_tasks:
        st.info("No tasks scheduled.")
    else:
        warnings = scheduler.check_conflicts(sorted_tasks)
        for w in warnings:
            st.warning(f"⚠️ {w}")

        priority_colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}

        for i, task in enumerate(sorted_tasks):
            with st.container(border=True):
                c1, c2, c3 = st.columns([1, 4, 1])
                with c1:
                    st.markdown(f"### {task.time}")
                with c2:
                    p_emoji = priority_colors.get(task.priority, "")
                    st.markdown(f"**{p_emoji} {task.pet_name}**: {task.description}")
                    st.caption(f"{task.duration} mins | {task.frequency} | {task.priority} Priority")
                with c3:
                    if task.is_completed:
                        st.write("✅ Done")
                    elif st.button("Finish", key=f"finish_{i}"):
                        task.mark_complete()
                        # Handle recurrence
                        p_obj = next(p for p in owner.pets if p.name == task.pet_name)
                        scheduler.handle_recurrence(p_obj, task)
                        save_changes()
                        st.rerun()

    st.divider()
    st.subheader("Analytics & Status")
    total = len(all_tasks)
    done = len([t for t in all_tasks if t.is_completed])
    st.progress(done / total if total > 0 else 0)
    st.write(f"Completion: {done}/{total} tasks")
