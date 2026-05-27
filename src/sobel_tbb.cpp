#include "common.h"
#include <chrono>
#include <cmath>
#include <algorithm>
#include <tbb/parallel_for.h>
#include <tbb/blocked_range2d.h>
#include <tbb/global_control.h>

SobelResult run_sobel_tbb(const unsigned char* image_in, unsigned char* image_out, int width, int height) {
    auto start = std::chrono::high_resolution_clock::now();

    // nr de thread uri folosite de tbb
    int threads_used = tbb::global_control::active_value(tbb::global_control::max_allowed_parallelism);

    // kernel uri sobel
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{1, 2, 1}, {0, 0, 0}, {-1, -2, -1}};

    tbb::parallel_for(tbb::blocked_range2d<int>(1, height - 1, 1, width - 1),
        [&](const tbb::blocked_range2d<int>& r) {
            for (int y = r.rows().begin(); y != r.rows().end(); ++y) {
                for (int x = r.cols().begin(); x != r.cols().end(); ++x) {
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
        });

    // contur
    tbb::parallel_for(tbb::blocked_range<int>(0, width),
        [&](const tbb::blocked_range<int>& r) {
            for (int x = r.begin(); x != r.end(); ++x) {
                image_out[x] = 0;                           // rand sus
                image_out[(height - 1) * width + x] = 0;  // rand jos
            }
        });

    tbb::parallel_for(tbb::blocked_range<int>(0, height),
        [&](const tbb::blocked_range<int>& r) {
            for (int y = r.begin(); y != r.end(); ++y) {
                image_out[y * width] = 0;                   // col st
                image_out[y * width + (width - 1)] = 0;   // col dr
            }
        });

    auto end = std::chrono::high_resolution_clock::now();
    
    SobelResult result;
    result.time_total_ms = std::chrono::duration<double, std::milli>(end - start).count();
    result.threads_used = threads_used;
    
    return result;
}
