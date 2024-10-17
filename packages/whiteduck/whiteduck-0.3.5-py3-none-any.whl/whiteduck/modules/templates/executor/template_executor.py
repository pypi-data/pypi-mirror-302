from loguru import logger
from rich.console import Console
from rich.markdown import Markdown

from whiteduck.exceptions import StepExecutionError
from whiteduck.modules.templates.executor.step_processor import process_steps
from whiteduck.modules.templates.executor.variable_processor import process_variables
from whiteduck.modules.templates.model.template import Template

console = Console()


class TemplateExecutor:
    def __init__(self, template_path: str):
        logger.info(f"Initializing TemplateExecutor with template: {template_path}")
        self.template: Template = Template.load_template(template_path)

    def execute(self) -> None:
        logger.info("Executing template")

        console.print(Markdown("--------------------------------------------------"))
        title = "\n\n# 🚀" + self.template.template + " 🚀"
        console.print(Markdown(title), style="bold green", justify="left", markup=True)

        variables = process_variables(self.template.variables)
        try:
            process_steps(
                self.template.steps,
                variables,
                self.template.modules,
                self.template.prompts,
            )
        except StepExecutionError as e:
            console.print(f"\n[bold red]❌ Error:[/bold red] {e!s}")
            console.print("[bold red]❗Execution aborted due to an error in one of the steps.[/bold red]")
            raise

    @staticmethod
    def execute_template(template: Template) -> None:
        logger.info("Executing template")

        console.print(Markdown("--------------------------------------------------"))
        title = "\n\n# 🚀" + template.template + " 🚀"
        console.print(Markdown(title), style="bold green", justify="left", markup=True)

        variables = process_variables(template.variables)
        try:
            process_steps(
                template.steps,
                variables,
                template.modules,
                template.prompts,
            )
        except StepExecutionError as e:
            console.print(f"\n[bold red]❌ Error:[/bold red] {e!s}")
            console.print("[bold red]❗Execution aborted due to an error in one of the steps.[/bold red]")
            raise
