import requests
from bs4 import BeautifulSoup
import PySimpleGUI as sg
from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)








