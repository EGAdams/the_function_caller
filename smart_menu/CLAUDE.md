# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Python-based smart menu system that provides terminal-based command execution with JSON configuration. The system uses a modular object-oriented design with dynamic menu loading and command execution capabilities.

## Development Commands

### Running the Application
```bash
# Run with default config.json
python3 test_smart_menu_system.py

# Run with specific configuration file
python3 test_smart_menu_system.py path/to/config.json

# Run with specific menu configurations
python3 test_smart_menu_system.py linux_bash_config.json
python3 test_smart_menu_system.py project_menu.json
python3 test_smart_menu_system.py agent_config.json
```

### Dependencies
```bash
# Install required Python dialog library
pip install pythondialog
```

### Testing
```bash
# Run the test system
python3 test_smart_menu_system.py
```

## Architecture Overview

### Core Components

**Menu System Architecture**:
- `Menu` - Container for menu items with display and selection logic
- `MenuItem` - Individual executable commands with execution options
- `SmartMenuItem` - Enhanced menu items that can contain sub-menus
- `MenuManager` - Handles menu loading, saving, and dynamic item addition
- `CommandExecutor` - Executes commands with directory/subprocess control
- `ConfigReader` - JSON configuration file parsing with error handling

**Two UI Implementations**:
- `CommandMenuApp` - npyscreen-based TUI (currently commented out)
- `Menu.display_and_select()` - Simple text-based menu interface

### Key Design Patterns

**Command Pattern**: MenuItem encapsulates command execution with configurable options:
- `working_directory` - Directory context for command execution
- `open_in_subprocess` - Whether to run in separate process
- `use_expect_library` - Integration with expect library for interactive commands

**Configuration-Driven**: JSON files define menu structure and commands, enabling:
- Dynamic menu loading from external configuration
- Runtime menu item addition with persistence
- Multiple menu configurations for different contexts

**Modular Execution**: CommandExecutor provides centralized command handling with:
- Directory context management
- Subprocess vs current process execution
- Error handling and cleanup

### JSON Configuration Structure

Menu configurations follow this format:
```json
[
  {
    "title": "Display name",
    "action": "command to execute",
    "working_directory": "path/to/working/dir",
    "open_in_subprocess": false,
    "use_expect_library": false
  }
]
```

### File Structure

**Core Classes**:
- `Menu.py` - Main menu container and display logic
- `MenuItem.py` - Command execution item
- `SmartMenuItem.py` - Enhanced menu item with sub-menu support
- `MenuManager.py` - Menu lifecycle management
- `CommandExecutor.py` - Command execution abstraction
- `ConfigReader.py` - Configuration file handling

**Entry Points**:
- `test_smart_menu_system.py` - Main CLI entry point
- `CommandMenuApp.py` - Alternative npyscreen-based UI (requires npyscreen)

**Configuration Files**:
- `config.json` - Default menu configuration
- `linux_bash_config.json` - Linux-specific commands
- `project_menu.json` - Project-specific menu items
- `agent_config.json` - Agent system commands

## Development Notes

### Menu Item Execution
Commands are executed through CommandExecutor which handles:
- Working directory changes with automatic restoration
- Subprocess vs direct execution based on configuration
- Error handling and user feedback

### Configuration Management
- JSON configurations are loaded at startup
- New menu items can be added dynamically and persisted
- ConfigReader handles file not found and JSON parsing errors gracefully

### UI Flexibility
The system supports both simple text-based menus and enhanced TUI through npyscreen. The text-based interface is the primary implementation, while the npyscreen version provides a more sophisticated terminal experience.

### Error Handling
- JSON parsing errors are caught and handled gracefully
- Command execution errors are captured and displayed to users
- File not found errors provide helpful feedback

## Common Usage Patterns

1. **Loading Custom Menus**: Pass configuration file as command line argument
2. **Adding Menu Items**: Use the "Add a menu item" option during runtime
3. **Command Execution**: Items execute in specified working directory with subprocess control
4. **Configuration Persistence**: New items are automatically saved to JSON configuration