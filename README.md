# Clarity – Senior Developer Code Test

## Table of contents
1. [:memo: Challenge description](#desc)
2. [:dart: Goals to Achieve](#goals)
3. [:toolbox: Solution](#solution)
4. [:package: Installation](#install)
5. [:white_check_mark: Testing](#tests)
6. [:hammer: Future Work](#future-work)
7. [:memo: License](#license)

    <div id="desc"></div>

## :memo: Challenge description

The exercise consists of implementing a console-based social networking app
satisfying the scenarios below:

### Scenarios

**Posting**: Anyone can publish messages on their personal timeline:
```
Unset
> Alice -> I love the weather today
> Bob -> Damn! We lost!
> Bob -> Good game though.
```

**Reading**: Anyone can view anyone’s timeline
```
Unset
> Alice
I love the weather today (5 minutes ago)
> Bob
Good game though. (1 minute ago)
Damn! We lost! (2 minutes ago)
```

**Following**: Anyone can subscribe to anyone’s timelines,
and view an aggregated list of all subscriptions.

```
Unset
> Charlie -> I'm in New York today! Anyone want to have a coffee?
> Charlie follows Alice
> Charlie wall
Charlie - I'm in New York today! Anyone want to have a coffee? (2
seconds ago)
Alice - I love the weather today (5 minutes ago)

> Charlie follows Bob
> Charlie wall
Charlie - I'm in New York today! Anyone wants to have a coffee?
(15 seconds ago)
Bob - Good game though. (1 minute ago)
Bob - Damn! We lost! (2 minutes ago)
Alice - I love the weather today (5 minutes ago)
```

<div id="goals"></div>

## :dart: Goals to Achieve

### Requirements

- The application must use the console for input and output.
- Users submit commands to the application.
- Commands always start with the user’s name.
- There are four types commands:
    - **posting**: user name -> message
    - **reading**: user name
    - **following**: user name follows another user
    - **wall**: user name wall

### Expectations

- **Focus on Core Logic**:
We want to assess your problem-solving skills and coding style.
Therefore, please keep the implementation focused on the application’s core logic.
There's no need to use external frameworks or databases for this exercise.
Simple, in-memory data structures are perfectly acceptable.
- **Emphasis on Testing**:
We highly value robust and reliable software.
Demonstrating your commitment to testing is crucial.
We encourage you to showcase your testing approach to ensure the quality
and correctness of your solution.
- **Test-Driven Development (TDD) - A Bonus**:
While not mandatory, applying Test-Driven Development principles would be a plus.
- **Code Clarity and Approach**:
We are very interested in seeing your code, understanding your design choices,
and how you approach problem-solving.
Please write clean, well-structured, and easy-to-understand code.
- **Iterative Development (Baby Steps)**:
We appreciate seeing the evolution of your solution.
We value an iterative development approach,
breaking down the problem into smaller, manageable steps.
Committing your code frequently to a version control system (like Git)
to reflect these steps is highly encouraged.
This allows us to understand your thought process
and how you build up the solution incrementally.
- **Time Commitment**:
While we understand you have other commitments
and are not strictly timing this test,
we believe a reasonable timeframe to complete this exercise with quality
would be around three hours.
- **Sharing Your Solution**:
Once you have completed the test, please share the repository
(e.g., GitHub, GitLab, Bitbucket) containing your code with us
so we can review your work.
- **Extensibility and Adaptability**:
Consider that real-world applications often evolve.
Design your solution to be extensible and adaptable to potential future requirements.
While you only need to implement the current scenarios,
think about how easily your code could be modified or expanded.
Demonstrating foresight in design for change is a valuable skill.

<div id="solution"></div>

## :toolbox: Solution

I have opted to build a simple [**Python**](https://www.python.org) library
that leverages [**Object-Oriented Programming (OOP)**](https://en.wikipedia.org/wiki/Object-oriented_programming) principles.

Note that the proposed solution also follows the [**Single Responsibility Principle (SRP)**](https://en.wikipedia.org/wiki/Single_responsibility_principle):
- Each class has a clear, single purpose.
- Responsibilities are properly separated.
- Changes to one aspect don't require changes to others.
- Classes work together through well-defined interfaces.

This makes the code more maintainable, testable, and easier to extend.

The source code of the proposed solution is located in `src/sr_sw_dev/`.

Here's a brief description of each class in the social networking
application:

#### Post

The `Post` class represents a single message in the social network.

- Contains content and timestamp.
- Supports chronological sorting and author attribution.
- Formats elapsed time since creation.

#### User

The `User` class represents a user in the social network.

- Manages user's posts and following relationships.
- Provides timeline and wall views of posts.
- Handles post creation and user following.

#### Social Network

The `SocialNetwork` class manages the collection of users in the social network.

- Provides user management (add, find, count).
- Handles post creation and retrieval.
- Manages following relationships between users.

#### Application

The `Application` class provides the command-line interface.

- Parses and executes user commands.
- Supports posting, following, and viewing timelines/walls.
- Handles error cases and user input validation.

<div id="install"></div>

## :package: Installation

To install the proposed solution as a Python library,
run the following shell command from the root directory of this project:

```
pip install --upgrade build
python -m build
python -m pip install .
```

Once installed, run the following command to see it in action:

```
python src/sr_sw_dev/social_networking.py
```

<div id="tests"></div>

## :white_check_mark: Testing

Writing tests for your code is a great practice.
Tests helps you not only identify and resolve issues early but also debug your code faster.
As a result, tests boost your productivity and promote more robust software.
If you depend on a chunk of code, you should write tests for it.

During software development, you may inadvertently alter
an existing chunk of code on which your project depends.
This change may break other functions or workflows
that rely on that code snippet.
Writing tests that get automatically executed automatically and continuously
will help you catch these changes before you merge them into your codebase.

I opted to use [pytest](https://docs.pytest.org/en/stable/) to write some tests
to ensure that my social networking application behaves as expected.
`pytest` makes it easy to write small and readable tests,
and is also well-equipped to grow in complexity if needed.

See `tests/` for more details about the written tests.

To automatically run all the tests included in this project,
execute the following shell command from the main directory:
```
pytest tests
```

You may want to get more details about the test coverage
by running the following shell command:
```
pytest tests --cov=src.sr_sw_dev --cov-report=term-missing
```

Note that other tools such as [mypy](https://www.mypy-lang.org/index.html)
(a static type checker) could also help you identify bugs in your programs
without even running them!

#### :traffic_light: Test-Driven Development

I have applied [**Test-Driven Development (TDD)**](https://en.wikipedia.org/wiki/Test-driven_development) principles to this project.
This means that I have written the tests before the code.
This is a great practice because it forces you to think about the requirements
and the expected behavior of the code before you actually write it.

<div id="future-work"></div>

## :hammer: Future Work

Future work could focus on the following aspects:

1. I could leverage **short-lived feature branches** to keep track of my progress during the TDD process (until I got the tests to pass)[^1][^2].

2. Short-lived branches would allow me to set up a **CI pipeline**
to run the tests automatically in the main branch,
blocking merges into the main branch until the tests pass[^3][^4].
This would:
    - Catch bugs early, before they are merged into the main branch.
    - Ensure the code in the main branch is always in a working state.

3. I could leverage **pre-commit hooks** to run ruff linting and formatting
before committing my changes to ensure code quality[^5].

4. The proposed implementation of the `Application` class could be improved
for future extensibility.
For instance, it currently hardcodes the available commands.
However, the current implementation is already flexible enough to support
new commands without breaking existing functionality.

<div id="license"></div>

## :memo: License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.

[^1]: See Git official documentation
for more details on Git branching strategies (accessed on 2025-04-18):
https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows
[^2]: See Trunk-based Development site
for more details about short-lived feature branches, potential pitfalls, and alternatives (accessed on 2025-04-18):
https://trunkbaseddevelopment.com/short-lived-feature-branches/
[^3]: See Trunk-based Development site
for more details about continuous integration (accessed on 2025-04-18):
https://trunkbaseddevelopment.com/continuous-integration/
[^3]: See Github Actions official documentation for more details about
building and testing Python applications (accessed on 2025-04-18):
https://docs.github.com/en/actions/use-cases-and-examples/building-and-testing/building-and-testing-python
[^4]: See Ruff official documentation for more details about
integrating Ruff with Github Actions (accessed on 2025-04-18):
https://docs.astral.sh/ruff/integrations/#github-actions
[^5]: See Ruff official documentation for more details about
integrating Ruff with pre-commit hooks (accessed on 2025-04-18):
https://docs.astral.sh/ruff/integrations/#pre-commit