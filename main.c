#include <stdio.h>
#include <stdlib.h>


//TODO: all_permutation()
struct permutation {
    int* seq;
    int* timing;
    int delay;
    struct permutation* next;
} ;


int factorial(int n);
int sum(int seq[], int start, int end);

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


#define DEBUG 1
#define SIZE 3

int main() {
    int tab[SIZE][2] = {
            {2, 10},
            {3, 10},
            {3, 40}
    };


#if DEBUG==1
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
    int* a = get_one_permutation(tab);
    show_seq(a, get_length(tab));
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
        length += 40 / tab[i][1];
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
        for (int i=1 ; i<=40 / T ; i++) seq[index++] = 10 * (line+1) + i;
    }

    return seq;
}

struct permutation* all_permutations(int tab[][2]) {
    return NULL;
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