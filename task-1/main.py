

class MyDataFrame:
    def __init__(self, data: list[tuple], columns: list[str]) -> None:
        self.data = data
        self.columns = columns
        self._col_to_index = {col: idx for idx, col in enumerate(columns)}
        # We need to validate input data
        if len(data) == 0:
            raise ValueError("Data cannot be empty")
        if not all(len(row) == len(self.columns) for row in data):
            raise ValueError("All rows in data must have the same length of columns!")

    def __getattr__(self, name):
        """
        This method will help you to retrieve column from dataset like attribute, for example:
        >>> df.a
        which `a` in this case is the column name

        :param name:
        :return:
        """
        if name in self._col_to_index:
            col_idx = self._col_to_index[name]
            return [row[col_idx] for row in self.data]
        raise AttributeError(f"{self.__class__.__name__} object has no attribute '{name}'")

    def __getitem__(self, name):
        """
        This method helps to slice our dataset, I just wrote list method for slicing it could be expended
        But for this task `list` would be enough.
        :param name:
        :return:
        """
        if isinstance(name, list):
            for col in name:
                if col not in self._col_to_index:
                    raise ValueError(f"Column {col} does not exits in DataFrame!")
            col_idx = [self._col_to_index[col] for col in name]
            selected_rows = [[row[idx] for row in self.data] for idx in col_idx]
            return selected_rows
        else:
            raise ValueError(f"Format not supported yet! use column slicing instead!")

    def index(self, idx):
        """
        This method will retrieve specific index
        :param idx:
        :return:
        """
        if idx <0 or idx >= len(self.data):
            raise ValueError("Index out of range!")
        return self.data[idx]


    def sort(self, column, mode="ascending"):
        """
        This method will sort data set based on specified column.
        :param column:
        :param mode:
        :return:
        """
        if column not in self.columns:
            raise ValueError(f"Column {column} does not exits in DataFrame!")

        col_idx = self._col_to_index[column]
        sort_mode = True if mode == "ascending" else False
        # self.data.sort(key=lambda row: row[col_idx], reverse=not sort_mode)
        """
        If there isn't None in the data we could simply use above line of the code for sorting,
        But it's not, so we have to convert it to inf which help us to apply comparison operation
        in case of sorting 
        """
        self.data.sort(
            key=lambda row: (row[col_idx] is None, row[col_idx] if row[col_idx] is not None else float('-inf')),
            reverse=not sort_mode,
        )
        return self.__repr__()
        

    def __repr__(self):
        """
        This is a simple representation of dataframe could be better like what the Pandas library does such as:
        adding column width
        adding table like style
        But it's out of task scope, lets keep it simple.
        """
        header = " ".join(self.columns)
        rows = [" ".join(map(str, row)) for row in self.data]

        return f"{header}\n" + "\n".join(rows)


df = MyDataFrame(data=[(1, 2, 3), (4, None, 10), (5, 1, 19)], columns=['a', 'b', 'c'])
# calling __repr__ method here.
print(df)
# calling __getattr__ method.
print(df.a)
print(df.b)
# In this case I've tested slicing method according to document.
print(df[["a", "c"]])
# Finally the sort method which worked as expected.
print(df.sort("b", mode="ascending"))
