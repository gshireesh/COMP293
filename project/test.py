from rich import pretty
pretty.install()
from rich.console import Console

console = Console()
console.print([1,2,3])
console.print("Hello", "World!", style="bold red")

