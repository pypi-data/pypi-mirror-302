import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Type, Union

import covalent as ct
import covalent_cloud as cc
from covalent_cloud.function_serve.deployment import Deployment
from pydantic import BaseModel, Field

CC_API_KEY = cc.get_api_key()
if not CC_API_KEY:
    raise ValueError("No API key found. Please set your API key.")


def _skip_comments(f):
    while line := f.readline():
        if not line.startswith("#"):
            return line.strip()


def read_all_city_names(file: str) -> List[str]:
    with open(file, "r", encoding="utf-8") as f:
        names = []
        line = _skip_comments(f)
        while line.strip():
            names.append(line)
            line = f.readline().strip()
    return names


def read_all_distance_matrix(file: str, size: int) -> List[List[Any]]:
    with open(file, "r", encoding="utf-8") as f:
        # read matrix
        matrix = []
        row = []
        line = _skip_comments(f)
        while line.strip():
            entries = [int(x) for x in line.split()]
            row.extend(entries)
            if len(row) >= size:
                matrix.append(row[:size])
                row = row[size:]
            line = f.readline()

    if not all(len(row) == len(matrix) for row in matrix):
        raise RuntimeError(f"Matrix is not square, expected {size} x {size}")
    return matrix


with open("./install_concorde.sh", "r", encoding="utf-8") as f_:
    CONCORDE_SETUP_SCRIPT = f_.read()

ALL_CITY_NAMES = read_all_city_names("usca312/usca312_name.txt")

ALL_DISTANCE_MATRIX = read_all_distance_matrix(
    "usca312/usca312_dist.txt",
    size=312
)


class TSPFile(BaseModel):
    """
    Schema for specifying a TSP problem as a file in TSPLIB 95 format
    http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf
    """
    NAME: str = ""
    TYPE: str = "TSP"
    COMMENT: str = ""
    DIMENSION: int
    CAPACITY: Optional[int] = None
    EDGE_WEIGHT_TYPE: str = ""
    EDGE_WEIGHT_FORMAT: str = ""
    EDGE_DATA_FORMAT: str = ""
    NODE_COORD_TYPE: str = ""
    DISPLAY_DATA_TYPE: str = ""
    NODE_COORD_SECTION: str = ""
    DEPOT_SECTION: str = ""
    DEMAND_SECTION: str = ""
    EDGE_DATA_SECTION: str = ""
    FIXED_EDGES_SECTION: str = ""
    DISPLAY_DATA_SECTION: str = ""
    TOUR_SECTION: str = ""
    EDGE_WEIGHT_SECTION: str = ""

    def __str__(self) -> str:
        content = [
            f"NAME : {self.NAME}",
            f"TYPE : {self.TYPE}",
            f"COMMENT : {self.COMMENT}",
            f"DIMENSION : {self.DIMENSION}",
            f"CAPACITY : {self.CAPACITY}" if self.CAPACITY is not None else "",
        ]
        ex = {"NAME", "TYPE", "COMMENT", "DIMENSION", "CAPACITY"}
        content += [f"{k} : {v}" for k,
                    v in self.model_dump(exclude=ex).items() if v]
        content.append("EOF")
        return "\n".join(line for line in content if line)

    def to_file(self, file_path: Union[Path, str]) -> Path:
        file_path = Path(file_path).expanduser().absolute()
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(self))
            f.write("\nEOF")

        return file_path

    @classmethod
    def from_distance_matrix(cls, matrix: Sequence[Sequence[int]], **kwargs):
        dimension = len(matrix)
        edge_weight_matrix = "\n".join(
            " " + " ".join(str(x) for x in row) for row in matrix)
        edge_weight_section = "\n".join([str(dimension), edge_weight_matrix])
        return cls(
            DIMENSION=dimension,
            EDGE_WEIGHT_TYPE="EXPLICIT",
            EDGE_WEIGHT_FORMAT="FULL_MATRIX",
            EDGE_WEIGHT_SECTION=edge_weight_section,
            **{k.upper(): v for k, v in kwargs.items()}
        )


class ConcordeSolver:
    """
    Bare-bones Python wrapper for `concorde` TSP solver.
    https://www.math.uwaterloo.ca/tsp/concorde/index.html
    """

    def __init__(self, concorde_executable_path: str):
        _exec = Path(concorde_executable_path).expanduser().absolute()
        assert _exec.exists(), f"Concorde executable not found at {_exec}"
        self.exec = _exec

    def solve(
        self,
        input_file: str,
        problem_type: str = "TSP",
    ) -> List[int]:
        """Use the solver to find an optimal solution to a TSP problem."""
        if problem_type != "TSP":
            raise NotImplementedError("Only TSP problems are supported")

        input_file = Path(input_file).expanduser().absolute()
        output_file = input_file.with_suffix(".sol")

        # Call Concorde
        subprocess.run(
            f"{self.exec} -x -o {output_file} {input_file}",
            shell=True, check=False, stderr=sys.stderr, stdout=sys.stderr
        )

        return self.read_tsp_solution(output_file)

    @staticmethod
    def read_tsp_solution(file: str) -> List[int]:
        """Read the solution sequence (shortest_path) from a Concorde output file."""
        with open(file, "r", encoding="utf-8") as f:
            # skip count line
            line = f.readline()

            shortest_path = []
            while line := f.readline().strip():
                nodes = [int(i) for i in line.split()]
                shortest_path.extend(nodes)

        return shortest_path


pkgs = ["accelerate", "bitsandbytes", "sentencepiece",
        "transformers", "lm-format-enforcer"]
cc.create_env(name="llm-backend", pip=pkgs, wait=True)

l40_gpu = cc.CloudExecutor(
    env="llm-backend",
    num_cpus=8,
    num_gpus=1,
    gpu_type=cc.cloud_executor.GPU_TYPE.L40,
    memory="32GB",
    time_limit="6 hours",
    validate_environment=False,
)


@cc.service(executor=l40_gpu, name="TSP LLM Backend")
def llm_backend_service(model_id: str = "meta-llama/Meta-Llama-3.1-8B-Instruct"):
    """Hosted LLM Backend for various agents."""
    import torch
    import transformers

    pipe = transformers.pipeline(
        "text-generation",
        model=model_id,
        model_kwargs={"torch_dtype": torch.bfloat16, "cache_dir": "/scratch"},
        device_map="auto",
    )
    return {"pipe": pipe}


@llm_backend_service.endpoint("/generate")
def generate(
    pipe=None,
    *,
    messages: List[Dict[str, str]],
    pipe_kwargs: Optional[dict] = None,
    json_schema: Optional[dict] = None,
):
    """Generate a response from a list of messages"""
    if pipe_kwargs is None:
        pipe_kwargs = {"max_new_tokens": 3200}

    if json_schema is None:
        output_dict = pipe(messages, **pipe_kwargs)
    else:
        from lmformatenforcer import JsonSchemaParser
        from lmformatenforcer.integrations.transformers import build_transformers_prefix_allowed_tokens_fn

        parser = JsonSchemaParser(json_schema)
        prefix_function = build_transformers_prefix_allowed_tokens_fn(
            pipe.tokenizer, parser)
        output_dict = pipe(
            messages, prefix_allowed_tokens_fn=prefix_function, **pipe_kwargs)

    return output_dict[0]['generated_text'][-1]


class LLMAgent:
    """Define an LLM Agent with custom prompting and optional response format enforcement."""

    def __init__(
        self,
        system_prompt: str,
        backend: Deployment,
        response_model: Optional[Type[BaseModel]] = None,
        user_prompt_template: str = "{}",
        prepend_messages: Optional[List[Dict[str, str]]] = None,
    ):
        self.backend = backend
        self.system_prompt = system_prompt
        self.response_model = response_model
        self.json_schema = None if response_model is None else response_model.model_json_schema()
        self.user_prompt_template = user_prompt_template
        self.prepend_messages = prepend_messages or []

    def generate(
        self,
        prompt: str,
        **pipe_kwargs
    ) -> Any:
        """Generate a response to a user prompt."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.prepend_messages,
            {"role": "user",
                "content": self.user_prompt_template.format(prompt)},
        ]
        response: Dict[str, str] = self.backend.generate(
            messages=messages,
            pipe_kwargs=None if not pipe_kwargs else pipe_kwargs,
            json_schema=self.json_schema
        )
        if self.response_model is not None:
            response["content"] = self.response_model.model_validate(
                json.loads(response["content"]))
        return response


class RouteIssue(BaseModel):
    """An issue responsible for travel delays along a route between two cities."""

    cities: Tuple[str, str] = Field(
        default=...,
        description="The two cities between which the issue occurs.",
        examples=[("Toronto, ON", "Hamilton, ON"),
                  ("Trenton, NJ", "Philadelphia, PA")]
    )
    reason: str = Field(
        default=...,
        description="Brief description of the reason for the delay.",
        examples=[
            "Poor driving conditions due to heavy snowfall in the tri-state area."
        ],
    )
    severity: int = Field(
        default=...,
        description="An integer between 1 and 5 which indicates the severity of the delay. A severity of 1 represents a minor delay, like a single blocked lane on the freeway, while a severity of 5 implies that travel between the two cities is practically impossible.",
        examples=[1, 2, 3, 4, 5],
    )


class RouteIssuesResponse(BaseModel):
    """A collection of one or more route issues across Canada and the USA."""

    issues: List[RouteIssue] = Field(
        default=...,
        description="A list of route issues, each responsible for a travel delay between a pair of cities.",
    )


CITY_NAME_CORRECTIONS = {
    "New York City, NY": "New York, NY",
    "St. John's, NF": "Saint John's, NF",
}


def process_issues(
    issues: List[RouteIssue],
    base_severity: float = 2.0,
) -> Tuple[List[List[int]], Dict[str, int], List[str]]:

    # Copy the all-to-all distance matrix to scale the edge weights.
    matrix = ALL_DISTANCE_MATRIX.copy()

    no_index_cities = []
    indices = {}
    total_severity = {}

    def _get_index(city: str) -> Union[int, None]:
        if city in no_index_cities:
            return None
        if (idx := indices.get(city)) is not None:
            return idx

        for i, name in enumerate(ALL_CITY_NAMES):
            if city == name:
                idx = i
                break

        if idx is None:
            no_index_cities.append(city)
        else:
            indices[city] = idx
        return idx

    def _scale_weight(weights, severity) -> int:
        severity /= base_severity
        return round(weights * (1 + severity))

    for issue in issues:
        # Map synonyms to canonical city names.
        c1 = CITY_NAME_CORRECTIONS.get(issue.cities[0], issue.cities[0])
        c2 = CITY_NAME_CORRECTIONS.get(issue.cities[1], issue.cities[1])
        if _get_index(c1) is None or _get_index(c2) is None:
            continue

        issue.cities = (c1, c2)
        cities = frozenset(issue.cities)

        # Count (A,B) and (B,A) as the same edge.
        if cities in total_severity:
            total_severity[cities] += issue.severity
        else:
            total_severity[cities] = issue.severity

    # Scale edge weights based on severity.
    for cities, severity in total_severity.items():
        c1, c2 = list(cities)
        i1, i2 = _get_index(c1), _get_index(c2)
        matrix[i1][i2] = matrix[i2][i1] = _scale_weight(
            matrix[i1][i2],
            severity
        )

    return matrix, indices, no_index_cities


SYSTEM_PROMPT_DELAY_INTERPRETER = f"""You are an AI assistant who interprets general information to anticipate travel delays between specific pairs of <cities>.

In your response, refer ONLY to <cities> from the following list:

<cities>
{json.dumps(ALL_CITY_NAMES, indent=2)}
</cities>

Ensure your entire response is parsable JSON according to the <schema> provided.

<schema>
{json.dumps(RouteIssuesResponse.model_json_schema(), indent=2)}
</schema>

Include as many issues as could possibly be anticipated from the user's input.
"""

USER_PROMPT_ISSUES_0 = "The entire US-Canada border is closed due to a massive snowstorm."
ASSISTANT_RESPONSE_ISSUES_0 = """{
  "issues": [
    {
      "cities": [
        "Abilene, TX",
        "Winnipeg, MB"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Akron, OH",
        "Windsor, ON"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Albany, NY",
        "Ottawa, ON"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Albuquerque, NM",
        "Calgary, AB"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Alert, NT",
        "Fairbanks, AK"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Allentown, PA",
        "Sarnia, ON"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Amarillo, TX",
        "Winnipeg, MB"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Anchorage, AK",
        "Whitehorse, YK"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Ann Arbor, MI",
        "Toronto, ON"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Asheville, NC",
        "Sudbury, ON"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Ashland, KY",
        "Niagara Falls, ON"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Atlanta, GA",
        "Montreal, QC"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Atlantic City, NJ",
        "Ottawa, ON"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Augusta, GA",
        "Quebec City, QC"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Augusta, ME",
        "St. John, NB"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Austin, TX",
        "Winnipeg, MB"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Bakersfield, CA",
        "Calgary, AB"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Baltimore, MD",
        "Toronto, ON"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Bangor, ME",
        "Moncton, NB"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    },
    {
      "cities": [
        "Baton Rouge, LA",
        "Winnipeg, MB"
      ],
      "reason": "The entire US-Canada border is closed due to a massive snowstorm, preventing travel between the two countries and causing delays for those attempting to cross the border by land or air",
      "severity": 5
    }
  ]
}"""

USER_PROMPT_ISSUES_1 = """Long-term construction has begun across Highway 401, with lane reductions expected to cause delays in both directions.

Laura Kelly has announced new road construction that will affect travel between Wichita and Joplin."""
ASSISTANT_RESPONSE_ISSUES_1 = """{
  "issues": [
    {
      "cities": [
        "Toronto, ON",
        "Hamilton, ON"
      ],
      "reason": "Long-term construction has begun across Highway 401, with lane reductions expected to cause delays in both directions",
      "severity": 3
    },
    {
      "cities": [
        "London, ON",
        "Kitchener, ON"
      ],
      "reason": "Long-term construction has begun across Highway 401, with lane reductions expected to cause delays in both directions",
      "severity": 3
    },
    {
      "cities": [
        "Kitchener, ON"
        "Guelph, ON",
      ],
      "reason": "Long-term construction has begun across Highway 401, with lane reductions expected to cause delays in both directions",
      "severity": 3
    },
    {
      "cities": [
        "Wichita, KS",
        "Joplin, MO"
      ],
      "reason": "New road construction project announced by Laura Kelly",
      "severity": 2
    }
  ]
}"""

USER_PROMPT_ISSUES_2 = "Earthquake cleanup continues in British Columbia; premier announces new task force to deliver supplies."
USER_PROMPT_ISSUES_3 = "Avalanches continue in the southern Rockies, putting winter travel plans at risk in the Northwest."


class TSP(BaseModel):
    """A solution to a Traveling Salesman Problem."""

    matrix: List[List[int]] = Field(
        default_factory=lambda: ALL_DISTANCE_MATRIX.copy())
    """All-to-all distance matrix between cities."""

    issues: List[RouteIssue] = Field(default_factory=list)
    """A list of route issues responsible for travel delays between pairs of cities."""

    no_index_cities: List[str] = Field(default_factory=list)
    """LLM-chosen cities that could not be found in the distance matrix."""

    indices: Dict[str, int] = Field(default_factory=dict)
    """Mapping of city names to indices in the distance matrix."""

    tour: List[int] = Field(default_factory=list)
    """Shortest path through all cities."""

    @property
    def cities(self) -> List[str]:
        """List of cities considered in the issues."""
        return list(self.indices.keys())


cc.create_env(name="tsp-solver", pip=["numpy==1.23.5"],
              conda=["anaconda::make", "conda-forge::gcc"], wait=True)


small_cpu = cc.CloudExecutor(
    env="tsp-solver", num_cpus=4, memory="12GB", time_limit="6 hours")
large_cpu = cc.CloudExecutor(
    env="tsp-solver", num_cpus=12, memory="24GB", time_limit="6 hours")


@ct.electron(executor=small_cpu)
def llama_analysis_agent(
    agent: LLMAgent,
    info: str,
) -> RouteIssuesResponse:
    return agent.generate(prompt=info)["content"]


@ct.electron(executor=large_cpu, deps_bash=f"echo '{CONCORDE_SETUP_SCRIPT}' | /bin/sh")
def solver(issues_response: Optional[RouteIssuesResponse] = None, base_severity: float = 2.0) -> dict:
    """CPU-based task that solves a TSP problem using Concorde."""
    if issues_response is None:
        tsp_data = TSP()
    else:
        issues = issues_response.issues
        matrix, indices, no_index_cities = process_issues(
            issues, base_severity)
        tsp_data = TSP(
            matrix=matrix,
            issues=[i.model_dump() for i in issues],
            no_index_cities=no_index_cities,
            indices=indices
        )

    # Read executable path created by setup script
    with open(Path.home() / "concorde_path.txt", "r", encoding="utf-8") as f:
        concorde_executable_path = f.read().strip()

    # Create a TSP File and solve the TSP problem
    tsp_file = TSPFile.from_distance_matrix(
        tsp_data.matrix,
        type="TSP",
        name="US/CA trip",
        comment="LLM-adjusted TSP file",
    )
    solver = ConcordeSolver(concorde_executable_path)
    tsp_data.tour = solver.solve(tsp_file.to_file("usca312.tsp"))
    return tsp_data.model_dump()


@ct.electron(executor=small_cpu)
def collect_results(sol1, sol2, sol3, sol4) -> List[dict]:
    """Convert TSP data to a list of dictionaries for easier parsing."""
    new_tsp_data_list = []
    for tsp_data in [sol1, sol2, sol3, sol4]:
        if len(tsp_data["issues"]) == 0 and len(tsp_data["invalid_cities"]) != 0:
            # Skip fully invalid solutions.
            continue
        # Make tour circular (back to start)
        tsp_data["tour"].append(tsp_data["tour"][0])
        new_tsp_data_list.append(tsp_data)

    return new_tsp_data_list


@ct.lattice(executor=small_cpu, workflow_executor=small_cpu)
def get_tsp_solution(llm: LLMAgent, info: str) -> List[dict]:
    if info:
        ai_issues_output = llama_analysis_agent(llm, info)
        sol1 = solver(ai_issues_output, base_severity=1.0)
        sol2 = solver(ai_issues_output, base_severity=2.0)
        sol3 = solver(ai_issues_output, base_severity=3.0)
        sol4 = solver(ai_issues_output, base_severity=4.0)
        return collect_results(sol1, sol2, sol3, sol4)

    return [solver()]  # default solution weighted only by distance


@cc.service(executor=small_cpu, name="TSP Interface Service")
def tsp_interface_service(llm_backend):
    """Solve a traveling salesman problem with AI-weighted edges."""
    cc.save_api_key(CC_API_KEY)
    llm = LLMAgent(
        system_prompt=SYSTEM_PROMPT_DELAY_INTERPRETER,
        backend=llm_backend,
        response_model=RouteIssuesResponse,
        prepend_messages=[
            {"role": "user", "content": USER_PROMPT_ISSUES_0},
            {"role": "assistant", "content": ASSISTANT_RESPONSE_ISSUES_0},
            {"role": "user", "content": USER_PROMPT_ISSUES_1},
            {"role": "assistant", "content": ASSISTANT_RESPONSE_ISSUES_1},
        ]
    )
    return {"llm": llm}


@tsp_interface_service.endpoint("/solve")
def solve_tsp(
    llm: LLMAgent,
    *,
    info: str = "",
    redispatch_id: str = "",
    wait: bool = True,
):
    """Get the optimal route. Pass a `redispatch_id` to redispatch an existing solver workflow."""
    cc_dispatch = cc.redispatch if redispatch_id else cc.dispatch
    response = {"id": cc_dispatch(get_tsp_solution)(llm, info)}
    if not wait:
        return response

    result = cc.get_result(response["id"], wait=True).result
    result.load()
    response.update(result=result.value)
    return response


latt_ex = cc.CloudExecutor(env="llm-backend", num_cpus=1, memory="4GB")


@ct.lattice(executor=latt_ex, workflow_executor=latt_ex)
def llm_tsp_setup() -> Deployment:
    """Create the Covalent function services that power the TSP application."""
    llm_backend = llm_backend_service()
    return llm_backend, tsp_interface_service(llm_backend)


dispatch_id = cc.dispatch(llm_tsp_setup)()
