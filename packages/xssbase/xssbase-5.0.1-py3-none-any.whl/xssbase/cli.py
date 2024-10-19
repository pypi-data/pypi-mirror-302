import argparse
from .xss import test_xss_payloads, load_payloads_from_file, is_valid_url, format_url

def main():
    parser = argparse.ArgumentParser(description='XSS Testing Tool')
    parser.add_argument('--url', required=True, help='Target URL to test for XSS vulnerabilities')
    parser.add_argument('--payload', help='Path to custom payload file (optional)')

    args = parser.parse_args()

    target = format_url(args.url)  # Format the URL

    if not is_valid_url(target):
        print("Invalid URL format. Please enter a valid URL.")
        return

    if args.payload:
        payloads = load_payloads_from_file(args.payload)
    else:
        payloads = load_payloads_from_file('xssbase/payload.txt')

    results = test_xss_payloads(target, payloads)

    for payload, link, vulnerable, status in results:
        if vulnerable:
            print(f"[VULNERABLE] Payload: {payload} | Link: {link} | Status Code: {status}")
        else:
            print(f"[NOT VULNERABLE] Tested Payload: {payload} | Link: {link} | Status Code: {status}")

if __name__ == "__main__":
    main()
