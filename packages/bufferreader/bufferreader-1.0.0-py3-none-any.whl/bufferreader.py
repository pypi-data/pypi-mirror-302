"""BufferReader Module.

This module provides the `BufferReader` class for reading, navigating, and manipulating text buffers.
It handles the movement of internal pointers and offers methods for reading, resetting,
and retrieving streams of characters from the buffer.

Key Features:
- Move a pointer forward or backward through a multi-line text buffer.
- Read a specific range of characters between positions.
- Efficient handling of pointer operations without throwing exceptions.
- Customizable forward and backward step sizes to control pointer navigation.
- Stores the current stream of characters based on the last read operation.

Typical use case involves reading a text buffer sequentially or non-sequentially with pointer-based navigation.

Exceptions:
- The class avoids exceptions for pointer movement by returning status flags (True/False) to indicate success
or failure of operations.

Note:
- Input buffer is expected to be a string and must be properly formatted. Non-string input will raise a `TypeError`.

"""

from __future__ import annotations


class BufferReader:
    r"""A class to manage reading and pointer navigation within a multi-line text buffer.

    The `BufferReader` class is designed for reading text data and moving through it with an internal pointer system.
    It efficiently handles reading characters by moving forward or backward, while maintaining state and avoiding
    runtime exceptions for invalid pointer movements.
    Instead, it returns success flags to indicate pointer movement results.

    Attributes:
        stream (str): The currently selected character or string of characters from the last read operation.
        line (int): Current line index in the buffer, starting from 0.
        char (int): Current character index within the current line in the buffer, starting from 0.
        __steps_forward (int): Number of steps forward for the `next()` operation.
        __steps_back (int): Number of steps backward for the `before()` operation.

    Methods:
        move(steps: int) -> bool:
            Moves the internal pointer by a given number of steps and updates the current stream.

        read(start: int = 0, end: int = 0) -> bool:
            Reads characters from the buffer based on the range between the start and end positions.
            Updates the current stream and adjusts the forward/backward step sizes for future movement.

        next() -> bool:
            Moves the pointer forward by the number of characters read in the previous operation.

        before() -> bool:
            Moves the pointer backward by the number of characters read in the previous operation.

        reset() -> None:
            Resets the `stream` to the current character at the pointer position, and resets step sizes.

        set_pointer(line_pointer: int, char_pointer: int) -> bool:
            Sets the internal pointers to the specified line and character indices.
            Returns False if the indices are out of bounds.

    Usage Example:
        buffer = "Hello\\nWorld"
        reader = BufferReader(buffer)

        reader.read(0, 4)  # Reads "Hello"
        reader.next()  # Moves forward by 5 characters
        reader.before()  # Moves backward by 1 characters
        reader.set_pointer(1, 0)  # Moves the pointer to line 1, character 0 ("W")
        print(reader.stream)  # Outputs: "W"
    """

    def __init__(self, buffer: str) -> None:
        """Initializes the BufferReader with a text buffer.

        Args:
            buffer (str): The text content to be read.

        Raises:
            TypeError: If the input buffer is not a string.
        """
        if not isinstance(buffer, str):
            raise TypeError("Buffer must be a string.")

        self.__lines = buffer.splitlines(keepends=True)
        self.__line_pointer: int = 0
        self.__char_pointer: int = 0
        self.__steps_forward: int = 1
        self.__steps_back: int = 1
        self.stream: str = self.__lines[0][0] if self.__lines else ""

    @property
    def line(self) -> int:
        """Returns the current line pointer position."""
        return self.__line_pointer

    @property
    def char(self) -> int:
        """Returns the current character pointer position."""
        return self.__char_pointer

    def set_pointer(self, line_pointer: int, char_pointer: int) -> bool:
        """Sets the line and character pointers to specific positions.

        Args:
            line_pointer (int): The line number to set the pointer to.
            char_pointer (int): The character position to set the pointer to.

        Returns:
            bool: True if the pointer was successfully set, False otherwise.
        """
        if line_pointer < 0 or line_pointer >= len(self.__lines):
            return False
        if char_pointer < 0 or char_pointer >= len(self.__lines[line_pointer]):
            return False
        self.__line_pointer = line_pointer
        self.__char_pointer = char_pointer
        return True

    def __get_positions(self, position: int) -> tuple[int, int] | None:
        """Gets the target line and character positions after moving by a given number of steps."""
        if position == 0:
            return (self.__line_pointer, self.__char_pointer)

        move_line_pointer = self.__line_pointer
        move_char_pointer = self.__char_pointer

        if position > 0:
            while move_line_pointer < len(self.__lines) and position > 0:
                if position > len(self.__lines[move_line_pointer]) - move_char_pointer:
                    position -= len(self.__lines[move_line_pointer]) - move_char_pointer
                    move_char_pointer = 0
                    move_line_pointer += 1
                else:
                    move_char_pointer += position
                    position = 0
        else:
            position = -1 * position
            while move_line_pointer >= 0 and position > 0:
                if position > move_char_pointer:
                    position -= move_char_pointer + 1
                    move_line_pointer -= 1
                    move_char_pointer = len(self.__lines[move_line_pointer]) - 1
                else:
                    move_char_pointer -= position
                    position = 0

        if position == 0:
            return (move_line_pointer, move_char_pointer)
        else:
            return None

    def __get_stream(
        self,
        start_line_pos: int,
        start_char_pos: int,
        end_line_pos: int,
        end_char_pos: int,
    ) -> str:
        """Retrieves the output string between the start and end positions.

        Args:
            start_line_pos (int): Starting line index.
            start_char_pos (int): Starting character index.
            end_line_pos (int): Ending line index.
            end_char_pos (int): Ending character index.

        Returns:
            str: The substring between the specified positions.
        """
        stream = []
        if start_line_pos == end_line_pos:
            return self.__lines[start_line_pos][start_char_pos : end_char_pos + 1]

        stream.append(self.__lines[start_line_pos][start_char_pos:])
        stream.extend([self.__lines[line_pointer] for line_pointer in range(start_line_pos + 1, end_line_pos)])
        stream.append(self.__lines[end_line_pos][: end_char_pos + 1])

        return "".join(stream)

    def seek(self, steps: int) -> bool:
        """Move the pointer based on the provided offset.

        Args:
            steps (int): The number of characters to move the pointer.
        """
        positions = self.__get_positions(steps)
        if positions is not None:
            self.__line_pointer, self.__char_pointer = positions
            self.stream = self.__lines[self.__line_pointer][self.__char_pointer]
            self.__steps_forward, self.__steps_back = 1, 1
            return True
        else:
            return False

    def reset(self) -> None:
        """Resets the stream to the current character and resets movement steps.

        This method sets the stream to the current character in the buffer, without
        moving the pointer. It also resets both the forward and backward step counters to 1,
        so that the next move operation will advance or rewind by one character.

        Returns:
            None
        """
        self.seek(0)

    def read(
        self,
        start: int = 0,
        end: int = 0,
    ) -> bool:
        """Reads text from the buffer between the given start and end positions.

        Args:
            start (int): The start position offset.
            end (int): The end position offset.

        Returns:
            bool: True if reading was successful, False otherwise.
        """
        if start == 0 and end == 0:
            self.__steps_forward, self.__steps_back = 1, 1
            self.stream = self.__lines[self.__line_pointer][self.__char_pointer]
            return True

        is_reversed = False
        if start > end:
            is_reversed = True
            start, end = end, start

        start_positions = self.__get_positions(start)
        end_positions = self.__get_positions(end)
        if start_positions is None or end_positions is None:
            return False

        start_line_pos, start_char_pos = start_positions
        end_line_pos, end_char_pos = end_positions

        if end < 0:
            self.stream = self.__get_stream(start_line_pos, start_char_pos, end_line_pos, end_char_pos)
            steps_between_before = self.__get_stream(
                end_line_pos, end_char_pos, self.__line_pointer, self.__char_pointer
            )[1:]
            self.__steps_back = len(self.stream) + len(steps_between_before)
            self.__steps_forward = 1
        elif start > 0:
            self.stream = self.__get_stream(start_line_pos, start_char_pos, end_line_pos, end_char_pos)
            steps_between_after = self.__get_stream(
                self.__line_pointer, self.__char_pointer, start_line_pos, start_char_pos
            )[:-1]
            self.__steps_forward = len(steps_between_after) + len(self.stream)
        else:
            self.stream = self.__get_stream(start_line_pos, start_char_pos, end_line_pos, end_char_pos)
            if start < 0:
                self.__steps_back = -1 * start + 1
            else:
                self.__steps_back = 1
            if end > 0:
                self.__steps_forward = end + 1
            else:
                self.__steps_forward = 1
        if is_reversed:
            self.stream = self.stream[::-1]
        return True

    def next(self) -> bool:
        """Moves the pointer forward by the last read steps.

        Returns:
            bool: True if the movement was successful, False otherwise.
        """
        if self.seek(self.__steps_forward):
            return True
        else:
            return False

    def before(self) -> bool:
        """Moves the pointer backward by the last read steps.

        Returns:
            bool: True if the movement was successful, False otherwise.
        """
        if self.seek(-self.__steps_back):
            return True
        else:
            return False
