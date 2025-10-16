class PipPage:


    def __init__(self,page):
        self.page=page
        self.closeDialog = self.page.locator("xpath=//dialog//button[@aria-label='close-global-modal']")


    def closeDialog(self):
        self.closeDialog.click()



