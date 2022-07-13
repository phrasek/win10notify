import logging
import threading
from os.path import realpath

import winsdk.windows.data.xml.dom as dom
import winsdk.windows.ui.notifications as notifications

__all__ = ["Notifier"]
logger = logging.getLogger(__name__)


class Notifier(object):
    """
    Create a windows toast notification.
    """

    def __init__(self):
        self._thread = None

    def _notify(self, title, msg, imgpath, appid, supressToast) -> None:
        notificationManager = notifications.ToastNotificationManager
        template = notificationManager.get_template_content(
            notifications.ToastTemplateType.TOAST_IMAGE_AND_TEXT02
        )
        toastXml = dom.XmlDocument()
        toastXml.load_xml(
            template.get_xml()
            .replace('<text id="1"></text>', f'<text id="1">{title}</text>')
            .replace('<text id="2"></text>', f'<text id="2">{msg}</text>')
            .replace(
                '<image id="1" src=""/>',
                f'<image id="1" src="{realpath(imgpath)}"/>',
            )
        )
        toast = notifications.ToastNotification(toastXml)
        toast.suppress_popup = supressToast
        toast.tag = appid
        toast.group = appid
        mytoast = notificationManager.create_toast_notifier(appid)
        logger.debug(f"Showing notification with title {title} and app id {appid}")
        mytoast.show(toast)

        return None

    def notify(
        self,
        title: str = "",
        msg: str = "",
        imgpath: str = "",
        appid: str = "appid",
        supressToast: bool = False,
        threaded: bool = False,
    ) -> None:
        """
        Notification settings.

        :title: notification title
        :msg: notification message
        :imgpath: path to an image to use for the toast
        :appid: Appid to use when creating the toast
        :supressToast: supress the toast and only show in action center

        Duration that toast notification is shown on screen for can be modified via windows settings
        """
        if not threaded:
            self._notify(
                title=title,
                msg=msg,
                imgpath=imgpath,
                appid=appid,
                supressToast=supressToast,
            )
        else:
            if self.notification_active():
                logger.debug(
                    "Notification already active, starting background thread to notify later"
                )
                return False

            self._thread = threading.Thread(
                target=self._notify,
                args=(title, msg, imgpath, appid, supressToast),
            )
            self._thread.start()
        return None

    def notification_active(self) -> bool:
        """See if there is an active notification showing"""
        if self._thread is not None and self._thread.is_alive():
            # There is an active notification, let it finish before sending another
            return True
        return False
