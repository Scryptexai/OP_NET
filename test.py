import asyncio
from playwright.async_api import async_playwright
import os
import sys

async def test_browser_launch():
    """Test if browser can be launched successfully"""
    try:
        async with async_playwright() as p:
            print("Testing browser launch...")
            
            # Try different launch options
            launch_configs = [
                {
                    "name": "Headless with basic options",
                    "config": {
                        "headless": True,
                        "args": ["--no-sandbox", "--disable-setuid-sandbox"]
                    }
                },
                {
                    "name": "Headless with full compatibility",
                    "config": {
                        "headless": True,
                        "args": [
                            "--no-sandbox",
                            "--disable-setuid-sandbox",
                            "--disable-dev-shm-usage",
                            "--disable-gpu",
                            "--no-first-run",
                            "--no-zygote",
                            "--single-process",
                            "--disable-extensions",
                            "--disable-background-timer-throttling",
                            "--disable-backgrounding-occluded-windows",
                            "--disable-renderer-backgrounding"
                        ]
                    }
                }
            ]
            
            for config in launch_configs:
                try:
                    print(f"\nTrying: {config['name']}")
                    browser = await p.chromium.launch(**config['config'])
                    context = await browser.new_context()
                    page = await context.new_page()
                    
                    # Test basic navigation
                    await page.goto("https://www.example.com")
                    title = await page.title()
                    print(f"✅ Success! Page title: {title}")
                    
                    await browser.close()
                    return config['config']  # Return working config
                    
                except Exception as e:
                    print(f"❌ Failed: {e}")
                    continue
            
            print("❌ All browser launch attempts failed!")
            return None
            
    except Exception as e:
        print(f"❌ Playwright initialization failed: {e}")
        return None

async def deploy_contract_simple(wasm_file_path: str, browser_config: dict):
    """Simplified deployment function"""
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(**browser_config)
            context = await browser.new_context()
            page = await context.new_page()

            print("Browser launched successfully!")
            print("Note: This is a simplified version for testing browser functionality.")
            print("The actual OP_WALLET interaction would need to be implemented based on the wallet's UI.")
            
            # For now, just test that we can create a page
            await page.goto("about:blank")
            print("✅ Page created successfully!")
            print(f"Contract file to deploy: {wasm_file_path}")
            
            await browser.close()
            print("✅ Browser closed successfully!")
            
        except Exception as e:
            print(f"❌ Error in deploy_contract_simple: {e}")

async def main():
    """Main function"""
    print("=== Playwright Browser Test ===")
    
    # Test browser launch first
    working_config = await test_browser_launch()
    
    if working_config is None:
        print("\n❌ Cannot launch browser. Please check:")
        print("1. Dependencies: sudo playwright install-deps")
        print("2. Browser binaries: playwright install chromium")
        print("3. Virtual environment is activated")
        return
    
    print(f"\n✅ Found working browser configuration!")
    
    # Check for wasm file
    wasm_to_deploy = "OP_20_TKA/build/TokenA.wasm"
    
    if not os.path.exists(wasm_to_deploy):
        print(f"\n⚠️  Warning: {wasm_to_deploy} not found.")
        # Create a dummy file for testing
        os.makedirs(os.path.dirname(wasm_to_deploy), exist_ok=True)
        with open(wasm_to_deploy, 'wb') as f:
            f.write(b'dummy wasm content for testing')
        print(f"Created dummy file: {wasm_to_deploy}")
    
    # Test deployment function
    print("\n=== Testing Deployment Function ===")
    await deploy_contract_simple(wasm_to_deploy, working_config)

if __name__ == "__main__":
    # Check if we're in the right environment
    print("Python version:", sys.version)
    print("Current directory:", os.getcwd())
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()