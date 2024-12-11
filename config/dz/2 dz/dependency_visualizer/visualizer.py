import argparse
import subprocess
import os
from graph_builder import build_dependency_graph, save_graph_to_dot

def visualize_graph(dot_file_path, visualizer_program):
    output_image = "dependencies.png"
    try:
        result = subprocess.run(
            [visualizer_program, "-Tpng", dot_file_path, "-o", output_image],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Graph visualization saved as '{output_image}'.")
        visualize_graph_on_screen(output_image)
    except FileNotFoundError:
        print(f"Error: Program '{visualizer_program}' not found. Please ensure it is installed and in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error running the visualizer: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def visualize_graph_on_screen(image_path):
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' does not exist.")
        return
    try:
        if os.name == "posix":
            subprocess.run(["xdg-open", image_path])  # Для Linux
        elif os.name == "nt":
            subprocess.run(["mspaint", image_path])  # Для Windows
        elif os.name == "darwin":
            subprocess.run(["open", image_path])  # Для macOS
        else:
            print(f"Unable to open image automatically. Please open '{image_path}' manually.")
    except Exception as e:
        print(f"Error opening image: {e}")

def main():
    parser = argparse.ArgumentParser(description="Visualize git dependency graph.")
    parser.add_argument("visualizer", help="Path to Graphviz visualization program (e.g., dot, xdot).")
    parser.add_argument("repository", help="Path to the git repository.")
    parser.add_argument("--output", help="Path to save the output image.", default="dependencies.png")
    args = parser.parse_args()

    dot_file = "dependencies.dot"
    print(f"Building dependency graph for repository: {args.repository}...")
    graph = build_dependency_graph(args.repository)
    if not graph:
        print("Graph construction failed. Exiting.")
        return

    print("Saving graph to DOT file...")
    save_graph_to_dot(graph, dot_file)

    print("Visualizing graph...")
    visualize_graph(dot_file, args.visualizer)

if __name__ == "__main__":
    main()
