from matrix_client.client import MatrixClient

from lemmymodbot import MatrixConfig


class MatrixFacade:
    config: MatrixConfig
    client: MatrixClient

    def __init__(self, config: MatrixConfig):
        self.config = config
        self.client = MatrixClient(config.server)

    def _login(self):
        self.client.login(self.config.account, self.config.password)

    def _logout(self):
        self.client.logout()

    def send_message(self, content: str, room_id: str):
        if room_id is None:
            room_id = self.config.room_id

        self._login()

        room = self.client.join_room(room_id)
        room.send_text(text=content)

        self._logout()

    def report_error(self):
        matrix_message = '\n\nMod bot (with L plates) : ' + ', '.join(flags)
        matrix_message = matrix_message + '\n' + str(extras)
        matrix_message = matrix_message + '\n' + str(elem.comment_view.comment)
        self.send_message(matrix_message)