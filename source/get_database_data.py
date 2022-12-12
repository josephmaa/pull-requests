import MySQLdb

# import tensorflow
import pandas as pd
import matplotlib.pyplot as plt
from keys import user, passwd, database


def get_schema(cursor, table: str):
    query = f"DESCRIBE {table}"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def get_query(query: str, cursor):
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def plot_timeseries(df: pd.DataFrame, column: str, title: str):
    fig, ax = plt.subplots()
    ax.plot_date(df[column], y=[1] * len(df[column]), alpha=0.5, ms=10)
    ax.set_alpha(0.5)
    fig.suptitle(title)
    plt.show()


def plot_hist(df: pd.DataFrame, column: str, title: str):
    fig, ax = plt.subplots()
    vals = df[column].astype(float)
    vals = vals.fillna(0)
    ax.hist(vals, alpha=0.5)
    ax.set_alpha(0.5)
    fig.suptitle(title)
    plt.show()


def main():
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    mydb = MySQLdb.connect(
        host="sansa.cs.uoregon.edu",
        port=3331,
        user=user,
        passwd=passwd,
        database=database,
    )
    mycursor = mydb.cursor()

    get_schema(mycursor, "pr")

    # get_query("show tables", cursor=mycursor)
    # get_query(
    #     query="select count(*) from pr where project_id=30", cursor=mycursor
    # )  # 30=anl_test_repo
    # get_query(query="select * from project", cursor=mycursor)
    # get_query(query="select * from pr where project_id=30", cursor=mycursor)

    print("All queries completed")

    df = pd.read_sql("select * from pr where project_id=30", mydb)
    # plot_timeseries(df=df, column="updated_at", title="Distribution of pull requests for project id 30.)

    df["updated_at_shift"] = df["updated_at"].shift(-1)
    df["time_difference"] = df["updated_at_shift"] - df["updated_at"]
    df["time_difference_hourly"] = df["time_difference"] / pd.Timedelta(hours=1)

    print(df["time_difference_hourly"])

    plot_hist(
        df=df,
        column="time_difference_hourly",
        title="Time difference on updated at columns.",
    )


if __name__ == "__main__":
    main()
