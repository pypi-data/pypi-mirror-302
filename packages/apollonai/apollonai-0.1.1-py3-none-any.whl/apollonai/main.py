import typer
from cli import setup_logging, log_info

cli = typer.Typer()

setup_logging("util4all")

# CLI Commands
@cli.command("test1")
def start():
    """Test 133"""
    
    log_info(f"Test 1 with cli typer command")

@cli.command("test3")
def start():
    """Test 12"""
    
    log_info(f"Test 2 with cli typer command")



if __name__ == "__main__":
    log_info(f"Test 1 with cli typer command")
    cli()