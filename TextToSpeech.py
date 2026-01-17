import pyttsx3
import threading
import queue
import pythoncom
from Helper import log_debug_message


class TextToSpeech:
    def __init__(self):
        self._request_queue = queue.Queue()
        self._speech_finished_event = threading.Event()
        self._exit_flag = False
        
        # Start a dedicated worker thread for all engine operations
        # This solves the COM thread affinity issue with SAPI5
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()
        
        log_debug_message("TextToSpeech", "TTS Worker thread started.")

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
        Handles sequential initialization, speech, and teardown of engines.
        """
        # CRITICAL: SAPI5 requires COM initialization for each thread that uses it
        pythoncom.CoInitialize()
        
        try:
            while not self._exit_flag:
                # Step 1: Pre-initialize a fresh engine
                log_debug_message("TextToSpeech", "Worker: Initializing fresh engine...")
                engine = pyttsx3.init('sapi5')
                voice_list = engine.getProperty("voices")
                if voice_list:
                    engine.setProperty("voice", voice_list[0].id)
                engine.setProperty("rate", 150)
                log_debug_message("TextToSpeech", "Worker: Engine initialized and ready.")

                # Step 2: Wait for a speech request
                # We stay in this wait loop until we get a request or need to exit.
                text = None
                while not self._exit_flag:
                    try:
                        text = self._request_queue.get(timeout=1.0)
                        break # Got text, proceed to speak
                    except queue.Empty:
                        continue # Still waiting, check exit flag and loop back

                if text is not None:
                    # Step 3: Speak the text
                    log_debug_message("TextToSpeech", f"Worker: Speaking: {text}")
                    engine.say(text)
                    engine.runAndWait()
                    log_debug_message("TextToSpeech", f"Worker: Finished speaking: {text}")

                    # Step 4: Signal completion to the caller
                    self._speech_finished_event.set()

                    # Step 5: Shut down and discard the engine to reset state
                    # This ensures the next engine starts fresh and stable
                    engine.stop()
                    del engine
                    log_debug_message("TextToSpeech", "Worker: Engine discarded. Preparing next engine...")
                else:
                    # If we broke out of the wait loop without text, it means self._exit_flag is True.
                    engine.stop()
                    del engine

        except Exception as e:
            log_debug_message("TextToSpeech", f"ERROR: TTS Worker loop crashed: {e}")
            # Ensure the caller isn't hung if the worker dies
            self._speech_finished_event.set()
        finally:
            pythoncom.CoUninitialize()

    def Shutdown(self):
        """Stops the worker thread."""
        self._exit_flag = True
        if self._worker_thread.is_alive():
            self._worker_thread.join(timeout=2.0)
