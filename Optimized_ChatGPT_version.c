#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <limits.h>

#define TASKS 6

// Data structure for storing a valid permutation
typedef struct permutation {
    int* seq;             // sequence of task occurrences
    int* timing;          // timing array (2*length + 2)
    int delay;            // total delay
    struct permutation* next;
} permutation;

// Utility functions
int sum_array(int arr[], int start, int end);
int max_period(int tab[][2]);
float is_schedulable(int tab[][2], int size);
int is_valid(int seq[], int size);
int* get_timing(int tab[][2], int seq[], int size);
int get_length(int tab[][2]);
int* get_initial_sequence(int tab[][2]);

// Linked-list management
permutation* create_permutation(int* seq, int* timing, int delay);
void append_permutation(permutation** head_ref, permutation* new_node);
int count_permutations(permutation* head);
void free_permutation_list(permutation* head);

// Output
void print_permutation_nicely(permutation* head, int size);
int min_delay(permutation* head);
permutation* min_delay_permutations(permutation* head, int best_delay);

// Swap helper
static void swap_int(int* a, int* b) {
    int t = *a; *a = *b; *b = t;
}

// Backtracking permutation generator with prefix pruning
static void permute_dfs(int index, int* seq, int length, int tab[][2], permutation** head) {
    if (index == length) {
        // Full sequence generated
        int* timing = get_timing(tab, seq, length);
        if (timing[2*length + 1]) {
            int delay = timing[2*length];
            int* seq_copy = malloc(sizeof(int) * length);
            memcpy(seq_copy, seq, sizeof(int) * length);
            permutation* node = create_permutation(seq_copy, timing, delay);
            append_permutation(head, node);
        } else {
            free(timing);
        }
        return;
    }
    for (int i = index; i < length; i++) {
        swap_int(&seq[index], &seq[i]);
        // Prune: only proceed if current prefix is valid
        if (is_valid(seq, index + 1)) {
            permute_dfs(index + 1, seq, length, tab, head);
        }
        swap_int(&seq[index], &seq[i]);
    }
}

// Generate all valid permutations using DFS + pruning
permutation* all_permutations(int tab[][2]) {
    permutation* head = NULL;
    int length = get_length(tab);
    int* seq = get_initial_sequence(tab);
    permute_dfs(0, seq, length, tab, &head);
    free(seq);
    return head;
}

int main(void) {
    int tab[TASKS][2] = {
            {2, 10},
            {3, 10},
            {2, 20},
            {2, 20},
            {2, 40},
            {2, 40}
    };
    clock_t start = clock();
    float util = is_schedulable(tab, TASKS);
    if (util > 1.0f) {
        printf("Not schedulable (utilization = %.3f)\n", util);
        return EXIT_FAILURE;
    }
    permutation* all = all_permutations(tab);
    int total = count_permutations(all);
    printf("%d valid permutations generated.\n", total);
    int best = min_delay(all);
    printf("Minimum delay: %d\n", best);
    permutation* best_list = min_delay_permutations(all, best);
    printf("%d permutations achieve minimum delay.\n", count_permutations(best_list));
    print_permutation_nicely(best_list, get_length(tab));
    free_permutation_list(all);
    double elapsed = (double)(clock() - start) / CLOCKS_PER_SEC;
    printf("\nExecution time: %.5f s\n", elapsed);
    return 0;
}

// -------------------- Utility Implementations --------------------
int sum_array(int arr[], int start, int end) {
    int s = 0; for (int i = start; i < end; i++) s += arr[i]; return s;
}
int max_period(int tab[][2]) {
    int m = 0; for (int i = 0; i < TASKS; i++) if (tab[i][1] > m) m = tab[i][1]; return m;
}
float is_schedulable(int tab[][2], int size) {
    float u = 0; for (int i = 0; i < size; i++) u += (float)tab[i][0]/tab[i][1]; return u;
}
int is_valid(int seq[], int size) {
    for (int i = 0; i < size; i++) {
        int ti = seq[i]/10, oi = seq[i]%10;
        for (int j = 0; j < i; j++)
            if (seq[j]/10 == ti && seq[j]%10 > oi) return 0;
    }
    return 1;
}
int* get_timing(int tab[][2], int seq[], int size) {
    int full = 2*size+2, di = 2*size, ok = 2*size+1;
    int* timing = calloc(full, sizeof(int));
    int* passed = calloc(TASKS, sizeof(int)); if (!timing||!passed) exit(EXIT_FAILURE);
    int idx = 0, miss5 = 0;
    for (int c = 0; c < size; c++) {
        int code = seq[c], t = code/10-1, o = code%10;
        int per = tab[t][1], cnt = tab[t][0];
        int start_norm = per*(o-1), end_norm = start_norm+per;
        if (passed[t]) {
            while (idx%per) { timing[2*c-1]++; idx++; for (int k=0;k<TASKS;k++) if (!(idx%tab[k][1])) passed[k]=0; }
            passed[t]=0;
        }
        passed[t]=1;
        for (int e=0;e<cnt;e++){ timing[2*c]++; idx++; for(int k=0;k<TASKS;k++) if(!(idx%tab[k][1])) passed[k]=0; }
        int real_s = sum_array(timing,0,2*c), real_e = real_s+timing[2*c];
        if(real_s<start_norm||(real_e> end_norm&&(t!=TASKS-1||miss5++))) { timing[ok]=0; free(passed); return timing; }
        timing[di]+=real_s-start_norm;
    }
    timing[ok]=1; free(passed); return timing;
}
int get_length(int tab[][2]){
    int h=max_period(tab), len=0; for(int i=0;i<TASKS;i++) len+=h/tab[i][1]; return len;
}
int* get_initial_sequence(int tab[][2]){
    int len=get_length(tab), *seq=malloc(sizeof(int)*len), idx=0, h=max_period(tab);
    for(int t=0;t<TASKS;t++){ int occ=h/tab[t][1]; for(int o=1;o<=occ;o++) seq[idx++]=10*(t+1)+o; }
    return seq;
}
permutation* create_permutation(int* seq,int* timing,int delay){
    permutation* p=malloc(sizeof(*p)); if(!p) exit(EXIT_FAILURE);
    p->seq=seq; p->timing=timing; p->delay=delay; p->next=NULL; return p;
}
void append_permutation(permutation** h, permutation* n){ if(!*h){*h=n;return;} permutation* c=*h; while(c->next)c=c->next; c->next=n; }
int count_permutations(permutation* h){int c=0;while(h){c++;h=h->next;}return c;}
void free_permutation_list(permutation* h){ while(h){ permutation* t=h;h=h->next; free(t->seq); free(t->timing); free(t);} }
void print_permutation_nicely(permutation* h,int sz){int i=1;while(h){ printf("Perm %2d: [",i++); for(int j=0;j<sz;j++) printf(" %d",h->seq[j]); printf(" ] Delay: %d\n",h->delay); h=h->next;} }
int min_delay(permutation* h){int m=INT_MAX;while(h){if(h->delay<m)m=h->delay;h=h->next;}return m;}
permutation* min_delay_permutations(permutation* h,int d){permutation* f=NULL; while(h){ if(h->delay==d){ append_permutation(&f, create_permutation(h->seq,h->timing,h->delay)); } h=h->next;} return f;}
