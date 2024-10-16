# stringstyler

Add color and change the format of your strings !

# Usage

## The print_color_text() function

The print_color_text() function :

```python
from stringstyler import print_styler


print_color_text('Hello, World!', 'red')
print_color_text('Hello, World!', 'red', style='bold')
print_color_text('Hello, World!', 'green', style='underline')
print_color_text('Hello, World!', 'blue', style='reverse')
print_color_text('Hello, World!', 'magenta', style='invisible')
print_color_text('Hello, World!', 'cyan', style='strikethrough')
```

## The text_styler decorator

```python
from stringstyler import text_styler

@text_styler(color="yellow", style="bold")
def greet(name: str):
    """Greets a person by name."""
    return f"Hello, {name}!"
```