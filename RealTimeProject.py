import numpy as np
import matplotlib.pyplot as plt
import time


def factorial(n):
    return n if n ==1 else n * factorial(n-1)


def is_scheduable(C, T):
    print(np.round(np.sum(C / T), 2), end="\t")
    if np.sum(C / T) < 1:
        print("Is schedulable.")
        return True
    else:
        print("Is not schedulable.", end="")
        return False

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




def all_permutations(task):
    a = task
    n = len(a)
    
    c = [0] * n
    
    # results = np.zeros((factorial(sum(30 // tab[:, 1])), n), dtype=int)
    results = []
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
            c[i] += 1
            i = 0
        else:
            c[i] = 0
            i += 1
    
    # return np.array(results)
    return np.array(results), np.array(timings), np.array(delays)


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
    
    x = np.arange(0, 45)
    labels = np.array([f"task {tab.shape[0] - i}" for i in range(tab.shape[0])])
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
            
            y[start_task:end_task] = 3 - task_i

            mask[end_task:end_pause] = False

        mask[end_pause:] = False
            
        width = np.full_like(x, .91, dtype=float)
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


def show_schedual(permutation, timing):
    plt.figure(figsize=(16, 3))
    
    x = np.arange(0, 45)
    labels = np.array([f"task {tab.shape[0] - i}" for i in range(tab.shape[0])])
    
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
        
        y[start_task:end_task] = 3 - task_i

        mask[end_task:end_pause] = False
        
    mask[end_pause:] = False
        
    width = np.full_like(x, .91, dtype=float)
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
tab = np.array([[2, 10],
                [3, 10],
                [2, 20],
                [3, 40]])

task = get_one_permutation(tab)


if not is_scheduable(tab[:, 0], tab[:, 1]):
    raise ValueError("Tab is not scheduable !!")

# task = np.array([11, 12, 21], dtype='int16')

valid_perm, timings, delays = all_permutations(task)
# valid_perm = valid_permutations(permutations)


# for perm in permutations:
#     print(perm)


print()
print(valid_perm.shape[0], "valid permutations. \n")


min_arg = np.argmin(delays)
n = len(np.where(delays == delays[min_arg]))

print("minimum delay:", delays[min_arg])
print(f"There is {n} best schedual.")
print(f"permutation n°{min_arg}:", valid_perm[min_arg])

show_schedual(valid_perm[min_arg], timings[min_arg])


end_clock = time.time()

print("Run time:", end_clock - start_clock)
