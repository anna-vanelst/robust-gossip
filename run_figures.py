from plot.plot_rank_a import main as plot_rank_a
from plot.plot_rank_b import main as plot_rank_b
from plot.plot_rank_c import main as plot_rank_c
from plot.plot_trim import main as plot_trim
from plot.plot_trim_a import main as plot_trim_a
import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plot_name", type=str, required=True, help="Name of plot")
    args = parser.parse_args()
    plot_name = args.plot_name
    path = os.path.join("results", "figures")
    os.makedirs(path, exist_ok=True)

    if plot_name == "rank_a":
        plot_rank_a("exp2", save_path="plot_rank_a.pdf")  # watts-strogatz
    elif plot_name == "rank_a_appendix":
        exp_names = ["exp1", "exp2", "exp3"]  # for all graphs
        save_paths = [
            "plot_rank_a_complete.pdf",
            "plot_rank_a_ws.pdf",
            "plot_rank_a_grid.pdf",
        ]
        for exp_name, save_path in zip(exp_names, save_paths):
            plot_rank_a(exp_name, save_path)
    elif plot_name == "rank_b":
        exp_names = ["exp6", "exp5", "exp4"]
        # exp_names = ["exp33", "exp31", "exp32"]
        plot_rank_b(exp_names, save_path="plot_rank_b.pdf")
    elif plot_name == "rank_c":
        plot_rank_c("exp8", save_path="plot_rank_c.pdf")  # watts-strogatz
    elif plot_name == "rank_c_appendix":
        exp_names = ["exp7", "exp8", "exp9"]
        save_paths = [
            "plot_rank_c_ws.pdf",
            "plot_rank_c_grid.pdf",
            "plot_rank_c_complete.pdf",
        ]
        for exp_name, save_path in zip(exp_names, save_paths):
            plot_rank_c(exp_name, save_path)
    elif plot_name == "trim_a":
        plot_trim_a("exp10", save_path="plot_trim_a.pdf")
    elif plot_name == "trim_a_appendix":
        exp_names = ["exp10", "exp10a", "exp10b"]
        save_paths = [
            "plot_trim_a_ws.pdf",
            "plot_trim_a_grid.pdf",
            "plot_trim_a_complete.pdf",
        ]
        for exp_name, save_path in zip(exp_names, save_paths):
            plot_trim_a(exp_name, save_path)
    elif plot_name == "trim_b":
        plot_trim("exp12", save_path="plot_trim_b.pdf")
    elif plot_name == "trim_b_appendix":
        exp_names = ["exp11", "exp12", "exp13"]
        save_paths = [
            "plot_trim_b_complete.pdf",
            "plot_trim_b_grid.pdf",
            "plot_trim_b_ws.pdf",
        ]
        for exp_name, save_path in zip(exp_names, save_paths):
            plot_trim(exp_name, save_path)
    elif plot_name == "trim_c":
        plot_trim("exp14", save_path="plot_trim_c.pdf")
    elif plot_name == "rank_d_appendix":
        exp_names = ["exp15", "exp16", "exp17"]
        save_paths = [
            "plot_rank_d_ws.pdf",
            "plot_rank_d_complete.pdf",
            "plot_rank_d_grid.pdf",
        ]
        for exp_name, save_path in zip(exp_names, save_paths):
            plot_rank_c(exp_name, save_path)
    elif plot_name == "large_rank_c":
        exp_name = ["exp18", "exp19", "exp20"]
        save_path = [
            "plot_large_rank_c_ws.pdf",
            "plot_large_rank_c_grid.pdf",
            "plot_large_rank_c_complete.pdf",
        ]
        for name, path in zip(exp_name, save_path):
            plot_rank_c(name, save_path=path)
    elif plot_name == "xl_rank_c":
        exp_name = ["exp21", "exp22", "exp23"]
        save_path = [
            "plot_xl_rank_c_ws.pdf",
            "plot_xl_rank_c_grid.pdf",
            "plot_xl_rank_c_complete.pdf",
        ]
        for name, path in zip(exp_name, save_path):
            plot_rank_c(name, save_path=path)
    elif plot_name == "large_trim_c":
        exp_name = ["exp24", "exp25"]
        save_path = [
            "plot_large_trim_c_ws.pdf",
            "plot_large_trim_c_grid.pdf",
        ]
        for name, path in zip(exp_name, save_path):
            plot_trim(name, save_path=path)
    elif plot_name == "xl_trim_c":
        exp_name = ["exp26", "exp27"]
        save_path = [
            "plot_xl_trim_c_ws.pdf",
            "plot_xl_trim_c_grid.pdf",
        ]
        for name, path in zip(exp_name, save_path):
            plot_trim(name, save_path=path)
    elif plot_name == "xxl_rank_c":
        exp_name = "exp28"
        plot_name = "plot_xxl_rank_c.pdf"
        plot_rank_c(exp_name, save_path=plot_name)
    elif plot_name == "clustered":
        exp_name = "exp29"
        plot_name = "plot_clustered.pdf"
        plot_rank_c(exp_name, save_path=plot_name)
    elif plot_name == "sparse_rank":
        exp_names = ["exp33", "exp31", "exp32"]
        save_path = "plot_sparse_rank.pdf"
        plot_rank_b(exp_names, save_path=save_path)
    elif plot_name == "sparse_trim":
        exp_names = "exp36"
        save_path = "plot_sparse_trim.pdf"
        plot_trim(exp_names, save_path=save_path)


if __name__ == "__main__":
    main()
