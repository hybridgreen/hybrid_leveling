'''
This file handles all the rendering of UI elements, and collecting data
'''

from appglobal import context
from nicegui import ui
from nanoid import generate
from Model import *

# -------------------#
#  Event Handler     #
# -------------------#
def on_submit (caller, *args):
    match caller:
        case 'create user':
            context.current_user = create_user(args[0], args[1]) #ID and Username
            ui.notify("User created!")
            #save()
        case 'add_workout':
            with ui.card() as activity_card:
                ui.label('Shazam')
            pass
        case _:
            pass
    dashboard()


# -------------------#
#  Pages             #
# -------------------#
def page_new_user():
    context.main_page.clear()
    with ui.card():
        id = "U"+generate("123456789", size=3)
        ui.label(f"Welcome, your id is {id}, please save it")
        username = ui.input(label="Enter user name", validation = {'Username cannot be empty': lambda value: len(value)< 20})
        name = username.value
        ui.button('Submit', on_click = lambda : on_submit('create_user',id,name))

def page_fetch_user():
    pass


def page_add_workout():
    context.main_page.clear()
    with ui.card() as activity_card:
        with ui.row():
            ui.label('Activity Type:')
        with ui.row():
            type = ui.select(['Run', 'Bike','Strength'] ,value = 'Run')
            with ui.input('Date') as date:
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
            hours = ui.input(label ='hh',value = 00, validation = {'Only numbers allowed': lambda value: value.isdecimal()})
            minutes = ui.input(label = 'mm',value = 00, validation = {'Only numbers allowed': lambda value: value.isdecimal()})
            duration = hours.value * 60 + minutes.value
        with ui.row().style('width: 100%'):
            rpe = ui.slider(min = 1, max = 10, value = 2)
            ui.label().bind_text_from(rpe, 'value')
        with ui.row():
            ui.button('Submit', on_click = lambda : [on_submit('add_workout', type, timestamp, duration,rpe), activity_card.clear()])
    

def page_display_activities():
    pass

def dashboard():
    context.main_page.clear()
    with context.main_page:
        ui.button('Add Workout', on_click = lambda: page_add_workout())
        ui.button('View Activities', on_click = lambda: page_display_activities())
    pass
