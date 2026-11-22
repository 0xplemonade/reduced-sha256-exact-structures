#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _OPENMP
#include <omp.h>
#endif

enum { WORD_BITS = 32 };
static const uint64_t DOMAIN = UINT64_C(1) << WORD_BITS;
static const uint64_t BITSET_WORDS = (UINT64_C(1) << WORD_BITS) / 64;

static inline uint32_t rotr32(uint32_t x, unsigned n) {
    return (x >> n) | (x << (32 - n));
}

static inline uint32_t s0(uint32_t x) {
    return rotr32(x, 7) ^ rotr32(x, 18) ^ (x >> 3);
}

static inline uint32_t s1(uint32_t x) {
    return rotr32(x, 17) ^ rotr32(x, 19) ^ (x >> 10);
}

static inline void bitset_add(uint64_t *set, uint32_t value) {
    set[value >> 6] |= UINT64_C(1) << (value & 63);
}

static inline int bitset_has(const uint64_t *set, uint32_t value) {
    return (int)((set[value >> 6] >> (value & 63)) & 1);
}

static uint64_t bitset_count(const uint64_t *set) {
    uint64_t total = 0;
    #pragma omp parallel for reduction(+:total) schedule(static)
    for (uint64_t i = 0; i < BITSET_WORDS; ++i)
        total += (uint64_t)__builtin_popcountll(set[i]);
    return total;
}

/* Build the inverse of s1 as two 16-bit lookup tables.  The construction
   starts from the 32x32 matrix of s1 and row-reduces [matrix | identity]. */
static void build_s1_inverse_tables(uint32_t **lo_out, uint32_t **hi_out) {
    uint64_t row[32] = {0};
    for (unsigned r = 0; r < 32; ++r) {
        uint32_t coeff = 0;
        for (unsigned c = 0; c < 32; ++c)
            coeff |= ((s1(UINT32_C(1) << c) >> r) & 1U) << c;
        row[r] = (uint64_t)coeff | (UINT64_C(1) << (32 + r));
    }
    for (unsigned c = 0; c < 32; ++c) {
        unsigned p = c;
        while (p < 32 && !((uint32_t)row[p] & (UINT32_C(1) << c))) ++p;
        if (p == 32) {
            fputs("s1 matrix is singular\n", stderr);
            exit(2);
        }
        uint64_t tmp = row[c]; row[c] = row[p]; row[p] = tmp;
        for (unsigned r = 0; r < 32; ++r)
            if (r != c && ((uint32_t)row[r] & (UINT32_C(1) << c))) row[r] ^= row[c];
    }

    uint32_t inv_col[32] = {0};
    for (unsigned r = 0; r < 32; ++r) {
        uint32_t inv_row = (uint32_t)(row[r] >> 32);
        for (unsigned c = 0; c < 32; ++c)
            inv_col[c] |= ((inv_row >> c) & 1U) << r;
    }

    uint32_t *lo = calloc(UINT64_C(1) << 16, sizeof(*lo));
    uint32_t *hi = calloc(UINT64_C(1) << 16, sizeof(*hi));
    if (!lo || !hi) { fputs("inverse table allocation failed\n", stderr); exit(2); }
    for (uint32_t v = 1; v < (UINT32_C(1) << 16); ++v) {
        uint32_t b = (uint32_t)__builtin_ctz(v);
        uint32_t rest = v & (v - 1);
        lo[v] = lo[rest] ^ inv_col[b];
        hi[v] = hi[rest] ^ inv_col[b + 16];
    }
    *lo_out = lo;
    *hi_out = hi;
}

static inline uint32_t inv_s1(uint32_t y, const uint32_t *lo, const uint32_t *hi) {
    return lo[y & 0xffffU] ^ hi[y >> 16];
}

int main(int argc, char **argv) {
    const int r37 = argc == 2 && strcmp(argv[1], "r37") == 0;
    if (argc > 2 || (argc == 2 && !r37 && strcmp(argv[1], "r38") != 0)) {
        fprintf(stderr, "usage: %s [r38|r37]\n", argv[0]);
        return 2;
    }
    const char *arm = r37 ? "public-r37" : "shifted-public-r38";
    const uint32_t p = r37 ? UINT32_C(0x0000a000) : UINT32_C(0x00028000);
    const uint32_t g = r37 ? UINT32_C(0xfdffc000) : UINT32_C(0x07ff0000);
    const uint32_t d8 = r37 ? UINT32_C(0xd0007c70) : UINT32_C(0);
    const uint32_t terminal_target = r37 ? UINT32_C(1) : UINT32_C(4);
    uint64_t *row24_image = calloc(BITSET_WORDS, sizeof(*row24_image));
    uint64_t *w39_d37_image = calloc(BITSET_WORDS, sizeof(*w39_d37_image));
    uint32_t *inv_lo = NULL, *inv_hi = NULL;
    if (!row24_image || !w39_d37_image) {
        fputs("bitset allocation failed\n", stderr);
        return 2;
    }
    build_s1_inverse_tables(&inv_lo, &inv_hi);

    /* Exact row-24 image: every D_s0(W9,p). */
    for (uint64_t i = 0; i < DOMAIN; ++i) {
        uint32_t x = (uint32_t)i;
        bitset_add(row24_image, s0(x + p) - s0(x));
    }

    /* Exact W39-compatible dW37 image.  D_s1(x,d)=terminal_target iff
       d = inv_s1(s1(x)+terminal_target)-x. */
    for (uint64_t i = 0; i < DOMAIN; ++i) {
        uint32_t x = (uint32_t)i;
        uint32_t d = inv_s1(s1(x) + terminal_target, inv_lo, inv_hi) - x;
        bitset_add(w39_d37_image, d);
    }

    /* Sanity-check the generated inverse on a fixed, spread-out sample. */
    uint64_t inverse_failures = 0;
    for (uint64_t i = 0; i < DOMAIN; i += UINT64_C(0x01010101)) {
        uint32_t x = (uint32_t)i;
        inverse_failures += inv_s1(s1(x), inv_lo, inv_hi) != x;
    }

    uint64_t row24_w22_count = 0;
    uint64_t w39_w22_count = 0;
    uint64_t compatible_w22_count = 0;
    uint64_t first = UINT64_MAX;

    #pragma omp parallel for reduction(+:row24_w22_count,w39_w22_count,compatible_w22_count) reduction(min:first) schedule(static)
    for (uint64_t i = 0; i < DOMAIN; ++i) {
        uint32_t w22 = (uint32_t)i;
        uint32_t row24_need = -(s1(w22 + g) - s1(w22)) - d8;
        uint32_t d37 = s0(w22 + g) - s0(w22);
        int a = bitset_has(row24_image, row24_need);
        int b = bitset_has(w39_d37_image, d37);
        row24_w22_count += (uint64_t)a;
        w39_w22_count += (uint64_t)b;
        compatible_w22_count += (uint64_t)(a && b);
        if (a && b && i < first) first = i;
    }

    printf("{\n");
    printf("  \"arm\": \"%s\",\n", arm);
    printf("  \"dW9\": \"%08" PRIx32 "\",\n", p);
    printf("  \"dW22\": \"%08" PRIx32 "\",\n", g);
    printf("  \"dW8\": \"%08" PRIx32 "\",\n", d8);
    printf("  \"terminal_D_s1_target\": \"%08" PRIx32 "\",\n", terminal_target);
    printf("  \"row24_derivative_image_size\": %" PRIu64 ",\n", bitset_count(row24_image));
    printf("  \"w39_eligible_dW37_image_size\": %" PRIu64 ",\n", bitset_count(w39_d37_image));
    printf("  \"W22_passing_row24_exists\": %" PRIu64 ",\n", row24_w22_count);
    printf("  \"W22_passing_W39_derivative_exists\": %" PRIu64 ",\n", w39_w22_count);
    printf("  \"W22_passing_both\": %" PRIu64 ",\n", compatible_w22_count);
    printf("  \"first_W22_passing_both\": ");
    if (first == UINT64_MAX) printf("null,\n");
    else printf("\"%08" PRIx64 "\",\n", first);
    printf("  \"inverse_sample_failures\": %" PRIu64 "\n", inverse_failures);
    printf("}\n");

    free(inv_lo); free(inv_hi); free(row24_image); free(w39_d37_image);
    return inverse_failures ? 1 : 0;
}
