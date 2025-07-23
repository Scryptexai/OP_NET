import asyncio
from playwright.async_api import async_playwright
import os
import sys

async def deploy_contract(wasm_file_path: str):
    """
    Deploy a WASM contract using OP_WALLET extension
    """
    try:
        async with async_playwright() as p:
            # Launch browser with extension support
            # Note: Extensions only work in non-headless mode
            browser_args = [
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-extensions-except=/path/to/extension',  # Update with actual extension path
                '--load-extension=/path/to/extension',  # Update with actual extension path
            ]
            
            # Check if we have a display (for GUI)
            has_display = os.environ.get('DISPLAY') is not None
            
            if has_display:
                print("Display detected. Running in GUI mode.")
                browser = await p.chromium.launch(
                    headless=False,
                    args=browser_args
                )
            else:
                print("No display detected. Running in headless mode.")
                print("Warning: Chrome extensions don't work in headless mode.")
                print("Consider using Xvfb for virtual display or run on a machine with GUI.")
                
                # Try to use xvfb-run if available
                try:
                    import subprocess
                    result = subprocess.run(['which', 'xvfb-run'], capture_output=True)
                    if result.returncode == 0:
                        print("Xvfb detected. You can run this script with:")
                        print("xvfb-run -a python3.11 deploy_contract.py")
                        return False
                except:
                    pass
                
                # Fallback to headless (won't work with extensions)
                browser = await p.chromium.launch(headless=True)
            
            context = await browser.new_context()
            page = await context.new_page()

            # Navigate to the OP_WALLET extension internal URL
            op_wallet_url = "chrome-extension://pmbjpcmaaladnfpacpmhmnfmpklgbdjb/index.html#/main"
            
            try:
                await page.goto(op_wallet_url, wait_until="load", timeout=30000)
                print("Successfully navigated to OP_WALLET")
            except Exception as e:
                print(f"Failed to navigate to OP_WALLET: {e}")
                print("\nPossible solutions:")
                print("1. Make sure OP_WALLET extension is installed")
                print("2. Update the extension ID in the script")
                print("3. Run in non-headless mode with GUI")
                print("4. Use 'xvfb-run -a python3.11 deploy_contract.py' for virtual display")
                await browser.close()
                return False

            # Wait for the wallet to load and potentially unlock
            print("Waiting for wallet to load...")
            await asyncio.sleep(5)
            
            # Check if wallet is locked (look for unlock interface)
            try:
                unlock_button = await page.query_selector("button:has-text('Unlock')")
                password_input = await page.query_selector("input[type='password']")
                
                if unlock_button or password_input:
                    print("Wallet appears to be locked. Please unlock manually.")
                    print("Waiting 15 seconds for manual unlock...")
                    await asyncio.sleep(15)
            except:
                pass

            # Navigate to deploy section
            print("Looking for Deploy option...")
            deploy_selectors = [
                "text=Deploy",
                "button:has-text('Deploy')",
                "[data-testid*='deploy']",
                ".deploy-button",
                "#deploy-btn"
            ]
            
            deploy_found = False
            for selector in deploy_selectors:
                try:
                    await page.click(selector, timeout=5000)
                    print(f"Found and clicked deploy button: {selector}")
                    deploy_found = True
                    break
                except:
                    continue
            
            if not deploy_found:
                print("Deploy button not found. Trying direct navigation...")
                deploy_url = "chrome-extension://pmbjpcmaaladnfpacpmhmnfmpklgbdjb/index.html#/deploy"
                try:
                    await page.goto(deploy_url, wait_until="load", timeout=10000)
                    print("Navigated directly to deploy page")
                except Exception as e:
                    print(f"Direct navigation failed: {e}")
                    await browser.close()
                    return False

            # Wait for deploy page to load
            print("Waiting for file upload interface...")
            try:
                await page.wait_for_selector("input[type=file]", timeout=10000)
                print("File upload interface found")
            except:
                print("File upload interface not found. Manual intervention may be needed.")
                await asyncio.sleep(5)

            # Upload the .wasm file
            file_inputs = await page.query_selector_all("input[type=file]")
            if file_inputs:
                file_input = file_inputs[0]  # Use the first file input found
                await file_input.set_input_files(wasm_file_path)
                print(f"Successfully uploaded: {wasm_file_path}")
                
                # Wait a moment for the file to be processed
                await asyncio.sleep(2)
            else:
                print("No file input found. The interface might be different than expected.")
                await browser.close()
                return False

            # Look for deployment confirmation button
            print("Looking for deployment confirmation...")
            confirm_selectors = [
                "text=Deploy Contract",
                "button:has-text('Deploy')",
                "button:has-text('Confirm')",
                "button:has-text('Sign')",
                "[data-testid*='confirm']",
                ".confirm-button"
            ]
            
            confirm_found = False
            for selector in confirm_selectors:
                try:
                    await page.click(selector, timeout=5000)
                    print(f"Clicked confirmation button: {selector}")
                    confirm_found = True
                    break
                except:
                    continue
            
            if not confirm_found:
                print("No confirmation button found. Manual confirmation may be required.")
                print("Please check the wallet interface and confirm the transaction manually.")

            print("Deployment process initiated. Monitoring for 10 seconds...")
            await asyncio.sleep(10)

            # Check for any success/error messages
            try:
                success_indicators = await page.query_selector_all(".success, .error, .notification")
                for indicator in success_indicators:
                    text = await indicator.text_content()
                    if text:
                        print(f"Status message: {text}")
            except:
                pass

            await browser.close()
            return True
            
    except Exception as e:
        print(f"An error occurred during deployment: {e}")
        return False

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("Checking prerequisites...")
    
    # Check if playwright is properly installed
    try:
        from playwright.async_api import async_playwright
        print("✅ Playwright imported successfully")
    except ImportError as e:
        print(f"❌ Playwright import failed: {e}")
        print("Run: pip install playwright && playwright install chromium")
        return False
    
    # Check if we're in the right environment
    if not os.path.exists("venv_opnet"):
        print("⚠️  Virtual environment 'venv_opnet' not found in current directory")
    else:
        print("✅ Virtual environment found")
    
    return True

async def main():
    """Main function"""
    print("OP_NET Contract Deployment Tool")
    print("=" * 40)
    
    if not check_prerequisites():
        print("Prerequisites not met. Please fix the issues above.")
        return
    
    # Specify the WASM file to deploy
    wasm_file_path = "OP_20_TKA/build/TokenA.wasm"
    
    # Check if the WASM file exists
    if not os.path.exists(wasm_file_path):
        print(f"❌ Error: {wasm_file_path} not found.")
        print("Please ensure the contract is built and the path is correct.")
        
        # Look for alternative WASM files
        print("\nLooking for other WASM files...")
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(".wasm"):
                    full_path = os.path.join(root, file)
                    print(f"Found: {full_path}")
        return
    
    print(f"✅ WASM file found: {wasm_file_path}")
    print(f"Deploying contract: {wasm_file_path}")
    
    # Deploy the contract
    success = await deploy_contract(wasm_file_path)
    
    if success:
        print("\n✅ Deployment process completed!")
        print("Please check your OP_WALLET for transaction status.")
    else:
        print("\n❌ Deployment failed!")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    asyncio.run(main())