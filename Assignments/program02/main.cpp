/**
 * ============================================================
 *  SDL2 Shape Renderer
 * ============================================================
 *  This program loads Conway's Game of Life patterns from JSON
 *  and renders them as filled rectangles in an SDL2 window.
 *
 *  Concepts introduced:
 *   - Loading and parsing JSON data
 *   - Converting grid coordinates to pixel coordinates
 *   - Drawing filled rectangles (cells)
 *   - Centering patterns in the window
 *   - Generating random colors
 *   - Handling ESC key input to quit
 *   - Optional command-line pattern selection
 *
 */
#include <SDL.h>
#include <fstream>
#include <iostream> 
#include <cstdlib>
#include <ctime>
#include <string>
#include "json.hpp"

using json = nlohmann::json;

using namespace std;

int main(int argc, char* argv[]) {
    // ------------------------------------------------------------
    // CONFIGURATION SECTION
    // ------------------------------------------------------------
    // Seed random number generator for random colors (Requirement: random color)
    srand(time(0));


    const int windowWidth = 500;
    const int windowHeight = 500;

    //Requirement 3
    const int cellSize = 10;
    
    //Requirement 2
    string patternName = "glider";

    //Requirement 6
    if (argc > 1) {
        patternName = argv[1];
        cout << "Loading pattern: " << patternName << "\n";
    }

    //Requirement 5
    Uint8 r = rand() % 256;
    Uint8 g = rand() % 256;
    Uint8 b = rand() % 256;

    // ------------------------------------------------------------
    // INITIALIZE SDL
    // ------------------------------------------------------------
    // SDL_Init starts the requested SDL subsystems.
    // SDL_INIT_VIDEO allows us to create a window and draw graphics.
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        std::cerr << "SDL Init Error: " << SDL_GetError() << "\n";
        return 1;  // Return non-zero to indicate an error
    }

    // ------------------------------------------------------------
    // CREATE THE WINDOW
    // ------------------------------------------------------------
    // SDL_CreateWindow opens a visible OS-level window.
    // Parameters:
    //   - Title text
    //   - x, y screen position (SDL_WINDOWPOS_CENTERED lets SDL decide)
    //   - Width and height in pixels
    //   - Flags (SDL_WINDOW_SHOWN = visible on creation)
    SDL_Window* window = SDL_CreateWindow(
        "SDL2 Grid Example",     // title
        SDL_WINDOWPOS_CENTERED,  // x position
        SDL_WINDOWPOS_CENTERED,  // y position
        windowWidth,             // window width (pixels)
        windowHeight,            // window height (pixels)
        SDL_WINDOW_SHOWN         // flags
    );

    // Verify the window was successfully created
    if (!window) {
        std::cerr << "Window Error: " << SDL_GetError() << "\n";
        SDL_Quit();  // Clean up SDL before exiting
        return 1;
    }

    // ------------------------------------------------------------
    // CREATE A RENDERER
    // ------------------------------------------------------------
    // The renderer handles drawing operations on the window.
    // SDL_RENDERER_ACCELERATED tells SDL to use GPU acceleration.
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        std::cerr << "Renderer Error: " << SDL_GetError() << "\n";
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    // ------------------------------------------------------------
    // MAIN LOOP
    // MAIN LOOP
    // "running" flag controls the lifetime of the program.
    bool      running = true;
    SDL_Event event;  // Struct that holds event information (keyboard, mouse, quit, etc.)

    //Requirement 1
    ifstream f("shapes.json");
    if (!f.is_open()) {
        std::cerr << "Error: Could not open shapes.json file\n";
        SDL_DestroyRenderer(renderer);
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    json data = json::parse(f);
    f.close();

    // Extract the selected pattern from JSON
    // Access the pattern data: data["shapes"][patternName]
    if (data["shapes"].find(patternName) == data["shapes"].end()) {
        std::cerr << "Error: Pattern '" << patternName << "' not found in shapes.json\n";
        SDL_DestroyRenderer(renderer);
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    auto pattern = data["shapes"][patternName];
    auto cells = pattern["cells"];  // Array of {x, y} objects
    auto size = pattern["size"];    // {w, h} for pattern dimensions

    // Calculate pattern bounds to center it (Requirement: center pattern in window)
    int patternWidth = size["w"];
    int patternHeight = size["h"];

    //Requirement4
    int offsetX = (windowWidth - (patternWidth * cellSize)) / 2;
    int offsetY = (windowHeight - (patternHeight * cellSize)) / 2;

    while (running) {
        // --------------------------------------------------------
        // EVENT HANDLING
        // --------------------------------------------------------
        // SDL_PollEvent() pulls events from the event queue.
        // This loop checks for any pending events, e.g. user clicking "X" to close.
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                // Window close event
                running = false;
            } else if (event.type == SDL_KEYDOWN) {
                // Requirement 7
                if (event.key.keysym.sym == SDLK_ESCAPE) {
                    running = false;
                }
            }
        }

        // --------------------------------------------------------
        // CLEAR SCREEN
        // --------------------------------------------------------
        // Set the background color to black
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        // --------------------------------------------------------
        // DRAW FILLED RECTANGLES FOR PATTERN CELLS
        // --------------------------------------------------------
        // Set the color to the random color we generated earlier
        // (Requirement: pattern should have a random color)
        SDL_SetRenderDrawColor(renderer, r, g, b, 255);

        // Iterate through each cell in the pattern
        // (Requirement: each cell is a filled rectangle of fixed size)
        for (const auto& cell : cells) {
            int gridX = cell["x"];  // Grid coordinate
            int gridY = cell["y"];  // Grid coordinate

            // Convert grid coordinates to pixel coordinates
            // Then apply centering offset (Requirement: centered in window)
            int pixelX = offsetX + (gridX * cellSize);
            int pixelY = offsetY + (gridY * cellSize);

            // Create a rectangle for this cell
            SDL_Rect rect = {pixelX, pixelY, cellSize, cellSize};

            // Draw the filled rectangle
            SDL_RenderFillRect(renderer, &rect);
        }

        // --------------------------------------------------------
        // SHOW THE RESULT
        // --------------------------------------------------------
        // Swap the off-screen buffer with the on-screen buffer.
        // Everything drawn since the last call to SDL_RenderPresent()
        // now becomes visible.
        SDL_RenderPresent(renderer);

        // --------------------------------------------------------
        // FRAME RATE LIMIT
        // --------------------------------------------------------
        // Delay ~16 ms to target roughly 60 frames per second.
        // (1000 ms / 60 ≈ 16.6 ms)
        SDL_Delay(16);
    }

    // ------------------------------------------------------------
    // CLEANUP
    // ------------------------------------------------------------
    // Free SDL resources before exiting to avoid memory leaks.
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;  // 0 = successful program termination
}
