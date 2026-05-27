#include "common.h"
#include <vector>
#include <chrono>

OtsuResult run_otsu_cpu(const unsigned char* image_in, unsigned char* image_out, int width, int height) {
    OtsuResult result;
    int total_pixels = width * height;

    auto t_start = std::chrono::high_resolution_clock::now();

    // 1. Calculate Histogram
    auto t0 = std::chrono::high_resolution_clock::now();
    std::vector<int> histogram(256, 0);
    for (int i = 0; i < total_pixels; ++i) {
        histogram[image_in[i]]++;
    }
    auto t1 = std::chrono::high_resolution_clock::now();
    result.time_histogram_ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

    // 2. Calculate Otsu Threshold
    t0 = std::chrono::high_resolution_clock::now();
    float sum = 0;
    for (int i = 0; i < 256; ++i) {
        sum += i * histogram[i];
    }

    float sumB = 0;
    int wB = 0;
    int wF = 0;

    float varMax = 0;
    int threshold = 0;

    for (int i = 0; i < 256; ++i) {
        wB += histogram[i];
        if (wB == 0) continue;

        wF = total_pixels - wB;
        if (wF == 0) break;

        sumB += (float)(i * histogram[i]);

        float mB = sumB / wB;
        float mF = (sum - sumB) / wF;

        float varBetween = (float)wB * (float)wF * (mB - mF) * (mB - mF);

        if (varBetween > varMax) {
            varMax = varBetween;
            threshold = i;
        }
    }
    result.threshold = threshold;
    t1 = std::chrono::high_resolution_clock::now();
    result.time_threshold_ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

    // 3. Apply Threshold
    t0 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < total_pixels; ++i) {
        image_out[i] = (image_in[i] >= threshold) ? 255 : 0;
    }
    t1 = std::chrono::high_resolution_clock::now();
    result.time_apply_ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

    auto t_end = std::chrono::high_resolution_clock::now();
    result.time_total_ms = std::chrono::duration<double, std::milli>(t_end - t_start).count();

    return result;
}
