import src.repository.dayPasswordRepository


class AuthenticationManager:
    def __init__(
            self,
            day_password_repository: dayPasswordRepository
    ):
        self.day_password_repository = day_password_repository

    def is_authenticated(self):
        pass

    def authenticate(self, password):
        pass