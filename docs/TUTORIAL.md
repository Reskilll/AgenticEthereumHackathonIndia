# Smart Contract Audit MCP Server Tutorial

## Quick Start Guide

This tutorial demonstrates how to use the Smart Contract Audit MCP Server to perform comprehensive security audits on smart contracts using AI-powered analysis.

## Prerequisites

1. **Python 3.11+**
2. **Foundry** - Install with `foundryup`
3. **Slither** - Install with `pip install slither-analyzer`
4. **OpenAI API Key** - For AI analysis
5. **Etherscan API Key** - For contract fetching

## Installation

```bash
# 1. Clone the repository
git clone git@github.com:gabinfay/AgenticEthereumHackathonIndia.git
cd AgenticEthereumHackathonIndia

# 2. Install dependencies
cd backend
pip install -r requirements.txt

# 3. Install required tools
foundryup
pip install slither-analyzer

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys
```

## MCP Integration with Cursor

Add to your Cursor MCP config (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "audit_mcp": {
      "command": "/path/to/AgenticEthereumHackathonIndia/backend/.venv/bin/python",
      "args": [
        "/path/to/AgenticEthereumHackathonIndia/backend/audit_mcp_server.py"
      ],
      "env": {
        "OPENAI_API_KEY": "your_openai_key",
        "ETHERSCAN_API_KEY": "your_etherscan_key"
      }
    }
  }
}
```

## Tutorial: Auditing the Noya Protocol

This tutorial walks through auditing the included `noya-JUL-2025-audit-scope` project.

### Step 1: Start the Audit

**Tell Cursor:**
```
I want to audit the noya-JUL-2025-audit-scope project for critical vulnerabilities. Start by generating a detailed index.
```

**What happens:**
- MCP server calls `generate_detailed_index_for_audit()`
- Creates AI-powered contract summaries
- Excludes library code for focused analysis
- Manages token counts for efficient context usage

### Step 2: Static Analysis

**Tell Cursor:**
```
Run Slither analysis on the contracts to identify potential vulnerabilities.
```

**What happens:**
- Executes `run_slither_analysis()` with 70+ detectors
- Returns structured JSON findings
- Categorizes vulnerabilities by severity
- Filters out false positives

### Step 3: Deep Code Analysis

**Tell Cursor:**
```
Read the high-priority contracts and analyze them for reentrancy, access control issues, and logic bugs.
```

**What happens:**
- Uses `read_multiple_files()` for parallel processing
- Applies systematic audit prompts
- Focuses on critical security patterns
- Provides detailed vulnerability analysis

### Step 4: Dependency Mapping

**Tell Cursor:**
```
Generate a dependency graph to understand contract interactions and potential attack vectors.
```

**What happens:**
- Creates comprehensive dependency mapping
- Identifies external dependencies
- Detects circular dependencies
- Maps inheritance relationships

### Step 5: Dynamic Testing

**Tell Cursor:**
```
Run Foundry tests and fuzz testing to validate the security analysis.
```

**What happens:**
- Executes existing test suites
- Performs property-based fuzzing
- Generates coverage reports
- Validates security assumptions

### Step 6: Proof of Concept

**Tell Cursor:**
```
For any critical vulnerabilities found, help me create a proof-of-concept exploit.
```

**What happens:**
- Provides POC development guidance
- Sets up Anvil fork environment
- Generates exploit templates
- Demonstrates vulnerability impact

## Advanced Usage

### Fetching Live Contracts

```
Fetch the Uniswap V3 Factory contract from Ethereum mainnet and audit it.
```

This will:
1. Download the contract from Etherscan
2. Reconstruct multi-file projects
3. Run complete audit workflow
4. Generate comprehensive findings

### Custom Analysis

```
Run a focused analysis on reentrancy vulnerabilities in the vault contracts.
```

This will:
1. Use specialized audit prompts
2. Focus on specific vulnerability types
3. Provide targeted recommendations
4. Generate relevant test cases

## Expected Outcomes

After completing a full audit, you'll have:

1. **Detailed Index**: AI-powered project overview with contract summaries
2. **Static Analysis**: Slither findings with severity classifications
3. **Code Analysis**: Deep dive into critical contracts
4. **Dependency Map**: Visual representation of contract relationships
5. **Test Results**: Validation of security assumptions
6. **POC Exploits**: Working demonstrations of vulnerabilities
7. **Recommendations**: Actionable security improvements

## Best Practices

1. **Start with indexing** to understand project structure
2. **Use static analysis** for comprehensive coverage
3. **Focus on high-value targets** identified in the index
4. **Validate findings** with dynamic testing
5. **Create POCs** for critical vulnerabilities
6. **Document everything** for future reference

## Troubleshooting

### Common Issues

1. **MCP Server Not Starting**
   - Check API keys in .env file
   - Verify Python path in MCP config
   - Ensure dependencies are installed

2. **Analysis Failures**
   - Confirm Slither installation
   - Check Foundry is available
   - Verify project structure

3. **No Findings**
   - Review exclusion patterns
   - Check contract compilation
   - Validate network connectivity

### Getting Help

- Review the API documentation in `docs/API.md`
- Check the GitHub repository for issues
- Consult the MCP protocol documentation

## Next Steps

1. **Extend the server** with additional security tools
2. **Create custom prompts** for specific vulnerability types
3. **Integrate with CI/CD** for automated security checking
4. **Build a web interface** for easier access
5. **Share findings** with the security community

This tutorial demonstrates how AI-powered security analysis can make professional-grade smart contract auditing accessible to any developer through simple conversational commands. 