class LineIterator:
    def __init__(self, lines):
        """
        Initializes the iterator with a list of lines.

        :param lines: List of lines to iterate over.
        """
        self.lines = lines
        self.index = 0
        self.line_number = 0
        self.file_path = ''

    def __iter__(self):
        """
        Returns the iterator object itself.

        :return: The iterator object.
        """
        return self

    def __next__(self):
        """
        Returns the next line from the iterator.

        :return: The next line (str) from the lines list.
        :raises StopIteration: When all lines have been iterated.
        """
        if self.index >= len(self.lines):
            raise StopIteration
        line = self.lines[self.index].strip()
        self.index += 1
        self.line_number += 1
        return line

    def peek(self):
        """
        Returns the current line without advancing the iterator.

        :return: The current line (str), or raise StopIteration if there are no more lines.
        """
        if self.index < len(self.lines):
            return self.lines[self.index].strip()
        raise StopIteration

    def push_back(self):
        """
        Pushes back the last returned line to the iterator.
        This allows revisiting the last consumed line.
        """
        if self.index > 0:
            self.index -= 1
            self.line_number -= 1
