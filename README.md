# Google-Map-Scraper
This is a Python web scraper that allows you to collect place details from Google Maps based on search queries. The scraper utilizes the power of automation and web scraping to extract information and save it to an output.csv file.

## Installation
To use this scraper, you need to have Python installed on your system. Clone this repository and install the required dependencies using the following command:
```bash
pip install -r requirements.txt
```
Make sure you have a compatible version of Chrome browser installed as the scraper utilizes Selenium WebDriver for automation.

## Usage
1. Prepare your input data by adding search queries to the input.csv file.

2. Run the scraper script using the following command:
```bash
python scraper.py
```
This will initiate the scraping process and the scraper will start searching the queries on Google Maps.

3. The scraper will gather place details, such as name, address, contact information, and more, and save them to the output.csv file.

Please note that web scraping Google Maps may be subject to their terms of service and usage policies. Ensure that your scraping activities comply with the applicable terms and legal requirements.

## Customization
Feel free to modify the script according to your requirements. You can customize the scraping process, add additional data fields to collect, or integrate with other tools and services.

## Contributing
Contributions to this project are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License
This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License.

## Disclaimer
Please use this scraper responsibly and respect the terms of service of the websites you are scraping. The authors of this project are not responsible for any misuse or legal issues arising from the use of this scraper.
