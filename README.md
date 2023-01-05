Программа работает с матрицей смежности ацикличного графа.Также в программе есть проверка на ацикличность графа.
В процессе выводится матрица смежности с добавочным столбцом, в котором отображается высота вершины.
На последней итерации выводится матрица со всеми высотами.

Работа программы построена на следующем алгоритме:
Шаг 0. Для построения матрицы М0 добавляем к матрице М слева пустой столбец; далее находим нулевые столбцы матрицы М;
 соответствующие этим вершинам строки матрицы М0 помечаем, а в соответствующих клетках добавленного столбца ставим символ 0.
Шаг 1. Для построения матрицы М1 находим те столбцы матрицы М0, в которых символ 1 стоит ТОЛЬКО в отмеченных строках;
 соответствующие этим вершинам строки матрицы помечаем, а в соответствующих клетках добавленного столбца ставим символ 1.
И т.д. процесс продолжается до тех пор, пока все строки матрицы станут отмеченными.
Тогда добавочный столбец будет полностью заполнен, а стоящие в нем числа указывают высоту соответствующих вершин графа.

Экземпляр хранит в себе матрицу смежности с добавленным столбцом, а также множество отмеченных строк.

    class Graph:
        def __init__(self, matrix: list) -> None:
            self.matrix: list = matrix
            for i in range(len(self)):
                self.matrix[i].insert(0, None)
            self.marked_lines = set()


Метод __check_column проверяет, что столбец не нулевой.

    def __check_column(self, column_number: int) -> bool:
            # column_number НЕ должен быть меньше 1
            # если столбец не нулевой вернет True
            if column_number < 1:
                raise IndexError('column_number НЕ должен быть меньше 1')
            column = [int(self.matrix[line][column_number]) for line in range(len(self.matrix))]  # список столбца
            return any(column)

Метод __len__ переопределяет функцию len для экземпляров класса.

     def __len__(self) -> int:
         return len(self.matrix)

Метод __check_add_column проверяет что в добавленном столбце еще есть незаполненные вершины.

    def __check_add_column(self) -> bool:
        add_column = [self.matrix[line][0] for line in range(len(self))]
        return not all(add_column)


Находим нулевые столбцы матрицы М0;
 соответствующие этим вершинам строки матрицы М0 помечаем, а в соответствующих клетках добавленного столбца ставим символ 0.

    def __stage0(self) -> None:
        for column in range(1, len(self) + 1):  # все столбцы кроме 0(он добавочный)
            if not self.__check_column(column):
                self.matrix[column - 1][
                    0] = '0'  # в данном случае помечаем строку которая соотвествует column в добавленном столбце
                self.marked_lines.add(column - 1)  # возврат к нумерации с 0


Находим те столбцы матрицы М0, в которых символ 1 стоит только в отмеченных строках;
 соответствующие этим вершинам строки матрицы помечаем, а в соответствующих клетках добавленного столбца ставим текущую высоту.

    def __stage1(self, k: int) -> int:
        tmp_list = []
        for column in range(1, len(self) + 1):
            flag = True
            for line in range(len(self)):
                if (self.matrix[line][column] == 1) and (
                        line not in self.marked_lines):  # все нулевые в шаге 2 помечаются
                    flag = False
            if flag and ((column - 1) not in self.marked_lines):
                tmp_list.append(column - 1)
                self.matrix[column - 1][0] = str(k)
        for x in tmp_list:
            self.marked_lines.add(x)
        k += 1
        return k


Метод считает все высоты для всех вершин (пока есть незаполненные вершины в добавочной матрице) и выводит матрицу на каждой итерации.

    def calc_all_heights(self) -> None:
        self.__stage0()
        k = 1
        self.print_matrix()
        while self.__check_add_column():
            k = self.__stage1(k)
            self.print_matrix()


Метод выводит матриицу

    def print_matrix(self) -> None:
        print()
        print(*[line for line in self.matrix], sep='\n')


Метод проверяет на циклы от заданной вершины(по умолчанию 0) путем поиска в глубину и раскрашивает в 3 цвета. 
Белые - непосещенные вершины, серые - посещенные, черные -  вершины,из которых вышли окончательно, то есть они точно не состоят в цикле

    def __dfs(self, colors: list, start: int = 0, answer: bool = False) -> bool:
        if len(colors) == 0:
            colors = ['white'] * len(self.matrix)
        if colors[start] == 'grey':
            answer = True
            return answer
        colors[start] = 'grey'
        if colors[start] != 'black':
            for i in range(len(self.matrix)):
                if self.matrix[start][i]:
                    answer = self.__dfs(colors, i, answer)
                    colors[i] = 'black'
        colors[start] = 'black'
        return answer


Метод проверяет граф на циклы. Запускает проверку на циклы поиском в глубину от каждой вершины

    def is_cycled(self) -> bool:
        is_cycled = False
        edges = range(len(self))
        for i in edges:
            if self.__dfs(list(), i):
                is_cycled = True
                break
        return is_cycled


Функция читает матрицу из файла

    def read_file():
        with open('matrix.txt') as file:
            str_matrix = file.readlines()
            matrix = []
            for s in str_matrix:
                matrix.append(list(map(int, s.split())))
            try:
                assert len(matrix) != 0
            except AssertionError:
                print("Матрица Пустая")
                input()
                exit(-1)
            try:
                assert len(matrix) == len(matrix[0])
            except AssertionError:
                print("Матрица не квадратная или лишние отступы в файле")
                input()
                exit(-1)
        return matrix


