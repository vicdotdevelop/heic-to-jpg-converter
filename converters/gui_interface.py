"""
GUI Interface Module
Provides a graphical user interface for the HEIC converter.
"""
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Dict, Any, Callable, Optional
import threading
import queue

from .file_handler import process_input, SUPPORTED_FORMATS
from .logger import setup_logger

class LogHandler:
    """Custom log handler that redirects logs to the GUI."""
    
    def __init__(self, callback: Callable[[str, str], None]):
        """
        Initialize the log handler.
        
        Args:
            callback: Function to call with log level and message
        """
        self.callback = callback
        self.queue = queue.Queue()
        self.running = True
        self.thread = threading.Thread(target=self._process_queue)
        self.thread.daemon = True
        self.thread.start()
    
    def emit(self, level: str, msg: str):
        """
        Emit a log message.
        
        Args:
            level: Log level
            msg: Log message
        """
        self.queue.put((level, msg))
    
    def _process_queue(self):
        """Process log messages from the queue."""
        while self.running:
            try:
                level, msg = self.queue.get(block=True, timeout=0.1)
                self.callback(level, msg)
                self.queue.task_done()
            except queue.Empty:
                continue
    
    def stop(self):
        """Stop the log handler thread."""
        self.running = False
        if self.thread.is_alive():
            self.thread.join(timeout=1.0)


class HeicConverterApp(tk.Tk):
    """Main GUI application for HEIC converter."""
    
    def __init__(self):
        super().__init__()
        
        self.title("HEIC Image Converter")
        self.geometry("700x600")
        self.minsize(600, 500)
        
        self.logger = setup_logger()
        self.log_handler = None
        self.conversion_thread = None
        self.is_converting = False
        
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self):
        """Create GUI widgets."""
        # Frame for input options
        self.input_frame = ttk.LabelFrame(self, text="Input Options")
        
        # Input selection
        self.input_path_var = tk.StringVar()
        ttk.Label(self.input_frame, text="Input:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(self.input_frame, textvariable=self.input_path_var, width=50).grid(row=0, column=1, padx=5, pady=5, sticky="we")
        ttk.Button(self.input_frame, text="Browse File", command=self._browse_input_file).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(self.input_frame, text="Browse Folder", command=self._browse_input_folder).grid(row=0, column=3, padx=5, pady=5)
        
        # Output selection
        self.output_path_var = tk.StringVar()
        ttk.Label(self.input_frame, text="Output:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(self.input_frame, textvariable=self.output_path_var, width=50).grid(row=1, column=1, padx=5, pady=5, sticky="we")
        ttk.Button(self.input_frame, text="Browse", command=self._browse_output_folder).grid(row=1, column=2, padx=5, pady=5)
        
        # Frame for conversion settings
        self.settings_frame = ttk.LabelFrame(self, text="Conversion Settings")
        
        # Format selection
        ttk.Label(self.settings_frame, text="Output Format:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.format_var = tk.StringVar(value="jpg")
        format_combo = ttk.Combobox(self.settings_frame, textvariable=self.format_var, values=SUPPORTED_FORMATS, state="readonly")
        format_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Quality slider
        ttk.Label(self.settings_frame, text="Quality:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.quality_var = tk.IntVar(value=90)
        quality_frame = ttk.Frame(self.settings_frame)
        quality_frame.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        quality_slider = ttk.Scale(quality_frame, from_=1, to=100, orient="horizontal", variable=self.quality_var, length=200)
        quality_slider.pack(side="left", fill="x", expand=True)
        ttk.Label(quality_frame, textvariable=self.quality_var, width=3).pack(side="left", padx=5)
        
        # Metadata checkbox
        self.preserve_metadata_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.settings_frame, 
            text="Preserve metadata", 
            variable=self.preserve_metadata_var
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        # Threading options
        ttk.Label(self.settings_frame, text="Threads:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.threads_var = tk.StringVar(value="Auto")
        threads_values = ["Auto"] + [str(i) for i in range(1, os.cpu_count() + 1)]
        threads_combo = ttk.Combobox(self.settings_frame, textvariable=self.threads_var, values=threads_values, state="readonly", width=5)
        threads_combo.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Action buttons
        self.button_frame = ttk.Frame(self)
        self.convert_button = ttk.Button(self.button_frame, text="Convert", command=self._start_conversion)
        self.convert_button.pack(side="left", padx=5, pady=5)
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self._cancel_conversion, state="disabled")
        self.cancel_button.pack(side="left", padx=5, pady=5)
        
        # Progress bar
        self.progress_frame = ttk.Frame(self)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x", padx=5, pady=5, expand=True)
        
        # Log output
        self.log_frame = ttk.LabelFrame(self, text="Log")
        self.log_text = tk.Text(self.log_frame, wrap="word", height=12)
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(self.log_text, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text["yscrollcommand"] = scrollbar.set
        self.log_text.config(state="disabled")
    
    def _setup_layout(self):
        """Set up the layout for the GUI."""
        self.input_frame.pack(fill="x", expand=False, padx=10, pady=(10, 5))
        self.settings_frame.pack(fill="x", expand=False, padx=10, pady=5)
        self.button_frame.pack(fill="x", expand=False, padx=10, pady=5)
        self.progress_frame.pack(fill="x", expand=False, padx=10, pady=5)
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        # Make the input path column expandable
        self.input_frame.columnconfigure(1, weight=1)
    
    def _browse_input_file(self):
        """Open file browser to select input HEIC file."""
        file_path = filedialog.askopenfilename(
            title="Select HEIC file",
            filetypes=[("HEIC files", "*.heic *.HEIC *.heif *.HEIF"), ("All files", "*.*")]
        )
        if file_path:
            self.input_path_var.set(file_path)
            # Set default output path to same directory
            if not self.output_path_var.get():
                self.output_path_var.set(os.path.dirname(file_path))
    
    def _browse_input_folder(self):
        """Open folder browser to select input directory."""
        folder_path = filedialog.askdirectory(title="Select input folder")
        if folder_path:
            self.input_path_var.set(folder_path)
            # Set default output path to same directory
            if not self.output_path_var.get():
                self.output_path_var.set(folder_path)
    
    def _browse_output_folder(self):
        """Open folder browser to select output directory."""
        folder_path = filedialog.askdirectory(title="Select output folder")
        if folder_path:
            self.output_path_var.set(folder_path)
    
    def _log_to_gui(self, level: str, msg: str):
        """
        Add log message to the GUI log widget.
        
        Args:
            level: Log level
            msg: Log message
        """
        def _update_log():
            self.log_text.config(state="normal")
            if level.lower() == "error":
                self.log_text.insert("end", f"ERROR: {msg}\n", "error")
                self.log_text.tag_config("error", foreground="red")
            elif level.lower() == "warning":
                self.log_text.insert("end", f"WARNING: {msg}\n", "warning")
                self.log_text.tag_config("warning", foreground="orange")
            else:
                self.log_text.insert("end", f"{msg}\n")
            self.log_text.see("end")
            self.log_text.config(state="disabled")
        
        # Execute in main thread
        self.after(0, _update_log)
    
    def _start_conversion(self):
        """Start the conversion process in a separate thread."""
        # Validate inputs
        input_path = self.input_path_var.get().strip()
        output_path = self.output_path_var.get().strip()
        
        if not input_path:
            messagebox.showerror("Error", "Please select an input file or folder.")
            return
        
        if not os.path.exists(input_path):
            messagebox.showerror("Error", f"Input path does not exist: {input_path}")
            return
        
        if not output_path:
            messagebox.showerror("Error", "Please select an output folder.")
            return
        
        # Update UI for conversion
        self.is_converting = True
        self.convert_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.progress_var.set(0)
        
        # Clear log
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, "end")
        self.log_text.config(state="disabled")
        
        # Set up log handler
        self.log_handler = LogHandler(self._log_to_gui)
        
        # Get thread count
        thread_count = None
        if self.threads_var.get() != "Auto":
            try:
                thread_count = int(self.threads_var.get())
            except ValueError:
                thread_count = None
        
        # Start conversion in a separate thread
        self.conversion_thread = threading.Thread(
            target=self._run_conversion,
            args=(
                input_path,
                output_path,
                self.format_var.get(),
                self.quality_var.get(),
                self.preserve_metadata_var.get(),
                thread_count
            )
        )
        self.conversion_thread.daemon = True
        self.conversion_thread.start()
        
        # Start progress polling
        self._poll_conversion_progress()
    
    def _run_conversion(self, input_path: str, output_path: str, output_format: str, 
                       quality: int, preserve_metadata: bool, thread_count: Optional[int]):
        """
        Run the conversion process.
        
        Args:
            input_path: Input file or directory path
            output_path: Output directory path
            output_format: Output format
            quality: Output quality
            preserve_metadata: Whether to preserve metadata
            thread_count: Number of threads to use
        """
        try:
            # Create a custom logger for the GUI
            log_queue = queue.Queue()
            
            self._log_to_gui("info", f"Starting conversion from HEIC to {output_format.upper()}...")
            self._log_to_gui("info", f"Input: {input_path}")
            self._log_to_gui("info", f"Output: {output_path}")
            
            # Count total files for progress tracking
            total_files = 0
            if os.path.isdir(input_path):
                for root, _, files in os.walk(input_path):
                    total_files += sum(1 for f in files if f.lower().endswith(('.heic', '.heif')))
            elif os.path.isfile(input_path) and input_path.lower().endswith(('.heic', '.heif')):
                total_files = 1
            
            self.total_files = total_files
            self.processed_files = 0
            
            # Use a custom tracking function
            def file_processed_callback(result):
                if not self.is_converting:
                    return
                
                if result["success"] or result["skipped"]:
                    self.processed_files += 1
            
            # Process input
            results = process_input(
                input_path=input_path,
                output_dir=output_path,
                output_format=output_format,
                quality=quality,
                preserve_metadata=preserve_metadata,
                logger=self.logger,
                max_workers=thread_count
            )
            
            if self.is_converting:  # Check if user hasn't canceled
                # Display summary
                self._log_to_gui("info", "\nConversion Summary:")
                self._log_to_gui("info", f"Total files processed: {results['total']}")
                self._log_to_gui("info", f"Success: {results['success']}")
                self._log_to_gui("info", f"Failed: {results['failed']}")
                self._log_to_gui("info", f"Skipped: {results['skipped']}")
                
                if results['errors']:
                    self._log_to_gui("info", "\nErrors:")
                    for error in results['errors']:
                        self._log_to_gui("error", error)
                
                self._log_to_gui("info", "\nConversion complete!")
                
                # Show message box with results
                if results['failed'] == 0:
                    messagebox.showinfo("Conversion Complete", 
                                        f"Successfully converted {results['success']} files.\n"
                                        f"Skipped {results['skipped']} files.")
                else:
                    messagebox.showwarning("Conversion Complete with Errors",
                                          f"Converted: {results['success']}\n"
                                          f"Failed: {results['failed']}\n"
                                          f"Skipped: {results['skipped']}\n\n"
                                          f"Check the log for details.")
        except Exception as e:
            self._log_to_gui("error", f"An error occurred: {str(e)}")
            messagebox.showerror("Error", f"An error occurred during conversion:\n{str(e)}")
        finally:
            # Update UI when done
            self._conversion_finished()
    
    def _poll_conversion_progress(self):
        """Update the progress bar based on conversion progress."""
        if not self.is_converting:
            return
        
        # Update progress if we know the total files
        if hasattr(self, 'total_files') and self.total_files > 0:
            progress = (self.processed_files / self.total_files) * 100
            self.progress_var.set(progress)
        
        # Schedule next update
        self.after(100, self._poll_conversion_progress)
    
    def _cancel_conversion(self):
        """Cancel the ongoing conversion process."""
        if self.is_converting:
            self._log_to_gui("warning", "Conversion canceled by user.")
            self.is_converting = False
            self._conversion_finished()
    
    def _conversion_finished(self):
        """Reset UI after conversion is finished (success or canceled)."""
        self.is_converting = False
        self.convert_button.config(state="normal")
        self.cancel_button.config(state="disabled")
        
        if self.log_handler:
            self.log_handler.stop()
            self.log_handler = None
    
    def run(self):
        """Run the application main loop."""
        self.mainloop()


def run_gui():
    """Run the HEIC Converter GUI application."""
    app = HeicConverterApp()
    app.run()