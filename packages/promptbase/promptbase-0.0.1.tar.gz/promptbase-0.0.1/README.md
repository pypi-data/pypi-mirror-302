# PromptBase

**PromptBase** is a cutting-edge paradigm designed to provide a holistic approach to managing prompts in applications or with users. Traditional LLM (Large Language Model) applications typically have a codebase and a database, with prompts either embedded in the code or stored in the database. However, both approaches have limitations and are not always feasible due to various reasons, such as maintainability, scalability, and flexibility.

PromptBase addresses these challenges by offering a comprehensive solution for prompt management, testing, optimization, and organization. It enables developers and teams to store prompts along with sample inputs and outputs, perform A/B testing, optimize prompts using LLM agents, and much more.

---

## Table of Contents

- [Key Features](#key-features)
- [Why PromptBase?](#why-promptbase)
- [Installation](#installation)
- [Getting Started](#getting-started)
  - [Creating Prompts](#creating-prompts)
  - [Organizing Prompts](#organizing-prompts)
  - [Versioning](#versioning)
- [Usage Examples](#usage-examples)
  - [Running Prompt Tests](#running-prompt-tests)
  - [Prompt Optimization](#prompt-optimization)
  - [Safety Checks](#safety-checks)
  - [Annotations and Notes](#annotations-and-notes)
- [API Integration](#api-integration)
- [Additional Tools](#additional-tools)
  - [Format Conversion](#format-conversion)
  - [Auto Translation](#auto-translation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Key Features

- **Prompt Storage with Samples**: Store your prompts along with sample inputs and outputs to maintain context and reference implementations.
- **Embedded A/B Testing Tools**: Automatically assess prompt quality using embedded LLM-based A/B testing tools.
- **Multi-Model Testing**: Run prompt tests across multiple models without the need to run your main application.
- **LLM Agents for Optimization**: Utilize LLM agents to optimize prompts for better performance and results.
- **Hierarchical Organization**: Organize prompts by hierarchy, type, and version for easy management.
- **Safety and Vulnerability Checks**: Embedded tools to check prompt safety and reduce vulnerabilities.
- **API Access**: Optionally provide an API for external applications to interact with the prompt database.
- **Annotations and Notes**: Enable users to add notes or explanations to prompts for better collaboration.
- **Format Conversion**: Support converting prompts between different formats or models.
- **Auto Translation**: Use auto prompt translation tools to support multiple languages.

---

## Why PromptBase?

In traditional LLM applications, prompts are often hard-coded or stored in databases without proper management, making it difficult to maintain, update, or optimize them. PromptBase offers a solution by providing:

- **Centralized Management**: Keep all your prompts in one place with proper organization and version control.
- **Scalability**: Efficiently manage hundreds or thousands of prompts without clutter or confusion.
- **Collaboration**: Enhance teamwork with features like annotations, versioning, and shared access.
- **Optimization Tools**: Improve the effectiveness of your prompts using built-in testing and optimization features.
- **Flexibility**: Easily adapt prompts for different models, formats, or languages.

---

## Installation

To install PromptBase, use the following command:

```bash
pip install promptbase
```

**Note**: Ensure that you have Python 3.7 or higher installed.

---

## Getting Started

### Creating Prompts

Begin by creating prompts and storing them in PromptBase along with sample inputs and outputs:

```python
from promptbase import PromptBase

# Initialize PromptBase
pb = PromptBase()

# Create a new prompt
prompt_id = pb.create_prompt(
    name="Customer Support Response",
    content="Dear {customer_name},\n\nThank you for reaching out...",
    samples={
        "input": {"customer_name": "John Doe"},
        "output": "Dear John Doe,\n\nThank you for reaching out..."
    },
    tags=["customer support", "email"],
    version="1.0"
)
```

### Organizing Prompts

Organize your prompts using hierarchies, tags, and types:

```python
# Add tags or categories
pb.add_tags(prompt_id, ["urgent", "priority"])

# Move prompt to a different category
pb.move_prompt(prompt_id, new_category="Support Emails")
```

### Versioning

Maintain different versions of your prompts:

```python
# Update prompt content and create a new version
pb.update_prompt(
    prompt_id,
    new_content="Hello {customer_name},\n\nWe appreciate your feedback...",
    version="1.1"
)

# Retrieve a specific version
prompt_v1 = pb.get_prompt(prompt_id, version="1.0")
```

---

## Usage Examples

### Running Prompt Tests

Test prompts across multiple models:

```python
# Define models to test
models = ["gpt-3", "gpt-4"]

# Run tests
test_results = pb.run_tests(prompt_id, models=models)

# View results
for model, result in test_results.items():
    print(f"Model: {model}")
    print(f"Output: {result['output']}")
    print(f"Evaluation Score: {result['score']}")
```

### Prompt Optimization

Use LLM agents to optimize prompts:

```python
# Optimize prompt for better clarity
optimized_prompt = pb.optimize_prompt(prompt_id, goal="Improve clarity")

# Save optimized prompt as a new version
pb.update_prompt(
    prompt_id,
    new_content=optimized_prompt,
    version="1.2"
)
```

### Safety Checks

Check prompts for potential vulnerabilities or safety issues:

```python
# Run safety check
safety_report = pb.check_safety(prompt_id)

# View report
print(safety_report)
```

### Annotations and Notes

Add annotations or notes to prompts:

```python
# Add a note
pb.add_annotation(prompt_id, "This prompt needs to be updated for GDPR compliance.")

# Retrieve annotations
annotations = pb.get_annotations(prompt_id)
```

---

## API Integration

PromptBase provides an optional API for external applications to interact with the prompt database.

```python
# Enable API access
pb.enable_api(access_token="your_api_token")

# Use the API to fetch a prompt
import requests

response = requests.get(
    "https://api.promptbase.com/prompts/{prompt_id}",
    headers={"Authorization": "Bearer your_api_token"}
)

prompt_data = response.json()
```

---

## Additional Tools

### Format Conversion

Convert prompts between different formats or models:

```python
# Convert prompt to a format compatible with a specific model
converted_prompt = pb.convert_format(prompt_id, target_format="openai")
```

### Auto Translation

Automatically translate prompts to support multiple languages:

```python
# Translate prompt to Spanish
translated_prompt = pb.translate_prompt(prompt_id, target_language="es")

# Save translated prompt
pb.create_prompt(
    name="Customer Support Response (Spanish)",
    content=translated_prompt,
    tags=["customer support", "email", "spanish"],
    version="1.0"
)
```

---

## Contributing

We welcome contributions from the community! If you'd like to contribute to PromptBase, please follow these steps:

1. **Fork the repository** on GitHub.
2. **Create a new branch** for your feature or bug fix.
3. **Commit your changes** with clear and descriptive messages.
4. **Submit a pull request**, detailing the changes you've made and any issues that are fixed.

Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

---

## License

PromptBase is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software in accordance with the terms of the license.

---

## Contact

For questions, suggestions, or support, please reach out to:

- **Email**: support@promptbase.com
- **GitHub Issues**: [https://github.com/your_username/promptbase/issues](https://github.com/your_username/promptbase/issues)

---

**Note**:

- Replace placeholders like `your_username` and contact details with actual information.
- Ensure that you include a `LICENSE` file in your repository specifying the terms under which others can use your code.
- Add more detailed instructions or documentation as needed, especially in the code examples.

---

By providing a comprehensive README, users and contributors can better understand the purpose of PromptBase, how to use it, and how they can contribute to its development.
