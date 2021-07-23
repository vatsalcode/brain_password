import csv
import glob
import os
from uuid import uuid4
from faker import Faker
from pymongo import MongoClient
from uuid import UUID, uuid4


PATH = os.path.abspath("./dataset")
dataset = [f for f in glob.glob(PATH + "/*")]
dataset_subject = {i: glob.glob(i+"/*.csv") for i in dataset}


# db_url = "mongodb+srv://siddharth:bF2eVWqicP1XcfQ9@cluster0.wvigh.mongodb.net/brain_password?retryWrites=true&w=majority"
db_url = "mongodb://localhost:27017"
db_name = "brain_password"
user_collection = "users"
eeg_recordings_collection = "eeg_recordings"


fake = Faker()


def startup_db_client():
  db_client = MongoClient(db_url, uuidRepresentation="standard")
  db = db_client[db_name]
  return db


def shutdown_db_client(db_client):
  db_client.close()


def gen_fake_data():
  user_id = uuid4()
  name = fake.name().split(" ")
  f_name, l_name = name[0], name[1]
  email = f_name + "." + l_name + "@gmail.com"
  return user_id, f_name, l_name, email.lower()


def read_csv(csv_file_path):
  with open(csv_file_path, "r") as file:
    reader = csv.reader(file, delimiter=",")
    x = list(map(float, [row for row in reader][0]))
  return x


if __name__ == "__main__":
  db = startup_db_client()
  count = 1

  for k, v in dataset_subject.items():
    user_id, f_name, l_name, email = gen_fake_data()

    subject_id = int(k.split("_")[-1])

    user_doc = {
      "user_id": user_id,
      "subject_id": subject_id,
      "f_name": f_name,
      "l_name": l_name,
      "email": email
    }

    signals = [read_csv(i) for i in v]
    signal_doc = {"eeg_recording_"+str(i): j for i,j in enumerate(signals, start=1)}
    signal_doc["user_id"] = user_id
    signal_doc["subject_id"] = subject_id

    user_insert = db[user_collection].insert_one(user_doc)
    signal_insert = db[eeg_recordings_collection].insert_one(signal_doc)
    print(str(count) + ": done")
    count += 1