
from option import Result, Option, Ok, Err
import dtshare as dt
import matplotlib as my
def test01(s: str) -> int:
    print("ssss")
    print("ssss%s", s)

    return ''


import time


# 定义装饰器
def time_calc(func):
    def wrapper(*args, **kargs):
        start_time = time.time()
        f = func(*args, **kargs)
        exec_time = time.time() - start_time
        return f

    return wrapper


# 使用装饰器
@time_calc
def add(a, b):
    return a + b


@time_calc
def sub(a, b):
    return a - b


if __name__ == '__main__':
    test01(3)
    s=  isinstance("",str)
    print(s)
    add(3,4)

    aa=Ok(1)
    print(aa.is_ok)
    print(aa.unwrap())
    print(aa._val)
    df = dt.get_tick_data('600868')
    print(df)
