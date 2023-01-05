class Graph:
    def __init__(self, matrix: list) -> None:
        # выполняет шаг 0 в т.ч
        self.matrix: list = matrix
        if self.is_cycled():
            print("Граф цикличный")
            input()
            exit(-1)
        for i in range(len(self)):
            self.matrix[i].insert(0, None)
        self.marked_lines = set()

    def __check_column(self, column_number: int) -> bool:
        # column_number не должен быть меньше 1
        if column_number < 1:
            raise IndexError('column_number не должен быть меньше 1')
        column = [int(self.matrix[line][column_number]) for line in range(len(self.matrix))]  # список столбца
        return any(column)  # если столбец ненулевой,то вернет True

    def __stage0(self) -> None:
        for column in range(1, len(self) + 1):  # все столбцы кроме 0(он добавочный)
            if not self.__check_column(column):
                self.matrix[column - 1][
                    0] = '0'  # в данном случае помечаем строку,которая соотвествует column в добавленном столбце
                self.marked_lines.add(column - 1)  # возврат к нумерации с 0

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

    def calc_all_heights(self) -> None:
        self.__stage0()
        k = 1
        self.print_matrix()
        while self.__check_add_column():
            k = self.__stage1(k)
            self.print_matrix()

    def __check_add_column(self) -> bool:
        # проверяет,что в добавленном столбце еще есть незаполненные вершины
        add_column = [self.matrix[line][0] for line in range(len(self))]
        return not all(add_column)

    def print_matrix(self) -> None:
        print()
        print(*[line for line in self.matrix], sep='\n')

    def __dfs(self, colors: list, start: int = 0, answer: bool = False) -> bool:
        # проверка на циклы от заданной вершины(по умолчанию 0) путем поиска в глубину
        # и раскраски в 3 цвета. Белые - не посещенные вершины, серые - посещенные, черные - точно не состоят в цикле
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

    def is_cycled(self) -> bool:
        # Проверяет граф на циклы. Запускает проверку на циклы поиском в глубину от каждой вершины
        is_cycled = False
        edges = range(len(self))
        for i in edges:
            if self.__dfs(list(), i):
                is_cycled = True
                break
        return is_cycled

    def __len__(self) -> int:
        return len(self.matrix)


def read_file():
    # Считывание матрицы из файла
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

print('Программа считает высоты вершин ацикличного графа')
print("Вводите в текстовый файл корректную матрицу смежности")
print('И пожалуйста, если вы найдете ошибки, напишите нам в сообщения')

try:
    N = read_file()
    test = Graph(N)
    test.calc_all_heights()
    input()
except:
    print("Произошла ошибка. Проверьте файл и его содержимое")
    input()

