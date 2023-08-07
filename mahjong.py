import pyglet
from pyglet.gl import glClearColor, GL_COLOR_BUFFER_BIT
import random

white_pieces = True


def sort_hand(hand):
    # Sorting function for the pieces (you may customize this based on your rules)
    def sort_key(piece_name):
        # Define the sorting order for numbered pieces (1 to 9) based on the prefix (sou, man, pin)
        numbered_order = {"Sou": 0, "Man": 1, "Pin": 2}

        # Extract the prefix (sou, man, or pin) and the number from the piece name
        prefix, number = piece_name[:-1], piece_name[-1]

        # Return a tuple with two elements: the sorting priority and the piece name
        return (numbered_order.get(prefix, 3), prefix, number)

    return sorted(hand, key=sort_key)


class player:
    def __init__(self, pieces):
        self.pieces = sort_hand(pieces)


def get_sprite(image_path, scale_factor, x, y, rot):
    image = pyglet.image.load(image_path)
    sprite = pyglet.sprite.Sprite(image, x=x, y=y)
    sprite.update(scale=scale_factor, rotation=rot)
    return sprite


def show_hands(hands, window_width, window_height):
    piece = pyglet.resource.image("Front.png")
    piece_width, piece_height = piece.width, piece.height
    scale_factor = (
        1 * (min(window_width, window_height) / 16) / (max(piece_width, piece_height))
    )
    true_piece_width = piece_width * scale_factor
    for j, hand in enumerate(hands):
        for i, piece_name in enumerate(hand):
            spacing = 5
            start_x = window_width / 2 - (6.5 * (true_piece_width + spacing))
            start_y = window_height / 2 - (6.5 * (true_piece_width + spacing))
            start_x_2 = window_width / 2 + (6.5 * (true_piece_width + spacing))
            start_y_2 = window_height / 2 + (6.5 * (true_piece_width + spacing))
            piece_path = ""
            if white_pieces:
                piece_path = f"white_pieces/{piece_name}.png"
            else:
                piece_path = f"black_pieces/{piece_name}.png"
            try:
                x_pos = 0
                y_pos = 0
                rot = 0
                if j == 0:
                    x_pos = start_x + (i * (true_piece_width + spacing))
                    y_pos = start_y - 2 * true_piece_width
                if j == 1:
                    x_pos = start_x_2 + 2 * true_piece_width
                    y_pos = start_y + (i * (true_piece_width + spacing))
                    rot = 270
                if j == 2:
                    x_pos = start_x_2 - (i * (true_piece_width + spacing))
                    y_pos = start_y_2 + 2 * true_piece_width
                    rot = 180
                if j == 3:
                    x_pos = start_x - 2 * true_piece_width
                    y_pos = start_y_2 - (i * (true_piece_width + spacing))
                    rot = 90
                sprite1 = get_sprite(piece_path, scale_factor, x_pos, y_pos, rot)
                sprite1.draw()
            except FileNotFoundError:
                print(f"Image not found for {piece_name}")


suits = ["Sou", "Man", "Pin"]

ranks = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

# Define special tiles
special_tiles = ["East", "West", "North", "South", "Blank", "Fa", "Chun"]

# Create the deck of tiles
deck = []

for suit in suits:
    for rank in ranks:
        for _ in range(4):
            deck.append(f"{suit}{rank}")

for _ in range(4):
    deck.extend(special_tiles)

# Shuffle the deck
random.shuffle(deck)


def deal(num_tiles):
    hand_1 = []
    hand_2 = []
    hand_3 = []
    hand_4 = []
    for _ in range(num_tiles):
        hand_1.append(deck.pop())
        hand_2.append(deck.pop())
        hand_3.append(deck.pop())
        hand_4.append(deck.pop())
    return (sort_hand(hand_1), sort_hand(hand_2), sort_hand(hand_3), sort_hand(hand_4))


def draw_window(hands):
    window = pyglet.window.Window(fullscreen=True)
    green_color = (0.0, 0.3, 0.0, 1.0)
    window_width, window_height = window.get_size()

    button_label = pyglet.text.Label(
        "Toggle",
        font_size=24,
        x=window.width // 2,
        y=window.height // 2,
        anchor_x="center",
        anchor_y="center",
    )
    button_x = (
        button_label.content_width // 2 + 10
    )  # 10 pixels padding from the left edge
    button_y = (
        window.height - button_label.content_height // 2 - 10
    )  # 10 pixels padding from the top edge
    button_x = (
        button_label.content_width // 2 + 10
    )  # 10 pixels padding from the left edge
    button_y = (
        window.height - button_label.content_height // 2 - 10
    )  # 10 pixels padding from the top edge
    button_label.x = button_x
    button_label.y = button_y

    # Create a rectangle around the button without covering it
    padding = 5
    rect_x = button_label.x - button_label.content_width // 2 - padding
    rect_y = button_label.y - button_label.content_height // 2 - padding
    rect_width = button_label.content_width + 2 * padding
    rect_height = button_label.content_height + 2 * padding

    # Set the color of the rectangle (grey)
    rect_color = (128, 128, 128)  # RGB values for grey

    # Create the grey background rectangle
    button_rect = pyglet.shapes.Rectangle(
        x=rect_x,
        y=rect_y,
        width=rect_width,
        height=rect_height,
        color=rect_color,
    )

    # Set the color of the border rectangle (black)
    border_color = (0, 0, 0)  # RGB values for black

    # Create the black border rectangle (slightly smaller than the grey background)
    border_padding = 1
    border_rect = pyglet.shapes.Rectangle(
        x=rect_x + border_padding,
        y=rect_y + border_padding,
        width=rect_width - 2 * border_padding,
        height=rect_height - 2 * border_padding,
        color=border_color,
    )

    @window.event
    def on_draw():
        glClearColor(*green_color)
        window.clear()
        button_rect.draw()
        border_rect.draw()
        button_label.draw()
        show_hands(hands, window_width, window_height)

    def on_button_click(x, y):
        global white_pieces
        white_pieces = not white_pieces
        print("Button clicked! Toggle state:", white_pieces)

    # Register the event handler for the button click
    @window.event
    def on_mouse_press(x, y, button, modifiers):
        # Check if the mouse click happened within the bounding box of the button
        if (
            button_label.x - button_label.content_width // 2
            <= x
            <= button_label.x + button_label.content_width // 2
            and button_label.y - button_label.content_height // 2
            <= y
            <= button_label.y + button_label.content_height // 2
        ):
            on_button_click(x, y)

    pyglet.app.run()


def main():
    p1, p2, p3, p4 = deal(num_tiles=13)

    while True:
        print("Your hand:", p1)
        print("p2 hand:", p2)
        print("p3 hand:", p3)
        print("p4 hand:", p4)
        draw_window([p1, p2, p3, p4])
        break


if __name__ == "__main__":
    main()
