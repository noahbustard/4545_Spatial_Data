CXX := g++
CXXFLAGS := -Wall -std=c++17 $(shell PKG_CONFIG_PATH=/opt/homebrew/lib/pkgconfig pkg-config --cflags sdl2)
LDFLAGS := $(shell PKG_CONFIG_PATH=/opt/homebrew/lib/pkgconfig pkg-config --libs sdl2)

TARGET := program00
SRC := main.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)
