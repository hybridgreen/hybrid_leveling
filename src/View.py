'''
This file handles all the rendering of UI elements, and collecting data
'''

from appglobal import context, nav_history
from nicegui import ui
from nanoid import generate
from Model import *
import datetime

# -------------------#
#  Event Handler     #
# -------------------#
def on_submit (caller, *args):
    match caller:
        case 'create user':
            context.current_user = create_user(args[0], args[1]) #ID and Username
            ui.notify("User created!")
            save()
        case 'add activity':
            create_activity(args[0],args[1], args[2], args[3])
            ui.notify('Activity created!')
            save()
            pass
        case 'fetch user':
            context.current_user = context.users[args[0]]
            ui.notify(f"Welcome {context.current_user.name}")
        case _:
            pass
    dashboard()

def dispatch(caller):
    match caller:
        case 'back':
            previous_page = nav_history.pop()
            previous_page()


# -------------------#
#  Pages             #
# -------------------#

def page_login():
    nav_history.push(page_login)
    ui.label("Are you a new user?")
    ui.button('YES', on_click = page_new_user)
    ui.button('NO', on_click = page_fetch_user)

def page_new_user():
    nav_history.push(page_new_user)
    context.main_page.clear()
    with ui.card():
        id = "U"+generate("123456789", size=3)
        ui.label(f"Welcome, your id is {id}, please save it")
        username = ui.input(label="Enter user name", validation = {'Username max length = 10 ': lambda value: len(value)< 10})
        ui.button('Submit', on_click = lambda : on_submit('create user',id,username.value))

def page_fetch_user():
    nav_history.push(page_fetch_user)
    context.main_page.clear()
    with ui.card():
        id = ui.input(label = " Enter user ID", validation = {'User ID max length = 4': lambda value: value.startswith('U') and len(value)<5})
        ui.button('Submit', on_click = lambda : on_submit('fetch user',id.value))


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
            hours = ui.input(label ='Hours',value = 00, validation = {'Only numbers allowed': lambda value: value.isdecimal()})
            minutes = ui.input(label = 'Minutes',value = 00, validation = {'Only numbers allowed': lambda value: value.isdecimal()})
            duration = hours.value * 60 + minutes.value
        with ui.row().style('width: 100%'):
            rpe = ui.slider(min = 1, max = 10, value = 2)
            ui.label().bind_text_from(rpe, 'value')
        with ui.row():
            ui.button('Submit', on_click = lambda : [on_submit('add activity',type.value ,duration, rpe.value,  timestamp)])
    

def page_activities():
    nav_history.push(page_activities)
    for activity in context.current_user.activities:
        with ui.card() as activity_card:
            with ui.row():
                ui.label(f'Activity Type:{activity.type}')
                ui.label(f'Date:{activity.timestamp}')
        with ui.row():
            ui.label(f'Activity Duration: {activity.duration}')
        with ui.row():
            ui.label(f'Perceived Effort: {activity.rpe}')
    pass

def dashboard():
    nav_history.push(dashboard)
    context.main_page.clear()
    with context.main_page:
        ui.button('Add Workout', on_click = lambda: page_add_workout())
        ui.button('View Activities', on_click = lambda: page_activities())
    pass
