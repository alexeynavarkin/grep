
GREP
==================

Функция частично реализующая функционал консольной утилиты grep.

Описание
--------

Функция фильтрует строки, поступающие на стандартный вход и фильтрует их, согласно параметрам.

Перечисление параметров:
* _invert_ — выводить строки, которые __НЕ__ совпадают с шаблоном
* _ignore_case_ — при сравнении шаблона не учитывать регистр
* _count_ — выводить только число строк удовлетворивших шаблону
* _line_number_ — перед срокой выводить также и ее номер (строки нумеруются с единицы) в виде "5:строка"
* _context_ __N__ — помимо строки удовлетворяющей шаблону вывести также и __N__ строк до и __N__ строк после нее если столько есть. Если соседние блоки пересекаются то их нужно объединять. Если используется флаг _line_number_, то строки контекста нумеруются так "5-строка".
* _before_context_ __N__ — аналогично _context_, но выводить нужно только строки __ДО__ найденой.
* _after_context_ __N__ — аналогично _context_, но выводить нужно только строки __ПОСЛЕ__ найденой.
* _pattern_ __str__ — строка, описывающая шаблон поиска. В строке могут использоваться специальные сиволы:
    * __"?"__ — один любой символ;
    * __"*"__ — ноль или несколько любых символов (но в рамках одной строки)

