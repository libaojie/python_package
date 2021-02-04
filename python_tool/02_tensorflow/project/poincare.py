import random
from datetime import datetime

"""
庞加莱回归时间
"""
data = [1, 2, 3, 4, 5, 6, 7, 8]
length = len(data)


def main():
    start_time = datetime.now()
    numb = 1
    new_data = random.sample(data, length)
    while data != new_data:
        print(f"第【{numb}】次运算，结果为【{new_data}】")
        new_data = random.sample(new_data, length)
        numb += 1

    print(f"共运算【{numb}】次，时间为【{datetime.now() - start_time}】")


main()
