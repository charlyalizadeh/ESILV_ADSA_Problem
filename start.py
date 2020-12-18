from adsaapp import ADSAApp
from interface import App


def main():
    main_app = App()
    adsa_app = ADSAApp(main_app)
    adsa_app.start()

if __name__ == '__main__':
    main()


