def func_a():
    print("func_a")
    func_b()

def func_b():
    print("func_b")
    func_a()

if __name__ == "__main__":
    func_a()
