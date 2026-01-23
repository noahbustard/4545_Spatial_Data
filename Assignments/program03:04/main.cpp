/**
 * ============================================================
 *  SDL2 Conway's Game of Life - Pattern Loader
 * ============================================================
 *  - Loads a pattern (e.g., "glider") from shapes.json
 *  - Initializes a Game of Life grid with that pattern
 *  - Runs Conway's Game of Life so the pattern evolves/moves
 *  - Renders live cells as filled rectangles in an SDL2 window
 *
 *  Usage:
 *      ./program2                // uses "glider" by default
 *      ./program2 blinker        // or any pattern in shapes.json
 *
 */

#include <SDL.h>
#include <fstream>
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <string>
#include <vector>
#include "json.hpp"

using json = nlohmann::json;
using namespace std;

int main(int argc, char* argv[]) {

    srand(static_cast<unsigned int>(time(nullptr)));

    const int windowWidth  = 500;
    const int windowHeight = 500;
    const int cellSize     = 10;


    const int cols = windowWidth / cellSize;
    const int rows = windowHeight / cellSize;


    string patternName = "glider";


    if (argc > 1) {
        patternName = argv[1];
        cout << "Loading pattern: " << patternName << "\n";
    }


    Uint8 r = rand() % 256;
    Uint8 g = rand() % 256;
    Uint8 b = rand() % 256;


    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        cerr << "SDL Init Error: " << SDL_GetError() << "\n";
        return 1;
    }

    SDL_Window* window = SDL_CreateWindow(
        "Conway's Game of Life",
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        windowWidth,
        windowHeight,
        SDL_WINDOW_SHOWN
    );

    if (!window) {
        cerr << "Window Error: " << SDL_GetError() << "\n";
        SDL_Quit();
        return 1;
    }

    SDL_Renderer* renderer = SDL_CreateRenderer(
        window,
        -1,
        SDL_RENDERER_ACCELERATED
    );

    if (!renderer) {
        cerr << "Renderer Error: " << SDL_GetError() << "\n";
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    ifstream f("shapes.json");
    if (!f.is_open()) {
        cerr << "Error: Could not open shapes.json\n";
        SDL_DestroyRenderer(renderer);
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    json data = json::parse(f);
    f.close();

    if (!data.contains("shapes") ||
        data["shapes"].find(patternName) == data["shapes"].end()) {
        cerr << "Error: Pattern '" << patternName
             << "' not found in shapes.json\n";
        SDL_DestroyRenderer(renderer);
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    auto pattern = data["shapes"][patternName];
    auto cells   = pattern["cells"];
    auto size    = pattern["size"];

    // 0 = dead, 1 = alive
    vector<vector<int>> grid(rows, vector<int>(cols, 0));
    vector<vector<int>> nextGrid(rows, vector<int>(cols, 0));


    int centerX = cols / 2;
    int centerY = rows / 2;

    // Place the pattern into the grid, centered
    for (const auto& cell : cells) {
        int dx = cell["x"]; 
        int dy = cell["y"]; 

        int gx = centerX + dx;
        int gy = centerY + dy;

        if (gx >= 0 && gx < cols && gy >= 0 && gy < rows) {
            grid[gy][gx] = 1;
        }
    }


    bool      running      = true;
    SDL_Event event;
    Uint32    lastUpdate   = SDL_GetTicks();
    const Uint32 stepDelay = 150; 

    while (running) {
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = false;
            } else if (event.type == SDL_KEYDOWN) {
                if (event.key.keysym.sym == SDLK_ESCAPE) {
                    running = false;
                }
            }
        }

        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);


        SDL_SetRenderDrawColor(renderer, r, g, b, 255);
        for (int y = 0; y < rows; y++) {
            for (int x = 0; x < cols; x++) {
                if (grid[y][x] == 1) {
                    SDL_Rect rect;
                    rect.x = x * cellSize;
                    rect.y = y * cellSize;
                    rect.w = cellSize;
                    rect.h = cellSize;
                    SDL_RenderFillRect(renderer, &rect);
                }
            }
        }

        SDL_RenderPresent(renderer);

        Uint32 now = SDL_GetTicks();
        if (now - lastUpdate >= stepDelay) {
            for (int y = 0; y < rows; y++) {
                for (int x = 0; x < cols; x++) {
                    int neighbors = 0;


                    for (int dy = -1; dy <= 1; dy++) {
                        for (int dx = -1; dx <= 1; dx++) {
                            if (dx == 0 && dy == 0) continue;

                            int nx = x + dx;
                            int ny = y + dy;

                            if (nx >= 0 && nx < cols &&
                                ny >= 0 && ny < rows) {
                                neighbors += grid[ny][nx];
                            }
                        }
                    }

                    int current = grid[y][x];

                    // Game of Life rules:
                    // 1. Any live cell with 2 or 3 neighbors survives.
                    // 2. Any dead cell with exactly 3 neighbors becomes alive.
                    // 3. All other live cells die in the next generation.
                    if (current == 1) {
                        if (neighbors == 2 || neighbors == 3) {
                            nextGrid[y][x] = 1;
                        } else {
                            nextGrid[y][x] = 0;
                        }
                    } else {
                        if (neighbors == 3) {
                            nextGrid[y][x] = 1;
                        } else {
                            nextGrid[y][x] = 0;
                        }
                    }
                }
            }

            // Swap grids
            grid.swap(nextGrid);
            lastUpdate = now;
        }

        // Small delay for smoother rendering
        SDL_Delay(16);
    }


    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
