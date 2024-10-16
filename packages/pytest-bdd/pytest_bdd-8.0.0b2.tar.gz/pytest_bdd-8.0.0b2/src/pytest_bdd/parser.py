from __future__ import annotations

import os.path
import re
import textwrap
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

from .exceptions import StepError
from .gherkin_parser import Background as GherkinBackground
from .gherkin_parser import DataTable, ExamplesTable
from .gherkin_parser import Feature as GherkinFeature
from .gherkin_parser import GherkinDocument
from .gherkin_parser import Scenario as GherkinScenario
from .gherkin_parser import Step as GherkinStep
from .gherkin_parser import Tag as GherkinTag
from .gherkin_parser import get_gherkin_document
from .types import GIVEN, STEP_TYPES, THEN, WHEN

STEP_PARAM_RE = re.compile(r"<(.+?)>")
COMMENT_RE = re.compile(r"(^|(?<=\s))#")


def strip_comments(line: str) -> str:
    """Remove comments from a line of text.

    Args:
        line (str): The line of text from which to remove comments.

    Returns:
        str: The line of text without comments, with leading and trailing whitespace removed.
    """
    if res := COMMENT_RE.search(line):
        line = line[: res.start()]
    return line.strip()


@dataclass(eq=False)
class Feature:
    """Represents a feature parsed from a feature file.

    Attributes:
        scenarios (OrderedDict[str, ScenarioTemplate]): A dictionary of scenarios in the feature.
        filename (str): The absolute path of the feature file.
        rel_filename (str): The relative path of the feature file.
        name (Optional[str]): The name of the feature.
        tags (set[str]): A set of tags associated with the feature.
        background (Optional[Background]): The background steps for the feature, if any.
        line_number (int): The line number where the feature starts in the file.
        description (str): The description of the feature.
    """

    scenarios: OrderedDict[str, ScenarioTemplate]
    filename: str
    rel_filename: str
    name: str | None
    tags: set[str]
    background: Background | None
    line_number: int
    description: str


@dataclass(eq=False)
class Examples:
    """Represents examples used in scenarios for parameterization.

    Attributes:
        line_number (Optional[int]): The line number where the examples start.
        name (Optional[str]): The name of the examples.
        example_params (List[str]): The names of the parameters for the examples.
        examples (List[Sequence[str]]): The list of example rows.
    """

    line_number: int | None = None
    name: str | None = None
    example_params: list[str] = field(default_factory=list)
    examples: list[Sequence[str]] = field(default_factory=list)

    def set_param_names(self, keys: Iterable[str]) -> None:
        """Set the parameter names for the examples.

        Args:
            keys (Iterable[str]): The parameter names to set.
        """
        self.example_params = [str(key) for key in keys]

    def add_example(self, values: Sequence[str]) -> None:
        """Add a new example row.

        Args:
            values (Sequence[str]): The values for the example row.
        """
        self.examples.append([str(value) if value is not None else "" for value in values])

    def as_contexts(self) -> Iterable[dict[str, Any]]:
        """Generate contexts for the examples.

        Yields:
            Dict[str, Any]: A dictionary mapping parameter names to their values for each example row.
        """
        for row in self.examples:
            assert len(self.example_params) == len(row)
            yield dict(zip(self.example_params, row))

    def __bool__(self) -> bool:
        """Check if there are any examples.

        Returns:
            bool: True if there are examples, False otherwise.
        """
        return bool(self.examples)


@dataclass(eq=False)
class ScenarioTemplate:
    """Represents a scenario template within a feature.

    Attributes:
        feature (Feature): The feature to which this scenario belongs.
        name (str): The name of the scenario.
        line_number (int): The line number where the scenario starts in the file.
        templated (bool): Whether the scenario is templated.
        description (Optional[str]): The description of the scenario.
        tags (set[str]): A set of tags associated with the scenario.
        _steps (List[Step]): The list of steps in the scenario (internal use only).
        examples (Optional[Examples]): The examples used for parameterization in the scenario.
    """

    feature: Feature
    name: str
    line_number: int
    templated: bool
    description: str | None = None
    tags: set[str] = field(default_factory=set)
    _steps: list[Step] = field(init=False, default_factory=list)
    examples: Examples | None = field(default_factory=Examples)

    def add_step(self, step: Step) -> None:
        """Add a step to the scenario.

        Args:
            step (Step): The step to add.
        """
        step.scenario = self
        self._steps.append(step)

    @property
    def steps(self) -> list[Step]:
        """Get all steps for the scenario, including background steps.

        Returns:
            List[Step]: A list of steps, including any background steps from the feature.
        """
        return (self.feature.background.steps if self.feature.background else []) + self._steps

    def render(self, context: Mapping[str, Any]) -> Scenario:
        """Render the scenario with the given context.

        Args:
            context (Mapping[str, Any]): The context for rendering steps.

        Returns:
            Scenario: A Scenario object with steps rendered based on the context.
        """
        background_steps = self.feature.background.steps if self.feature.background else []
        scenario_steps = [
            Step(
                name=step.render(context),
                type=step.type,
                indent=step.indent,
                line_number=step.line_number,
                keyword=step.keyword,
                datatable=step.datatable,
            )
            for step in self._steps
        ]
        steps = background_steps + scenario_steps
        return Scenario(
            feature=self.feature,
            name=self.name,
            line_number=self.line_number,
            steps=steps,
            tags=self.tags,
            description=self.description,
        )


@dataclass(eq=False)
class Scenario:
    """Represents a scenario with steps.

    Attributes:
        feature (Feature): The feature to which this scenario belongs.
        name (str): The name of the scenario.
        line_number (int): The line number where the scenario starts in the file.
        steps (List[Step]): The list of steps in the scenario.
        description (Optional[str]): The description of the scenario.
        tags (set[str]): A set of tags associated with the scenario.
    """

    feature: Feature
    name: str
    line_number: int
    steps: list[Step]
    description: str | None = None
    tags: set[str] = field(default_factory=set)


@dataclass(eq=False)
class Step:
    """Represents a step within a scenario or background.

    Attributes:
        type (str): The type of step (e.g., 'given', 'when', 'then').
        name (str): The name of the step.
        line_number (int): The line number where the step starts in the file.
        indent (int): The indentation level of the step.
        keyword (str): The keyword used for the step (e.g., 'Given', 'When', 'Then').
        failed (bool): Whether the step has failed (internal use only).
        scenario (Optional[ScenarioTemplate]): The scenario to which this step belongs (internal use only).
        background (Optional[Background]): The background to which this step belongs (internal use only).
    """

    type: str
    name: str
    line_number: int
    indent: int
    keyword: str
    datatable: DataTable | None = None
    failed: bool = field(init=False, default=False)
    scenario: ScenarioTemplate | None = field(init=False, default=None)
    background: Background | None = field(init=False, default=None)

    def __init__(
        self, name: str, type: str, indent: int, line_number: int, keyword: str, datatable: DataTable | None = None
    ) -> None:
        """Initialize a step.

        Args:
            name (str): The name of the step.
            type (str): The type of the step (e.g., 'given', 'when', 'then').
            indent (int): The indentation level of the step.
            line_number (int): The line number where the step starts in the file.
            keyword (str): The keyword used for the step (e.g., 'Given', 'When', 'Then').
        """
        self.name = name
        self.type = type
        self.indent = indent
        self.line_number = line_number
        self.keyword = keyword
        self.datatable = datatable

    def __str__(self) -> str:
        """Return a string representation of the step.

        Returns:
            str: A string representation of the step.
        """
        return f'{self.type.capitalize()} "{self.name}"'

    @property
    def params(self) -> tuple[str, ...]:
        """Get the parameters in the step name.

        Returns:
            Tuple[str, ...]: A tuple of parameter names found in the step name.
        """
        return tuple(frozenset(STEP_PARAM_RE.findall(self.name)))

    def render(self, context: Mapping[str, Any]) -> str:
        """Render the step name with the given context, but avoid replacing text inside angle brackets if context is missing.

        Args:
            context (Mapping[str, Any]): The context for rendering the step name.

        Returns:
            str: The rendered step name with parameters replaced only if they exist in the context.
        """

        def replacer(m: re.Match) -> str:
            varname = m.group(1)
            # If the context contains the variable, replace it. Otherwise, leave it unchanged.
            return str(context.get(varname, f"<{varname}>"))

        return STEP_PARAM_RE.sub(replacer, self.name)


@dataclass(eq=False)
class Background:
    """Represents the background steps for a feature.

    Attributes:
        feature (Feature): The feature to which this background belongs.
        line_number (int): The line number where the background starts in the file.
        steps (List[Step]): The list of steps in the background.
    """

    feature: Feature
    line_number: int
    steps: list[Step] = field(init=False, default_factory=list)

    def add_step(self, step: Step) -> None:
        """Add a step to the background.

        Args:
            step (Step): The step to add.
        """
        step.background = self
        self.steps.append(step)


class FeatureParser:
    """Converts a feature file into a Feature object.

    Args:
        basedir (str): The basedir for locating feature files.
        filename (str): The filename of the feature file.
        encoding (str): File encoding of the feature file to parse.
    """

    def __init__(self, basedir: str, filename: str, encoding: str = "utf-8"):
        self.abs_filename = os.path.abspath(os.path.join(basedir, filename))
        self.rel_filename = os.path.join(os.path.basename(basedir), filename)
        self.encoding = encoding

    @staticmethod
    def get_tag_names(tag_data: list[GherkinTag]) -> set[str]:
        """Extract tag names from tag data.

        Args:
            tag_data (List[dict]): The tag data to extract names from.

        Returns:
            set[str]: A set of tag names.
        """
        return {tag.name.lstrip("@") for tag in tag_data}

    def parse_steps(self, steps_data: list[GherkinStep]) -> list[Step]:
        """Parse a list of step data into Step objects.

        Args:
            steps_data (List[dict]): The list of step data.

        Returns:
            List[Step]: A list of Step objects.
        """

        def get_step_content(_gherkin_step: GherkinStep) -> str:
            step_name = strip_comments(_gherkin_step.text)
            if _gherkin_step.docstring:
                step_name = f"{step_name}\n{_gherkin_step.docstring.content}"
            return step_name

        if not steps_data:
            return []

        first_step = steps_data[0]
        if first_step.keyword.lower() not in STEP_TYPES:
            raise StepError(
                message=f"First step in a scenario or background must start with 'Given', 'When' or 'Then', but got {first_step.keyword}.",
                line=first_step.location.line,
                line_content=get_step_content(first_step),
                filename=self.abs_filename,
            )

        steps = []
        current_type = first_step.keyword.lower()
        for step in steps_data:
            name = get_step_content(step)
            keyword = step.keyword.lower()
            if keyword in STEP_TYPES:
                current_type = keyword
            steps.append(
                Step(
                    name=name,
                    type=current_type,
                    indent=step.location.column - 1,
                    line_number=step.location.line,
                    keyword=step.keyword.title(),
                    datatable=step.datatable,
                )
            )
        return steps

    def parse_scenario(self, scenario_data: GherkinScenario, feature: Feature) -> ScenarioTemplate:
        """Parse a scenario data dictionary into a ScenarioTemplate object.

        Args:
            scenario_data (dict): The dictionary containing scenario data.
            feature (Feature): The feature to which this scenario belongs.

        Returns:
            ScenarioTemplate: A ScenarioTemplate object representing the parsed scenario.
        """
        templated = bool(scenario_data.examples)
        scenario = ScenarioTemplate(
            feature=feature,
            name=strip_comments(scenario_data.name),
            line_number=scenario_data.location.line,
            templated=templated,
            tags=self.get_tag_names(scenario_data.tags),
            description=textwrap.dedent(scenario_data.description),
        )
        for step in self.parse_steps(scenario_data.steps):
            scenario.add_step(step)

        for example_data in scenario_data.examples:
            examples = Examples(
                line_number=example_data.location.line,
                name=example_data.name,
            )
            if example_data.table_header is not None:
                param_names = [cell.value for cell in example_data.table_header.cells]
                examples.set_param_names(param_names)
                if example_data.table_body is not None:
                    for row in example_data.table_body:
                        values = [cell.value or "" for cell in row.cells]
                        examples.add_example(values)
                    scenario.examples = examples

        return scenario

    def parse_background(self, background_data: GherkinBackground, feature: Feature) -> Background:
        background = Background(
            feature=feature,
            line_number=background_data.location.line,
        )
        background.steps = self.parse_steps(background_data.steps)
        for step in background.steps:
            step.background = background
        return background

    def _parse_feature_file(self) -> GherkinDocument:
        """Parse a feature file into a Feature object.

        Returns:
            Dict: A Gherkin document representation of the feature file.
        """
        return get_gherkin_document(self.abs_filename, self.encoding)

    def parse(self) -> Feature:
        gherkin_doc: GherkinDocument = self._parse_feature_file()
        feature_data: GherkinFeature = gherkin_doc.feature
        feature = Feature(
            scenarios=OrderedDict(),
            filename=self.abs_filename,
            rel_filename=self.rel_filename,
            name=strip_comments(feature_data.name),
            tags=self.get_tag_names(feature_data.tags),
            background=None,
            line_number=feature_data.location.line,
            description=textwrap.dedent(feature_data.description),
        )

        for child in feature_data.children:
            if child.background:
                feature.background = self.parse_background(child.background, feature)
            elif child.scenario:
                scenario = self.parse_scenario(child.scenario, feature)
                feature.scenarios[scenario.name] = scenario

        return feature
