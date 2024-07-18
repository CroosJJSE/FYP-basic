# g++ -o convert_to_bw convert_to_bw.cpp `pkg-config --cflags --libs opencv4`


#include <opencv2/opencv.hpp>
#include <iostream>
#include <chrono>

using namespace cv;
using namespace std;

int main(int argc, char** argv) {
    if (argc != 3) {
        cout << "Usage: convert_to_bw <input_image_path> <output_image_path>" << endl;
        return -1;
    }

    string input_image_path = argv[1];
    string output_image_path = argv[2];

    Mat color_image = imread(input_image_path, IMREAD_COLOR);
    if (color_image.empty()) {
        cout << "Could not open or find the image" << endl;
        return -1;
    }

    Mat gray_image;
    auto start = chrono::high_resolution_clock::now();
    cvtColor(color_image, gray_image, COLOR_BGR2GRAY);
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> diff = end - start;

    imwrite(output_image_path, gray_image);
    cout << "Processing time: " << diff.count() << " s" << endl;

    return 0;
}
