import pandas as pd
import matplotlib.pyplot as plt
from source.query import Query, Database
import os


def plot_timeseries(
    project_id_dataframe: pd.DataFrame, column: str, title: str, output: str = ""
):
    fig, ax = plt.subplots()
    ax.plot_date(
        project_id_dataframe[column],
        y=[1] * len(project_id_dataframe[column]),
        alpha=0.5,
        ms=10,
    )
    ax.set_alpha(0.5)
    fig.suptitle(title)
    if not output:
        plt.show()
    else:
        plt.savefig(fname=output)


def plot_hist(
    project_id_dataframe: pd.DataFrame, column: str, title: str, output: str = ""
):
    fig, ax = plt.subplots()
    vals = project_id_dataframe[column].astype(float)
    vals = vals.fillna(0)
    ax.hist(vals, alpha=0.5)
    ax.set_alpha(0.5)
    fig.suptitle(title)
    # TODO: Make it so plot histogram function does not modify state by changing directory state.
    if not output:
        plt.show()
    else:
        plt.savefig(fname=output)


def main():
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    database = Database(name="sansa")
    schema = database.get_schema(table="pr")
    for row in schema:
        print(row)

    query = Query(query_string="select distinct project_id from pr")
    query_result = database.execute_query(query=query)
    min_project_id, max_project_id = float("inf"), -1
    for row in query_result:
        project_id = row[0]
        min_project_id = min(project_id, min_project_id)
        max_project_id = max(project_id, max_project_id)

    print("All queries completed")

    current_directory = os.getcwd()

    # Make output folders.
    os.makedirs("timeseries", exist_ok=True)
    os.makedirs("histogram", exist_ok=True)

    for current_project_id in range(min_project_id, max_project_id):
        # Initialize the dataframe with pandas.
        project_id_dataframe = pd.read_sql(
            f"select * from pr where project_id={current_project_id}",
            Database("sansa").get_database(),
        )
        plot_timeseries(
            project_id_dataframe=project_id_dataframe,
            column="updated_at",
            title=f"Distribution of pull requests for project id: {current_project_id}.",
            output=os.path.join("timeseries", str(current_project_id)),
        )

        # TODO: Move these dataframe calculations into a custom project id dataframe object.
        project_id_dataframe["updated_at_shift"] = project_id_dataframe[
            "updated_at"
        ].shift(-1)
        project_id_dataframe["time_difference"] = (
            project_id_dataframe["updated_at_shift"]
            - project_id_dataframe["updated_at"]
        )
        project_id_dataframe["time_difference_hourly"] = project_id_dataframe[
            "time_difference"
        ] / pd.Timedelta(hours=1)

        plot_hist(
            project_id_dataframe=project_id_dataframe,
            column="time_difference_hourly",
            title=f"Time difference on updated at columns for project_id: {current_project_id}.",
            output=os.path.join("histogram", str(current_project_id)),
        )


if __name__ == "__main__":
    main()
