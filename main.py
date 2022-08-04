import pandas as pd
import pulp

BUDGET = 100
POSITIONS = {
    "GK": 2,
    "D": 5,
    "M": 5,
    "F": 3,
}


def solver(df: pd.DataFrame) -> pulp.LpProblem:
    prob = pulp.LpProblem(sense=pulp.LpMaximize)

    # Initialise Variables
    picked = [pulp.LpVariable(str(i), cat="Binary") for i in range(len(df))]

    # Set objective
    prob += pulp.lpSum(v * p for v, p in zip(picked, df["Total"]))

    # Add constraints
    prob += pulp.lpSum(v * p for v, p in zip(picked, df["Price"])) <= BUDGET

    for position in POSITIONS:
        prob += (
            pulp.lpSum(v for v, p in zip(picked, df["Pos"]) if p == position)
            <= POSITIONS[position]
        )

    for team in df["Team"].unique():
        prob += (
            pulp.lpSum(v for v, t in zip(picked, df["Team"]) if t == team) <= 3
        )  # No more than 3 players can be selected from the same team

    prob.solve()

    return prob


def main():
    # Read and transform data
    df = pd.read_csv("FPL.csv")[["Player", "Team", "Pos", "Price", "Total"]]
    df["Price"] = df["Price"].str.replace("m", "").astype(float)

    prob = solver(df)
    print(df.iloc[[int(v.name) for v in prob.variables() if v.varValue]])


if __name__ == "__main__":
    main()
