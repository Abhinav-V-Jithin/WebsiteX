import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import urllib.request
engine = create_engine('postgresql://postgres:1029384756Vithayathil@localhost:5432/book_review')
db = scoped_session(sessionmaker(bind=engine))
def connect(host='https://www.google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False
res = ''
def main():
    line=0
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn,title,author,year in reader:
        while 1:
            try:
                res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "XvwqEKsB6436BG1hfKWg", "isbns": isbn})
            except:
                print("No internet. Retrying...")
                continue
            break
        if res.status_code != 200:
            print("Found errors at:")
            print(f"status:{res.status_code}")
            print(f"line:{line+1}")
            continue
        data= res.json()
        data = data["books"]
        work_ratings_count = ''
        average_rating = ''
        id = 0
        for list in data:
            work_ratings_count = list["work_ratings_count"]
            average_rating     = list["average_rating"]
            id =  list["id"]
        db.execute("INSERT INTO goodreadsrating (isbn,rating,avg) VALUES(:isbn,:rating,:avg)",{"isbn":isbn,"rating":work_ratings_count,"avg":average_rating})
        db.execute("INSERT INTO books (isbn,title,author,year) VALUES (:isbn,:title,:author,:year)",{"isbn":isbn,"title":title,"author":author,"year":year})
        print(f"Added book with isbn={isbn} title={title} author={author} year={year}")
        print(f"Added good reads book with isbn={isbn} rating={work_ratings_count} avg={average_rating}")
        line = line+1
    db.commit()
if __name__ == '__main__':
    main()
