"""
Utility functions for the Codebase Genius system.
Provides helper functions for file operations, text processing, and more.
"""

import os
import re
import json
from typing import Dict, List, Any, Optional
from pathlib import Path


class FileUtils:
    """Utility class for file operations."""

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Get file extension from path."""
        return Path(file_path).suffix.lower()

    @staticmethod
    def is_text_file(file_path: str) -> bool:
        """Check if file is a text file based on extension."""
        text_extensions = {'.py', '.jac', '.md', '.txt', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.json', '.yaml', '.yml', '.xml', '.html', '.css', '.sh', '.bat', '.ps1'}
        return FileUtils.get_file_extension(file_path) in text_extensions

    @staticmethod
    def read_file_content(file_path: str, max_size: int = 10 * 1024 * 1024) -> Optional[str]:
        """Read file content with size limit."""
        try:
            if not os.path.exists(file_path):
                return None

            file_size = os.path.getsize(file_path)
            if file_size > max_size:
                print(f"Warning: File {file_path} is too large ({file_size} bytes), skipping")
                return None

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None

    @staticmethod
    def get_directory_size(dir_path: str) -> int:
        """Get total size of directory in bytes."""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, IOError):
                    pass
        return total_size


class TextProcessor:
    """Utility class for text processing and analysis."""

    @staticmethod
    def extract_functions_python(content: str) -> List[Dict[str, Any]]:
        """Extract function definitions from Python code."""
        functions = []

        # Match function definitions
        func_pattern = r'def\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*[^:]+)?\s*:'
        matches = re.finditer(func_pattern, content, re.MULTILINE)

        for match in matches:
            func_name = match.group(1)
            params_str = match.group(2)

            # Parse parameters
            parameters = []
            if params_str.strip():
                # Simple parameter parsing (can be enhanced)
                params = [p.strip() for p in params_str.split(',')]
                for param in params:
                    if param and not param.startswith('*'):
                        param_name = param.split(':')[0].split('=')[0].strip()
                        parameters.append(param_name)

            # Extract docstring
            docstring = TextProcessor._extract_docstring_after_match(content, match.end())

            functions.append({
                'name': func_name,
                'parameters': parameters,
                'docstring': docstring,
                'line_start': content[:match.start()].count('\n') + 1
            })

        return functions

    @staticmethod
    def extract_classes_python(content: str) -> List[Dict[str, Any]]:
        """Extract class definitions from Python code."""
        classes = []

        # Match class definitions
        class_pattern = r'class\s+(\w+)(?:\(([^)]+)\))?\s*:'
        matches = re.finditer(class_pattern, content, re.MULTILINE)

        for match in matches:
            class_name = match.group(1)
            inherits_str = match.group(2) if match.group(2) else ""

            # Parse inheritance
            inherits_from = []
            if inherits_str.strip():
                inherits_from = [cls.strip() for cls in inherits_str.split(',')]

            # Extract docstring
            docstring = TextProcessor._extract_docstring_after_match(content, match.end())

            classes.append({
                'name': class_name,
                'inherits_from': inherits_from,
                'docstring': docstring,
                'line_start': content[:match.start()].count('\n') + 1
            })

        return classes

    @staticmethod
    def extract_imports_python(content: str) -> List[str]:
        """Extract import statements from Python code."""
        imports = []

        # Match different import patterns
        patterns = [
            r'^import\s+([^\n]+)',  # import statements
            r'^from\s+([^\n]+)'     # from statements
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            imports.extend(matches)

        return imports

    @staticmethod
    def _extract_docstring_after_match(content: str, position: int) -> str:
        """Extract docstring starting after a given position."""
        # Look for triple quotes after the match
        docstring_pattern = r'""".*?"""'
        matches = re.findall(docstring_pattern, content[position:position+1000], re.DOTALL)

        if matches:
            return matches[0].strip('"""').strip()

        return ""

    @staticmethod
    def calculate_cyclomatic_complexity(content: str) -> int:
        """Calculate cyclomatic complexity of code (basic implementation)."""
        # Count decision points
        complexity = 1  # Base complexity

        # Count if, elif, else, for, while, with, try, except, finally
        decision_keywords = ['if ', 'elif ', 'for ', 'while ', 'with ', 'try:', 'except', 'finally:']
        for keyword in decision_keywords:
            complexity += len(re.findall(keyword, content))

        # Count logical operators
        logical_ops = [' and ', ' or ', ' not ']
        for op in logical_ops:
            complexity += len(re.findall(op, content))

        return complexity


class CodeMetrics:
    """Class for calculating code metrics and statistics."""

    @staticmethod
    def calculate_file_metrics(file_path: str) -> Dict[str, Any]:
        """Calculate metrics for a single file."""
        content = FileUtils.read_file_content(file_path)
        if not content:
            return {}

        lines = content.split('\n')
        total_lines = len(lines)
        code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        comment_lines = len([line for line in lines if line.strip().startswith('#')])
        blank_lines = len([line for line in lines if not line.strip()])

        return {
            'total_lines': total_lines,
            'code_lines': code_lines,
            'comment_lines': comment_lines,
            'blank_lines': blank_lines,
            'comment_ratio': comment_lines / total_lines if total_lines > 0 else 0,
            'file_size': os.path.getsize(file_path)
        }

    @staticmethod
    def calculate_project_metrics(project_path: str) -> Dict[str, Any]:
        """Calculate metrics for entire project."""
        metrics = {
            'total_files': 0,
            'total_lines': 0,
            'total_size': 0,
            'files_by_type': {},
            'language_complexity': {}
        }

        for root, dirs, files in os.walk(project_path):
            # Skip common directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.git']]

            for file in files:
                file_path = os.path.join(root, file)

                if FileUtils.is_text_file(file_path):
                    file_metrics = CodeMetrics.calculate_file_metrics(file_path)

                    metrics['total_files'] += 1
                    metrics['total_lines'] += file_metrics['total_lines']
                    metrics['total_size'] += file_metrics['file_size']

                    # Track by file type
                    ext = FileUtils.get_file_extension(file_path)
                    if ext not in metrics['files_by_type']:
                        metrics['files_by_type'][ext] = []
                    metrics['files_by_type'][ext].append(file_metrics)

        return metrics


class MermaidGenerator:
    """Generate Mermaid diagrams for code visualization."""

    @staticmethod
    def generate_call_graph(functions: Dict[str, Any]) -> str:
        """Generate Mermaid diagram for function call graph."""
        if not functions:
            return "graph TD\n    A[No functions found]"

        diagram = "graph TD\n"

        for func_name, func_info in functions.items():
            # Add function node
            diagram += f'    {func_name}["{func_name}()"]\n'

            # Add calls
            for called_func in func_info.get('calls', []):
                diagram += f'    {func_name} --> {called_func}\n'

        return diagram

    @staticmethod
    def generate_inheritance_graph(classes: Dict[str, Any]) -> str:
        """Generate Mermaid diagram for class inheritance."""
        if not classes:
            return "graph TD\n    A[No classes found]"

        diagram = "graph TD\n"

        for class_name, class_info in classes.items():
            # Add class node
            diagram += f'    {class_name}["{class_name}"]\n'

            # Add inheritance relationships
            for parent_class in class_info.get('inherits_from', []):
                diagram += f'    {parent_class} --> {class_name}\n'

        return diagram

    @staticmethod
    def generate_file_structure_tree(file_tree: Dict[str, Any]) -> str:
        """Generate Mermaid diagram for file structure."""
        if not file_tree:
            return "graph TD\n    A[Empty repository]"

        diagram = "graph TD\n"

        def add_node(node: Dict[str, Any], parent: str = None):
            node_id = node['name'].replace('.', '_').replace('-', '_')

            if node['type'] == 'directory':
                diagram = f'    {node_id}["📁 {node["name"]}"]\n'
                if parent:
                    diagram += f'    {parent} --> {node_id}\n'

                for child in node.get('children', []):
                    add_node(child, node_id)
            else:
                diagram = f'    {node_id}["📄 {node["name"]}"]\n'
                if parent:
                    diagram += f'    {parent} --> {node_id}\n'

        add_node(file_tree)
        return diagram


class ValidationUtils:
    """Utility class for validation operations."""

    @staticmethod
    def validate_github_url(url: str) -> bool:
        """Validate if URL is a valid GitHub repository URL."""
        if not url:
            return False

        # Basic URL validation
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)

            if parsed.scheme not in ['http', 'https']:
                return False

            if 'github.com' not in parsed.netloc:
                return False

            # Check if it's a repository path (user/repo format)
            path_parts = parsed.path.strip('/').split('/')
            if len(path_parts) < 2:
                return False

            # Check for common issues
            if path_parts[-1] in ['issues', 'pulls', 'wiki', 'settings']:
                return False

            return True

        except Exception:
            return False

    @staticmethod
    def validate_file_size(file_path: str, max_size: int = 10 * 1024 * 1024) -> bool:
        """Validate if file size is within limits."""
        try:
            return os.path.getsize(file_path) <= max_size
        except (OSError, IOError):
            return False

    @staticmethod
    def validate_language_support(file_path: str) -> bool:
        """Check if file language is supported."""
        supported_extensions = {
            '.py', '.jac', '.js', '.ts', '.java', '.cpp', '.c', '.h',
            '.md', '.txt', '.json', '.yaml', '.yml', '.xml', '.html', '.css'
        }

        return FileUtils.get_file_extension(file_path) in supported_extensions
