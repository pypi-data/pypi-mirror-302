import time
from typing import List

from loguru import logger
from rich.console import Console
from rich.markdown import Markdown

from whiteduck.exceptions import StepExecutionError
from whiteduck.modules.templates.model.prompt import Prompt
from whiteduck.modules.templates.model.step import Step
from whiteduck.modules.templates.model.util_classes import Module, Variable
from whiteduck.modules.templates.steps.module_step import ModuleStep
from whiteduck.modules.templates.steps.prompt_step import PromptStep
from whiteduck.modules.templates.steps.wizard_step import WizardStep
from whiteduck.modules.templates.utils.steps_utils import check_condition, find_module_by_id, find_prompt_by_id

console = Console()


def process_steps(steps: List[Step], variables: List[Variable], modules: List[Module], prompts: List[Prompt]) -> None:
    """
    Process each step by type and execute it if conditions are met.

    Args:
        steps (List[Step]): A list of serialized Step objects.
        variables (List[Variable]): A dictionary of Variable objects for step execution.
        modules (List[Module]): A list of Module objects available for execution.
        prompts (List[Prompt]): A list of Prompt objects available for execution.
    """
    logger.info("Processing steps")

    for step in steps:
        time.sleep(0.5)
        step_id = step.id
        step_type = step.type
        condition = step.condition
        title = f"{step.title or step_id}"
        console.print(Markdown(title), style="bold yellow", justify="left", markup=True)
        console.line(1)
        if not check_condition(condition, variables):  # type: ignore
            logger.info(f"Skipping step: {step_id} (condition not met)")
            console.print(f"\n[yellow]Skipping Step:[/yellow] {step_id} (condition not met)")
            console.line(1)
            continue

        try:
            if step_type == "prompt_id":
                prompt = find_prompt_by_id(str(step.value), prompts)
                if prompt:
                    PromptStep(step, prompts).execute(variables)
                else:
                    raise StepExecutionError(f"Prompt not found: {step.value}")
            elif step_type == "module_id":
                module = find_module_by_id(str(step.value), modules)
                if module:
                    ModuleStep(step, modules).execute(variables)
                else:
                    raise StepExecutionError(f"Module not found: {step.value}")
            elif step_type == "wizard":
                WizardStep(step, prompts).execute(variables)
            elif step_type == "module":
                ModuleStep(step, modules).execute(variables)
            elif step_type == "prompt":
                PromptStep(step, prompts).execute(variables)
                pass
            else:
                logger.warning(f"Unknown step type: {step_type}")
                raise StepExecutionError(f"Unknown step type: {step_type}")

            console.line(1)
        except Exception as e:
            logger.error(f"Error executing step {step_id}: {str(e)}")
            raise StepExecutionError(f"Error executing step {step_id}: {str(e)}")
