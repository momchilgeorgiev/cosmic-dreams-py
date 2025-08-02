#!/usr/bin/env python3
"""
Interactive Fractal Poetry CLI - A sophisticated command-line interface
for exploring the intersection of mathematics, chaos theory, and poetry.
"""

import sys
import random
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import asdict
import argparse

from fractal_poetry import FractalPoetryGenerator, MandelbrotEngine, JuliaEngine
from fractal_visualizer import InteractiveFractalExplorer, create_fractal_mandala


class FractalPoetrySession:
    """Manages a complete fractal poetry exploration session."""
    
    def __init__(self):
        self.generator = FractalPoetryGenerator()
        self.explorer = InteractiveFractalExplorer()
        self.session_history = []
        self.bookmarks = {}
        self.current_location = {'engine': 'mandelbrot', 'x': 0, 'y': 0, 'zoom': 1}
    
    def save_bookmark(self, name: str) -> None:
        """Save current location as a bookmark."""
        self.bookmarks[name] = self.current_location.copy()
        print(f"📍 Bookmark '{name}' saved at {self.current_location}")
    
    def load_bookmark(self, name: str) -> bool:
        """Load a saved bookmark."""
        if name in self.bookmarks:
            self.current_location = self.bookmarks[name].copy()
            print(f"🚀 Jumped to bookmark '{name}'")
            return True
        else:
            print(f"❌ Bookmark '{name}' not found")
            return False
    
    def list_bookmarks(self) -> None:
        """List all saved bookmarks."""
        if not self.bookmarks:
            print("📝 No bookmarks saved yet")
        else:
            print("📚 Saved Bookmarks:")
            for name, location in self.bookmarks.items():
                print(f"  {name}: {location['engine']} at ({location['x']:.3f}, {location['y']:.3f}) zoom {location['zoom']:.1f}x")
    
    def navigate(self, direction: str, step_size: float = 0.1) -> None:
        """Navigate through fractal space."""
        zoom_factor = step_size / self.current_location['zoom']
        
        if direction == 'up':
            self.current_location['y'] += zoom_factor
        elif direction == 'down':
            self.current_location['y'] -= zoom_factor
        elif direction == 'left':
            self.current_location['x'] -= zoom_factor
        elif direction == 'right':
            self.current_location['x'] += zoom_factor
        elif direction == 'in':
            self.current_location['zoom'] *= 2
        elif direction == 'out':
            self.current_location['zoom'] /= 2
        else:
            print(f"❌ Unknown direction: {direction}")
            return
        
        print(f"🧭 Moved {direction}. Now at ({self.current_location['x']:.3f}, {self.current_location['y']:.3f}) zoom {self.current_location['zoom']:.1f}x")
    
    def switch_fractal(self, engine_name: str) -> None:
        """Switch to a different fractal type."""
        if engine_name in self.generator.engines:
            self.current_location['engine'] = engine_name
            print(f"🔄 Switched to {engine_name} fractal")
        else:
            print(f"❌ Unknown fractal type: {engine_name}")
    
    def explore_current(self) -> None:
        """Explore current location."""
        result = self.explorer.explore_region(
            self.current_location['engine'],
            self.current_location['x'],
            self.current_location['y'],
            self.current_location['zoom']
        )
        print(result)
        
        # Add to session history
        self.session_history.append({
            'action': 'explore',
            'location': self.current_location.copy(),
            'timestamp': len(self.session_history)
        })
    
    def generate_poem(self, lines: int = 8) -> None:
        """Generate a poem at current location."""
        poem = self.generator.create_fractal_poem(
            self.current_location['engine'],
            self.current_location['x'],
            self.current_location['y'],
            self.current_location['zoom'],
            lines
        )
        print(poem)
        
        # Add to session history
        self.session_history.append({
            'action': 'poem',
            'location': self.current_location.copy(),
            'poem': poem,
            'timestamp': len(self.session_history)
        })
    
    def random_jump(self) -> None:
        """Jump to a random interesting location."""
        interesting_locations = [
            {'engine': 'mandelbrot', 'x': -0.7, 'y': 0, 'zoom': 4},
            {'engine': 'mandelbrot', 'x': -0.16, 'y': 1.04, 'zoom': 20},
            {'engine': 'mandelbrot', 'x': -0.4, 'y': 0.6, 'zoom': 10},
            {'engine': 'julia', 'x': 0, 'y': 0, 'zoom': 2},
            {'engine': 'mandelbrot', 'x': -1.25, 'y': 0, 'zoom': 8},
        ]
        
        self.current_location = random.choice(interesting_locations)
        print(f"🎲 Random jump to {self.current_location}")
        self.explore_current()
    
    def export_session(self, filename: str) -> None:
        """Export session history to a file."""
        session_data = {
            'history': self.session_history,
            'bookmarks': self.bookmarks,
            'current_location': self.current_location
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2)
            print(f"💾 Session exported to {filename}")
        except Exception as e:
            print(f"❌ Failed to export session: {e}")
    
    def show_help(self) -> None:
        """Show available commands."""
        help_text = """
🌌 FRACTAL POETRY EXPLORER COMMANDS 🌌

Navigation:
  up/down/left/right [step]  - Move through fractal space
  in/out [factor]            - Zoom in/out
  jump <x> <y> [zoom]        - Jump to specific coordinates
  random                     - Jump to random interesting location

Fractals:
  mandelbrot                 - Switch to Mandelbrot set
  julia                      - Switch to Julia set
  
Exploration:
  explore                    - Explore current location
  poem [lines]               - Generate poetry at current location
  journey [steps]            - Take a guided journey
  tour                       - Full guided tour
  mandala                    - Show fractal mandala

Bookmarks:
  save <name>                - Save current location
  load <name>                - Load saved location
  bookmarks                  - List all bookmarks

Session:
  history                    - Show session history
  export <filename>          - Export session to file
  status                     - Show current status
  
Utilities:
  help                       - Show this help
  quit/exit                  - Exit the explorer

Examples:
  > explore
  > poem 6
  > up 0.2
  > save spiral_region
  > random
  > tour
        """
        print(help_text)


def run_interactive_session():
    """Run the interactive fractal poetry exploration session."""
    session = FractalPoetrySession()
    
    print("""
🌌✨ WELCOME TO FRACTAL POETRY EXPLORER ✨🌌

Where mathematics meets poetry, and chaos becomes art.
Explore infinite worlds of fractals and generate unique poems
inspired by the mathematical beauty of complex numbers.

Type 'help' for commands or 'tour' for a guided experience.
""")
    
    while True:
        try:
            command = input("\n🔮 fractal-poetry> ").strip().lower()
            
            if not command:
                continue
            
            parts = command.split()
            cmd = parts[0]
            
            if cmd in ['quit', 'exit']:
                print("🌟 Thank you for exploring the infinite! Goodbye! 🌟")
                break
            
            elif cmd == 'help':
                session.show_help()
            
            elif cmd in ['up', 'down', 'left', 'right']:
                step = float(parts[1]) if len(parts) > 1 else 0.1
                session.navigate(cmd, step)
            
            elif cmd in ['in', 'out']:
                session.navigate(cmd)
            
            elif cmd == 'jump':
                if len(parts) >= 3:
                    x, y = float(parts[1]), float(parts[2])
                    zoom = float(parts[3]) if len(parts) > 3 else 1
                    session.current_location.update({'x': x, 'y': y, 'zoom': zoom})
                    print(f"🚀 Jumped to ({x:.3f}, {y:.3f}) zoom {zoom:.1f}x")
                else:
                    print("❌ Usage: jump <x> <y> [zoom]")
            
            elif cmd == 'random':
                session.random_jump()
            
            elif cmd in ['mandelbrot', 'julia']:
                session.switch_fractal(cmd)
            
            elif cmd == 'explore':
                session.explore_current()
            
            elif cmd == 'poem':
                lines = int(parts[1]) if len(parts) > 1 else 8
                session.generate_poem(lines)
            
            elif cmd == 'journey':
                steps = int(parts[1]) if len(parts) > 1 else 5
                poem = session.generator.explore_fractal_journey(
                    session.current_location['engine'], steps
                )
                print(poem)
            
            elif cmd == 'tour':
                print(session.explorer.guided_tour())
            
            elif cmd == 'mandala':
                print("\n🕉️  Fractal Mandala:")
                print(create_fractal_mandala(20))
            
            elif cmd == 'save':
                if len(parts) > 1:
                    session.save_bookmark(parts[1])
                else:
                    print("❌ Usage: save <name>")
            
            elif cmd == 'load':
                if len(parts) > 1:
                    session.load_bookmark(parts[1])
                else:
                    print("❌ Usage: load <name>")
            
            elif cmd == 'bookmarks':
                session.list_bookmarks()
            
            elif cmd == 'history':
                if session.session_history:
                    print("📜 Session History:")
                    for i, entry in enumerate(session.session_history[-10:]):  # Last 10
                        print(f"  {i+1}. {entry['action']} at {entry['location']}")
                else:
                    print("📝 No history yet")
            
            elif cmd == 'export':
                if len(parts) > 1:
                    session.export_session(parts[1])
                else:
                    print("❌ Usage: export <filename>")
            
            elif cmd == 'status':
                loc = session.current_location
                print(f"📍 Current: {loc['engine']} at ({loc['x']:.3f}, {loc['y']:.3f}) zoom {loc['zoom']:.1f}x")
                print(f"📚 Bookmarks: {len(session.bookmarks)}")
                print(f"📜 History entries: {len(session.session_history)}")
            
            else:
                print(f"❌ Unknown command: {cmd}. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n🌟 Thank you for exploring the infinite! Goodbye! 🌟")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main entry point with command-line argument support."""
    parser = argparse.ArgumentParser(description="Fractal Poetry Explorer - Where Math Meets Art")
    parser.add_argument('--interactive', '-i', action='store_true', 
                       help='Start interactive exploration session')
    parser.add_argument('--demo', action='store_true',
                       help='Run a quick demo')
    parser.add_argument('--tour', action='store_true',
                       help='Take the guided tour')
    parser.add_argument('--poem', action='store_true',
                       help='Generate a single poem')
    parser.add_argument('--fractal', choices=['mandelbrot', 'julia'], default='mandelbrot',
                       help='Fractal type for single operations')
    
    args = parser.parse_args()
    
    if args.interactive or len(sys.argv) == 1:
        run_interactive_session()
    elif args.tour:
        explorer = InteractiveFractalExplorer()
        print(explorer.guided_tour())
    elif args.demo:
        print("🎨 Quick Fractal Poetry Demo:")
        generator = FractalPoetryGenerator()
        explorer = InteractiveFractalExplorer()
        
        print(generator.create_fractal_poem('mandelbrot', -0.5, 0, 2, 6))
        print("\n" + "="*50)
        print(explorer.explore_region('julia', 0, 0, 1))
    elif args.poem:
        generator = FractalPoetryGenerator()
        poem = generator.create_fractal_poem(args.fractal)
        print(poem)
    else:
        print("Use --interactive for full experience, --tour for guided tour, or --demo for quick preview")


if __name__ == "__main__":
    main()