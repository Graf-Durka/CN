import csv
import re
import subprocess


DOMAINS = ["wikipedia.org", "yandex.ru", "github.com"]
OUTPUT_CSV = "results.csv"

def resolve_domain(domain):
    result = subprocess.run(["dig", "+short", domain], capture_output=True, text=True)
    ips = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return sorted(set(ips))

def trace_route(ip):
    proc = subprocess.run(
        ["traceroute", "-n", "-q", "1", "-w", "1", ip],
        capture_output=True, text=True
    )
    hop_pattern = re.compile(r"^(\d+)\s+(.*)$")
    rtt_pattern = re.compile(r"([0-9.]+)\s*ms")
    rows = []

    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue

        match = hop_pattern.match(line)
        if not match:
            continue

        hop, rest = match.groups()
        if rest.startswith("*"):
            rows.append({
                "hop": hop, "status": "timeout",
                "hop_address": "", "rtt_ms": "", "raw_line": line
            })
        else:
            hop_address = rest.split()[0]
            rtt_match = rtt_pattern.search(rest)
            rows.append({
                "hop": hop, "status": "ok",
                "hop_address": hop_address,
                "rtt_ms": rtt_match.group(1) if rtt_match else "",
                "raw_line": line
            })
    return rows

def main():
    all_rows = []
    for domain in DOMAINS:
        for ip in resolve_domain(domain):

            all_rows.append({
                "phase": "dns", "domain": domain, "ip": ip,
                "hop": "", "status": "resolved",
                "hop_address": "", "rtt_ms": "", "raw_line": ""
            })

            for hop_row in trace_route(ip):
                hop_row.update({"phase": "traceroute", "domain": domain, "ip": ip})
                all_rows.append(hop_row)

    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "phase", "domain", "ip", "hop", "status",
            "hop_address", "rtt_ms", "raw_line"
        ])
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Saved {len(all_rows)} rows to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()