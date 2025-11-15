# Automation Practice Site - Test Automation Framework

## Framework Structure
```
automationpractice-site-automation/
├── pages/              # Page Object Model classes
├── tests/              # Test cases
├── testdata/           # Excel test data files
├── testrunner/         # Test runners for each module
├── utils/              # Helper utilities and configurations
├── reports/            # HTML and Allure test reports
└── conftest.py         # Pytest fixtures and configurations
```

## Prerequisites
- Python 3.12+
- Chrome Browser
- Required packages: `pip install -r requirements.txt`

## Running Tests

### Run All Tests
```bash
python testrunner/all_tests_runner.py
```

### Run Module-Specific Tests
```bash
python testrunner/login_runner.py
python testrunner/registration_runner.py
python testrunner/profile_runner.py
python testrunner/cart_runner.py
```

## Test Reports
- HTML reports are generated in `reports/` directory
- Logs are captured and displayed in HTML reports
- Each test run creates a module-specific report (e.g., `login_report.html`)

---

## Test Cases Documentation

### 1. CART MODULE

#### **TC01: Add Single Product to Cart**
- **Objective**: Verify user can add a single product to shopping cart
- **Steps**:
  1. Navigate to Shop page
  2. Select a product
  3. Click "Add to Cart"
  4. View cart
- **Expected Result**: Product is added to cart with correct details
- **Priority**: Critical
- **Status**: Automated ✅

#### **TC02: Add Multiple Quantities of Same Product**
- **Objective**: Verify user can add multiple quantities of the same product
- **Steps**:
  1. Navigate to Shop page
  2. Select a product
  3. Increase quantity
  4. Click "Add to Cart"
  5. View cart
- **Expected Result**: Cart shows correct quantity and total price
- **Priority**: High
- **Status**: Automated ✅

#### **TC03: Add Different Products to Cart**
- **Objective**: Verify user can add multiple different products
- **Steps**:
  1. Navigate to Shop page
  2. Add first product to cart
  3. Continue shopping
  4. Add second product to cart
  5. View cart
- **Expected Result**: Both products appear in cart with correct details
- **Priority**: High
- **Status**: Automated ✅

#### **TC04: Remove Single Product**
- **Objective**: Verify user can remove a product from cart
- **Steps**:
  1. Add product to cart
  2. View cart
  3. Click remove/delete icon
- **Expected Result**: Product is removed, cart updates correctly
- **Priority**: High
- **Status**: Automated ✅

#### **TC05: Remove One Product from Multiple**
- **Objective**: Verify removing one product when cart has multiple items
- **Steps**:
  1. Add multiple products to cart
  2. View cart
  3. Remove one specific product
  4. Verify remaining products
- **Expected Result**: Only selected product is removed, others remain in cart
- **Priority**: Medium
- **Status**: Automated ✅

---
### 2. PROFILE MODULE

#### **TC01: Add Valid Address**
- **Objective**: Verify user can add and save billing address
- **Precondition**: User must be logged in
- **Test Data**: 
  - Street: 123 Main St
  - City: Chennai
  - State: Chennai
  - Postcode: 110001
  - Country: India
- **Steps**:
  1. Navigate to My Account
  2. Click Edit Address (Billing)
  3. Enter valid address details
  4. Click Save Address
- **Expected Result**: Address saved successfully, success message displayed
- **Priority**: High
- **Status**: Automated ✅

#### **TC02: Add Shipping Address**
- **Objective**: Verify user can add shipping address separately from billing
- **Precondition**: User must be logged in
- **Test Data**: 
  - Street: 45 Park Ave
  - City: Hyderabad
  - State: Telangana
  - Postcode: 400001
  - Country: India
- **Steps**:
  1. Navigate to My Account
  2. Click Edit Shipping Address
  3. Enter valid shipping address details
  4. Click Save Address
- **Expected Result**: Shipping address saved successfully and displayed correctly
- **Priority**: High
- **Notes**: Ensures shipping address is saved separately from billing address
- **Status**: Automated ✅

#### **TC03: Verify Address Persistence After Logout/Login**
- **Objective**: Verify saved address persists across user sessions
- **Precondition**: User has saved address
- **Test Data**: N/A (uses previously saved address)
- **Steps**:
  1. Add valid address (123 Main St, Chennai, 110001)
  2. Logout from account
  3. Login again with same credentials
  4. Navigate to Edit Address
  5. Verify address details are displayed
- **Expected Result**: Previously saved address details (street, city, postcode) are displayed correctly
- **Priority**: High
- **Notes**: Validates data persistence across sessions
- **Status**: Automated ✅
---

### 3. LOGIN MODULE

#### **LOG-01: Login with Correct Credentials**
- **Objective**: Verify successful login with valid email and password
- **Test Data**: 
  - Email: user123@mail.com
  - Password: Str0ngPass!
- **Steps**:
  1. Navigate to My Account page
  2. Enter valid email and password
  3. Click Login button
- **Expected Result**: Login succeeds, user account dashboard is displayed
- **Priority**: Critical
- **Status**: Automated ✅

#### **LOG-02: Login with Email in Different Case**
- **Objective**: Verify login is case-insensitive for email
- **Test Data**: 
  - Email: User123@mail.com (mixed case)
  - Password: Str0ngPass!
- **Steps**:
  1. Navigate to My Account page
  2. Enter email with different case
  3. Click Login button
- **Expected Result**: Login succeeds despite case difference
- **Priority**: High
- **Status**: Automated ✅

#### **LOG-NEG-01: Login with Incorrect Password**
- **Objective**: Verify login fails with wrong password
- **Test Data**: 
  - Email: user123@mail.com
  - Password: WrongPass!
- **Steps**:
  1. Navigate to My Account page
  2. Enter valid email but incorrect password
  3. Click Login button
- **Expected Result**: Login fails with error message "The password you entered is incorrect"
- **Priority**: Critical
- **Status**: Automated ✅

#### **LOG-NEG-02: Login with Non-Existent Email**
- **Objective**: Verify login fails with unregistered email
- **Test Data**: 
  - Email: nouser@mail.com
  - Password: AnyPass123
- **Steps**:
  1. Navigate to My Account page
  2. Enter non-existent email
  3. Click Login button
- **Expected Result**: Login fails with error "No account found"
- **Priority**: High
- **Status**: Automated ✅

#### **LOG-NEG-03: Login with Blank Fields**
- **Objective**: Verify validation for empty email and password
- **Test Data**: 
  - Email: (empty)
  - Password: (empty)
- **Steps**:
  1. Navigate to My Account page
  2. Leave email and password fields blank
  3. Click Login button
- **Expected Result**: Required field error messages are displayed
- **Priority**: Medium
- **Status**: Automated ✅

---

### 4. REGISTRATION MODULE

#### **REG-01: Register with Valid New Email/Password**
- **Objective**: Verify successful registration with valid credentials
- **Test Data**: 
  - Email: Randomly generated (e.g., userABC123@gmail.com)
  - Password: Strong password (e.g., Test@1234)
- **Steps**:
  1. Navigate to My Account page
  2. Enter unique email and strong password
  3. Click Register button
- **Expected Result**: User account is created, account page displayed with no errors
- **Priority**: Critical
- **Status**: Automated ✅

#### **REG-02: Register with Minimum Valid Password**
- **Objective**: Verify registration with shortest allowed password
- **Test Data**: 
  - Email: Randomly generated
  - Password: Minimum length password meeting requirements
- **Steps**:
  1. Navigate to My Account page
  2. Enter unique email and minimum valid password
  3. Click Register button
- **Expected Result**: Registration succeeds with minimum password length
- **Priority**: High
- **Status**: Automated ✅

#### **REG-NEG-01: Register with Already Registered Email**
- **Objective**: Verify system prevents duplicate account creation
- **Test Data**: 
  - Email: user123@mail.com (existing account)
  - Password: Test@1234
- **Steps**:
  1. Navigate to My Account page
  2. Enter already registered email
  3. Click Register button
- **Expected Result**: Registration fails, error message about existing account
- **Priority**: Critical
- **Status**: Automated ✅

#### **REG-NEG-02: Register with Invalid Email Format**
- **Objective**: Verify email format validation
- **Test Data**: 
  - Email: invalidemail (no @ or domain)
  - Password: Test@1234
- **Steps**:
  1. Navigate to My Account page
  2. Enter invalid email format
  3. Click Register button
- **Expected Result**: Error message for invalid email format
- **Priority**: High
- **Status**: Automated ✅

#### **REG-NEG-03: Register with Weak Password**
- **Objective**: Verify password strength requirements are enforced
- **Test Data**: 
  - Email: Randomly generated
  - Password: 123 (weak password)
- **Steps**:
  1. Navigate to My Account page
  2. Enter weak password
  3. Verify password strength indicator shows "Very weak"
- **Expected Result**: Registration blocked, password strength warning displayed
- **Priority**: High
- **Status**: Automated ✅

#### **REG-NEG-04: Register with Blank Fields**
- **Objective**: Verify required field validation
- **Test Data**: 
  - Email: (empty)
  - Password: (empty)
- **Steps**:
  1. Navigate to My Account page
  2. Leave fields blank
  3. Click Register button
- **Expected Result**: Required field validation errors displayed
- **Priority**: Medium
- **Status**: Automated ✅

---



## Test Data Management
- All test data is stored in Excel files under `testdata/` directory
- Each module has its own Excel file with test cases and data
- Test data includes: Test Case ID, Title, Steps, Expected Results, Priority, Status

## Logging
- Comprehensive logging implemented for all test modules
- Logs capture:
  - Test execution flow
  - User actions (login, navigation, form filling)
  - Verification results
  - Error messages
- Logs are displayed in:
  - Console output
  - HTML test reports

## Page Object Model
The framework uses Page Object Model (POM) design pattern:
- `base_page.py`: Common methods for all pages
- `login_page.py`: Login page elements and methods
- `registration_page.py`: Registration page elements and methods
- `profile_page.py`: Profile/address management elements and methods
- `cart_page.py`: Shopping cart elements and methods
- `shop_page.py`: Shop/product listing elements and methods

## Reporting
- HTML reports with detailed test results
- Allure reports support (results stored in `allure-results/`)
- Screenshots captured on test failures
- Test execution logs embedded in reports

## Best Practices Implemented
1. **Page Object Model**: Separation of test logic and page elements
2. **Data-Driven Testing**: Excel-based test data management
3. **Reusable Components**: Common utilities and helper functions
4. **Comprehensive Logging**: Detailed execution logs for debugging
5. **Modular Test Structure**: Independent test modules for each feature
6. **Explicit Waits**: Proper synchronization with WebDriverWait
7. **Error Handling**: Try-catch blocks with screenshot capture on failures

## Contributing
When adding new test cases:
1. Add test data to appropriate Excel file
2. Update page objects if new elements are needed
3. Write test methods following existing patterns
4. Add comprehensive logging
5. Update this README with test case documentation

## Support
For issues or questions, refer to the test execution logs and HTML reports in the `reports/` directory.
