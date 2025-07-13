# Smart Contract Audit MCP Server API Documentation

## Overview

The Smart Contract Audit MCP Server provides 9 powerful tools for comprehensive smart contract security analysis through the Model Context Protocol (MCP).

## Available Tools

### 1. `make_audit`
Complete audit workflow orchestration.

**Parameters:**
- `project_path` (string): Path to smart contract project
- `include_etherscan` (bool): Whether to fetch from Etherscan first
- `contract_address` (string): Contract address for Etherscan
- `network` (string): Network for Etherscan fetch

**Returns:**
- Complete audit results with all analysis steps
- JSON report with findings and recommendations

### 2. `fetch_contract_from_etherscan`
Download verified contracts from blockchain explorers.

**Parameters:**
- `address` (string): Contract address (0x...)
- `network` (string): Network name (mainnet, arbitrum, base, etc.)

**Returns:**
- Contract source code and metadata
- Multi-file contract reconstruction

### 3. `generate_detailed_index_for_audit`
Create AI-powered project index with token counts.

**Parameters:**
- `project_path` (string): Path to the smart contract project
- `exclude_libs` (bool): Whether to exclude lib folders (default: True)

**Returns:**
- Detailed markdown index with AI summaries
- Token count for context management

### 4. `run_slither_analysis`
Static analysis with Slither's 70+ detectors.

**Parameters:**
- `project_path` (string): Path to the smart contract project
- `output_format` (string): Output format (json, text, sarif)

**Returns:**
- Comprehensive vulnerability findings
- Structured JSON output for AI processing

### 5. `run_foundry_tests_and_fuzz`
Foundry testing and fuzzing.

**Parameters:**
- `project_path` (string): Path to the Foundry project
- `fuzz_runs` (int): Number of fuzz runs (default: 256)

**Returns:**
- Test results and coverage analysis
- Fuzzing findings with gas reports

### 6. `read_multiple_files`
Read multiple contract files in parallel.

**Parameters:**
- `file_paths` (list): List of file paths to read
- `base_path` (string): Base directory path (optional)

**Returns:**
- File contents with metadata
- Token counts for context management

### 7. `generate_dependency_graph`
Map contract dependencies and inheritance.

**Parameters:**
- `project_path` (string): Path to the smart contract project

**Returns:**
- Dependency graph with nodes and edges
- Circular dependency detection

### 8. `get_audit_prompt`
Get specialized audit prompt templates.

**Parameters:**
- `prompt_type` (string): Type of prompt (bootstrap, vulnerability_scan, etc.)
- `**kwargs`: Variables to substitute in the prompt

**Returns:**
- Formatted audit prompt for systematic analysis

### 9. `get_poc_tutorial`
Get tutorial for exploit development.

**Parameters:**
- None

**Returns:**
- Comprehensive POC development guide
- Anvil setup and Foundry exploit templates

## Usage Examples

```python
# Complete audit workflow
result = make_audit("./contracts", include_etherscan=True, 
                   contract_address="0x...", network="mainnet")

# Fetch specific contract
contract = fetch_contract_from_etherscan("0x...", "arbitrum")

# Generate project index
index = generate_detailed_index_for_audit("./project")

# Run security analysis
findings = run_slither_analysis("./project")
```

## Error Handling

All tools return standardized error responses:
```json
{
  "error": "Description of the error",
  "details": "Additional context if available"
}
```

## Integration

The MCP server integrates with any MCP-compatible client:
- Cursor IDE
- Claude Desktop
- Custom MCP clients

Configuration example for Cursor:
```json
{
  "mcpServers": {
    "audit_mcp": {
      "command": "python",
      "args": ["audit_mcp_server.py"],
      "env": {
        "OPENAI_API_KEY": "your_key",
        "ETHERSCAN_API_KEY": "your_key"
      }
    }
  }
}
``` 