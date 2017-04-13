# story-card-painter

A story card painter for creating a physical scrum

## I/O file format

Input: `CSV`

Output: `PDF`

### CSV rules

The input backlog file should be CSV format with 6 columns according to the order of: `ID`, `Name`, `Importance`, `Estimate`, `How to demo`, `Notes` for the stories.

Notice that the first row would be ignored as header.

## Usage

- `normal-painter.py`: 1/2 A4
- `small-painter.py`: 1/4 A4, less fields

Set I/O paths in the `main` function.
