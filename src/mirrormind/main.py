import kivy
from kivy.lang import Builder
from kivy.config import Config
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
import ollama

# set kivy version
kivy.require("2.3.0")

# get model list from ollama
model_list = [x["name"] for x in ollama.list()["models"]]

class MirrorMindMainApp(App):
    """
    A simple Kivy application with a main window, text output and input fields, and buttons.
    The main window spawns in the center of the screen at 65% of the screen size.
    The application features a dark gray theme with an almost white title.
    """

    def build(self):
        """
        Build and return the root widget.
        """
        self.title = '𝕞𝕚𝕣𝕣𝕠𝕣𝕞𝕚𝕟𝕕'
        
        # Calculate 65% of the screen size
        screen_width, screen_height = Window.size
        initial_width = screen_width * 0.65
        initial_height = screen_height * 0.65

        # Set the initial and minimum size of the window
        Window.size = (initial_width, initial_height)
        Config.set("graphics", "resizable", True)
        Window.minimum_width, Window.minimum_height = 1280, 720
        
        # Main layout
        layout = BoxLayout(
            orientation="vertical", padding=10, spacing=10, size_hint=(1, 1)
        )
        

        # Horizontal layout for the label and drop-down
        dropdown_layout = BoxLayout(size_hint_y=0.1)

        # Label
        label = Label(text="Model: ", size_hint_x=0.3)

        # Drop-down menu (Spinner)
        self.spinner = Spinner(
            text=model_list[0],
            values=model_list,
            size_hint_x=0.7
        )

        # Add widgets to the horizontal layout
        dropdown_layout.add_widget(label)
        dropdown_layout.add_widget(self.spinner)

        # Add the horizontal layout to the main layout
        layout.add_widget(dropdown_layout)      
        

        # Text output field inside a scroll view
        self.text_output = TextInput(
            text="",
            size_hint=(1, None),
            font_size=25,
            multiline=True,
            readonly=True,
            foreground_color=[0.9, 0.9, 0.9, 1],
            background_color=[0.2, 0.2, 0.2, 1],
        )
        self.text_output.bind(minimum_height=self.text_output.setter('height'))
        
        # Here, setting a large enough initial height for the TextInput to ensure it visually occupies the space
        self.text_output.height = 500  # Example height, adjust based on your UI's needs

        scroll_view = StyledScrollView()
        scroll_view.add_widget(self.text_output)
        layout.add_widget(scroll_view)

        # Text input field
        self.text_input = TextInput(
            text="",
            size_hint=(1.0, 0.2),
            multiline=True,
            foreground_color=[0.8, 0.8, 0.8, 1],
            background_color=[0.2, 0.2, 0.2, 1],
        )
        layout.add_widget(self.text_input)

        # Button layout
        button_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)

        # Left-aligned buttons
        left_buttons_layout = BoxLayout(size_hint_x=None, width=210, spacing=10)
        self.btn_topics = Button(text="topics", size_hint_x=None, width=100)
        self.btn_settings = Button(text="settings", size_hint_x=None, width=100)
        left_buttons_layout.add_widget(self.btn_topics)
        left_buttons_layout.add_widget(self.btn_settings)

        # Right-aligned buttons
        right_buttons_layout = BoxLayout(size_hint_x=None, width=210, spacing=10)
        self.btn_export = Button(
            text="export", size_hint_x=None, width=100, disabled=True
        )
        self.btn_send = Button(text="send", size_hint_x=None, width=100, disabled=True)
        right_buttons_layout.add_widget(self.btn_export)
        right_buttons_layout.add_widget(self.btn_send)

        # Add left and right button layouts to the main button layout
        button_layout.add_widget(left_buttons_layout)
        button_layout.add_widget(AnchorLayout(anchor_x="right", size_hint_x=1))
        button_layout.add_widget(right_buttons_layout)

        layout.add_widget(button_layout)

        # Bindings
        self.text_input.bind(text=self.on_text)  # type: ignore
        self.text_input.bind(on_keyboard=self.on_key_down)
        self.btn_send.bind(on_press=self.press_send)
        
        self.btn_topics.bind(on_press=self.press_topics)
        self.btn_settings.bind(on_press=self.press_topics)

        return layout
    
    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        """
        Handles key down events on the text input field.
        Specifically looking for the ENTER key press.
        """
        if keycode == 40:  # 40 is the keycode for ENTER
            self.process_input()
            return True  # return True to accept the key press
        return False

    def press_send(self, instance):
        if len(self.text_input.text.strip()) > 0:
            self.btn_send.disabled = True
            send_status = self.send_prompt(self.text_input.text)
            if send_status:
                self.btn_send.disabled = False
        pass

    def press_settings(self, instance):
        show_niy_msg()
        pass

    def press_topics(self, instance):
        show_niy_msg()
        pass

    
    def process_input(self):
        """
        Processes the input text when ENTER is pressed.
        Calls an external function and clears the input if the function returns True.
        Also, defocuses the text input field.
        """
        result = self.send_prompt(self.text_input.text)
        if result:
            self.text_input.text = ''
        self.text_input.focus = False

    def on_text(self, instance, value):
        """
        Callback for text input changes. Enables the 'send' button if the text input field is not empty.

        :param instance: The instance of the text input widget.
        :param value: The current text in the text input widget.
        """
        # Enable 'send' button if text input is not empty
        self.btn_send.disabled = len(value.strip()) == 0
        
    def send_prompt(self, prompt: str) -> bool:
        try:
            
            stream = ollama.chat(
                model=self.spinner.text,
                messages=[{'role': 'user', 'content': str(prompt)}],
                stream=True,
            )
        
            for chunk in stream:
                self.text_output.text = self.text_output.text + str(chunk['message']['content'])
            self.text_output.scroll_y = 0
            return True
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
        finally:
            return False

# show a message dialog
def show_message(title="", message=""):
    box = BoxLayout(orientation='vertical', padding=(10))
    box.add_widget(Label(text=message))
    close_btn = Button(text="Close", size_hint=(1, 0.2))
    
    popup = Popup(title=title, content=box, size_hint=(None, None), size=(400, 300))
    close_btn.bind(on_press=popup.dismiss)
    box.add_widget(close_btn)
    
    popup.open()

def show_niy_msg():
    show_message("nope", "not implemented, yet.")

class StyledScrollView(ScrollView):
    """
    Define a customized scroll view.

    Args:
        ScrollView (_type_): Just the default Kivy ScrollView
    """
    def __init__(self, **kwargs):
        super(StyledScrollView, self).__init__(**kwargs)
        self.bar_width = 10
        self.bar_color = [0.8, 0.8, 0.8, 1]
        self.do_scroll_x=False,  # Disable horizontal scrolling
        self.do_scroll_y=True,  # Enable vertical scrolling        
        self.bar_inactive_color: [0.5, 0.5, 0.5, 1]  # Darker red when not scrolling
        self.scroll_type: ['bars']  # Enable scrollbars and content scrolling
        self.effect_cls: 'ScrollEffect'  # Use the default scroll effect
        self.bar_pos_x: 'right'  # Position the vertical scrollbar on the right
        self.bar_pos_y: 'bottom'  # Position the horizontal scrollbar at the bottom



if __name__ == "__main__":
    MirrorMindMainApp().run()
