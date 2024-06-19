import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set initial balance and fixed deposit rate as mentioned in the problem statement
starting_balance = 100000
fixed_deposit_rate = 0.0006

# Get the file path from input
file_path = "daily_pnl.csv"

# Loading the CSV file
data = pd.read_csv(file_path, index_col=0, parse_dates=True, header=None)
data.columns = ['pnl']

# Calculating  the balance
data['balance'] = starting_balance + data['pnl'].cumsum()

# Identifying  trading days and calculate FD balance where assuming FD return on non trading days is zero
data['trading_day'] = data.index.weekday < 5
data['fd_rate'] = np.where(data['trading_day'], fixed_deposit_rate, 0)
data['fd_balance'] = starting_balance * (1 + data['fd_rate']).cumprod()

# Calculate drawdown with respect to FD
data['fd_drawdown'] = 1 - data['balance'] / data['fd_balance'].cummax()

# Calculate maximum drawdown with respect to FD
max_fd_drawdown = data['fd_drawdown'].max() * 100
print(f"Max Drawdown (w.r.t FD): {max_fd_drawdown:.2f}%")

# Calculate daily PnL percentage
data['pnl_pct'] = data['pnl'] / starting_balance * 100

# Identify drawdown days where daily PnL < FD return
data['drawdown_fd'] = data['pnl_pct'] < data['fd_rate'] * 100

# Calculate drawdown streaks
drawdown_streak = (data['drawdown_fd'].diff() != 0).cumsum()
drawdown_streak_counts = drawdown_streak[data['drawdown_fd']].value_counts()
max_drawdown_streak = drawdown_streak_counts.idxmax()
avg_drawdown_streak = drawdown_streak_counts.mean()
std_drawdown_streak = drawdown_streak_counts.std()
print(f"Max Drawdown Streak (based on daily PnL < FD return): {max_drawdown_streak} days")
print(f"Average Drawdown Streak: {avg_drawdown_streak:.2f} days")
print(f"Std Dev of Drawdown Streak: {std_drawdown_streak:.2f}")

# Calculate profit streaks
data['profit_day'] = data['pnl'] > 0
profit_streak = (data['profit_day'].diff() != 0).cumsum()
profit_streak_counts = profit_streak[data['profit_day']].value_counts()
max_profit_streak = profit_streak_counts.max()
avg_profit_streak = profit_streak_counts.mean()
std_profit_streak = profit_streak_counts.std()
print(f"Max Profit Streak: {max_profit_streak} days")
print(f"Average Profit Streak: {avg_profit_streak:.2f} days")
print(f"Std Dev of Profit Streak: {std_profit_streak:.2f}")

# Find the longest drawdown streak
drawdown_streaks = data[data['drawdown_fd']].groupby(drawdown_streak)
longest_streak = drawdown_streaks.get_group(max_drawdown_streak)
start_date = longest_streak.index.min()
end_date = longest_streak.index.max()
print(f"Longest Drawdown Streak: Start Date = {start_date}, End Date = {end_date}")

# Calculate maximum drawdown and drawdown streak up to each day
data['max_dd'] = (data['fd_drawdown'].cummax() * 100).round(4)
data['dds'] = data['drawdown_fd'].cumsum()

# Save the results to a CSV file
data[['pnl', 'max_dd', 'dds']].to_csv('output.csv')

# Format the output CSV file
output_data = pd.read_csv('output.csv', index_col=0)
output_data.index.name = 'date'
output_data.to_csv('formatted_output.csv')

# Plot the equity curve
fig, ax = plt.subplots(figsize=(12, 6))
data['balance'].plot(ax=ax)
ax.set_xlabel('Date')
ax.set_ylabel('Balance')
ax.set_title('Equity Curve')
ax.grid(True)
ax.text(0.05, 0.95, f"Max Drawdown: {max_fd_drawdown:.2f}%", transform=ax.transAxes, va='top')
plt.show()