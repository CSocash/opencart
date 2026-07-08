import pytest
import allure
from pathlib import Path
from playwright.sync_api import sync_playwright
# ========================================================================
# PYTEST + PLAYWRIGHT TEST CONFIGURATION FILE
# ========================================================================
# This file provides:
# 1. Command-line options (browser, base URL, video, screenshots, etc.)
# 2. Hooks to track test results.  Hooks are used to change pytest configurations
# 3. Fixtures for browser setup and teardown.  Fixtures are reusable methods.
# 4. Screenshot, video, and trace attachments to Allure reports
# ========================================================================
# ----------------------------------------------------------------------------
# STEP 1: ADD COMMAND LINE OPTIONS
# ----------------------------------------------------------------------------
def pytest_addoption(parser):  
    """
    This method is a hook to provide usable command line arguments for the test configuration
    (adds command line options to the parser), ex: --browser chromium
    The default used is what is stored in the pytest.ini file.  But one can override these when
    running pytest by adding one or more of these commands in the command line at run time 
    (priority is given to the options specified in the command line).
    """
    parser.addoption("--browser", default="chromium", help="Browser: chromium, firefox, webkit")
    parser.addoption("--headed", action="store_true", help="Run in headed (visible) mode")
    parser.addoption("--base-url", default="https://tutorialsninja.com/demo/", help="Base URL for tests")
    parser.addoption("--video", default="retain-on-failure", help="Record video: on, off, retain-on-failure")
    parser.addoption("--screenshot", default="only-on-failure", help="Take screenshot: on, off, only-on-failure")
    parser.addoption("--tracing", default="retain-on-failure", help="Tracing: on, off, retain-on-failure")
# ----------------------------------------------------------------------------
# STEP 2: GET CONFIGURATION VALUE (CMDLINE OR pytest.ini)
# ----------------------------------------------------------------------------
def get_config_value(config, option_name):
    """
    This method actually reads in the arguments which are passed in the command line or else from pytest.ini
    Helper to read configuration values.
    Tries to get from command line first, otherwise from pytest.ini.
    Supports both string and boolean options.
    config is a pytest.Config instance (from pytest.config).  There are built-in methods on config through pytest: 
    .getoption() is for retrieving command line options or options registered with pytest (pytest.ini_options
    or pytest plugins).  
    .getini() reads directly from pytest.ini.
    """
    # Try command-line first
    cmd_value = config.getoption(option_name)
    if cmd_value is not None:
        return cmd_value
    # Fallback to pytest.ini
    if option_name == "headed":
        ini_value = config.getini(option_name)
        return ini_value.lower() == "true" if isinstance(ini_value, str) else ini_value
    else:
        return config.getini(option_name)
# ----------------------------------------------------------------------------
# STEP 3: HOOK TO TRACK TEST RESULTS (PASS/FAIL)
# ----------------------------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    hookimpl is a method used by pytest.  It captures/returns the test result (pass/fail/skip)
    after each test.
    This is used later to decide whether to take screenshots or save traces.
    """
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
# ----------------------------------------------------------------------------
# STEP 4: FIXTURE 1 - BROWSER CONTEXT SETUP
# ----------------------------------------------------------------------------
@pytest.fixture(scope="function")
def browser_context(request):
    """
    This is the main fixture that controls everything.
    Creates and manages the Playwright browser context.
    - Reads configuration (browser, headed mode, video settings)
    - Starts the Playwright browser
    - Enables video recording if configured
    - Returns (sends) this context to the test
    - Cleans up automatically after each test
    """
# Read configuration values first from command line, otherwise pytest.ini
    browser_name = get_config_value(request.config, "browser")
    headed_flag = get_config_value(request.config, "headed")
    video_option = get_config_value(request.config, "video")
    print(f"\n🎯 Starting browser: {browser_name}")
    print(f"🎯 Headless mode: {not headed_flag} (headed={headed_flag})")
    
    # Start Playwright
    playwright = sync_playwright().start()
    
    # Create/Launch the specified browser
    if browser_name.lower() == "chromium":
        browser = playwright.chromium.launch(headless=not headed_flag)
    elif browser_name.lower() == "firefox":
        browser = playwright.firefox.launch(headless=not headed_flag)
    elif browser_name.lower() == "webkit":
        browser = playwright.webkit.launch(headless=not headed_flag)
    else:
        raise ValueError(f"❌ Unsupported browser: {browser_name}")
    
    # Create a browser context (optionally with video recording) to control video and trace
    if video_option in ["on", "retain-on-failure"]:
        context = browser.new_context(record_video_dir="reports/videos")
    else:
        context = browser.new_context()
    
    # Yield the context for use in tests
    # Yield does two jobs: if fixture wants to return a value, you can specify it with the yield.
    # In this example, the fixture is returning "context" to the test
    # And if we want to execute steps after the fixture, you can put them after the yield.
    yield context
    
    # Clean up after the test
    print("🧹 Closing browser context and stopping Playwright...")
    context.close()
    browser.close()
    playwright.stop()
# ----------------------------------------------------------------------------
# STEP 5: FIXTURE 2 - PAGE CREATION AND TEST ARTIFACT MANAGEMENT
# ----------------------------------------------------------------------------
@pytest.fixture(scope="function")
def page(request, browser_context):
    """
    Creates a new browser page for each test.
    - Navigates to the base URL
    - Starts tracing (if enabled)
    - Captures screenshots, traces, and videos for failed tests
    - Attaches all artifacts to Allure report
    """
    # Read test configuration at the time of launching the page
    base_url = get_config_value(request.config, "base_url")
    screenshot_option = get_config_value(request.config, "screenshot")
    tracing_option = get_config_value(request.config, "tracing")
    video_option = get_config_value(request.config, "video")

    print(f"🌐 Navigating to: {base_url}")

    # Start tracing if enabled
    # Note: initial default tracing setting is set in the pytest.ini file
    if tracing_option in ["on", "retain-on-failure"]:
        print("📹 Tracing enabled - capturing screenshots and actions")
        browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    # Create and navigate to base URL
    page = browser_context.new_page()
    page.goto(base_url)
    
    # Yield the page to the test
    yield page
# ------------------------------------------------------------------------
# After the test: manage artifacts (screenshots, videos, traces)
# ------------------------------------------------------------------------
    test_name = request.node.name
    test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    
    print(f"\n📊 Test '{test_name}' result: {'❌ FAILED' if test_failed else '✅ PASSED'}")
    
    # Save and attach trace
    if tracing_option in ["on", "retain-on-failure"]:
        trace_path = f"reports/traces/{test_name}_trace.zip"
        browser_context.tracing.stop(path=trace_path)
        print(f"💾 Trace saved: {trace_path}")
        # Attach trace to Allure report if test failed
        # Currently ZIP file is not supporting to attach in allure reports
        # if test_failed:
        # allure.attach.file(
        # trace_path,
        # name=f"{test_name}_trace",
        # attachment_type=allure.attachment_type.ZIP
        # )
        # print("📎 Trace attached to Allure report")
    
    # Take screenshot if test failed
    if test_failed and screenshot_option in ["on", "only-on-failure"]:
        screenshot_path = f"reports/screenshots/{test_name}.png"
        page.screenshot(path=screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")
    
        # Attach to Allure report
        allure.attach.file(screenshot_path,name=f"{test_name}_screenshot",attachment_type=allure.attachment_type.PNG)
        print("📎 Screenshot attached to Allure report")
    
    
    # Attach video if available and test failed
    if test_failed and video_option in ["on", "retain-on-failure"]:
        video_path = page.video.path() if page.video else None
        if video_path and Path(video_path).exists():
            allure.attach.file(video_path,name=f"{test_name}_video",attachment_type=allure.attachment_type.WEBM)
        print("🎥 Video attached to Allure report")


    

    # Additional Notes
    # to play the trace, enter the following command:
    # playwright show-trace traces/playwright show-trace reports/traces/[test name]__trace.zip
    # ex: playwright show-trace traces/playwright show-trace reports/traces/[test_user_registration]__trace.zip