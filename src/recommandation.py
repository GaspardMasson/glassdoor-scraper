from dataset import read_data
from distances import *


def sort_by_enterprise_type(dataset, enterprise_type):





def get_recommandations(offer_style, city, enterprise_type):

    dataset = read_data()

    # add a column to the dataset with the distance between the city and the offer
    dataset['distance'] = dataset.apply(lambda row: calculate_distance(row['city'], city), axis=1)

    