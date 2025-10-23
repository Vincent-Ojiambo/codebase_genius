# Import utility functions from Python module
py_module utils from "./utils";

# Node types for representing code structure
node Repo {
    has url: str;
    has name: str;
    has path: str;
    has readme_summary: str;
    has file_tree: Dict[str, Any];
    has analysis_status: str = "pending";
    has documentation: str = "";
}

node File {
    has path: str;
    has type: str;  # python, jac, etc.
    has size: int;
    has content: str = "";
    has parsed: bool = false;
    has dependencies: List[File];
    has functions: List[str];
    has classes: List[str];
}

node Function {
    has name: str;
    has file: File;
    has calls: List[Function];
    has called_by: List[Function];
    has parameters: List[str];
    has docstring: str = "";
}

node Class {
    has name: str;
    has file: File;
    has methods: List[Function];
    has inherits_from: List[Class];
    has docstring: str = "";
}

node Documentation {
    has repo: Repo;
    has sections: Dict[str, str];
    has diagrams: Dict[str, str];
    has generated_at: str;
}

# Edge types
edge has_file(Repo, File);
edge calls(Function, Function);
edge defines(File, Function);
edge defines(File, Class);
edge inherits(Class, Class);
edge contains(Class, Function);

# Main graph
graph CodebaseGraph {
    has repos: List[Repo];
    has current_repo: Repo?;
}

# Supervisor agent - orchestrates the entire workflow
walker CodeGenius {
    has graph: CodebaseGraph;

    can process_repo with url: str {
        # Validate URL and clone repository
        if not self._validate_url(url) {
            return "Error: Invalid repository URL";
        }

        repo_name = self._extract_repo_name(url);
        temp_path = self._clone_repo(url, repo_name);

        if not temp_path {
            return "Error: Failed to clone repository";
        }

        # Create repository node
        repo = Repo(
            url=url,
            name=repo_name,
            path=temp_path,
            readme_summary="",
            file_tree={},
            analysis_status="cloning_complete"
        );

        self.graph.repos.append(repo);
        self.graph.current_repo = repo;

        # Start the documentation pipeline
        return self._orchestrate_documentation(repo);
    }

    can _validate_url with url: str -> bool {
        # Use utility function for better validation
        return utils.ValidationUtils.validate_github_url(url);
    }

    can _extract_repo_name with url: str -> str {
        # Extract repository name from GitHub URL
        match = re.search(r"github\.com/([^/]+/[^/]+?)(?:\.git)?/?$", url);
        return match.group(1).replace("/", "_") if match else "unknown_repo";
    }

    can _clone_repo with url: str, repo_name: str -> str? {
        try {
            temp_dir = tempfile.mkdtemp(prefix=f"codebase_genius_{repo_name}_");
            result = subprocess.run(
                ["git", "clone", url, temp_dir],
                capture_output=True,
                text=True,
                timeout=300
            );

            if result.returncode == 0 {
                return temp_dir;
            } else {
                shutil.rmtree(temp_dir, ignore_errors=True);
                return None;
            }
        } catch {
            return None;
        }
    }

    can _orchestrate_documentation with repo: Repo -> str {
        # Phase 1: Repository mapping
        self._log("Starting repository mapping phase");
        mapping_result = RepoMapper().map_repository(repo.path);

        if not mapping_result {
            return "Error: Failed to map repository";
        }

        repo.file_tree = mapping_result["file_tree"];
        repo.readme_summary = mapping_result["readme_summary"];
        repo.analysis_status = "mapping_complete";

        # Phase 2: Code analysis
        self._log("Starting code analysis phase");
        analysis_result = CodeAnalyzer().analyze_codebase(repo.path, repo.file_tree);

        if not analysis_result {
            return "Error: Failed to analyze codebase";
        }

        repo.analysis_status = "analysis_complete";

        # Phase 3: Documentation generation
        self._log("Starting documentation generation phase");
        documentation = DocGenie().generate_documentation(
            repo,
            analysis_result,
            repo.file_tree,
            repo.readme_summary
        );

        repo.documentation = documentation;
        repo.analysis_status = "documentation_complete";

        # Save documentation
        output_path = self._save_documentation(repo);
        return f"Documentation generated successfully: {output_path}";
    }

    can _log with message: str {
        print(f"[CodeGenius] {message}");
    }

    can _save_documentation with repo: Repo -> str {
        output_dir = f"./outputs/{repo.name}";
        os.makedirs(output_dir, exist_ok=True);

        docs_path = f"{output_dir}/README.md";
        with open(docs_path, "w") as f {
            f.write(repo.documentation);

        return docs_path;
    }
}

# Repository Mapper agent
walker RepoMapper {
    can map_repository with repo_path: str -> Dict[str, Any]? {
        try {
            # Build file tree
            file_tree = self._build_file_tree(repo_path);

            # Generate README summary
            readme_summary = self._summarize_readme(repo_path);

            return {
                "file_tree": file_tree,
                "readme_summary": readme_summary
            };
        } catch {
            return None;
        }
    }

    can _build_file_tree with repo_path: str -> Dict[str, Any] {
        file_tree = {"name": os.path.basename(repo_path), "type": "directory", "children": []};

        for root, dirs, files in os.walk(repo_path) {
            # Skip irrelevant directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.git']];

            relative_root = os.path.relpath(root, repo_path);
            current_node = file_tree;

            if relative_root != "." {
                for part in relative_root.split(os.sep) {
                    for child in current_node["children"] {
                        if child["name"] == part and child["type"] == "directory" {
                            current_node = child;
                            break;
                    }
            }

            for file in files {
                if not file.startswith('.') and file.endswith(('.py', '.jac', '.md', '.txt', '.js', '.ts', '.java', '.cpp', '.c', '.h')) {
                    file_path = os.path.join(root, file);
                    file_size = os.path.getsize(file_path);

                    current_node["children"].append({
                        "name": file,
                        "type": "file",
                        "path": os.path.relpath(file_path, repo_path),
                        "size": file_size,
                        "extension": os.path.splitext(file)[1]
                    });
                }
            }
        }

        return file_tree;
    }

    can _summarize_readme with repo_path: str -> str {
        readme_paths = ["README.md", "README.txt", "readme.md", "README.rst"];

        for readme_path in readme_paths {
            full_path = os.path.join(repo_path, readme_path);
            if os.path.exists(full_path) {
                try {
                    with open(full_path, "r", encoding="utf-8") as f {
                        content = f.read();

                    # Simple summary extraction
                    lines = content.split('\n');
                    title = "";
                    description = "";
                    installation = "";
                    usage = "";

                    for line in lines[:50]:  # First 50 lines
                        line = line.strip();
                        if line.startswith('# ') and not title {
                            title = line[2:].strip();
                        } elif line.startswith('## ') and 'install' in line.lower() and not installation {
                            installation = line;
                        } elif line.startswith('## ') and 'usage' in line.lower() and not usage {
                            usage = line;
                        } elif line and not description and len(line) > 20 {
                            description = line;

                    summary = f"**{title}**\n\n{description}\n\n";
                    if installation:
                        summary += f"**Installation:** {installation}\n\n";
                    if usage:
                        summary += f"**Usage:** {usage}\n\n";

                    return summary;
                } except:
                    continue;
        }

        return "No README found or unable to parse.";
    }
}

# Code Analyzer agent
walker CodeAnalyzer {
    can analyze_codebase with repo_path: str, file_tree: Dict[str, Any] -> Dict[str, Any]? {
        try {
            analysis = {
                "functions": {},
                "classes": {},
                "dependencies": {},
                "call_graph": {},
                "inheritance_graph": {}
            };

            # Analyze each file
            self._analyze_files(repo_path, file_tree, analysis);

            # Build call graph
            self._build_call_graph(analysis);

            # Build inheritance graph
            self._build_inheritance_graph(analysis);

            return analysis;
        } catch {
            return None;
        }
    }

    can _analyze_files with repo_path: str, file_tree: Dict[str, Any], analysis: Dict[str, Any] {
        def process_node(node: Dict[str, Any]) {
            if node["type"] == "file" and node["extension"] in [".py", ".jac"] {
                file_path = os.path.join(repo_path, node["path"]);
                if os.path.exists(file_path) {
                    self._analyze_file(file_path, node, analysis);
                }
            } elif node["type"] == "directory" and "children" in node {
                for child in node["children"] {
                    process_node(child);
                }
            }
        }

        process_node(file_tree);
    }

    can _analyze_file with file_path: str, file_node: Dict[str, Any], analysis: Dict[str, Any] {
        try {
            with open(file_path, "r", encoding="utf-8") as f {
                content = f.read();

            if file_node["extension"] == ".py" {
                self._analyze_python_file(content, file_path, analysis);
            } elif file_node["extension"] == ".jac" {
                self._analyze_jac_file(content, file_path, analysis);
            }
        } catch {
            # Skip files that can't be read
            pass;
        }
    }

    can _analyze_python_file with content: str, file_path: str, analysis: Dict[str, Any] {
        # Use utility functions for better analysis
        functions = utils.TextProcessor.extract_functions_python(content);
        classes = utils.TextProcessor.extract_classes_python(content);
        imports = utils.TextProcessor.extract_imports_python(content);

        # Store functions with enhanced information
        for func in functions {
            if func["name"] not in analysis["functions"] {
                analysis["functions"][func["name"]] = {
                    "file": file_path,
                    "calls": [],
                    "called_by": [],
                    "parameters": func["parameters"],
                    "docstring": func["docstring"],
                    "line_start": func["line_start"],
                    "complexity": utils.TextProcessor.calculate_cyclomatic_complexity(content)
                };
            }
        }

        # Store classes with enhanced information
        for cls in classes {
            if cls["name"] not in analysis["classes"] {
                analysis["classes"][cls["name"]] = {
                    "file": file_path,
                    "methods": [],
                    "inherits_from": cls["inherits_from"],
                    "docstring": cls["docstring"],
                    "line_start": cls["line_start"]
                };
            }
        }

        # Store dependencies
        analysis["dependencies"][file_path] = {
            "imports": imports,
            "functions": [f["name"] for f in functions],
            "classes": [c["name"] for c in classes]
        };
    }

    can _analyze_jac_file with content: str, file_path: str, analysis: Dict[str, Any] {
        # Similar analysis for Jac files using regex patterns
        functions = re.findall(r'can\s+(\w+)', content);
        classes = re.findall(r'node\s+(\w+)', content);
        imports = re.findall(r'import\s+([^\n;]+)', content);

        # Store in analysis
        for func in functions {
            if func not in analysis["functions"] {
                analysis["functions"][func] = {
                    "file": file_path,
                    "calls": [],
                    "called_by": [],
                    "parameters": [],
                    "docstring": ""
                };
            }
        }

        for cls in classes {
            if cls not in analysis["classes"] {
                analysis["classes"][cls] = {
                    "file": file_path,
                    "methods": [],
                    "inherits_from": [],
                    "docstring": ""
                };
            }
        }

        # Store dependencies for Jac files
        analysis["dependencies"][file_path] = {
            "imports": imports,
            "functions": functions,
            "classes": classes
        };
    }

    can _build_call_graph with analysis: Dict[str, Any] {
        # Build function call relationships
        for func_name, func_info in analysis["functions"].items() {
            analysis["call_graph"][func_name] = {
                "calls": func_info["calls"],
                "called_by": func_info["called_by"]
            };
        }
    }

    can _build_inheritance_graph with analysis: Dict[str, Any] {
        # Build class inheritance relationships
        for cls_name, cls_info in analysis["classes"].items() {
            analysis["inheritance_graph"][cls_name] = {
                "inherits_from": cls_info["inherits_from"],
                "methods": cls_info["methods"]
            };
        }
    }
}

# Documentation Generator agent
walker DocGenie {
    can generate_documentation with repo: Repo, analysis: Dict[str, Any], file_tree: Dict[str, Any], readme_summary: str -> str {
        documentation = f"""# {repo.name} - Codebase Documentation

## Overview

{readme_summary}

## Project Structure

```
{self._format_file_tree(file_tree)}
```

## Code Analysis

### Functions ({len(analysis["functions"])} total)

{self._generate_function_docs(analysis["functions"])}

### Classes ({len(analysis["classes"])} total)

{self._generate_class_docs(analysis["classes"])}

### Dependencies

{self._generate_dependency_docs(analysis["dependencies"])}

### Function Call Graph

{self._generate_call_graph_docs(analysis["call_graph"])}

### Class Inheritance

{self._generate_inheritance_docs(analysis["inheritance_graph"])}

## Installation

```bash
# Installation instructions would go here
# Based on README analysis or standard practices
```

## Usage

```python
# Usage examples would go here
# Generated from code analysis
```

## API Reference

{self._generate_api_reference(analysis)}

---
*Generated by Codebase Genius on {self._get_timestamp()}*
""";

        return documentation;
    }

    can _format_file_tree with tree: Dict[str, Any], prefix: str = "" -> str {
        result = "";

        if tree["type"] == "directory" {
            result += f"{prefix}{tree['name']}/\n";
            for child in tree.get("children", []) {
                result += self._format_file_tree(child, prefix + "  ");
            }
        } else {
            result += f"{prefix}{tree['name']} ({tree.get('size', 0)} bytes)\n";

        return result;
    }

    can _generate_function_docs with functions: Dict[str, Any] -> str {
        if not functions:
            return "No functions found.\n";

        result = "";
        for name, info in functions.items() {
            result += f"#### `{name}`\n\n";
            result += f"**File:** `{info['file']}`\n\n";
            if info["docstring"] {
                result += f"**Description:** {info['docstring']}\n\n";
            }
            if info["calls"] {
                result += f"**Calls:** {', '.join(f'`{c}`' for c in info['calls'])}\n\n";
            }
            result += "\n";
        }
        return result;
    }

    can _generate_class_docs with classes: Dict[str, Any] -> str {
        if not classes:
            return "No classes found.\n";

        result = "";
        for name, info in classes.items() {
            result += f"#### `{name}`\n\n";
            result += f"**File:** `{info['file']}`\n\n";
            if info["inherits_from"] {
                result += f"**Inherits from:** {', '.join(f'`{c}`' for c in info['inherits_from'])}\n\n";
            }
            if info["methods"] {
                result += f"**Methods:** {', '.join(f'`{m}`' for m in info['methods'])}\n\n";
            }
            result += "\n";
        }
        return result;
    }

    can _generate_dependency_docs with dependencies: Dict[str, Any] -> str {
        if not dependencies:
            return "No dependencies found.\n";

        result = "";
        for file_path, deps in dependencies.items() {
            result += f"**{file_path}:**\n";
            if deps["imports"] {
                result += f"- Imports: {', '.join(deps['imports'])}\n";
            }
            result += "\n";
        }
        return result;
    }

    can _generate_call_graph_docs with call_graph: Dict[str, Any] -> str {
        # Use utility function for better diagram generation
        functions = {};
        for func_name, info in call_graph.items() {
            functions[func_name] = info;
        }
        return utils.MermaidGenerator.generate_call_graph(functions);
    }

    can _generate_inheritance_docs with inheritance_graph: Dict[str, Any] -> str {
        # Use utility function for better diagram generation
        classes = {};
        for cls_name, info in inheritance_graph.items() {
            classes[cls_name] = info;
        }
        return utils.MermaidGenerator.generate_inheritance_graph(classes);
    }

    can _generate_api_reference with analysis: Dict[str, Any] -> str {
        result = "";
        for func_name, info in analysis["functions"].items() {
            result += f"### `{func_name}()`\n\n";
            result += f"Defined in: `{info['file']}`\n\n";
            if info["docstring"] {
                result += f"{info['docstring']}\n\n";
            }
        }
        return result;
    }

    can _get_timestamp -> str {
        from datetime import datetime;
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S");
    }
}

# API endpoints
walker api {
    can generate_docs with repo_url: str -> str {
        return CodeGenius().process_repo(repo_url);
    }

    can get_status -> str {
        return "Codebase Genius API is running";
    }

    can list_outputs -> str {
        import glob;
        outputs = glob.glob("./outputs/*");
        if not outputs:
            return "No documentation outputs found";

        result = "Available documentation:\n";
        for output in outputs {
            result += f"- {output}\n";
        return result;
    }
}
