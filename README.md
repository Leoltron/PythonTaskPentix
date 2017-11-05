# Игра "Пентикс"
Автор: Пироговский Леонид

## Описание
Данная игра является аналогом знаменитого "Тетриса" с фигурами из 5 клеток. Правила стандартные: в поле 15 на 30 сверху вниз падают управляемые игроком фигуры, которые можно двигать из стороны в сторону, вращать и "бросать", ускоряя их падение. Заполняя линию поля, она исчезает. За уничтожение нескольких линий подряд очки начисляются следующим образом:
* 1 линия - 100 очков
* 2 линии - 300 очков
* 3 линии - 700 очков 
* 4 линии - 1500 очков
* 5 линий - 3100 очков

Игра заканчивается, когда фигуры переполняют поле.

## Дополнительные особенности
* Фигура "Ластик" - Фигура 1x1, выглядит как рамка - фигура, стирающая все клетки, по которым проходит. Может двигаться в стороны только раз в одной линии.
* Фигура "Бомба" - Фигура 1x1, выглядит, как ромб - после падения ждет падения еще 4 фигур, после уничтожает все фигуры в радиусе 1 вокруг себя. Количество четвертей показывает время до взрыва.
* Цветные линии - если все клетки в заполненой линии оказываются одного цвета, то линия считается за три. При включенном режиме цветных линий появляется дополнительный цвет - радужный.

## Управление
* Стрелка влево/A - сдвинуть фигуру влево 
* Стрелка вправо/D - сдвинуть фигуру вправо
* Стрелка вверх/W - развернуть (против часовой стрелки)
* Стрелка вниз/S - сдвинуть фигуру вниз
* Пробел - мгновенно сбросить фигуру вниз

## Пакетный режим

Справка: main.py --help Пример запуска: main.py --width 10 --height 10 --bg cyan --cc green blue magenta
