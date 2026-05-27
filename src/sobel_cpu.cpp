#include "common.h"
#include <chrono>
#include <cmath>
#include <algorithm>

SobelResult run_sobel_cpu(const unsigned char* image_in, unsigned char* image_out, int width, int height) {
    auto start = std::chrono::high_resolution_clock::now();

    // kernel-uri sobel
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{1, 2, 1}, {0, 0, 0}, {-1, -2, -1}};

    // procesare pixeli interiori
    for (int y = 1; y < height - 1; ++y) {
        for (int x = 1; x < width - 1; ++x) {
            int sum_x = 0;
            int sum_y = 0;

            for (int i = -1; i <= 1; ++i) {
                for (int j = -1; j <= 1; ++j) {
                    int pixel = image_in[(y + i) * width + (x + j)];
                    sum_x += pixel * gx[i + 1][j + 1];
                    sum_y += pixel * gy[i + 1][j + 1];
                }
            }

            int magnitude = std::min(255, (int)std::sqrt(sum_x * sum_x + sum_y * sum_y));
            image_out[y * width + x] = static_cast<unsigned char>(magnitude);
        }
    }

    // contur
    for (int x = 0; x < width; ++x) {
        image_out[x] = 0;                           // randul de sus
        image_out[(height - 1) * width + x] = 0;  // randul de jos
    }
    for (int y = 0; y < height; ++y) {
        image_out[y * width] = 0;                   // coloana st
        image_out[y * width + (width - 1)] = 0;   // coloana dr
    }

    auto end = std::chrono::high_resolution_clock::now();
    
    SobelResult result;
    result.time_total_ms = std::chrono::duration<double, std::milli>(end - start).count();
    result.threads_used = 1;
    
    return result;
}
