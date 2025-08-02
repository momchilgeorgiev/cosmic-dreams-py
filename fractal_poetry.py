#!/usr/bin/env python3
"""
Fractal Poetry Generator - An AI-powered creative tool that generates poetry
inspired by fractal mathematics and visualizes the intersection of chaos theory
and natural language.

This project explores the beauty found in mathematical infinity and translates
complex patterns into human-readable verse.
"""

import math
import random
import colorsys
import argparse
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class FractalPoint:
    """Represents a point in fractal space with its mathematical properties."""
    x: float
    y: float
    iterations: int
    escaped: bool
    magnitude: float
    
    def to_poetry_seed(self) -> Dict[str, float]:
        """Convert fractal properties to poetry generation parameters."""
        return {
            'complexity': min(self.iterations / 100, 1.0),
            'intensity': self.magnitude,
            'chaos': 1.0 if self.escaped else 0.0,
            'rhythm': (self.x + self.y) % 1.0
        }


class FractalEngine(ABC):
    """Abstract base class for fractal computation engines."""
    
    @abstractmethod
    def compute_point(self, x: float, y: float, max_iter: int = 100) -> FractalPoint:
        """Compute fractal properties for a given point."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of this fractal type."""
        pass


class MandelbrotEngine(FractalEngine):
    """Mandelbrot set fractal engine."""
    
    def compute_point(self, x: float, y: float, max_iter: int = 100) -> FractalPoint:
        c = complex(x, y)
        z = 0
        
        for i in range(max_iter):
            if abs(z) > 2:
                magnitude = math.log(abs(z)) if abs(z) > 0 else 0
                return FractalPoint(x, y, i, True, magnitude)
            z = z*z + c
        
        magnitude = abs(z)
        return FractalPoint(x, y, max_iter, False, magnitude)
    
    def get_name(self) -> str:
        return "Mandelbrot"


class JuliaEngine(FractalEngine):
    """Julia set fractal engine."""
    
    def __init__(self, c_real: float = -0.7, c_imag: float = 0.27015):
        self.c = complex(c_real, c_imag)
    
    def compute_point(self, x: float, y: float, max_iter: int = 100) -> FractalPoint:
        z = complex(x, y)
        
        for i in range(max_iter):
            if abs(z) > 2:
                magnitude = math.log(abs(z)) if abs(z) > 0 else 0
                return FractalPoint(x, y, i, True, magnitude)
            z = z*z + self.c
        
        magnitude = abs(z)
        return FractalPoint(x, y, max_iter, False, magnitude)
    
    def get_name(self) -> str:
        return f"Julia({self.c.real:.3f}+{self.c.imag:.3f}i)"


class PoetryGenerator:
    """Generates poetry based on fractal mathematical properties."""
    
    def __init__(self):
        self.vocabulary = {
            'cosmic': ['infinite', 'eternal', 'boundless', 'celestial', 'astral', 'cosmic'],
            'chaos': ['turbulent', 'chaotic', 'swirling', 'spiraling', 'dancing', 'writhing'],
            'beauty': ['beautiful', 'elegant', 'sublime', 'graceful', 'delicate', 'intricate'],
            'nature': ['river', 'mountain', 'ocean', 'forest', 'wind', 'storm', 'dawn', 'twilight'],
            'emotion': ['yearning', 'wonder', 'mystery', 'passion', 'serenity', 'melancholy'],
            'movement': ['flows', 'cascades', 'spirals', 'unfolds', 'emerges', 'transforms'],
            'time': ['moment', 'eternity', 'instant', 'forever', 'cycle', 'rhythm']
        }
        
        self.templates = [
            "In {cosmic} {nature}, {emotion} {movement}",
            "Where {chaos} patterns {movement}, {beauty} forms emerge",
            "Through {time}'s {cosmic} dance, {nature} {emotion} flows",
            "{beauty} {chaos} in {cosmic} {nature}, {emotion} without end",
            "As {nature} {movement} through {time}, {beauty} {chaos} awakens"
        ]
    
    def generate_line(self, fractal_point: FractalPoint) -> str:
        """Generate a single line of poetry from fractal properties."""
        seed = fractal_point.to_poetry_seed()
        
        # Use fractal properties to influence word selection
        template = random.choice(self.templates)
        
        words = {}
        for category, word_list in self.vocabulary.items():
            # Use fractal properties to bias word selection
            if category == 'chaos' and seed['chaos'] > 0.5:
                words[category] = word_list[int(seed['intensity'] * len(word_list)) % len(word_list)]
            elif category == 'cosmic' and seed['complexity'] > 0.7:
                words[category] = word_list[int(seed['rhythm'] * len(word_list)) % len(word_list)]
            else:
                index = int((seed['complexity'] + seed['intensity']) * len(word_list)) % len(word_list)
                words[category] = word_list[index]
        
        # Capitalize first letter of sentence if at beginning
        first_placeholder = template.split('{')[1].split('}')[0] if '{' in template else ''
        if first_placeholder in words:
            words[first_placeholder] = words[first_placeholder].capitalize()
        
        return template.format(**words)
    
    def generate_poem(self, fractal_points: List[FractalPoint], title: str = "") -> str:
        """Generate a complete poem from a collection of fractal points."""
        lines = [self.generate_line(point) for point in fractal_points]
        
        poem = f"# {title}\n\n" if title else ""
        poem += "\n".join(lines)
        
        return poem


class FractalPoetryGenerator:
    """Main class that orchestrates fractal computation and poetry generation."""
    
    def __init__(self):
        self.engines = {
            'mandelbrot': MandelbrotEngine(),
            'julia': JuliaEngine()
        }
        self.poetry_generator = PoetryGenerator()
    
    def sample_fractal_region(self, engine_name: str, center_x: float = 0, center_y: float = 0, 
                            zoom: float = 1, samples: int = 10, max_iter: int = 100) -> List[FractalPoint]:
        """Sample points from a fractal region for poetry generation."""
        engine = self.engines.get(engine_name)
        if not engine:
            raise ValueError(f"Unknown fractal engine: {engine_name}")
        
        points = []
        for _ in range(samples):
            # Generate points in a region around the center
            x = center_x + random.uniform(-2/zoom, 2/zoom)
            y = center_y + random.uniform(-2/zoom, 2/zoom)
            point = engine.compute_point(x, y, max_iter)
            points.append(point)
        
        return points
    
    def create_fractal_poem(self, engine_name: str = 'mandelbrot', 
                          center_x: float = 0, center_y: float = 0,
                          zoom: float = 1, lines: int = 8) -> str:
        """Create a poem inspired by a specific fractal region."""
        points = self.sample_fractal_region(engine_name, center_x, center_y, zoom, lines)
        engine = self.engines[engine_name]
        title = f"Fractal Dreams: {engine.get_name()}"
        
        return self.poetry_generator.generate_poem(points, title)
    
    def explore_fractal_journey(self, engine_name: str = 'mandelbrot', steps: int = 5) -> str:
        """Create a poem by taking a journey through fractal space."""
        journey_points = []
        
        # Start at origin and zoom in with slight movements
        x, y, zoom = 0, 0, 1
        
        for step in range(steps):
            # Sample current region
            points = self.sample_fractal_region(engine_name, x, y, zoom, 2)
            journey_points.extend(points)
            
            # Move to interesting region (where fractal boundary exists)
            interesting_point = max(points, key=lambda p: p.iterations if not p.escaped else 0)
            x, y = interesting_point.x, interesting_point.y
            zoom *= 2
        
        engine = self.engines[engine_name]
        title = f"Journey Through {engine.get_name()}"
        
        return self.poetry_generator.generate_poem(journey_points, title)


def main():
    """Command-line interface for the Fractal Poetry Generator."""
    parser = argparse.ArgumentParser(description="Generate poetry inspired by fractal mathematics")
    parser.add_argument('--fractal', choices=['mandelbrot', 'julia'], default='mandelbrot',
                       help='Fractal type to use for inspiration')
    parser.add_argument('--mode', choices=['region', 'journey'], default='region',
                       help='Generation mode: single region or journey through fractal space')
    parser.add_argument('--lines', type=int, default=8, help='Number of lines in the poem')
    parser.add_argument('--x', type=float, default=0, help='Center X coordinate')
    parser.add_argument('--y', type=float, default=0, help='Center Y coordinate')
    parser.add_argument('--zoom', type=float, default=1, help='Zoom level')
    
    args = parser.parse_args()
    
    generator = FractalPoetryGenerator()
    
    print("🌌 Fractal Poetry Generator 🌌")
    print("=" * 40)
    
    if args.mode == 'region':
        poem = generator.create_fractal_poem(args.fractal, args.x, args.y, args.zoom, args.lines)
    else:
        poem = generator.explore_fractal_journey(args.fractal, args.lines)
    
    print(poem)
    print("\n" + "=" * 40)
    print("Generated with mathematical chaos and AI creativity")


if __name__ == "__main__":
    main()