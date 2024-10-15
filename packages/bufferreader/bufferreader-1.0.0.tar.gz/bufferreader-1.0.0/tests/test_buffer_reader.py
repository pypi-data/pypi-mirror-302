from bufferreader import BufferReader

# Move tests
def test__move_pointer_greather_than_0_same_line():
    buffer = BufferReader("123456789\nabcdefghij")
    buffer.set_pointer(0, 2)
    assert buffer.seek(7) == True
    assert buffer.line == 0
    assert buffer.char == 9

def test__move_pointer_greather_than_0_next_line():
    buffer = BufferReader("123456789\nabcdefghij")
    buffer.set_pointer(0, 2)
    assert buffer.seek(11) == True
    assert buffer.line == 1
    assert buffer.char == 3

def test__move_pointer_greather_than_0_overflow():
    buffer = BufferReader("123456789\nabcdefghij")
    buffer.set_pointer(0, 2)
    assert buffer.seek(20) == False
    assert buffer.line == 0
    assert buffer.char == 2

def test__move_pointer_lesser_than_0_same_line():
    buffer = BufferReader("123456789\nabcdefghij")
    buffer.set_pointer(1, 4)
    assert buffer.seek(-2) == True
    assert buffer.line == 1
    assert buffer.char == 2

def test__move_pointer_lesser_than_0_next_line():
    buffer = BufferReader("123456789\nabcdefghij")
    buffer.set_pointer(1, 3)
    assert buffer.seek(-11) == True
    assert buffer.line == 0
    assert buffer.char == 2


def test__move_pointer_lesser_than_0_overflow():
    buffer = BufferReader("123456789\nabcdefghij")
    buffer.set_pointer(0, 2)
    assert buffer.seek(-20) == False
    assert buffer.line == 0
    assert buffer.char == 2

# Read tests

def test__read_greather_than_0_same_line():
    buffer = BufferReader("123456789\nabcdefghij")
    buffer.set_pointer(0, 4)
    assert buffer.read(0,3) == True
    assert buffer.stream == "5678"

def test__read_pointer_greather_than_0_next_line():
    buffer = BufferReader("012345678\nabcdefghij")
    buffer.set_pointer(0, 4)
    assert buffer.read(0,10) == True
    assert buffer.stream == "45678\nabcde"

def test__read_pointer_greather_than_0_overflow():
    buffer = BufferReader("123456789\nabcdefghij")
    buffer.set_pointer(0, 2)
    assert buffer.read(20) == False


def test__read_pointer_lesser_than_0_same_line():
    buffer = BufferReader("012345678\nabcdefghij")
    buffer.set_pointer(1, 4)
    assert buffer.read(-2,0) == True
    assert buffer.stream == "cde"


def test__read_pointer_lesser_than_0_next_line():
    buffer = BufferReader("123456789\nabcdefghij")
    buffer.set_pointer(1, 4)
    assert buffer.read(-10,0) == True
    assert buffer.char == 4
    assert buffer.line == 1
    assert buffer.stream == "56789\nabcde"



def test__read_pointer_lesser_than_0_overflow():
    buffer = BufferReader("123456789\nabcdefghij")
    buffer.set_pointer(1, 4)
    assert buffer.read(-20) == False

def test__read_before_and_after():
    buffer = BufferReader("012345678\nabcdefghij")
    buffer.set_pointer(1, 4)
    assert buffer.read(-2,2) == True
    assert buffer.stream == "cdefg"
    assert buffer._BufferReader__steps_back == 3 # type: ignore
    assert buffer._BufferReader__steps_forward == 3 # type: ignore

def test__read_before():
    buffer = BufferReader("012345678\nabcdefghij")
    buffer.set_pointer(1, 4)
    assert buffer.read(-6,-2) == True
    assert buffer.stream == "8\nabc"
    assert buffer._BufferReader__steps_back == 7 # type: ignore
    assert buffer._BufferReader__steps_forward == 1 # type: ignore

def test__read_after():
    buffer = BufferReader("012345678\nabcdefghij")
    buffer.set_pointer(0, 2)
    assert buffer.read(2,6) == True
    assert buffer.stream == "45678"
    assert buffer._BufferReader__steps_back == 1 # type: ignore
    assert buffer._BufferReader__steps_forward == 7 # type: ignore

def test_next():
    buffer = BufferReader("012345678\nabcdefghij")
    buffer.set_pointer(0, 2)
    assert buffer.read(2,6) == True
    assert buffer._BufferReader__steps_forward == 7 # type: ignore
    assert buffer.next() == True
    assert buffer.line == 0
    assert buffer.char == 9
    assert buffer.stream == "\n"

def test_before():
    buffer = BufferReader("012345678\nabcdefghij")
    buffer.set_pointer(1, 2)
    assert buffer.read(-8,-4) == True
    assert buffer._BufferReader__steps_forward == 1 # type: ignore
    assert buffer._BufferReader__steps_back == 9 # type: ignore
    assert buffer.before() == True
    assert buffer.line == 0
    assert buffer.char == 3
    assert buffer.stream == "3"
