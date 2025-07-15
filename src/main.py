from nicegui import ui
from Model import *
from View import *
from appglobal import context, nav_history


def main():
    print("Starting App")
    try: 
        load()
    except Exception as e:
        print(f"Error occured: {e}")

    print("User data loaded succesfully")

    result = ui.label().classes('mr-auto')
    with ui.row():
        with ui.button(icon='menu'):
            with ui.menu() as menu:
                ui.menu_item('Dashboard', lambda: dashboard())
                ui.menu_item('User preferences')
                ui.menu_item('Activities', lambda: page_activities())
                ui.separator()
                ui.menu_item('Close', menu.close)
        ui.button(icon = 'arrow_back', on_click = lambda: dispatch('back'))

    context.main_page = ui.column().props('full-width')

    page_login()
    ui.run()

if __name__ in {"__main__", "__mp_main__"}:
    main()