import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm



def factorial(n):
    return n if n ==1 else n * factorial(n-1)


def is_valid(C, T):
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
def all_permutations(task):
    a = task
    n = len(a)
    
    c = [0] * n
    
    results = np.zeros((factorial(sum(30 // tab[:, 1])), n), dtype=int)
    results[0, :] = a.copy()
    index = 1
    
    i = 0
    while i < n:
        if c[i] < i:
            swap_idx = 0 if i%2 == 0 else c[i]
            temp = a[i]
            a[i] = a[swap_idx]
            a[swap_idx] = temp
            results[index] = a.copy()
            index += 1
            c[i] += 1
            i = 0
        else:
            c[i] = 0
            i += 1
    
    return np.array(results)
    


def valid_permutations(permutations):
    col = permutations.shape[1]
    lin = count_valid(30 // tab[:, 1])
    # print(col, lin)
    valid = np.zeros((lin, col), dtype=int)
    
    index = 0
    for perm in tqdm(permutations):
        ok = True
        
        for i in range(col):
            for j in range(i):
                task_i, occ_i = divmod(perm[i], 10)
                task_j, occ_j = divmod(perm[j], 10)
                
                # if same task but a later occurrence appears before an earlier one → invalid
                if task_i == task_j and occ_i < occ_j:
                    ok = False
                    break
                
            if not ok:
                break
            
        if ok:
            valid[index] = perm
            index += 1
            
    return valid


def get_one_permutation(tab):
    task = []
    maximum = np.max(tab[:, 1])
    
    for line in range(tab.shape[0]):
        t = tab[line, 1]
        for i in range(maximum // t):
            task.append(10 * (line+1) + (i+1))
    return np.array(task)

# %% showing functions

def show_schedual_test(timed_permutation, n=8, search=0):
    fig, axes = plt.subplots(n, 1, figsize=(16, 1.17*n), sharex=False)
    
    x = np.arange(0, timed_permutation.shape[1])
    labels = np.array([f"task {tab.shape[0] - i}" for i in range(tab.shape[0])])
    current_perm_index = n*search
    for ax, current in zip(axes, timed_permutation[n*search:n*(search+1)]):
        labels_bar = []

        mask = np.ones(len(x), dtype=bool)
        
        for i in range(len(current)):
            if current[i] == 0:
                mask[i] = False
            else:
                current[i] = 5 - current[i]
            
        width = np.full_like(x, .93, dtype=float)
        ax.barh(current[mask]-1, width[mask], left=x[mask], color = 'red', edgecolor = 'red', align='center', height=1)
        
        for xi, yi, lbl in zip(x, current, labels_bar): # annotate each bar
            ax.text(xi + 0.93/2, yi, lbl, va='center', ha='center', color='white', fontsize=8)
        
        ax.set_yticks(np.arange(len(labels)))
        ax.set_yticklabels(labels)
        ax.set_xlim(0, len(x))
        ax.grid(True, alpha=.2, linestyle="-.", )
        ax.set_title(f"Permutation: {valid_perm[current_perm_index]}")
        # print(y)
        current_perm_index += 1
        
    plt.tight_layout()
    plt.show()
    return None


def show_scheduals(permutations, timings, n=8, search=0):
    fig, axes = plt.subplots(n, 1, figsize=(16, 2.17*n), sharex=False)
    
    x = np.arange(0, 31)
    labels = np.array([f"task {tab.shape[0] - i}" for i in range(tab.shape[0])])
    current_perm_index = n*search
    for ax, current in zip(axes, permutations[n*search:n*(search+1)]):
        labels_bar = []

        mask = np.ones(len(x), dtype=bool)
        y = np.zeros_like(x)
        # print("-"*5, current, "-"*5)
        for i in range(len(current)):
            
            task_i, occ_i = divmod(current[i], 10)
            task_i -= 1 # en indice
            
            start_task = sum(timings[current_perm_index, :2*i])
            end_task = start_task + timings[current_perm_index, 2*i]
            end_pause = end_task + timings[current_perm_index, 2*i+1]
            
            y[start_task:end_task] = 4 - task_i

            mask[end_task:end_pause] = False

            # print(f"task{task_i+1}", tab[task_i, 0], timings[current_perm_index, 2*i])
            # print(end_task - start_task, end_pause - end_task)
            # print(y[start_task:end_pause])
        mask[end_pause:] = False
        
        
        # for i in range(len(current)):
        #     if current[i] == 0:
        #         mask[i] = False
        #     else:
        #         current[i] = 5 - current[i]
            
        width = np.full_like(x, .91, dtype=float)
        ax.barh(y[mask]-1, width[mask], left=x[mask], color = 'red', edgecolor = 'red', align='center', height=1)
        
        # for xi, yi, lbl in zip(x, current, labels_bar): # annotate each bar
        #     ax.text(xi + 0.91/2, yi, lbl, va='center', ha='center', color='white', fontsize=8)
        
        ax.set_yticks(np.arange(len(labels)))
        ax.set_yticklabels(labels)
        ax.set_xlim(0, len(x))
        ax.grid(True, alpha=.2, linestyle="-.", )
        ax.set_title(f"Permutation: {current}")
        # print(y)
        # if current_perm_index == 5:
        #     break
        current_perm_index += 1
        
        
    plt.tight_layout()
    plt.show()
    return None


def show_schedual(permutation, timing):
    plt.figure(figsize=(16, 3))
    
    x = np.arange(0, 31)
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
        
        y[start_task:end_task] = 4 - task_i

        mask[end_task:end_pause] = False

        # print(f"task{task_i+1}", tab[task_i, 0], timings[current_perm_index, 2*i])
        # print(end_task - start_task, end_pause - end_task)
        # print(y[start_task:end_pause])
    mask[end_pause:] = False
    
    
    # for i in range(len(current)):
    #     if current[i] == 0:
    #         mask[i] = False
    #     else:
    #         current[i] = 5 - current[i]
        
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
tab = np.array([[3, 5],
                [2, 15],
                [3, 30]])

task = get_one_permutation(tab)


if not is_valid(tab[:, 0], tab[:, 1]):
    raise ValueError("Tab is not scheduable !!")

# task = np.array([11, 12, 21], dtype='int16')

permutations = all_permutations(task)
valid_perm = valid_permutations(permutations)


# for perm in permutations:
#     print(perm)


print()
print(valid_perm.shape[0], "valid permutations. \n")
print(valid_perm[:10])
    
        
# %% add timing to tasks


timings = np.zeros((valid_perm.shape[0], valid_perm.shape[1] * 2), dtype=int)


for current_index in range(valid_perm.shape[0]): # valid_perm.shape[0]
    current = valid_perm[current_index]
    did_pass = np.zeros(tab.shape[0], dtype=bool)
    
    
    idx = 0
    for c_index in range(len(current)):
        c = current[c_index]
        # print("c:", c)
        task_i, occ_i = divmod(c, 10)
        task_i -= 1 # make index
        # print(task_i+1, occ_i, "\t", did_pass)
        
        count = tab[task_i, 0]
        if did_pass[task_i]: # déjà passé, doit attendre
            # print(f"task {task_i + 1} already passed")
            while idx%tab[task_i, 1] != 0:
                timings[current_index, 2*c_index-1] += 1
                
                idx += 1
                for pos in np.argwhere(idx % tab[:, 1] == 0):
                    # print("pos :", pos)
                    did_pass[pos] = False
                    
            did_pass[task_i] = False
            
        
        # print(f"task {task_i + 1} not passed yet")

        did_pass[task_i] = True 
        
        for _ in range(count):
            timings[current_index, 2*c_index] += 1
            # print(task_i)
            idx += 1
            for pos in np.argwhere(idx % tab[:, 1] == 0):
                # print("pos :", pos)
                did_pass[pos] = False
        # print(timing[0])


# show_scheduals(valid_perm, timings, 2, search=0)

# %% verify if timing is respected

final_permutations = []
final_timings = []
final_delay = []

lim = 0
for current, timing in zip(valid_perm, timings):
    is_ok = True
    # print(current, '\t', timing)
    # print("-"*30)
    delay = 0
    for i in range(len(current)):
        task_i, occ_i = divmod(current[i], 10)
        task_i -= 1
        # print(task_i, occ_i, "|-|")
        normal_start = tab[task_i, 1] * (occ_i-1)
        normal_end = normal_start + tab[task_i, 1]
        # print(f"task {task_i+1}{occ_i}:", normal_start, normal_end, end='\t')
        real_start = sum(timing[:i*2])
        real_end = real_start + timing[2*i]
        # print(real_start, real_end, end='\n')
        delay += real_start - normal_start
    # if lim == 1:
    #     break
        if real_start < normal_start or real_end > normal_end:
            is_ok = False
            continue
        
    if is_ok:
        final_permutations.append(current)
        final_timings.append(timing)
        final_delay.append(delay)
            
        
    # print()
    lim += 1

# %% show best

final_permutations = np.array(final_permutations)
final_timings = np.array(final_timings)

min_arg = np.argmin(final_delay)

show_schedual(final_permutations[min_arg], final_timings[min_arg])


print(f"permutation n°{min_arg}:", final_permutations[min_arg])
print("delay:", final_delay[min_arg])

# Tableau avec les taches consécutives
# Tableau avec les temps de taches (paire) et temps de pause (impaire)
# un peu comme un truc compressé. comme ça je garde la forme de valid_perm et timed_perm c'est que dans la fonction