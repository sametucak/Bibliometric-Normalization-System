"""
Bibliometric Normalization System (BNS)
Graphical User Interface

Version: 1.1.0
"""

import os
import threading
from pathlib import Path
import tkinter as tk

from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from main import run_pipeline


class BNSApplication(tk.Tk):
    """Main BNS graphical user interface."""

    def __init__(self) -> None:
        super().__init__()

        self.title("Bibliometric Normalization System (BNS)")
        self.geometry("760x560")
        self.minsize(700, 500)

        self._configure_style()
        self._build_interface()

    def _configure_style(self) -> None:
        """Configure ttk styles."""

        style = ttk.Style(self)

        try:
            style.theme_use("vista")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 18, "bold"),
        )

        style.configure(
            "Version.TLabel",
            font=("Segoe UI", 10),
        )

        style.configure(
            "Section.TLabel",
            font=("Segoe UI", 11, "bold"),
        )

    def select_input_file(self) -> None:
        """Select the input Excel file."""

        file_path = filedialog.askopenfilename(
            title="Select BNS Input Excel File",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*"),
            ],
        )

        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)

    def select_output_folder(self) -> None:
        """Select the output folder."""

        folder_path = filedialog.askdirectory(
            title="Select BNS Output Folder"
        )

        if folder_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder_path)

    def start_analysis(self) -> None:
        """Start the BNS analysis."""

        input_file = Path(
            self.input_entry.get().strip()
        )

        output_dir = Path(
            self.output_entry.get().strip()
        )

        if not input_file:
            messagebox.showwarning(
                "Missing Input File",
                "Please select an input Excel file.",
            )
            return

        if not input_file.exists():
            messagebox.showerror(
                "Input File Not Found",
                f"The selected input file does not exist:\n\n{input_file}",
            )
            return

        if not output_dir:
            messagebox.showwarning(
                "Missing Output Folder",
                "Please select an output folder.",
            )
            return

        try:
            output_dir.mkdir(
                parents=True,
                exist_ok=True,
            )
        except OSError as exc:
            messagebox.showerror(
                "Output Folder Error",
                f"Could not create the output folder:\n\n{exc}",
            )
            return

        self.start_button.config(
            state="disabled"
        )

        self.output_folder_button.config(
            state="disabled"
        )

        self.progress["value"] = 0

        self.status_label.config(
            text="Status: Running analysis..."
        )

        self.result_label.config(
            text="BNS analysis is running..."
        )

        worker = threading.Thread(
            target=self._run_analysis,
            args=(input_file, output_dir),
            daemon=True,
        )

        worker.start()

    def update_progress(
        self,
        value: int,
        message: str,
    ) -> None:
        """Update GUI progress from the pipeline."""

        self.after(
            0,
            lambda: (
                self.progress.configure(value=value),
                self.status_label.configure(
                text=f"Status: {message}"
                ),
            ),
        )

    def _run_analysis(
        self,
        input_file: Path,
        output_dir: Path,
    ) -> None:
        """Run the BNS pipeline in a background thread."""

        try:
            run_pipeline(
                input_file,
                output_dir,
                progress_callback=self.update_progress,
            )

        except Exception as exc:
            self.after(
                0,
                self._analysis_failed,
                exc,
            )
            return

        self.after(
            0,
            self._analysis_completed,
        )

    def _analysis_completed(self) -> None:
        """Handle successful analysis completion."""

        self.progress["value"] = 100

        self.status_label.config(
            text="Status: Analysis completed."
        )

        self.result_label.config(
            text="✓ BNS analysis completed successfully."
        )

        self.start_button.config(
            state="normal"
        )

        self.output_folder_button.config(
            state="normal"
        )

        messagebox.showinfo(
            "BNS Analysis Completed",
            "BNS analysis completed successfully.\n\n"
            "All output files have been generated.",
        )

    def open_output_folder(self) -> None:
        """Open the selected output folder in Windows Explorer."""

        output_dir = Path(
            self.output_entry.get().strip()
        )

        if output_dir.exists():
            os.startfile(output_dir)

    def _analysis_failed(
        self,
        exc: Exception,
    ) -> None:
        """Handle analysis errors."""

        self.progress["value"] = 0

        self.status_label.config(
            text="Status: Analysis failed."
        )

        self.result_label.config(
            text="✗ BNS analysis failed.",
        )

        self.start_button.config(
            state="normal"
        )

        self.output_folder_button.config(
            state="disabled"
        )

        messagebox.showerror(
            "BNS Analysis Error",
            f"The BNS analysis could not be completed.\n\n"
            f"Error:\n{exc}",
        )

    def _build_interface(self) -> None:
        """Build the main application interface."""

        main_frame = ttk.Frame(
            self,
            padding=25,
        )
        main_frame.pack(
            fill="both",
            expand=True,
        )

        title = ttk.Label(
            main_frame,
            text="Bibliometric Normalization System (BNS)",
            style="Title.TLabel",
        )
        title.pack(anchor="w")

        version = ttk.Label(
            main_frame,
            text="Version 1.1.0",
            style="Version.TLabel",
        )
        version.pack(
            anchor="w",
            pady=(3, 20),
        )

        separator = ttk.Separator(main_frame)
        separator.pack(
            fill="x",
            pady=(0, 20),
        )

        input_section = ttk.Label(
            main_frame,
            text="Input Excel File",
            style="Section.TLabel",
        )
        input_section.pack(anchor="w")

        input_frame = ttk.Frame(main_frame)
        input_frame.pack(
            fill="x",
            pady=(8, 20),
        )

        self.input_entry = ttk.Entry(
            input_frame
        )
        self.input_entry.pack(
            side="left",
            fill="x",
            expand=True,
        )

        browse_button = ttk.Button(
            input_frame,
            text="Browse...",
            command=self.select_input_file,
        )
        browse_button.pack(
            side="left",
            padx=(10, 0),
        )

        output_section = ttk.Label(
            main_frame,
            text="Output Folder",
            style="Section.TLabel",
        )
        output_section.pack(anchor="w")

        output_frame = ttk.Frame(main_frame)
        output_frame.pack(
            fill="x",
            pady=(8, 20),
        )

        self.output_entry = ttk.Entry(
            output_frame
        )
        self.output_entry.pack(
            side="left",
            fill="x",
            expand=True,
        )

        output_button = ttk.Button(
            output_frame,
            text="Browse...",
            command=self.select_output_folder,
        )

        output_button.pack(
            side="left",
            padx=(10, 0),
        )

        self.start_button = ttk.Button(
            main_frame,
            text="START ANALYSIS",
            command=self.start_analysis,
        )
        self.start_button.pack(
            pady=(10, 25),
            ipadx=20,
            ipady=8,
        )

        self.output_folder_button = ttk.Button(
            main_frame,
            text="OPEN OUTPUT FOLDER",
            command=self.open_output_folder,
            state="disabled",
        )

        self.output_folder_button.pack(
            pady=(0, 20),
            ipadx=15,
            ipady=5,
        )

        progress_section = ttk.Label(
            main_frame,
            text="Progress",
            style="Section.TLabel",
        )
        progress_section.pack(anchor="w")

        self.progress = ttk.Progressbar(
            main_frame,
            mode="determinate",
            maximum=100,
        )
        self.progress.pack(
            fill="x",
            pady=(8, 10),
        )

        self.status_label = ttk.Label(
            main_frame,
            text="Status: Ready",
        )
        self.status_label.pack(anchor="w")

        separator_bottom = ttk.Separator(main_frame)
        separator_bottom.pack(
            fill="x",
            pady=(25, 15),
        )

        self.result_label = ttk.Label(
            main_frame,
            text="BNS is ready.",
        )
        self.result_label.pack(anchor="w")


if __name__ == "__main__":
    app = BNSApplication()
    app.mainloop()