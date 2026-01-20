import threading
import queue
import pythoncom
import time
import platform
from Helper import log_debug_message

# Conditional imports for cross-platform support
if platform.system() == "Windows":
    import win32com.client
else:
    import pyttsx3


class TextToSpeech:
    def __init__(self):
        self._request_queue = queue.Queue()
        self._speech_finished_event = threading.Event()
        self._exit_flag = False
        self._is_windows = platform.system() == "Windows"
        
        # Start a dedicated worker thread for all engine operations
        # This solves the COM thread affinity issue with SAPI5
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True, name="TTSWorkerThread")
        self._worker_thread.start()
        
        engine_name = "SAPI.SpVoice (Native)" if self._is_windows else "pyttsx3 (Cross-platform)"
        log_debug_message("TextToSpeech", f"TTS Worker thread started using {engine_name}.")

    def Speak(self, string):
        """
        Submits a speech request to the worker thread and waits for it to finish.
        Returns as soon as the current string has been spoken.
        """
        try:
            log_debug_message("TextToSpeech", f"Speak requested: {string}")
            self._speech_finished_event.clear()
            self._request_queue.put(string)
            
            # Wait for the worker to signal that speech is complete
            self._speech_finished_event.wait()
            log_debug_message("TextToSpeech", f"Speak returned: {string}")
        except Exception as e:
            log_debug_message("TextToSpeech", f"ERROR: Speak function failed: {e}")

    def _worker_loop(self):
        """
        Main loop for the dedicated TTS thread. 
        Detects platform and uses appropriate engine sequentially.
        """
        try:
            while not self._exit_flag:
                # Step 1: Wait for a speech request
                text = None
                while not self._exit_flag:
                    try:
                        text = self._request_queue.get(timeout=0.5)
                        break 
                    except queue.Empty:
                        continue 

                if text is not None:
                    if self._is_windows:
                        self._handle_windows_speech(text)
                    else:
                        self._handle_unix_speech(text)

                    # Signal completion
                    self._speech_finished_event.set()
                    
                    # Delay to allow resources/audio devices to settle
                    time.sleep(0.5)
        except Exception as e:
            log_debug_message("TextToSpeech", f"ERROR: TTS Worker loop crashed: {e}")
            self._speech_finished_event.set()

    def _handle_windows_speech(self, text):
        """Windows-specific speech using direct SAPI5 for stability."""
        pythoncom.CoInitialize()
        try:
            log_debug_message("TextToSpeech", "Worker: Initializing SAPI.SpVoice...")
            voice = win32com.client.Dispatch("SAPI.SpVoice")
            
            log_debug_message("TextToSpeech", f"Worker: Speaking (Windows/Native): {text}")
            # 0 = Synchronous speak (blocks until finished)
            voice.Speak(text, 0)
            
            del voice
            log_debug_message("TextToSpeech", "Worker: SAPI Voice released.")
        except Exception as e:
            log_debug_message("TextToSpeech", f"ERROR: Windows SAPI operation failed: {e}")
        finally:
            pythoncom.CoUninitialize()

    def _handle_unix_speech(self, text):
        """Cross-platform speech fallback using pyttsx3."""
        try:
            log_debug_message("TextToSpeech", "Worker: Initializing pyttsx3...")
            engine = pyttsx3.init()
            engine.setProperty("rate", 150)
            
            log_debug_message("TextToSpeech", f"Worker: Speaking (Unix/pyttsx3): {text}")
            engine.say(text)
            engine.runAndWait()
            
            engine.stop()
            del engine
            log_debug_message("TextToSpeech", "Worker: pyttsx3 engine released.")
        except Exception as e:
            log_debug_message("TextToSpeech", f"ERROR: Unix/pyttsx3 operation failed: {e}")

    def Shutdown(self):
        """Stops the worker thread."""
        log_debug_message("TextToSpeech", "Shutdown requested for TTS worker...")
        self._exit_flag = True
        if self._worker_thread.is_alive():
            log_debug_message("TextToSpeech", "Joining TTS worker thread...")
            self._worker_thread.join(timeout=2.0)
            log_debug_message("TextToSpeech", "TTS worker thread joined.")
