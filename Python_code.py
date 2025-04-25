import numpy as np
import matplotlib.pyplot as plt
import time


def factorial(n):
    return n if n ==1 else n * factorial(n-1)


def is_scheduable(task_set):
    total_utilization = np.sum(task_set[:, 0] / task_set[:, 1])
    print(f"Total Utilization is {total_utilization:<.3f}", end=" ")
    if total_utilization < 1:
        print("--> Is schedulable.")
    else:
        raise ValueError("Task set is not schedulable.")

def count_valid(k):
    print(k)
    return factorial(sum(k)) // np.prod([factorial(ki) for ki in k])

# %% permutation functions

def is_valid(seq):
    n = len(seq)
    for i in range(n):
        task_i, occ_i = divmod(seq[i], 10)
        for j in range(i):
            task_j, occ_j = divmod(seq[j], 10)
            
            if task_i == task_j and occ_i < occ_j:
                return False
    return True


def get_timing(seq):
    timing = np.zeros(len(seq)*2, dtype=int)
    did_pass = np.zeros(tab.shape[0], dtype=bool)
    
    delay = 0
    idx = 0
    for c_index in range(len(seq)):
        
        c = seq[c_index]
        
        task_i, occ_i = divmod(c, 10)
        task_i -= 1 # make index
        
        normal_start = tab[task_i, 1] * (occ_i-1)
        normal_end = normal_start + tab[task_i, 1]
        
        count = tab[task_i, 0]
        if did_pass[task_i]: # déjà passé, doit attendre
            # print(f"task {task_i + 1} already passed")
            while idx%tab[task_i, 1] != 0:
                timing[2*c_index-1] += 1
                
                idx += 1
                for pos in np.argwhere(idx % tab[:, 1] == 0):
                    # print("pos :", pos)
                    did_pass[pos] = False
                    
            did_pass[task_i] = False
        
        did_pass[task_i] = True
        for _ in range(count):
            timing[2*c_index] += 1
            # print(task_i)
            idx += 1
            for pos in np.argwhere(idx % tab[:, 1] == 0):
                # print("pos :", pos)
                did_pass[pos] = False
        
        real_start = sum(timing[:2*c_index])
        real_end = real_start + timing[2*c_index]
        
        if real_start < normal_start or real_end > normal_end:
            return timing, delay, False
        
        delay += real_start - normal_start
    
    return timing, delay, True




def all_permutations(tab):
    a = get_one_permutation(tab)
    n = len(a)
    
    c = [0] * n
    
    # results = np.zeros((factorial(sum(30 // tab[:, 1])), n), dtype=int)
    results = []
    bad = []
    bad_timings = []
    timings = []
    delays = []
    
    index = 0
    if is_valid(a):
        # results[0, :] = a.copy()
        # index += 1
        timing, delay, is_timing_ok = get_timing(a.copy())
        if is_timing_ok:
            results.append(a.copy())
            timings.append(timing)
            delays.append(delay)
        
    
    i = 0
    while i < n:
        if c[i] < i:
            swap_idx = 0 if i%2 == 0 else c[i]
            temp = a[i]
            a[i] = a[swap_idx]
            a[swap_idx] = temp
            
            if is_valid(a):
                # results[index] = a.copy()
                # index += 1
                
                
                # create timing
                timing, delay, is_timing_ok = get_timing(a.copy())
                # print(a)
                # print(timing)
                
                # if timing ok, append
                if is_timing_ok:
                    results.append(a.copy())
                    timings.append(timing)
                    delays.append(delay)
                else:
                    bad.append(a.copy())
                    bad_timings.append(timing)
            c[i] += 1
            i = 0
        else:
            c[i] = 0
            i += 1
    
    # return np.array(results)
    return np.array(results), np.array(timings), np.array(delays), bad, bad_timings


def get_one_permutation(tab):
    task = []
    maximum = np.max(tab[:, 1])
    
    for line in range(tab.shape[0]):
        t = tab[line, 1]
        for i in range(maximum // t):
            task.append(10 * (line+1) + (i+1))
    return np.array(task)

# %% showing functions


def show_scheduals(permutations, timings, n=8, search=0):
    fig, axes = plt.subplots(n, 1, figsize=(16, 2.17*n), sharex=False)
    
    x = np.arange(0, 40)
    labels = np.array([f"task {6 - i}" for i in range(6)])
    current_perm_index = n*search
    for ax, current in zip(axes, permutations[n*search:n*(search+1)]):
        labels_bar = []

        mask = np.ones(len(x), dtype=bool)
        y = np.zeros_like(x)

        for i in range(len(current)):
            
            task_i, occ_i = divmod(current[i], 10)
            task_i -= 1 # en indice
            
            start_task = sum(timings[current_perm_index, :2*i])
            end_task = start_task + timings[current_perm_index, 2*i]
            end_pause = end_task + timings[current_perm_index, 2*i+1]
            
            y[start_task:end_task] = 6 - task_i

            mask[end_task:end_pause] = False

        mask[end_pause:] = False
            
        width = np.full_like(x, .93, dtype=float)
        ax.barh(y[mask]-1, width[mask], left=x[mask], color = 'red', edgecolor = 'red', align='center', height=1)
        
        
        ax.set_yticks(np.arange(len(labels)))
        ax.set_yticklabels(labels)
        ax.set_xlim(0, len(x))
        ax.grid(True, alpha=.2, linestyle="-.", )
        ax.set_title(f"Permutation: {current}")

        current_perm_index += 1
        
        
    plt.tight_layout()
    plt.show()
    return None


def show_schedual(permutation, timing, l=30):
    plt.figure(figsize=(16, 3))
    
    x = np.arange(0, l)
    labels = np.array([f"task {i}" for i in range(tab.shape[0])])
    
    labels_bar = []

    mask = np.ones(len(x), dtype=bool)
    y = np.zeros_like(x)
    # print("-"*5, current, "-"*5)
    for i in range(len(permutation)):
        task_i, occ_i = divmod(permutation[i], 10)
        task_i -= 1 # en indice
        
        start_task = sum(timing[:2*i])
        end_task = start_task + timing[2*i]
        end_pause = end_task + timing[2*i+1]
        
        y[start_task:end_task] = 7 - task_i

        mask[end_task:end_pause] = False
        
    mask[end_pause:] = False
        
    width = np.full_like(x, 1, dtype=float)
    plt.barh(y[mask]-1, width[mask], left=x[mask], color = 'red', edgecolor = 'red', align='center', height=1)
    
    # for xi, yi, lbl in zip(x, current, labels_bar): # annotate each bar
    #     ax.text(xi + 0.91/2, yi, lbl, va='center', ha='center', color='white', fontsize=8)
    
    plt.yticks(np.arange(len(labels)))
    plt.xlim(0, len(x))
    # plt.set_yticklabels(labels)
    
    plt.grid(True, alpha=.2, linestyle="-.", )
    plt.title(f"Permutation: {permutation}")
    # print(y)
    # if current_perm_index == 5:
    #     break
        
        
    plt.tight_layout()
    plt.show()
    return None


# %% start here

start_clock = time.time()

# shorter task set, less time consumming.
tab = np.array([[2, 10],
                [2, 20],
                [2, 20],
                [2, 40]])

task = get_one_permutation(tab)

is_scheduable(tab)

# task = np.array([11, 12, 21], dtype='int16')

valid_perm, timings, delays, bad, bad_timings = all_permutations(tab)
# valid_perm = valid_permutations(permutations)


# for perm in permutations:
#     print(perm)


print()
print(valid_perm.shape[0], "valid permutations. \n")


min_arg = np.argmin(delays)
n = len(np.where(delays == delays[min_arg])[0])

print("minimum delay:", delays[min_arg])
print(f"There is {n} best schedual.")
print(f"permutation n°{min_arg}:", valid_perm[min_arg])

show_schedual(bad[0], bad_timings[0], l=30)


end_clock = time.time()

print("Run time:", end_clock - start_clock)


# %% testing area

tab = np.array([[2, 10],
                [3, 10],
                [2, 20],
                [3, 40]])



def test():
    
    is_scheduable(tab)

    arr1 = np.array([11, 31, 21, 12, 22, 13, 23])
    arr2 = np.array([21, 11, 12, 22, 31, 13, 23])
    arr3 = np.array([11, 31, 22, 12, 21, 13, 23])
    
    print("arr1 validity:", is_valid(arr1))
    print("arr2 validity:", is_valid(arr2))
    print("arr3 validity:", is_valid(arr3))
    print("-"*15)
    
    timing1, delay1, is_timing_ok1 = get_timing(arr1)
    timing2, delay2, is_timing_ok2 = get_timing(arr2)
    timing3, delay3, is_timing_ok3 = get_timing(arr3)
    
    print("arr1 timing:", timing1)
    print("arr1 delay: ", delay1)
    print("arr1 is ok?:", is_timing_ok1)
    
    print("-"*15)
    
    print("arr2 timing:", timing2)
    print("arr2 delay: ", delay2)
    print("arr2 is ok?:", is_timing_ok2)
    
    print("-"*15)
    
    print("arr3 timing:", timing3)
    print("arr3 delay: ", delay3)
    print("arr3 is ok?:", is_timing_ok3)
    
    
if __name__ == '__main__':
    test()
    
    
# %%

seq1 = np.array([31, 11, 61, 21, 41, 12, 51, 22, 32, 13, 42, 23, 14, 24])
seq2 = np.array([41, 61, 11, 21, 51, 12, 31, 22, 13, 32, 42, 23, 14, 24])
seq3 = np.array([11, 61, 51, 21, 41, 31, 12, 22, 32, 42, 13, 23, 14, 24])

timing1, delay1, isok1 = get_timing(seq1)
timing2, delay2, isok2 = get_timing(seq2)
timing3, delay3, isok3 = get_timing(seq3)

show_scheduals(np.array([seq1, seq2, seq3]),
               np.array([timing1, timing2, timing3]),
               n=3)
