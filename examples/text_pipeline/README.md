# Text Pipeline Example

This example demonstrates the core features of the Pudding pipeline framework using a simple text processing pipeline.

## Overview

The pipeline consists of three components:
1. **TextLoader** - Loads and validates text input
2. **TextCleaner** - Normalizes text (removes extra spaces, converts to lowercase, removes special characters)
3. **WordCounter** - Generates word statistics from cleaned text

## Features Demonstrated

### 1. Universal Input Handling
The framework's `run()` method accepts multiple input types:
- Direct data (dictionaries, Pydantic models)
- Component results (for chaining)
- Other components (automatically uses their latest output)
- File paths (loads saved samples)
- No arguments (replay mode)

### 2. Self-Describing Data
Every piece of data is wrapped in a `DataEnvelope` containing:
- Processing lineage (which components processed it)
- Schema information and validation
- Execution context and timestamps
- Component metadata

### 3. Configuration Options
- **Debug mode**: Saves all inputs/outputs for inspection
- **Production mode**: No saving, includes execution IDs
- **Testing mode**: Selective saving for test scenarios

### 4. Component Registry
- Automatic component registration
- Connection compatibility checking
- Schema validation between components

## Running the Example

```bash
cd examples/text_pipeline
python demo.py
```

## What Happens

The demo runs through 6 different scenarios:

1. **Basic Pipeline** - Shows standard pipeline execution with debug output
2. **Replay Mode** - Demonstrates running without arguments to replay saved data
3. **Chaining Methods** - Shows different ways to connect components
4. **Error Handling** - Demonstrates graceful error handling
5. **Registry** - Shows component discovery and compatibility checking
6. **Configurations** - Demonstrates different execution modes

## Sample Files

After running, check the `sample_data/` directory:
```bash
ls sample_data/*/
```

You'll find JSON files containing:
- Input data envelopes
- Output data envelopes
- Complete execution metadata
- Processing lineage

## Example Output

```bash
╰─ python demo.py                                                                                                  ─╯

============================================================
🍮 PUDDING PIPELINE FRAMEWORK DEMO
============================================================

============================================================
DEMO 1: Basic Pipeline Execution
============================================================
2025-06-08 14:45:15,638 - pudding.core.base_component - INFO - Initialized text_loader v1.0.0
2025-06-08 14:45:15,638 - pudding.core.registry - INFO - Registered component: text_loader v1.0.0
2025-06-08 14:45:15,638 - pudding.core.base_component - INFO - Initialized text_cleaner v1.0.0
2025-06-08 14:45:15,638 - pudding.core.registry - INFO - Registered component: text_cleaner v1.0.0
2025-06-08 14:45:15,638 - pudding.core.base_component - INFO - Initialized word_counter v1.0.0
2025-06-08 14:45:15,638 - pudding.core.registry - INFO - Registered component: word_counter v1.0.0

1. Running full pipeline with debug mode:
2025-06-08 14:45:15,639 - pudding.core.base_component - INFO - 
2025-06-08 14:45:15,639 - pudding.core.base_component - INFO - 💾 text_loader: Saved component_input to /Users/kasimtasdemir/Documents/projects/pipeline/20250607_pudding/examples/text_pipeline/sample_data/text_loader/input_20250608_144515_639.json
2025-06-08 14:45:15,639 - pudding.core.base_component - INFO - 💾 text_loader: Saved component_output to /Users/kasimtasdemir/Documents/projects/pipeline/20250607_pudding/examples/text_pipeline/sample_data/text_loader/output_20250608_144515_639.json
2025-06-08 14:45:15,639 - pudding.core.base_component - INFO - ✅ text_loader: Completed successfully
   Loader: Success=True
2025-06-08 14:45:15,639 - pudding.core.base_component - INFO - From: text_loader | Schema: TextInput
2025-06-08 14:45:15,640 - pudding.core.base_component - INFO - 💾 text_cleaner: Saved component_input to /Users/kasimtasdemir/Documents/projects/pipeline/20250607_pudding/examples/text_pipeline/sample_data/text_cleaner/input_20250608_144515_639.json
2025-06-08 14:45:15,640 - pudding.core.base_component - INFO - 💾 text_cleaner: Saved component_output to /Users/kasimtasdemir/Documents/projects/pipeline/20250607_pudding/examples/text_pipeline/sample_data/text_cleaner/output_20250608_144515_640.json
2025-06-08 14:45:15,640 - pudding.core.base_component - INFO - ✅ text_cleaner: Completed successfully
   Cleaner: Success=True
   Changes made: ['removed_extra_whitespace', 'converted_to_lowercase', 'removed_special_characters']
2025-06-08 14:45:15,640 - pudding.core.base_component - INFO - From: text_cleaner | Schema: CleanedText
2025-06-08 14:45:15,640 - pudding.core.base_component - INFO - 💾 word_counter: Saved component_input to /Users/kasimtasdemir/Documents/projects/pipeline/20250607_pudding/examples/text_pipeline/sample_data/word_counter/input_20250608_144515_640.json
2025-06-08 14:45:15,641 - pudding.core.base_component - INFO - 💾 word_counter: Saved component_output to /Users/kasimtasdemir/Documents/projects/pipeline/20250607_pudding/examples/text_pipeline/sample_data/word_counter/output_20250608_144515_640.json
2025-06-08 14:45:15,641 - pudding.core.base_component - INFO - ✅ word_counter: Completed successfully
   Counter: Success=True
   Stats: 40 words, 35 unique
   Most common: [('and', 3), ('test', 2), ('it', 2), ('quotes', 2), ('hello', 1)]

============================================================
DEMO 2: Replay Mode
============================================================
2025-06-08 14:45:15,641 - pudding.core.base_component - INFO - Initialized text_cleaner v1.0.0
2025-06-08 14:45:15,641 - pudding.core.registry - INFO - Registered component: text_cleaner v1.0.0

1. Replaying last cleaner execution:
2025-06-08 14:45:15,641 - pudding.core.base_component - INFO - 🔄 REPLAY MODE: Using latest saved input for text_cleaner
   Success! Replayed from saved input
   Is replay: True
   Text preview: hello world this is a test of the pudding pipeline...

============================================================
DEMO 3: Component Chaining Methods
============================================================
2025-06-08 14:45:15,641 - pudding.core.base_component - INFO - Initialized text_loader v1.0.0
2025-06-08 14:45:15,641 - pudding.core.registry - INFO - Registered component: text_loader v1.0.0
2025-06-08 14:45:15,641 - pudding.core.base_component - INFO - Initialized text_cleaner v1.0.0
2025-06-08 14:45:15,641 - pudding.core.registry - INFO - Registered component: text_cleaner v1.0.0
2025-06-08 14:45:15,641 - pudding.core.base_component - INFO - Initialized word_counter v1.0.0
2025-06-08 14:45:15,641 - pudding.core.registry - INFO - Registered component: word_counter v1.0.0

1. Method A: Pass ComponentResult directly
2025-06-08 14:45:15,641 - pudding.core.base_component - INFO - 💾 text_loader: Saved component_output to /Users/kasimtasdemir/Documents/projects/pipeline/20250607_pudding/examples/text_pipeline/sample_data/text_loader/output_20250608_144515_641.json
   Success: True

2. Method B: Pass component itself (uses latest output)
2025-06-08 14:45:15,641 - pudding.core.base_component - INFO - Loading latest output from text_cleaner
   Success: True

3. Method C: Load specific sample file
   Success: True
   Loaded from: output_20250608_143614.json

============================================================
DEMO 4: Error Handling
============================================================
2025-06-08 14:45:15,642 - pudding.core.base_component - INFO - Initialized text_cleaner v1.0.0
2025-06-08 14:45:15,642 - pudding.core.registry - INFO - Registered component: text_cleaner v1.0.0

1. Invalid input data:
2025-06-08 14:45:15,642 - pudding.core.base_component - ERROR - Component text_cleaner failed: 1 validation error for TextInput
text
  Field required [type=missing, input_value={'wrong_field': "This won't work"}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.11/v/missing
   Error handled: True
   Error message: Component text_cleaner failed: 1 validation error for TextInput
text
  Field required [type=missing, input_value={'wrong_field': "This won't work"}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.11/v/missing

2. Component works after error:
   Success: True

============================================================
DEMO 5: Component Registry
============================================================

1. Registered components:
   - text_loader
   - text_cleaner
   - word_counter

2. Checking connections:
   text_loader → text_cleaner: True
   text_cleaner → word_counter: True
   text_loader → word_counter: False
   Reason: Schema mismatch: text_loader outputs TextInput, word_counter expects CleanedText

============================================================
DEMO 6: Configuration Options
============================================================
2025-06-08 14:45:15,642 - pudding.core.base_component - INFO - Initialized text_loader v1.0.0
2025-06-08 14:45:15,642 - pudding.core.registry - INFO - Registered component: text_loader v1.0.0

1. Debug mode (saves everything):
2025-06-08 14:45:15,642 - pudding.core.base_component - INFO - 
2025-06-08 14:45:15,642 - pudding.core.base_component - INFO - 💾 text_loader: Saved component_input to /Users/kasimtasdemir/Documents/projects/pipeline/20250607_pudding/examples/text_pipeline/sample_data/text_loader/input_20250608_144515_642.json
2025-06-08 14:45:15,643 - pudding.core.base_component - INFO - 💾 text_loader: Saved component_output to /Users/kasimtasdemir/Documents/projects/pipeline/20250607_pudding/examples/text_pipeline/sample_data/text_loader/output_20250608_144515_642.json
2025-06-08 14:45:15,643 - pudding.core.base_component - INFO - ✅ text_loader: Completed successfully
   Samples saved: 7

2. Production mode (no saving):
   Execution ID: prod_001

3. Testing mode (output only):
2025-06-08 14:45:15,643 - pudding.core.base_component - INFO - 
2025-06-08 14:45:15,643 - pudding.core.base_component - INFO - 💾 text_loader: Saved component_output to /Users/kasimtasdemir/Documents/projects/pipeline/20250607_pudding/examples/text_pipeline/sample_data/text_loader/output_20250608_144515_643.json
2025-06-08 14:45:15,643 - pudding.core.base_component - INFO - ✅ text_loader: Completed successfully
   Debug mode: True

============================================================
✨ KEY FEATURES DEMONSTRATED:
============================================================
1. Universal run() method handles any input type
2. Replay mode with no arguments
3. Multiple chaining methods
4. Graceful error handling
5. Component registry for discovery
6. Flexible configuration system
============================================================
```

## Key Takeaways

1. **Debugging is Easy**: Every execution can be replayed and inspected
2. **Type Safety**: Pydantic validation ensures data integrity
3. **Flexible Chaining**: Multiple ways to connect components
4. **Production Ready**: Same code works locally and in production
5. **Unicode Support**: Handles international text and special characters correctly

## Next Steps

Try modifying the example:
1. Add a new component (e.g., `SentimentAnalyzer`)
2. Change the text processing logic
3. Create a branching pipeline
4. Add custom configuration options

## Code Structure

```
text_pipeline/
├── components.py    # Component implementations
├── demo.py         # Demonstration script
├── README.md       # This file
└── sample_data/    # Created after first run
    ├── text_loader/
    ├── text_cleaner/
    └── word_counter/
```

## Understanding the Code

### Component Definition
```python
class TextCleaner(BaseComponent[TextInput, CleanedText]):
    def __init__(self):
        super().__init__(
            name="text_cleaner",
            version="1.0.0",
            input_schema=TextInput,
            output_schema=CleanedText
        )
    
    async def process(self, input_data: TextInput) -> CleanedText:
        # Your processing logic here
        return CleanedText(...)
```

### Running Components
```python
# Debug mode - saves everything
result = await component.run(data, config=RunConfig.debug())

# Chain components
result1 = await component1.run(data)
result2 = await component2.run(result1)  # Pass result directly

# Replay last execution
result = await component.run()  # No arguments!
```

## Benefits

- **Fast Development**: Create components in minutes
- **Easy Debugging**: Inspect any execution with saved samples
- **Type Safe**: Catch errors early with Pydantic
- **Flexible**: Works standalone or in complex pipelines
- **Traceable**: Complete lineage for every piece of data
