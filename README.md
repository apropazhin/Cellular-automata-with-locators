# Cellular automata with locators

**Запуск программы:**
1. Сначала нужно создать решетку: CellAutoWall(n), где n - размер решетки. Работа с решеткой похожа на работу с системой координат за тем исключением, что начало координат находится в верхнем левом углу и что при движении вниз координата увеличивается, а не уменьшается.
2. Далее идет вызов тестирующей функции test(cell_auto, y_s, x_s, y_e, x_e, y_u, y_d, x_u, x_d), где cell_auto - решетка; y_s, x_s - координаты одной из начальных клеток; y_e, x_e - координаты второй начальной клетки; y_u, y_d, x_u, x_d - координаты двух углов (верхний левый (u) и нижний правый (d)) препятствия, по которым оно однозначно задается.

Примеры запуска функции test есть в функции main. Необходимо раскомментировать один из случаев и запустить программу.
