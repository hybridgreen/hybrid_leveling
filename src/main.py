from nicegui import ui
from Model import *
from View import *
from appglobal import context
def main():
    print("Starting App")
    try: 
        load()
    except Exception as e:
        print(f"Error occured: {e}")
        
    print("User data loaded succesfully")

    context.main_page = ui.column().props('full-width')

    with context.main_page:
        ui.label("Are you a new user?")
        ui.button('YES', on_click = page_new_user)
        ui.button('NO', on_click = fetch_user)

    ui.run()

if __name__ in {"__main__", "__mp_main__"}:
    main()