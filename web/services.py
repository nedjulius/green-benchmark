import csv

def get_rating_data():
    ratings = list(csv.reader(open("../data/final_ratings.csv", "r"), delimiter=","))
    ratings.pop()
    return ratings

# search ratings by comparing topic to make and model
def search_ratings(topic):
    results = []
    ratings = get_rating_data()
    for row in ratings:
        make_and_model = " ".join([row[0], row[1]]).lower()
        if make_and_model.find(topic.lower()) != -1:
            results.append({'make': row[0], 'model': row[1], 'rating': row[2]})

    return results

