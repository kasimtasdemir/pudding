"""Demonstration of the pudding pipeline framework."""

# examples/text_pipeline/demo.py
import asyncio
import logging

from components import TextCleaner, TextLoader, WordCounter

from pudding.core import RunConfig, SampleSaveMode, registry

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def demo_basic_pipeline():
    """Demonstrate basic pipeline usage."""
    print("\n" + "=" * 60)
    print("DEMO 1: Basic Pipeline Execution")
    print("=" * 60)

    # Initialize components
    loader = TextLoader()
    cleaner = TextCleaner()
    counter = WordCounter()

    # Sample text with Unicode characters
    sample_text = """
    Hello World! This is a TEST of the pudding pipeline framework.
    It should handle    extra spaces, MIXED case, and special characters!!!
    Let's see how it works… "with quotes" and 'smart quotes' too!
    Em—dashes, ellipses… and café résumé naïve 你好 🍮
    Unicode test: \u2019 \u201c \u201d \u2014 \u2026
    """

    # Run pipeline with debug mode
    print("\n1. Running full pipeline with debug mode:")

    # Load text
    result1 = await loader.run(
        {"text": sample_text, "source": "demo"}, config=RunConfig.debug()
    )
    print(f"   Loader: Success={result1.error is None}")

    # Clean text
    result2 = await cleaner.run(result1, config=RunConfig.debug())
    print(f"   Cleaner: Success={result2.error is None}")
    print(f"   Changes made: {result2.data.changes_made}")

    # Count words
    result3 = await counter.run(result2, config=RunConfig.debug())
    print(f"   Counter: Success={result3.error is None}")
    print(
        f"   Stats: {result3.data.total_words} words, {result3.data.unique_words} unique"
    )
    print(f"   Most common: {result3.data.most_common_words}")


async def demo_replay_mode():
    """Demonstrate replay functionality."""
    print("\n" + "=" * 60)
    print("DEMO 2: Replay Mode")
    print("=" * 60)

    cleaner = TextCleaner()

    # Run without arguments - uses latest saved input
    print("\n1. Replaying last cleaner execution:")
    result = await cleaner.run()  # No arguments!

    if result.error:
        print(f"   Error: {result.error}")
    else:
        print("   Success! Replayed from saved input")
        print(f"   Is replay: {result.metadata.is_replay}")
        print(f"   Text preview: {result.data.text[:50]}...")


async def demo_chaining_methods():
    """Demonstrate different ways to chain components."""
    print("\n" + "=" * 60)
    print("DEMO 3: Component Chaining Methods")
    print("=" * 60)

    loader = TextLoader()
    cleaner = TextCleaner()
    counter = WordCounter()

    # First, create some data
    text_data = {
        "text": "Different chaining methods work seamlessly!",
        "source": "chain_demo",
    }

    print("\n1. Method A: Pass ComponentResult directly")
    result_a = await loader.run(
        text_data, config=RunConfig(save_samples=SampleSaveMode.OUTPUT)
    )
    result_b = await cleaner.run(result_a)  # Pass the result directly
    print(f"   Success: {result_b.error is None}")

    print("\n2. Method B: Pass component itself (uses latest output)")
    result_c = await counter.run(cleaner)  # Pass the component
    print(f"   Success: {result_c.error is None}")

    print("\n3. Method C: Load specific sample file")
    samples = cleaner.list_samples("output")
    if samples:
        result_d = await counter.run(
            (cleaner, samples[0])
        )  # Pass tuple of (component, filename)
        print(f"   Success: {result_d.error is None}")
        print(f"   Loaded from: {samples[0]}")


async def demo_error_handling():
    """Demonstrate error handling."""
    print("\n" + "=" * 60)
    print("DEMO 4: Error Handling")
    print("=" * 60)

    cleaner = TextCleaner()

    # Try with invalid data
    print("\n1. Invalid input data:")
    result = await cleaner.run({"wrong_field": "This won't work"})
    print(f"   Error handled: {result.error is not None}")
    print(f"   Error message: {result.error}")

    # Component still works after error
    print("\n2. Component works after error:")
    result = await cleaner.run({"text": "This will work", "source": "recovery"})
    print(f"   Success: {result.error is None}")


async def demo_registry():
    """Demonstrate component registry."""
    print("\n" + "=" * 60)
    print("DEMO 5: Component Registry")
    print("=" * 60)

    print("\n1. Registered components:")
    for comp in registry.list_components():
        print(f"   - {comp}")

    print("\n2. Checking connections:")
    can_connect, reason = registry.can_connect("text_loader", "text_cleaner")
    print(f"   text_loader → text_cleaner: {can_connect}")

    can_connect, reason = registry.can_connect("text_cleaner", "word_counter")
    print(f"   text_cleaner → word_counter: {can_connect}")

    can_connect, reason = registry.can_connect("text_loader", "word_counter")
    print(f"   text_loader → word_counter: {can_connect}")
    if not can_connect:
        print(f"   Reason: {reason}")


async def demo_different_configs():
    """Demonstrate different configuration options."""
    print("\n" + "=" * 60)
    print("DEMO 6: Configuration Options")
    print("=" * 60)

    loader = TextLoader()
    text_data = {"text": "Testing different configurations", "source": "config_demo"}

    print("\n1. Debug mode (saves everything):")
    result = await loader.run(text_data, config=RunConfig.debug())
    print(f"   Samples saved: {len(loader.list_samples())}")

    print("\n2. Production mode (no saving):")
    result = await loader.run(
        text_data, config=RunConfig.production(execution_id="prod_001")
    )
    print(f"   Execution ID: {result.metadata.execution_id}")

    print("\n3. Testing mode (output only):")
    result = await loader.run(
        text_data, config=RunConfig.testing(save_output_only=True)
    )
    print(f"   Debug mode: {result.metadata.debug_mode}")


async def main():
    """Run all demonstrations."""
    print("\n" + "=" * 60)
    print("🍮 PUDDING PIPELINE FRAMEWORK DEMO")
    print("=" * 60)

    await demo_basic_pipeline()
    await demo_replay_mode()
    await demo_chaining_methods()
    await demo_error_handling()
    await demo_registry()
    await demo_different_configs()

    print("\n" + "=" * 60)
    print("✨ KEY FEATURES DEMONSTRATED:")
    print("=" * 60)
    print("1. Universal run() method handles any input type")
    print("2. Replay mode with no arguments")
    print("3. Multiple chaining methods")
    print("4. Graceful error handling")
    print("5. Component registry for discovery")
    print("6. Flexible configuration system")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
