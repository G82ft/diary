from tkinter import Widget, Frame


class Table:
    frame: Frame
    columns: list['Column']

    def __init__(self, master: Widget):
        self.frame = Frame(master)

        self.frame.rowconfigure(0, weight=1)

        self.columns = []

    def __getitem__(self, index: int) -> 'Column':
        return self.columns[index]

    def __setitem__(self, index: int, value: 'Column') -> None:
        self.columns[index] = value

        self.update(index)

    def __delitem__(self, index: int) -> None:
        self.columns[index].destroy()
        del self.columns[index]

        self.update(index)

    def append(self, column: 'Column') -> None:
        self.columns.append(column)

        index: int = len(self.columns) - 1
        self.frame.columnconfigure(index, weight=1, uniform='columns')

        self.update(index)

    def insert(self, index: int, column: 'Column') -> None:
        self.columns.insert(index, column)

        self.frame.columnconfigure(len(self.columns) - 1, weight=1, uniform='columns')

        self.update(index)

    def remove(self, index: int) -> None:
        del self.columns[index]

        self.update(index)

    def update(self, start: int = 0) -> None:
        for index, column in enumerate(self.columns[start:], start=start):
            column.grid_remove()
            column.grid(
                row=0,
                column=index,
                sticky='nesw'
            )

    def grid(self, **kwargs) -> None:
        return self.frame.grid(**kwargs)

    def grid_remove(self) -> None:
        return self.frame.grid_remove()

    def destroy(self):
        for column in self.columns:
            column.destroy()


class Column:
    table: Table
    rows: list[Widget]
    frame: Frame

    def __init__(self, table: Table):
        self.table = table
        self.frame = Frame(table.frame)
        self.frame.columnconfigure(0, weight=1)
        self.rows = []

    def __getitem__(self, index: int) -> Widget:
        return self.rows[index]

    def __setitem__(self, index: int, value: Widget):
        self.rows[index] = value

        self.update(index)

    def __delitem__(self, index: int):
        self.rows[index].destroy()
        del self.rows[index]

        self.update(index)

    def append(self, value: Widget) -> None:
        self.rows.append(value)

        index: int = len(self.rows) - 1
        self.frame.rowconfigure(index, weight=1)

        self.update(index)

    def insert(self, index: int, value: Widget) -> None:
        self.rows.insert(index, value)

        self.frame.rowconfigure(len(self.rows) - 1, weight=1)

        self.update(index)

    def remove(self, index: int) -> None:
        self.rows[index].destroy()
        del self.rows[index]

        self.update(index)

    def update(self, start: int = 0) -> None:
        for row, widget in enumerate(self.rows[start:], start=start):
            widget.grid_remove()
            widget.grid(
                row=row,
                column=0,
                sticky='nesw'
            )

    def grid_remove(self) -> None:
        return self.frame.grid_remove()

    def grid(self, **kwargs) -> None:
        return self.frame.grid(**kwargs)

    def destroy(self):
        for row in self.rows:
            row.destroy()
