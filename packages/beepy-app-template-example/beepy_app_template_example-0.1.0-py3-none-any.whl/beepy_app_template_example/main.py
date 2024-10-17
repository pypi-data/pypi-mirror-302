from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Label


class TemplateApp(App):
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield Label("Get writing your new app!")
        yield Footer()

    def on_mount(self) -> None:
        pass

    def sample_add_method(self, a: int, b: int) -> int:
        return a + b


def main() -> None:
    TemplateApp().run()


if __name__ == "__main__":
    main()
