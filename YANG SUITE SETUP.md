YANG SUITE SETUP (15 minuten)
YANG Suite = GUI tool om YANG-modellen te exploreren + deploy
Stappen:
1. Browser → https://192.168.19.141:8443/yangtree/explore/
2. Add Device → CSR1000v (192.168.19.139, admin/123)
3. Create Repository → Cisco native models
4. Select YANG Set → cisco-ios-xe-native
5. Find Model → interfaces
6. Build XML payload
7. Deploy via NETCONF
8. Verify in CLI

HEB JE NODIG:
□ YANG Suite credentials:

Admin / 123
IP: 192.168.19.139
Port: 830 (NETCONF)

□ GitHub repo klaar:

https://github.com/Fedor-Goossens-pxl/lab-8-2-automation
XML configs voorbereid
Python scripts template

□ Tasks volgorde:

Task 1-5: Interface basics
Task 6-10: Loopback, routing
Task 11-20: Advanced config
Task 21+: Transactions

□ Git/SSH setup:

SSH key for GitHub
Git configured locally