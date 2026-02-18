# from src.app import App
# funcs = App()


# classes
from src.auth.auth_flow import AuthFlow

if __name__ == "__main__":
    authflow = AuthFlow()
    authflow.run()
