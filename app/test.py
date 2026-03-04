def func_a():
    """
    Prints "func_a" and invokes func_b.
    
    This function outputs the literal string "func_a" to standard output and then calls func_b. As written, calling this function (together with the provided func_b) leads to unbounded mutual recursion and will raise a RecursionError when the Python recursion limit is reached.
    """
    print("func_a")
    func_b()

def func_b():
    """
    Trigger the execution of func_a after printing 'func_b'.
    """
    print("func_b")
    func_a()

if __name__ == "__main__":
    func_a()
