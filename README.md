# The Profitabox
Is that movie a Boom or Bomb? Find out here.

## Description
This dataset is comprised of movies general data, e.g. Title, Director, Runtime, MPAA Rating, Box Office Revenues, along with their budgets and profit. The profits displayed here are estimated using 50/40/25 rule that's been around. The budgets are directly extracted from web sources (Box Office Mojo and IMDb) wwithout intervention from me, thus I know nothing about their credibility. Feel free to contribute!

### Prerequisites
1. Git (duh)
2. [Python 3](https://https://www.python.org/downloads/)

### How to run
1. Clone and go to the directory
```
git clone https://github.com/primetime49/profitabox.git
cd profitabox
```
2. Install requirements
```
pip install -r requirements.txt
```
3. Run GUI (using the pre-built dataset I've provided in here)
```
python gui.py
```

#### OPTIONAL - If you want to try building the dataset from scratch
1. Init dataset
```
python create.py
```
2. Update dataset regularly, if you want. (I usually update them weekly and only for this year's movies)
```
python update.py
```

### Acknowledgements:
- https://www.boxofficemojo.com/
- https://www.crummy.com/software/BeautifulSoup/

If you have any questions or feedback, just contact [me](mailto:adityo.anggraito@gmail.com) :)
