from distance import DistanceSensorComm
from ring import Ring
from math import pow
import time

def measure_and_print(name, points):
    print("-----------------------------")
    print(name)
    print("-----------------------------")
    sens = DistanceSensorComm('P20','P21')
    r = Ring('f', points)
    print("Measuring..")
    for i in range(0,points):
        # Without this the output is just random noise
        # 20ms is as low as we can go for ~4m
        time.sleep(0.02)
        r.push(sens.distance())
    print("MEASURED.")
    for i in reversed(range(0,points)):
        pr = r.prev(i)
        print(pr)

def count_objects(interval_ms, var_max):
    r = Ring('f', 64)
    times = Ring('I', 64)
    sens = DistanceSensorComm('P20','P21')
    # This is to eliminate the initial variance from 0-initialized ring
    for i in range(0,64):
        r.push(sens.distance())

    count = 0
    tf = time.ticks_ms() + interval_ms
    t = time.ticks_ms()
    while t < tf:
        time.sleep(0.02)
        d = sens.distance()
        if d < 400:
            r.push(d)
            mean = d + r.prev(1) + r.prev(2)
            mean /= 3.0
            var = pow(d - mean, 2) + pow(r.prev(1) - mean, 2) + pow(r.prev(2) - mean, 2)
            var /= 3.0
            #if (r.prev(1) + d) < (1.5 * 25):
            if var > var_max:
                times.push(t)
                if t - times.prev(1) > 100:
                    count += 1
                    print(count)
        t = time.ticks_ms()
    return count

print("Hello there :)")
