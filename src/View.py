'''
This file handles all the rendering of UI elements, and collecting data
'''

from appglobal import context, nav_history
from nicegui import ui
from nanoid import generate
from Model import *
import datetime

# -------------------#
#  Event Handlers     #
# -------------------#
def on_submit (caller, *args):
    match caller:
        case 'create user':
            context.current_user = create_user(args[0], args[1]) #ID and Username
            ui.notify("User created!")
            save()
        case 'add activity':
            if args[1] is not None and args[2] is not None:
                duration = args[1] * 60 +  args[2]
                create_activity(args[0],duration, args[3], args[4])
            else:
                ui.notify('Invalid duration')
            ui.notify('Activity created!')
            save()
            pass
        case 'fetch user':
                id = args[0]
                if id in context.users:
                    context.current_user = context.users[id]
                    ui.notify(f"Welcome {context.current_user.name}")
                else:
                    ui.notify("User id not recognised")

        case 'edit activity':
            if args[1] is not None and args[2] is not None:
                duration = args[1] * 60 +  args[2]
                edit_activity(args[0],duration, args[3], args[4], args[5])
            else:
                ui.notify('Invalid duration')
            save()

        case _:
            pass

    if context.current_user is not None:
        dashboard()
    else:
        page_login()

def dispatch(caller):
    ui.notify(caller)
    with context.main_page:
        match caller:
            case 'back':
                if nav_history.double_peek() is not None:    
                    nav_history.pop()
                    previous_page = nav_history.pop()
                    previous_page()
            case _:
                pass

# -------------------#
#  Helpers           #
# -------------------#

def validate_gap(day1, day2):
    if day1 and day2:
        gap = abs(day2 - day1)
        if gap < 2:
            ui.notify('Please ensure at least 2 days between hard and long runs.')
            return False
        else:
            return True

def format_week_for_table(workout_list):
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return {
        day: f"{workout[0]} ({int(workout[1])})"
        for day, workout in zip(days_of_week, workout_list)
    }


# -------------------#
#  Pages             #
# -------------------#

def page_login():
    nav_history.push(page_login)
    context.main_page.clear()
    with context.main_page:
        ui.label("Are you a new user?")
        ui.button('YES', on_click = page_new_user)
        ui.button('NO', on_click = page_fetch_user)

def page_new_user():
    nav_history.push(page_new_user)
    context.main_page.clear()
    with context.main_page:
        with ui.card():
            id = "U"+generate("123456789", size=3)
            ui.label(f"Welcome, your id is {id}, please save it")
            username = ui.input(label="Enter user name", validation = {'Username max length = 10 ': lambda value: len(value)< 10})
            ui.button('Submit', on_click = lambda : on_submit('create user',id,username.value))

def page_fetch_user():
    nav_history.push(page_fetch_user)
    context.main_page.clear()
    with ui.card():
        id = ui.input(label = " Enter user ID", validation = {'User ID must start with U': lambda value: value.startswith('U'),'User ID cannot be empty, max length is 4': lambda value: len(value)<5 and len(value)>0})
        ui.button('Submit', on_click = lambda : on_submit('fetch user',id.value))
    context.user_logged_in = True

def page_add_workout():
    nav_history.push(page_add_workout)
    context.main_page.clear()
    with ui.card() as activity_card:
        with ui.row():
            ui.label('Activity Type:')
        with ui.row():
            type = ui.select(['Run', 'Bike','Strength'] ,value = 'Run')
            with ui.input('Date', value = datetime.date.today()) as date:
                with ui.menu().props('no-parent-event') as menu:
                    with ui.date().bind_value(date):
                        with ui.row().classes('justify-end'):
                            ui.button('Close', on_click=menu.close).props('flat')
                with date.add_slot('append'):
                    ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
            timestamp = date.value
        with ui.row():
            ui.label('Activity Duration:')
        with ui.row():
            hours = ui.number(label ='Hours', value = 0, min = 0)
            minutes = ui.number(label = 'Minutes', value = 0, min = 0, step = 10)
        with ui.row().style('width: 100%'):
            rpe = ui.slider(min = 1, max = 10, value = 2)
            ui.label().bind_text_from(rpe, 'value')
        with ui.row():
            ui.button('Submit', on_click = lambda : [on_submit('add activity',type.value ,hours.value, minutes.value, rpe.value,  timestamp)])
    
def page_activities():

    if context.current_user is None:
            ui.notify('Please login to view this page')
            page_login()
    else:
        nav_history.push(page_activities)
        context.main_page.clear()
        with context.main_page :
            for act_id in context.current_user.activities:
                activity = context.current_user.activities[act_id]
                with ui.card():
                    with ui.row():
                        ui.label(f'Activity Type: {activity.type}')
                        ui.label(f'Date: {activity.timestamp}')
                        ui.button(icon = "edit", on_click = lambda id = act_id :page_edit_activity(id)) # Lambda remebers the variable not the value
                        ui.button(icon = "delete", on_click = lambda id = act_id: page_delete_activity(id))
                    with ui.row():
                        hours = activity.duration // 60
                        minutes =((activity.duration / 60) - hours) * 60
                        ui.label(f'Activity Duration: {hours}:{minutes:.0f}')
                    with ui.row():
                        ui.label(f'Perceived Effort: {activity.rpe}')
        pass

def page_edit_activity(act_id):
    context.main_page.clear()
    activity = context.current_user.activities[act_id]
    with context.main_page:
        with ui.card():
                with ui.row():
                    ui.label('Editing Activity:')
                    ui.button(icon = 'save', on_click = lambda : [on_submit('edit activity',type.value ,hours.value, minutes.value, rpe.value, timestamp, act_id)])
                with ui.row():
                    type = ui.select(['Run', 'Bike','Strength'] ,value = f'{activity.type}')
                    with ui.input('Date', value = activity.timestamp) as date:
                        with ui.menu().props('no-parent-event') as menu:
                            with ui.date().bind_value(date):
                                with ui.row().classes('justify-end'):
                                    ui.button('Close', on_click=menu.close).props('flat')
                        with date.add_slot('append'):
                            ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
                    timestamp = date.value
                with ui.row():
                    ui.label('Activity Duration:')
                with ui.row():
                    hours = ui.number(label ='Hours', value = activity.duration // 60, min = 0)
                    minutes = ui.number(label = 'Minutes', value = ((activity.duration / 60) - hours.value) * 60, min = 0, step = 10, precision = 0)
                with ui.row().style('width: 100%'):
                    rpe = ui.slider(min = 1, max = 10, value = activity.rpe)
                    ui.label().bind_text_from(rpe, 'value')
            
def page_delete_activity(act_id):
        with ui.dialog().props('backdrop-filter="blur(8px) brightness(40%)"') as dialog:
            with ui.row():
                ui.label('Deleting...Are you sure?').classes('text-3xl text-white')
            with ui.row():
                ui.button('Yes', on_click = lambda : [delete_activity(act_id), ui.notify('Activity deleted!'), save() ,page_activities()])
                ui.button('Cancel', on_click = dialog.close)
        dialog.open()
        pass

def page_userpref(): #incomplete
    context.main_page.clear()
    if context.current_user is None:
        ui.notify("Login first!")
        page_login()
    else:
        nav_history.push(page_userpref)
        with context.main_page:
            with ui.card():
                ui.label(f"Welcome {context.current_user.name}, your user ID is {context.current_user.id}")
                username = ui.input(label= 'Change username')
                ui.label("Training Parameters")

    pass

def page_training_split():
    context.main_page.clear()
    #if context.current_user is None:
    #    ui.notify("Login first!")
    #    page_login()
    #else:
    nav_history.push(page_training_split)

    weekdays = {
    0: 'MONDAY',
    1: 'TUESDAY',
    2: 'WEDNESDAY',
    3: 'THURSDAY',
    4: 'FRIDAY',
    5: 'SATURDAY',
    6: 'SUNDAY',
    }

    with context.main_page:
        with ui.card():
            ui.label("How many hours do you currently run?")
            current_time = ui.slider(min = 1, max = 12, value = 3).props('label')
            ui.label("How much time do you have to run?")
            budget = ui.slider(min = 1, max = 12, value = 3).props('label')
            ui.label("How many times per week can you run?")
            number_of_runs = ui.slider(min = 3, max = 7, value = 4).props('label')
            with ui.row():
                ui.label('Select Hard workout day:')
                hard_day = ui.select(weekdays, label = "Hard day", value = 2, on_change = lambda : generate_button.set_enabled(validate_gap(hard_day.value, long_day.value)))
            with ui.row():
                ui.label('Select Long run day:')    
                long_day = ui.select( weekdays, label = "Long day", value = 6 , on_change = lambda : generate_button.set_enabled(validate_gap(hard_day.value, long_day.value)) )
            generate_button = ui.button('Generate Split', on_click = lambda: [ page_training_split(), page_display_split(generate_split(current_time.value, budget.value, number_of_runs.value, hard_day = hard_day.value, long_day = long_day.value))])
            generate_button.enable()

def page_display_split(block):
       
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    columns = [{'name': day, 'label' : day, 'field': day} for day in days_of_week]
    
    rows = [format_week_for_table(week) for week in block]

    with context.main_page:
        splits = ui.table(columns = columns, rows = rows )

def dashboard():
        if context.current_user is None:
            ui.notify('Please login to view this page')
            page_login()
        else:
            nav_history.push(dashboard)
            context.main_page.clear()
            with context.main_page:
                ui.button('Add Workout', on_click = lambda: page_add_workout())
                ui.button('View Activities', on_click = lambda: page_activities())