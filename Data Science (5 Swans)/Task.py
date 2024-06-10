import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the daily PnL CSV file
pnl_df = pd.read_csv('daily_pnl.csv', header=None, names=['Date', 'PnL'])

# Convert the date column to datetime format
pnl_df['Date'] = pd.to_datetime(pnl_df['Date'])

# Assumptions
initial_balance = 100000  # Initial account balance
fd_rate = 0.01 / 100  # Daily fixed deposit rate (0.01%)

# Calculate the equity curve
pnl_df['Account Balance'] = initial_balance + pnl_df['PnL'].cumsum()

# Calculate FD growth
pnl_df['FD Growth'] = initial_balance * ((1 + fd_rate) ** np.arange(len(pnl_df)))

# Calculate peak balances
pnl_df['Peak Balance'] = pnl_df['Account Balance'].cummax()

# Drawdown logic considering FD rate
pnl_df['FD Threshold'] = initial_balance * (1 + fd_rate)
drawdown = []
drawdown_duration = []
current_dd_duration = 0

# Iterate over the dataframe to calculate the drawdown and duration with respect to FD
for i in range(len(pnl_df)):
    if pnl_df.loc[i, 'PnL'] < pnl_df.loc[i, 'FD Threshold'] - initial_balance:
        current_dd_duration += 1
        drawdown.append(pnl_df.loc[i, 'Account Balance'] - pnl_df.loc[i, 'Peak Balance'])
        drawdown_duration.append(current_dd_duration)
    else:
        current_dd_duration = 0
        drawdown.append(0)
        drawdown_duration.append(0)

pnl_df['Drawdown w.r.t FD'] = drawdown
pnl_df['Drawdown Duration w.r.t FD'] = drawdown_duration

# Maximum drawdown and drawdown duration with respect to FD
max_dd_fd = min(drawdown)  # Minimum value since drawdown is negative
max_dds_fd = max(drawdown_duration)

# Calculate profit streak stats
pnl_df['Profit Streak'] = pnl_df['PnL'].where(pnl_df['PnL'] > 0).groupby((pnl_df['PnL'] <= 0).cumsum()).cumcount()

# Output the results
print(f"Maximum Drawdown (w.r.t FD): {max_dd_fd:.2f}")
print(f"Maximum Drawdown Duration (DDS w.r.t FD): {max_dds_fd:.2f}")

drawdown_streaks = pnl_df['Drawdown Duration w.r.t FD'].value_counts()
profit_streaks = pnl_df['Profit Streak'].value_counts()

print("\nDrawdown Streak Stats:")
print(drawdown_streaks.describe())

print("\nProfit Streak Stats:")
print(profit_streaks.describe())

# Print intermediate values for debugging
print("\nDrawdown Streaks:")
print(drawdown_streaks)

print("\nProfit Streaks:")
print(profit_streaks)

# Plotting
plt.figure(figsize=(14, 7))

# Plot equity curve
plt.subplot(2, 1, 1)
plt.plot(pnl_df['Date'], pnl_df['Account Balance'], label='Equity Curve')
plt.plot(pnl_df['Date'], pnl_df['FD Growth'], label='FD Growth', linestyle='--')
plt.title('Equity Curve and FD Growth')
plt.xlabel('Date')
plt.ylabel('Account Balance')
plt.legend()

# Plot drawdown
plt.subplot(2, 1, 2)
plt.plot(pnl_df['Date'], pnl_df['Drawdown w.r.t FD'], label='Drawdown w.r.t FD')
plt.title('Drawdown w.r.t FD')
plt.xlabel('Date')
plt.ylabel('Drawdown')
plt.axhline(0, color='gray', linestyle='--')
plt.legend()

plt.tight_layout()
plt.show()

# Plotting streak stats
plt.figure(figsize=(14, 7))

# Drawdown streaks
plt.subplot(2, 1, 1)
plt.hist(drawdown_streaks, bins=20, edgecolor='k', alpha=0.7)
plt.title('Drawdown Streak Duration')
plt.xlabel('Days')
plt.ylabel('Frequency')

# Profit streaks
plt.subplot(2, 1, 2)
plt.hist(profit_streaks, bins=20, edgecolor='k', alpha=0.7)
plt.title('Profit Streak Duration')
plt.xlabel('Days')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()
