#include <inttypes.h>
#include <omp.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define TABLE_BITS 16u
#define TABLE_SIZE (1u << TABLE_BITS)
#define TABLE_MASK (TABLE_SIZE - 1u)
#define DELTA UINT32_C(0x03010000)
#define TARGET UINT32_C(0xc05a1dc0)
#define PUBLIC_W24 UINT32_C(0xcc584832)

typedef struct {
    uint32_t key;
    uint32_t representative;
    uint32_t basis[32];
    uint64_t count;
    unsigned rank;
    unsigned used;
} component;

static inline uint32_t rotr32(uint32_t x, unsigned n) {
    return (x >> n) | (x << (32u - n));
}

static inline uint32_t sigma0(uint32_t x) {
    return rotr32(x, 7) ^ rotr32(x, 18) ^ (x >> 3);
}

static inline uint32_t hash32(uint32_t x) {
    x ^= x >> 16;
    x *= UINT32_C(0x7feb352d);
    x ^= x >> 15;
    x *= UINT32_C(0x846ca68b);
    x ^= x >> 16;
    return x;
}

static component *lookup(component *table, uint32_t key) {
    uint32_t slot = hash32(key) & TABLE_MASK;
    for (;;) {
        if (!table[slot].used || table[slot].key == key) return &table[slot];
        slot = (slot + 1u) & TABLE_MASK;
    }
}

static void insert_vector(component *item, uint32_t value) {
    while (value) {
        const unsigned pivot = 31u - (unsigned)__builtin_clz(value);
        if (item->basis[pivot]) {
            value ^= item->basis[pivot];
        } else {
            item->basis[pivot] = value;
            ++item->rank;
            return;
        }
    }
}

static void add_solution(component *table, uint32_t key, uint32_t value) {
    component *item = lookup(table, key);
    if (!item->used) {
        item->used = 1;
        item->key = key;
        item->representative = value;
        item->count = 1;
        return;
    }
    insert_vector(item, value ^ item->representative);
    ++item->count;
}

static void merge_component(component *table, const component *source) {
    component *target = lookup(table, source->key);
    if (!target->used) {
        target->used = 1;
        target->key = source->key;
        target->representative = source->representative;
    } else {
        insert_vector(target, source->representative ^ target->representative);
    }
    for (unsigned bit = 0; bit < 32; ++bit) {
        if (source->basis[bit]) insert_vector(target, source->basis[bit]);
    }
    target->count += source->count;
}

static void normalize(component *item) {
    for (int pivot = 31; pivot >= 0; --pivot) {
        if (!item->basis[pivot]) continue;
        for (unsigned other = 0; other < 32; ++other) {
            if ((int)other != pivot && (item->basis[other] & (UINT32_C(1) << pivot))) {
                item->basis[other] ^= item->basis[pivot];
            }
        }
        if (item->representative & (UINT32_C(1) << pivot)) {
            item->representative ^= item->basis[pivot];
        }
    }
}

static int verify_component(const component *item) {
    uint32_t vectors[32];
    unsigned n = 0;
    for (unsigned bit = 0; bit < 32; ++bit) {
        if (item->basis[bit]) vectors[n++] = item->basis[bit];
    }
    if (n != item->rank || item->rank >= 63) return 0;
    const uint64_t size = UINT64_C(1) << item->rank;
    if (item->count != size) return 0;

    uint32_t value = item->representative;
    uint64_t previous_gray = 0;
    for (uint64_t index = 0; index < size; ++index) {
        const uint64_t gray = index ^ (index >> 1);
        if (index) {
            const uint64_t changed = gray ^ previous_gray;
            value ^= vectors[(unsigned)__builtin_ctzll(changed)];
        }
        previous_gray = gray;
        const uint32_t right = value + DELTA;
        if ((value ^ right) != item->key) return 0;
        if ((uint32_t)(sigma0(right) - sigma0(value)) != TARGET) return 0;
    }
    return 1;
}

static int by_key(const void *a, const void *b) {
    const component *x = (const component *)a;
    const component *y = (const component *)b;
    return (x->key > y->key) - (x->key < y->key);
}

int main(void) {
    const int threads = omp_get_max_threads();
    component **locals = calloc((size_t)threads, sizeof(*locals));
    if (!locals) return 2;

    #pragma omp parallel
    {
        const int tid = omp_get_thread_num();
        const int nth = omp_get_num_threads();
        component *table = calloc(TABLE_SIZE, sizeof(*table));
        if (!table) abort();
        locals[tid] = table;

        for (uint64_t raw = (uint64_t)tid; raw < (UINT64_C(1) << 32); raw += (uint64_t)nth) {
            const uint32_t left = (uint32_t)raw;
            const uint32_t right = left + DELTA;
            if ((uint32_t)(sigma0(right) - sigma0(left)) == TARGET) {
                add_solution(table, left ^ right, left);
            }
        }
    }

    component *merged = calloc(TABLE_SIZE, sizeof(*merged));
    if (!merged) return 2;
    for (int thread = 0; thread < threads; ++thread) {
        for (uint32_t slot = 0; slot < TABLE_SIZE; ++slot) {
            if (locals[thread][slot].used) merge_component(merged, &locals[thread][slot]);
        }
        free(locals[thread]);
    }
    free(locals);

    size_t strata = 0;
    uint64_t total = 0;
    for (uint32_t slot = 0; slot < TABLE_SIZE; ++slot) {
        if (merged[slot].used) {
            normalize(&merged[slot]);
            if (!verify_component(&merged[slot])) return 4;
            ++strata;
            total += merged[slot].count;
        }
    }

    component *rows = calloc(strata, sizeof(*rows));
    if (!rows) return 2;
    size_t at = 0;
    for (uint32_t slot = 0; slot < TABLE_SIZE; ++slot) {
        if (merged[slot].used) rows[at++] = merged[slot];
    }
    free(merged);
    qsort(rows, strata, sizeof(*rows), by_key);

    const uint32_t public_right = PUBLIC_W24 + DELTA;
    const uint32_t public_mask = PUBLIC_W24 ^ public_right;
    const uint32_t public_derivative = sigma0(public_right) - sigma0(PUBLIC_W24);
    int public_component = -1;
    for (size_t i = 0; i < strata; ++i) {
        uint32_t residual = PUBLIC_W24 ^ rows[i].representative;
        for (int bit = 31; bit >= 0; --bit) {
            if (residual & (UINT32_C(1) << bit)) residual ^= rows[i].basis[bit];
        }
        if (rows[i].key == public_mask && residual == 0) public_component = (int)i;
    }

    printf("{\n");
    printf("  \"threads\": %d,\n", threads);
    printf("  \"delta\": \"%08" PRIx32 "\",\n", DELTA);
    printf("  \"target\": \"%08" PRIx32 "\",\n", TARGET);
    printf("  \"total_solutions\": %" PRIu64 ",\n", total);
    printf("  \"strata\": %zu,\n", strata);
    printf("  \"all_components_verified\": true,\n");
    printf("  \"public\": {\"left\": \"%08" PRIx32 "\", \"right\": \"%08" PRIx32
           "\", \"xor_mask\": \"%08" PRIx32 "\", \"derivative\": \"%08" PRIx32
           "\", \"component_index\": %d},\n",
           PUBLIC_W24, public_right, public_mask, public_derivative, public_component);
    printf("  \"components\": [\n");
    for (size_t i = 0; i < strata; ++i) {
        printf("    {\"xor_mask\": \"%08" PRIx32 "\", \"count\": %" PRIu64
               ", \"rank\": %u, \"representative\": \"%08" PRIx32 "\", \"basis\": [",
               rows[i].key, rows[i].count, rows[i].rank, rows[i].representative);
        unsigned emitted = 0;
        for (unsigned bit = 0; bit < 32; ++bit) {
            if (rows[i].basis[bit]) {
                printf("%s\"%08" PRIx32 "\"", emitted ? ", " : "", rows[i].basis[bit]);
                ++emitted;
            }
        }
        printf("]}%s\n", i + 1 == strata ? "" : ",");
    }
    printf("  ]\n}\n");
    free(rows);
    return public_derivative == TARGET && public_component >= 0 ? 0 : 3;
}
