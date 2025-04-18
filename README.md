This project aims to generate a high-fidelity dataset for training machine learning models to detect Distributed Denial-of-Service (DDoS) attacks. Traditional datasets are often outdated or lack realistic protocol distributions, so we are developing a hybrid approach that combines simulated attack traffic with authentic-looking normal traffic.

We have built a virtual web environment that simulates a functioning website with user interactions such as logins, API calls, and comment submissions. Normal traffic is generated using custom Python scripts that simulate diverse user agents, realistic sleep intervals (following normal distributions), and regionally clustered IP addresses, with a strong bias toward U.S.-based traffic.

On the attack side, we have implemented and tested multiple types of DDoS attacks including:

Bandwidth Flood: High-throughput data bursts targeting server bandwidth.

Packet Flood: Flooding with diverse protocols (TCP, ICMP, UDP) with IP/protocol/time variance.

Request Flood: HTTP(S) floods with realistic headers, randomized URIs, and varied methods (GET/POST).

Captured traffic is saved using tools like tcpdump, and the resulting pcap or CSV files are annotated for supervised learning. We are also incorporating autoencoders and variational autoencoders (VAEs) for anomaly detection and feature extraction from the generated traffic data.

The next steps include improving the balance and interleaving of normal and attack traffic, refining the ML models, and releasing labeled datasets for benchmarking.

