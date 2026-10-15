# Maloni Removals Calculator

## Run the bundled Windows app

The PyInstaller build includes its own Python runtime, so Python does not need
to be installed to run the app. From the project folder, launch:

```powershell
.\dist\RemovalsCalculator\RemovalsCalculator.exe
```

To use the app on another Windows computer, copy the complete
`dist\RemovalsCalculator` folder and run `RemovalsCalculator.exe` from it.
Do not distribute a `.env` file containing email credentials.

## Run from source or rebuild

The existing `.venv` was created from a Python installation on another
computer, so its interpreter path is invalid here. A replacement environment
named `.venv314` has been created from Python 3.14. To create it on another
development computer, install Python 3.14 and run:

```powershell
py -3.14 -m venv .venv314
.\.venv314\Scripts\python.exe -m pip install -r requirements.txt
.\.venv314\Scripts\python.exe -m pip install pyinstaller
```

Run from source:

```powershell
.\.venv314\Scripts\python.exe desktop_app.py
```

Rebuild the bundled app:

```powershell
.\.venv314\Scripts\python.exe -m PyInstaller --clean --noconfirm RemovalsCalculator.spec
```
