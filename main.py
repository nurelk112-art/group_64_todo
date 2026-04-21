import flet as ft
from db import main_db


def main(page: ft.Page):
    # Настройки страницы 
    page.title = 'ToDoList'
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 600
    page.window_height = 800
    page.padding = 20

    # Переменные состояния
    filter_type = 'all'
    task_list = ft.Column(spacing=10)

    # Функции работы с данными и UI 
    def load_tasks():
        """Загружает задачи из базы данных с учетом фильтра"""
        task_list.controls.clear()
        # Извлекаем 4 значения: id, текст, дата, статус
        for task_id, task, date, completed in main_db.get_tasks(filter_type=filter_type):
            task_list.controls.append(
                view_tasks(task_id, task, date, completed)
            )
        page.update()

    def add_task_event(e):
        """Обработчик добавления новой задачи"""
        if task_input.value:
            task_text = task_input.value
            task_id, task_date = main_db.add_task(task=task_text)
            
            if filter_type != 'completed':
                task_list.controls.append(view_tasks(task_id, task_text, task_date, 0))
            
            task_input.value = ""
            page.update()

    def set_filter(filter_value):
        """Переключает текущий фильтр отображения"""
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()

    def clear_completed_tasks(e):
        """Удаляет все выполненные задачи из БД и обновляет UI"""
        main_db.delete_completed() 
        load_tasks()
        page.update()

    # Компонент одной строки задачи

    def view_tasks(task_id, task_text, task_date, completed=0):
        # Текстовое поле задачи
        task_field = ft.TextField(
            value=task_text,
            read_only=True,
            expand=True,
            border=ft.InputBorder.NONE,
            text_size=16
        )
        
        # Чекбокс статуса
        checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: (
                main_db.update_task(task_id=task_id, completed=int(e.control.value)),
                load_tasks() if filter_type != 'all' else page.update()
            )
        )
        
        # Подпись с датой
        date_label = ft.Text(value=task_date, size=12, color=ft.Colors.GREY_500)

        # Функции редактирования внутри компонента
        def edit_clicked(e):
            task_field.read_only = False
            task_field.border = ft.InputBorder.OUTLINE
            task_field.focus()
            page.update()

        def save_clicked(e):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            task_field.border = ft.InputBorder.NONE
            page.update()

        # Кнопки действий
        edit_btn = ft.IconButton(ft.Icons.EDIT, on_click=edit_clicked, icon_color=ft.Colors.BLUE)
        save_btn = ft.IconButton(ft.Icons.SAVE, on_click=save_clicked, icon_color=ft.Colors.GREEN)
        delete_btn = ft.IconButton(
            ft.Icons.DELETE, 
            icon_color=ft.Colors.RED,
            on_click=lambda _: (main_db.delete_task(task_id), load_tasks())
        )

        return ft.Row(
            controls=[
                checkbox,
                ft.Column([task_field, date_label], expand=True, spacing=0),
                edit_btn,
                save_btn,
                delete_btn
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    #  Элементы интерфейса (UI) 

    task_input = ft.TextField(label='Что нужно сделать?', expand=True, on_submit=add_task_event)
    add_btn = ft.ElevatedButton('Добавить', icon=ft.Icons.ADD, on_click=add_task_event)

    filter_row = ft.Row([
        ft.TextButton('Все', on_click=lambda _: set_filter('all')),
        ft.TextButton('В работе', on_click=lambda _: set_filter('uncompleted')),
        ft.TextButton('Готово', on_click=lambda _: set_filter('completed')),
    ], alignment=ft.MainAxisAlignment.CENTER)

    clear_completed_btn = ft.ElevatedButton(
        "Очистить выполненные", 
        icon=ft.Icons.DELETE_SWEEP, 
        color=ft.Colors.RED_400,
        on_click=clear_completed_tasks
    )

    # Сборка страницы 
    page.add(
        ft.Row([task_input, add_btn]),
        ft.Divider(),
        filter_row,
        ft.Row([clear_completed_btn], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        task_list
    )

    # Запуск начальной загрузки
    load_tasks()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)