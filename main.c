#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


//TODO: all_permutation()
struct permutation {
    int* seq;
    int* timing;
    int delay;
    struct permutation* next;
} ;


int factorial(int n);
int sum(int seq[], int start, int end);
int maxT(int tab[][2]);

void show_seq(int seq[], const int size);

float is_scheduable(int tab[][2], const int size);
int is_valid(int seq[], const int size);
int* get_timing(int tab[][2], int seq[], const int size);

int get_length(int tab[][2]);
int* get_one_permutation(int tab[][2]);
struct permutation* all_permutations(int tab[][2]);

int count_permutations(struct permutation* head);
void append_permutation(struct permutation** head_ref, struct permutation* new_node);
struct permutation* create_permutation(int* seq, int* timing, int delay);
void free_permutation_list(struct permutation* head);

void print_permutation_list(struct permutation* head, int size);
void print_permutation_nicely(struct permutation* head, int size);

int min_delay(struct permutation* head);
struct permutation* min_delay_permutations(struct permutation* head, int min_delay);


#define DEBUG 0
#define SIZE 6

int main() {
    int tab[SIZE][2] = {
            {2, 10},
            {3, 10},
            {2, 20},
            {2, 20},
            {2, 40},
            {2, 40}
    };


#if DEBUG
    printf("Running debug...\n\n");
    int seq_size = 7;
    int arr1[] = {11, 31, 21, 12, 22, 13, 23};
    int arr2[] = {21, 11, 12, 22, 31, 13, 23};
    int arr3[] = {11, 31, 22, 12, 21, 13, 23};

    printf("%s: %.3f\n", is_scheduable(tab, SIZE)? "Is scheduable": "Is not scheduable", is_scheduable(tab, SIZE));

    printf("arr1 validity: %s\n", (is_valid(arr1, seq_size))? "True": "False");
    printf("arr2 validity: %s\n", (is_valid(arr2, seq_size))? "True": "False");
    printf("arr3 validity: %s\n", (is_valid(arr3, seq_size))? "True": "False");
    printf("---------------------------\n");
    int* timing1 = get_timing(tab, arr1, seq_size);
    int delay1 = timing1[seq_size*2];
    int is_ok1 = timing1[seq_size*2 + 1];
    printf("arr1 timing: "); show_seq(timing1, seq_size*2);
    printf("arr1 delay: %d\n", delay1);
    printf("arr1 is_ok?: %s\n", is_ok1? "True": "False");

    printf("---------------------------\n");

    int* timing2 = get_timing(tab, arr2, seq_size);
    int delay2 = timing2[seq_size*2];
    int is_ok2 = timing2[seq_size*2 + 1];
    printf("arr2 timing: "); show_seq(timing2, seq_size*2);
    printf("arr2 delay: %d\n", delay2);
    printf("arr2 is_ok?: %s\n", is_ok2? "True": "False");

    printf("---------------------------\n");

    int* timing3 = get_timing(tab, arr3, seq_size);
    int delay3 = timing3[seq_size*2];
    int is_ok3 = timing3[seq_size*2 + 1];
    printf("arr3 timing: "); show_seq(timing3, seq_size*2);
    printf("arr3 delay: %d\n", delay3);
    printf("arr3 is_ok?: %s\n", is_ok3? "True": "False");

    printf("---------------------------\n");

    printf("max is %d\n", maxT(tab));
#else
    clock_t start, end;
    double time_used;

    start = clock();

    if (is_scheduable(tab, SIZE) > 1.0f) {
        printf("tab is Not Scheduable: %.3lf", is_scheduable(tab, SIZE));
        return 0;
    }

    short int seq_size = get_length(tab);
    struct permutation* head = all_permutations(tab);



    printf("%d valid permutations.\n", count_permutations(head));

    int best_delay = min_delay(head);
    printf("Best delay is %d\n", best_delay);

    struct permutation* best_permutations = min_delay_permutations(head, best_delay);
    printf("%d equivalent best permutations.\n", count_permutations(best_permutations));


    print_permutation_nicely(best_permutations, get_length(tab));
    free_permutation_list(head);
    end = clock();
    time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("\nRunning time: %.5lf s\n", time_used);
#endif
    return 0;
}

// ---------------------------------------------------------------------------------------------------------------------
int factorial(int n) {
    if (n <= 1) return 1;
    else return n * factorial(n - 1);
}


int sum(int seq[], int start, int end) {
    int s = 0;
    for (int i=start ; i<end ; i++) s += seq[i];
    return s;
}


int maxT(int tab[][2]) {
    int max = 0;
    for (int i=0 ; i<SIZE ; i++) {
        if (max < tab[i][1]) max = tab[i][1];
    }
    return max;
}


void show_seq(int seq[], const int size) {
    printf("[ ");
    for (int i = 0; i < size; i++) printf("%d ", seq[i]);
    printf("]\n");
}


float is_scheduable(int tab[][2], const int size) {
    float sum = 0.0f;
    for (int i = 0; i < size; i++) {
        sum += (float)tab[i][0] / (float)tab[i][1];
    }
    return sum;
}


int is_valid(int seq[], const int size) {
    for (int i=0 ; i<size ; i++) {
        int task_i = seq[i] / 10;
        int occ_i = seq[i] % 10;
        for (int j=0 ; j<i ; j++) {
            int task_j = seq[j] / 10;
            int occ_j = seq[j] % 10;
            if (task_i == task_j  && occ_i < occ_j) return 0;
        }
    }
    return 1;
}


int* get_timing(int tab[][2], int seq[], const int size) {
    const int full_size = size * 2 + 2;
    const int delay_index = 2*size;
    const int is_ok_index = 2*size + 1;

    int* timing = (int*)malloc(sizeof(int) * full_size);
    int* did_pass = (int*)malloc(sizeof(int) * SIZE);

    if (timing == NULL) return NULL;
    if (did_pass == NULL) return NULL;

    for (int i = 0; i < full_size; i++) timing[i] = 0; // initialize to zero
    for (int i=0 ; i<SIZE ; i++) did_pass[i] = 0; // initialize to False

    int delay = 0;
    int idx = 0;
    for (int c_index=0 ; c_index<size ; c_index++) {
        int c = seq[c_index];

        int task_i = c / 10 - 1;
        int occ_i = c % 10;

        int normal_start = tab[task_i][1] * (occ_i-1);
        int normal_end = normal_start + tab[task_i][1];

        int count = tab[task_i][0];
        if (did_pass[task_i]) {
            while (idx % tab[task_i][1] != 0) {
                timing[2*c_index-1]++;
                idx++;

                // for pos in np.argwhere(idx % tab[:, 1] == 0):
                for (int i = 0; i < SIZE; i++) {
                    if (idx % tab[i][1] == 0) {
                        did_pass[i] = 0;
                    }
                }
            }
            did_pass[task_i] = 0;
        }

        did_pass[task_i] = 1;
        for (int i=0 ; i<count ; i++) {
            timing[2*c_index]++;
            idx++;

            // for pos in np.argwhere(idx % tab[:, 1] == 0):
            for (int i = 0; i < SIZE; i++) {
                if (idx % tab[i][1] == 0) {
                    did_pass[i] = 0;
                }
            }
        }

        int real_start = sum(timing, 0, 2*c_index);
        int real_end = real_start + timing[2*c_index];

        if (real_start < normal_start || real_end > normal_end) {
            timing[is_ok_index] = 0;
            return timing;
        }

        timing[delay_index] += real_start - normal_start;
    }
    timing[is_ok_index] = 1;
    return timing;
}


int get_length(int tab[][2]) {
    int length = 0;
    for (int i=0 ; i<SIZE ; i++) {
        length += maxT(tab) / tab[i][1];
    }
    return length;
}


int* get_one_permutation(int tab[][2]) {
    int length = get_length(tab);
    int* seq = (int*) malloc((sizeof(int) * length));
    if (seq == NULL) return NULL;

    short int index = 0;
    for (int line=0 ; line<SIZE ; line++) {
        int T = tab[line][1];
        for (int i=1 ; i<=maxT(tab) / T ; i++) seq[index++] = 10 * (line+1) + i;
    }

    return seq;
}


struct permutation* all_permutations(int tab[][2]) {
    struct permutation* head = NULL;

    int* seq = get_one_permutation(tab);
    int length = get_length(tab);

    short int c[length];
    for (int i=0 ; i<length ; i++) c[i] = 0;

    // short index = 0;
    if (is_valid(seq, length)) {
        int* timing = get_timing(tab, seq, length);

        if (timing[2*length + 1]) {
            int delay = timing[2*length];

            int* seq_copy = (int*)malloc(sizeof(int) * length);
            memcpy(seq_copy, seq, sizeof(int) * length);

            struct permutation* new = create_permutation(seq_copy, timing, delay);
            append_permutation(&head, new);

        } else free(timing);
    }
    int i = 0;
    while (i < length) {
        if (c[i] < i) {
            short int swap_idx = 0;
            if (i%2 != 0) swap_idx = c[i];

            int temp = seq[i];
            seq[i] = seq[swap_idx];
            seq[swap_idx] = temp;

            if (is_valid(seq, length)) {
                int* timing = get_timing(tab, seq, length);

                if (timing[2*length + 1]) {
                    int delay = timing[2*length];

                    int* seq_copy = (int*)malloc(sizeof(int) * length);
                    memcpy(seq_copy, seq, sizeof(int) * length);

                    struct permutation* new = create_permutation(seq_copy, timing, delay);
                    append_permutation(&head, new);

                } else free(timing);
            }
            c[i]++;
            i = 0;
        }
        else {
            c[i] = 0;
            i++;
        }
    }

    return head;
}


// liked list functions ----------------------------------------------------------------
int count_permutations(struct permutation* head) {
    int count = 0;
    while (head != NULL) {
        count++;
        head = head->next;
    }
    return count;
}


void append_permutation(struct permutation** head_ref, struct permutation* new_node) {
    if (*head_ref == NULL) {
        *head_ref = new_node;
        return;
    }

    struct permutation* current = *head_ref;
    while (current->next != NULL) {
        current = current->next;
    }
    current->next = new_node;
}


struct permutation* create_permutation(int* seq, int* timing, int delay) {
    struct permutation* new_node = (struct permutation*)malloc(sizeof(struct permutation));
    if (!new_node) return NULL;

    new_node->seq = seq;
    new_node->timing = timing;
    new_node->delay = delay;
    new_node->next = NULL;

    return new_node;
}


void free_permutation_list(struct permutation* head) {
    while (head != NULL) {
        struct permutation* temp = head;
        head = head->next;

        free(temp->seq);
        free(temp->timing);
        free(temp);
    }
}


void print_permutation_list(struct permutation* head, int size) {
    int index = 0;
    while (head != NULL) {
        printf("Permutation %d: delay = %d\n", index++, head->delay);
        printf("  seq: ");
        for (int i = 0; i < size; i++) {
            printf("%d ", head->seq[i]);
        }
        printf("\n  timing: ");
        for (int i = 0; i < size * 2; i++) {
            printf("%d ", head->timing[i]);
        }
        printf("\n");

        head = head->next;
    }
}


void print_permutation_nicely(struct permutation* head, int size) {
    int index = 0;
    while (head != NULL) {
        printf("Permutation %2d: [ ", ++index);
        for (int i = 0; i < size; i++) {
            printf("%d ", head->seq[i]);
        }
        printf("]");
        printf("\tdelay = %d\t", head->delay);
        printf("\n");

        head = head->next;
    }
}


int min_delay(struct permutation* head) {
    int min = INT_MAX;
    struct permutation* current = head;
    while (current != NULL) {
        if (current->delay < min) min = current->delay;
        current = current->next;
    }
    return min;
}


struct permutation* min_delay_permutations(struct permutation* head, int min_delay) {
    struct permutation* filtered_head = NULL;
    struct permutation* current = head;

    while (current != NULL) {
        if (current->delay == min_delay) {
            // Make deep copies of seq and timing
            //int* seq_copy = (int*)malloc(sizeof(int) * get_length_from_timing(current->timing)); // assume length can be inferred
            //memcpy(seq_copy, current->seq, sizeof(int) * get_length_from_timing(current->timing));

            //int timing_len = get_timing_length(current->timing); // must return 2*length+2
            //int* timing_copy = (int*)malloc(sizeof(int) * timing_len);
            //memcpy(timing_copy, current->timing, sizeof(int) * timing_len);

            struct permutation* new_perm = create_permutation(current->seq, current->timing, current->delay);
            append_permutation(&filtered_head, new_perm);
        }

        current = current->next;
    }

    return filtered_head;
}
