#include <iostream>
#include <vector>
#include <cmath>

std::string decideColor(const std::vector<int>& RGB) {
    int R = RGB[0] / 256;
    int G = RGB[1] / 256;
    int B = RGB[2] / 256;
    double Max = std::max({ R, G, B });
    double Min = std::min({ R, G, B });

    double h = Max - Min;
    if (h == 0) {
        h = 1;
    }

    double S = (h / Max) * 100;
    double V = Max * 100;
    double H;

    if (Max == R) {
        H = 60 * ((G - B) / h);
        if (H < 0) {
            H = 360 - std::abs(H);
        }
    }
    else if (Max == G) {
        H = 60 * ((B - R) / h) + 120;
    }
    else if (Max == B) {
        H = 60 * ((R - G) / h) + 240;
    }
    else if (R == G && G == B) {
        H = 0;
    }
    else {
        // Should not reach this point
        return "Unknown";
    }

    if ((H >= 0 && H < 30) || (H >= 340 && H <= 360)) {
        if (S <= 10 && V > 85) {
            return "White";
        }
        else if (S <= 10 && V > 15 && V <= 85) {
            return "Gray";
        }
        else if (V <= 15) {
            return "Black";
        }
        else {
            return "Red";
        }
    }
    else if (H >= 30 && H < 40) {
        if (S <= 10 && V > 85) {
            return "White";
        }
        else if (S <= 10 && V > 15 && V <= 85) {
            return "Gray";
        }
        else if (V <= 15) {
            return "Black";
        }
        else if (S >= 50 && V <= 80 && V > 15) {
            return "Brown";
        }
        else {
            return "Orange";
        }
    }
    else if (H >= 40 && H < 65) {
        if (S <= 10 && V > 85) {
            return "White";
        }
        else if (S <= 10 && V > 15 && V <= 85) {
            return "Gray";
        }
        else if (V <= 15) {
            return "Black";
        }
        else {
            return "Yellow";
        }
    }
    else if (H >= 65 && H < 165) {
        if (S <= 10 && V > 85) {
            return "White";
        }
        else if (S <= 10 && V > 15 && V <= 85) {
            return "Gray";
        }
        else if (V <= 15) {
            return "Black";
        }
        else {
            return "Green";
        }
    }
    else if (H >= 165 && H < 265) {
        if (S <= 10 && V > 85) {
            return "White";
        }
        else if (S <= 10 && V > 15 && V <= 85) {
            return "Gray";
        }
        else if (V <= 15) {
            return "Black";
        }
        else {
            return "Blue";
        }
    }
    else if (H >= 265 && H < 340) {
        if (S <= 10 && V > 85) {
            return "White";
        }
        else if (S <= 10 && V > 15 && V <= 85) {
            return "Gray";
        }
        else if (V <= 15) {
            return "Black";
        }
        else if (H >= 300 && S > 5 && V >= 80) {
            return "Pink";
        }
        else {
            return "Purple";
        }
    }
    else {
        return "Unknown";
    }
}

int main() {
    std::vector<int> RGB = { 255, 0, 0 };

    std::string color = decideColor(RGB);
    std::cout << "The color is: " << color << std::endl;

    return 0;
}