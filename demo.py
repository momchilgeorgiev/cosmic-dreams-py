#!/usr/bin/env python3
"""
Quick demo of the Fractal Poetry Generator capabilities.
"""

from fractal_poetry import FractalPoetryGenerator
from fractal_visualizer import InteractiveFractalExplorer, create_fractal_mandala


def main():
    print("🌌✨ FRACTAL POETRY GENERATOR DEMO ✨🌌")
    print("=" * 50)
    
    generator = FractalPoetryGenerator()
    explorer = InteractiveFractalExplorer()
    
    print("\n🎭 Sample Poems:")
    print("-" * 30)
    
    # Generate a few sample poems
    poem1 = generator.create_fractal_poem('mandelbrot', -0.5, 0, 2, 4)
    print(poem1)
    
    print("\n")
    poem2 = generator.create_fractal_poem('julia', 0, 0, 1, 4)
    print(poem2)
    
    print("\n🎨 Fractal Visualization:")
    print("-" * 30)
    print(explorer.explore_region('mandelbrot', -0.7, 0, 4))
    
    print("\n🕉️ Fractal Mandala:")
    print("-" * 20)
    print(create_fractal_mandala(12))
    
    print("\n🚀 Try Interactive Mode:")
    print("python fractal_cli.py --interactive")
    print("\n✨ Explore infinite mathematical poetry! ✨")


if __name__ == "__main__":
    main()