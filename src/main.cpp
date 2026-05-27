#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <filesystem>
#include <fstream>
#include <algorithm> // Added missing include
#include "common.h"

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

namespace fs = std::filesystem;

void print_results(const std::string& name, const SobelResult& result) {
    std::cout << std::left << std::setw(10) << name
              << std::fixed << std::setprecision(4)
              << std::setw(15) << result.time_total_ms
              << std::endl;
}

void process_image(const fs::path& input_path, const fs::path& output_dir, std::ofstream& csv_file) {
    std::cout << "\n================================================================================\n";
    std::cout << "Processing: " << input_path.filename().string() << std::endl;

    int width, height, channels;
    // Load as grayscale (1 channel)
    unsigned char* image_data = stbi_load(input_path.string().c_str(), &width, &height, &channels, 1);

    if (!image_data) {
        std::cerr << "Error loading image: " << input_path.string() << std::endl;
        return;
    }

    int pixels = width * height;
    std::cout << "Resolution: " << width << "x" << height << " (" << pixels << " pixels)\n";

    std::vector<unsigned char> image_out_cpu(pixels);
    std::vector<unsigned char> image_out_omp(pixels);
    std::vector<unsigned char> image_out_tbb(pixels);

    SobelResult result_cpu = run_sobel_cpu(image_data, image_out_cpu.data(), width, height);
    SobelResult result_omp = run_sobel_omp(image_data, image_out_omp.data(), width, height);
    SobelResult result_tbb = run_sobel_tbb(image_data, image_out_tbb.data(), width, height);

    std::cout << std::left << std::setw(10) << "Method" << std::setw(15) << "Time (ms)" << std::endl;
    print_results("CPU", result_cpu);
    print_results("OpenMP", result_omp);
    print_results("TBB", result_tbb);

    // Calculate speedups
    double speedup_omp = result_cpu.time_total_ms / result_omp.time_total_ms;
    double speedup_tbb = result_cpu.time_total_ms / result_tbb.time_total_ms;
    
    std::cout << std::endl;
    std::cout << "Speedup OpenMP vs CPU: " << std::fixed << std::setprecision(2) << speedup_omp << "x" << std::endl;
    std::cout << "Speedup TBB vs CPU:    " << std::fixed << std::setprecision(2) << speedup_tbb << "x" << std::endl;

    // Save outputs
    std::string base_name = input_path.stem().string();
    stbi_write_png((output_dir / (base_name + "_out_cpu.png")).string().c_str(), width, height, 1, image_out_cpu.data(), width);
    stbi_write_png((output_dir / (base_name + "_out_omp.png")).string().c_str(), width, height, 1, image_out_omp.data(), width);
    stbi_write_png((output_dir / (base_name + "_out_tbb.png")).string().c_str(), width, height, 1, image_out_tbb.data(), width);

    // Write to CSV
    if (csv_file.is_open()) {
        csv_file << input_path.filename().string() << "," << width << "," << height << "," << pixels << ","
                 << result_cpu.time_total_ms << "," << result_omp.time_total_ms << "," << result_tbb.time_total_ms << "\n";
    }

    stbi_image_free(image_data);
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <input_image_or_directory_path>" << std::endl;
        return 1;
    }

    fs::path target_path = argv[1];

    if (!fs::exists(target_path)) {
        std::cerr << "Error: Path does not exist: " << target_path << std::endl;
        return 1;
    }

    fs::path output_dir;
    if (fs::is_regular_file(target_path)) {
        output_dir = target_path.parent_path() / "output";
    } else {
        output_dir = target_path / "output";
    }

    if (!fs::exists(output_dir)) {
        fs::create_directory(output_dir);
    }

    // Open CSV file
    std::ofstream csv_file(output_dir / "results.csv");
    if (csv_file.is_open()) {
        csv_file << "Image,Width,Height,Pixels,Time_CPU_ms,Time_OMP_ms,Time_TBB_ms\n";
    } else {
        std::cerr << "Warning: Could not open results.csv for writing." << std::endl;
    }

    if (fs::is_regular_file(target_path)) {
        process_image(target_path, output_dir, csv_file);
    } else if (fs::is_directory(target_path)) {
        int processed_count = 0;
        for (const auto& entry : fs::directory_iterator(target_path)) {
            if (entry.is_regular_file()) {
                std::string ext = entry.path().extension().string();
                std::transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
                if (ext == ".png" || ext == ".jpg" || ext == ".jpeg" || ext == ".bmp") {
                    process_image(entry.path(), output_dir, csv_file);
                    processed_count++;
                }
            }
        }
        std::cout << "\nProcessed " << processed_count << " images. Results saved in CSV." << std::endl;
    }

    if (csv_file.is_open()) {
        csv_file.close();
    }
    return 0;
}
