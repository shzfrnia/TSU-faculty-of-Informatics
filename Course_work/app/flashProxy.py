from flask import flash


class FlashProxy():
    SUCCESS = 'success'
    INFO = 'info'
    WARNING = 'warning'
    DANGER = 'danger'

    @staticmethod
    def flash(message, category='info'):
        """Proxy for flask's flash.
        Args:
            message: Message for flash.
            category: Category message.
        """
        allowed_catogory = frozenset(
            [FlashProxy.SUCCESS,
             FlashProxy.INFO,
             FlashProxy.WARNING,
             FlashProxy.DANGER]
        )
        if category not in allowed_catogory:
            raise ValueError("Uncorrect message's category!")
        flash(message, category)
