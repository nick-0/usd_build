from pxr import Tf
from pxr.Usdviewq.plugin import PluginContainer

class TutorialPluginContainer(PluginContainer):

    def registerPlugins(self, plugRegistry, usdviewApi):
        
        # defferred import to speed up usdview launch
        printer =self.deferredImport(".printer")
        self._printMessage = plugRegistry.registerCommandPlugin(
            "TutorialPluginContainer.printMessage",
            "Print Message",
            printer.printMessage)
        
        sendMail = self.deferredImport(".sendMail")
        self._sendEmail = plugRegistry.registerCommandPlugin(
            "TutorialPluginContainer.sendMail",
            "Send Screenshot via Email",
            sendMail.SendMail)

        massProps = self.deferredImport(".massProps")
        self._massProps = plugRegistry.registerCommandPlugin(
            "TutorialPluginContainer.massProps",
            "Prints Mass Properties",
            massProps.MassProps
        )
        print(dir(self._massProps))
        usdviewApi.dataModel.selection.signalPrimSelectionChanged.connect(self._massProps.run)

    def configureView(self, plugRegistry, plugUIBuilder):
        tutMenu = plugUIBuilder.findOrCreateMenu("Tutorial")
        tutMenu.addItem(self._printMessage)
        tutMenu.addItem(self._sendEmail)

Tf.Type.Define(TutorialPluginContainer)