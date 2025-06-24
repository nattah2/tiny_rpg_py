import os

venv="myvenv"

if os.getenv("CURRENT_ENVIRONMENT") != "GAMEDEV":
    print("Error. Not within environment.")

print("You're in the gamedev environment.")

from textual.app import App, ComposeResult
from textual.widgets import Button, Label, Header, Footer

class MenuApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Press '1', '2', or 'q' to select an option:")
        yield Button("Option 1", id="option1")
        yield Button("Option 2", id="option2")
        yield Button("Quit", id="quit")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.exit()
        else:
            self.query_one(Label).update(f"You selected {event.button.id}")

    def on_key(self, event):
        if event.key == '1':
            self.query_one(Label).update("You pressed Option 1!")
        elif event.key == '2':
            self.query_one(Label).update("You pressed Option 2!")
        elif event.key == 'q':
            self.exit()

if __name__ == "__main__":
    MenuApp().run()
