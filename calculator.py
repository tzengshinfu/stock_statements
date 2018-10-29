from selenium import webdriver

driver = webdriver.Remote(
    command_executor='http://localhost:9999',
    desired_capabilities={'app': 'C:\\windows\\system32\\calc.exe'})

window = driver.find_element_by_class_name('CalcFrame')
window.find_element_by_name('7').click()
