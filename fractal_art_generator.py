#!/usr/bin/env python3
"""
Advanced Fractal Art Generator - Creates exportable fractal art with poetry
and sophisticated color mapping techniques.
"""

import math
import random
import csv
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

from fractal_poetry import FractalEngine, FractalPoint, MandelbrotEngine, JuliaEngine, PoetryGenerator


@dataclass
class ColorPalette:
    """Represents a color palette for fractal rendering."""
    name: str
    colors: List[Tuple[int, int, int]]  # RGB tuples
    
    def get_color(self, t: float) -> Tuple[int, int, int]:
        """Get interpolated color at position t (0-1)."""
        if len(self.colors) < 2:
            return self.colors[0] if self.colors else (0, 0, 0)
        
        # Clamp t to [0, 1]
        t = max(0, min(1, t))
        
        # Find the two colors to interpolate between
        scaled_t = t * (len(self.colors) - 1)
        idx = int(scaled_t)
        frac = scaled_t - idx
        
        if idx >= len(self.colors) - 1:
            return self.colors[-1]
        
        c1 = self.colors[idx]
        c2 = self.colors[idx + 1]
        
        # Linear interpolation
        return (
            int(c1[0] + frac * (c2[0] - c1[0])),
            int(c1[1] + frac * (c2[1] - c1[1])),
            int(c1[2] + frac * (c2[2] - c1[2]))
        )


class PaletteLibrary:
    """Collection of predefined color palettes."""
    
    @staticmethod
    def get_palettes() -> Dict[str, ColorPalette]:
        return {
            'fire': ColorPalette('Fire', [
                (0, 0, 0), (64, 0, 0), (128, 0, 0), (255, 0, 0),
                (255, 128, 0), (255, 255, 0), (255, 255, 255)
            ]),
            'ocean': ColorPalette('Ocean', [
                (0, 0, 64), (0, 64, 128), (0, 128, 255),
                (64, 192, 255), (128, 224, 255), (255, 255, 255)
            ]),
            'cosmic': ColorPalette('Cosmic', [
                (0, 0, 0), (32, 0, 64), (64, 0, 128), (128, 0, 255),
                (255, 0, 255), (255, 128, 255), (255, 255, 255)
            ]),
            'forest': ColorPalette('Forest', [
                (0, 32, 0), (0, 64, 0), (0, 128, 0), (64, 192, 64),
                (128, 255, 128), (192, 255, 192), (255, 255, 255)
            ]),
            'sunset': ColorPalette('Sunset', [
                (64, 0, 64), (128, 0, 64), (255, 64, 0),
                (255, 128, 0), (255, 192, 64), (255, 255, 128)
            ])
        }


class FractalArtRenderer:
    """Advanced fractal renderer with multiple export formats."""
    
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.palettes = PaletteLibrary.get_palettes()
    
    def render_to_ppm(self, engine: FractalEngine, filename: str,
                      x_min: float = -2, x_max: float = 2,
                      y_min: float = -2, y_max: float = 2,
                      max_iter: int = 100, palette_name: str = 'fire') -> None:
        """Render fractal to PPM image format."""
        palette = self.palettes.get(palette_name, self.palettes['fire'])
        
        with open(filename, 'w') as f:
            # PPM header
            f.write(f"P3\n{self.width} {self.height}\n255\n")
            
            for row in range(self.height):
                y = y_min + (y_max - y_min) * row / self.height
                
                for col in range(self.width):
                    x = x_min + (x_max - x_min) * col / self.width
                    point = engine.compute_point(x, y, max_iter)
                    
                    if point.escaped:
                        t = point.iterations / max_iter
                        # Add some variation based on magnitude
                        t = (t + point.magnitude * 0.1) % 1.0
                    else:
                        t = 0.0
                    
                    r, g, b = palette.get_color(t)
                    f.write(f"{r} {g} {b} ")
                
                f.write("\n")
    
    def render_ascii_art(self, engine: FractalEngine, 
                        x_min: float = -2, x_max: float = 2,
                        y_min: float = -2, y_max: float = 2,
                        max_iter: int = 50, style: str = 'gradient') -> str:
        """Render fractal as detailed ASCII art."""
        if style == 'gradient':
            chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/*tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
        elif style == 'blocks':
            chars = " ░▒▓█"
        elif style == 'dots':
            chars = " ·•○●"
        else:
            chars = " .-=+*#"
        
        lines = []
        for row in range(self.height // 8):  # Reduced resolution for ASCII
            line = ""
            y = y_min + (y_max - y_min) * row / (self.height // 8)
            
            for col in range(self.width // 8):
                x = x_min + (x_max - x_min) * col / (self.width // 8)
                point = engine.compute_point(x, y, max_iter)
                
                if point.escaped:
                    char_index = min(point.iterations * len(chars) // max_iter, len(chars) - 1)
                else:
                    char_index = len(chars) - 1
                
                line += chars[char_index]
            
            lines.append(line)
        
        return "\n".join(lines)


class FractalDataExporter:
    """Exports fractal data in various formats for analysis."""
    
    def export_fractal_data(self, engine: FractalEngine, filename: str,
                           x_min: float = -2, x_max: float = 2,
                           y_min: float = -2, y_max: float = 2,
                           resolution: int = 100, max_iter: int = 100) -> None:
        """Export fractal iteration data to CSV."""
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['x', 'y', 'iterations', 'escaped', 'magnitude'])
            
            for row in range(resolution):
                y = y_min + (y_max - y_min) * row / resolution
                
                for col in range(resolution):
                    x = x_min + (x_max - x_min) * col / resolution
                    point = engine.compute_point(x, y, max_iter)
                    
                    writer.writerow([
                        x, y, point.iterations, point.escaped, point.magnitude
                    ])
    
    def export_poetry_analysis(self, poems: List[str], filename: str) -> None:
        """Export poetry analysis data."""
        with open(filename, 'w') as f:
            f.write("Fractal Poetry Analysis Report\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total poems: {len(poems)}\n\n")
            
            for i, poem in enumerate(poems, 1):
                f.write(f"Poem {i}:\n")
                f.write("-" * 20 + "\n")
                f.write(poem + "\n\n")
                
                # Basic analysis
                lines = poem.split('\n')
                word_count = sum(len(line.split()) for line in lines if line.strip())
                f.write(f"Lines: {len([l for l in lines if l.strip()])}\n")
                f.write(f"Words: {word_count}\n")
                f.write(f"Characters: {len(poem)}\n\n")


class AdvancedFractalStudio:
    """Complete fractal art studio with all advanced features."""
    
    def __init__(self):
        self.art_renderer = FractalArtRenderer(400, 300)
        self.data_exporter = FractalDataExporter()
        self.poetry_generator = PoetryGenerator()
        self.engines = {
            'mandelbrot': MandelbrotEngine(),
            'julia': JuliaEngine(),
            'julia_spiral': JuliaEngine(-0.8, 0.156),
            'julia_dragon': JuliaEngine(0.285, 0.01),
            'julia_snowflake': JuliaEngine(-0.4, 0.6)
        }
    
    def create_art_collection(self, collection_name: str) -> None:
        """Create a complete art collection with multiple pieces."""
        print(f"🎨 Creating '{collection_name}' art collection...")
        
        # Define interesting regions for each fractal
        regions = [
            ('mandelbrot', -0.5, 0, 2, 'fire', 'The Classic View'),
            ('mandelbrot', -0.7, 0, 4, 'ocean', 'Seahorse Valley'),
            ('mandelbrot', -0.16, 1.04, 20, 'cosmic', 'Spiral Dreams'),
            ('julia', 0, 0, 1, 'sunset', 'Julia Beauty'),
            ('julia', 0, 0, 1, 'forest', 'Spiral Dance'),
            ('julia', 0, 0, 2, 'fire', 'Dragon Curves'),
        ]
        
        poems = []
        
        for i, (engine_name, x, y, zoom, palette, title) in enumerate(regions):
            print(f"  Creating piece {i+1}: {title}...")
            
            engine = self.engines[engine_name]
            
            # Calculate bounds
            size = 2 / zoom
            x_min, x_max = x - size, x + size
            y_min, y_max = y - size, y + size
            
            # Generate art
            ppm_filename = f"{collection_name}_{i+1:02d}_{engine_name}_{palette}.ppm"
            self.art_renderer.render_to_ppm(
                engine, ppm_filename, x_min, x_max, y_min, y_max, 150, palette
            )
            
            # Generate ASCII version
            ascii_art = self.art_renderer.render_ascii_art(
                engine, x_min, x_max, y_min, y_max, 100, 'gradient'
            )
            
            with open(f"{collection_name}_{i+1:02d}_ascii.txt", 'w') as f:
                f.write(f"{title}\n")
                f.write("=" * len(title) + "\n\n")
                f.write(ascii_art)
            
            # Generate poetry
            generator = FractalPoetryGenerator()
            poem = generator.create_fractal_poem(engine_name, x, y, zoom, 6)
            poems.append(poem)
            
            print(f"    ✓ Generated {ppm_filename}")
            print(f"    ✓ Generated ASCII art")
            print(f"    ✓ Generated poetry")
        
        # Export poetry collection
        self.data_exporter.export_poetry_analysis(poems, f"{collection_name}_poetry.txt")
        
        # Create master catalog
        with open(f"{collection_name}_catalog.txt", 'w') as f:
            f.write(f"{collection_name.upper()} - FRACTAL ART COLLECTION\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Created by Fractal Poetry Generator - AI Art Studio\n\n")
            
            f.write("COLLECTION CONTENTS:\n")
            for i, (engine_name, x, y, zoom, palette, title) in enumerate(regions):
                f.write(f"{i+1:2d}. {title}\n")
                f.write(f"    Fractal: {engine_name}\n")
                f.write(f"    Region: ({x:.3f}, {y:.3f}) at {zoom:.1f}x zoom\n")
                f.write(f"    Palette: {palette}\n")
                f.write(f"    Files: {collection_name}_{i+1:02d}_*\n\n")
        
        print(f"🎉 Collection '{collection_name}' complete!")
        print(f"   Generated {len(regions)} art pieces with poetry and ASCII variants")
    
    def fractal_poetry_challenge(self) -> None:
        """Generate a themed poetry challenge based on fractal exploration."""
        themes = [
            ("Infinite Recursion", "mandelbrot", -0.75, 0.1, 10),
            ("Chaos and Order", "julia", 0, 0, 2),
            ("Mathematical Beauty", "mandelbrot", -0.16, 1.04, 50),
            ("Complex Dynamics", "julia_spiral", 0, 0, 1),
            ("Fractal Dreams", "julia_dragon", 0, 0, 3)
        ]
        
        print("🏆 FRACTAL POETRY CHALLENGE 🏆")
        print("=" * 40)
        
        for theme, engine, x, y, zoom in themes:
            print(f"\n📝 Theme: {theme}")
            print("-" * 30)
            
            generator = FractalPoetryGenerator()
            poem = generator.create_fractal_poem(engine, x, y, zoom, 4)
            print(poem)
        
        print("\n🌟 Challenge complete! Each poem inspired by unique fractal mathematics.")


# Import statement for the main module
from fractal_poetry import FractalPoetryGenerator


if __name__ == "__main__":
    print("🎨 Advanced Fractal Art Studio 🎨")
    print("=" * 40)
    
    studio = AdvancedFractalStudio()
    
    # Create a sample art collection
    studio.create_art_collection("cosmic_dreams")
    
    print("\n")
    studio.fractal_poetry_challenge()