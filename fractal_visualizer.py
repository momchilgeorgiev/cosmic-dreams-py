#!/usr/bin/env python3
"""
Fractal Visualizer - Creates ASCII art and color representations of fractals
combined with poetry for a unique artistic experience.
"""

import math
import random
from typing import List, Tuple, Optional
from fractal_poetry import FractalEngine, MandelbrotEngine, JuliaEngine, FractalPoint


class ASCIIFractalRenderer:
    """Renders fractals as ASCII art with poetry integration."""
    
    def __init__(self, width: int = 80, height: int = 24):
        self.width = width
        self.height = height
        self.chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/*tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    
    def render_fractal(self, engine: FractalEngine, 
                      x_min: float = -2, x_max: float = 2,
                      y_min: float = -2, y_max: float = 2,
                      max_iter: int = 50) -> List[str]:
        """Render a fractal region as ASCII art."""
        lines = []
        
        for row in range(self.height):
            line = ""
            y = y_min + (y_max - y_min) * row / self.height
            
            for col in range(self.width):
                x = x_min + (x_max - x_min) * col / self.width
                point = engine.compute_point(x, y, max_iter)
                
                if point.escaped:
                    char_index = min(point.iterations * len(self.chars) // max_iter, len(self.chars) - 1)
                else:
                    char_index = len(self.chars) - 1
                
                line += self.chars[char_index]
            
            lines.append(line)
        
        return lines
    
    def render_with_poetry(self, engine: FractalEngine, poem_lines: List[str],
                          x_min: float = -2, x_max: float = 2,
                          y_min: float = -2, y_max: float = 2) -> str:
        """Render fractal with poetry overlay."""
        fractal_lines = self.render_fractal(engine, x_min, x_max, y_min, y_max)
        
        # Overlay poetry on fractal
        result = []
        poetry_line_index = 0
        
        for i, fractal_line in enumerate(fractal_lines):
            if i % (self.height // max(len(poem_lines), 1)) == 0 and poetry_line_index < len(poem_lines):
                # Insert poetry line
                poem_line = poem_lines[poetry_line_index]
                if len(poem_line) > self.width:
                    poem_line = poem_line[:self.width-3] + "..."
                
                # Center the poetry line
                padding = max(0, (self.width - len(poem_line)) // 2)
                result.append(" " * padding + poem_line)
                poetry_line_index += 1
            else:
                result.append(fractal_line)
        
        return "\n".join(result)


class ColorFractalRenderer:
    """Renders fractals with ANSI color codes."""
    
    def __init__(self, width: int = 60, height: int = 20):
        self.width = width
        self.height = height
    
    def hsv_to_ansi(self, h: float, s: float, v: float) -> str:
        """Convert HSV color to ANSI escape code."""
        if v < 0.1:
            return "\033[40m"  # Black background
        
        # Map hue to basic ANSI colors
        color_map = [31, 33, 32, 36, 34, 35]  # Red, Yellow, Green, Cyan, Blue, Magenta
        color_index = int(h * len(color_map)) % len(color_map)
        
        if v > 0.7:
            return f"\033[1;{color_map[color_index]}m"  # Bright
        else:
            return f"\033[{color_map[color_index]}m"    # Normal
    
    def render_colored_fractal(self, engine: FractalEngine,
                             x_min: float = -2, x_max: float = 2,
                             y_min: float = -2, y_max: float = 2,
                             max_iter: int = 50) -> str:
        """Render fractal with colors."""
        result = []
        
        for row in range(self.height):
            line = ""
            y = y_min + (y_max - y_min) * row / self.height
            
            for col in range(self.width):
                x = x_min + (x_max - x_min) * col / self.width
                point = engine.compute_point(x, y, max_iter)
                
                if point.escaped:
                    # Color based on iteration count and magnitude
                    hue = (point.iterations / max_iter) % 1.0
                    saturation = min(point.magnitude / 2, 1.0)
                    value = 0.8
                else:
                    # Inside set - darker colors
                    hue = point.magnitude % 1.0
                    saturation = 0.5
                    value = 0.3
                
                color = self.hsv_to_ansi(hue, saturation, value)
                line += color + "█" + "\033[0m"  # Reset color
            
            result.append(line)
        
        return "\n".join(result)


class InteractiveFractalExplorer:
    """Interactive fractal exploration with real-time poetry generation."""
    
    def __init__(self):
        self.ascii_renderer = ASCIIFractalRenderer(60, 15)
        self.color_renderer = ColorFractalRenderer(40, 12)
        self.engines = {
            'mandelbrot': MandelbrotEngine(),
            'julia': JuliaEngine(),
            'julia2': JuliaEngine(-0.8, 0.156),
            'julia3': JuliaEngine(0.285, 0.01)
        }
    
    def explore_region(self, engine_name: str, x: float, y: float, zoom: float = 1) -> str:
        """Explore a specific fractal region."""
        engine = self.engines.get(engine_name, self.engines['mandelbrot'])
        
        # Calculate view bounds
        size = 2 / zoom
        x_min, x_max = x - size, x + size
        y_min, y_max = y - size, y + size
        
        # Generate mini poem for this region
        points = []
        for _ in range(3):
            px = x + random.uniform(-size/2, size/2)
            py = y + random.uniform(-size/2, size/2)
            points.append(engine.compute_point(px, py))
        
        # Create a haiku-like poem
        poem_fragments = []
        for point in points:
            if point.escaped:
                if point.iterations < 10:
                    poem_fragments.append("chaos blooms")
                elif point.iterations < 30:
                    poem_fragments.append("patterns dance")
                else:
                    poem_fragments.append("order emerges")
            else:
                poem_fragments.append("infinite depth")
        
        # Render fractal
        ascii_art = self.ascii_renderer.render_fractal(engine, x_min, x_max, y_min, y_max, 30)
        colored_art = self.color_renderer.render_colored_fractal(engine, x_min, x_max, y_min, y_max, 30)
        
        result = f"\n🔍 Exploring {engine.get_name()} at ({x:.3f}, {y:.3f}) zoom {zoom:.1f}x\n"
        result += "=" * 60 + "\n"
        result += f"Poetry essence: {' • '.join(poem_fragments)}\n\n"
        result += "ASCII Fractal:\n"
        result += "\n".join(ascii_art[:8])  # Show only part for space
        result += "\n\nColored Fractal:\n"
        result += colored_art
        result += "\n" + "=" * 60
        
        return result
    
    def guided_tour(self) -> str:
        """Take a guided tour through interesting fractal regions."""
        tour_stops = [
            ('mandelbrot', 0, 0, 1, "The Classic Mandelbrot Set"),
            ('mandelbrot', -0.7, 0, 4, "The Seahorse Valley"),
            ('mandelbrot', -0.16, 1.04, 20, "Spiral Patterns"),
            ('julia', 0, 0, 1, "Julia Set Beauty"),
            ('julia2', 0, 0, 1, "Alternative Julia"),
        ]
        
        result = "\n🌟 FRACTAL POETRY TOUR 🌟\n"
        result += "=" * 50 + "\n"
        
        for engine_name, x, y, zoom, description in tour_stops:
            result += f"\n📍 {description}\n"
            result += self.explore_region(engine_name, x, y, zoom)
            result += "\n"
        
        return result


def create_fractal_mandala(size: int = 20) -> str:
    """Create a fractal-inspired mandala pattern."""
    mandala = []
    center = size // 2
    
    for row in range(size):
        line = ""
        for col in range(size):
            # Distance from center
            dx, dy = col - center, row - center
            distance = math.sqrt(dx*dx + dy*dy)
            angle = math.atan2(dy, dx)
            
            # Create mandala pattern using trigonometric functions
            pattern_value = (
                math.sin(distance * 0.5) * 
                math.cos(angle * 3) * 
                math.sin(angle * 5 + distance * 0.3)
            )
            
            if pattern_value > 0.3:
                line += "●"
            elif pattern_value > 0:
                line += "○"
            elif pattern_value > -0.3:
                line += "·"
            else:
                line += " "
        
        mandala.append(line)
    
    return "\n".join(mandala)


if __name__ == "__main__":
    print("🎨 Fractal Visualizer Demo 🎨")
    print("=" * 40)
    
    explorer = InteractiveFractalExplorer()
    
    # Quick demo
    print(explorer.explore_region('mandelbrot', -0.5, 0, 2))
    
    print("\n\n🕉️  Fractal Mandala:")
    print(create_fractal_mandala(15))
    
    print("\n\nRun with different parameters for more exploration!")