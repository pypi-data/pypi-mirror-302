from kivy.uix.button import Button as KivyButton
from kivy.graphics import Line, Color
from kivy.core.window import Window as KivyWindow
from kivy.core.text import LabelBase


class BasicButton:
    _window_bound = False  # Track if the window mouse binding is set up

    def __init__(self, window, x, y, width=140, height=50, text="CLICK ME",
                 font="Roboto", font_size=16, font_color="#FFFFFF",
                 bold=False, italic=False, underline=False, strikethrough=False,
                 idle_color="#f9b732", hover_color="#ffd278", clicked_color="#d1910f",
                 border_color=(0, 0, 0, 0), border_thickness=0,
                 on_hover=None, on_click=None, on_release=None, name=None):  # New parameter to force window binding
        # Initialize button properties
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.idle_color = idle_color
        self.hover_color = hover_color
        self.clicked_color = clicked_color
        self.font_color = font_color
        self.border_color = border_color
        self.border_thickness = border_thickness
        self.font_size = font_size
        self.on_click = on_click
        self.on_release = on_release
        self.on_hover = on_hover  # Store the hover callback function
        self.name = name
        self.is_pressed = False  # Track if the button is pressed

        # Text styling options
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.strikethrough = strikethrough

        # Apply text styles to the button label
        self.text = self.apply_markup(text)

        # Register font if a file path is provided
        if font.endswith((".ttf", ".otf")):
            LabelBase.register(name="CustomFont", fn_regular=font)
            self.font_name = "CustomFont"
        else:
            self.font_name = font

        # Create a Kivy button widget with markup enabled
        self.button_widget = KivyButton(
            text=self.text,
            size=(self.width, self.height),
            pos=(self.x, self.y),  # Positioning will work with FloatLayout
            background_normal='',  # Disable default Kivy background
            background_down='',  # Disable default Kivy down state
            background_color=self.idle_color,
            color=self.font_color,
            font_name=self.font_name,
            font_size=self.font_size,
            markup=True,  # Enable BBCode-style tags
            size_hint=(None, None)  # Disable size_hint to manually set size
        )

        # Draw the custom border
        self.draw_border()

        # Bind events for click, release, and hover callbacks
        self.button_widget.bind(on_press=self.handle_click)  # Use internal click handler
        self.button_widget.bind(on_release=self.handle_release)  # Always bind release for safety



        force_bind = False
        # Ensure window mouse binding is done as needed
        if force_bind or not BasicButton._window_bound:
            KivyWindow.bind(mouse_pos=self.on_mouse_pos)
            BasicButton._window_bound = True

        # Add the button to the window
        window.add_widget(self.button_widget)

    def apply_markup(self, text):
        """Apply markup tags to the text based on style properties."""
        styled_text = text
        if self.strikethrough:
            styled_text = f"[s]{styled_text}[/s]"
        if self.underline:
            styled_text = f"[u]{styled_text}[/u]"
        if self.italic:
            styled_text = f"[i]{styled_text}[/i]"
        if self.bold:
            styled_text = f"[b]{styled_text}[/b]"
        return styled_text

    def draw_border(self):
        """Draw a custom border around the button."""
        with self.button_widget.canvas.before:
            Color(*self.border_color)  # Set the border color
            Line(
                rectangle=(
                    self.button_widget.x, self.button_widget.y, self.button_widget.width, self.button_widget.height),
                width=self.border_thickness
            )

    def handle_click(self, instance):
        """Handle the button click event and change the color to clicked state."""
        self.is_pressed = True
        self.update_button_color(self.clicked_color)
        if self.on_click:
            self.on_click(self)  # Invoke the click callback

    def handle_release(self, instance):
        """Handle the button release event and revert color based on mouse position."""
        self.is_pressed = False
        if self.on_release:
            self.on_release(self)  # Invoke the release callback
        self.on_mouse_pos(None, KivyWindow.mouse_pos)  # Re-check hover state

    def on_mouse_pos(self, window, pos):
        """Detect hover by checking if the mouse is within the button area."""
        if self.is_mouse_hovering(pos):
            if self.is_pressed:
                self.update_button_color(self.clicked_color)
            else:
                self.update_button_color(self.hover_color)
            if self.on_hover:
                self.on_hover(self)  # Invoke the hover callback
        else:
            self.update_button_color(self.idle_color)

    def update_button_color(self, color):
        """Update the button's background color."""
        self.button_widget.background_color = color

    def is_mouse_hovering(self, pos):
        """Check if the mouse is within the button's boundaries."""
        return (self.button_widget.x <= pos[0] <= self.button_widget.x + self.button_widget.width and
                self.button_widget.y <= pos[1] <= self.button_widget.y + self.button_widget.height)

    def set_text(self, text):
        """Update the button text content."""
        self.text = self.apply_markup(text)
        self.button_widget.text = self.text

    def set_font(self, font):
        """Set a new font for the button text."""
        if font and font.endswith((".ttf", ".otf")):
            LabelBase.register(name="CustomFont", fn_regular=font)
            self.font_name = "CustomFont"
        else:
            self.font_name = font
        self.button_widget.font_name = self.font_name

    def set_font_size(self, font_size):
        """Set a new font size for the button text."""
        self.font_size = font_size
        self.button_widget.font_size = self.font_size

    def set_color(self, color):
        """Set the color of the button text."""
        self.font_color = color
        self.button_widget.color = self.font_color


if __name__ == "__main__":
    import pyvisual as pv

    window = pv.Window()
    # Create a button with various text styles
    button = BasicButton(
        window=window,
        x=325, y=275,
        width=200, height=60,
        text="Styled Button",
        font_size=24,
        bold=True,  # Bold text
        italic=True

    )

    window.show()
