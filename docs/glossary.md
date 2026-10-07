# Glossary

Plain-language definitions of the terms used in this course, grouped by topic. Use your browser's find (Ctrl+F / ⌘F) to jump to a word.

## Your computer

Terminal (shell, command line)
:   A text window where you type commands instead of clicking. PowerShell on Windows, Terminal on macOS and Linux.

Folder (directory) and path
:   A folder holds files. A **path** is a folder or file's address, like `labs/week01/01_hello.py`. A *relative* path starts from where you are now; an *absolute* path starts from the top of the drive.

Code editor
:   An app for writing code. The course uses VS Code.

## Python

Script
:   A file of Python code (`.py`) you run with `python file.py`.

Function
:   A named, reusable block of code that takes inputs and returns an output.

List / dictionary
:   A **list** is an ordered collection (`[1, 2, 3]`). A **dictionary** maps keys to values (`{"name": "Ava", "age": 31}`).

Exception (error)
:   What Python raises when something goes wrong, such as a missing file. You can *catch* it with `try` / `except`.

Package and pip
:   A **package** is code someone else wrote that you can install and use. **pip** installs packages.

Virtual environment (venv)
:   A private folder of packages for one project, so projects don't interfere with each other. This course's is `.venv`.

Test (pytest)
:   Code that checks other code gives the right answers. **pytest** finds and runs tests.

## Git and GitHub

Repository (repo)
:   A project folder whose history git tracks.

Commit
:   A saved snapshot of your changes, with a message saying what changed.

Clone / fork
:   **Clone** downloads a repo to your computer. **Fork** makes your own copy of someone else's repo on GitHub.

Push / pull
:   **Push** uploads your commits to GitHub; **pull** downloads new commits.

Branch
:   A separate line of work in a repo, so you can try things without touching the main version.

GitHub Actions / CI
:   Automation that runs on GitHub when you push, e.g. running tests. **CI** (continuous integration) is the general name.

GitHub Pages
:   GitHub's free website hosting. This site is published with it.

## The web and APIs

API
:   A way for programs to talk to each other. A **web API** accepts requests over the internet and returns data.

HTTP, endpoint, status code
:   **HTTP** is the protocol of the web. An **endpoint** is one API address (a URL). A **status code** says how a request went: 200 OK, 400 bad request, 401 not authorised, 404 not found, 429 too many requests, 500 server error.

JSON
:   A text format for data that looks like Python lists and dictionaries. Most APIs use it.

API key
:   A secret string that identifies you to an API. Treat it like a password.

Environment variable / `.env` file
:   Settings kept outside your code. This course keeps them in `labs/.env`, which git never uploads.

SDK
:   A package that makes an API easier to use from a programming language, e.g. the `anthropic` Python package.

## Working with Claude

Model
:   The AI system that generates responses. Claude comes in several models that trade speed and cost against capability.

Prompt / system prompt
:   The text you send. The **system prompt** sets the role, rules and context; the **user message** is the specific request.

Token
:   The unit models read and write, roughly a short word or part of a word. You pay per token.

Context window
:   The maximum amount of text (in tokens) a model can consider at once.

Streaming
:   Receiving the response piece by piece as it's generated, instead of all at the end.

Structured outputs / schema
:   Making the model's answer follow a **schema**, a precise description of fields and types, so your code can rely on its shape.

Prompt caching
:   Reusing the processed start of a long prompt across requests, which is cheaper and faster.

Agent / tool use
:   An **agent** is a system where the model decides on steps and calls **tools** (functions you provide) to act, such as looking up an order.

RAG (retrieval-augmented generation)
:   Finding relevant documents first and giving them to the model so it answers from them.

MCP (Model Context Protocol)
:   An open standard for connecting AI applications to tools and data sources.

## Quality and safety

Eval
:   A repeatable test of an AI system's quality: run it on known cases and measure the results.

Golden set
:   The known cases for an eval: inputs plus the answers experts agree are right.

Grader / LLM-as-judge
:   A **grader** scores outputs. Code graders check exact things; an **LLM-as-judge** uses a model to score things code can't, such as whether a summary is faithful.

Regression
:   Something that used to work and broke after a change.

Acceptance criteria
:   The measurable conditions, agreed with a customer, that say "this is good enough to ship".

Prompt injection
:   Text hidden in content (an email, a web page, a log line) that tries to give an AI system new instructions. Treat it as data, never as commands.

Redaction
:   Removing or masking sensitive details (keys, card numbers, emails) before text is sent anywhere.

Rate limit / spend limit
:   Caps on how many requests you can make, or how much you can spend, in a period.

Latency
:   How long a response takes.

## Delivery

Forward Deployed Engineer (FDE)
:   An engineer who works with a customer to build, prove and hand over systems that fit the customer's environment.

Discovery
:   The early phase where you learn what the customer actually needs, who will use it, and what constraints apply.

Capstone
:   The end-of-phase project, run like a real engagement.

Handover
:   Giving the customer everything they need to run and change the system without you.

## Security track (optional)

SIEM / Splunk
:   A **SIEM** collects and searches security logs; **Splunk** is a popular one.

HEC (HTTP Event Collector)
:   Splunk's web API for sending in events.

Docker / container
:   A tool for running software in an isolated, disposable package called a container.
