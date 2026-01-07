import os
import logging
import httpx
from src.utils.logger import get_logger
from src.llm.prompt_template2 import build_summary_prompt
from llama_index.llms.ollama import Ollama
import pandas as pd

logger = get_logger(__name__)

def check_ollama_running() -> bool:
    """Check if Ollama service is running"""
    try:
        response = httpx.get("http://localhost:11434/api/tags", timeout=5)
        response.raise_for_status()
        return True
    except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPStatusError) as e:
        logger.error(f"Ollama check failed: {e}")
        return False

def call_llm(prompt: str, model: str = "llama3.1:8b", timeout: int = 300) -> str:
    """
    Call Ollama LLM with error handling
    
    Args:
        prompt: The prompt to send
        model: Model name (default: llama3.1:8b)
        timeout: Request timeout in seconds (increased to 300 for larger responses)
    
    Returns:
        str: LLM response text
        
    Raises:
        RuntimeError: If Ollama is not running or other errors occur
    """
    # Check if Ollama is running
    if not check_ollama_running():
        error_msg = (
            "\n❌ Ollama is NOT running!\n"
            "Please start Ollama:\n"
            "1. Open a new terminal\n"
            "2. Run: ollama serve\n"
            "3. In another terminal, verify: ollama list\n"
            "4. If model is missing, run: ollama pull llama3.1:8b"
        )
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    
    try:
        logger.info(f'Calling LLM model: {model} with timeout={timeout}s')
        logger.info(f'Prompt length: {len(prompt)} characters')
        
        # Initialize Ollama with increased timeout
        llm = Ollama(model=model, request_timeout=timeout)
        
        # Make the request
        logger.info('Sending request to Ollama...')
        response = llm.complete(prompt)
        
        response_txt = str(response)
        logger.info(f'✅ Received response: {len(response_txt)} characters')
        logger.debug(f'Response preview: {response_txt[:200]}...')
        
        return response_txt
        
    except httpx.ReadTimeout:
        error_msg = (
            f"\n❌ Request timed out after {timeout} seconds!\n"
            "Possible solutions:\n"
            "1. Increase timeout (current: {timeout}s)\n"
            "2. Use a smaller model (e.g., llama3.2:1b)\n"
            "3. Reduce the amount of data in the prompt\n"
            "4. Check if your system has enough resources"
        )
        logger.error(error_msg)
        raise RuntimeError(error_msg)
        
    except httpx.ConnectError:
        error_msg = "\n❌ Cannot connect to Ollama. Make sure 'ollama serve' is running."
        logger.error(error_msg)
        raise RuntimeError(error_msg)
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            error_msg = (
                f"\n❌ Model '{model}' not found!\n"
                f"Pull it with: ollama pull {model}"
            )
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        else:
            logger.error(f"HTTP error: {e}")
            raise
            
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

def generate_summary(df, rows: int = 20, model: str = "llama3.1:8b", timeout: int = 300) -> str:
    """
    Generate financial summary from DataFrame
    
    Args:
        df: pandas DataFrame with financial data
        rows: Number of rows to include (default: 20)
        model: Ollama model name (default: llama3.1:8b)
        timeout: Request timeout in seconds (default: 300)
        
    Returns:
        str: Generated summary from LLM
    """
    try:
        logger.info(f'Generating summary from {len(df)} rows (using first {rows})')
        
        # Convert to CSV snippet
        csv_snippet = df.head(rows).to_csv(index=False)
        logger.info(f'CSV snippet size: {len(csv_snippet)} characters')
        
        # Build prompt
        prompt = build_summary_prompt(csv_snippet)
        logger.info(f'Full prompt size: {len(prompt)} characters')
        
        # Call LLM
        result = call_llm(prompt=prompt, model=model, timeout=timeout)
        
        return result
        
    except Exception as e:
        logger.error(f'Error generating summary: {e}')
        raise

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 TESTING OLLAMA LLM INTEGRATION")
    print("="*60 + "\n")
    
    # Step 1: Check Ollama status
    print("1️⃣ Checking Ollama status...")
    if check_ollama_running():
        print("   ✅ Ollama is running!\n")
    else:
        print("   ❌ Ollama is NOT running!")
        print("\n📋 To fix this:")
        print("   1. Open a new terminal")
        print("   2. Run: ollama serve")
        print("   3. Keep that terminal open")
        print("   4. Run this script again\n")
        exit(1)
    
    # Step 2: Run test
    logger.info('Starting main function')
    
    print("2️⃣ Creating test data...")
    test_df = pd.DataFrame({
        'Date': ['2024-01-01', '2024-02-01', '2024-03-01'],
        'Revenue': [100000, 110000, 105000],
        'Expenses': [60000, 65000, 63000],
        'EBITDA': [40000, 45000, 42000],
        'Free_Cash_Flow': [35000, 40000, 37000]
    })
    print("   ✅ Test DataFrame created\n")
    print(test_df)
    
    print("\n3️⃣ Generating summary (this may take 30-60 seconds)...")
    try:
        result = generate_summary(test_df, rows=3, timeout=300)
        
        print("\n" + "="*60)
        print("📝 GENERATED SUMMARY:")
        print("="*60)
        print(result)
        print("="*60)
        
        logger.info('✅ Done!')
        print("\n✅ Test completed successfully!")
        
    except RuntimeError as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logger.exception("Unexpected error in test")
        exit(1)