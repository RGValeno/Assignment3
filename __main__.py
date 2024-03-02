from assignment3_JSON_redis import Assignment3

def main():
    assignment = Assignment3()
    assignment.read_api()
    assignment.json_into_redis()
    assignment.read_data_from_redis()
    assignment.clean_data()
    assignment.plot_diagram()
    assignment.index_JSON()
    assignment.simple_search()
    assignment.query()

if __name__ == "__main__":
    main()
