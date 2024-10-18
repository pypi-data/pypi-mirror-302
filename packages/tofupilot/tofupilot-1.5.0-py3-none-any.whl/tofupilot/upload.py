import json
import openhtf
import websocket as websocket_client


class UploadToTofuPilot:
    def __init__(self, ws_url: str = "ws://localhost:3000/api/ws"):
        """Initialize the WebSocket connection."""
        self.ws_url = ws_url
        self.ws = None

    def open_socket(self):
        """Open a WebSocket connection."""
        self.ws = websocket_client.WebSocket()
        self.ws.connect(self.ws_url)

    def close_socket(self):
        """Close the WebSocket connection."""
        if self.ws:
            self.ws.close()

    def __call__(self, test_record):
        """Upload test results to TofuPilot and send real-time updates via WebSocket."""
        try:
            self.open_socket()

            # Send the final test result to the WebSocket
            final_results = {
                "status": "completed",
                "test_name": test_record.metadata.get("test_name", "Unnamed Test"),
                "outcome": str(test_record.outcome),
                "measurements": test_record.measurements,
            }
            self.ws.send(json.dumps(final_results))

        finally:
            self.close_socket()

    def send_phase_update(self, phase_name, phase_status):
        """Send real-time phase updates during test execution."""
        if self.ws:
            message = {
                "phase": phase_name,
                "status": phase_status,
            }
            self.ws.send(json.dumps(message))
