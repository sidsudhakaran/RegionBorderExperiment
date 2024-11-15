import ast
import argparse
from shapely.geometry import LineString

def read_coordinates_array_txt(file_path):
    """
    Reads coordinates from a TXT file containing an array of (x, y) tuples.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            # Safely evaluate the list using ast.literal_eval
            points = ast.literal_eval(content)
            # Validate that it's a list of tuples or lists
            if isinstance(points, list) and all(isinstance(pt, (list, tuple)) and len(pt) == 2 for pt in points):
                # Convert all points to tuples
                points = [tuple(pt) for pt in points]
                return points
            else:
                print("Error: The file must contain a list of (x, y) tuples.")
                return []
    except FileNotFoundError:
        print(f"Error: File not found - '{file_path}'")
        return []
    except (SyntaxError, ValueError) as e:
        print(f"Error: Failed to parse the file - {e}")
        return []

def ensure_polygon_closed(points):
    """
    Ensures that the polygon is closed by appending the first point to the end if necessary.
    """
    if not points:
        return points
    if points[0] != points[-1]:
        points.append(points[0])
    return points

def undo_scenekit_transformation(transformed_points):
    """
    Reverses the SceneKit transformation applied as:
    CGPoint(x: -data.y, y: -data.x)

    """
    original_points = [(-y, -x) for (x, y) in transformed_points]
    return original_points

def validate_polygon(points):
    """
    Validates basic properties of the polygon.
    """
    if len(points) < 4:
        print("Error: A polygon must have at least 3 distinct points (with closure).")
        return False
    # Check for consecutive duplicate points
    for i in range(len(points) - 1):
        if points[i] == points[i + 1]:
            print(f"Error: Consecutive duplicate points at index {i} ({points[i], points[i+1]}).")
            return False
    return True

def detect_self_intersections(points):
    """
    Detects if the polygon defined by 'points' has any self-intersections.
    Returns True if simple (no self-intersections), False otherwise.
    """
    polygon_boundary = LineString(points)
    is_simple = polygon_boundary.is_simple
    if is_simple:
        print("Result: The polygon is simple (no self-intersections).")
    else:
        print("Result: The polygon is complex (has self-intersections).")
    return is_simple

def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Detect self-intersections in a polygon defined by (x, y) coordinates in a TXT file.")
    
    # Add the file path argument
    parser.add_argument(
        'filepath',
        type=str,
        help="Path to the TXT file containing the polygon coordinates."
    )
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Extract the file path
    file_path = args.filepath
    
    # Step 1: Read coordinates from the TXT file
    points = read_coordinates_array_txt(file_path)
    
    if not points:
        print("Exiting due to errors in reading the file.")
        return
    
    # Step 2: Undo the SceneKit transformation to get original points
    points = undo_scenekit_transformation(points)

    # Step 2: Ensure the polygon is closed
    points = ensure_polygon_closed(points)
    
    # Step 3: Validate the polygon
    if not validate_polygon(points):
        print("Exiting due to invalid polygon data.")
        return
    
    # Step 4: Detect self-intersections
    detect_self_intersections(points)
    
    # End of script

if __name__ == "__main__":
    main()
