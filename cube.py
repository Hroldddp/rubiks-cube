import pygame
import math
from pygame.math import Vector3

# Initialize Pygame
pygame.init()

# Set up the display
infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h
display = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("3D Rubik's Cube")

# Colors for the cube faces
colors = {
    'white': (255, 255, 255),
    'yellow': (255, 255, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'red': (255, 0, 0),
    'orange': (255, 165, 0)
}

# Cube properties
cube_size = 3
cube_dim = 60  # Increased from 50 to 60
gap = 1

# Camera properties
camera_distance = 600  # Increased from 500 to 600 to accommodate larger cube

# Rotation angles and speed
angle_x, angle_y, angle_z = 0, 0, 0
rotation_speed = 0.02

def rotate_point(point, angle_x, angle_y, angle_z):
    # Rotate around Z-axis
    x = point[0] * math.cos(angle_z) - point[1] * math.sin(angle_z)
    y = point[0] * math.sin(angle_z) + point[1] * math.cos(angle_z)
    z = point[2]
    
    # Rotate around Y-axis
    x, z = x * math.cos(angle_y) - z * math.sin(angle_y), x * math.sin(angle_y) + z * math.cos(angle_y)
    
    # Rotate around X-axis
    y, z = y * math.cos(angle_x) - z * math.sin(angle_x), y * math.sin(angle_x) + z * math.cos(angle_x)
    
    return Vector3(x, y, z)

def project_point(point):
    x = point[0] * camera_distance / (point[2] + camera_distance) + width / 2
    y = point[1] * camera_distance / (point[2] + camera_distance) + height / 2
    return int(x), int(y)

def draw_face(vertices, color):
    pygame.draw.polygon(display, color, vertices)
    pygame.draw.polygon(display, (0, 0, 0), vertices, 1)  # Draw black outline

def draw_cube():
    faces = []
    for x in range(cube_size):
        for y in range(cube_size):
            for z in range(cube_size):
                cube_pos = Vector3(
                    (x - cube_size // 2) * (cube_dim + gap),
                    (y - cube_size // 2) * (cube_dim + gap),
                    (z - cube_size // 2) * (cube_dim + gap)
                )
                
                vertices = [
                    rotate_point(Vector3(cube_pos.x, cube_pos.y, cube_pos.z), angle_x, angle_y, angle_z),
                    rotate_point(Vector3(cube_pos.x + cube_dim, cube_pos.y, cube_pos.z), angle_x, angle_y, angle_z),
                    rotate_point(Vector3(cube_pos.x + cube_dim, cube_pos.y + cube_dim, cube_pos.z), angle_x, angle_y, angle_z),
                    rotate_point(Vector3(cube_pos.x, cube_pos.y + cube_dim, cube_pos.z), angle_x, angle_y, angle_z),
                    rotate_point(Vector3(cube_pos.x, cube_pos.y, cube_pos.z + cube_dim), angle_x, angle_y, angle_z),
                    rotate_point(Vector3(cube_pos.x + cube_dim, cube_pos.y, cube_pos.z + cube_dim), angle_x, angle_y, angle_z),
                    rotate_point(Vector3(cube_pos.x + cube_dim, cube_pos.y + cube_dim, cube_pos.z + cube_dim), angle_x, angle_y, angle_z),
                    rotate_point(Vector3(cube_pos.x, cube_pos.y + cube_dim, cube_pos.z + cube_dim), angle_x, angle_y, angle_z)
                ]
                
                projected_vertices = [project_point(v) for v in vertices]
                
                # Store faces with their average z-coordinate for depth sorting
                faces.extend([
                    (sum(v.z for v in vertices[0:4]) / 4, [projected_vertices[i] for i in [0, 1, 2, 3]], colors['red']),
                    (sum(v.z for v in vertices[4:8]) / 4, [projected_vertices[i] for i in [4, 5, 6, 7]], colors['orange']),
                    (sum(v.z for v in [vertices[0], vertices[1], vertices[5], vertices[4]]) / 4, [projected_vertices[i] for i in [0, 1, 5, 4]], colors['white']),
                    (sum(v.z for v in [vertices[2], vertices[3], vertices[7], vertices[6]]) / 4, [projected_vertices[i] for i in [2, 3, 7, 6]], colors['yellow']),
                    (sum(v.z for v in [vertices[0], vertices[3], vertices[7], vertices[4]]) / 4, [projected_vertices[i] for i in [0, 3, 7, 4]], colors['blue']),
                    (sum(v.z for v in [vertices[1], vertices[2], vertices[6], vertices[5]]) / 4, [projected_vertices[i] for i in [1, 2, 6, 5]], colors['green'])
                ])
    
    # Sort faces by z-coordinate (painter's algorithm)
    faces.sort(key=lambda f: f[0], reverse=True)
    
    # Draw sorted faces
    for _, face_vertices, color in faces:
        draw_face(face_vertices, color)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Add escape key to exit fullscreen
                running = False
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:  # Left mouse button
                dx, dy = event.rel
                angle_y += dx * 0.01
                angle_x += dy * 0.01

    # Auto-rotation
    angle_y += rotation_speed
    angle_x += rotation_speed / 2
    angle_z += rotation_speed / 3

    display.fill((0, 0, 0))  # Clear the screen
    draw_cube()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()