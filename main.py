import flet as ft
from db import main_db


def main(page: ft.Page):
    page.title = 'ToDoList'
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 600
    page.window_height = 800

    task_list = ft.Column(spacing=10)

    def view_tasks(task_id, task_text, task_date):
        task_field = ft.TextField(read_only=True, value=task_text, expand=True, border=ft.InputBorder.NONE)
        
        # Текст с датой
        date_text = ft.Text(value=task_date, size=12, color=ft.Colors.GREY_500)

        def enable_edit(_):
            task_field.read_only = not task_field.read_only
            task_field.border = ft.InputBorder.OUTLINE if not task_field.read_only else ft.InputBorder.NONE
            page.update()
        
        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            task_field.border = ft.InputBorder.NONE
            page.update()

        def delete_task_ui(_):
            main_db.delete_task(task_id)
            task_list.controls.remove(row_container) # Удаляем строку из списка
            page.update()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit, icon_color=ft.Colors.BLUE)
        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task, icon_color=ft.Colors.GREEN)
        # Кнопка удаления (Красная)
        delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=delete_task_ui, icon_color=ft.Colors.RED)

        # Контейнер для одной задачи
        row_container = ft.Row([
            ft.Column([task_field, date_text], expand=True, spacing=0),
            edit_button,
            save_button,
            delete_button
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        return row_container

    def add_task_db(_):
        if task_input.value:
            task_text = task_input.value
            # Получаем ID и созданную дату из БД
            task_id, task_date = main_db.add_task(task=task_text)
            
            # Добавляем в UI
            task_list.controls.append(view_tasks(task_id, task_text, task_date))
            task_input.value = ""
            page.update()

    task_input = ft.TextField(label='Введите задачу', expand=True, on_submit=add_task_db)
    add_task_button = ft.ElevatedButton('ADD', on_click=add_task_db, icon=ft.Icons.ADD)

    page.add(
        ft.Row([task_input, add_task_button]),
        ft.Divider(),
        task_list
    )

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)