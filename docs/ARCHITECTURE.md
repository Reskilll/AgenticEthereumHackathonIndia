# Smart Contract Audit MCP Server Architecture

## System Overview

The Smart Contract Audit MCP Server is built on the Model Context Protocol (MCP) framework, providing a standardized interface for AI agents to perform comprehensive smart contract security audits.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Agent (Cursor/Claude)                     │
│              ┌─────────────────────────────────────┐            │
│              │        Natural Language Input       │            │
│              │     "Audit this contract..."        │            │
│              └─────────────────────────────────────┘            │
└─────────────────────────┬───────────────────────────────────────┘
                          │ MCP Protocol
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MCP Server (FastMCP)                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Tool Router   │  │  Context Manager│  │ Response Handler│ │
│  │                 │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Audit Engine                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │Contract Fetcher │  │  Index Generator│  │ Analysis Engine │ │
│  │                 │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Slither Runner │  │  Foundry Runner │  │  POC Generator  │ │
│  │                 │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                 External Services                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Etherscan API  │  │    OpenAI API   │  │  Slither Tool   │ │
│  │                 │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Foundry Suite  │  │   Anvil Fork    │  │  Token Counter  │ │
│  │                 │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. MCP Server Layer
- **FastMCP Framework**: Handles MCP protocol communication
- **Tool Router**: Dispatches requests to appropriate audit functions
- **Context Manager**: Manages token limits and conversation context
- **Response Handler**: Formats responses for AI agent consumption

### 2. Audit Engine
- **Contract Fetcher**: Downloads verified contracts from blockchain explorers
- **Index Generator**: Creates AI-powered project summaries
- **Analysis Engine**: Coordinates multi-tool security analysis
- **Slither Runner**: Executes static analysis with 70+ detectors
- **Foundry Runner**: Performs dynamic testing and fuzzing
- **POC Generator**: Creates exploit demonstrations

### 3. External Services
- **Blockchain APIs**: Etherscan, Arbiscan, Basescan for contract fetching
- **AI Services**: OpenAI GPT-4 for intelligent analysis
- **Security Tools**: Slither, Foundry, Anvil for comprehensive testing
- **Utilities**: Token counting, file management, dependency analysis

## Data Flow

### 1. Contract Fetching Flow
```
User Request → MCP Server → Etherscan API → Contract Download → 
File Reconstruction → Metadata Extraction → Cache Storage
```

### 2. Index Generation Flow
```
Project Path → File Discovery → Content Analysis → AI Summarization → 
Token Counting → Markdown Generation → Context Optimization
```

### 3. Static Analysis Flow
```
Contract Files → Slither Execution → Detector Results → 
JSON Parsing → Severity Classification → Finding Aggregation
```

### 4. Dynamic Testing Flow
```
Foundry Project → Test Discovery → Fuzz Configuration → 
Test Execution → Coverage Analysis → Result Compilation
```

### 5. POC Generation Flow
```
Vulnerability Discovery → Exploit Template → Anvil Setup → 
Test Generation → Exploitation Steps → Validation
```

## Security Considerations

### 1. Input Validation
- Sanitize all user inputs and file paths
- Validate contract addresses and network parameters
- Prevent path traversal attacks

### 2. API Key Management
- Store API keys in environment variables
- Implement rate limiting for external APIs
- Use secure communication protocols

### 3. Code Execution Safety
- Sandbox all external tool execution
- Implement timeouts for long-running operations
- Validate all generated code before execution

### 4. Data Privacy
- No sensitive data logging
- Temporary file cleanup
- Secure cache management

## Performance Optimization

### 1. Parallel Processing
- Concurrent file reading with asyncio
- Parallel contract analysis
- Background task execution

### 2. Caching Strategy
- Contract source code caching
- Analysis result caching
- Intelligent cache invalidation

### 3. Memory Management
- Token counting for context limits
- Streaming large file processing
- Garbage collection for temporary data

### 4. Resource Limits
- Configurable timeout values
- Memory usage monitoring
- Process isolation

## Extensibility

### 1. Plugin Architecture
- Modular tool integration
- Custom detector development
- Prompt template system

### 2. API Extensibility
- New blockchain network support
- Additional security tools
- Custom analysis workflows

### 3. Configuration Management
- Environment-based settings
- Runtime parameter adjustment
- Feature toggles

## Error Handling

### 1. Graceful Degradation
- Fallback mechanisms for failed tools
- Partial result handling
- User-friendly error messages

### 2. Logging and Monitoring
- Structured logging with levels
- Performance metrics collection
- Error tracking and alerting

### 3. Recovery Mechanisms
- Automatic retry logic
- State persistence
- Transaction rollback

## Technology Stack

### Core Technologies
- **Python 3.11+**: Core runtime environment
- **FastMCP**: MCP protocol implementation
- **OpenAI API**: AI-powered analysis
- **Asyncio**: Asynchronous processing

### Security Tools
- **Slither**: Static analysis framework
- **Foundry**: Smart contract testing suite
- **Anvil**: Local blockchain simulation
- **Tiktoken**: Token counting utilities

### Infrastructure
- **HTTPX**: HTTP client for API calls
- **Python-dotenv**: Environment management
- **Pathlib**: File system operations
- **JSON**: Data serialization

## Deployment Considerations

### 1. Environment Setup
- Python virtual environment isolation
- Dependency management with requirements.txt
- Environment variable configuration

### 2. Tool Dependencies
- Foundry installation and setup
- Slither installation and configuration
- Node.js for additional tools

### 3. Performance Tuning
- Worker process configuration
- Memory allocation limits
- Network timeout settings

This architecture provides a robust, scalable, and extensible foundation for AI-powered smart contract security auditing through the Model Context Protocol. 