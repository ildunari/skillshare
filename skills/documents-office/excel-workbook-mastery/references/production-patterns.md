# Production Patterns — openpyxl Implementation

This file bridges the design guidelines from the rest of the skill to concrete openpyxl implementation patterns. Use it when Claude is scripting .xlsx file generation and needs to apply the skill's design principles programmatically.

See also: `workbook-architecture.md` for structure decisions, `visual-design.md` for formatting choices, and `charts-and-visualization.md` for chart configuration.

**Contents:** When to use this file · Setup and workbook initialization · Style constants · Multi-sheet workbook architecture · Input cell formatting · Data validation patterns · Number format recipes · Table creation · Chart creation · Conditional formatting for checks · Print layout setup · Protection pattern · Freeze panes

## When to use this file

Load this file when the task involves generating or editing .xlsx files through Python. The other reference files tell you *what* the workbook should look like; this file tells you *how* to produce it with openpyxl.

If the xlsx public skill is also loaded, use that skill for boilerplate file-creation mechanics. This file focuses specifically on applying excel-workbook-mastery design principles in code.

## Setup and workbook initialization

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, Protection, numbers
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, ScatterChart, Reference
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule

wb = Workbook()
```

## Style constants — matching visual-design.md conventions

```python
# Typography (visual-design.md defaults)
FONT_TITLE = Font(name='Aptos', size=14, bold=True)
FONT_SECTION = Font(name='Aptos', size=11, bold=True)
FONT_BODY = Font(name='Aptos', size=10)
FONT_NOTE = Font(name='Aptos', size=9, color='666666')

# Finance color conventions (visual-design.md)
FONT_INPUT = Font(name='Aptos', size=10, color='0000CC')       # Blue — editable inputs
FONT_FORMULA = Font(name='Aptos', size=10, color='000000')     # Black — formulas
FONT_LINK = Font(name='Aptos', size=10, color='006600')        # Green — internal links
FONT_EXTERNAL = Font(name='Aptos', size=10, color='CC0000')    # Red — external links

# Fills
FILL_INPUT = PatternFill(start_color='EBF5FB', end_color='EBF5FB', fill_type='solid')
FILL_HEADER = PatternFill(start_color='D5E8D4', end_color='D5E8D4', fill_type='solid')
FILL_TOTAL = PatternFill(start_color='F2F2F2', end_color='F2F2F2', fill_type='solid')
FILL_WARNING = PatternFill(start_color='FFF3CD', end_color='FFF3CD', fill_type='solid')

# Borders
THIN_BORDER = Border(
    bottom=Side(style='thin', color='CCCCCC')
)
TOTAL_BORDER = Border(
    top=Side(style='thin', color='000000'),
    bottom=Side(style='double', color='000000')
)

# Alignment
ALIGN_LEFT = Alignment(horizontal='left', vertical='center')
ALIGN_RIGHT = Alignment(horizontal='right', vertical='center')
ALIGN_CENTER = Alignment(horizontal='center', vertical='center')
ALIGN_WRAP = Alignment(horizontal='left', vertical='top', wrap_text=True)
```

## Multi-sheet workbook architecture

Implement the layered architecture from workbook-architecture.md:

```python
def create_structured_workbook(title, has_checks=True):
    """Create a workbook with the standard sheet architecture."""
    wb = Workbook()

    # Remove default sheet
    wb.remove(wb.active)

    # Create sheets in order
    ws_readme = wb.create_sheet('00_README')
    ws_inputs = wb.create_sheet('01_Inputs')
    ws_data = wb.create_sheet('02_RawData')
    ws_calc = wb.create_sheet('03_Calc')
    if has_checks:
        ws_checks = wb.create_sheet('04_Checks')
    ws_output = wb.create_sheet('05_Output')

    # README content
    readme_fields = [
        ('Workbook:', title),
        ('Purpose:', ''),
        ('Owner:', ''),
        ('Version:', '1.0'),
        ('Last updated:', ''),
        ('Data refreshed:', ''),
        ('Key assumptions:', 'See 01_Inputs'),
        ('Known limitations:', ''),
        ('How to use:', 'Edit blue cells on 01_Inputs only.'),
    ]
    for i, (label, value) in enumerate(readme_fields, 1):
        ws_readme.cell(row=i, column=1, value=label).font = FONT_SECTION
        ws_readme.cell(row=i, column=2, value=value).font = FONT_BODY

    ws_readme.column_dimensions['A'].width = 20
    ws_readme.column_dimensions['B'].width = 60

    return wb
```

## Input cell formatting

Make editable cells unmistakable per workbook-architecture.md — use multiple signals:

```python
def format_input_cell(ws, row, col, value=None, validation=None):
    """Format a cell as a user-editable input with visual signals."""
    cell = ws.cell(row=row, column=col, value=value)
    cell.font = FONT_INPUT
    cell.fill = FILL_INPUT
    cell.alignment = ALIGN_RIGHT
    cell.protection = Protection(locked=False)

    if validation:
        ws.add_data_validation(validation)
        validation.add(cell)

    return cell
```

## Data validation patterns

```python
# Drop-down list from a range
scenario_dv = DataValidation(
    type='list',
    formula1='"Base,Upside,Downside"',
    allow_blank=False,
    showErrorMessage=True,
    errorTitle='Invalid scenario',
    error='Choose Base, Upside, or Downside.'
)

# Percentage bounds
pct_dv = DataValidation(
    type='decimal',
    operator='between',
    formula1='0',
    formula2='1',
    showErrorMessage=True,
    errorTitle='Invalid percentage',
    error='Enter a value between 0% and 100%.'
)

# Positive integer
count_dv = DataValidation(
    type='whole',
    operator='greaterThan',
    formula1='0',
    showErrorMessage=True,
    errorTitle='Invalid count',
    error='Enter a positive whole number.'
)
```

## Number format recipes

```python
# Map from visual-design.md number format guidance
NUMBER_FORMATS = {
    'currency': '#,##0',
    'currency_m': '#,##0.0',          # Millions with 1 decimal
    'percent_1': '0.0%',              # One decimal
    'percent_0': '0%',                # No decimals
    'count': '#,##0',                 # No decimals
    'date': 'YYYY-MM-DD',
    'scientific': '0.00E+00',
    'finance_negative': '#,##0_);(#,##0)',  # Parentheses for negatives
    'finance_dash_zero': '#,##0_);(#,##0);"-"',  # Dash for zeros
    'multiplier': '0.0"x"',
}
```

## Table creation with proper structure

```python
from openpyxl.worksheet.table import Table, TableStyleInfo

def create_data_table(ws, data, headers, start_row=1, start_col=1, table_name='tblData'):
    """Create a formatted Excel Table from data."""
    # Write headers
    for j, header in enumerate(headers):
        cell = ws.cell(row=start_row, column=start_col + j, value=header)
        cell.font = FONT_SECTION
        cell.alignment = ALIGN_CENTER

    # Write data
    for i, row_data in enumerate(data):
        for j, value in enumerate(row_data):
            cell = ws.cell(row=start_row + 1 + i, column=start_col + j, value=value)
            cell.font = FONT_BODY

    # Create Table object
    end_row = start_row + len(data)
    end_col = start_col + len(headers) - 1
    ref = f"{get_column_letter(start_col)}{start_row}:{get_column_letter(end_col)}{end_row}"

    table = Table(displayName=table_name, ref=ref)
    style = TableStyleInfo(
        name='TableStyleMedium2',
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False
    )
    table.tableStyleInfo = style
    ws.add_table(table)

    # Auto-fit column widths (approximate)
    for j, header in enumerate(headers):
        max_len = len(str(header))
        for row_data in data:
            if j < len(row_data):
                max_len = max(max_len, len(str(row_data[j])))
        ws.column_dimensions[get_column_letter(start_col + j)].width = min(max_len + 4, 30)

    return table
```

## Chart creation — applying charts-and-visualization.md principles

```python
def create_clean_chart(chart_type, title, x_title=None, y_title=None, width=15, height=10):
    """Create a chart with Tufte-inspired defaults: minimal gridlines, no fill, direct style."""
    ChartClass = {
        'bar': BarChart,
        'line': LineChart,
        'scatter': ScatterChart,
    }[chart_type]

    chart = ChartClass()
    chart.title = title
    chart.width = width
    chart.height = height

    # Strip chartjunk
    chart.legend = None  # Prefer direct labels; re-enable if needed
    chart.style = 2      # Minimal built-in style

    if x_title:
        chart.x_axis.title = x_title
    if y_title:
        chart.y_axis.title = y_title

    # Light gridlines only
    chart.y_axis.majorGridlines = None  # Remove if not needed
    chart.x_axis.majorGridlines = None

    return chart
```

## Conditional formatting for checks

```python
def add_check_formatting(ws, check_range):
    """Apply pass/fail conditional formatting to a check column."""
    # Green for PASS
    ws.conditional_formatting.add(
        check_range,
        CellIsRule(
            operator='equal',
            formula=['"PASS"'],
            fill=PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid'),
            font=Font(color='006100')
        )
    )
    # Red for FAIL
    ws.conditional_formatting.add(
        check_range,
        CellIsRule(
            operator='equal',
            formula=['"FAIL"'],
            fill=PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid'),
            font=Font(color='9C0006')
        )
    )
```

## Print layout setup

```python
def setup_print_layout(ws, orientation='landscape', fit_cols=1, repeat_rows=1):
    """Configure print settings per visual-design.md guidance."""
    ws.page_setup.orientation = orientation
    ws.page_setup.fitToWidth = fit_cols
    ws.page_setup.fitToHeight = 0  # Auto pages vertically
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    # Repeat header row on every printed page
    if repeat_rows:
        ws.print_title_rows = f'1:{repeat_rows}'

    # Margins (inches)
    ws.page_margins.left = 0.5
    ws.page_margins.right = 0.5
    ws.page_margins.top = 0.75
    ws.page_margins.bottom = 0.75

    # Header/footer
    ws.oddHeader.center.text = ws.title
    ws.oddFooter.right.text = 'Page &P of &N'
```

## Protection pattern

```python
def protect_with_input_zones(ws, password=None):
    """Lock the sheet but leave input-formatted cells editable."""
    # All cells locked by default in openpyxl
    # Input cells were already set to locked=False via format_input_cell()
    ws.protection.sheet = True
    ws.protection.enable()
    if password:
        ws.protection.password = password
```

## Freeze panes

```python
def freeze_headers(ws, row=2, col=1):
    """Freeze panes so headers stay visible during scrolling."""
    ws.freeze_panes = ws.cell(row=row, column=col)
```
