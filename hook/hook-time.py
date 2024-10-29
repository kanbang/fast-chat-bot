import time

# 确保在打包时使用 time.perf_counter 作为替代
if not hasattr(time, 'clock'):
    time.clock = time.perf_counter
