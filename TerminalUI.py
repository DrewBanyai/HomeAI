import threading
import json
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from Helper import log_debug_message

class TerminalUI(App):
    """A Textual app to manage HomeAI."""

    TITLE = "HomeAI"
    CSS_PATH = "TerminalUI.css"

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    
    ENABLE_COMMAND_PALETTE = False  # Disable the command palette button

    dark = reactive(True) # Dark mode is default

    def __init__(self, home_ai_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.home_ai = home_ai_instance
        self.home_ai_thread = None
        self.conversation_history = []
        self.weather_timer = None
        log_debug_message("TerminalUI", f"TerminalUI initialized. Initial self.dark={self.dark}")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        with Horizontal(id="custom_header"):
            yield Button("X", id="close_button", variant="error")
            yield Static(self.TITLE, id="header_title")
        yield Container(
            Static("Status: Initializing...", id="status"),
            Static("Currently Playing: None", id="currently_playing"),
            Container(
                Static("--- Conversation History ---", classes="command-history-title"),
                Static(id="command_history_box"),
                id="command_history_container"
            ),
            Container(
                Static("Weather Report", classes="weather-report-title"),
                Static(id="weather_report_box"),
                id="weather_report_container"
            ),
            id="main_container"
        )
        yield Footer()

    def watch_dark(self, dark: bool) -> None:
        """Called when dark reactive property changes."""
        log_debug_message("TerminalUI", f"watch_dark called with dark={dark}")
        # Update the app's CSS classes
        self.set_class(dark, "-dark-mode")
        self.set_class(not dark, "-light-mode")
        
        try:
            # Safely apply to the active screen
            if self.screen:
                self.screen.set_class(dark, "-dark-mode")
                self.screen.set_class(not dark, "-light-mode")
        except Exception:
            # Catch all screen access errors during init/shutdown
            pass
        log_debug_message("TerminalUI", f"App classes after watch_dark: {self.classes}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id in ["shutdown_button", "close_button"]:
            log_debug_message("TerminalUI", f"{event.button.id} pressed. Exiting application.")
            self.exit()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        log_debug_message("TerminalUI", "action_toggle_dark called.")
        log_debug_message("TerminalUI", f"Before toggle: self.dark={self.dark}")
        self.dark = not self.dark
        log_debug_message("TerminalUI", f"After toggle: self.dark={self.dark}")

    def update_status(self, status: str):
        """Update the status display."""
        self.query_one("#status").update(f"Status: {status}")

    def update_currently_playing(self, text: str):
        """Update the currently playing display."""
        self.query_one("#currently_playing").update(f"Currently Playing: {text}")

    def add_line_to_history(self, prefix: str, text: str):
        """Add a line to the conversation history and update the display."""
        # Check for endline character first
        newline_index = text.find('\n')
        if newline_index != -1:
            text = text[:newline_index] + "..."

        # Format and truncate the line
        line = f"{prefix}{text}"
        if len(line) > 60: # Corrected truncation length to 60 characters
            line = line[:57] + "..." # 57 characters + "..." = 60
        
        self.conversation_history.append(line)
        # Keep only the last 6 lines
        self.conversation_history = self.conversation_history[-6:]
        
        history_display = "\n".join(self.conversation_history)
        self.query_one("#command_history_box").update(history_display)

    def generate_weather_item(self, code, high, low, day):
        """Format a single weather icon with its temperatures and day name."""
        from _env import WEATHER_ASCII
        icon = WEATHER_ASCII.get(code, list(WEATHER_ASCII.values())[0])
        lines = icon.split("\n")
        
        # Center the day name on the top border (index 0)
        # The line is usually "==============" (14 chars)
        day_text = day.center(12)
        lines[0] = f"={day_text}="

        # Format temperatures on the 9th line (index 8)
        # The line is usually "=            ="
        temp_text = f"H:{high} L:{low}"
        # Center the temp text within the 12 characters between borders
        padded_temp = temp_text.center(12)
        lines[8] = f"={padded_temp}="
        
        return lines

    def update_weather_report(self, weather_data_json: str = None):
        """Generate and display weather reports from a JSON string."""
        from _env import WEATHER_ASCII
        import random

        if weather_data_json:
            try:
                weather_data = json.loads(weather_data_json)
            except Exception as e:
                log_debug_message("TerminalUI", f"Error parsing weather JSON: {e}")
                return
        else:
            # Fallback to random data if none provided (for initialization)
            codes = list(WEATHER_ASCII.keys())
            weather_data = []
            for i in range(7):
                code = random.choice(codes)
                high = random.randint(30, 95)
                low = random.randint(high - 20, high - 2)
                weather_data.append({"code": code, "high": high, "low": low, "day": f"Day {i+1}"})
        
        all_items_lines = []
        for item in weather_data:
            code = item.get("code")
            high = item.get("high")
            low = item.get("low")
            day = item.get("day", "Unknown")
            all_items_lines.append(self.generate_weather_item(code, high, low, day))
            
        # Stitch lines horizontally
        final_lines = []
        for i in range(10):
            # Join line 'i' of all items side-by-side with 2 spaces
            combined_line = "  ".join(item[i] for item in all_items_lines)
            final_lines.append(combined_line)
            
        report_display = "\n".join(final_lines)
        self.query_one("#weather_report_box").update(report_display)
        # Show the container now that we have data
        self.query_one("#weather_report_container").display = True
        
        # Reset and start the 45-second auto-hide timer
        if self.weather_timer:
            self.weather_timer.cancel()
        self.weather_timer = self.set_timer(45, self.hide_weather_report)

    def hide_weather_report(self):
        """Hide the weather report container."""
        log_debug_message("TerminalUI", "Hiding weather report container.")
        self.query_one("#weather_report_container").display = False
        self.weather_timer = None

    async def on_mount(self) -> None:
        """Called when app is mounted."""
        # Ensure initial dark mode state is applied
        self.watch_dark(self.dark)
        
        log_debug_message("TerminalUI", f"on_mount called. self.dark={self.dark}")
        log_debug_message("TerminalUI", f"App classes on_mount: {self.classes}")
        self.home_ai.ui = self
        
        self.home_ai_thread = threading.Thread(target=self.home_ai.run)
        self.home_ai_thread.start()

    async def on_unmount(self) -> None:
        """Called when app is unmounted."""
        log_debug_message("TerminalUI", "on_unmount called.")
        self.home_ai.Exit = True
        if self.home_ai_thread:
            self.home_ai_thread.join()