import signal
import time


def timeout_handler(sig, frame):
    raise RuntimeError


try:
    signal.signal(signal.SIGALRM, timeout_handler)  # 设置信号和回调函数
    signal.alarm(3)  # 设置 num 秒的闹钟
    print('start alarm signal.')
    time.sleep(4)
    print('close alarm signal.')
    signal.alarm(0)  # 关闭闹钟
except RuntimeError as e:
    print("Runtime error")
