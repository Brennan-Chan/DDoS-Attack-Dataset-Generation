import random
import pandas as pd
import ace_tools as tools

# US-focused public IP ranges (approx)
us_ranges = [f"3.80.{i}.{j}" for i in range(0, 5) for j in range(1, 10)]  # Amazon EC2 US
us_ranges += [f"18.204.{i}.{j}" for i in range(0, 5) for j in range(1, 10)]  # AWS US

# English-speaking countries
ca_ranges = [f"99.232.{i}.{j}" for i in range(0, 2) for j in range(1, 10)]   # Canada (Rogers)
uk_ranges = [f"51.140.{i}.{j}" for i in range(0, 2) for j in range(1, 10)]   # UK (Azure)
au_ranges = [f"139.130.{i}.{j}" for i in range(0, 2) for j in range(1, 10)]  # Australia (Telstra)
nz_ranges = [f"202.27.{i}.{j}" for i in range(0, 1) for j in range(1, 10)]   # New Zealand (Spark)

# Mix with bias: 60% US, 30% other English-speaking, 10% global random (non-Ukraine)
us_ips = random.choices(us_ranges, k=60)
eng_ips = random.choices(ca_ranges + uk_ranges + au_ranges + nz_ranges, k=30)
global_safe_ips = [f"{a}.{b}.{c}.{d}" for a in range(23, 100) if a != 91  # exclude Ukraine (e.g., 91.*)
                   for b in range(1, 2) for c in range(1, 2) for d in range(1, 2)]
safe_global_ips = random.choices(global_safe_ips, k=10)

# Combine and shuffle
final_ips = us_ips + eng_ips + safe_global_ips
random.shuffle(final_ips)

# Display as DataFrame
df_ips = pd.DataFrame(final_ips, columns=["Simulated Public IPs"])
tools.display_dataframe_to_user(name="Diverse Simulated IPs", dataframe=df_ips)
