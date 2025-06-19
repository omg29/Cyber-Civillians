import pygame
import math

def getRotatedImage(image, rect, angle):
    """
    Rotate a surface (image) by a given angle while keeping its center position.

    Args:
        image: The pygame.Surface to rotate.
        rect: The pygame.Rect of the original image.
        angle: The angle in degrees to rotate the image.

    Returns:
        rotated_image: The rotated pygame.Surface.
        rotated_rect: The pygame.Rect of the rotated image, centered on original position.

    Why:
        Rotating an image changes its bounding rectangle size and shape.
        This function recalculates the rect so the rotated image stays centered
        where the original image was, preventing "jumping" positions during rotation.
    """
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=rect.center)
    return rotated_image, rotated_rect

def angleBetweenPoints(x1, y1, x2, y2):
    """
    Calculate the angle in degrees from point (x1, y1) to (x2, y2).

    Args:
        x1, y1: Coordinates of the first point (e.g., player position).
        x2, y2: Coordinates of the second point (e.g., mouse position).

    Returns:
        angle: The angle in degrees pointing from (x1, y1) to (x2, y2).

    Why:
        Useful for aiming or orienting sprites towards a target.
        Uses atan2 for correct quadrant calculation.
        Negative y is used because pygame's y-axis increases downward,
        so this flips the vertical direction for correct math orientation.
    """
    dx = x2 - x1
    dy = y2 - y1
    angle = math.degrees(math.atan2(-dy, dx))
    return angle

def centeringCoords(thingy, screen):
    """
    Calculate coordinates to center a surface 'thingy' on the 'screen'.

    Args:
        thingy: A pygame.Surface or any object with get_width() and get_height().
        screen: The pygame display Surface.

    Returns:
        (new_x, new_y): Coordinates to position 'thingy' so it is centered on 'screen'.

    Why:
        When positioning UI elements or images, centering them improves user experience.
        This helper makes centering easy by handling the math for you.
    """
    new_x = screen.get_width() / 2 - thingy.get_width() / 2
    new_y = screen.get_height() / 2 - thingy.get_height() / 2
    return new_x, new_y
