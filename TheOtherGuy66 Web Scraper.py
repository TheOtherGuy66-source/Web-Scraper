import subprocess
import sys

def install_packages():
    required_packages = ['PyQt5', 'requests', 'bs4']
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

install_packages()

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QCheckBox, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QFont
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

class WebScraperGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("TheOtherGuy66 Web Scraper")
        self.setGeometry(100, 100, 900, 760)
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff;")

        font = QFont("Courier", 10)

        vbox = QVBoxLayout()

        # URL Entry
        hbox_url = QHBoxLayout()
        self.url_label = QLabel("Enter URL:")
        self.url_label.setFont(font)
        hbox_url.addWidget(self.url_label)
        self.url_entry = QLineEdit(self)
        self.url_entry.setFont(font)
        hbox_url.addWidget(self.url_entry)
        vbox.addLayout(hbox_url)

        # Options
        self.options_label = QLabel("Select Options:")
        self.options_label.setFont(font)
        vbox.addWidget(self.options_label)

        # Checkboxes
        self.check_var_html = QCheckBox("Full HTML", self)
        self.check_var_html.setFont(font)
        vbox.addWidget(self.check_var_html)

        self.check_var_heading = QCheckBox("Headings", self)
        self.check_var_heading.setFont(font)
        vbox.addWidget(self.check_var_heading)

        self.check_var_paragraph = QCheckBox("Paragraphs", self)
        self.check_var_paragraph.setFont(font)
        vbox.addWidget(self.check_var_paragraph)

        self.check_var_css = QCheckBox("CSS", self)
        self.check_var_css.setFont(font)
        vbox.addWidget(self.check_var_css)

        self.check_var_table = QCheckBox("Tables", self)
        self.check_var_table.setFont(font)
        vbox.addWidget(self.check_var_table)

        self.check_var_links = QCheckBox("Links", self)
        self.check_var_links.setFont(font)
        vbox.addWidget(self.check_var_links)

        self.check_var_files = QCheckBox("Files", self)
        self.check_var_files.setFont(font)
        vbox.addWidget(self.check_var_files)

        self.check_var_m3u = QCheckBox("M3U/M3U8 Files", self)
        self.check_var_m3u.setFont(font)
        vbox.addWidget(self.check_var_m3u)

        self.check_var_images = QCheckBox("Images", self)
        self.check_var_images.setFont(font)
        vbox.addWidget(self.check_var_images)

        self.check_var_videos = QCheckBox("Videos", self)
        self.check_var_videos.setFont(font)
        vbox.addWidget(self.check_var_videos)

        self.check_var_metadata = QCheckBox("Metadata", self)
        self.check_var_metadata.setFont(font)
        vbox.addWidget(self.check_var_metadata)

        # Buttons
        hbox_buttons = QHBoxLayout()
        
        self.scrape_button = QPushButton("SCRAPE", self)
        self.scrape_button.setFont(font)
        self.scrape_button.setStyleSheet("background-color: #3c3f41; color: #ffffff;")
        self.scrape_button.clicked.connect(self.scrape)
        hbox_buttons.addWidget(self.scrape_button)
        
        self.save_result_button = QPushButton("Save Result", self)
        self.save_result_button.setFont(font)
        self.save_result_button.setStyleSheet("background-color: #3c3f41; color: red;")
        self.save_result_button.clicked.connect(self.save_result)
        hbox_buttons.addWidget(self.save_result_button)
        
        self.clear_content_button = QPushButton("Clear Content", self)
        self.clear_content_button.setFont(font)
        self.clear_content_button.setStyleSheet("background-color: #3c3f41; color: #ffffff;")
        self.clear_content_button.clicked.connect(self.clear_content)
        hbox_buttons.addWidget(self.clear_content_button)
        
        vbox.addLayout(hbox_buttons)

        # Result Text Field
        self.result_label = QLabel("Scraped Content of Websites:")
        self.result_label.setFont(font)
        vbox.addWidget(self.result_label)

        self.result_text = QTextEdit(self)
        self.result_text.setFont(font)
        self.result_text.setStyleSheet("background-color: #3c3f41; color: #ffffff;")
        vbox.addWidget(self.result_text)

        self.setLayout(vbox)

    def scrape(self):
        url = self.url_entry.text()
        if not url:
            return
        
        options = {
            'html': self.check_var_html.isChecked(),
            'heading': self.check_var_heading.isChecked(),
            'paragraph': self.check_var_paragraph.isChecked(),
            'css': self.check_var_css.isChecked(),
            'table': self.check_var_table.isChecked(),
            'links': self.check_var_links.isChecked(),
            'files': self.check_var_files.isChecked(),
            'm3u': self.check_var_m3u.isChecked(),
            'images': self.check_var_images.isChecked(),
            'videos': self.check_var_videos.isChecked(),
            'metadata': self.check_var_metadata.isChecked()
        }
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        result = ""
        if options['html']:
            result += str(soup) + '\n\n'

        if options['heading']:
            headings = soup.find_all(re.compile('^h[1-6]$'))
            for heading in headings:
                result += heading.text + '\n'
            result += '\n'

        if options['paragraph']:
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                result += paragraph.text + '\n'
            result += '\n'

        if options['css']:
            css_links = [link['href'] for link in soup.find_all('link', rel='stylesheet')]
            result += "CSS Links:\n"
            for css_link in css_links:
                full_url = urljoin(url, css_link)
                result += full_url + '\n'
            result += '\n'

        if options['table']:
            tables = soup.find_all('table')
            result += "Tables:\n"
            for table in tables:
                result += str(table) + '\n'
            result += '\n'

        if options['links']:
            links = soup.find_all('a', href=True)
            result += "Links:\n"
            for link in links:
                if link['href'].startswith('http'):
                    result += f"Text: {link.text}, URL: {link['href']}\n"
                else:
                    full_url = urljoin(url, link['href'])
                    result += f"Text: {link.text}, URL: {full_url}\n"
            result += '\n'

        if options['files']:
            try:
                file_links = [link['href'] for link in soup.find_all('a', href=True) if re.search(r'\.[^.]+$', link['href'])]
                result += "File Links:\n"
                for file_link in file_links:
                    full_url = urljoin(url, file_link)
                    result += full_url + '\n'
                result += '\n'
            except AttributeError as e:
                result += f"Error occurred while fetching file links: {e}\n\n"

        if options['m3u']:
            m3u_links = soup.find_all('a', href=True, text=re.compile(r'.*\.m3u8?$'))
            result += "M3U/M3U8 Files:\n"
            for m3u_link in m3u_links:
                if m3u_link['href'].startswith('http'):
                    result += f"URL: {m3u_link['href']}\n"
                else:
                    full_url = urljoin(url, m3u_link['href'])
                    result += f"URL: {full_url}\n"
                
                response = requests.get(full_url)
                if response.ok:
                    content = response.text.split('\n')
                    for line in content:
                        if line.startswith('#EXTINF'):
                            result += f"Segment: {line.split(',')[-1]}\n"
                        elif line and not line.startswith('#'):
                            result += f"URL: {line}\n"
                else:
                    result += f"Failed to fetch M3U/M3U8 content from {full_url}\n"
            result += '\n'

        if options['images']:
            images = soup.find_all('img', src=True)
            result += "Images:\n"
            for image in images:
                full_url = urljoin(url, image['src'])
                result += f"Image: {full_url}\n"
            result += '\n'

        if options['videos']:
            videos = soup.find_all('video', src=True)
            result += "Videos:\n"
            for video in videos:
                full_url = urljoin(url, video['src'])
                result += f"Video: {full_url}\n"
            result += '\n'

        if options['metadata']:
            metadata = soup.find_all(['meta', 'title'])
            result += "Metadata:\n"
            for data in metadata:
                result += str(data) + '\n'
            result += '\n'

        self.result_text.setPlainText(result)

    def save_result(self):
        result_text = self.result_text.toPlainText()
        if not result_text.strip():
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Result", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(result_text)

    def clear_content(self):
        self.result_text.clear()

def main():
    app = QApplication(sys.argv)
    scraper = WebScraperGUI()
    scraper.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
