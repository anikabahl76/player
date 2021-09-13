from playeranalyze import get_player_data
import matplotlib.pyplot as plt

def organize_data_by_over(player_data):
    player_data["over"] = player_data["over"] + (player_data["ball"] / 6)
    player_data = player_data[["over", "total_runs"]]
    player_data[["over", "total_runs"]] = player_data.groupby("over",as_index=False).mean()
    player_data = player_data.dropna()
    return player_data

def plot_organized_data(player_data, player_name):
    fig1, ax1 = plt.subplots()
    plot = ax1.plot(player_data["over"], player_data["total_runs"])
    ax1.set_title(f"{player_name}'s runs over a T20 game")
    ax1.set_xlabel('Overs')
    ax1.set_ylabel('Runs')
    plt.show()
    return player_data

def plot_player_trends(player_name):
    plot_organized_data(organize_data_by_over(get_player_data(player_name)), player_name)
    return player_name